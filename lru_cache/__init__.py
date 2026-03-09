from collections import OrderedDict
from typing import Any

class LRUCache:
    def __init__(self, capacity: int):
        """
        Initialize LRU Cache with given capacity.
        Uses OrderedDict for O(1) operations.
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: Any) -> Any:
        """
        Get value by key. If exists, move to end (MRU).
        Returns None if key not found (change to -1 if ints expected).
        """
        if key not in self.cache:
            return None
        # Move to end to mark as recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        """
        Put key-value pair. If exists, update and move to end.
        If at capacity, evict LRU (first item) before adding.
        """
        if key in self.cache:
            # Update and move to end
            self.cache[key] = value
            self.cache.move_to_end(key)
        else:
            # New item
            if len(self.cache) >= self.capacity:
                # Evict LRU (pop first item)
                self.cache.popitem(last=False)
            self.cache[key] = value
            self.cache.move_to_end(key)  # Ensure at end

cache = LRUCache(2)
cache.put("user1", {"name": "Alice"})  # Key: str, Value: dict
cache.put(123, [1, 2, 3])             # Key: int, Value: list
print(cache.get("user1"))              # {"name": "Alice"}
cache.put("new", "value")              # Evicts 123 (LRU)
