"""Shared utilities: custom exceptions, logging setup, unit conversions."""
import logging


class CalculatorError(Exception):
    """Base exception for all calculator-specific errors."""


class InvalidExpressionError(CalculatorError):
    """Raised when an expression can't be parsed or evaluated safely."""


class UnknownFunctionError(CalculatorError):
    """Raised when an expression calls a function the calculator doesn't recognize."""


def setup_logger(log_file="calculator.log"):
    logger = logging.getLogger("calculator")
    logger.setLevel(logging.INFO)
    if not logger.handlers:  # avoid duplicate log lines if this is called more than once
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
        logger.addHandler(handler)
    return logger


# --- Unit conversions ---

def convert_length(value, from_unit, to_unit):
    to_meters = {"mm": 0.001, "cm": 0.01, "m": 1, "km": 1000, "in": 0.0254, "ft": 0.3048, "mi": 1609.34}
    if from_unit not in to_meters or to_unit not in to_meters:
        raise ValueError(f"Unsupported length unit. Choose from {list(to_meters)}.")
    return value * to_meters[from_unit] / to_meters[to_unit]


def convert_weight(value, from_unit, to_unit):
    to_grams = {"mg": 0.001, "g": 1, "kg": 1000, "oz": 28.3495, "lb": 453.592}
    if from_unit not in to_grams or to_unit not in to_grams:
        raise ValueError(f"Unsupported weight unit. Choose from {list(to_grams)}.")
    return value * to_grams[from_unit] / to_grams[to_unit]


def convert_temperature(value, from_unit, to_unit):
    from_unit, to_unit = from_unit.upper(), to_unit.upper()
    if from_unit == to_unit:
        return value

    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "K":
        celsius = value - 273.15
    else:
        raise ValueError("Temperature unit must be 'C', 'F', or 'K'.")

    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return celsius * 9 / 5 + 32
    elif to_unit == "K":
        return celsius + 273.15
    else:
        raise ValueError("Temperature unit must be 'C', 'F', or 'K'.")
