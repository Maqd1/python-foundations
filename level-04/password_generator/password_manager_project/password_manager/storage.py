"""Encrypted vault, history, and backup/restore."""

from __future__ import annotations

import base64
import getpass
import hashlib
import json
import os
import shutil
from datetime import datetime
from pathlib import Path

from .core import check_strength

# Optional crypto: use `cryptography` if available, otherwise fall back
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    _HAS_CRYPTO = True
except ImportError:
    _HAS_CRYPTO = False


# ---------- Simple obfuscation fallback (NOT secure — warn the user) ----------
def _fallback_key(master: str) -> bytes:
    return hashlib.sha256(master.encode()).digest()


def _fallback_encrypt(data: bytes, master: str) -> bytes:
    key = _fallback_key(master)
    out = bytearray()
    for i, b in enumerate(data):
        out.append(b ^ key[i % len(key)])
    return base64.b64encode(bytes(out))


def _fallback_decrypt(data: bytes, master: str) -> bytes:
    key = _fallback_key(master)
    raw = base64.b64decode(data)
    out = bytearray()
    for i, b in enumerate(raw):
        out.append(b ^ key[i % len(key)])
    return bytes(out)


def _derive_fernet_key(master: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(master.encode()))


# ---------- Vault ----------
class Vault:
    """Encrypted JSON vault of {service: {username, password, ...}}."""

    def __init__(self, path: str | Path = "vault.enc", keyfile: str | Path | None = None):
        self.path = Path(path)
        self.keyfile = Path(keyfile) if keyfile else None
        self._entries: dict = {}
        self._master: str | None = None

    # ---- master password / key file ----
    def _read_keyfile(self) -> str:
        if not self.keyfile or not self.keyfile.exists():
            return ""
        return self.keyfile.read_text(encoding="utf-8").strip()

    def _compose_secret(self, master: str) -> str:
        # Multi-factor: master password + optional key file
        return master + "|" + self._read_keyfile()

    # ---- low-level file I/O ----
    def _write_file(self, plaintext: bytes, master: str) -> None:
        secret = self._compose_secret(master)
        if _HAS_CRYPTO:
            salt = os.urandom(16)
            key = _derive_fernet_key(secret, salt)
            token = Fernet(key).encrypt(plaintext)
            payload = {"v": 2, "salt": base64.b64encode(salt).decode(),
                       "data": token.decode()}
            self.path.write_bytes(json.dumps(payload).encode())
        else:
            self.path.write_bytes(_fallback_encrypt(plaintext, secret))

    def _read_file(self, master: str) -> bytes:
        secret = self._compose_secret(master)
        raw = self.path.read_bytes()
        if _HAS_CRYPTO:
            try:
                payload = json.loads(raw)
                salt = base64.b64decode(payload["salt"])
                key = _derive_fernet_key(secret, salt)
                return Fernet(key).decrypt(payload["data"].encode())
            except Exception as e:
                raise ValueError("Invalid master password or corrupted vault") from e
        return _fallback_decrypt(raw, secret)

    # ---- public API ----
    def unlock(self, master: str) -> None:
        """Open (or create) the vault with a master password."""
        self._master = master
        if self.path.exists():
            data = self._read_file(master)
            try:
                self._entries = json.loads(data)
            except json.JSONDecodeError as e:
                raise ValueError("Vault is corrupted") from e
        else:
            self._entries = {}

    def _save(self) -> None:
        if self._master is None:
            raise RuntimeError("Vault is locked")
        blob = json.dumps(self._entries, indent=2).encode()
        self._write_file(blob, self._master)

    def add_entry(self, service: str, username: str, password: str) -> dict:
        if self._master is None:
            raise RuntimeError("Unlock the vault first")
        entry = {
            "username": username,
            "password": password,
            "strength": check_strength(password)["score"],
            "created": datetime.now().isoformat(timespec="seconds"),
            "modified": datetime.now().isoformat(timespec="seconds"),
        }
        self._entries[service] = entry
        self._save()
        return entry

    def get_entry(self, service: str) -> dict | None:
        return self._entries.get(service)

    def delete_entry(self, service: str) -> bool:
        if service in self._entries:
            del self._entries[service]
            self._save()
            return True
        return False

    def list_entries(self) -> list[str]:
        return sorted(self._entries.keys())

    def search(self, query: str) -> list[str]:
        q = query.lower()
        return [s for s in self._entries if q in s.lower()]

    def clear(self) -> None:
        self._entries = {}
        self._save()

    def stats(self) -> dict:
        if not self._entries:
            return {"total": 0, "avg_strength": 0, "weak": 0,
                    "services": [], "unique": 0}
        scores = [e["strength"] for e in self._entries.values()]
        weak = sum(1 for s in scores if s < 50)
        return {
            "total": len(self._entries),
            "avg_strength": round(sum(scores) / len(scores), 1),
            "weak": weak,
            "services": sorted(self._entries.keys()),
            "unique": len(self._entries),
        }

    def is_unlocked(self) -> bool:
        return self._master is not None

    def entries(self) -> dict:
        """Read-only-ish view of the entries (used by backup/export)."""
        return dict(self._entries)

    def load_entries(self, data: dict) -> None:
        """Replace entries (used by import/restore)."""
        self._entries = dict(data)
        if self._master is not None:
            self._save()


# ---------- History ----------
class History:
    """JSON log of generated passwords (only hashes and metadata)."""

    def __init__(self, path: str | Path = "history.json"):
        self.path = Path(path)
        if self.path.exists():
            try:
                self._items: list[dict] = json.loads(
                    self.path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self._items = []
        else:
            self._items = []

    def _save(self) -> None:
        self.path.write_text(json.dumps(self._items, indent=2), encoding="utf-8")

    def log_generation(self, password: str, strength: int) -> dict:
        entry = {
            "hash": hashlib.sha256(password.encode()).hexdigest()[:16],
            "strength": strength,
            "length": len(password),
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        self._items.append(entry)
        self._save()
        return entry

    def get_history(self, limit: int | None = None) -> list[dict]:
        items = list(reversed(self._items))
        return items if limit is None else items[:limit]

    def get_stats(self) -> dict:
        if not self._items:
            return {"count": 0}
        strengths = [i["strength"] for i in self._items]
        lengths = [i["length"] for i in self._items]
        return {
            "count": len(self._items),
            "avg_strength": round(sum(strengths) / len(strengths), 1),
            "avg_length": round(sum(lengths) / len(lengths), 1),
            "max_strength": max(strengths),
            "min_strength": min(strengths),
            "last_generated": self._items[-1]["timestamp"],
        }

    def export_history(self, filename: str | Path) -> Path:
        out = Path(filename)
        out.write_text(json.dumps(self._items, indent=2), encoding="utf-8")
        return out


# ---------- Backup / restore ----------
def backup_vault(vault: Vault, filename: str | Path) -> Path:
    """Copy the encrypted vault file as-is."""
    if not vault.path.exists():
        raise FileNotFoundError("Vault file does not exist yet")
    out = Path(filename)
    shutil.copy2(vault.path, out)
    return out


def restore_vault(vault: Vault, filename: str | Path,
                  master: str | None = None) -> None:
    """Replace the current vault file with a backup copy."""
    src = Path(filename)
    if not src.exists():
        raise FileNotFoundError(src)
    vault.path.write_bytes(src.read_bytes())
    if master is not None:
        vault.unlock(master)


def export_vault(vault: Vault, filename: str | Path) -> Path:
    """⚠️ Export decrypted vault to JSON. Only for migration."""
    out = Path(filename)
    out.write_text(json.dumps(vault.entries(), indent=2), encoding="utf-8")
    return out


def import_vault(vault: Vault, filename: str | Path) -> int:
    """Import entries from a JSON export. Returns count imported."""
    data = json.loads(Path(filename).read_text(encoding="utf-8"))
    vault.load_entries(data)
    return len(data)