# CSV to List Converter

## Difficulty

Easy

## Description

A command-line tool that reads a CSV file, converts its rows into a list of dictionaries, displays the data, and allows the user to filter records by column and value.

## Features

* Reads CSV files using Python's `csv` module
* Uses `csv.DictReader` to convert rows into dictionaries
* Displays the CSV columns and records
* Allows filtering by column name
* Allows filtering by column value
* Handles column names case-insensitively
* Handles filter values case-insensitively
* Exports filtered records to a new CSV file
* Handles missing files gracefully

## Example

```text
Enter filename: employees.csv

📊 CSV READER 📊
📋 DATA LOADED (5 rows):
Columns: Name, Department, Salary, Age
Row 1: Damilola | Engineering | 450000 | 28
Row 2: John | Sales | 350000 | 35
Row 3: Alice | Marketing | 380000 | 30
Row 4: Fatima | Engineering | 500000 | 32
Row 5: David | Sales | 400000 | 29

Filter by column: department
Filter by value: engineering

Rows found: 2
Row 1: Damilola | Engineering | 450000 | 28
Row 2: Fatima | Engineering | 500000 | 32

Export filtered data? (y/n): y
✅ Filtered data exported to engineering_employees.csv
```

## Concepts

* CSV files
* `csv.DictReader`
* `csv.DictWriter`
* Lists
* Dictionaries
* List comprehensions
* Iteration
* Filtering
* Case-insensitive comparison
* File reading
* File writing
* Exception handling
* `FileNotFoundError`
* User input
* Formatted strings
