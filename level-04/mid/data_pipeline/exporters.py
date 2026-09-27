import json


def to_json(data, filename):
    """Exports dataset or analysis dict to a formatted JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def to_csv(data, filename):
    """Exports list or key-value dictionary to a CSV file."""
    with open(filename, "w") as f:
        if isinstance(data, dict):
            f.write("Metric,Value\n")
            for k, v in data.items():
                f.write(f"{k},{v}\n")
        elif isinstance(data, list):
            f.write("Value\n")
            for item in data:
                f.write(f"{item}\n")


def to_markdown(data, filename):
    """Exports data to a formatted Markdown table file."""
    with open(filename, "w") as f:
        if isinstance(data, dict):
            f.write("| Metric | Value |\n")
            f.write("| --- | --- |\n")
            for k, v in data.items():
                f.write(f"| {k} | {v} |\n")
        elif isinstance(data, list):
            f.write("| Index | Value |\n")
            f.write("| --- | --- |\n")
            for idx, item in enumerate(data, 1):
                f.write(f"| {idx} | {item} |\n")