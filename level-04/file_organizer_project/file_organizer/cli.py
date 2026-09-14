"""CLI for the file organizer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import (
    scan_directory, get_file_stats, find_duplicates, remove_duplicates,
    archive_directory, extract_archive,
    generate_report, generate_duplicate_report,
    generate_visual_report, export_to_html,
)
from .scanner import human_size
from .organizer import (
    organize_by_type, organize_by_date, organize_by_size,
    organize_by_custom_rules, rename_batch, add_prefix,
    preview_organization,
)
from .rules import watch_directory


BANNER = "📁 FILE ORGANIZER v2.0 📁"


# ---------- helpers ----------
def _bar(pct: float, width: int = 20) -> str:
    return "█" * int(round(pct / 100 * width))


def _print_scan(stats: dict) -> None:
    print("📊 SCAN RESULTS:")
    print(f"Found: {stats['total_files']:,} files ({stats['total_size_human']})")
    print(f"Directory: {stats['directory']}\n")

    print("📁 File Type Distribution:")
    total = stats["total_files"] or 1
    for cat, info in sorted(stats["by_category"].items(),
                            key=lambda x: -x[1]["size"]):
        pct = info["count"] / total * 100
        print(f"  {cat}: {info['count']} ({pct:.1f}%) - {human_size(info['size'])}")
    print()

    if stats["by_year"]:
        print("📅 Date Distribution:")
        for year, count in stats["by_year"].items():
            print(f"  {year}: {count} files")
        print()


# ---------- commands ----------
def cmd_scan(args) -> int:
    stats = get_file_stats(args.directory)
    _print_scan(stats)
    return 0


def cmd_organize(args) -> int:
    root = Path(args.directory)
    if not root.is_dir():
        print(f"❌ Not a directory: {root}")
        return 1

    mode = "type"
    if args.date: mode = "date"
    elif args.size: mode = "size"
    elif args.rules: mode = "rules"

    if mode == "rules":
        if not Path(args.rules).exists():
            print(f"❌ Rules file not found: {args.rules}")
            return 1
        results = organize_by_custom_rules(root, args.rules,
                                           dry_run=args.preview)
        if args.preview:
            print("📋 PREVIEW: Custom Rules")
            for r in results:
                print(f"  [{r.get('rule', '?')}] {r['action']}: {r['src']}")
        else:
            print(f"✅ Applied {len(results)} rule actions")
        return 0

    # type/date/size
    plan = preview_organization(root, mode=mode)
    if not plan:
        print("Nothing to organize.")
        return 0

    print(f"📋 PREVIEW: Organization by {mode.capitalize()}")
    for folder, files in sorted(plan.items()):
        print(f"{folder}/")
        for f in files[:5]:
            print(f"  {f}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")
        print()

    if args.preview:
        print("(preview only — nothing moved)")
        return 0

    confirm = input("Continue with organization? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return 0

    if mode == "type":
        result = organize_by_type(root)
    elif mode == "date":
        result = organize_by_date(root)
    else:
        result = organize_by_size(root)

    print(f"✅ Organized {result['moved']} files into "
          f"{len(result['folders'])} folders")
    return 0


def cmd_deduplicate(args) -> int:
    root = Path(args.directory)
    if not root.is_dir():
        print(f"❌ Not a directory: {root}")
        return 1

    print("🔍 SCANNING FOR DUPLICATES...")
    dupes = find_duplicates(root)
    total_dupes = sum(g["duplicate_count"] for g in dupes.values())
    total_wasted = sum(g["wasted"] for g in dupes.values())

    if not dupes:
        print("✅ No duplicates found.")
        return 0

    print(f"Found {len(dupes)} duplicate groups (total: {total_dupes} duplicates)")
    print(f"Saving potential: {human_size(total_wasted)}\n")

    for i, (gid, g) in enumerate(dupes.items(), 1):
        if i > 3 and not args.all:
            print(f"... and {len(dupes) - 3} more groups (use --all)")
            break
        print(f"Duplicate Group {i}:")
        for j, f in enumerate(g["files"]):
            tag = " - duplicate" if j > 0 else ""
            print(f"  {Path(f).name} ({g['size_human']}){tag}")
        print()

    if args.preview:
        return 0

    confirm = input("Remove duplicates? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return 0

    result = remove_duplicates(root, strategy=args.strategy)
    print(f"✅ Removed {result['count']} duplicate files "
          f"(saved {result['freed_human']})")
    return 0


def cmd_watch(args) -> int:
    if not Path(args.directory).is_dir():
        print(f"❌ Not a directory: {args.directory}")
        return 1

    if args.rules:
        watch_directory(args.directory, args.rules,
                        interval=args.interval,
                        max_iterations=args.iterations)
    else:
        print("❌ --rules is required for watch")
        return 1
    return 0


def cmd_report(args) -> int:
    root = Path(args.directory)
    if not root.is_dir():
        print(f"❌ Not a directory: {root}")
        return 1

    report = generate_report(root)
    print("📊 ORGANIZATION REPORT")
    print(f"Date: {report['generated']}")
    print(f"Directory: {report['directory']}")
    print(f"Files organized: {report['total_files']}")
    print(f"Duplicates found: {report['duplicate_groups']} "
          f"({report['duplicate_files']} files)")
    print(f"Space wasted: {report['wasted_human']}")
    print()

    print("📁 Structure:")
    for cat, info in sorted(report["by_category"].items(),
                            key=lambda x: -x[1]["size"]):
        print(f"  {cat}/ - {info['count']} files ({human_size(info['size'])})")
    print()

    if args.export == "html":
        out = export_to_html(root, args.output or "report.html")
        print(f"✅ Report exported to {out}")
    elif args.export == "json":
        out = Path(args.output or "report.json")
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"✅ Report exported to {out}")
    elif args.export == "charts":
        charts = generate_visual_report(root, args.output or "report_charts")
        if charts:
            print("✅ Charts generated:")
            for name, p in charts.items():
                print(f"  {name}: {p}")
        else:
            print("⚠️  matplotlib not installed; skipping charts.")
    return 0


def cmd_rename(args) -> int:
    root = Path(args.directory)
    if args.prefix:
        results = add_prefix(root, args.prefix, dry_run=args.preview)
    else:
        results = rename_batch(root, args.pattern, dry_run=args.preview)

    for r in results:
        print(f"{r['src']}  →  {r['dst']}")
    print(f"\n{'(preview only) ' if args.preview else ''}"
          f"{len(results)} files")
    return 0


def cmd_archive(args) -> int:
    root = Path(args.directory)
    if args.extract:
        dest = extract_archive(args.extract, args.output or "extracted")
        print(f"✅ Extracted to {dest}")
        return 0
    out = archive_directory(root, args.output or f"{root.name}.zip")
    print(f"✅ Archived to {out}")
    return 0


# ---------- parser ----------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="file-organizer", description=BANNER)
    sub = p.add_subparsers(dest="command", required=True)

    # scan
    s = sub.add_parser("scan", help="Scan a directory")
    s.add_argument("directory")
    s.set_defaults(func=cmd_scan)

    # organize
    o = sub.add_parser("organize", help="Organize files")
    o.add_argument("directory")
    o.add_argument("--type", action="store_true", help="Organize by type")
    o.add_argument("--date", action="store_true", help="Organize by date")
    o.add_argument("--size", action="store_true", help="Organize by size")
    o.add_argument("--rules", help="Custom rules JSON file")
    o.add_argument("--preview", action="store_true", help="Preview only")
    o.set_defaults(func=cmd_organize)

    # deduplicate
    d = sub.add_parser("deduplicate", help="Find/remove duplicates")
    d.add_argument("directory")
    d.add_argument("--hash", action="store_true", help="Use content hash")
    d.add_argument("--preview", action="store_true")
    d.add_argument("--all", action="store_true", help="Show all groups")
    d.add_argument("--strategy", default="oldest",
                   choices=["oldest", "newest", "shortest_path"])
    d.set_defaults(func=cmd_deduplicate)

    # watch
    w = sub.add_parser("watch", help="Watch a directory")
    w.add_argument("directory")
    w.add_argument("--rules", required=True)
    w.add_argument("--interval", type=float, default=1.0)
    w.add_argument("--iterations", type=int, default=None)
    w.set_defaults(func=cmd_watch)

    # report
    r = sub.add_parser("report", help="Generate report")
    r.add_argument("directory")
    r.add_argument("--export", choices=["html", "json", "charts"])
    r.add_argument("--output", default=None)
    r.set_defaults(func=cmd_report)

    # rename
    rn = sub.add_parser("rename", help="Batch rename")
    rn.add_argument("directory")
    rn.add_argument("--pattern", default="file_{n:03d}{ext}")
    rn.add_argument("--prefix", default=None)
    rn.add_argument("--preview", action="store_true")
    rn.set_defaults(func=cmd_rename)

    # archive
    a = sub.add_parser("archive", help="Archive directory")
    a.add_argument("directory")
    a.add_argument("--output", default=None)
    a.add_argument("--extract", default=None)
    a.set_defaults(func=cmd_archive)

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    print(BANNER)
    print()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())