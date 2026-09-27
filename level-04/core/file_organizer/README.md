# 📁 CORE FILE ORGANIZER - The Smart File Organizer Package 🗂️

Build a comprehensive file organization package with rules engine and AI capabilities!

Package Structure:

file_organizer/
    __init__.py
    scanner.py
    rules.py
    organizer.py
    deduplicator.py
    archiver.py
    watcher.py
    report.py
    cli.py
    gui.py
rules/
    default_rules.json
    custom_rules.json
tests/
    test_organizer.py
README.md
setup.py

Requirements:

1. File Scanner (scanner.py):

    scan_directory(directory, recursive=True) → Scan files

    get_file_info(filepath) → Size, type, modified date, etc.

    get_file_tree(directory) → Build file tree structure

    get_file_stats(directory) → Counts, sizes, types

    find_files(directory, pattern) → Find by pattern


2. Rule Engine (rules.py) - HARD:

    add_rule(name, condition, action) → Add organization rule

    load_rules(filename) → Load rules from JSON

    evaluate_rules(file, rules) → Apply rules to file

    Rule conditions:

        By extension (.jpg, .pdf, .py)

        By size (> 10MB, < 1KB)

        By date (created/modified)

        By name pattern (contains 'photo', starts with 'DSC')

        By file type (image, document, video)

    Rule actions:

        Move to folder

        Copy to folder

        Rename

        Delete (with confirmation)

        Archive (zip)


3. Organizer (organizer.py):

    organize_by_type(directory) → Move to type folders

    organize_by_date(directory, format) → Move to date folders

    organize_by_size(directory) → Move to size folders

    organize_by_custom_rules(directory) → Apply custom rules

    rename_batch(directory, pattern) → Batch rename files

    add_prefix(directory, prefix) → Add prefix to filenames


4. Deduplicator (deduplicator.py):

    find_duplicates(directory) → Find duplicate files

    find_duplicates_by_name(directory) → Find by name

    find_duplicates_by_hash(directory) → Find by content (MD5)

    find_similar_files(directory, threshold=0.85) → Find similar (for images)

    remove_duplicates(directory, strategy) → Remove duplicates

    replace_with_hardlink(directory) → Replace duplicates with hardlinks


5. Archiver (archiver.py):

    archive_directory(directory, filename) → Create ZIP archive

    extract_archive(filename, destination) → Extract archive

    compress_files(files, archive_name) → Compress files

    create_encrypted_archive(directory, password) → Encrypted archive


6. File Watcher (watcher.py) - HARDEST:

    watch_directory(directory, rules) → Monitor directory

    on_file_created(event) → Handle new files

    on_file_modified(event) → Handle modifications

    on_file_deleted(event) → Handle deletions

    run_watcher() → Run file watcher daemon


7. Report Generation (report.py):

    generate_report(directory) → Full organization report

    generate_duplicate_report(directory) → Duplicate report

    generate_visual_report(directory) → Visual report with charts

    export_to_html(directory, output) → HTML report


8. CLI Interface (cli.py):

    def main():
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        # Organize command
        org_parser = subparsers.add_parser('organize')
        org_parser.add_argument(
            'directory',
            help='Directory to organize'
        )
        org_parser.add_argument(
            '--type',
            action='store_true',
            help='Organize by type'
        )
        org_parser.add_argument(
            '--date',
            action='store_true',
            help='Organize by date'
        )
        org_parser.add_argument(
            '--rules',
            help='Custom rules file'
        )
        org_parser.add_argument(
            '--preview',
            action='store_true',
            help='Preview only'
        )

        # Deduplicate command
        dedup_parser = subparsers.add_parser('deduplicate')
        dedup_parser.add_argument(
            'directory',
            help='Directory to scan'
        )
        dedup_parser.add_argument(
            '--hash',
            action='store_true',
            help='Use hash comparison'
        )

        # Watch command
        watch_parser = subparsers.add_parser('watch')
        watch_parser.add_argument(
            'directory',
            help='Directory to watch'
        )
        watch_parser.add_argument(
            '--rules',
            help='Rules file to apply'
        )


Sample Output:

📁 FILE ORGANIZER v2.0 📁

>> scan /home/user/downloads

📊 SCAN RESULTS:
Found: 1,247 files (45.3 GB)
Directory: /home/user/downloads

📁 File Type Distribution:
Images: 423 (33.9%) - 12.4 GB
Documents: 289 (23.2%) - 3.7 GB
Videos: 187 (15.0%) - 21.4 GB
Audio: 156 (12.5%) - 4.8 GB
Archives: 98 (7.9%) - 1.9 GB
Programs: 64 (5.1%) - 1.1 GB
Others: 30 (2.4%) - 0.0 GB

📅 Date Distribution:
2026: 456 files
2025: 389 files
2024: 234 files
2023: 126 files
2022: 42 files

>> organize /home/user/downloads --type --preview

📋 PREVIEW: Organization by Type

Images -> /home/user/downloads/Images/
  vacation_photo.jpg
  screenshot_001.png
  ...

Documents -> /home/user/downloads/Documents/
  report_2026.pdf
  notes.txt
  ...

Videos -> /home/user/downloads/Videos/
  tutorial.mp4
  conference.mp4
  ...

Continue with organization? (y/n): y

✅ Organized 1,247 files into 7 folders

>> deduplicate /home/user/downloads

🔍 SCANNING FOR DUPLICATES...
Found 47 duplicate groups (total: 134 duplicates)
Saving potential: 3.2 GB

Duplicate Group 1:
  vacation.jpg (2.4 MB)
  vacation.jpg (2.4 MB) - duplicate
  vacation.jpg (2.4 MB) - duplicate

Duplicate Group 2:
  report.pdf (456 KB)
  report.pdf (456 KB) - duplicate

[Similar files: 5 groups]

Remove duplicates? (y/n): y

✅ Removed 134 duplicate files (saved 3.2 GB)

>> watch /home/user/downloads --rules custom_rules.json

👁️ WATCHING DIRECTORY...
Rules loaded: 12 custom rules

2026-09-05 14:30:22 - New file: "image123.png"
  ✅ Rule "Images to Images" matched → Moving to Images/

2026-09-05 14:31:05 - New file: "report.docx"
  ✅ Rule "Documents by date" matched → Moving to Documents/2026/09/

2026-09-05 14:32:15 - New file: "virus.exe"
  ❌ Rule "Block executables" matched → Moving to Quarantine/

>> report /home/user/downloads --export html

📊 ORGANIZATION REPORT
Date: 2026-09-05
Directory: /home/user/downloads
Files organized: 1,247
Duplicate found: 47 (3.8%)
Space saved: 3.2 GB
Rules applied: 12

📁 New structure:

/home/user/downloads/
  Images/ - 423 files (12.4 GB)
  Documents/ - 289 files (3.7 GB)
  Videos/ - 187 files (21.4 GB)
  Audio/ - 156 files (4.8 GB)
  Archives/ - 98 files (1.9 GB)
  Programs/ - 64 files (1.1 GB)
  Quarantine/ - 30 files (0.0 GB)

✅ Report exported to report.html


## Concepts Tested:

- Recursive functions
- File system operations (os, shutil, pathlib)
- Hashing (MD5)
- Rule engine pattern
- File watching (watchdog)
- Argument parsing
- HTML generation
- JSON configuration
- Event handling