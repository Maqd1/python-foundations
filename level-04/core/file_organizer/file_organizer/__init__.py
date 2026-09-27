"""Smart File Organizer package."""
from .scanner import (
    scan_directory, get_file_info, get_file_tree, get_file_stats,
    find_files, find_duplicates, find_duplicates_by_name,
    find_duplicates_by_hash, find_similar_files,
    remove_duplicates, replace_with_hardlink,
    archive_directory, extract_archive, compress_files,
    create_encrypted_archive,
    generate_report, generate_duplicate_report,
    generate_visual_report, export_to_html,
)
from .rules import (
    Rule, RuleEngine, RuleAction, Condition, load_rules,
    evaluate_rules, FileWatcher, watch_directory,
)
from .organizer import (
    organize_by_type, organize_by_date, organize_by_size,
    organize_by_custom_rules, rename_batch, add_prefix,
    preview_organization,
)

__version__ = "2.0.0"
__all__ = [
    "scan_directory", "get_file_info", "get_file_tree", "get_file_stats",
    "find_files", "find_duplicates", "find_duplicates_by_name",
    "find_duplicates_by_hash", "find_similar_files",
    "remove_duplicates", "replace_with_hardlink",
    "archive_directory", "extract_archive", "compress_files",
    "create_encrypted_archive",
    "generate_report", "generate_duplicate_report",
    "generate_visual_report", "export_to_html",
    "Rule", "RuleEngine", "RuleAction", "Condition", "load_rules",
    "evaluate_rules", "FileWatcher", "watch_directory",
    "organize_by_type", "organize_by_date", "organize_by_size",
    "organize_by_custom_rules", "rename_batch", "add_prefix",
    "preview_organization",
]