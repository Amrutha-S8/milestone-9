# StayZa Milestone 9 — API Reference

## Overview

The StayZa API provides multilingual language processing, evaluation, review management, and monitoring. All APIs are served from a single FastAPI application.

**Base URL:** `http://localhost:8000`
**OpenAPI Docs:** `/docs`
**ReDoc:** `/redoc`

## Authentication

Most endpoints require an API key via the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/language/detect
```

Authentication can be disabled via `STAYZA_DISABLE_API_AUTH=true`.

## Rate Limiting

- Default: 100 requests per 60 seconds per IP
- Configurable via `STAYZA_RATE_LIMIT_MAX` and `STAYZA_RATE_LIMIT_WINDOW`
- Rate limit headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Endpoints

### NLU Pipeline

| Method | Path | Description |
|--------|------|-------------|
| POST | `/language/detect` | Detect language of input text |
| POST | `/language/analyze` | Full NLU pipeline (detect → intent → entities → session) |
| GET | `/language/session/{session_id}` | Get multi-turn session context |
| GET | `/language/supported` | List supported languages |

### Evaluation

| Method | Path | Description |
|--------|------|-------------|
| POST | `/language/evaluation/run` | Run full evaluation engine |
| GET | `/language/evaluation/results` | Get latest evaluation results |
| GET | `/language/languages/status` | Get pass/fail status per language |
| GET | `/language/evaluate` | Run benchmark accuracy evaluation |

### Review System

| Method | Path | Description |
|--------|------|-------------|
| POST | `/reviews/reviewers` | Register a reviewer |
| GET | `/reviews/reviewers` | List reviewers |
| POST | `/reviews/conversations` | Store conversation |
| POST | `/reviews/create` | Create review with ratings |
| GET | `/reviews` | List paginated reviews |
| GET | `/reviews/{id}` | Get review by ID |
| PUT | `/reviews/{id}` | Update review |
| DELETE | `/reviews/{id}` | Delete review |
| GET | `/reviews/language/{language}` | Reviews by language |
| GET | `/reviews/analytics` | Review analytics |
| GET | `/reviews/reports/generate` | Generate JSON report |

### Monitoring

| Method | Path | Description |
|--------|------|-------------|
| GET | `/monitoring/metrics` | Application metrics |
| GET | `/monitoring/health` | Comprehensive health |
| GET | `/monitoring/health/live` | Liveness probe |
| GET | `/monitoring/health/ready` | Readiness probe |

### Integration (Milestone 8)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/analyze` | Analyze utterance |
| POST | `/api/v1/evaluate` | Run evaluation |
| GET | `/api/v1/languages` | List languages with codes |
| GET | `/api/v1/health` | Integration health |

### Health & Status

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root metadata |
| GET | `/health` | Legacy health check |
| GET | `/language/review/flagged` | Flagged utterances |

## Request Examples

### Language Detection

```json
POST /language/detect
{
  "text": "మాకు ఒక గది కావాలి"
}
```

Response:
```json
{
  "language": "Telugu",
  "confidence": 0.99,
  "script": "Telugu"
}
```

### Full Analysis

```json
POST /language/analyze
{
  "text": "I want to book a deluxe room for 2 adults tomorrow",
  "language": "English"
}
```

Response:
```json
{
  "language": "English",
  "intent": "booking",
  "confidence": 0.97,
  "entities": {
    "room_type": "deluxe",
    "guests": 2,
    "check_in": "tomorrow"
  },
  "next_action": "ask_checkin_date"
}
```

## Error Responses

```json
{
  "detail": "Valid API key required. Provide it via the X-API-Key header."
}
```

Status codes:
- `200` — Success
- `201` — Created
- `204` — Deleted (no content)
- `400` — Bad request
- `401` — Unauthorized (missing/invalid API key)
- `404` — Not found
- `413` — Request too large
- `422` — Validation error
- `429` — Rate limited
