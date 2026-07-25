import time
import threading
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Counter:
    value: int = 0

    def inc(self, n: int = 1):
        self.value += n


@dataclass
class Histogram:
    values: list[float] = field(default_factory=list)

    def observe(self, value: float):
        self.values.append(value)

    @property
    def count(self) -> int:
        return len(self.values)

    @property
    def sum(self) -> float:
        return sum(self.values)

    @property
    def avg(self) -> float:
        return round(sum(self.values) / len(self.values), 2) if self.values else 0.0

    @property
    def p50(self) -> float:
        if not self.values:
            return 0.0
        sorted_v = sorted(self.values)
        return sorted_v[len(sorted_v) // 2]

    @property
    def p95(self) -> float:
        if not self.values:
            return 0.0
        sorted_v = sorted(self.values)
        idx = int(len(sorted_v) * 0.95)
        return sorted_v[min(idx, len(sorted_v) - 1)]

    @property
    def p99(self) -> float:
        if not self.values:
            return 0.0
        sorted_v = sorted(self.values)
        idx = int(len(sorted_v) * 0.99)
        return sorted_v[min(idx, len(sorted_v) - 1)]


@dataclass
class Gauge:
    value: float = 0.0

    def set(self, value: float):
        self.value = value

    def inc(self, delta: float = 1.0):
        self.value += delta

    def dec(self, delta: float = 1.0):
        self.value -= delta


class MetricsCollector:
    def __init__(self):
        self._lock = threading.RLock()
        self._counters: dict[str, Counter] = defaultdict(Counter)
        self._histograms: dict[str, Histogram] = defaultdict(Histogram)
        self._gauges: dict[str, Gauge] = defaultdict(Gauge)

    def counter(self, name: str) -> Counter:
        with self._lock:
            return self._counters[name]

    def histogram(self, name: str) -> Histogram:
        with self._lock:
            return self._histograms[name]

    def gauge(self, name: str) -> Gauge:
        with self._lock:
            return self._gauges[name]

    def increment(self, name: str, n: int = 1):
        with self._lock:
            self._counters[name].inc(n)

    def record_latency(self, name: str, value_ms: float):
        with self._lock:
            self._histograms[name].observe(value_ms)

    def set_gauge(self, name: str, value: float):
        with self._lock:
            self._gauges[name].set(value)

    def snapshot(self) -> dict:
        with self._lock:
            return {
                "counters": {k: v.value for k, v in self._counters.items()},
                "histograms": {
                    k: {
                        "count": v.count,
                        "sum": round(v.sum, 2),
                        "avg": v.avg,
                        "p50": round(v.p50, 2),
                        "p95": round(v.p95, 2),
                        "p99": round(v.p99, 2),
                    }
                    for k, v in self._histograms.items()
                },
                "gauges": {k: round(v.value, 2) for k, v in self._gauges.items()},
            }

    def reset(self):
        with self._lock:
            self._counters.clear()
            self._histograms.clear()
            self._gauges.clear()


_collector: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    global _collector
    if _collector is None:
        _collector = MetricsCollector()
    return _collector
