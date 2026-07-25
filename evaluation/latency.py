"""
Latency Metrics Profiler and per-language latency measurement.
"""

import functools
import time
from collections.abc import Callable
from typing import Any


class LatencyProfiler:

    def __init__(self):
        self._latencies: list[float] = []
        self._language_latencies: dict[str, list[float]] = {}

    def measure(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> tuple[Any, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        latency_ms = round((end - start) * 1000, 2)
        self._latencies.append(latency_ms)
        return result, latency_ms

    def measure_language(self, func: Callable[..., Any], language: str, *args: Any, **kwargs: Any) -> tuple[Any, float]:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        latency_ms = round((end - start) * 1000, 2)
        self._latencies.append(latency_ms)
        if language not in self._language_latencies:
            self._language_latencies[language] = []
        self._language_latencies[language].append(latency_ms)
        return result, latency_ms

    def get_stats(self) -> dict[str, float]:
        if not self._latencies:
            return {"count": 0, "avg_ms": 0.0, "p50_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}

        sorted_lat = sorted(self._latencies)
        count = len(sorted_lat)
        avg = sum(sorted_lat) / count
        p50 = sorted_lat[int(count * 0.50)]

        return {
            "count": count,
            "avg_ms": round(avg, 2),
            "p50_ms": round(p50, 2),
            "min_ms": round(sorted_lat[0], 2),
            "max_ms": round(sorted_lat[-1], 2)
        }

    def get_language_stats(self) -> dict[str, dict[str, float]]:
        results = {}
        for lang, latencies in self._language_latencies.items():
            if not latencies:
                results[lang] = {"avg_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0, "count": 0}
                continue
            sorted_lat = sorted(latencies)
            count = len(sorted_lat)
            avg = sum(sorted_lat) / count
            results[lang] = {
                "count": count,
                "avg_ms": round(avg, 2),
                "p50_ms": round(sorted_lat[int(count * 0.50)], 2),
                "min_ms": round(sorted_lat[0], 2),
                "max_ms": round(sorted_lat[-1], 2)
            }
        return results

    def clear(self) -> None:
        self._latencies.clear()
        self._language_latencies.clear()


def profile_latency(func: Callable):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
