# StayZa Milestone 9 — Architecture

## System Overview

StayZa Milestone 9 is a production-hardened multilingual language processing engine for hotel booking voice conversations. It supports 6 Indian languages (English, Hindi, Hinglish, Telugu, Marathi, Malayalam) with automatic detection, intent classification, entity extraction, evaluation, and a native voice review system.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              StayZa Platform                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────────┐   ┌───────────────────┐   │
│  │ FastAPI   │──▶│ Providers│──▶│  Storage     │──▶│  Monitoring       │   │
│  │ (ASGI)    │   │ STT/LLM  │   │  PostgreSQL  │   │  Metrics/Health   │   │
│  │           │   │ /TTS     │   │  S3/MinIO    │   │                   │   │
│  └──────────┘   └──────────┘   └──────────────┘   └───────────────────┘   │
│       │              │               │                     │               │
│       ▼              ▼               ▼                     ▼               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Logging Service (5 channels: app, api, eval, error, audit)        │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│       │              │               │                     │               │
│       ▼              ▼               ▼                     ▼               │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  Backup Service  │  Migration    │  Security (Auth/CORS/Rate)      │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Processing Pipeline

```
Voice Input (M8)
    │
    ▼
┌──────────────┐
│ STT Provider │──▶ Whisper / Deepgram / Google STT (with fallback)
└──────┬───────┘
       ▼
┌──────────────────┐
│ Language Detect  │──▶ Unicode range + Hinglish lexicon detection
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Normalization    │──▶ lowercase → noise removal → abbreviation → transliteration
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Intent Classify  │──▶ LLM (GPT-4o / Claude) or keyword-based
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Entity Extract   │──▶ room_type, guests, check_in, booking_id, budget
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Session/Flow     │──▶ 8 intents, multi-turn state machine
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Evaluation       │──▶ accuracy, WER, flow completion, latency → score
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Review System    │──▶ human review, ratings, approval workflow
└──────┬───────────┘
       ▼
┌──────────────────┐
│ Final Response   │──▶ action + response template
└──────────────────┘
```

## Provider Architecture

All providers follow the **Adapter Pattern** with **Fallback Chain**:

| Service | Primary | Secondary | Tertiary |
|---------|---------|-----------|----------|
| STT | Whisper | Deepgram | Google STT |
| LLM | GPT-4o | Claude | — |
| TTS | Azure Neural TTS | OpenAI TTS | — |

## Key Components

### API Layer (`api/`, `integration/`, `review_system/`)
- FastAPI with 3 routers + monitoring router
- 30+ REST endpoints
- OpenAPI docs at `/docs`

### Evaluation Engine (`evaluation/`)
- Intent accuracy, WER, flow completion, latency
- Weighted scoring → PASS/WARNING/FAIL

### Review System (`review_system/`)
- 6 SQLAlchemy models (Reviewer, Conversation, Review, Rating, Approval, ApprovalHistory)
- Approval workflow with full audit trail
- Analytics engine

### Security (`security.py`)
- API key authentication, rate limiting, secure headers
- CORS, request size limits, secret management

### Monitoring (`monitoring/`)
- Metrics collection (counters, histograms, gauges)
- Health checks (database, providers)
- Kubernetes-ready liveness/readiness probes

### Storage (`storage/`)
- PostgreSQL for persistent evaluation data
- S3/MinIO for report archival

## Deployment

See [deployment.md](deployment.md) for Docker, environment, and production setup.
