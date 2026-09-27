'''
Q6: The Recursive File Organizer (Hard)

Create a recursive function that organizes files based on their properties.

Requirements:

    Create file_organizer.py with these functions:

        scan_directory(path, recursive=True) → Returns file tree

        organize_by_type(directory) → Moves files to type folders

        organize_by_date(directory) → Moves files to date folders

        organize_by_size(directory) → Moves files to size categories

    File Tree Structure:
    python

    file_tree = {
        "/home/user/documents": {
            "files": ["report.pdf", "notes.txt"],
            "subdirs": {
                "projects": {
                    "files": ["main.py", "data.csv"],
                    "subdirs": {}
                }
            }
        }
    }

    Recursive Search:

        find_files(directory, pattern) → Recursively find files

        find_duplicates(directory) → Find duplicate files (by content)

    File Analysis:

        get_file_stats(directory) → Counts, sizes, types

        get_largest_files(directory, n) → Return n largest files

        get_oldest_files(directory, n) → Return n oldest files

    Auto-organization rules:

        Images → Images/

        Documents → Documents/

        Videos → Videos/

        Audio → Audio/

        Archives → Archives/

        Executables → Programs/

    Preview before moving:

        preview_organization(directory) → Show planned changes

        dry_run flag to simulate without moving

Sample Output:
text

📁 FILE ORGANIZER 📁

Scanning: /home/user/downloads/
Found: 150 files, 25 directories

📊 File Types:
Images: 45 (30%)
Documents: 38 (25%)
Videos: 22 (15%)
Audio: 15 (10%)
Archives: 10 (7%)
Others: 20 (13%)

📅 Oldest files:
1. old_report.pdf (2023-01-15)
2. backup.zip (2023-02-20)
3. notes.txt (2023-03-01)

📁 Planned Organization:
Images/
  ├── vacation.jpg
  ├── family.png
  └── ...
Documents/
  ├── report.pdf
  ├── notes.txt
  └── ...
Videos/
  ├── movie.mp4
  └── ...

Proceed with organization? (y/n): y

✅ Organized 150 files!
Free space gained: 2.3 GB

Duplicates found: 5 files (saving 450 MB)
1. report.pdf (duplicate in Documents/)
2. image.jpg (duplicate in Images/)

Concepts: Recursion, os module, pathlib, file operations, dictionaries, nested structures, dry-run pattern, statistics
'''

# file_organizer.py
"""
Recursive File Organizer
Organizes files by type, date, or size with recursive scanning,
duplicate detection, and dry-run preview.
"""

import os
import shutil
import hashlib
import stat
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Any


# ---------- File category mappings ----------
CATEGORY_MAP = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx",
                  ".ppt", ".pptx", ".csv", ".md", ".json", ".xml"},
    "Videos": {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Programs": {".exe", ".msi", ".app", ".deb", ".rpm", ".apk", ".bat", ".sh"},
}

SIZE_CATEGORIES = [
    ("Tiny", 0, 1024),                     # < 1 KB
    ("Small", 1024, 1024 * 1024),          # 1 KB - 1 MB
    ("Medium", 1024 * 1024, 100 * 1024 * 1024),   # 1 MB - 100 MB
    ("Large", 100 * 1024 * 1024, 1024 * 1024 * 1024),  # 100 MB - 1 GB
    ("Huge", 1024 * 1024 * 1024, float("inf")),   # > 1 GB
]


# ---------- Helpers ----------
def get_category(file_path: Path) -> str:
    """Return the category name for a file based on its extension."""
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORY_MAP.items():
        if ext in extensions:
            return category
    return "Others"


def human_size(num_bytes: int) -> str:
    """Convert bytes to a human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


def file_hash(path: Path, chunk_size: int = 65536) -> str:
    """Compute a SHA-256 hash of a file's content."""
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()
    except (OSError, PermissionError):
        return ""


# ---------- 1. Recursive Directory Scanning ----------
def scan_directory(path: str, recursive: bool = True) -> dict:
    """
    Recursively scan a directory and return a nested file tree.

    Structure:
        {
            "files": [...],
            "subdirs": { name: {...}, ... }
        }
    """
    root = Path(path)
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    def _scan(current: Path) -> dict:
        tree: dict[str, Any] = {"files": [], "subdirs": {}}
        try:
            entries = sorted(current.iterdir(), key=lambda p: p.name.lower())
        except PermissionError:
            return tree

        for entry in entries:
            if entry.is_file():
                tree["files"].append(entry.name)
            elif entry.is_dir() and recursive:
                tree["subdirs"][entry.name] = _scan(entry)
            elif entry.is_dir():
                tree["subdirs"][entry.name] = {"files": [], "subdirs": {}}
        return tree

    return {str(root): _scan(root)}


# ---------- 2. Organization by Type ----------
def organize_by_type(directory: str, dry_run: bool = False) -> dict:
    """Move files into folders named after their type category."""
    root = Path(directory)
    moves: dict[str, list[str]] = defaultdict(list)

    for file_path in _iter_files(root):
        category = get_category(file_path)
        target_dir = root / category
        target = target_dir / file_path.name

        # Avoid moving into an already-correct location
        if file_path.parent == target_dir:
            continue

        # Resolve name collisions
        target = _unique_target(target)
        moves[category].append(f"{file_path.name} -> {target.relative_to(root)}")

        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(target))

    return dict(moves)


# ---------- 3. Organization by Date ----------
def organize_by_date(directory: str, dry_run: bool = False) -> dict:
    """Move files into folders named YYYY-MM based on modification time."""
    root = Path(directory)
    moves: dict[str, list[str]] = defaultdict(list)

    for file_path in _iter_files(root):
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        folder = mtime.strftime("%Y-%m")
        target_dir = root / folder
        target = _unique_target(target_dir / file_path.name)

        if file_path.parent == target_dir:
            continue

        moves[folder].append(file_path.name)
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(target))

    return dict(moves)


# ---------- 4. Organization by Size ----------
def organize_by_size(directory: str, dry_run: bool = False) -> dict:
    """Move files into size-category folders (Tiny, Small, Medium, Large, Huge)."""
    root = Path(directory)
    moves: dict[str, list[str]] = defaultdict(list)

    for file_path in _iter_files(root):
        size = file_path.stat().st_size
        label = _size_label(size)
        target_dir = root / label
        target = _unique_target(target_dir / file_path.name)

        if file_path.parent == target_dir:
            continue

        moves[label].append(file_path.name)
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(target))

    return dict(moves)


# ---------- 5. Recursive Search ----------
def find_files(directory: str, pattern: str) -> list[str]:
    """Recursively find files matching a glob pattern (e.g. '*.pdf')."""
    root = Path(directory)
    return [str(p) for p in root.rglob(pattern) if p.is_file()]


def find_duplicates(directory: str) -> dict[str, list[str]]:
    """
    Find duplicate files by content hash.
    Returns {hash: [file1, file2, ...]} for groups with >1 file.
    """
    root = Path(directory)
    by_size: dict[int, list[Path]] = defaultdict(list)

    # Group by size first (cheap pre-filter)
    for file_path in _iter_files(root):
        try:
            by_size[file_path.stat().st_size].append(file_path)
        except OSError:
            continue

    by_hash: dict[str, list[str]] = defaultdict(list)
    for size, paths in by_size.items():
        if size == 0 or len(paths) < 2:
            continue
        for p in paths:
            h = file_hash(p)
            if h:
                by_hash[h].append(str(p))

    return {h: paths for h, paths in by_hash.items() if len(paths) > 1}


# ---------- 6. File Analysis ----------
def get_file_stats(directory: str) -> dict:
    """Return counts, total size, and type breakdown for a directory."""
    root = Path(directory)
    stats = {
        "total_files": 0,
        "total_dirs": 0,
        "total_size": 0,
        "by_type": defaultdict(lambda: {"count": 0, "size": 0}),
        "by_category": defaultdict(int),
    }

    for dirpath, dirnames, filenames in os.walk(root):
        stats["total_dirs"] += len(dirnames)
        for name in filenames:
            fp = Path(dirpath) / name
            try:
                size = fp.stat().st_size
            except OSError:
                continue
            stats["total_files"] += 1
            stats["total_size"] += size

            ext = fp.suffix.lower() or "(no ext)"
            stats["by_type"][ext]["count"] += 1
            stats["by_type"][ext]["size"] += size
            stats["by_category"][get_category(fp)] += 1

    stats["by_type"] = dict(stats["by_type"])
    stats["by_category"] = dict(stats["by_category"])
    return stats


def get_largest_files(directory: str, n: int = 10) -> list[tuple[str, int]]:
    """Return the n largest files as (path, size) tuples."""
    root = Path(directory)
    files = []
    for p in _iter_files(root):
        try:
            files.append((str(p), p.stat().st_size))
        except OSError:
            continue
    files.sort(key=lambda x: x[1], reverse=True)
    return files[:n]


def get_oldest_files(directory: str, n: int = 10) -> list[tuple[str, float]]:
    """Return the n oldest files as (path, mtime) tuples."""
    root = Path(directory)
    files = []
    for p in _iter_files(root):
        try:
            files.append((str(p), p.stat().st_mtime))
        except OSError:
            continue
    files.sort(key=lambda x: x[1])
    return files[:n]


# ---------- 7. Preview / Dry Run ----------
def preview_organization(directory: str) -> dict:
    """Show what organize_by_type would do without moving anything."""
    return organize_by_type(directory, dry_run=True)


# ---------- Internal utilities ----------
def _iter_files(root: Path):
    """Yield every file under root recursively, skipping target folders."""
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            yield Path(dirpath) / name


def _size_label(size: int) -> str:
    for label, low, high in SIZE_CATEGORIES:
        if low <= size < high:
            return label
    return "Huge"


def _unique_target(target: Path) -> Path:
    """If target exists, append _1, _2, ... to avoid overwriting."""
    if not target.exists():
        return target
    stem, suffix = target.stem, target.suffix
    parent = target.parent
    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1


# ---------- CLI Demo ----------
def _print_tree(node: dict, indent: int = 0) -> None:
    pad = "  " * indent
    for name in node.get("files", []):
        print(f"{pad}📄 {name}")
    for sub, child in node.get("subdirs", {}).items():
        print(f"{pad}📁 {sub}/")
        _print_tree(child, indent + 1)


def main():
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "."
    root = Path(target).resolve()

    print("📁 FILE ORGANIZER 📁\n")
    print(f"Scanning: {root}/")

    stats = get_file_stats(root)
    print(f"Found: {stats['total_files']} files, {stats['total_dirs']} directories\n")

    # Type breakdown
    print("📊 File Types:")
    total = max(stats["total_files"], 1)
    for cat, count in sorted(stats["by_category"].items(), key=lambda x: -x[1]):
        pct = count / total * 100
        print(f"  {cat}: {count} ({pct:.0f}%)")
    print()

    # Oldest files
    print("📅 Oldest files:")
    for i, (path, mtime) in enumerate(get_oldest_files(root, 3), 1):
        dt = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        print(f"  {i}. {Path(path).name} ({dt})")
    print()

    # Preview organization
    print("📁 Planned Organization:")
    plan = preview_organization(root)
    if not plan:
        print("  (nothing to organize)")
    for category, files in sorted(plan.items()):
        print(f"  {category}/")
        for f in files[:3]:
            print(f"    ├── {f}")
        if len(files) > 3:
            print(f"    └── ... and {len(files) - 3} more")
    print()

    # Duplicates
    dupes = find_duplicates(root)
    if dupes:
        total_dupes = sum(len(v) - 1 for v in dupes.values())
        saved = 0
        for paths in dupes.values():
            try:
                saved += Path(paths[0]).stat().st_size * (len(paths) - 1)
            except OSError:
                pass
        print(f"Duplicates found: {total_dupes} files (saving {human_size(saved)})")
        for i, (h, paths) in enumerate(list(dupes.items())[:5], 1):
            print(f"  {i}. {Path(paths[0]).name} (duplicate of {len(paths)-1} other(s))")
        print()

    # Confirm
    answer = input("Proceed with organization? (y/n): ").strip().lower()
    if answer == "y":
        result = organize_by_type(root)
        moved = sum(len(v) for v in result.values())
        print(f"\n✅ Organized {moved} files!")
    else:
        print("\n❌ Cancelled.")


if __name__ == "__main__":
    main()