"""High-level organization actions."""

from __future__ import annotations

import shutil
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from .scanner import (
    categorize, size_label, human_size, iter_files,
    TYPE_CATEGORIES, SIZE_CATEGORIES,
)
from .rules import RuleEngine


# ---------- Helpers ----------
def _unique(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    i = 1
    while True:
        cand = path.parent / f"{stem}_{i}{suffix}"
        if not cand.exists():
            return cand
        i += 1


def _plan_moves(root: Path, classify) -> dict[str, list[tuple[Path, Path]]]:
    """Return {folder: [(src, dst), ...]} without touching the FS."""
    plan: dict[str, list[tuple[Path, Path]]] = defaultdict(list)
    for p in iter_files(root):
        folder = classify(p)
        if folder is None:
            continue
        target_dir = root / folder
        if p.parent == target_dir:
            continue
        plan[folder].append((p, target_dir / p.name))
    return dict(plan)


def _execute(plan: dict[str, list[tuple[Path, Path]]]) -> dict:
    moved = 0
    by_folder: dict[str, int] = {}
    for folder, pairs in plan.items():
        target_dir = None
        for src, dst in pairs:
            target_dir = dst.parent
            target_dir.mkdir(parents=True, exist_ok=True)
            dst = _unique(dst)
            shutil.move(str(src), str(dst))
            moved += 1
        by_folder[folder] = len(pairs)
    return {"moved": moved, "folders": by_folder}


# ---------- Preview ----------
def preview_organization(directory: str | Path, mode: str = "type") -> dict:
    root = Path(directory)
    if mode == "type":
        classify = lambda p: categorize(p)
    elif mode == "date":
        classify = lambda p: datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m")
    elif mode == "size":
        classify = lambda p: size_label(p.stat().st_size)
    else:
        raise ValueError(f"Unknown mode: {mode}")

    plan = _plan_moves(root, classify)
    return {
        folder: [str(src.relative_to(root)) for src, _ in pairs]
        for folder, pairs in plan.items()
    }


# ---------- organize_by_type ----------
def organize_by_type(directory: str | Path, dry_run: bool = False) -> dict:
    root = Path(directory)
    plan = _plan_moves(root, lambda p: categorize(p))
    if dry_run:
        return {
            "dry_run": True,
            "plan": {f: [str(s.relative_to(root)) for s, _ in v]
                     for f, v in plan.items()},
            "total": sum(len(v) for v in plan.values()),
        }
    return _execute(plan)


# ---------- organize_by_date ----------
def organize_by_date(directory: str | Path, fmt: str = "%Y-%m",
                     dry_run: bool = False) -> dict:
    root = Path(directory)
    plan = _plan_moves(
        root,
        lambda p: datetime.fromtimestamp(p.stat().st_mtime).strftime(fmt),
    )
    if dry_run:
        return {
            "dry_run": True,
            "plan": {f: [str(s.relative_to(root)) for s, _ in v]
                     for f, v in plan.items()},
            "total": sum(len(v) for v in plan.values()),
        }
    return _execute(plan)


# ---------- organize_by_size ----------
def organize_by_size(directory: str | Path, dry_run: bool = False) -> dict:
    root = Path(directory)
    plan = _plan_moves(root, lambda p: size_label(p.stat().st_size))
    if dry_run:
        return {
            "dry_run": True,
            "plan": {f: [str(s.relative_to(root)) for s, _ in v]
                     for f, v in plan.items()},
            "total": sum(len(v) for v in plan.values()),
        }
    return _execute(plan)


# ---------- organize_by_custom_rules ----------
def organize_by_custom_rules(directory: str | Path,
                             rules_file: str | Path,
                             dry_run: bool = False) -> list[dict]:
    engine = RuleEngine()
    engine.load(rules_file)
    return engine.apply_all(directory, dry_run=dry_run)


# ---------- Batch rename ----------
def rename_batch(directory: str | Path, pattern: str,
                 start: int = 1, dry_run: bool = False) -> list[dict]:
    """
    Rename files in a directory using a pattern with {n}, {name}, {ext}.
    Example: 'photo_{n:03d}{ext}'
    """
    root = Path(directory)
    results: list[dict] = []
    files = sorted([p for p in root.iterdir() if p.is_file()])
    for i, p in enumerate(files, start):
        new_name = pattern.format(n=i, name=p.stem, ext=p.suffix)
        target = p.parent / new_name
        if target == p:
            continue
        target = _unique(target)
        results.append({"src": str(p), "dst": str(target)})
        if not dry_run:
            p.rename(target)
    return results


def add_prefix(directory: str | Path, prefix: str,
               dry_run: bool = False) -> list[dict]:
    root = Path(directory)
    results: list[dict] = []
    for p in sorted(root.iterdir()):
        if not p.is_file() or p.name.startswith(prefix):
            continue
        target = _unique(p.parent / (prefix + p.name))
        results.append({"src": str(p), "dst": str(target)})
        if not dry_run:
            p.rename(target)
    return results