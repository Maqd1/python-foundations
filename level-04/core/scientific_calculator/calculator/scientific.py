"""Scientific operations. sin/cos/tan take RADIANS; the _deg variants take degrees."""
import math


def sqrt(x):
    if x < 0:
        raise ValueError("Cannot take the square root of a negative number.")
    return math.sqrt(x)


def log(x, base=10):
    if x <= 0:
        raise ValueError("Logarithm is undefined for non-positive numbers.")
    return math.log(x, base)


def ln(x):
    if x <= 0:
        raise ValueError("Natural log is undefined for non-positive numbers.")
    return math.log(x)


def sin(x):
    return math.sin(x)


def cos(x):
    return math.cos(x)


def tan(x):
    return math.tan(x)


def sin_deg(x):
    return math.sin(math.radians(x))


def cos_deg(x):
    return math.cos(math.radians(x))


def tan_deg(x):
    return math.tan(math.radians(x))


def factorial(x):
    if x < 0 or x != int(x):
        raise ValueError("Factorial is only defined for non-negative whole numbers.")
    return math.factorial(int(x))


def pi():
    return math.pi


def e():
    return math.e
