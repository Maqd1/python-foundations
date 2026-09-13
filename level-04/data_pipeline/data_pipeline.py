'''
Q4: The Data Pipeline Package (Mid)

Create a package for data processing pipelines.

Requirements:

    Create package structure:
    text

    data_pipeline/
        __init__.py
        transformers.py
        analyzers.py
        exporters.py

    transformers.py: Functions that transform data

        filter_data(data, condition) → Filter using lambda

        map_data(data, transform) → Transform each item

        reduce_data(data, operation, initial) → Reduce to single value

        clean_data(data, remove_nulls=True) → Clean dirty data

    analyzers.py: Functions for analysis

        get_statistics(data) → Mean, median, mode, std

        get_correlation(x, y) → Pearson correlation

        get_quartiles(data) → Q1, Q2, Q3, IQR

        get_outliers(data) → Find outliers using IQR

    exporters.py: Export functions

        to_json(data, filename) → Export to JSON

        to_csv(data, filename) → Export to CSV

        to_markdown(data, filename) → Export to Markdown table

    __init__.py: Import the most useful functions

    Create main.py that demonstrates the pipeline

Sample Output:
text

📊 DATA PIPELINE PACKAGE 📊

Original Data: [1, 5, 3, 7, 9, 2, 4, 6, 8, 10, 15, 100]

Filtered (>5): [7, 9, 6, 8, 10, 15, 100]
Mapped (doubled): [14, 18, 12, 16, 20, 30, 200]
Reduced (sum): 310

📊 Statistics:
Mean: 14.17
Median: 6.5
Mode: None
Std Dev: 28.43

📊 Quartiles:
Q1: 4.0
Q2: 6.5
Q3: 9.5
IQR: 5.5

⚠️ Outliers: [100]

📁 Exported to:
- data.json
- data.csv
- data.md

Concepts: Package structure, lambda functions, functional programming, statistical calculations, file I/O, data transformation
'''