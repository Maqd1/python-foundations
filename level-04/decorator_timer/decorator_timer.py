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

