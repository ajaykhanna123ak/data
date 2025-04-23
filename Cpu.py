import psutil
import os
import time
import functools
import inspect
import logging

def log_resource_usage(logger=logging):
    def decorator(func):
        func_name = func.__name__

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                process = psutil.Process(os.getpid())
                start_cpu = process.cpu_percent(interval=None)
                start_time = time.time()

                result = await func(*args, **kwargs)

                end_cpu = process.cpu_percent(interval=None)
                mem_info = process.memory_info()
                duration = time.time() - start_time

                logger.info(
                    f"[ASYNC] Function '{func_name}' — CPU: {end_cpu:.2f}%, "
                    f"Memory: {mem_info.rss / 1024**2:.2f} MB, Duration: {duration:.2f}s"
                )
                return result
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                process = psutil.Process(os.getpid())
                start_cpu = process.cpu_percent(interval=None)
                start_time = time.time()

                result = func(*args, **kwargs)

                end_cpu = process.cpu_percent(interval=None)
                mem_info = process.memory_info()
                duration = time.time() - start_time

                logger.info(
                    f"[SYNC] Function '{func_name}' — CPU: {end_cpu:.2f}%, "
                    f"Memory: {mem_info.rss / 1024**2:.2f} MB, Duration: {duration:.2f}s"
                )
                return result
            return sync_wrapper
    return decorator
