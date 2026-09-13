"""Command-line interface for the scientific calculator."""

from calculator import Calculator, CalculatorError


def format_result(entry, precision):
    value = entry["result"]
    if isinstance(value, (int, float)):
        return f"{entry['operation']} = {value:.{precision}f}"
    return f"{entry['operation']} = {value}"


def print_history(calc):
    print("\U0001f4dc Calculation History:")
    entries = calc.history.history
    if not entries:
        print("(empty)")
        return
    last_index = len(entries) - 1
    for i, entry in enumerate(entries):
        line = f"{i + 1}: {format_result(entry, calc.config.settings['precision'])}"
        if i == last_index:
            line += "  [undo available]"
        print(line)


def print_stats(calc):
    stats = calc.history.get_statistics()
    print("\U0001f4ca Usage Statistics:")
    if stats["total_calculations"] == 0:
        print("No calculations recorded yet.")
        return
    print("Most used operations:")
    for i, (op, count, pct) in enumerate(stats["most_used_operations"][:3], start=1):
        print(f"{i}. {op} ({pct:.0f}%)")
    print(f"\nAverage result: {stats['average_result']:.1f}")
    print(f"Total calculations: {stats['total_calculations']:,}")


def main():
    calc = Calculator()
    print("\U0001f9ee PYTHON SCIENTIFIC CALCULATOR v2.0 \U0001f9ee")
    print(f"\nMode: Scientific | Precision: {calc.config.settings['precision']} | "
          f"Angle: {calc.config.settings['angle_mode']}")

    while True:
        expr = input("\n>> ").strip()

        if expr == "quit":
            print("Goodbye! \U0001f44b")
            break
        elif expr == "":
            continue
        elif expr == "history()":
            print_history(calc)
        elif expr == "stats()":
            print_stats(calc)
        elif expr == "undo()":
            undone = calc.history.undo()
            if undone:
                print(f"\u2705 Undone: {format_result(undone, calc.config.settings['precision'])}")
            else:
                print("Nothing to undo.")
        elif expr == "redo()":
            redone = calc.history.redo()
            if redone:
                print(f"\u2705 Redone: {format_result(redone, calc.config.settings['precision'])}")
            else:
                print("Nothing to redo.")
        elif expr.startswith("save "):
            filename = expr[len("save "):].strip()
            calc.history.export_history(filename)
            print(f"\u2705 History saved to {filename}")
        elif expr.startswith("load "):
            filename = expr[len("load "):].strip()
            try:
                calc.history.import_history(filename)
                print(f"\u2705 History loaded from {filename}")
            except OSError as exc:
                print(f"Error: {exc}")
        else:
            try:
                result = calc.evaluate(expr)
                precision = calc.config.settings["precision"]
                if isinstance(result, (int, float)):
                    print(f"= {result:.{precision}f}")
                else:
                    print(f"= {result}")
            except (CalculatorError, ZeroDivisionError, ValueError, TypeError) as exc:
                print(f"Error: {exc}")


if __name__ == "__main__":
    main()
