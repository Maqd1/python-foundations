import csv


filename = input("Enter filename: ")

try:
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

except FileNotFoundError:
    print(f"❌ File not found: {filename}")

else:
    print("\n📊 CSV READER 📊")
    print(f"📋 DATA LOADED ({len(rows)} rows):")

    if not rows:
        print("No data found.")
    else:
        print(f"Columns: {', '.join(rows[0].keys())}")

        for number, row in enumerate(rows, start=1):
            values = " | ".join(row.values())
            print(f"Row {number}: {values}")

        column = input("\nFilter by column: ").strip()
        value = input("Filter by value: ").strip()
        
        actual_column = next(
            (
                key
                for key in rows[0]
                if key.lower() == column.lower()
            ),
            None,
        )
        
        if actual_column is None:
            print(f"❌ Column not found: {column}")
        else:
            filtered_rows = [
                row
                for row in rows
                if row[actual_column].lower() == value.lower()
            ]
        
            print(f"\nRows found: {len(filtered_rows)}")
        
            for number, row in enumerate(filtered_rows, start=1):
                values = " | ".join(row.values())
                print(f"Row {number}: {values}")
        
            export = input(
                "\nExport filtered data? (y/n): "
            ).strip().lower()
        
            if export == "y" and filtered_rows:
                output_filename = f"{value.lower()}_employees.csv"
        
                with open(
                    output_filename,
                    "w",
                    newline=""
                ) as file:
                    writer = csv.DictWriter(
                        file,
                        fieldnames=rows[0].keys()
                    )
        
                    writer.writeheader()
                    writer.writerows(filtered_rows)
        
                print(
                    f"✅ Filtered data exported to "
                    f"{output_filename}"
                )