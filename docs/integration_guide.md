# Milestone 8 to Milestone 9 Integration Guide

## Architecture

```
M8 Voice Agent                    M9 Evaluation Engine
      │                                  │
      │  POST /api/v1/analyze            │
      │  POST /api/v1/evaluate           │
      │  GET  /api/v1/languages          │
      │  GET  /api/v1/health             │
      │─────────────────────────────────>│
      │                                  │
      │  JSON Response                   │
      │<─────────────────────────────────│
```

## Integration APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/analyze` | Analyze single utterance (WER, intent, entities) |
| POST | `/api/v1/evaluate` | Run full evaluation across all languages |
| GET | `/api/v1/languages` | List 6 supported Indian languages |
| GET | `/api/v1/health` | Integration service health check |
| GET | `/health` | Application health check |

## Authentication (Optional)

Set `INTEGRATION_API_KEY` env var, then pass `X-API-Key` header.

## Example: POST /api/v1/analyze

```json
{
  "text": "book a deluxe room",
  "language": "en-IN",
  "intent_label": "book_room",
  "entities": {"room_type": "deluxe"},
  "critical_fields": {"date": "2026-08-01"}
}
```

Response:
```json
{
  "utterance_id": "utt_abc123",
  "language": "en-IN",
  "word_error_rate": 0.0,
  "intent_correct": true,
  "entities_correct": 1,
  "critical_fields_correct": 1
}
```

## Example: POST /api/v1/evaluate

```json
{"count": 50}
```

Response provides per-language accuracy, WER, flow completion, latency scores, and pass/fail gates.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `INTEGRATION_API_KEY` | (empty) | API key for auth |
| `INTEGRATION_LOG_LEVEL` | INFO | Log level |
| `INTEGRATION_LOG_DIR` | logs/integration | Log directory |
