import hashlib
import time
from typing import Any


class MemoryCache:
    def __init__(self, default_ttl_seconds: int = 300):
        self._store: dict[str, tuple[float, Any]] = {}
        self._default_ttl = default_ttl_seconds

    def get(self, key: str):
        entry = self._store.get(key)
        if entry is None:
            return None
        expires_at, value = entry
        if time.time() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: int | None = None):
        ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        self._store[key] = (time.time() + ttl, value)

    def delete(self, key: str):
        self._store.pop(key, None)

    def clear(self):
        self._store.clear()

    def make_key(self, prefix: str, *args, **kwargs):
        parts = [prefix]
        parts.extend(str(a) for a in args)
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            parts.extend(f"{k}={v}" for k, v in sorted_kwargs)
        raw = ":".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()[:32]


_cache: MemoryCache | None = None


def get_cache(default_ttl_seconds: int = 300) -> MemoryCache:
    global _cache
    if _cache is None:
        _cache = MemoryCache(default_ttl_seconds=default_ttl_seconds)
    return _cache
