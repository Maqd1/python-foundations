# config.py
"""Configuration loading and environment-specific config."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_ENV = "development"


def load_json(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_config(path: str | Path, env: str | None = None) -> dict:
    """
    Load base config and merge env-specific overrides.

    Expected layout:
        {
            "database": {...},
            "logging": {...},
            "environments": {
                "development": {"database": {"url": "...dev"}},
                "production":  {"database": {"url": "...prod"}}
            }
        }
    """
    data = load_json(path)
    env = env or os.getenv("APP_ENV", DEFAULT_ENV)
    env_overrides = data.pop("environments", {}).get(env, {})
    return _deep_merge(data, env_overrides)


def load_env_config(directory: str | Path, env: str | None = None) -> dict:
    """Load config.json plus optional config.<env>.json from a directory."""
    directory = Path(directory)
    env = env or os.getenv("APP_ENV", DEFAULT_ENV)

    base = load_json(directory / "config.json")
    env_file = directory / f"config.{env}.json"
    if env_file.exists():
        base = _deep_merge(base, load_json(env_file))
    return base


def _deep_merge(a: dict, b: dict) -> dict:
    out = dict(a)
    for k, v in b.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


# ---------- Test doubles (for override examples) ----------
class FakeDatabase:
    def __init__(self, url: str = "sqlite://:memory:"):
        self.url = url
        self.queries: list[str] = []

    def query(self, sql: str):
        self.queries.append(sql)
        return {"id": 1, "name": "TestUser"}


class FakeLogger:
    def __init__(self):
        self.messages: list[str] = []

    def info(self, msg: str):
        self.messages.append(msg)