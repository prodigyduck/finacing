"""
Retry Decorator

Decorator for retry logic with exponential backoff for transient failures.
"""

import time
import functools
import logging
from typing import Callable, TypeVar, Any, Optional

# Type variable for function result
T = TypeVar('T')

logger = logging.getLogger(__name__)


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    on_final_failure: Optional[Callable[[Exception], Any]] = None,
):
    """
    Decorator for retry logic with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each attempt
        exceptions: Exception types to catch and retry

    Returns:
        Decorated function with retry logic
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    result = func(*args, **kwargs)

                    if attempt > 0:
                        logger.info(f"Success on attempt {attempt + 1}/{max_attempts}")

                    return result

                except exceptions as e:
                    last_exception = e

                    if attempt < max_attempts - 1:
                        wait_time = delay * (backoff_factor ** attempt)
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed. "
                            f"Retrying in {wait_time:.1f} seconds..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed. "
                            f"Last exception: {type(e).__name__}: {str(e)}"
                        )
                        # Call hook if provided before re-raising
                        if on_final_failure is not None:
                            try:
                                on_final_failure(e)
                            except Exception:
                                logger.exception("on_final_failure hook raised an exception")
                        raise

            # Fallback - re-raise last exception if somehow loop exits
            if last_exception is not None:
                raise last_exception

            # Should not reach here - defensive
            raise RuntimeError("retry decorator failed without capturing an exception")

        return wrapper

    return decorator
