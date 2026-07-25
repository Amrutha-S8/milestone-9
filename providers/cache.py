import hashlib
import time
import threading
from typing import Any, Optional, Callable


class LRUCache:
    def __init__(self, max_size: int = 1024, default_ttl_seconds: int = 300):
        self._max_size = max_size
        self._default_ttl = default_ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = threading.RLock()

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            expires_at, value = entry
            if time.time() > expires_at:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        with self._lock:
            if len(self._store) >= self._max_size:
                oldest = min(self._store.keys(), key=lambda k: self._store[k][0])
                del self._store[oldest]
            ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
            self._store[key] = (time.time() + ttl, value)

    def delete(self, key: str):
        with self._lock:
            self._store.pop(key, None)

    def clear(self):
        with self._lock:
            self._store.clear()

    def make_key(self, prefix: str, *args, **kwargs) -> str:
        parts = [prefix]
        parts.extend(str(a) for a in args)
        if kwargs:
            parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        raw = ":".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()[:32]

    def __len__(self) -> int:
        with self._lock:
            return len(self._store)


class BatchedProcessor:
    def __init__(self, batch_size: int = 32):
        self._batch_size = batch_size

    def process(self, items: list, processor_fn: Callable[[list], list]) -> list:
        results = []
        for i in range(0, len(items), self._batch_size):
            batch = items[i:i + self._batch_size]
            results.extend(processor_fn(batch))
        return results


class LazyLoader:
    def __init__(self, loader_fn: Callable[[], Any], ttl_seconds: int = 300):
        self._loader_fn = loader_fn
        self._ttl = ttl_seconds
        self._value: Optional[Any] = None
        self._loaded_at: float = 0
        self._lock = threading.RLock()

    def get(self) -> Any:
        with self._lock:
            if time.time() - self._loaded_at > self._ttl or self._value is None:
                self._value = self._loader_fn()
                self._loaded_at = time.time()
            return self._value

    def invalidate(self):
        with self._lock:
            self._loaded_at = 0
            self._value = None


_default_cache: Optional[LRUCache] = None


def get_cache(max_size: int = 1024, default_ttl_seconds: int = 300) -> LRUCache:
    global _default_cache
    if _default_cache is None:
        _default_cache = LRUCache(max_size=max_size, default_ttl_seconds=default_ttl_seconds)
    return _default_cache
