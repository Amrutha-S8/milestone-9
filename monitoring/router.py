import time
import logging

from fastapi import APIRouter, Depends, Request

from monitoring.metrics import get_metrics_collector
from monitoring.health import get_health_checker

logger = logging.getLogger("stayza.monitoring.router")

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])


@router.get("/metrics", summary="Get application metrics")
async def get_metrics():
    collector = get_metrics_collector()
    return collector.snapshot()


@router.get("/health", summary="Get comprehensive health status")
async def get_health(request: Request, detailed: bool = False):
    checker = get_health_checker()
    if detailed:
        checker.run_all()
    return checker.status(include_metrics=True)


@router.get("/health/live", summary="Liveness probe")
async def liveness():
    return {"status": "alive"}


@router.get("/health/ready", summary="Readiness probe")
async def readiness(request: Request):
    engine = getattr(request.app.state, "evaluation_engine", None)
    if engine is None:
        return {"status": "not_ready", "reason": "evaluation_engine_not_initialized"}
    return {"status": "ready"}


class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start = time.perf_counter()
        method = scope.get("method", "UNKNOWN")
        path = scope.get("path", "/unknown")

        async def send_with_metrics(message):
            if message["type"] == "http.response.start":
                status = message.get("status", 0)
                duration = (time.perf_counter() - start) * 1000
                collector = get_metrics_collector()
                collector.increment(f"http_requests_total")
                collector.increment(f"http_{status}_total")
                collector.record_latency(f"http_request_duration_ms", duration)
                collector.record_latency(f"http_{method}_{path.replace('/', '_')}_duration_ms", duration)
            await send(message)

        await self.app(scope, receive, send_with_metrics)
