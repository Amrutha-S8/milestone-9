"""
Main FastAPI Application Entrypoint for StayZa Milestone 9: Language Flows, Evaluation, Review & Production Hardening.

Design Rationale:
- Clean FastAPI instantiation with OpenAPI metadata.
- Includes CORS, secure headers, rate limiting, request size limit middleware.
- Mounts all routers: language, integration, review, monitoring.
- Initializes production services: logging, provider registry, health checks.
"""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.dependencies import evaluation_engine
from api.router import router as language_router
from integration.router import router as integration_router
from logservice.service import get_logging_service
from monitoring.health import get_health_checker
from monitoring.router import MetricsMiddleware
from monitoring.router import router as monitoring_router
from providers.registry import get_provider_registry
from review_system.router import router as review_router
from security import (
    RateLimitMiddleware,
    RequestSizeLimitMiddleware,
    SecureHeadersMiddleware,
    get_cors_origins,
)

log_service = get_logging_service()
logger = log_service.application()

app = FastAPI(
    title="StayZa Milestone 9: Language Flows, Evaluation & Review API",
    description="Production-hardened module providing Language Detection, Intent Classification, Flow Transitions, Evaluation Metrics, Pronunciation Dictionaries, Native Voice Review System, Provider Integration, and Integration APIs for Milestone 8.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

cors_origins = get_cors_origins()
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SecureHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestSizeLimitMiddleware)
app.add_middleware(MetricsMiddleware)

app.state.evaluation_engine = evaluation_engine

provider_registry = get_provider_registry()
app.state.provider_registry = provider_registry

health_checker = get_health_checker()
try:
    from review_system.database import SessionLocal
    health_checker.register_check("database", health_checker.make_database_check(SessionLocal))
except Exception as e:
    logger.warning("Database health check not registered: %s", e)
health_checker.register_check("providers", health_checker.make_provider_check(provider_registry))

log_service.log_application("INFO", "StayZa Milestone 9 starting up")

app.include_router(language_router)
app.include_router(integration_router)
app.include_router(review_router)
app.include_router(monitoring_router)


@app.get("/", tags=["Health & Status"])
async def root():
    return {
        "module": "StayZa Milestone 9 - Language Flows, Evaluation & Review",
        "status": "healthy",
        "version": "1.0.0",
        "docs": "/docs",
        "monitoring": "/monitoring/health",
    }


@app.get("/health", tags=["Health & Status"])
async def health_check():
    return health_checker.status(include_metrics=False)


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("STAYZA_HOST", "0.0.0.0")
    port = int(os.getenv("STAYZA_PORT", "8000"))
    reload = os.getenv("STAYZA_RELOAD", "false").lower() == "true"
    workers = int(os.getenv("STAYZA_WORKERS", "1"))
    uvicorn.run("main:app", host=host, port=port, reload=reload, workers=workers)
