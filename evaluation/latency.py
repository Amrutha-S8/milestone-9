"""
Latency Metrics Profiler and per-language latency measurement.
"""

import time
import functools
from typing import Callable, Any, Dict, List


class LatencyProfiler:

    def __init__(self):
        self._latencies: List[float] = []
        self._language_latencies: Dict[str, List[float]] = {}

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

    def get_stats(self) -> Dict[str, float]:
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

    def get_language_stats(self) -> Dict[str, Dict[str, float]]:
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
        start = time.perf_counter()
        res = func(*args, **kwargs)
        return res
    return wrapper