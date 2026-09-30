import argparse
import fnmatch
import hashlib
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class FileInfo:
    path: Path
    relative_path: Path
    size: int
    modified_time: float
    md5: str


def calculate_md5(file_path):
    """Calculate the MD5 hash of a file."""
    md5 = hashlib.md5()

    with file_path.open("rb") as file:
        while chunk := file.read(8192):
            md5.update(chunk)

    return md5.hexdigest()


def get_file_info(base_directory, file_path):
    """Create FileInfo for a file."""
    stat = file_path.stat()

    return FileInfo(
        path=file_path,
        relative_path=file_path.relative_to(base_directory),
        size=stat.st_size,
        modified_time=stat.st_mtime,
        md5=calculate_md5(file_path),
    )


def should_exclude(relative_path, exclude_patterns):
    """Check whether a relative path matches an exclude pattern."""
    path_string = relative_path.as_posix()

    for pattern in exclude_patterns:
        if fnmatch.fnmatch(path_string, pattern):
            return True

        if fnmatch.fnmatch(relative_path.name, pattern):
            return True

    return False


def scan_directory(directory, exclude_patterns=None):
    """
    Scan a directory recursively.

    Returns:
        Dictionary mapping relative paths to FileInfo objects.
    """
    directory = Path(directory)
    exclude_patterns = exclude_patterns or []

    files = {}

    if not directory.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    for file_path in directory.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(directory)

        if should_exclude(relative_path, exclude_patterns):
            continue

        files[relative_path] = get_file_info(
            directory,
            file_path,
        )

    return files


def compare_directories(source_files, target_files):
    """Compare two directory snapshots."""
    source_paths = set(source_files)
    target_paths = set(target_files)

    source_only = source_paths - target_paths
    target_only = target_paths - source_paths

    common_paths = source_paths & target_paths

    modified = set()
    unchanged = set()

    for relative_path in common_paths:
        source = source_files[relative_path]
        target = target_files[relative_path]

        if source.md5 == target.md5:
            unchanged.add(relative_path)
        else:
            modified.add(relative_path)

    return {
        "source_only": source_only,
        "target_only": target_only,
        "modified": modified,
        "unchanged": unchanged,
    }


def format_path(path):
    """Convert a Path into a readable string."""
    return path.as_posix()


def copy_file(source, destination, dry_run=False):
    """Copy one file while preserving metadata."""
    if dry_run:
        print(f"[DRY-RUN] COPY {source} -> {destination}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)

    print(f"[COPIED] {source} -> {destination}")


def delete_file(file_path, dry_run=False):
    """Delete a file."""
    if dry_run:
        print(f"[DRY-RUN] DELETE {file_path}")
        return

    file_path.unlink()
    print(f"[DELETED] {file_path}")


def synchronize_one_way(
    source_directory,
    target_directory,
    source_files,
    target_files,
    conflict_strategy="newest",
    dry_run=False,
):
    """
    Synchronize source -> target.

    The source directory is treated as authoritative for files
    that exist only on the source side.

    Files that exist only on target are removed.
    Modified files are resolved according to conflict_strategy.
    """
    comparison = compare_directories(source_files, target_files)

    report = {
        "copied": [],
        "deleted": [],
        "updated": [],
        "unchanged": [],
        "conflicts": [],
    }

    # Files existing only in source.
    for relative_path in sorted(comparison["source_only"]):
        source_file = source_directory / relative_path
        target_file = target_directory / relative_path

        copy_file(
            source_file,
            target_file,
            dry_run,
        )

        report["copied"].append(relative_path)

    # Files existing only in target.
    for relative_path in sorted(comparison["target_only"]):
        target_file = target_directory / relative_path

        delete_file(
            target_file,
            dry_run,
        )

        report["deleted"].append(relative_path)

    # Files existing on both sides but with different content.
    for relative_path in sorted(comparison["modified"]):
        source_file = source_files[relative_path]
        target_file = target_files[relative_path]

        chosen_side = resolve_conflict(
            relative_path,
            source_file,
            target_file,
            conflict_strategy,
        )

        if chosen_side == "source":
            copy_file(
                source_file.path,
                target_file.path,
                dry_run,
            )
            report["updated"].append(relative_path)

        elif chosen_side == "target":
            copy_file(
                target_file.path,
                source_file.path,
                dry_run,
            )
            report["updated"].append(relative_path)

        elif chosen_side == "skip":
            print(f"[SKIPPED] {relative_path}")

        report["conflicts"].append(
            {
                "path": relative_path,
                "resolution": chosen_side,
            }
        )

    for relative_path in sorted(comparison["unchanged"]):
        report["unchanged"].append(relative_path)

    return report


def synchronize_bidirectional(
    source_directory,
    target_directory,
    source_files,
    target_files,
    conflict_strategy="newest",
    dry_run=False,
):
    """
    Synchronize both directories.

    Files that exist on only one side are copied to the other side.

    Files modified on both sides are resolved according to the
    selected conflict strategy.
    """
    comparison = compare_directories(source_files, target_files)

    report = {
        "copied": [],
        "updated": [],
        "unchanged": [],
        "conflicts": [],
    }

    # Source-only files.
    for relative_path in sorted(comparison["source_only"]):
        source_file = source_directory / relative_path
        target_file = target_directory / relative_path

        copy_file(
            source_file,
            target_file,
            dry_run,
        )

        report["copied"].append(relative_path)

    # Target-only files.
    for relative_path in sorted(comparison["target_only"]):
        target_file = target_directory / relative_path
        source_file = source_directory / relative_path

        copy_file(
            target_file,
            source_file,
            dry_run,
        )

        report["copied"].append(relative_path)

    # Modified files.
    for relative_path in sorted(comparison["modified"]):
        source_file = source_files[relative_path]
        target_file = target_files[relative_path]

        chosen_side = resolve_conflict(
            relative_path,
            source_file,
            target_file,
            conflict_strategy,
        )

        if chosen_side == "source":
            copy_file(
                source_file.path,
                target_file.path,
                dry_run,
            )
            report["updated"].append(relative_path)

        elif chosen_side == "target":
            copy_file(
                target_file.path,
                source_file.path,
                dry_run,
            )
            report["updated"].append(relative_path)

        elif chosen_side == "skip":
            print(f"[SKIPPED] {relative_path}")

        report["conflicts"].append(
            {
                "path": relative_path,
                "resolution": chosen_side,
            }
        )

    for relative_path in sorted(comparison["unchanged"]):
        report["unchanged"].append(relative_path)

    return report


def resolve_conflict(
    relative_path,
    source_file,
    target_file,
    strategy,
):
    """Resolve a modified-file conflict."""
    if strategy == "source":
        print(f"[CONFLICT] {relative_path} -> SOURCE")
        return "source"

    if strategy == "target":
        print(f"[CONFLICT] {relative_path} -> TARGET")
        return "target"

    if strategy == "newest":
        if source_file.modified_time >= target_file.modified_time:
            print(f"[CONFLICT] {relative_path} -> SOURCE (newest)")
            return "source"

        print(f"[CONFLICT] {relative_path} -> TARGET (newest)")
        return "target"

    if strategy == "ask":
        return ask_conflict(relative_path)

    raise ValueError(f"Unknown conflict strategy: {strategy}")


def ask_conflict(relative_path):
    """Ask the user how to resolve a conflict."""
    while True:
        print()
        print(f"Conflict detected: {relative_path}")
        print("Choose a resolution:")
        print("  [s] Source")
        print("  [t] Target")
        print("  [k] Skip")

        choice = input("Choice: ").strip().lower()

        if choice == "s":
            return "source"

        if choice == "t":
            return "target"

        if choice == "k":
            return "skip"

        print("Invalid choice. Enter s, t, or k.")


def print_comparison(comparison):
    """Display the differences between two directories."""
    print()
    print("=" * 60)
    print("DIRECTORY COMPARISON")
    print("=" * 60)

    print(f"\nNew in source: {len(comparison['source_only'])}")

    for path in sorted(comparison["source_only"]):
        print(f"  + {format_path(path)}")

    print(f"\nNew in target: {len(comparison['target_only'])}")

    for path in sorted(comparison["target_only"]):
        print(f"  + {format_path(path)}")

    print(f"\nModified: {len(comparison['modified'])}")

    for path in sorted(comparison["modified"]):
        print(f"  ~ {format_path(path)}")

    print(f"\nUnchanged: {len(comparison['unchanged'])}")

    for path in sorted(comparison["unchanged"]):
        print(f"  = {format_path(path)}")

    print("=" * 60)


def print_report(report):
    """Display synchronization results."""
    print()
    print("=" * 60)
    print("SYNCHRONIZATION REPORT")
    print("=" * 60)

    print(f"Copied:    {len(report.get('copied', []))}")
    print(f"Updated:   {len(report.get('updated', []))}")
    print(f"Deleted:   {len(report.get('deleted', []))}")
    print(f"Unchanged: {len(report.get('unchanged', []))}")
    print(f"Conflicts: {len(report.get('conflicts', []))}")

    print("=" * 60)


def write_report(report, report_file):
    """Write a synchronization report to a text file."""
    report_file = Path(report_file)

    with report_file.open("w", encoding="utf-8") as file:
        file.write("DIRECTORY SYNCHRONIZATION REPORT\n")
        file.write("=" * 60 + "\n")
        file.write(
            f"Generated: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        file.write("=" * 60 + "\n\n")

        for category, items in report.items():
            file.write(f"{category.upper()}: {len(items)}\n")

            if category == "conflicts":
                for conflict in items:
                    file.write(
                        f"  {format_path(conflict['path'])}"
                        f" -> {conflict['resolution']}\n"
                    )
            else:
                for item in items:
                    file.write(f"  {format_path(item)}\n")

            file.write("\n")

    print(f"Report written to: {report_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Synchronize two directories."
    )

    parser.add_argument(
        "source",
        help="Source directory",
    )

    parser.add_argument(
        "target",
        help="Target directory",
    )

    parser.add_argument(
        "--mode",
        choices=["one-way", "bidirectional"],
        default="one-way",
        help="Synchronization mode.",
    )

    parser.add_argument(
        "--conflict",
        choices=["newest", "source", "target", "ask"],
        default="newest",
        help="Conflict resolution strategy.",
    )

    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Pattern to exclude. Can be specified multiple times.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without modifying files.",
    )

    parser.add_argument(
        "--report",
        nargs="?",
        const="sync_report.txt",
        help="Write synchronization report to a file.",
    )

    parser.add_argument(
        "--compare-only",
        action="store_true",
        help="Only compare directories without synchronizing.",
    )

    args = parser.parse_args()

    source_directory = Path(args.source).resolve()
    target_directory = Path(args.target).resolve()

    source_files = scan_directory(
        source_directory,
        args.exclude,
    )

    target_files = scan_directory(
        target_directory,
        args.exclude,
    )

    comparison = compare_directories(
        source_files,
        target_files,
    )

    print_comparison(comparison)

    if args.compare_only:
        return

    if args.mode == "one-way":
        report = synchronize_one_way(
            source_directory,
            target_directory,
            source_files,
            target_files,
            args.conflict,
            args.dry_run,
        )
    else:
        report = synchronize_bidirectional(
            source_directory,
            target_directory,
            source_files,
            target_files,
            args.conflict,
            args.dry_run,
        )

    print_report(report)

    if args.report:
        write_report(
            report,
            args.report,
        )


if __name__ == "__main__":
    main()