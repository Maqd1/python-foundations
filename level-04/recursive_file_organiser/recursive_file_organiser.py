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