"""Command-line interface for the password manager."""

from __future__ import annotations

import argparse
import getpass
import json
import sys
from pathlib import Path

from . import core
from .storage import (
    Vault, History,
    backup_vault, restore_vault, export_vault, import_vault,
)


BANNER = "🔐 ENTERPRISE PASSWORD MANAGER v3.0 🔐"


# ---------- Helpers ----------
def _prompt_master(confirm: bool = False) -> str:
    pw = getpass.getpass("Master password: ")
    if confirm:
        again = getpass.getpass("Confirm master password: ")
        if pw != again:
            print("❌ Passwords do not match")
            sys.exit(1)
    return pw


def _load_vault(args) -> Vault:
    v = Vault(path=args.vault, keyfile=args.keyfile)
    if not v.path.exists():
        master = _prompt_master(confirm=True)
    else:
        master = _prompt_master()
    try:
        v.unlock(master)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    return v


# ---------- Sub-commands ----------
def cmd_generate(args) -> int:
    # Build generation options from flags
    options = {
        "length": args.length,
        "uppercase": args.uppercase,
        "lowercase": args.lowercase,
        "digits": args.digits,
        "specials": args.specials,
        "exclude_ambiguous": args.exclude_ambiguous,
        "exclude_similar": args.exclude_similar,
    }

    if args.memorable:
        pw = core.generate_memorable(
            words=args.words, separator=args.separator,
        )
    elif args.pattern:
        pw = core.generate_pattern(args.pattern)
    elif args.pin:
        pw = core.generate_pin(args.length)
    elif args.pronounceable:
        pw = core.generate_pronounceable(args.length)
    elif args.count > 1:
        passwords = core.batch_generate(args.count, **options)
        print(f"🔑 Generated {len(passwords)} passwords:")
        for i, p in enumerate(passwords, 1):
            print(f"{i}. \"{p}\"")
        return 0
    else:
        pw = core.generate_random(**options)

    strength = core.check_strength(pw)
    entropy = core.get_entropy(pw)

    print(f"🔑 Generated Password: \"{pw}\"")
    print(f"Strength: {strength['score']}/100 ({strength['label']})")
    print(f"Entropy: {entropy} bits")
    print(f"Estimated crack time: {core.estimate_crack_time(pw)}")

    # Log to history
    hist = History(path=args.history)
    hist.log_generation(pw, strength["score"])
    return 0


def cmd_strength(args) -> int:
    pw = args.password
    if not pw:
        pw = getpass.getpass("Password to analyze: ")
    report = core.check_strength(pw)
    print(f"Password Strength: {report['label']} ({report['score']}/100)")
    if report["issues"]:
        print("Issues:")
        for i, issue in enumerate(report["issues"], 1):
            print(f"{i}. {issue}")
    if report["improvements"]:
        print("Improvements:")
        for imp in report["improvements"]:
            print(f"- {imp}")
    return 0


def cmd_vault(args) -> int:
    vault = _load_vault(args)

    if args.action == "add":
        if not (args.service and args.username):
            print("❌ --service and --username are required")
            return 1
        pw = args.password or getpass.getpass("Password to store: ")
        vault.add_entry(args.service, args.username, pw)
        print(f"✅ Added entry for '{args.service}' to vault")
        return 0

    if args.action == "get":
        entry = vault.get_entry(args.service)
        if not entry:
            print(f"❌ No entry for '{args.service}'")
            return 1
        print(f"Service: {args.service}")
        print(f"Username: {entry['username']}")
        print(f"Password: {entry['password']}")
        print(f"Strength: {entry['strength']}/100")
        print(f"Last modified: {entry['modified']}")
        return 0

    if args.action == "list":
        names = vault.list_entries()
        if not names:
            print("📦 Vault is empty")
            return 0
        print(f"📦 Password Vault ({len(names)} entries)")
        for i, name in enumerate(names, 1):
            user = vault.get_entry(name)["username"]
            print(f"{i}. {name} ({user})")
        return 0

    if args.action == "delete":
        if vault.delete_entry(args.service):
            print(f"✅ Deleted entry for '{args.service}'")
            return 0
        print(f"❌ No entry for '{args.service}'")
        return 1

    if args.action == "search":
        results = vault.search(args.service or "")
        if not results:
            print("No matches")
            return 0
        for name in results:
            print(name)
        return 0

    if args.action == "stats":
        stats = vault.stats()
        print("📊 VAULT STATISTICS")
        print(f"Total entries: {stats['total']}")
        print(f"Average strength: {stats['avg_strength']}/100")
        print(f"Weak passwords: {stats['weak']}")
        print(f"Unique services: {stats['unique']}")
        return 0

    if args.action == "clear":
        confirm = input("⚠️ WARNING: This will permanently delete ALL "
                        "passwords!\nConfirm? (y/n): ").strip().lower()
        if confirm == "y":
            vault.clear()
            print("✅ Vault cleared")
        else:
            print("Cancelled")
        return 0

    print("Unknown vault action")
    return 1


def cmd_history(args) -> int:
    hist = History(path=args.history)
    if args.action == "list":
        items = hist.get_history(limit=args.limit)
        if not items:
            print("No history yet")
            return 0
        for i, item in enumerate(items, 1):
            print(f"{i}. {item['hash']} | strength={item['strength']} "
                  f"| len={item['length']} | {item['timestamp']}")
        return 0
    if args.action == "stats":
        print(json.dumps(hist.get_stats(), indent=2))
        return 0
    if args.action == "export":
        out = hist.export_history(args.output or "history_export.json")
        print(f"✅ Exported history to {out}")
        return 0
    return 1


def cmd_backup(args) -> int:
    vault = _load_vault(args)

    if args.action == "backup":
        out = backup_vault(vault, args.filename or "vault_backup.enc")
        print(f"✅ Vault backed up to {out} (encrypted)")
        return 0
    if args.action == "restore":
        if not args.filename:
            print("❌ --filename required")
            return 1
        restore_vault(vault, args.filename)
        print(f"✅ Vault restored from {args.filename}")
        return 0
    if args.action == "export":
        out = export_vault(vault, args.filename or "vault_export.json")
        print(f"⚠️ Vault exported in PLAINTEXT to {out}")
        print("   Delete this file when you're done with it.")
        return 0
    if args.action == "import":
        if not args.filename:
            print("❌ --filename required")
            return 1
        n = import_vault(vault, args.filename)
        print(f"✅ Imported {n} entries")
        return 0
    return 1


# ---------- Parser ----------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="password-manager", description=BANNER)
    p.add_argument("--vault", default="vault.enc", help="Vault file path")
    p.add_argument("--keyfile", default=None,
                   help="Optional key file (2nd factor)")
    p.add_argument("--history", default="history.json",
                   help="History file path")
    sub = p.add_subparsers(dest="command", required=True)

    # generate
    g = sub.add_parser("generate", help="Generate a password")
    g.add_argument("--length", type=int, default=16)
    g.add_argument("--count", type=int, default=1)
    g.add_argument("--uppercase", action="store_true")
    g.add_argument("--lowercase", action="store_true")
    g.add_argument("--digits", action="store_true")
    g.add_argument("--specials", action="store_true")
    g.add_argument("--exclude-ambiguous", action="store_true")
    g.add_argument("--exclude-similar", action="store_true")
    g.add_argument("--memorable", action="store_true")
    g.add_argument("--words", type=int, default=4)
    g.add_argument("--separator", default="-")
    g.add_argument("--pattern", default=None)
    g.add_argument("--pin", action="store_true")
    g.add_argument("--pronounceable", action="store_true")

    # strength
    s = sub.add_parser("strength", help="Analyze password strength")
    s.add_argument("password", nargs="?", default=None)

    # vault
    v = sub.add_parser("vault", help="Manage the password vault")
    v.add_argument("action",
                   choices=["add", "get", "list", "delete", "search",
                            "stats", "clear"])
    v.add_argument("--service", default=None)
    v.add_argument("--username", default=None)
    v.add_argument("--password", default=None)

    # history
    h = sub.add_parser("history", help="View or export generation history")
    h.add_argument("action", choices=["list", "stats", "export"])
    h.add_argument("--limit", type=int, default=20)
    h.add_argument("--output", default=None)

    # backup
    b = sub.add_parser("backup", help="Backup / restore / export / import")
    b.add_argument("action",
                   choices=["backup", "restore", "export", "import"])
    b.add_argument("--filename", default=None)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    print(BANNER)
    print()

    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "strength":
        return cmd_strength(args)
    if args.command == "vault":
        return cmd_vault(args)
    if args.command == "history":
        return cmd_history(args)
    if args.command == "backup":
        return cmd_backup(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())