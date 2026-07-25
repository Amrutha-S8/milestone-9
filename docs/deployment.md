# StayZa Milestone 9 — Production Deployment Guide

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         StayZa Platform                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐        │
│  │  FastAPI  │   │ Provider │   │ Storage  │   │ Metrics  │        │
│  │  App      │──▶│ Registry │──▶│ Layer    │──▶│ & Health │        │
│  │  Port 8000│   │ (STT/LLM │   │ (PG/S3)  │   │ Checks   │        │
│  │           │   │  /TTS)   │   │          │   │          │        │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘        │
│       │                                                             │
│       ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Logging (app/api/eval/error/audit channels)                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌────────────────────────────┐     │
│  │  Backup  │   │ Migrate  │   │  Security (Auth/Rate/CORS) │     │
│  │  Service │──▶│ Scripts  │──▶│                            │     │
│  └──────────┘   └──────────┘   └────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Provider Architecture

### STT Pipeline (Adapter Pattern)
```
Audio Input
    │
    ▼
┌─────────────────────┐
│  FallbackSTT        │
│  ┌───────────────┐  │
│  │ 1. Whisper    │──│──▶ Local whisper.cpp / OpenAI
│  │ 2. Deepgram   │──│──▶ Deepgram API (nova-2)
│  │ 3. Google STT │──│──▶ Google Cloud Speech-to-Text
│  └───────────────┘  │
└─────────────────────┘
    │
    ▼
  STTResult{text, confidence, language, duration_ms}
```

### LLM Pipeline
```
Text Input
    │
    ▼
┌─────────────────────┐
│  FallbackLLM        │
│  ┌───────────────┐  │
│  │ 1. GPT-4o     │──│──▶ OpenAI / Azure OpenAI
│  │ 2. Claude     │──│──▶ Anthropic Claude
│  └───────────────┘  │
└─────────────────────┘
    │
    ▼
  LLMResult{text, intent, confidence, duration_ms}
```

### TTS Pipeline
```
Text Input
    │
    ▼
┌─────────────────────┐
│  FallbackTTS        │
│  ┌───────────────┐  │
│  │ 1. Azure TTS  │──│──▶ Azure Cognitive Services
│  │ 2. OpenAI TTS │──│──▶ OpenAI TTS API
│  └───────────────┘  │
└─────────────────────┘
    │
    ▼
  TTSResult{audio_data, duration_ms, format}
```

## Fallback Logic

Each provider implements `is_available()` and `transcribe/analyze/synthesize()`.

The fallback chain iterates through providers in order:
1. Check `is_available()` — skip if unavailable
2. Attempt operation — catch exceptions
3. On failure, log error and try next provider
4. If all fail, raise `RuntimeError("All providers failed")`

## Database Design

### SQLite (dev) / PostgreSQL (prod)

| Table | Purpose |
|-------|---------|
| `reviewers` | Native language reviewers |
| `conversations` | Stored utterances with pipeline metadata |
| `reviews` | Review linking conversation to reviewer |
| `ratings` | 6-category rating per review |
| `approvals` | Approval status per review |
| `approval_history` | Full audit trail of status changes |
| `evaluation_reports` | Persistent evaluation reports |
| `language_scores` | Historical language quality scores |
| `benchmark_results` | Benchmark accuracy records |
| `latency_history` | Per-language latency measurements |

## Security

| Measure | Implementation |
|---------|---------------|
| API Key Auth | `X-API-Key` header validation via `ApiKeyAuth` |
| Rate Limiting | In-memory sliding window (default 100 req/60s) |
| Secure Headers | `X-Content-Type-Options`, `X-Frame-Options`, `HSTS`, etc. |
| CORS | Configurable origins via `STAYZA_CORS_ORIGINS` |
| Request Size Limit | 10MB max body via `RequestSizeLimitMiddleware` |
| Secret Management | All secrets via `STAYZA_*` env vars with `SecretManager` |
| Input Validation | Pydantic schemas + manual validation in endpoints |

## Monitoring

| Endpoint | Purpose |
|----------|---------|
| `GET /monitoring/metrics` | Application metrics snapshot |
| `GET /monitoring/health` | Comprehensive health status |
| `GET /monitoring/health/live` | Liveness probe (K8s) |
| `GET /monitoring/health/ready` | Readiness probe (K8s) |

Metrics tracked:
- HTTP request count by status
- Request latency (avg, p50, p95, p99)
- Provider availability
- Evaluation scores per language
- Active language statuses

## Logging Channels

| Channel | Path | Content |
|---------|------|---------|
| Application | `logs/application/` | General app events |
| API | `logs/api/` | HTTP request/response logs |
| Evaluation | `logs/evaluation/` | Evaluation run results |
| Error | `logs/error/` | Warnings and errors |
| Audit | `logs/audit/` | Security-relevant events |

All channels use rotating file handlers (10MB, 10 backups).

## Backup & Restore

```bash
# Create backup
python -c "from backup.service import BackupService; BackupService().create_backup()"

# List backups
python -c "from backup.service import BackupService; print(BackupService().list_backups())"

# Restore latest
python -c "from backup.service import RestoreService; rs=RestoreService(); bk=rs.list_available()[0]; rs.restore(bk['name'])"
```

## Environment Variables

```
# Providers
OPENAI_API_KEY=
AZURE_TTS_KEY=
AZURE_TTS_REGION=eastus
DEEPGRAM_API_KEY=
GOOGLE_APPLICATION_CREDENTIALS=
ANTHROPIC_API_KEY=
WHISPER_MODEL_SIZE=medium

# Storage
STORAGE_TYPE=postgres
PGHOST=localhost
PGPORT=5432
PGDATABASE=stayza
PGUSER=stayza
PGPASSWORD=
S3_ENDPOINT=
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_BUCKET=stayza-reports

# Security
STAYZA_API_KEYS=key1,key2
STAYZA_CORS_ORIGINS=*
STAYZA_DISABLE_API_AUTH=false
STAYZA_RATE_LIMIT_MAX=100
STAYZA_RATE_LIMIT_WINDOW=60

# Logging
STAYZA_LOG_DIR=logs
STAYZA_LOG_LEVEL=INFO
STAYZA_LOG_MAX_BYTES=10485760
STAYZA_LOG_BACKUP_COUNT=10

# Backup
STAYZA_BACKUP_DIR=backup
STAYZA_MAX_BACKUPS=30
```

## Running in Production

```bash
# Install
pip install -r requirements.txt

# Database init + seed
python -c "from review_system.database import init_db; init_db()"
python -c "from migrations.seed import seed_reviewers; from review_system.database import SessionLocal; seed_reviewers(SessionLocal())"

# Run
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --proxy-headers --forwarded-allow-ips '*'

# With Docker
docker build -t stayza-milestone9 .
docker run -p 8000:8000 --env-file .env stayza-milestone9
```
