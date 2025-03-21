import logging
import memory_profiler
import asyncio
from functools import wraps

import logging

# root_logger = logging.getLogger()
# if not root_logger.handlers:
#     handler = logging.StreamHandler()  # Add a default handler if none exist
#     root_logger.addHandler(handler)

# root_logger.handlers[0].setFormatter(logging.Formatter("%(name)s: %(message)s"))
# profiler_logstream = memory_profiler.LogFile('memory_profiler_logs', True)

def memory_profiler_wrapper(func):
    """Decorator to apply memory profiling and logging for both sync & async functions."""
    profiled_func = memory_profiler.profile(func)  # Apply memory profiling

    if asyncio.iscoroutinefunction(func):  # Check if function is async
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            print(f"Executing async function: {func.__name__}")
            result = await profiled_func(*args, **kwargs)  # Await async function
            print(f"Async function '{func.__name__}' execution completed.")
            return result
        return async_wrapper

    else:  # Handle synchronous function
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            print(f"Executing function: {func.__name__}")
            result = profiled_func(*args, **kwargs)  # Execute sync function
            print("Function '{func.__name__}' execution completed.")
            return result
        return sync_wrapper

# Example Synchronous Function
@memory_profiler_wrapper
def sync_example():
    """A sample sync function."""
    data = [i for i in range(100000)]  # Allocate memory
    return sum(data)

# Example Asynchronous Function
@memory_profiler_wrapper
async def async_example():
    """A sample async function."""
    await asyncio.sleep(1)  # Simulate async task
    data = [i for i in range(100000)]  # Allocate memory
    return sum(data)

# Run both sync and async functions
if __name__ == "__main__":
    print("Running sync function...")
    sync_result = sync_example()
    print(f"Sync Result: {sync_result}")

    print("Running async function...")
    asyncio.run(async_example())  # Run async function in event loop
