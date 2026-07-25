# StayZa Milestone 9 — Testing Guide

## Test Suite Overview

**Total tests: 218+** across 10 test files.

| Test File | Tests | Category |
|-----------|-------|----------|
| `test_api.py` | 7 | FastAPI integration |
| `test_detection.py` | 7 | Language detection |
| `test_flows.py` | 6 | Multi-language flows |
| `test_english_flow.py` | 6 | English flow |
| `test_evaluation.py` | 50+ | Evaluation engine |
| `test_normalization.py` | 24 | Text normalization |
| `test_pronunciation.py` | 3 | Pronunciation |
| `test_nlu_pipeline.py` | 20+ | End-to-end NLU |
| `test_review_system.py` | 27 | Review system |
| `test_integration.py` | 7 | Integration APIs |
| `test_production.py` | 35 | Production hardening |
| `test_e2e_pipeline.py` | 10+ | End-to-end validation |

## Running Tests

```bash
# Full suite
python -m pytest tests/ -v

# Specific test file
python -m pytest tests/test_evaluation.py -v

# With coverage
python -m pytest tests/ --cov=. --cov-report=term --cov-report=html:coverage_reports

# End-to-end pipeline validation
python -m pytest tests/test_e2e_pipeline.py -v --tb=short

# Production hardening tests
python -m pytest tests/test_production.py -v

# Parallel execution
python -m pytest tests/ -n auto
```

## Coverage Requirements

- **Target:** ≥ 85% code coverage
- **Report formats:** XML (CI), HTML (local), terminal (summary)
- **Critical paths:** Pipeline processing, evaluation engine, review system

## Test Categories

### Unit Tests
Test individual components in isolation:
- Language detection rules
- WER calculation
- Rating validation
- Caching logic
- Fallback behavior

### Integration Tests
Test component interactions:
- API endpoints with TestClient
- Database CRUD operations
- Provider fallback chains
- Middleware pipeline

### End-to-End Tests
Test the complete processing pipeline:
- Language → Detection → Analysis → Evaluation → Review
- All 6 languages processed through full pipeline
- Validation report generation

### Load Tests
Test system under concurrent load:
- 10, 50, 100, 250, 500 concurrent users
- Locust-based load testing
- Metrics: latency, error rate, throughput

## CI/CD Pipeline

Tests run automatically on push/PR via GitHub Actions:
1. Lint & Format (ruff, mypy)
2. Security Scan (bandit, safety)
3. Unit & Integration Tests (pytest)
4. Docker Build & Test
5. End-to-End Validation
6. Final Report Generation

See `.github/workflows/ci.yml` for details.
