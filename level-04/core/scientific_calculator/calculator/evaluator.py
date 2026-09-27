"""Safe expression evaluator.

Deliberately does NOT use Python's eval() on the raw input string — eval()
on arbitrary user-typed text can execute arbitrary code (e.g. someone types
"__import__('os').system('rm -rf ~')" instead of a real expression). Instead
this parses the expression into an AST with ast.parse() and only walks a
small whitelist of node types (numbers, +/-/*//,**,%, unary minus, and calls
to a fixed table of known functions) — anything outside that whitelist is
rejected before it can run.
"""

import ast
import operator

from . import basic, scientific, statistical
from .plugins import get_plugin
from .utils import InvalidExpressionError, UnknownFunctionError

BIN_OPS = {
    ast.Add: basic.add,
    ast.Sub: basic.subtract,
    ast.Mult: basic.multiply,
    ast.Div: basic.divide,
    ast.Pow: basic.power,
    ast.Mod: basic.modulus,
    ast.FloorDiv: basic.floor_divide,
}

UNARY_OPS = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


class ExpressionEvaluator:
    def __init__(self, config):
        self.config = config

    def _function_table(self):
        degrees = self.config.settings["angle_mode"] == "DEG"
        return {
            "sqrt": scientific.sqrt,
            "log": scientific.log,
            "ln": scientific.ln,
            # bare sin/cos/tan respect the current angle mode; the _deg
            # variants are always available explicitly regardless of mode
            "sin": scientific.sin_deg if degrees else scientific.sin,
            "cos": scientific.cos_deg if degrees else scientific.cos,
            "tan": scientific.tan_deg if degrees else scientific.tan,
            "sin_deg": scientific.sin_deg,
            "cos_deg": scientific.cos_deg,
            "tan_deg": scientific.tan_deg,
            "factorial": scientific.factorial,
            "pi": scientific.pi,
            "e": scientific.e,
            "mean": statistical.mean,
            "median": statistical.median,
            "mode": statistical.mode,
            "variance": statistical.variance,
            "std_dev": statistical.std_dev,
            "correlation": statistical.correlation,
            "linear_regression": statistical.linear_regression,
        }

    def evaluate(self, expression):
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise InvalidExpressionError(f"Could not parse '{expression}': {exc}")
        return self._eval_node(tree.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise InvalidExpressionError(f"Unsupported literal: {node.value!r}")

        if isinstance(node, ast.List):
            return [self._eval_node(el) for el in node.elts]

        if isinstance(node, ast.BinOp):
            op_func = BIN_OPS.get(type(node.op))
            if op_func is None:
                raise InvalidExpressionError(f"Unsupported operator: {type(node.op).__name__}")
            return op_func(self._eval_node(node.left), self._eval_node(node.right))

        if isinstance(node, ast.UnaryOp):
            op_func = UNARY_OPS.get(type(node.op))
            if op_func is None:
                raise InvalidExpressionError(f"Unsupported unary operator: {type(node.op).__name__}")
            return op_func(self._eval_node(node.operand))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise InvalidExpressionError("Only simple function calls are supported.")
            name = node.func.id
            func = self._function_table().get(name) or get_plugin(name)
            if func is None:
                raise UnknownFunctionError(f"Unknown function: '{name}'")
            args = [self._eval_node(arg) for arg in node.args]
            return func(*args)

        if isinstance(node, ast.Name):
            table = self._function_table()
            if node.id in table:
                return table[node.id]()  # bare 'pi' / 'e' without parentheses
            raise InvalidExpressionError(f"Unknown name: '{node.id}'")

        raise InvalidExpressionError(f"Unsupported expression element: {type(node).__name__}")
