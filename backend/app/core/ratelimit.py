import asyncio
import time
from functools import wraps
from typing import Callable, Any

class AsyncTokenBucket:
    def __init__(self, capacity: float, fill_rate: float):
        """
        capacity: Maximum tokens in the bucket
        fill_rate: Tokens added per second
        """
        self.capacity = float(capacity)
        self.fill_rate = float(fill_rate)
        self.tokens = float(capacity)
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def consume(self, tokens: float = 1.0) -> None:
        while True:
            async with self._lock:
                now = time.monotonic()
                elapsed = now - self.last_update
                self.tokens = min(self.capacity, self.tokens + elapsed * self.fill_rate)
                self.last_update = now

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return
                
                # Calculate sleep time needed to get the required tokens
                deficit = tokens - self.tokens
                sleep_time = deficit / self.fill_rate
                
            # Sleep outside the lock
            await asyncio.sleep(sleep_time)

def with_exponential_backoff(max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        raise e
                    delay = min(max_delay, base_delay * (2 ** (retries - 1)))
                    await asyncio.sleep(delay)
        return wrapper
    return decorator
