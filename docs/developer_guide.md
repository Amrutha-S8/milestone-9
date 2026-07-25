# StayZa Milestone 9 — Developer Guide

## Getting Started

### Prerequisites
- Python 3.11+
- pip

### Setup

```bash
git clone <repo-url> stayza-milestone9
cd stayza-milestone9

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Running

```bash
# Development with auto-reload
python main.py  # or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# All tests
python -m pytest tests/ -v

# With coverage
python -m pytest tests/ --cov=. --cov-report=html
```

## Project Structure

```
stayza_milestone9/
├── api/                  # REST API layer
├── providers/            # STT, LLM, TTS adapters with fallback
├── storage/              # PostgreSQL + S3 storage
├── monitoring/           # Metrics, health checks
├── logservice/          # Multi-channel rotating logging
├── backup/               # Backup & restore
├── migrations/           # Alembic migration scripts
├── evaluation/           # Evaluation engine
├── review_system/        # Native voice review system
├── detection/            # Language detection
├── languages/            # Multi-language flow engine
├── datasets/             # Benchmark datasets
├── integration/          # Milestone 8 integration
├── security.py           # Auth, rate limiting, secure headers
├── tests/                # Test suite
└── docs/                 # Documentation
```

## Coding Standards

- **Python**: 3.11+ with type hints
- **Formatting**: Ruff (lint) + Black (format)
- **Imports**: Standard library → third-party → local
- **Testing**: pytest with FastAPI TestClient
- **Security**: Bandit for security scanning

## Environment Variables

All configuration is via `STAYZA_*` environment variables. See `.env.example` for the full list.

## Docker

```bash
# Build
docker build -t stayza-milestone9 .

# Run
docker compose up

# Test
curl http://localhost:8000/health
```

## Adding a New Language

1. Create `languages/<new_lang>/flow.json` with 8 intents
2. Create `languages/<new_lang>/flow.py` subclassing `JSONLanguageFlow`
3. Register in `api/dependencies.py`: `language_registry.register(NewLanguageFlow())`
4. Add detection rules in `detection/rules.py`
5. Add dataset in `datasets/<new_lang>.json`

## Adding a New Evaluation Metric

1. Create evaluator in `evaluation/<metric>.py`
2. Add to `EvaluationEngine.run_full_evaluation()` in `engine.py`
3. Include in `LanguageQualityScore.calculate()` in `score.py`
4. Add thresholds in `EvaluationThresholds` in `config.py`

## CI/CD

See `.github/workflows/ci.yml` for the CI pipeline configuration.
