import logging
import time
from datetime import UTC, datetime

from monitoring.metrics import get_metrics_collector

logger = logging.getLogger("stayza.monitoring.health")


class HealthChecker:
    def __init__(self):
        self._started_at = time.time()
        self._checks: dict[str, dict] = {}

    def register_check(self, name: str, check_fn, interval_seconds: int = 30):
        self._checks[name] = {
            "fn": check_fn,
            "interval": interval_seconds,
            "last_run": 0.0,
            "last_result": {"status": "unknown"},
        }

    def run_check(self, name: str) -> dict:
        check = self._checks.get(name)
        if not check:
            return {"status": "unknown", "error": f"No check registered: {name}"}
        try:
            result = check["fn"]()
            check["last_result"] = result
            check["last_run"] = time.time()
            return result
        except Exception as e:
            result = {"status": "unhealthy", "error": str(e)}
            check["last_result"] = result
            check["last_run"] = time.time()
            return result

    def run_all(self) -> dict:
        results = {}
        for name in self._checks:
            results[name] = self.run_check(name)
        return results

    def status(self, include_metrics: bool = False) -> dict:
        uptime_seconds = time.time() - self._started_at
        result = {
            "status": "healthy",
            "uptime_seconds": round(uptime_seconds, 2),
            "uptime_human": self._format_uptime(uptime_seconds),
            "started_at": datetime.fromtimestamp(self._started_at, tz=UTC).isoformat(),
            "checks": {},
        }
        all_healthy = True
        for name, check in self._checks.items():
            last = check.get("last_result", {"status": "unknown"})
            result["checks"][name] = {
                "status": last.get("status", "unknown"),
                "last_run": datetime.fromtimestamp(check["last_run"], tz=UTC).isoformat() if check["last_run"] else None,
            }
            if last.get("status") != "healthy":
                all_healthy = False

        if not all_healthy:
            result["status"] = "degraded"

        if include_metrics:
            metrics = get_metrics_collector().snapshot()
            result["metrics"] = metrics

        return result

    @staticmethod
    def _format_uptime(seconds: float) -> str:
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if days > 0:
            return f"{days}d {hours}h {minutes}m {secs}s"
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        if minutes > 0:
            return f"{minutes}m {secs}s"
        return f"{secs}s"

    def make_database_check(self, session_factory):
        def check():
            try:
                session = session_factory()
                session.execute(lambda: None)
                session.close()
                return {"status": "healthy"}
            except Exception as e:
                return {"status": "unhealthy", "error": str(e)}
        return check

    def make_provider_check(self, registry):
        def check():
            try:
                health = registry.health()
                all_ok = any(v for v in health.get("stt", {}).values()) or \
                         any(v for v in health.get("llm", {}).values()) or \
                         any(v for v in health.get("tts", {}).values())
                return {"status": "healthy" if all_ok else "degraded", "providers": health}
            except Exception as e:
                return {"status": "unhealthy", "error": str(e)}
        return check


_health_checker: HealthChecker | None = None


def get_health_checker() -> HealthChecker:
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker
