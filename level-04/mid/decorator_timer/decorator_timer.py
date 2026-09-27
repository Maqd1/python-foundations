'''
🟡 Mid Level (2 Questions)
Q3: The Decorator Timer Module (Mid)

Create a module with decorators for timing and logging functions.

Requirements:

    Create decorators.py module with:

        @timer → Prints execution time

        @logger → Logs function calls with args

        @retry(max_attempts=3) → Retries on failure

        @memoize → Caches results for repeated calls

    The @timer decorator:
    python

    @timer
    def slow_function():
        time.sleep(2)
        return "Done"

    # Output: "slow_function took 2.001 seconds"

    The @retry decorator:
    python

    @retry(max_attempts=5)
    def unstable_function():
        import random
        if random.random() < 0.7:
            raise ValueError("Random failure!")
        return "Success"

    # Will retry up to 5 times

    The @memoize decorator:
    python

    @memoize
    def expensive_function(n):
        # Simulate expensive computation
        return fibonacci(n)

    # Second call with same argument is instant

    Create main.py that demonstrates all decorators

Bonus:

    Add @timeout(seconds) that stops function if it takes too long

    Add @validate_args that checks argument types

Sample Output:
text

⏱️ DECORATOR DEMO ⏱️

Timer Demo:
slow_function took 2.003 seconds
Result: Done

Retry Demo:
Attempt 1 failed: Random failure!
Attempt 2 failed: Random failure!
Attempt 3 succeeded!
Result: Success

Memoize Demo:
First call: 3.456 seconds
Second call: 0.000 seconds (cached)

Combined: @timer @memoize
first_fib(35): 2.345 seconds
second_fib(35): 0.000 seconds (cached + timed)

Concepts: Decorators, function wrappers, closure, functools.wraps, error handling, time module
'''

import functools
import time


def timer(func):
    """Measures and prints execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"{func.__name__} took {elapsed:.3f} seconds")
        return result

    return wrapper


def logger(func):
    """Logs function calls, positional arguments, and keyword arguments."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result!r}")
        return result

    return wrapper


def retry(max_attempts=3):
    """Retries a function call up to max_attempts on exception failure."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    print(f"Attempt {attempt} succeeded!")
                    return result
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        raise e

        return wrapper

    return decorator


def memoize(func):
    """Caches evaluation results based on positional and keyword arguments."""
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


def timeout(seconds):
    """Raises TimeoutError if execution duration exceeds specified seconds."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed > seconds:
                raise TimeoutError(
                    f"{func.__name__} exceeded timeout limit of {seconds}s (took {elapsed:.3f}s)"
                )
            return result

        return wrapper

    return decorator


def validate_args(**expected_types):
    """Validates argument types passed to the decorated function."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            code = func.__code__
            arg_names = code.co_varnames[: code.co_argcount]

            passed_args = dict(zip(arg_names, args))
            passed_args.update(kwargs)

            for arg_name, expected_type in expected_types.items():
                if arg_name in passed_args:
                    val = passed_args[arg_name]
                    if not isinstance(val, expected_type):
                        raise TypeError(
                            f"Argument '{arg_name}' must be of type {expected_type.__name__}, got {type(val).__name__}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator