"""
File scanning, duplicate detection, archiving, and reporting.

Combines: scanner.py + deduplicator.py + archiver.py + report.py
"""
from __future__ import annotations

import hashlib
import html
import os
import shutil
import zipfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

# ---------- Category maps ----------
TYPE_CATEGORIES = {
    "Images":    {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx",
                  ".ppt", ".pptx", ".csv", ".md", ".json", ".xml"},
    "Videos":    {".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"},
    "Audio":     {".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"},
    "Archives":  {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    "Programs":  {".exe", ".msi", ".app", ".deb", ".rpm", ".apk", ".bat", ".sh"},
}

SIZE_CATEGORIES = [
    ("Tiny", 0, 1024),
    ("Small", 1024, 1024 * 1024),
    ("Medium", 1024 * 1024, 100 * 1024 * 1024),
    ("Large", 100 * 1024 * 1024, 1024 * 1024 * 1024),
    ("Huge", 1024 * 1024 * 1024, float("inf")),
]


# ---------- Helpers ----------
def human_size(num_bytes: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"


def categorize(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in TYPE_CATEGORIES.items():
        if ext in exts:
            return cat
    return "Others"


def size_label(size: int) -> str:
    for label, low, high in SIZE_CATEGORIES:
        if low <= size < high:
            return label
    return "Huge"


def iter_files(root: Path) -> Iterable[Path]:
    """Yield every file under root, recursively."""
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            yield Path(dirpath) / name


def file_hash(path: Path, algo: str = "md5", chunk: int = 65536) -> str:
    h = hashlib.new(algo)
    try:
        with path.open("rb") as f:
            while block := f.read(chunk):
                h.update(block)
        return h.hexdigest()
    except (OSError, PermissionError):
        return ""


# ---------- Scanning ----------
def get_file_info(filepath: str | Path) -> dict:
    p = Path(filepath)
    try:
        st = p.stat()
    except OSError as e:
        return {"path": str(p), "error": str(e)}

    return {
        "path": str(p),
        "name": p.name,
        "extension": p.suffix.lower(),
        "category": categorize(p),
        "size": st.st_size,
        "size_human": human_size(st.st_size),
        "modified": datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"),
        "created": datetime.fromtimestamp(st.st_ctime).isoformat(timespec="seconds"),
        "size_label": size_label(st.st_size),
    }


def scan_directory(directory: str | Path, recursive: bool = True) -> dict:
    """Return a summary + list of files under a directory."""
    root = Path(directory)
    if not root.is_dir():
        raise NotADirectoryError(root)

    files: list[dict] = []
    if recursive:
        for p in iter_files(root):
            info = get_file_info(p)
            if "error" not in info:
                files.append(info)
    else:
        for p in root.iterdir():
            if p.is_file():
                info = get_file_info(p)
                if "error" not in info:
                    files.append(info)

    total_size = sum(f["size"] for f in files)
    return {
        "directory": str(root),
        "recursive": recursive,
        "file_count": len(files),
        "total_size": total_size,
        "total_size_human": human_size(total_size),
        "files": files,
    }


def get_file_tree(directory: str | Path, recursive: bool = True) -> dict:
    """Nested {files: [...], subdirs: {...}} tree."""
    root = Path(directory)

    def _walk(current: Path) -> dict:
        node = {"files": [], "subdirs": {}}
        try:
            entries = sorted(current.iterdir(), key=lambda p: p.name.lower())
        except (PermissionError, OSError):
            return node
        for entry in entries:
            if entry.is_file():
                node["files"].append(entry.name)
            elif entry.is_dir() and recursive:
                node["subdirs"][entry.name] = _walk(entry)
        return node

    return {str(root): _walk(root)}


def get_file_stats(directory: str | Path) -> dict:
    """Counts + size + type + year distribution."""
    root = Path(directory)
    summary = scan_directory(root, recursive=True)

    by_category: dict[str, dict] = defaultdict(lambda: {"count": 0, "size": 0})
    by_year: dict[int, int] = defaultdict(int)
    by_extension: dict[str, int] = defaultdict(int)

    for f in summary["files"]:
        by_category[f["category"]]["count"] += 1
        by_category[f["category"]]["size"] += f["size"]
        by_extension[f["extension"] or "(none)"] += 1
        try:
            year = datetime.fromisoformat(f["modified"]).year
            by_year[year] += 1
        except ValueError:
            pass

    return {
        "directory": str(root),
        "total_files": summary["file_count"],
        "total_size": summary["total_size"],
        "total_size_human": summary["total_size_human"],
        "by_category": dict(by_category),
        "by_year": dict(sorted(by_year.items(), reverse=True)),
        "by_extension": dict(sorted(by_extension.items(), key=lambda x: -x[1])),
    }


def find_files(directory: str | Path, pattern: str) -> list[str]:
    """Recursively find files matching a glob (e.g. '*.pdf')."""
    root = Path(directory)
    return [str(p) for p in root.rglob(pattern) if p.is_file()]


# ---------- Deduplication ----------
def find_duplicates_by_name(directory: str | Path) -> dict[str, list[str]]:
    root = Path(directory)
    by_name: dict[str, list[str]] = defaultdict(list)
    for p in iter_files(root):
        by_name[p.name].append(str(p))
    return {name: paths for name, paths in by_name.items() if len(paths) > 1}


def find_duplicates_by_hash(directory: str | Path, algo: str = "md5") -> dict[str, list[str]]:
    root = Path(directory)
    by_size: dict[int, list[Path]] = defaultdict(list)
    for p in iter_files(root):
        try:
            by_size[p.stat().st_size].append(p)
        except OSError:
            continue

    by_hash: dict[str, list[str]] = defaultdict(list)
    for size, paths in by_size.items():
        if size == 0 or len(paths) < 2:
            continue
        for p in paths:
            h = file_hash(p, algo)
            if h:
                by_hash[h].append(str(p))

    return {h: paths for h, paths in by_hash.items() if len(paths) > 1}


def find_duplicates(directory: str | Path) -> dict[str, dict]:
    """Group duplicates: {group_id: {files: [...], size, wasted}}."""
    root = Path(directory)
    hashes = find_duplicates_by_hash(root)

    groups = {}
    for i, (h, paths) in enumerate(hashes.items(), 1):
        try:
            size = Path(paths[0]).stat().st_size
        except OSError:
            size = 0
        groups[f"group_{i}"] = {
            "hash": h,
            "files": paths,
            "size": size,
            "size_human": human_size(size),
            "duplicate_count": len(paths) - 1,
            "wasted": size * (len(paths) - 1),
            "wasted_human": human_size(size * (len(paths) - 1)),
        }
    return groups


def find_similar_files(directory: str | Path, threshold: float = 0.85) -> list[dict]:
    """
    Cheap image similarity using file size + name heuristics.
    (A real implementation would hash perceptual features.)
    """
    root = Path(directory)
    images = [p for p in iter_files(root)
              if categorize(p) == "Images"]
    buckets: dict[int, list[Path]] = defaultdict(list)
    for img in images:
        try:
            buckets[img.stat().st_size].append(img)
        except OSError:
            continue

    similar = []
    for size, group in buckets.items():
        if len(group) < 2:
            continue
        # Same size + similar names → flag as similar
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                if a.name.lower() == b.name.lower():
                    continue
                if abs(len(a.name) - len(b.name)) <= 3:
                    similar.append({
                        "a": str(a), "b": str(b),
                        "size": size, "size_human": human_size(size),
                        "score": threshold,
                    })
    return similar


def remove_duplicates(directory: str | Path, strategy: str = "oldest") -> dict:
    """
    Remove duplicates from each group.
    strategy: 'oldest' (keep oldest), 'newest' (keep newest),
              'shortest_path' (keep the one with the shortest path)
    """
    root = Path(directory)
    groups = find_duplicates(root)
    removed: list[str] = []
    kept: list[str] = []
    freed = 0

    for group in groups.values():
        paths = [Path(p) for p in group["files"]]
        if strategy == "oldest":
            keep = min(paths, key=lambda p: p.stat().st_mtime)
        elif strategy == "newest":
            keep = max(paths, key=lambda p: p.stat().st_mtime)
        elif strategy == "shortest_path":
            keep = min(paths, key=lambda p: len(str(p)))
        else:
            keep = paths[0]

        kept.append(str(keep))
        for p in paths:
            if p == keep:
                continue
            try:
                size = p.stat().st_size
                p.unlink()
                removed.append(str(p))
                freed += size
            except OSError:
                pass

    return {
        "removed": removed,
        "kept": kept,
        "freed": freed,
        "freed_human": human_size(freed),
        "count": len(removed),
    }


def replace_with_hardlink(directory: str | Path) -> dict:
    """Replace duplicate files with hardlinks to save disk space."""
    root = Path(directory)
    groups = find_duplicates(root)
    linked = 0
    freed = 0

    for group in groups.values():
        paths = [Path(p) for p in group["files"]]
        if len(paths) < 2:
            continue
        canonical = paths[0]
        try:
            canonical_size = canonical.stat().st_size
        except OSError:
            continue
        for p in paths[1:]:
            try:
                p.unlink()
                os.link(canonical, p)
                linked += 1
                freed += canonical_size
            except OSError:
                pass

    return {
        "linked": linked,
        "freed": freed,
        "freed_human": human_size(freed),
    }


# ---------- Archiver ----------
def archive_directory(directory: str | Path, filename: str | Path,
                      compression: int = zipfile.ZIP_DEFLATED) -> Path:
    """Zip up an entire directory."""
    src = Path(directory)
    out = Path(filename)
    with zipfile.ZipFile(out, "w", compression=compression) as zf:
        for file in src.rglob("*"):
            if file.is_file():
                zf.write(file, file.relative_to(src))
    return out


def extract_archive(filename: str | Path, destination: str | Path) -> Path:
    dest = Path(destination)
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(filename, "r") as zf:
        zf.extractall(dest)
    return dest


def compress_files(files: Iterable[str | Path], archive_name: str | Path) -> Path:
    out = Path(archive_name)
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            p = Path(f)
            if p.is_file():
                zf.write(p, p.name)
    return out


def create_encrypted_archive(directory: str | Path, password: str,
                             filename: str | Path | None = None) -> Path:
    """
    Create a password-protected ZIP.
    Uses pyminizip if available; otherwise falls back to plain zip and warns.
    """
    src = Path(directory)
    out = Path(filename or f"{src.name}.zip")

    try:
        import pyminizip  # type: ignore
        # pyminizip works on file lists, so compress each file
        file_list = [str(p) for p in src.rglob("*") if p.is_file()]
        if not file_list:
            raise ValueError("No files to archive")
        # pyminizip.compress_multiple(sources, prefixes, out, password, level)
        prefixes = ["" for _ in file_list]
        pyminizip.compress_multiple(file_list, prefixes, str(out), password, 5)
        return out
    except ImportError:
        print("⚠️  pyminizip not installed — creating UNENCRYPTED archive.")
        print("   Install with: pip install pyminizip")
        return archive_directory(src, out)


# ---------- Report ----------
def generate_report(directory: str | Path) -> dict:
    stats = get_file_stats(directory)
    dupes = find_duplicates(directory)
    total_wasted = sum(g["wasted"] for g in dupes.values())

    return {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "directory": stats["directory"],
        "total_files": stats["total_files"],
        "total_size": stats["total_size"],
        "total_size_human": stats["total_size_human"],
        "by_category": stats["by_category"],
        "by_year": stats["by_year"],
        "duplicate_groups": len(dupes),
        "duplicate_files": sum(g["duplicate_count"] for g in dupes.values()),
        "wasted": total_wasted,
        "wasted_human": human_size(total_wasted),
    }


def generate_duplicate_report(directory: str | Path) -> dict:
    dupes = find_duplicates(directory)
    similar = find_similar_files(directory)
    total_wasted = sum(g["wasted"] for g in dupes.values())
    return {
        "exact_groups": len(dupes),
        "exact_files": sum(g["duplicate_count"] for g in dupes.values()),
        "exact_wasted": total_wasted,
        "exact_wasted_human": human_size(total_wasted),
        "similar_groups": len(similar),
        "groups": dupes,
        "similar": similar,
    }


def generate_visual_report(directory: str | Path, output_dir: str | Path = "report_charts") -> dict:
    """Generate PNG charts (needs matplotlib). Returns {name: path}."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return {}

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    stats = get_file_stats(directory)
    files: dict[str, str] = {}

    # Category sizes
    cats = stats["by_category"]
    if cats:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(list(cats.keys()),
               [c["size"] / (1024 * 1024) for c in cats.values()],
               color="#4C72B0")
        ax.set_ylabel("Size (MB)")
        ax.set_title("File Size by Category")
        p = out / "categories.png"
        fig.tight_layout(); fig.savefig(p); plt.close(fig)
        files["categories"] = str(p)

    # Year distribution
    years = stats["by_year"]
    if years:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar([str(y) for y in years.keys()],
               list(years.values()), color="#55A868")
        ax.set_ylabel("Files")
        ax.set_title("Files by Year")
        p = out / "years.png"
        fig.tight_layout(); fig.savefig(p); plt.close(fig)
        files["years"] = str(p)

    return files


def export_to_html(directory: str | Path, output: str | Path) -> Path:
    report = generate_report(directory)
    dupes = generate_duplicate_report(directory)

    def esc(x): return html.escape(str(x))

    rows_cat = "".join(
        f"<tr><td>{esc(cat)}</td><td>{v['count']}</td>"
        f"<td>{human_size(v['size'])}</td></tr>"
        for cat, v in report["by_category"].items()
    )
    rows_year = "".join(
        f"<tr><td>{esc(y)}</td><td>{c}</td></tr>"
        for y, c in report["by_year"].items()
    )

    dup_html = ""
    for gid, g in dupes["groups"].items():
        files_li = "".join(f"<li>{esc(f)}</li>" for f in g["files"])
        dup_html += (
            f"<div class='card'><h3>{esc(gid)} — {esc(g['size_human'])}</h3>"
            f"<p>Duplicates: {g['duplicate_count']} "
            f"(wasted {esc(g['wasted_human'])})</p>"
            f"<ul>{files_li}</ul></div>"
        )

    html_doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>File Organizer Report</title>
<style>
 body{{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem}}
 .card{{border:1px solid #eee;border-radius:10px;padding:1rem;margin:1rem 0;background:#fafafa}}
 table{{border-collapse:collapse;width:100%}} td,th{{border-bottom:1px solid #eee;padding:.4rem;text-align:left}}
 h1{{margin-bottom:0}} .meta{{color:#666}}
</style></head><body>
<h1>📁 File Organizer Report</h1>
<p class="meta">{esc(report['generated'])} — {esc(report['directory'])}</p>

<div class="card">
 <h2>Summary</h2>
 <p>Total files: <b>{report['total_files']}</b> ({esc(report['total_size_human'])})</p>
 <p>Duplicate groups: {report['duplicate_groups']} ({report['duplicate_files']} files,
    wasted {esc(report['wasted_human'])})</p>
</div>

<div class="card"><h2>By Category</h2>
 <table><tr><th>Category</th><th>Count</th><th>Size</th></tr>{rows_cat}</table>
</div>

<div class="card"><h2>By Year</h2>
 <table><tr><th>Year</th><th>Files</th></tr>{rows_year}</table>
</div>

<div class="card"><h2>Duplicates</h2>{dup_html or '<p>No duplicates.</p>'}</div>

</body></html>"""

    out = Path(output)
    out.write_text(html_doc, encoding="utf-8")
    return out