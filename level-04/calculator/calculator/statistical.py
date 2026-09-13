"""Statistical operations. Most take *args; correlation/linear_regression take two lists."""
from collections import Counter


def mean(*args):
    if not args:
        raise ValueError("mean() requires at least one value.")
    return sum(args) / len(args)


def median(*args):
    if not args:
        raise ValueError("median() requires at least one value.")
    values = sorted(args)
    n = len(values)
    mid = n // 2
    if n % 2 == 0:
        return (values[mid - 1] + values[mid]) / 2
    return values[mid]


def mode(*args):
    if not args:
        raise ValueError("mode() requires at least one value.")
    counts = Counter(args)
    highest = max(counts.values())
    modes = [value for value, count in counts.items() if count == highest]
    return modes[0] if len(modes) == 1 else modes


def variance(*args):
    if not args:
        raise ValueError("variance() requires at least one value.")
    m = mean(*args)
    return sum((x - m) ** 2 for x in args) / len(args)


def std_dev(*args):
    return variance(*args) ** 0.5


def correlation(x_list, y_list):
    if len(x_list) != len(y_list) or len(x_list) < 2:
        raise ValueError("correlation() requires two equal-length lists of at least 2 values.")
    n = len(x_list)
    mean_x, mean_y = mean(*x_list), mean(*y_list)
    numerator = sum((x_list[i] - mean_x) * (y_list[i] - mean_y) for i in range(n))
    denom_x = sum((x - mean_x) ** 2 for x in x_list) ** 0.5
    denom_y = sum((y - mean_y) ** 2 for y in y_list) ** 0.5
    if denom_x == 0 or denom_y == 0:
        raise ValueError("correlation() is undefined when one list has zero variance.")
    return numerator / (denom_x * denom_y)


def linear_regression(x_list, y_list):
    if len(x_list) != len(y_list) or len(x_list) < 2:
        raise ValueError("linear_regression() requires two equal-length lists of at least 2 values.")
    n = len(x_list)
    mean_x, mean_y = mean(*x_list), mean(*y_list)
    numerator = sum((x_list[i] - mean_x) * (y_list[i] - mean_y) for i in range(n))
    denominator = sum((x - mean_x) ** 2 for x in x_list)
    if denominator == 0:
        raise ValueError("linear_regression() is undefined when all x values are identical.")
    slope = numerator / denominator
    intercept = mean_y - slope * mean_x
    return slope, intercept
