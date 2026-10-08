import html
import os


def format_number(value):
    if value is None:
        return ""

    if isinstance(value, float):
        return f"{value:,.2f}"

    if isinstance(value, int):
        return f"{value:,}"

    return html.escape(str(value))


def generate_html_report(
    df,
    statistics,
    correlations,
    outliers,
    output_file="analysis_report.html",
):
    rows = len(df)
    columns = len(df.columns)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Data Analysis Report</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 40px;
            background: #f5f5f5;
            color: #222;
        }}

        .container {{
            max-width: 1200px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
        }}

        h1 {{
            margin-bottom: 10px;
        }}

        h2 {{
            margin-top: 35px;
            border-bottom: 2px solid #ddd;
            padding-bottom: 8px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background: #eee;
        }}

        .summary {{
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }}

        .card {{
            flex: 1;
            padding: 20px;
            background: #eee;
            border-radius: 8px;
        }}

        .warning {{
            color: #b00020;
            font-weight: bold;
        }}

        .positive {{
            color: #087f23;
            font-weight: bold;
        }}
    </style>
</head>

<body>
<div class="container">

    <h1>📊 CSV DATA ANALYSIS REPORT</h1>

    <div class="summary">
        <div class="card">
            <strong>Rows</strong>
            <br>
            {rows:,}
        </div>

        <div class="card">
            <strong>Columns</strong>
            <br>
            {columns}
        </div>
    </div>

    <h2>📋 Column Summary</h2>

    <table>
        <tr>
            <th>Column</th>
            <th>Type</th>
            <th>Missing</th>
            <th>Unique Values</th>
        </tr>
"""

    for column in df.columns:
        column_type = str(df[column].dtype)
        missing = int(df[column].isna().sum())
        unique = int(df[column].nunique(dropna=True))

        html_content += f"""
        <tr>
            <td>{html.escape(str(column))}</td>
            <td>{html.escape(column_type)}</td>
            <td>{missing:,}</td>
            <td>{unique:,}</td>
        </tr>
"""

    html_content += """
    </table>

    <h2>📊 Statistics</h2>

    <table>
        <tr>
            <th>Column</th>
            <th>Mean</th>
            <th>Median</th>
            <th>Mode</th>
            <th>Std Dev</th>
            <th>Min</th>
            <th>Max</th>
            <th>Missing</th>
        </tr>
"""

    for column, stats in statistics.items():
        html_content += f"""
        <tr>
            <td>{html.escape(str(column))}</td>
            <td>{format_number(stats.get("mean"))}</td>
            <td>{format_number(stats.get("median"))}</td>
            <td>{format_number(stats.get("mode"))}</td>
            <td>{format_number(stats.get("std_dev"))}</td>
            <td>{format_number(stats.get("min"))}</td>
            <td>{format_number(stats.get("max"))}</td>
            <td>{format_number(stats.get("missing"))}</td>
        </tr>
"""

    html_content += """
    </table>

    <h2>📈 Correlation Analysis</h2>

    <table>
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
            <th>Correlation</th>
            <th>Strength</th>
            <th>Direction</th>
        </tr>
"""

    if correlations:
        for pair, value in correlations.items():
            if isinstance(pair, tuple):
                column1, column2 = pair
            else:
                parts = str(pair).split(" vs ")

                if len(parts) == 2:
                    column1, column2 = parts
                else:
                    column1 = str(pair)
                    column2 = ""

            if isinstance(value, dict):
                coefficient = value.get("coefficient")
                strength = value.get("strength", "")
                direction = value.get("direction", "")

                coefficient_display = (
                    f"{float(coefficient):.2f}"
                    if coefficient is not None
                    else ""
                )
            else:
                coefficient_display = (
                    f"{float(value):.2f}"
                    if isinstance(value, (int, float))
                    else html.escape(str(value))
                )
                strength = ""
                direction = ""

            html_content += f"""
            <tr>
                <td>{html.escape(str(column1))}</td>
                <td>{html.escape(str(column2))}</td>
                <td>{coefficient_display}</td>
                <td>{html.escape(str(strength))}</td>
                <td>{html.escape(str(direction))}</td>
            </tr>
"""

    html_content += """
    </table>

    <h2>⚠️ Outlier Detection</h2>

    <table>
        <tr>
            <th>Column</th>
            <th>Number of Outliers</th>
        </tr>
"""

    if outliers:
        for column, values in outliers.items():
            count = values.get("count", 0)

            html_content += f"""
            <tr>
                <td>{html.escape(str(column))}</td>
                <td class="warning">{count:,}</td>
            </tr>
"""

    html_content += """
    </table>

</div>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(
        f"✅ HTML report exported to: "
        f"{os.path.abspath(output_file)}"
    )