# StayZa Milestone 9 — Integration Guide

## Milestone 8 Integration

Milestone 9 integrates with Milestone 8 (Voice Foundation / Pipecat) via REST APIs.

### Integration Flow

```
┌─────────────────────┐         POST /api/v1/analyze         ┌──────────────────────┐
│  Milestone 8        │ ──────────────────────────────────▶  │  Milestone 9         │
│  STT → Text         │                                      │  Language Engine     │
│  TTS ← Response     │ ◀────────────────────────────────── │  Intent → Action     │
└─────────────────────┘         JSON Response                └──────────────────────┘
```

### Integration Endpoints

The integration layer at `/api/v1/*` provides Milestone 8 compatible APIs:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/analyze` | Single utterance analysis with WER, CER, entity validation |
| POST | `/api/v1/evaluate` | Full evaluation pipeline (file-based or engine-based) |
| GET | `/api/v1/languages` | List supported languages with ISO codes |
| GET | `/api/v1/health` | Integration health check |

### Integration Service

The `IntegrationService` in `integration/service.py` handles:
- WER/CER computation between reference and hypothesis text
- Entity correctness validation
- Batch metric computation
- Full evaluation orchestration

### Security

Integration APIs support:
- API key authentication via `X-API-Key` header
- Rate limiting (100 req/60s)
- Request logging with rotating files
- In-memory caching for language lists

## Review System Integration

The Native Voice Review System integrates via:
- **Auto-flagging**: Low-confidence (<0.70) utterances are flagged during NLU pipeline
- **Conversation storage**: Full pipeline metadata stored for reviewer evaluation
- **Analytics**: Per-language and per-reviewer statistics

## Provider Integration

### Adding a New STT Provider

1. Create `providers/stt/new_provider.py`
2. Implement `STTProvider` ABC with `name()`, `is_available()`, `transcribe()`
3. Add config to `providers/config.py`
4. Register in `providers/registry.py` fallback chain
5. Export in `providers/__init__.py`

### Adding a New LLM Provider

Same pattern as STT, implement `LLMProvider` ABC.

### Adding a New TTS Provider

Same pattern as STT, implement `TTSProvider` ABC.

## Evaluation Engine Integration

The evaluation engine can be run:
- **Via API**: `POST /language/evaluation/run`
- **Programmatically**: `EvaluationEngine.run_full_evaluation()`
- **From integration**: `POST /api/v1/evaluate`

Results are stored in:
- JSON reports (`reports/`)
- PostgreSQL (`evaluation_reports` table)
- S3/MinIO (optional, with S3ObjectStorage)
