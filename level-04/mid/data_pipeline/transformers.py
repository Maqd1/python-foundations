from functools import reduce


def filter_data(data, condition):
    """Filters data elements matching a predicate condition function."""
    return list(filter(condition, data))


def map_data(data, transform):
    """Transforms every item in data using a transform function."""
    return list(map(transform, data))


def reduce_data(data, operation, initial=None):
    """Reduces data elements to a single value using a binary operation."""
    if initial is not None:
        return reduce(operation, data, initial)
    return reduce(operation, data)


def clean_data(data, remove_nulls=True):
    """Cleans list of missing/None values and strips white spaces from strings."""
    cleaned = []
    for item in data:
        if remove_nulls and item is None:
            continue
        if isinstance(item, str):
            item = item.strip()
            if remove_nulls and not item:
                continue
        cleaned.append(item)
    return cleaned