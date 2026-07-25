import hashlib
import time
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

API_KEY_HEADER = "X-API-Key"
RATE_LIMIT_HEADER = "X-RateLimit-Remaining"
RATE_LIMIT_RESET_HEADER = "X-RateLimit-Reset"


class ApiKeyAuth:
    def __init__(self, api_keys: set[str] | None = None):
        self._api_keys = api_keys or set()
        env_key = os.getenv("INTEGRATION_API_KEY", "")
        if env_key:
            self._api_keys.add(env_key)

    def authenticate(self, api_key: str | None) -> bool:
        if not self._api_keys:
            return True
        if api_key is None:
            return False
        return api_key in self._api_keys


import os


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
            remaining = 0
            reset_at = int(window_start + self._window_seconds)
            return False, remaining, reset_at

        timestamps.append(now)
        self._buckets[key] = timestamps
        remaining = self._max_requests - len(timestamps)
        reset_at = int(window_start + self._window_seconds)
        return True, remaining, reset_at


class RateLimitMiddleware:
    def __init__(self, app: ASGIApp, max_requests: int = 100, window_seconds: int = 60):
        self.app = app
        self._limiter = InMemoryRateLimiter(max_requests, window_seconds)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        client_ip = scope.get("client", ("unknown", 0))[0]
        allowed, remaining, reset_at = self._limiter.check(client_ip)

        if not allowed:
            response = JSONResponse(
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
            await response(scope, receive, send)
            return

        async def send_with_headers(message: Message):
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                if isinstance(headers, list):
                    headers.append((RATE_LIMIT_HEADER.encode(), str(remaining).encode()))
                    headers.append((RATE_LIMIT_RESET_HEADER.encode(), str(reset_at).encode()))
                    message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_headers)


def require_api_key(
    request: Request,
    x_api_key: Annotated[str | None, Header(alias=API_KEY_HEADER)] = None,
):
    auth = ApiKeyAuth()
    if not auth.authenticate(x_api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Valid API key required. Provide it via the X-API-Key header.",
        )


ApiKeyDependency = Annotated[None, Depends(require_api_key)]
