# Q4: Data Pipeline Package

Create a data processing pipeline package that can transform, analyze, and export data.

## Requirements

Create the following package structure:

```text
data_pipeline/
├── __init__.py
├── transformers.py
├── analyzers.py
├── exporters.py
├── main.py
├── data.csv
├── data.json
└── data.md
1. Data Transformers

Create transformers.py containing functions for transforming data.

Implement functionality such as:

Filtering data
Sorting data
Mapping or modifying values
Cleaning data

Create:

filter_data(data, condition)

The condition should be callable, allowing functions such as lambda expressions to be used.

Example:

filtered = filter_data(
    data,
    lambda item: item["age"] > 18
)
2. Data Analyzers

Create analyzers.py containing functions for analyzing data.

Implement functionality such as:

Counting records
Calculating totals
Calculating averages
Finding minimum and maximum values
Generating useful statistics
3. Data Exporters

Create exporters.py containing functions for exporting processed data.

Support exporting data to formats such as:

CSV
JSON
Markdown
4. Main Program

Create main.py that:

Loads the sample data
Processes the data through the pipeline
Applies transformations
Performs analysis
Exports the results
Displays useful output
5. Sample Data

Include sample data files:

data.csv
data.json
data.md

Use them to demonstrate reading, processing, and exporting data.

Concepts
Python packages
Modules
Functions
Higher-order functions
Lambda functions
Data transformation
Data analysis
File handling
CSV
JSON
Markdown
Functional programming concepts
Modular architecture
Data pipelines
