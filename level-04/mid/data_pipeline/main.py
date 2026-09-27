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

from analyzers import (
    get_correlation,
    get_outliers,
    get_quartiles,
    get_statistics,
)
from exporters import to_csv, to_json, to_markdown
from transformers import clean_data, filter_data, map_data, reduce_data


def main():
    print("📊 DATA PIPELINE PACKAGE 📊\n")

    raw_data = [1, 5, 3, 7, 9, 2, 4, 6, 8, 10, 15, 100]
    print(f"Original Data: {raw_data}\n")

    # Pipeline transformations
    filtered = filter_data(raw_data, lambda x: x > 5)
    mapped = map_data(filtered, lambda x: x * 2)
    reduced = reduce_data(mapped, lambda acc, x: acc + x, initial=0)

    print(f"Filtered (>5): {filtered}")
    print(f"Mapped (doubled): {mapped}")
    print(f"Reduced (sum): {reduced}\n")

    # Analytical computations
    stats = get_statistics(raw_data)
    print("📊 Statistics:")
    print(f"Mean: {stats['mean']}")
    print(f"Median: {stats['median']}")
    print(f"Mode: {stats['mode']}")
    print(f"Std Dev: {stats['std_dev']}\n")

    quartiles = get_quartiles(raw_data)
    print("📊 Quartiles:")
    print(f"Q1: {quartiles['Q1']}")
    print(f"Q2: {quartiles['Q2']}")
    print(f"Q3: {quartiles['Q3']}")
    print(f"IQR: {quartiles['IQR']}\n")

    outliers = get_outliers(raw_data)
    print(f"⚠️ Outliers: {outliers}\n")

    # Exporters execution
    to_json(stats, "data.json")
    to_csv(raw_data, "data.csv")
    to_markdown(stats, "data.md")

    print("📁 Exported to:")
    print("- data.json")
    print("- data.csv")
    print("- data.md")


if __name__ == "__main__":
    main()