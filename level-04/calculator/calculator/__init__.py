"""Scientific Calculator package: ties together basic/scientific/statistical
operations, safe expression evaluation, history, and configuration."""

from . import plugins
from .config import CalculatorConfig
from .evaluator import ExpressionEvaluator
from .history import CalculationHistory
from .utils import CalculatorError, InvalidExpressionError, UnknownFunctionError, setup_logger

__version__ = "2.0"

__all__ = ["Calculator", "CalculatorError", "InvalidExpressionError", "UnknownFunctionError"]


class Calculator:
    def __init__(self, max_history=100):
        self.config = CalculatorConfig()
        self.config.set_history_size(max_history)
        self.history = CalculationHistory(max_size=max_history)
        self.evaluator = ExpressionEvaluator(self.config)
        self.logger = setup_logger()

    def evaluate(self, expression):
        result = self.evaluator.evaluate(expression)
        precision = self.config.settings["precision"]
        rounded = round(result, precision) if isinstance(result, (int, float)) else result
        self.history.add(operation=expression, a=None, b=None, result=rounded)
        self.logger.info(f"{expression} = {rounded}")
        return rounded

    def register_plugin(self, name, func):
        plugins.register_plugin(name, func)
