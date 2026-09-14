"""Rule engine and file watcher."""

from __future__ import annotations

import json
import re
import shutil
import time
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from .scanner import (
    categorize, human_size, size_label,
    TYPE_CATEGORIES, SIZE_CATEGORIES,
)


# ---------- Conditions ----------
class Condition:
    """Base class for rule conditions."""

    def matches(self, path: Path, info: dict) -> bool:
        raise NotImplementedError

    @staticmethod
    def from_dict(data: dict) -> "Condition":
        kind = data.get("type", "").lower()
        if kind == "extension":
            return ExtensionCondition(data["value"])
        if kind == "size":
            return SizeCondition(data.get("op", ">"), data["value"])
        if kind == "date":
            return DateCondition(data.get("op", ">"), data["value"])
        if kind == "name":
            return NameCondition(data.get("op", "contains"), data["value"])
        if kind == "category":
            return CategoryCondition(data["value"])
        raise ValueError(f"Unknown condition type: {kind}")


class ExtensionCondition(Condition):
    def __init__(self, extensions: str | list[str]):
        if isinstance(extensions, str):
            extensions = [extensions]
        self.extensions = {e.lower() if e.startswith(".") else f".{e.lower()}"
                           for e in extensions}

    def matches(self, path: Path, info: dict) -> bool:
        return path.suffix.lower() in self.extensions


class SizeCondition(Condition):
    """value is in bytes. op: >, <, >=, <=, ==."""

    def __init__(self, op: str, value: int):
        self.op = op
        self.value = value

    def matches(self, path: Path, info: dict) -> bool:
        size = info.get("size", path.stat().st_size)
        return {
            ">":  size >  self.value,
            "<":  size <  self.value,
            ">=": size >= self.value,
            "<=": size <= self.value,
            "==": size == self.value,
        }.get(self.op, False)


class DateCondition(Condition):
    """value: ISO date string, e.g. '2024-01-01'. op: >, <."""

    def __init__(self, op: str, value: str):
        self.op = op
        self.value = datetime.fromisoformat(value)

    def matches(self, path: Path, info: dict) -> bool:
        try:
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
        except OSError:
            return False
        return mtime > self.value if self.op == ">" else mtime < self.value


class NameCondition(Condition):
    """op: contains, starts, ends, regex."""

    def __init__(self, op: str, value: str):
        self.op = op
        self.value = value

    def matches(self, path: Path, info: dict) -> bool:
        name = path.name.lower()
        v = self.value.lower()
        if self.op == "contains":
            return v in name
        if self.op == "starts":
            return name.startswith(v)
        if self.op == "ends":
            return name.endswith(v)
        if self.op == "regex":
            return bool(re.search(self.value, path.name))
        return False


class CategoryCondition(Condition):
    def __init__(self, category: str):
        self.category = category

    def matches(self, path: Path, info: dict) -> bool:
        return categorize(path) == self.category


# ---------- Actions ----------
class RuleAction:
    """Base action."""

    def apply(self, path: Path, context: dict, dry_run: bool = False) -> dict:
        raise NotImplementedError

    @staticmethod
    def from_dict(data: dict) -> "RuleAction":
        kind = data.get("type", "").lower()
        if kind == "move":
            return MoveAction(data["destination"])
        if kind == "copy":
            return CopyAction(data["destination"])
        if kind == "rename":
            return RenameAction(data.get("pattern", "{name}{ext}"))
        if kind == "delete":
            return DeleteAction()
        if kind == "archive":
            return ArchiveAction(data.get("destination", "Archives"))
        raise ValueError(f"Unknown action type: {kind}")


def _unique(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    i = 1
    while True:
        candidate = path.parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


class MoveAction(RuleAction):
    def __init__(self, destination: str):
        self.destination = destination

    def apply(self, path: Path, context: dict, dry_run: bool = False) -> dict:
        root: Path = context["root"]
        target_dir = Path(self.destination)
        if not target_dir.is_absolute():
            target_dir = root / target_dir
        target = _unique(target_dir / path.name)
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))
        return {"action": "move", "src": str(path), "dst": str(target)}


class CopyAction(RuleAction):
    def __init__(self, destination: str):
        self.destination = destination

    def apply(self, path: Path, context: dict, dry_run: bool = False) -> dict:
        root: Path = context["root"]
        target_dir = Path(self.destination)
        if not target_dir.is_absolute():
            target_dir = root / target_dir
        target = _unique(target_dir / path.name)
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(path), str(target))
        return {"action": "copy", "src": str(path), "dst": str(target)}


class RenameAction(RuleAction):
    def __init__(self, pattern: str):
        self.pattern = pattern

    def apply(self, path: Path, context: dict, dry_run: bool = False) -> dict:
        new_name = self.pattern.format(
            name=path.stem, ext=path.suffix,
            date=datetime.now().strftime("%Y%m%d"),
            n=context.get("counter", 0),
        )
        target = _unique(path.parent / new_name)
        if not dry_run:
            path.rename(target)
        return {"action": "rename", "src": str(path), "dst": str(target)}


class DeleteAction(RuleAction):
    def apply(self, path: Path, context: dict, dry_run: bool = False) -> dict:
        if not dry_run:
            try:
                path.unlink()
            except OSError as e:
                return {"action": "delete", "src": str(path), "error": str(e)}
        return {"action": "delete", "src": str(path)}


class ArchiveAction(RuleAction):
    def __init__(self, destination: str = "Archives"):
        self.destination = destination

    def apply(self, path: Path, context: dict, dry_run: bool = False) -> dict:
        root: Path = context["root"]
        target_dir = Path(self.destination)
        if not target_dir.is_absolute():
            target_dir = root / target_dir
        archive = _unique(target_dir / (path.stem + ".zip"))
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
                zf.write(path, path.name)
            path.unlink()
        return {"action": "archive", "src": str(path), "dst": str(archive)}


# ---------- Rule ----------
@dataclass
class Rule:
    name: str
    conditions: list[Condition]
    action: RuleAction
    logic: str = "all"        # "all" | "any"
    enabled: bool = True

    @staticmethod
    def from_dict(data: dict) -> "Rule":
        conds = [Condition.from_dict(c) for c in data.get("conditions", [])]
        return Rule(
            name=data["name"],
            conditions=conds,
            action=RuleAction.from_dict(data["action"]),
            logic=data.get("logic", "all"),
            enabled=data.get("enabled", True),
        )

    def matches(self, path: Path, info: dict) -> bool:
        if not self.conditions:
            return False
        if self.logic == "any":
            return any(c.matches(path, info) for c in self.conditions)
        return all(c.matches(path, info) for c in self.conditions)

    def apply(self, path: Path, context: dict, dry_run: bool = False) -> dict:
        return self.action.apply(path, context, dry_run=dry_run)


# ---------- Rule engine ----------
class RuleEngine:
    def __init__(self, rules: list[Rule] | None = None):
        self.rules: list[Rule] = list(rules or [])

    def add_rule(self, name: str, conditions: list[dict],
                 action: dict, logic: str = "all") -> Rule:
        rule = Rule(
            name=name,
            conditions=[Condition.from_dict(c) for c in conditions],
            action=RuleAction.from_dict(action),
            logic=logic,
        )
        self.rules.append(rule)
        return rule

    def load(self, filename: str | Path) -> int:
        data = json.loads(Path(filename).read_text(encoding="utf-8"))
        rules = data.get("rules", data) if isinstance(data, dict) else data
        for r in rules:
            self.rules.append(Rule.from_dict(r))
        return len(rules)

    def evaluate(self, path: Path, info: dict | None = None) -> Rule | None:
        info = info or {}
        for r in self.rules:
            if r.enabled and r.matches(path, info):
                return r
        return None

    def apply_all(self, directory: str | Path,
                  dry_run: bool = False) -> list[dict]:
        from .scanner import iter_files
        root = Path(directory)
        results: list[dict] = []
        counter = 0
        for p in list(iter_files(root)):
            rule = self.evaluate(p)
            if rule is None:
                continue
            counter += 1
            res = rule.apply(p, {"root": root, "counter": counter},
                             dry_run=dry_run)
            res["rule"] = rule.name
            results.append(res)
        return results


def load_rules(filename: str | Path) -> RuleEngine:
    engine = RuleEngine()
    engine.load(filename)
    return engine


def evaluate_rules(path: str | Path, rules: RuleEngine | list[Rule]) -> Rule | None:
    if isinstance(rules, RuleEngine):
        return rules.evaluate(Path(path))
    engine = RuleEngine(rules)
    return engine.evaluate(Path(path))


# ---------- Watcher ----------
class FileWatcher:
    """
    Polling-based directory watcher (no external deps).
    For production use, prefer the `watchdog` library.
    """

    def __init__(self, directory: str | Path, engine: RuleEngine,
                 interval: float = 1.0):
        self.root = Path(directory)
        self.engine = engine
        self.interval = interval
        self._seen: dict[str, float] = {}
        self._running = False

    def _snapshot(self) -> dict[str, float]:
        from .scanner import iter_files
        return {str(p): p.stat().st_mtime for p in iter_files(self.root)
                if p.exists()}

    def on_file_created(self, path: Path) -> None:
        rule = self.engine.evaluate(path)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if rule:
            print(f"{ts} - New file: \"{path.name}\"")
            res = rule.apply(path, {"root": self.root}, dry_run=False)
            print(f"  ✅ Rule \"{rule.name}\" matched → "
                  f"{res['action']} to {res.get('dst', '')}")
        else:
            print(f"{ts} - New file: \"{path.name}\" (no rule matched)")

    def on_file_modified(self, path: Path) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{ts} - Modified: \"{path.name}\"")

    def on_file_deleted(self, path: Path) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{ts} - Deleted: \"{path.name}\"")

    def run(self, max_iterations: int | None = None) -> None:
        """Block and watch. Ctrl-C to stop."""
        self._seen = self._snapshot()
        self._running = True
        print(f"👁️  WATCHING DIRECTORY: {self.root}")
        print(f"Rules loaded: {len(self.engine.rules)} custom rules\n")

        iterations = 0
        try:
            while self._running:
                time.sleep(self.interval)
                current = self._snapshot()

                created = set(current) - set(self._seen)
                deleted = set(self._seen) - set(current)
                modified = {
                    p for p in set(current) & set(self._seen)
                    if current[p] != self._seen[p]
                }

                for p in sorted(created):
                    self.on_file_created(Path(p))
                for p in sorted(modified):
                    self.on_file_modified(Path(p))
                for p in sorted(deleted):
                    self.on_file_deleted(Path(p))

                self._seen = current
                iterations += 1
                if max_iterations and iterations >= max_iterations:
                    break
        except KeyboardInterrupt:
            print("\n👋 Watcher stopped.")

    def stop(self) -> None:
        self._running = False


def watch_directory(directory: str | Path, rules: RuleEngine | str | Path,
                    interval: float = 1.0,
                    max_iterations: int | None = None) -> None:
    if isinstance(rules, (str, Path)):
        rules = load_rules(rules)
    watcher = FileWatcher(directory, rules, interval=interval)
    watcher.run(max_iterations=max_iterations)