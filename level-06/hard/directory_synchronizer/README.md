# Directory Synchronizer

A Python command-line utility for comparing and synchronizing two directories.

## Features

* Recursive directory comparison
* Detects files that exist only in the source
* Detects files that exist only in the target
* Detects modified files
* Detects unchanged files
* Uses MD5 hashes to compare file contents
* One-way synchronization
* Bidirectional synchronization
* Conflict resolution:

  * `newest`
  * `source`
  * `target`
  * `ask`
* Exclude patterns
* Dry-run mode
* Synchronization reports
* File metadata preservation with `shutil.copy2()`

## Project Structure

```text
directory_synchronizer/
├── README.md
└── directory_synchronizer.py
```

## Basic Usage

Compare two directories without making changes:

```bash
python directory_synchronizer.py source target --compare-only
```

Synchronize source to target:

```bash
python directory_synchronizer.py source target
```

The default synchronization mode is one-way.

---

## Directory Comparison

The program recursively scans both directories and compares files using their relative paths and MD5 content hashes.

It identifies:

```text
Source only     → file exists only in source
Target only     → file exists only in target
Modified        → file exists in both but contents differ
Unchanged       → file exists in both with identical contents
```

Example:

```text
============================================================
DIRECTORY COMPARISON
============================================================

New in source: 1
  + report.pdf

New in target: 1
  + old.txt

Modified: 1
  ~ config.json

Unchanged: 3
  = README.md
  = notes.txt
  = data.csv

============================================================
```

## One-Way Synchronization

```bash
python directory_synchronizer.py source target --mode one-way
```

One-way synchronization treats the source directory as authoritative.

Files that exist only in the source are copied to the target.

Files that exist only in the target are deleted.

Modified files are resolved according to the selected conflict strategy.

For example:

```text
source/
├── a.txt
└── b.txt

target/
├── b.txt
└── c.txt
```

After synchronization:

```text
source/
├── a.txt
└── b.txt

target/
├── a.txt
└── b.txt
```

## Bidirectional Synchronization

```bash
python directory_synchronizer.py source target --mode bidirectional
```

Bidirectional synchronization copies files that exist only on one side to the other side.

For example:

```text
source/
└── source.txt

target/
└── target.txt
```

After synchronization:

```text
source/
├── source.txt
└── target.txt

target/
├── source.txt
└── target.txt
```

When the same file exists on both sides but has different contents, the selected conflict strategy determines which version is used.

## Conflict Resolution

A conflict occurs when the same relative file path exists in both directories but the contents are different.

### Newest

```bash
python directory_synchronizer.py source target --conflict newest
```

The file with the newer modification time is selected.

### Source

```bash
python directory_synchronizer.py source target --conflict source
```

The source version is selected.

### Target

```bash
python directory_synchronizer.py source target --conflict target
```

The target version is selected.

### Ask

```bash
python directory_synchronizer.py source target --conflict ask
```

The program interactively asks how each conflict should be resolved.

Available choices:

```text
[s] Source
[t] Target
[k] Skip
```

## MD5 File Comparison

The program calculates an MD5 hash for each file.

Files with matching hashes are treated as unchanged.

Files with different hashes are treated as modified.

The comparison therefore does not rely only on filenames or file sizes.

Conceptually:

```text
source/data.txt
      │
      ▼
   MD5 hash
      │
      │ compare
      ▼
target/data.txt
      │
      ▼
   MD5 hash
```

If both hashes match:

```text
UNCHANGED
```

If they differ:

```text
MODIFIED
```

## Excluding Files

Use `--exclude` to ignore files or patterns.

For example:

```bash
python directory_synchronizer.py source target \
    --exclude "*.log"
```

Multiple patterns can be supplied:

```bash
python directory_synchronizer.py source target \
    --exclude "*.log" \
    --exclude "*.tmp" \
    --exclude "__pycache__"
```

Excluded files are ignored during both comparison and synchronization.

## Dry Run

Use:

```bash
python directory_synchronizer.py source target --dry-run
```

Dry-run mode displays the operations that would be performed without modifying either directory.

Example:

```text
[DRY-RUN] COPY source/report.txt -> target/report.txt
[DRY-RUN] DELETE target/old.txt
```

This provides a safe way to inspect synchronization operations before applying them.

## Comparison Only

To compare directories without synchronizing:

```bash
python directory_synchronizer.py source target --compare-only
```

This is useful when you only want to inspect differences.

## Reports

Generate a synchronization report:

```bash
python directory_synchronizer.py source target --report
```

This creates:

```text
sync_report.txt
```

A custom report filename can also be supplied:

```bash
python directory_synchronizer.py source target \
    --report synchronization_report.txt
```

Reports contain:

* copied files
* updated files
* deleted files
* unchanged files
* conflict resolutions
* report generation time

Example:

```text
DIRECTORY SYNCHRONIZATION REPORT
============================================================
Generated: 2026-09-30 11:01:26
============================================================

COPIED: 1
  source.txt

DELETED: 1
  target.txt

UPDATED: 0

UNCHANGED: 0

CONFLICTS: 0
```

## Command-Line Options

| Option           | Description                            |
| ---------------- | -------------------------------------- |
| `source`         | Source directory                       |
| `target`         | Target directory                       |
| `--mode`         | `one-way` or `bidirectional`           |
| `--conflict`     | `newest`, `source`, `target`, or `ask` |
| `--exclude`      | Exclude a file pattern                 |
| `--dry-run`      | Show operations without applying them  |
| `--report`       | Generate a synchronization report      |
| `--compare-only` | Compare without synchronizing          |

## Concepts Practiced

This project demonstrates:

* `pathlib`
* recursive directory traversal
* file metadata
* MD5 hashing
* `hashlib`
* `shutil`
* file copying
* file deletion
* `dataclasses`
* dictionaries
* sets and set operations
* `argparse`
* command-line interfaces
* `fnmatch`
* pattern matching
* conflict resolution
* exception handling
* dry-run design
* report generation
* modular program design

## Design Overview

The program separates the synchronization process into several stages:

```text
Scan directories
       │
       ▼
Create file information
       │
       ├── relative path
       ├── file size
       ├── modified time
       └── MD5 hash
       │
       ▼
Compare directories
       │
       ├── source only
       ├── target only
       ├── modified
       └── unchanged
       │
       ▼
Resolve conflicts
       │
       ▼
Synchronize
       │
       ├── copy
       ├── update
       ├── delete
       └── skip
```

This separation makes the program easier to test, understand, and extend.
