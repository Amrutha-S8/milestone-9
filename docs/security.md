# StayZa Milestone 9 — Security Guide

## Security Architecture

### Authentication

- **Method**: API key via `X-API-Key` header
- **Implementation**: `ApiKeyAuth` class in `security.py`
- **Configuration**: `STAYZA_API_KEYS` env var (comma-separated)
- **Disable**: `STAYZA_DISABLE_API_AUTH=true`

### Authorization

- API keys validated per-request via FastAPI `Depends(require_api_key)`
- Key set managed via environment variables
- Integration endpoints protected by `ApiKeyDependency`

### Rate Limiting

- **Algorithm**: Sliding window (in-memory)
- **Default**: 100 requests per 60 seconds
- **Headers**: `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **Configuration**: `STAYZA_RATE_LIMIT_MAX`, `STAYZA_RATE_LIMIT_WINDOW`

### Secure Headers

All responses include:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Cache-Control: no-store
Permissions-Policy: geolocation=(), microphone=()
```

### CORS

- Configurable origins via `STAYZA_CORS_ORIGINS` (default: `*`)
- Applied via `CORSMiddleware` in FastAPI

### Request Size Limits

- **Maximum**: 10MB
- **Middleware**: `RequestSizeLimitMiddleware`
- **Response**: `413 Request Entity Too Large`

### Input Validation

- **Schema validation**: Pydantic v2 models with type constraints
- **Manual validation**: `validate_text_length()` for text fields
- **Bounds checking**: Rating values constrained to 0.0–10.0

### Secrets Management

- **Manager**: `SecretManager` in `providers/secrets.py`
- **Prefix**: All secrets via `STAYZA_*` environment variables
- **Template**: `.env.example` documents all required variables

### Dependency Security

- `requirements.txt` pinned with minimum versions
- CI/CD runs `bandit` for static analysis
- CI/CD runs `safety` for vulnerability scanning

## Security Audit

Run the security audit:

```bash
python scripts/security_audit.py
```

This checks:
- Authentication implementation
- Rate limiting correctness
- Secure headers presence
- Input validation edge cases
- Secrets management
- CORS configuration
- Dependency vulnerabilities
- File permissions

## Production Hardening Checklist

- [ ] API keys rotated regularly
- [ ] Rate limiting tuned for expected traffic
- [ ] CORS restricted to known origins
- [ ] HSTS enabled with preload
- [ ] Input validation for all endpoints
- [ ] Logging configured with appropriate retention
- [ ] Backups encrypted at rest
- [ ] Dependencies regularly updated
- [ ] Security scanning in CI/CD pipeline
- [ ] Audit logging enabled for sensitive operations
