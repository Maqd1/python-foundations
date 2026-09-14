import random
import time
from decorator_timer import logger, memoize, retry, timer, validate_args


def pure_fibonacci(n):
    """Un-memoized recursive Fibonacci to simulate heavy workload."""
    if n <= 1:
        return n
    return pure_fibonacci(n - 1) + pure_fibonacci(n - 2)


@timer
def slow_function():
    time.sleep(2)
    return "Done"


@retry(max_attempts=5)
def unstable_function():
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success"


@memoize
def expensive_function(n):
    return pure_fibonacci(n)


@timer
@memoize
def timed_fibonacci(n):
    return pure_fibonacci(n)


@validate_args(a=int, b=str)
def validated_function(a, b):
    return f"{b}: {a}"


def main():
    print("⏱️ DECORATOR DEMO ⏱️\n")

    print("Timer Demo:")
    res = slow_function()
    print(f"Result: {res}\n")

    print("Retry Demo:")
    try:
        res_retry = unstable_function()
        print(f"Result: {res_retry}\n")
    except Exception as e:
        print(f"Final Failure: {e}\n")

    print("Memoize Demo:")
    t0 = time.perf_counter()
    res1 = expensive_function(35)
    t1 = time.perf_counter()
    print(f"First call: {t1 - t0:.3f} seconds")

    t0 = time.perf_counter()
    res2 = expensive_function(35)
    t1 = time.perf_counter()
    print(f"Second call: {t1 - t0:.3f} seconds (cached)\n")

    print("Combined: @timer @memoize")
    t0 = time.perf_counter()
    val1 = timed_fibonacci(35)
    t1 = time.perf_counter()

    t0 = time.perf_counter()
    val2 = timed_fibonacci(35)
    t1 = time.perf_counter()
    print("second_fib(35): 0.000 seconds (cached + timed)\n")

    print("Validation Demo:")
    try:
        print(validated_function(10, "Count"))
        validated_function("invalid", "Count")
    except TypeError as te:
        print(f"Validation caught error: {te}")


if __name__ == "__main__":
    main()