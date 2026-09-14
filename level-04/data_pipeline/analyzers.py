from collections import Counter
import math


def get_statistics(data):
    """Calculates mean, median, mode, and sample standard deviation."""
    if not data:
        return {"mean": 0, "median": 0, "mode": None, "std_dev": 0}

    n = len(data)
    mean_val = sum(data) / n

    # Median calculation
    sorted_d = sorted(data)
    mid = n // 2
    if n % 2 == 0:
        median_val = (sorted_d[mid - 1] + sorted_d[mid]) / 2.0
    else:
        median_val = float(sorted_d[mid])

    # Mode calculation
    counts = Counter(data)
    max_freq = max(counts.values())
    modes = [val for val, cnt in counts.items() if cnt == max_freq]
    mode_val = modes[0] if max_freq > 1 and len(modes) < n else None

    # Sample standard deviation
    if n > 1:
        variance = sum((x - mean_val) ** 2 for x in data) / (n - 1)
        std_dev_val = math.sqrt(variance)
    else:
        std_dev_val = 0.0

    return {
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "mode": mode_val,
        "std_dev": round(std_dev_val, 2),
    }


def get_correlation(x, y):
    """Calculates Pearson correlation coefficient between two numeric lists."""
    if len(x) != len(y) or len(x) < 2:
        return 0.0

    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denom_x = math.sqrt(sum((x[i] - mean_x) ** 2 for i in range(n)))
    denom_y = math.sqrt(sum((y[i] - mean_y) ** 2 for i in range(n)))

    if denom_x == 0 or denom_y == 0:
        return 0.0

    return round(numerator / (denom_x * denom_y), 4)


def get_quartiles(data):
    """Computes Q1, Q2 (Median), Q3, and Interquartile Range (IQR)."""
    if not data:
        return {"Q1": 0.0, "Q2": 0.0, "Q3": 0.0, "IQR": 0.0}

    sorted_d = sorted(data)
    n = len(sorted_d)

    def _median(lst):
        m = len(lst)
        if m == 0:
            return 0.0
        mid = m // 2
        return (
            (lst[mid - 1] + lst[mid]) / 2.0 if m % 2 == 0 else float(lst[mid])
        )

    q2 = _median(sorted_d)

    if n % 2 == 0:
        lower_half = sorted_d[: n // 2]
        upper_half = sorted_d[n // 2 :]
    else:
        lower_half = sorted_d[: n // 2]
        upper_half = sorted_d[n // 2 + 1 :]

    q1 = _median(lower_half)
    q3 = _median(upper_half)
    iqr = q3 - q1

    return {
        "Q1": round(q1, 2),
        "Q2": round(q2, 2),
        "Q3": round(q3, 2),
        "IQR": round(iqr, 2),
    }


def get_outliers(data):
    """Detects numerical outliers using 1.5 * IQR thresholds."""
    quartiles = get_quartiles(data)
    q1 = quartiles["Q1"]
    q3 = quartiles["Q3"]
    iqr = quartiles["IQR"]

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    return [x for x in data if x < lower_bound or x > upper_bound]