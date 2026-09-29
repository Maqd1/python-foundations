# File Organizer

A Python file organization utility that scans a directory, categorizes files by extension, creates appropriate folders, and moves files into those folders.

## Features

* Scans a directory for files
* Categorizes files by extension
* Creates category folders automatically
* Moves files into their appropriate folders
* Handles duplicate filenames by adding numbered suffixes
* Records file movements in an organization log
* Supports dry-run mode for previewing changes without modifying files
* Ignores its own `organization_log.txt` file when scanning

## File Categories

| Category       | Extensions                      |
| -------------- | ------------------------------- |
| `IMAGES`       | `.jpg`, `.jpeg`, `.png`, `.gif` |
| `DOCS`         | `.doc`, `.docx`, `.pdf`         |
| `SPREADSHEETS` | `.xls`, `.xlsx`, `.csv`         |
| `TEXT`         | `.txt`                          |
| `OTHERS`       | Any unsupported extension       |

## Example

Given a directory containing:

```text
downloads/
├── photo.jpg
├── report.pdf
├── notes.txt
├── budget.xlsx
└── unknown.xyz
```

The organizer produces:

```text
downloads/
├── DOCS/
│   └── report.pdf
├── IMAGES/
│   └── photo.jpg
├── SPREADSHEETS/
│   └── budget.xlsx
├── TEXT/
│   └── notes.txt
└── OTHERS/
    └── unknown.xyz
```

An `organization_log.txt` file is also created containing the original and new paths of moved files.

## Duplicate Files

If a destination filename already exists, the organizer automatically generates a numbered filename.

For example:

```text
report.pdf
report_1.pdf
report_2.pdf
```

This prevents existing files from being overwritten.

## Dry-Run Mode

Dry-run mode previews the operations without actually creating folders or moving files.

Example:

```text
Dry-run mode? (y/n): y

👀 DRY-RUN MODE
Would move: downloads/report.pdf -> downloads/DOCS/report.pdf
Would move: downloads/photo.jpg -> downloads/IMAGES/photo.jpg

✅ Dry run complete. No files were moved.
```

## Usage

Run the program with:

```bash
python file_organizer.py
```

Enter the directory you want to organize:

```text
Enter directory to organize: /path/to/downloads
```

Confirm the operation:

```text
Proceed? (y/n): y
```

Choose whether to use dry-run mode:

```text
Dry-run mode? (y/n): n
```

## Concepts Practiced

* `pathlib.Path`
* File and directory operations
* `Path.iterdir()`
* `Path.is_file()`
* `Path.suffix`
* `Path.exists()`
* `Path.mkdir()`
* `Path.rename()`
* Dictionary-based categorization
* Sets
* List comprehensions
* Functions and parameters
* Conditional expressions
* File logging
* Duplicate filename handling
* Safe filesystem operations
* Dry-run design
* Exception-safe program structure
