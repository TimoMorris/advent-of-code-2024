"""Decorator for timing runtime of functions.

Copied from: https://realpython.com/primer-on-python-decorators/#timing-functions
"""
import functools
import time


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Ran in {run_time:.4f} secs: {func.__name__}()")
        return result
    return wrapper_timer
