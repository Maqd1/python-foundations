import os
import json
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from html_report import generate_html_report


# ============================================================
# CONFIGURATION
# ============================================================

CHUNK_SIZE = 50_000


# ============================================================
# DISPLAY HELPERS
# ============================================================

def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def print_success(message):
    print(f"✅ {message}")


def print_error(message):
    print(f"❌ {message}")


def print_info(message):
    print(f"ℹ️ {message}")


# ============================================================
# FILE LOADING
# ============================================================

def count_csv_rows(filepath):
    """Count CSV rows without loading the entire file."""
    try:
        with open(filepath, "rb") as file:
            return max(0, sum(1 for _ in file) - 1)
    except Exception:
        return 0


def load_csv(filepath, chunksize=CHUNK_SIZE):
    """Load CSV using chunks and show loading progress."""

    if not os.path.exists(filepath):
        print_error(f"File not found: {filepath}")
        return None

    print_header("📊 CSV DATA ANALYZER 📊")
    print(f"Loading: {filepath}")

    try:
        total_rows = count_csv_rows(filepath)

        chunks = []
        loaded_rows = 0

        reader = pd.read_csv(
            filepath,
            chunksize=chunksize,
            low_memory=False
        )

        for chunk in reader:
            chunks.append(chunk)
            loaded_rows += len(chunk)

            if total_rows:
                percentage = (loaded_rows / total_rows) * 100
                percentage = min(percentage, 100)
                print(
                    f"\rLoading: {percentage:6.2f}% "
                    f"({loaded_rows:,}/{total_rows:,} rows)",
                    end=""
                )
            else:
                print(
                    f"\rLoading: {loaded_rows:,} rows",
                    end=""
                )

        print()

        if not chunks:
            print_error("The CSV file contains no data.")
            return None

        df = pd.concat(chunks, ignore_index=True)

        print_success(
            f"Loaded {len(df):,} rows and {len(df.columns):,} columns."
        )

        return df

    except pd.errors.EmptyDataError:
        print_error("The CSV file is empty.")
        return None

    except pd.errors.ParserError as error:
        print_error(f"CSV parsing error: {error}")
        return None

    except Exception as error:
        print_error(f"Error loading CSV: {error}")
        return None


# ============================================================
# COLUMN TYPE DETECTION
# ============================================================

def detect_column_types(df):
    """Automatically detect numeric, categorical, date and string columns."""

    column_types = {}

    for column in df.columns:
        series = df[column]

        # Numeric
        if pd.api.types.is_numeric_dtype(series):
            column_types[column] = "Numeric"
            continue

        non_missing = series.dropna()

        if non_missing.empty:
            column_types[column] = "Unknown"
            continue

        # Try numeric conversion
        numeric_values = pd.to_numeric(
            non_missing,
            errors="coerce"
        )

        if numeric_values.notna().mean() >= 0.95:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )
            column_types[column] = "Numeric"
            continue

        # Try date conversion
        date_values = pd.to_datetime(
            non_missing,
            format="mixed",
            errors="coerce"
        )

        if date_values.notna().mean() >= 0.95:
            df[column] = pd.to_datetime(
                df[column],
                format="mixed",
                errors="coerce"
            )
            column_types[column] = "Date"
            continue

        # Categorical vs string
        unique_count = non_missing.nunique()
        total_count = len(non_missing)

        if total_count > 0 and unique_count / total_count <= 0.20:
            column_types[column] = (
                f"Categorical ({unique_count:,} categories)"
            )
        else:
            column_types[column] = "String"

    return column_types


# ============================================================
# COLUMN SUMMARY
# ============================================================

def column_summary(df, column_types):
    print_header("📋 COLUMN SUMMARY")

    for column, column_type in column_types.items():

        missing = df[column].isna().sum()
        missing_percentage = (
            missing / len(df) * 100
            if len(df) > 0
            else 0
        )

        print(f"\n{column}")

        if column_type == "Numeric":
            minimum = df[column].min()
            maximum = df[column].max()

            print("  Type: Numeric")
            print(f"  Range: {minimum:,.2f} - {maximum:,.2f}")

        elif column_type == "Date":
            minimum = df[column].min()
            maximum = df[column].max()

            print("  Type: Date")
            print(f"  Range: {minimum} - {maximum}")

        elif column_type.startswith("Categorical"):
            categories = df[column].nunique(dropna=True)

            print("  Type: Categorical")
            print(f"  Categories: {categories:,}")

        else:
            print(f"  Type: {column_type}")

        print(
            f"  Missing: {missing:,} "
            f"({missing_percentage:.2f}%)"
        )


# ============================================================
# BASIC STATISTICS
# ============================================================

def calculate_statistics(df, column_types):
    """Calculate mean, median, mode, std, min and max."""

    statistics = {}

    print_header("📊 BASIC STATISTICS")

    numeric_columns = [
        column
        for column, column_type in column_types.items()
        if column_type == "Numeric"
    ]

    if not numeric_columns:
        print_info("No numeric columns found.")
        return statistics

    for column in numeric_columns:

        series = df[column].dropna()

        if series.empty:
            continue

        mode_values = series.mode()

        if mode_values.empty:
            mode = None
        else:
            mode = mode_values.iloc[0]

        missing = df[column].isna().sum()
        missing_percentage = (
            missing / len(df) * 100
            if len(df)
            else 0
        )

        statistics[column] = {
            "mean": float(series.mean()),
            "median": float(series.median()),
            "mode": float(mode) if mode is not None else None,
            "std_dev": float(series.std()),
            "min": float(series.min()),
            "max": float(series.max()),
            "missing": int(missing),
            "missing_percentage": float(missing_percentage)
        }

        print(f"\n{column}:")
        print(f"  Mean: {series.mean():,.2f}")
        print(f"  Median: {series.median():,.2f}")
        print(
            f"  Mode: "
            f"{mode:,.2f}"
            if mode is not None
            else "  Mode: None"
        )
        print(f"  Std Dev: {series.std():,.2f}")
        print(f"  Min: {series.min():,.2f}")
        print(f"  Max: {series.max():,.2f}")
        print(
            f"  Missing: {missing:,} "
            f"({missing_percentage:.2f}%)"
        )

    return statistics


# ============================================================
# FILTERING
# ============================================================

def filter_rows(df):
    """Filter rows using a pandas query expression."""

    print_header("🔎 FILTER DATA")

    print("Examples:")
    print("  Salary > 300000")
    print("  Age >= 30")
    print("  Dept == 'Engineering'")
    print("  Salary > 300000 and Age < 40")

    condition = input("\nEnter filter condition: ").strip()

    if not condition:
        print_info("No filter entered.")
        return df

    try:
        filtered_df = df.query(condition)

        print_success(
            f"Filtered {len(df):,} rows → "
            f"{len(filtered_df):,} rows."
        )

        return filtered_df

    except Exception as error:
        print_error(f"Invalid filter: {error}")
        return df


# ============================================================
# SORTING
# ============================================================

def sort_data(df):
    """Sort data by a selected column."""

    print_header("↕️ SORT DATA")

    print("Available columns:")
    for column in df.columns:
        print(f"  - {column}")

    column = input("\nSort by column: ").strip()

    if column not in df.columns:
        print_error(f"Column '{column}' does not exist.")
        return df

    order = input("Ascending or descending? [a/d]: ").strip().lower()

    ascending = order != "d"

    sorted_df = df.sort_values(
        by=column,
        ascending=ascending
    ).reset_index(drop=True)

    direction = "ascending" if ascending else "descending"

    print_success(
        f"Sorted by {column} ({direction})."
    )

    return sorted_df


# ============================================================
# GROUPING AND AGGREGATION
# ============================================================

def group_and_aggregate(df):
    """Group data and calculate aggregate statistics."""

    print_header("📊 GROUP BY")

    categorical_columns = [
        column
        for column in df.columns
        if not pd.api.types.is_numeric_dtype(df[column])
    ]

    if not categorical_columns:
        print_info("No suitable grouping columns found.")
        return None

    print("Available grouping columns:")
    for column in categorical_columns:
        print(f"  - {column}")

    group_column = input("\nGroup by: ").strip()

    if group_column not in df.columns:
        print_error(f"Column '{group_column}' does not exist.")
        return None

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if not numeric_columns:
        print_info("No numeric columns available for aggregation.")
        return None

    print("\nNumeric columns:")
    for column in numeric_columns:
        print(f"  - {column}")

    selected = input(
        "\nColumns to aggregate "
        "(comma-separated, blank = all): "
    ).strip()

    if selected:
        aggregate_columns = [
            column.strip()
            for column in selected.split(",")
            if column.strip() in numeric_columns
        ]
    else:
        aggregate_columns = numeric_columns

    if not aggregate_columns:
        print_error("No valid numeric columns selected.")
        return None

    grouped = (
        df.groupby(group_column)[aggregate_columns]
        .agg(["count", "mean", "sum", "min", "max"])
        .round(2)
    )

    print("\n")
    print(grouped.to_string())

    return grouped


# ============================================================
# CALCULATED COLUMNS
# ============================================================

def add_calculated_column(df):
    """Create a new column from an expression."""

    print_header("➕ ADD CALCULATED COLUMN")

    print("Examples:")
    print("  Salary * 0.10")
    print("  Salary / Age")
    print("  Years_Exp + Age")

    column_name = input(
        "\nNew column name: "
    ).strip()

    if not column_name:
        print_error("Column name cannot be empty.")
        return df

    expression = input(
        "Calculation expression: "
    ).strip()

    if not expression:
        print_error("Expression cannot be empty.")
        return df

    try:
        df[column_name] = df.eval(expression)

        print_success(
            f"Calculated column '{column_name}' added."
        )

        print("\nPreview:")
        print(df[[column_name]].head().to_string(index=False))

        return df

    except Exception as error:
        print_error(
            f"Could not calculate column: {error}"
        )
        return df


# ============================================================
# FREQUENCY / DISTRIBUTION ANALYSIS
# ============================================================

def distribution_analysis(df, column_types):
    """Create frequency tables for categorical columns."""

    print_header("📊 DISTRIBUTION ANALYSIS")

    print("Available columns:")
    for column in df.columns:
        print(f"  - {column}")

    column = input(
        "\nColumn for frequency analysis: "
    ).strip()

    if column not in df.columns:
        print_error(f"Column '{column}' does not exist.")
        return None

    frequency = (
        df[column]
        .value_counts(dropna=False)
        .rename_axis(column)
        .reset_index(name="Frequency")
    )

    frequency["Percentage"] = (
        frequency["Frequency"] / len(df) * 100
    ).round(2)

    print("\nFrequency Table:")
    print(frequency.to_string(index=False))

    return frequency


# ============================================================
# CORRELATION
# ============================================================

def correlation_analysis(df):
    """Calculate Pearson correlations between numeric columns."""

    print_header("📈 CORRELATION ANALYSIS")

    numeric_df = df.select_dtypes(
        include=np.number
    )

    if numeric_df.shape[1] < 2:
        print_info(
            "At least two numeric columns are required."
        )
        return None

    correlation_matrix = numeric_df.corr()

    print(correlation_matrix.round(2).to_string())

    print("\nPairwise correlations:")

    correlations = {}

    columns = numeric_df.columns.tolist()

    for first in range(len(columns)):
        for second in range(first + 1, len(columns)):

            column_1 = columns[first]
            column_2 = columns[second]

            value = correlation_matrix.loc[
                column_1,
                column_2
            ]

            if pd.isna(value):
                continue

            absolute_value = abs(value)

            if absolute_value >= 0.7:
                strength = "Strong"
            elif absolute_value >= 0.4:
                strength = "Moderate"
            elif absolute_value >= 0.2:
                strength = "Weak"
            else:
                strength = "Very Weak"

            direction = (
                "Positive"
                if value > 0
                else "Negative"
                if value < 0
                else "None"
            )

            key = f"{column_1} vs {column_2}"

            correlations[key] = {
                "coefficient": float(value),
                "strength": strength,
                "direction": direction
            }

            print(
                f"  {column_1} vs {column_2}: "
                f"{value:.2f} "
                f"({strength} {direction})"
            )

    return correlations


# ============================================================
# OUTLIER DETECTION
# ============================================================

def detect_outliers(df):
    """Detect outliers using the IQR method."""

    print_header("⚠️ OUTLIER DETECTION")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    all_outliers = {}

    found_outlier = False

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        mask = (
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        )

        outlier_rows = df[mask]

        if outlier_rows.empty:
            continue

        found_outlier = True

        all_outliers[column] = {
            "count": int(len(outlier_rows)),
            "lower_bound": float(lower_bound),
            "upper_bound": float(upper_bound)
        }

        print(f"\n{column}:")
        print(f"  Outliers: {len(outlier_rows):,}")
        print(f"  Lower Bound: {lower_bound:,.2f}")
        print(f"  Upper Bound: {upper_bound:,.2f}")

        identifier_columns = [
            column_name
            for column_name in df.columns
            if (
                "name" in column_name.lower()
                or column_name.lower() == "id"
                or column_name.lower().endswith("_id")
            )
        ]

        display_columns = []

        if identifier_columns:
            display_columns.append(
                identifier_columns[0]
            )

        display_columns.append(column)

        preview = outlier_rows[
            display_columns
        ].head(5)

        print("\n  Examples:")
        print(
            preview.to_string(index=False)
        )

    if not found_outlier:
        print_info("No IQR outliers detected.")

    return all_outliers


# ============================================================
# CHARTS
# ============================================================

def generate_charts(df, output_directory="charts"):
    """Generate histogram charts for numeric columns."""

    print_header("📊 GENERATING CHARTS")

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    if not numeric_columns:
        print_info("No numeric columns available.")
        return []

    os.makedirs(output_directory, exist_ok=True)

    chart_files = []

    for column in numeric_columns:

        data = df[column].dropna()

        if data.empty:
            continue

        safe_name = (
            str(column)
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        output_path = os.path.join(
            output_directory,
            f"{safe_name}_distribution.png"
        )

        plt.figure(figsize=(9, 5))

        plt.hist(
            data,
            bins=30,
            edgecolor="black"
        )

        plt.title(
            f"Distribution of {column}"
        )
        plt.xlabel(column)
        plt.ylabel("Frequency")

        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

        chart_files.append(output_path)

        print_success(
            f"Chart created: {output_path}"
        )

    return chart_files


# ============================================================
# CSV EXPORT
# ============================================================

def export_csv(df, output_path="analyzed_data.csv"):
    """Export the current DataFrame to CSV."""

    try:
        df.to_csv(
            output_path,
            index=False
        )

        print_success(
            f"CSV exported to: {output_path}"
        )

    except Exception as error:
        print_error(
            f"CSV export failed: {error}"
        )


# ============================================================
# JSON EXPORT
# ============================================================

def clean_for_json(value):
    """Convert pandas/numpy values into JSON-safe values."""

    if value is None:
        return None

    if isinstance(value, (np.integer,)):
        return int(value)

    if isinstance(value, (np.floating,)):
        if np.isnan(value):
            return None
        return float(value)

    if isinstance(value, (np.bool_,)):
        return bool(value)

    if isinstance(value, float) and math.isnan(value):
        return None

    return value


def export_json(
    df,
    column_types,
    statistics,
    correlations,
    outliers,
    output_path="analysis_report.json"
):
    """Export analysis results to JSON."""

    report = {
        "file": os.path.basename(
            getattr(df, "_source_file", "")
        ),
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist(),
        "column_types": column_types,
        "statistics": statistics,
        "correlations": correlations,
        "outliers": outliers
    }

    def clean_object(value):
        if isinstance(value, dict):
            return {
                str(key): clean_object(item)
                for key, item in value.items()
            }

        if isinstance(value, list):
            return [
                clean_object(item)
                for item in value
            ]

        return clean_for_json(value)

    report = clean_object(report)

    try:
        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        print_success(
            f"JSON report exported to: {output_path}"
        )

    except Exception as error:
        print_error(
            f"JSON export failed: {error}"
        )


# ============================================================
# PREVIEW
# ============================================================

def preview_data(df):
    print_header("👀 DATA PREVIEW")

    print(df.head(10).to_string(index=False))

    print(
        f"\nShowing first 10 of "
        f"{len(df):,} rows."
    )


# ============================================================
# MENU
# ============================================================

def show_menu():
    print("""
============================================================
📊 CSV DATA ANALYZER
============================================================

1.  Column Summary
2.  Basic Statistics
3.  Filter Rows
4.  Sort Data
5.  Group & Aggregate
6.  Add Calculated Column
7.  Distribution / Frequency Analysis
8.  Correlation Analysis
9.  Detect Outliers
10. Generate Charts
11. Export CSV
12. Export JSON
13. Generate HTML Report
14. Preview Data
15. Run Full Analysis
0.  Exit

============================================================
""")


# ============================================================
# FULL ANALYSIS
# ============================================================

def run_full_analysis(
    df,
    column_types
):
    """Run the complete analysis suite."""

    statistics = calculate_statistics(
        df,
        column_types
    )

    correlations = correlation_analysis(
        df
    )

    outliers = detect_outliers(
        df
    )

    return statistics, correlations, outliers


# ============================================================
# MAIN
# ============================================================

def main():

    filepath = input(
        "Enter path to CSV file: "
    ).strip()

    if not filepath:
        filepath = "employee_data.csv"

    df = load_csv(filepath)

    if df is None:
        return

    column_types = detect_column_types(df)

    statistics = {}
    correlations = {}
    outliers = {}

    while True:

        show_menu()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":

            column_summary(
                df,
                column_types
            )

        elif choice == "2":

            statistics = calculate_statistics(
                df,
                column_types
            )

        elif choice == "3":

            df = filter_rows(df)

            column_types = detect_column_types(df)

        elif choice == "4":

            df = sort_data(df)

        elif choice == "5":

            group_and_aggregate(df)

        elif choice == "6":

            df = add_calculated_column(df)

            column_types = detect_column_types(df)

        elif choice == "7":

            distribution_analysis(
                df,
                column_types
            )

        elif choice == "8":

            correlations = correlation_analysis(
                df
            )

        elif choice == "9":

            outliers = detect_outliers(
                df
            )

        elif choice == "10":

            generate_charts(df)

        elif choice == "11":

            output_path = input(
                "Output CSV filename "
                "[analyzed_data.csv]: "
            ).strip()

            if not output_path:
                output_path = "analyzed_data.csv"

            export_csv(
                df,
                output_path
            )

        elif choice == "12":

            if not statistics:
                statistics = calculate_statistics(
                    df,
                    column_types
                )

            if not correlations:
                correlations = correlation_analysis(
                    df
                ) or {}

            if not outliers:
                outliers = detect_outliers(
                    df
                )

            output_path = input(
                "Output JSON filename "
                "[analysis_report.json]: "
            ).strip()

            if not output_path:
                output_path = "analysis_report.json"

            export_json(
                df,
                column_types,
                statistics,
                correlations,
                outliers,
                output_path
            )

        elif choice == "13":

            if not statistics:
                statistics = calculate_statistics(
                    df,
                    column_types
                )

            if not correlations:
                correlations = correlation_analysis(
                    df
                ) or {}

            if not outliers:
                outliers = detect_outliers(
                    df
                )

            output_path = input(
                "Output HTML filename "
                "[analysis_report.html]: "
            ).strip()

            if not output_path:
                output_path = "analysis_report.html"

            generate_html_report(
                df,
                statistics,
                correlations,
                outliers,
                output_path
            )

        elif choice == "14":

            preview_data(df)

        elif choice == "15":

            statistics, correlations, outliers = (
                run_full_analysis(
                    df,
                    column_types
                )
            )

            generate_charts(df)

            print_success(
                "Full analysis completed."
            )

        elif choice == "0":

            print("\n👋 CSV Analyzer closed.")
            break

        else:

            print_error(
                "Invalid choice. Select 0-15."
            )


if __name__ == "__main__":
    main()
