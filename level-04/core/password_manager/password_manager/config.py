"""Configuration and wordlist loading."""

from __future__ import annotations

import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

DEFAULT_WORDS = [
    "tiger", "sunset", "crystal", "mountain", "river", "forest", "ocean",
    "silver", "golden", "thunder", "winter", "summer", "phantom", "shadow",
    "falcon", "raven", "wolf", "dragon", "phoenix", "cosmic", "nebula",
    "guitar", "piano", "violin", "coffee", "chocolate", "vanilla", "cinnamon",
    "harbor", "meadow", "canyon", "desert", "island", "garden", "temple",
    "sapphire", "emerald", "diamond", "ruby", "amber", "jade",
    "compass", "lantern", "anchor", "beacon", "bridge", "castle",
]

DEFAULT_CONFIG = {
    "vault_file": "vault.enc",
    "history_file": "history.json",
    "wordlist_file": "words.txt",
    "default_length": 16,
    "default_words": 4,
    "default_separator": "-",
}


def load_config(path: str | Path | None = None) -> dict:
    if path is None:
        path = DATA_DIR / "config.json"
    cfg = dict(DEFAULT_CONFIG)
    p = Path(path)
    if p.exists():
        try:
            cfg.update(json.loads(p.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            pass
    return cfg


def load_words(path: str | Path | None = None) -> list[str]:
    if path is None:
        path = DATA_DIR / "words.txt"
    p = Path(path)
    if not p.exists():
        return list(DEFAULT_WORDS)
    words = [
        line.strip().lower()
        for line in p.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    return words or list(DEFAULT_WORDS)