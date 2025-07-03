from functools import wraps
from typing import Callable


def silent(fallback: object = None) -> object:
    """Suppress all exceptions in a function and return fallback value (default: None)."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            try:
                return func(*args, **kwargs)
            except Exception:  # noqa: BLE001
                return fallback

        return wrapper

    return decorator
