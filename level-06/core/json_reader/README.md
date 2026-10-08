# JSON Reader — JSON Explorer with Query Language 🔍

A command-line JSON data explorer built with Python. It supports nested JSON navigation, JSONPath-like queries, filtering, SQL-style querying, aggregation, data transformation, validation, visualization, statistics, and large JSON streaming.

## Features

### JSON Loading
- Load JSON from a file
- Load JSON from a string
- Handle nested objects and arrays
- Stream large JSON arrays incrementally

### Navigation
- Dot notation queries
- Nested value access
- JSONPath-like queries
- Array filtering
- Find all occurrences of a key

### Query Language
Supports queries such as:

```text
SELECT name, age WHERE age > 25
SELECT name, address.city WHERE active = true
SELECT name WHERE name contains 'Damilola'
```

[200~Supported conditions:
- =
- !=
- >
- <
- >=
- <=
- contains
- AND
- OR

## Aggregation
Supports:
- COUNT
- SUM
- AVG
- MIN
- MAX
- GROUP BY
Examples:
SELECT COUNT(*)
SELECT SUM(age)
SELECT AVG(age)
SELECT address.city, COUNT(*) GROUP BY address.city
SELECT address.city, AVG(age) GROUP BY address.city

Data Transformation
- Rename keys
- Extract nested values to the top level
- Convert arrays to objects
- Add computed fields
Validation
- JSON Schema validation
- Required field validation
- Type validation
- Value range validation
Supported types include:
string
integer
number
boolean
array
object
null

## Visualization & Statistics
- Pretty-print JSON
- Colored JSON output
- Tree visualization
- Summary statistics
- Numeric field statistics
Export
- Export transformed or filtered JSON data
Project Structure
json_reader/
├── json_reader.py
├── README.md
└── users.json

## Requirements
Python 3.10+
Install the JSON Schema dependency:
pip install jsonschema

Running the Application
cd ~/myproject/python-foundations/level-06/core/json_reader
python json_reader.py

The application provides an interactive menu for exploring the JSON data.
Sample Data
The included users.json contains user records with:
- ID
- Name
- Email
- Age
- Address
- City
- State
- Country
- Active status
Example Operations
Dot notation
0.address.city

JSONPath-like query
$[*].name

Filter
age > 25

Query
SELECT name, age WHERE age > 25

Aggregation
SELECT COUNT(*)

Grouping
SELECT address.city, COUNT(*) GROUP BY address.city

Rename keys
name=full_name
email=contact_email

Extract nested value
Source: address.city
Target: city

Computed field
age_next_year = age + 1

Value range validation
age:18:100

## Concepts Practiced
This project practices:
- JSON parsing
- File handling
- Nested data structures
- Dictionaries and lists
- Recursive data traversal
- Query parsing
- Conditional evaluation
- Aggregation
- Grouping
- Data transformation
- JSON Schema validation
- Type validation
- Statistics
- Streaming large JSON data
- Command-line interfaces
- Error handling

## Verification
Syntax can be checked with:
python -m py_compile json_reader.py

