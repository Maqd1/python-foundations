from pathlib import Path


CATEGORY_RULES = {
    "IMAGES": {".jpg", ".jpeg", ".png", ".gif"},
    "DOCS": {".doc", ".docx", ".pdf"},
    "SPREADSHEETS": {".xls", ".xlsx", ".csv"},
    "TEXT": {".txt"},
}

def get_category(file):
    extension = file.suffix.lower()

    for category, extensions in CATEGORY_RULES.items():
        if extension in extensions:
            return category

    return "OTHERS"

def scan_directory(directory):
    files = [
        item
        for item in directory.iterdir()
        if item.is_file()
        and item.name != "organization_log.txt"
    ]

    return files

def group_files(files):
    grouped = {}

    for file in files:
        category = get_category(file)

        if category not in grouped:
            grouped[category] = []

        grouped[category].append(file)

    return grouped

def display_plan(grouped, dry_run=False):
    print("\nFiles by category:")

    for category, files in grouped.items():
        print(f"{category}: {len(files)} files")

    print("\nPlan:")

    for category, files in grouped.items():
        action = "Would create" if dry_run else "Create"

        print(
            f"{action} '{category}' folder "
            f"({len(files)} files)"
        )

def get_unique_destination(destination):
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_destination = destination.with_name(new_name)

        if not new_destination.exists():
            return new_destination

        counter += 1

def organize_files(grouped, dry_run=False):
    moved = 0
    log_entries = []

    for category, files in grouped.items():
        destination_folder = files[0].parent / category

        if not dry_run:
            destination_folder.mkdir(exist_ok=True)

        for file in files:
            destination = destination_folder / file.name
            destination = get_unique_destination(destination)

            if dry_run:
                print(
                    f"Would move: "
                    f"{file} -> {destination}"
                )
            else:
                file.rename(destination)

                log_entries.append(
                    f"{file} -> {destination}"
                )

                moved += 1

    return moved, log_entries

def save_log(directory, entries):
    log_file = directory / "organization_log.txt"

    with open(log_file, "w") as file:
        for entry in entries:
            file.write(entry + "\n")

    return log_file

directory_input = input("Enter directory to organize: ").strip()
directory = Path(directory_input)

if not directory.exists():
    print(f"❌ Directory not found: {directory}")
    raise SystemExit

if not directory.is_dir():
    print(f"❌ Not a directory: {directory}")
    raise SystemExit

print("\n📁 FILE ORGANIZER 📁")
print(f"Directory: {directory.resolve()}")

print("\n📊 Scanning files...")

files = scan_directory(directory)

print(f"Found: {len(files)} files")

grouped = group_files(files)

proceed = input("\nProceed? (y/n): ").strip().lower()

if proceed != "y":
    print("❌ Operation cancelled.")
    raise SystemExit

dry_run = input(
    "\nDry-run mode? (y/n): "
).strip().lower() == "y"

display_plan(grouped, dry_run)

if dry_run:
    print("\n👀 DRY-RUN MODE")
    organize_files(grouped, dry_run=True)
    print("\n✅ Dry run complete. No files were moved.")
else:
    print("\n🔄 Moving files...")

    moved, log_entries = organize_files(
        grouped,
        dry_run=False
    )

    log_file = save_log(directory, log_entries)

    print(f"✅ Moved {moved} files")
    print(f"📋 Log saved to: {log_file}")