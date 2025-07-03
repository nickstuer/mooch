import functools
import time
from typing import Callable


def retry(
    times: int = 3,
    delay: float = 1.0,
) -> Callable:
    def decorator(fn: callable) -> callable:
        @functools.wraps(fn)
        def wrapper(*args: object, **kwargs: object) -> object:
            for i in range(times):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    if i + 1 >= times:
                        raise
                time.sleep(delay)
            return None  # only reached if times is 0

        return wrapper

    return decorator
