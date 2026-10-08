# CSV Analyzer 📊

A professional CSV data analysis tool built with Python, pandas, NumPy, and Matplotlib.

## Project Overview

The CSV Analyzer loads CSV files, automatically detects column types, performs statistical analysis, filters and sorts data, groups and aggregates records, detects correlations and outliers, generates charts, and exports analysis results in CSV, JSON, and HTML formats.

## Features

### Core Analysis
- CSV loading with chunked reading
- Automatic column type detection
- Numeric, categorical, and date detection
- Column summaries
- Mean
- Median
- Mode
- Standard deviation
- Minimum and maximum values
- Missing value detection

### Data Manipulation
- Filter rows using conditions
- Sort data by columns
- Group and aggregate data
- Add calculated columns
- Frequency/distribution analysis

### Advanced Analysis
- Pearson correlation analysis
- Correlation strength and direction
- IQR-based outlier detection
- Outlier examples
- Summary statistics

### Export
- Export analyzed data to CSV
- Export analysis results to JSON
- Generate HTML analysis reports
- Generate Matplotlib charts

### Performance
- Chunked CSV loading
- Progress display during loading
- Designed to support large CSV files

## Project Structure

```text
csv_analyzer/
├── csv_analyzer.py
├── html_report.py
├── employee_data.csv
├── analyzed_data.csv
├── analysis_report.json
├── analysis_report.html
├── charts/
│   ├── Age_distribution.png
│   ├── Salary_distribution.png
│   └── Years_Exp_distribution.png
└── README.md
```

[200~Technologies
- Python
- pandas
- NumPy
- Matplotlib

Running the Program
Activate the virtual environment:
source ../../../venv/bin/activate

Run the analyzer:
python csv_analyzer.py

Enter the path to a CSV file when prompted.
Menu
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
0. Exit

Sample Dataset
The included employee_data.csv contains employee information including:
- Name
- Department
- Salary
- Age
- Years of Experience
Tested Results
The analyzer was tested successfully with the included employee dataset.
Dataset
Rows: 10
Columns: 5

Statistics
Salary
Mean: 302,777.78
Median: 280,000.00
Mode: 240,000.00
Std Dev: 64,474.37
Min: 240,000.00
Max: 450,000.00
Missing: 1

Age
Mean: 31.30
Median: 30.50
Mode: 22.00
Std Dev: 5.54
Min: 22.00
Max: 41.00

Years_Exp
Mean: 7.80
Median: 6.50
Mode: 5.00
Std Dev: 4.76
Min: 1.00
Max: 16.00

Correlations
Salary vs Age: 0.57
Salary vs Years_Exp: 0.66
Age vs Years_Exp: 0.99

Outlier Detection
Salary outliers: 1
Lower Bound: 170,000.00
Upper Bound: 410,000.00
Outlier: John Smith — 450,000.00

Generated Charts
charts/Salary_distribution.png
charts/Age_distribution.png
charts/Years_Exp_distribution.png

## Export Tests
Successfully tested:
- CSV export
- JSON export
- HTML report generation
- Chart generation
- Data preview
- Full analysis

## Concepts Practiced
- CSV parsing
- pandas DataFrames
- NumPy statistics
- Data cleaning
- Missing data
- Filtering
- Sorting
- Grouping and aggregation
- Frequency analysis
- Correlation
- Outlier detection
- IQR
- HTML generation
- JSON generation
- CSV export
- Matplotlib visualization
- Chunked file processing
- Progress indicators
