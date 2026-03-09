import time
from functools import wraps
from typing import Callable, Any

def memoize(func: Callable) -> Callable:
    """Simple memoization decorator - caches all results indefinitely."""
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create hashable key
        key = (args, frozenset(kwargs.items()))
        
        # Return cached result if exists
        if key in cache:
            return cache[key]
        
        # Compute and cache
        result = func(*args, **kwargs)
        cache[key] = result
        return result

    # Cache management helpers
    wrapper.cache_clear = lambda: cache.clear()
    wrapper.cache_info = lambda: len(cache)

    return wrapper


def ttl_memoize(ttl: float = 60.0):
    """Memoize function results with TTL (seconds)."""
    def decorator(func: Callable) -> Callable:
        cache = {}  # {key: (result, timestamp)}

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            
            # Check cache
            if key in cache and now - cache[key][1] < ttl:
                return cache[key][0]
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result

        return wrapper
    return decorator

#### example:

@memoize()
def slow_fibonacci(n: int) -> int:
	pass

@ttl_memoize(ttl=5.0)  # 5 second cache
def slow_fibonacci(n: int) -> int:
	pass
