# StayZa Milestone 9: Multilingual Language Flows and Evaluation Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green.svg)](https://fastapi.tiangolo.com)
[![Pytest](https://img.shields.io/badge/Pytest-Passed-success.svg)](https://docs.pytest.org)

Production-ready, enterprise-grade **Milestone 9 (Language Flows and Evaluation)** module for **StayZa** voice platform. Supports 6 Indian languages (**English, Hindi, Hinglish, Telugu, Marathi, Malayalam**), dynamic JSON flow configuration, 300+ benchmark datasets, a fully automated evaluation engine with scoring, pass/fail, and WER metrics.

---

## Folder Structure

```
stayza_milestone9/
├── api/                        # REST API Layer
├── providers/                  # ★ Provider Adapters (NEW)
├── storage/                    # ★ Persistent Storage (NEW)
├── logservice/                 # ★ Multi-channel Logging (NEW)
├── monitoring/                 # ★ Monitoring & Metrics (NEW)
├── backup/                     # ★ Automated Backup (NEW)
├── migrations/                 # ★ Database Migration (NEW)
├── security.py                 # ★ Security Hardening (NEW)
├── detection/                  # Language Detection Engine
├── languages/                  # JSON-driven Multi-Language Flows
├── datasets/                   # 600+ Benchmark Datasets
├── evaluation/                 # Automated Evaluation Engine
├── session/                    # Multi-turn Session Management
├── normalization/              # Text Normalization
├── intent/                     # Intent Classification
├── entities/                   # Entity Extraction
├── integration/                # Milestone 8 Integration Layer
├── pronunciation/              # Pronunciation Dictionary
├── review_system/             # ★ Native Voice Review System (NEW)
│   ├── __init__.py               # Package exports
│   ├── database.py               # SQLAlchemy engine & session
│   ├── models.py                 # 6 DB models (Reviewer, Conversation, Review, Rating, Approval, ApprovalHistory)
│   ├── schemas.py                # Pydantic v2 review schemas
│   ├── service.py                # Business logic layer (CRUD, approval workflow)
│   ├── router.py                 # 12 FastAPI review endpoints
│   ├── analytics.py              # Analytics engine (averages, breakdowns, rates)
│   ├── reports.py                # JSON report generator & storage
│   └── auditor.py                # Auto-flagging of low-confidence utterances
├── review_data/               # ★ Review data (NEW)
│   ├── reviews.db              # SQLite database
│   └── reports/                # Auto-generated review reports
├── tests/
│   ├── __init__.py
│   ├── test_api.py             # FastAPI TestClient integration tests
│   ├── test_detection.py       # Language detection tests
│   ├── test_flows.py           # Multi-language flow tests
│   ├── test_english_flow.py    # English flow tests
│   ├── test_evaluation.py      # Comprehensive evaluation engine tests
│   ├── test_normalization.py   # Normalization tests
│   ├── test_pronunciation.py   # Pronunciation tests
│   ├── test_nlu_pipeline.py    # End-to-end NLU pipeline tests
│   ├── test_review_system.py   # ★ 27 review system tests
│   └── test_integration.py     # Integration API tests
├── docs/
│   ├── architecture.md         # Architecture specification
│   ├── api_spec.md             # API reference
│   ├── integration_guide.md    # M8 -> M9 integration guide
│   └── review_api.md           # ★ Full review API documentation (NEW)
├── main.py                     # FastAPI entrypoint
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

---

## Evaluation Engine

The evaluation engine (`evaluation/engine.py`) is a centralized orchestrator that automatically evaluates every supported language. It runs the complete pipeline:

1. **Intent Accuracy** — compares predicted vs expected intents from benchmark datasets
2. **WER (Word Error Rate)** — measures STT transcription quality using Levenshtein distance
3. **Flow Completion** — evaluates 8 hotel conversation scenarios per language
4. **Latency Profiling** — measures per-language processing time (detection, intent, entities, normalization)
5. **Language Quality Score** — weighted combination of all metrics (0-100)
6. **Pass/Fail Determination** — automatically marks languages as PASS/WARNING/FAIL

### Scoring Formula

The **Language Quality Score** uses configurable weights:

| Metric | Weight | Formula |
|--------|--------|---------|
| Intent Accuracy | 35% | `accuracy * 100` |
| WER | 25% | `(1 - wer) * 100` |
| Flow Completion | 25% | `completion_rate * 100` |
| Latency | 15% | `max(0, 100 - (latency_ms / 10))` |

**Final Score** = weighted sum of all metric scores (capped at 100).

### Evaluation Pipeline Flow

```
DatasetLoader
    │
    ▼
IntentAccuracyEvaluator ──► per-language accuracy
    │
    ├──► WEREvaluator ──► per-language WER %
    │
    ├──► FlowCompletionEvaluator ──► per-language completion rate
    │
    ├──► LatencyProfiler ──► per-language latency (ms)
    │
    ▼
LanguageQualityScore ──► final score (0-100)
    │
    ▼
LanguageStatusEvaluator ──► PASS / WARNING / FAIL
    │
    ▼
EvaluationReportGenerator ──► JSON report saved to reports/
```

### Word Error Rate (WER)

WER uses **Levenshtein distance** on word arrays:

```
WER = (Substitutions + Deletions + Insertions) / Total_Reference_Words
```

- **Exact match**: WER = 0%
- **One substitution**: WER = 16.67% (for 6-word sentence)
- **Completely different**: WER = 100%+

### Pass/Fail Rules

Default thresholds (all configurable in `evaluation/config.py`):

| Metric | PASS | WARNING | FAIL |
|--------|------|---------|------|
| Intent Accuracy | >= 95% | >= 85% | < 85% |
| WER | <= 5% | <= 10% | > 10% |
| Flow Completion | >= 95% | >= 85% | < 85% |
| Latency | <= 500ms | <= 800ms | > 800ms |

- **PASS**: All metrics meet pass thresholds → language is **enabled**
- **WARNING**: All metrics at least meet warning thresholds
- **FAIL**: One or more metrics below warning thresholds → language is **disabled**

---

## API Endpoints

### NLU Endpoints (under `/language` prefix)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/language/detect` | Detect language of input text |
| POST | `/language/analyze` | Full NLU pipeline (normalize → detect → intent → entities → session → audit) |
| GET | `/language/session/{session_id}` | Get multi-turn session context |
| GET | `/language/supported` | List supported languages |
| GET | `/language/evaluate` | Run benchmark accuracy evaluation |
| GET | `/language/review/flagged` | Get flagged low-confidence utterances |

### Evaluation Endpoints (under `/language` prefix)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/language/evaluation/run` | Run full evaluation engine (accuracy, WER, completion, latency, score, pass/fail) |
| GET | `/language/evaluation/results` | Get latest evaluation results |
| GET | `/language/languages/status` | Get pass/fail status for all languages |

### Example: POST /language/evaluation/run Response

```json
{
  "summary": {
    "total_languages_evaluated": 6,
    "total_samples": 612,
    "correct_intents": 580,
    "overall_accuracy": 0.9477,
    "languages_passed": 4,
    "languages_warning": 1,
    "languages_failed": 1
  },
  "per_language": {
    "English": {
      "language": "English",
      "intent_accuracy_pct": 98.2,
      "wer_pct": 2.3,
      "flow_completion_pct": 99.1,
      "avg_latency_ms": 185.0,
      "final_score": 97.0,
      "weights": {
        "accuracy": 0.35,
        "wer": 0.25,
        "completion": 0.25,
        "latency": 0.15
      }
    }
  },
  "report_path": "reports/eval_20250101_120000.json",
  "status": {
    "per_language": {
      "English": {
        "language": "English",
        "status": "PASS",
        "enabled": true
      }
    }
  }
}
```

### Example: GET /language/languages/status Response

```json
{
  "English": {
    "language": "English",
    "accuracy": 98.2,
    "wer": 2.3,
    "flow_completion": 99.1,
    "latency": 185.0,
    "final_score": 97.0,
    "status": "PASS",
    "enabled": true
  },
  "Hindi": {
    "language": "Hindi",
    "accuracy": 96.1,
    "wer": 3.1,
    "flow_completion": 87.5,
    "latency": 210.0,
    "final_score": 91.2,
    "status": "WARNING",
    "enabled": false
  }
}
```

---

## Configuration

All thresholds are configurable in `evaluation/config.py`:

```python
@dataclass
class EvaluationThresholds:
    accuracy_min: float = 0.95
    wer_max: float = 0.05
    flow_completion_min: float = 0.95
    latency_max_ms: float = 500.0
    accuracy_warning_min: float = 0.85
    wer_warning_max: float = 0.10
    flow_completion_warning_min: float = 0.85
    latency_warning_max_ms: float = 800.0
```

Score weights can also be customized:

```python
@dataclass
class ScoreWeights:
    accuracy_weight: float = 0.35
    wer_weight: float = 0.25
    flow_completion_weight: float = 0.25
    latency_weight: float = 0.15
```

---

## How to Add a New Language

1. Create directory `languages/<new_language>/`.
2. Add `languages/<new_language>/flow.json` specifying intent keywords and actions.
3. Subclass `JSONLanguageFlow` in `languages/<new_language>/flow.py`.
4. Register in `api/dependencies.py`: `language_registry.register(NewLanguageFlow())`

The evaluation engine will automatically include the new language.

---

## How to Add a New Evaluation Metric

1. Create a new evaluator class in `evaluation/` (e.g., `bleu.py`).
2. Add it to the `EvaluationEngine.run_full_evaluation()` pipeline in `engine.py`.
3. Include the metric in `LanguageQualityScore.calculate()` in `score.py`.
4. Add thresholds in `EvaluationThresholds` in `config.py`.

---

## Testing

Run the complete test suite:

```bash
python -m pytest -v tests/
```

Run evaluation-specific tests:

```bash
python -m pytest -v tests/test_evaluation.py -v
```

Run production hardening tests:

```bash
python -m pytest -v tests/test_production.py -v
```

---

---

## Production Hardening (Day 6)

The project has been hardened for production deployment with the following systems:

### Provider Integration (`providers/`)
Adapter pattern for real AI services with configurable fallback chains:

| Service | Provider 1 | Provider 2 | Provider 3 |
|---------|-----------|-----------|-----------|
| STT | Whisper | Deepgram | Google STT |
| LLM | GPT-4o | Claude | — |
| TTS | Azure TTS | OpenAI TTS | — |

Fallback chain: Provider 1 → Failure → Provider 2 → Failure → Provider 3 → Error

### Persistent Storage (`storage/`)
- **PostgreSQL** via SQLAlchemy for evaluation reports, language scores, benchmark results, latency history
- **S3/MinIO** for object storage of reports and backups
- Configurable via environment variables (`STORAGE_TYPE`, `PG*`, `S3_*`)

### Security (`security.py`)
| Measure | Implementation |
|---------|---------------|
| API Key Auth | `X-API-Key` header validation |
| Rate Limiting | 100 req/60s sliding window |
| Secure Headers | HSTS, X-Frame-Options, X-Content-Type-Options |
| Request Size Limit | 10MB max body |
| Secret Management | `STAYZA_*` environment variables |
| Input Validation | Pydantic + manual validation |

### Monitoring (`monitoring/`)
| Endpoint | Purpose |
|----------|---------|
| `GET /monitoring/metrics` | Counter, histogram, gauge snapshot |
| `GET /monitoring/health` | Comprehensive health + uptime |
| `GET /monitoring/health/live` | K8s liveness probe |
| `GET /monitoring/health/ready` | K8s readiness probe |

### Logging (`logservice/`)
Five rotating log channels:
- `logs/application/` — General application events
- `logs/api/` — HTTP request/response logs
- `logs/evaluation/` — Evaluation run results
- `logs/error/` — Warnings and errors (separated)
- `logs/audit/` — Security-relevant audit trail

Each channel uses 10MB rotating files with 10 backups.

### Database Migration (`migrations/`)
- Alembic migration scripts (`migrations/versions/001_initial_schema.py`)
- Seed scripts for reviewers and benchmark conversations
- Supports future schema changes via `alembic upgrade head`

### Backup & Restore (`backup/`)
- Full backup: database, reports, config, language dictionaries
- Automated compression (tar.gz)
- Cleanup old backups (configurable retention)
- Restore procedure via `RestoreService`

### Updated Folder Structure
```
stayza_milestone9/
├── providers/               # ★ Provider Adapters (NEW)
│   ├── __init__.py           # Exports all providers
│   ├── base.py               # STTProvider, LLMProvider, TTSProvider ABCs
│   ├── config.py             # Provider configuration dataclasses
│   ├── registry.py           # ProviderRegistry singleton
│   ├── fallback.py           # FallbackSTT, FallbackLLM, FallbackTTS
│   ├── cache.py              # LRUCache, BatchedProcessor, LazyLoader
│   ├── pipeline.py           # STTPipeline, LLMPipeline, TTSPipeline
│   ├── secrets.py            # SecretManager
│   ├── stt/                  # STT adapters
│   │   ├── whisper.py        # Whisper (local/OpenAI)
│   │   ├── deepgram.py       # Deepgram API
│   │   └── google.py         # Google Cloud STT
│   ├── llm/                  # LLM adapters
│   │   ├── gpt4o.py          # GPT-4o (OpenAI/Azure)
│   │   └── claude.py         # Claude (Anthropic)
│   └── tts/                  # TTS adapters
│       ├── azure.py          # Azure Neural TTS
│       └── openai.py         # OpenAI TTS
├── storage/                  # ★ Persistent Storage (NEW)
│   ├── __init__.py
│   ├── config.py             # PostgresConfig, S3Config
│   ├── postgres.py           # PostgresStorage (evaluation_reports, language_scores, etc.)
│   ├── s3.py                 # S3ObjectStorage (report backup)
│   └── factory.py            # StorageFactory
├── logservice/               # ★ Multi-channel Logging (NEW)
│   ├── __init__.py
│   ├── config.py             # LoggingConfig
│   └── service.py            # LoggingService (5 channels, rotating files)
├── monitoring/               # ★ Monitoring & Metrics (NEW)
│   ├── __init__.py
│   ├── metrics.py            # MetricsCollector (counters, histograms, gauges)
│   ├── health.py             # HealthChecker (database, providers)
│   └── router.py             # /monitoring endpoints + MetricsMiddleware
├── backup/                   # ★ Automated Backup (NEW)
│   ├── __init__.py
│   ├── config.py             # BackupConfig
│   └── service.py            # BackupService + RestoreService
├── migrations/               # ★ Database Migration (NEW)
│   ├── env.py                # Alembic environment
│   ├── alembic.ini           # Alembic configuration
│   ├── seed.py               # Seed scripts (reviewers, conversations)
│   └── versions/
│       └── 001_initial_schema.py
├── security.py               # ★ Security hardening (NEW)
│                              # ApiKeyAuth, RateLimitMiddleware,
│                              # SecureHeadersMiddleware, RequestSizeLimit
├── .env.example              # ★ Environment template
├── scripts/                  # Utility scripts
└── tests/
    └── test_production.py    # ★ 30+ production tests (NEW)
```

## Connection with Milestone 8 (Voice Foundation)

```
+--------------------------------+       POST /language/analyze       +------------------------------------+
|  Milestone 8 Pipecat STT       | ---------------------------------> |  Milestone 9 Multilingual Engine   |
|  (Audio -> Multi-script Text)  | <--------------------------------- |  (Language, Intent, Action, Flow)  |
+--------------------------------+  {"flow": "booking", ...}          +------------------------------------+
                                                                                        |
                                                                                        v
                                                                       +------------------------------------+
                                                                       |  Milestone 8 TTS Node              |
                                                                       |  (Synthesizes response_template)   |
                                                                       +------------------------------------+
```

---

## Milestone 9.2: Native Voice Review System

The **Native Voice Review System** (`review_system/`) enables native language reviewers to evaluate multilingual conversations across 6 Indian languages. It provides a complete audit trail with rating categories, approval workflow, analytics, and automated JSON reports.

### Review Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    StayZa Review Pipeline                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   POST /language/analyze (auto-flagging)                        │
│         │                                                       │
│         ▼                                                       │
│   ReviewAuditor (confidence < 0.70 → flagged queue)            │
│         │                                                       │
│         ▼                                                       │
│   Reviewer Service (manual review creation)                     │
│         │                                                       │
│   ┌─────┴─────┐                                                 │
│   │           │                                                 │
│   ▼           ▼                                                 │
│ Rating      Approval                                            │
│ (6 cats)    (4 statuses)                                        │
│   │           │                                                 │
│   └─────┬─────┘                                                 │
│         ▼                                                       │
│   Analytics Engine → Report Generator → JSON Report             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Review Workflow

1. **Utterance Recording** — Conversation audio is transcribed and analyzed by the NLU pipeline
2. **Auto-Flagging** — Low-confidence (<0.70) or unknown-intent utterances are automatically flagged
3. **Conversation Storage** — Original text, normalized text, detected language, intent, entities, expected intent, evaluation score, and latency are stored
4. **Review Creation** — A native language reviewer evaluates the conversation and provides:
   - **Ratings**: Pronunciation, Language Accuracy, Intent Accuracy, Naturalness, Conversation Quality, Overall (each 0-10)
   - **Feedback**: Textual observations
   - **Approval Status**: Pending, Approved, Rejected, or Needs Improvement
5. **Approval Workflow** — Status changes are tracked with full history
6. **Analytics Generation** — System computes per-language and per-reviewer statistics
7. **Report Generation** — JSON reports are automatically stored in `review_data/reports/`

### Folder Structure (Updated)

```
stayza_milestone9/
├── api/                          # REST API Layer
├── detection/                    # Language Detection Engine
├── languages/                    # JSON-driven Multi-Language Flows
├── datasets/                     # 600+ Benchmark Datasets
├── evaluation/                   # Automated Evaluation Engine
├── pronunciation/                # Pronunciation Dictionary
├── review_system/                # ★ Native Voice Review System (NEW)
│   ├── __init__.py               # Package exports
│   ├── database.py               # SQLAlchemy engine & session
│   ├── models.py                 # 6 DB models (Reviewer, Conversation, Review, Rating, Approval, ApprovalHistory)
│   ├── schemas.py                # Pydantic v2 review schemas
│   ├── service.py                # Business logic layer (CRUD, approval workflow)
│   ├── router.py                 # 12 FastAPI review endpoints
│   ├── analytics.py              # Analytics engine (averages, breakdowns, rates)
│   ├── reports.py                # JSON report generator & storage
│   ├── auditor.py                # Auto-flagging of low-confidence utterances
│   └── reports.py                # JSON report generator & storage
├── review_data/                  # ★ Review data directory (NEW)
│   ├── reviews.db                # SQLite database
│   └── reports/                  # Auto-generated JSON reports
├── tests/
│   ├── test_review_system.py     # ★ 22 comprehensive review tests (NEW)
│   └── ...
├── docs/
│   └── review_api.md             # ★ Full API documentation (NEW)
├── main.py
├── requirements.txt
└── README.md
```

### Review API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/reviews/reviewers` | Register a new native language reviewer |
| GET | `/reviews/reviewers` | List all registered reviewers |
| POST | `/reviews/conversations` | Store a conversation for review |
| POST | `/reviews/create` | Create a new review (with ratings & approval) |
| GET | `/reviews` | List all reviews (paginated) |
| GET | `/reviews/{id}` | Get a single review by ID |
| PUT | `/reviews/{id}` | Update review feedback, ratings, or approval |
| DELETE | `/reviews/{id}` | Delete a review and all related data |
| GET | `/reviews/language/{language}` | Get reviews filtered by language |
| GET | `/reviews/analytics` | Get review analytics (ratings, stats, rates) |
| GET | `/reviews/reports/generate` | Generate and store a JSON review report |

### How Reviewers Use the System

1. **Login** — Reviewers are registered via `POST /reviews/reviewers` with their name and language proficiencies
2. **Browse Flagged Conversations** — Reviewers can fetch flagged utterances via `GET /language/review/flagged`
3. **Evaluate Conversations** — Reviewers create reviews via `POST /reviews/create`:
   - Rate pronunciation, language accuracy, intent accuracy, naturalness, conversation quality, overall
   - Provide textual feedback
   - Set approval status (Pending / Approved / Rejected / Needs Improvement)
4. **Update Approvals** — Senior reviewers can update approval status with notes
5. **Monitor Analytics** — Reviewers check `GET /reviews/analytics` for per-language and per-reviewer statistics
6. **Download Reports** — Reviewers generate JSON reports via `GET /reviews/reports/generate`