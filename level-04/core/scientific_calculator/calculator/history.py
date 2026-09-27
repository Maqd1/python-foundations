"""Calculation history: stores every calculation, supports undo/redo and JSON export/import.

NOTE ON FIELDS: the spec's add(operation, a, b, result) signature assumes every
entry is a clean two-operand op. That doesn't fit compound expressions like
"15 + 7 * 3" or multi-arg calls like "mean(1,2,3)" — so here `operation` holds
the full expression as typed, and `a`/`b` are kept for simple two-operand calls
where they're meaningful, else left as None. This keeps the same method names
and behavior the spec describes while actually working for every expression
the evaluator supports.
"""
import json
from datetime import datetime


class CalculationHistory:
    def __init__(self, max_size=100):
        self.history = []
        self.max_size = max_size
        self.redo_stack = []

    def add(self, operation, a, b, result):
        entry = {
            "id": len(self.history) + 1,
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "a": a,
            "b": b,
            "result": result,
        }
        self.history.append(entry)
        self.redo_stack.clear()  # a new calculation invalidates any pending redo
        if len(self.history) > self.max_size:
            self.history.pop(0)

    def undo(self):
        if not self.history:
            return None
        entry = self.history.pop()
        self.redo_stack.append(entry)
        return entry

    def redo(self):
        if not self.redo_stack:
            return None
        entry = self.redo_stack.pop()
        self.history.append(entry)
        return entry

    def get_last(self, n=1):
        return self.history[-n:] if n <= len(self.history) else self.history

    def clear(self):
        self.history = []
        self.redo_stack.clear()

    def export_history(self, filename):
        with open(filename, "w") as f:
            json.dump(self.history, f, indent=2)

    def import_history(self, filename):
        with open(filename, "r") as f:
            self.history = json.load(f)

    def get_statistics(self):
        if not self.history:
            return {"total_calculations": 0, "most_used_operations": [], "average_result": 0}

        op_counts = {}
        results = []
        for entry in self.history:
            op_counts[entry["operation"]] = op_counts.get(entry["operation"], 0) + 1
            if isinstance(entry["result"], (int, float)):
                results.append(entry["result"])

        total = len(self.history)
        most_used = sorted(op_counts.items(), key=lambda item: item[1], reverse=True)
        most_used_pct = [(op, count, count / total * 100) for op, count in most_used]

        return {
            "total_calculations": total,
            "most_used_operations": most_used_pct,
            "average_result": sum(results) / len(results) if results else 0,
        }
