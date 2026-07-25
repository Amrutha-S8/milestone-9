import os
import time
import logging
from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.middleware.base import BaseHTTPMiddleware

from providers.secrets import get_secret_manager

logger = logging.getLogger("stayza.security")

API_KEY_HEADER = "X-API-Key"
RATE_LIMIT_HEADER = "X-RateLimit-Remaining"
RATE_LIMIT_RESET_HEADER = "X-RateLimit-Reset"
REQUEST_ID_HEADER = "X-Request-Id"
MAX_REQUEST_SIZE = 10 * 1024 * 1024


class ApiKeyAuth:
    def __init__(self, api_keys: Optional[set[str]] = None):
        self._api_keys = api_keys or set()
        secrets = get_secret_manager()
        env_keys = secrets.get("API_KEYS", "")
        for key in env_keys.split(","):
            key = key.strip()
            if key:
                self._api_keys.add(key)

    def authenticate(self, api_key: Optional[str]) -> bool:
        if not self._api_keys:
            return True
        if api_key is None:
            return False
        return api_key in self._api_keys

    def add_key(self, api_key: str):
        self._api_keys.add(api_key)


class InMemoryRateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._buckets: dict[str, list[float]] = {}

    def check(self, key: str) -> tuple[bool, int, int]:
        now = time.time()
        window_start = now - self._window_seconds
        timestamps = self._buckets.get(key, [])
        timestamps = [t for t in timestamps if t > window_start]

        if len(timestamps) >= self._max_requests:
            reset_at = int(window_start + self._window_seconds)
            return False, 0, reset_at

        timestamps.append(now)
        self._buckets[key] = timestamps
        remaining = self._max_requests - len(timestamps)
        reset_at = int(window_start + self._window_seconds)
        return True, remaining, reset_at


class SecureHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=()"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_requests: Optional[int] = None, window_seconds: Optional[int] = None):
        super().__init__(app)
        secrets = get_secret_manager()
        self._limiter = InMemoryRateLimiter(
            max_requests=max_requests or secrets.get_int("RATE_LIMIT_MAX", 100),
            window_seconds=window_seconds or secrets.get_int("RATE_LIMIT_WINDOW", 60),
        )

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        allowed, remaining, reset_at = self._limiter.check(client_ip)

        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": {
                        "code": "RATE_LIMITED",
                        "message": "Too many requests. Try again shortly.",
                    }
                },
                headers={
                    RATE_LIMIT_HEADER: "0",
                    RATE_LIMIT_RESET_HEADER: str(reset_at),
                    "Retry-After": str(int(reset_at - time.time())),
                },
            )

        response = await call_next(request)
        response.headers[RATE_LIMIT_HEADER] = str(remaining)
        response.headers[RATE_LIMIT_RESET_HEADER] = str(reset_at)
        return response


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, max_size: int = MAX_REQUEST_SIZE):
        super().__init__(app)
        self._max_size = max_size

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self._max_size:
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={"error": {"code": "REQUEST_TOO_LARGE", "message": f"Request body exceeds {self._max_size} bytes"}},
            )
        return await call_next(request)


def require_api_key(
    request: Request,
    x_api_key: Annotated[Optional[str], Header(alias=API_KEY_HEADER)] = None,
):
    secrets = get_secret_manager()
    if secrets.get_bool("DISABLE_API_AUTH", False):
        return
    auth = ApiKeyAuth()
    if not auth.authenticate(x_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Valid API key required. Provide it via the X-API-Key header.",
        )


ApiKeyDependency = Annotated[None, Depends(require_api_key)]


def validate_text_length(text: str, max_length: int = 10000) -> str:
    if not text or not text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Text field cannot be empty")
    if len(text) > max_length:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Text exceeds maximum length of {max_length} characters")
    return text.strip()


def get_cors_origins() -> list[str]:
    secrets = get_secret_manager()
    origins = secrets.get("CORS_ORIGINS", "*")
    if origins == "*":
        return ["*"]
    return [o.strip() for o in origins.split(",")]
