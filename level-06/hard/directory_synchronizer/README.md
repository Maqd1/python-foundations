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

## Directory Structure

```text
directory_synchronizer/
├── README.md
└── directory_synchronizer.py
```

## Basic Usage

Compare two directories:

```bash
python directory_synchronizer.py source target --compare-only
```

Synchronize source to target:

```bash
python directory_synchronizer.py source target
```

The default mode is one-way synchronization.

## One-Way Synchronization

```bash
python directory_synchronizer.py source target --mode one-way
```

In one-way mode, the source directory is treated as the authoritative directory.

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

`a.txt` is copied from source to target, while `c.txt` is removed from target.

## Bidirectional Synchronization

```bash
python directory_synchronizer.py source target --mode bidirectional
```

Files that exist only on one side are copied to the other side.

Example:

```text
source/
└── source.txt

target/
└── target.txt
```

After bidirectional synchronization:

```text
source/
├── source.txt
└── target.txt

target/
├── source.txt
└── target.txt
```

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

The program asks which version should be used for each conflict.

## MD5 File Comparison

The program calculates an MD5 hash for every file.

Files are considered unchanged when their hashes match.

For example:

```text
source/data.txt
MD5: abc123...

target/data.txt
MD5: abc123...
```

Because the hashes match, the files are considered identical.

If the hashes differ, the file is treated as modified.

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
    --exclude "__pycache__" \
    --exclude "*.tmp"
```

## Dry Run

Use:

```bash
python directory_synchronizer.py source target --dry-run
```

The program shows what it would do without changing either directory.

Example:

```text
[DRY-RUN] COPY source/report.txt -> target/report.txt
[DRY-RUN] DELETE target/old.txt
```

This is useful for safely checking synchronization before making changes.

## Comparison Only

To inspect differences without synchronizing:

```bash
python directory_synchronizer.py source target --compare-only
```

Example:

```text
============================================================
DIRECTORY COMPARISON
============================================================

New in source: 2
  + image.png
  + report.pdf

New in target: 1
  + old.txt

Modified: 1
  ~ data.csv

Unchanged: 3
  = README.md
  = config.json
  = notes.txt

============================================================
```

## Reports

Generate a report:

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
* sets and set operations
* dictionaries
* command-line arguments
* `argparse`
* pattern matching with `fnmatch`
* conflict resolution
* exception handling
* dry-run design
* report generation
* modular program design

## Important Design Idea

The program first creates a snapshot of both directories.

Each file is represented by information such as:

```text
relative path
file size
modified time
MD5 hash
```

The relative path is then used as the identity of the file.

The comparison process can therefore determine:

```text
source only     → new source file
target only     → new target file
both + same MD5 → unchanged
both + different MD5 → modified
```

This separation between **scanning**, **comparison**, **conflict resolution**, and **synchronization** keeps the program easier to understand and extend.
