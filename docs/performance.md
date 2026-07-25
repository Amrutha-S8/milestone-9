# StayZa Milestone 9 — Performance Guide

## Performance Architecture

### Caching Layers

| Layer | Type | TTL | Key |
|-------|------|-----|-----|
| STT | LRU Cache | 60s | Audio hash |
| LLM | LRU Cache | 120s | Text + language |
| TTS | LRU Cache | 300s | Text + voice |
| Languages | Memory Cache | 300s | Language list |

All caches use `LRUCache` (max 1024 entries, thread-safe).

### Connection Pooling

PostgreSQL pool (configurable):
- Pool size: 10 (default)
- Max overflow: 20 (default)
- Pool pre-ping enabled

### Batch Processing

The `BatchedProcessor` handles large datasets in configurable batches (default 32).

### Lazy Loading

The `LazyLoader` defers initialization of expensive resources:
- Language flows
- Large datasets
- Provider models

## Load Test Results

Load tests are run with Locust at various concurrency levels:

| Users | Expected Avg Latency | Expected P95 | Expected Error Rate |
|-------|---------------------|--------------|-------------------|
| 10 | < 200ms | < 500ms | 0% |
| 50 | < 500ms | < 1000ms | < 1% |
| 100 | < 1000ms | < 2000ms | < 2% |
| 250 | < 2000ms | < 5000ms | < 5% |
| 500 | < 5000ms | < 10000ms | < 10% |

## Optimization Tips

### Reduce Whisper Memory

```bash
export WHISPER_MODEL_SIZE=tiny   # smallest model
export WHISPER_DEVICE=cpu        # force CPU
```

### Increase Throughput

```bash
export STAYZA_WORKERS=4          # more workers
export PG_POOL_SIZE=20           # larger DB pool
export STAYZA_RATE_LIMIT_MAX=500 # increase rate limit
```

### Database Optimization

- Add indexes on frequently queried columns
- Use PostgreSQL for production (not SQLite)
- Configure `PG_POOL_SIZE` based on concurrent users

## Monitoring Performance

### Key Metrics

Track via `GET /monitoring/metrics`:

- `http_request_duration_ms` — histogram of all request latencies
- `http_requests_total` — counter of all requests
- Per-endpoint latency histograms

### Health Checks

Monitor via `GET /monitoring/health`:
- Database connection status
- Provider availability
- Uptime tracking

## Profiling

For detailed profiling:

```bash
pip install py-spy
py-spy record -o profile.svg --pid $(pgrep -f "uvicorn")
```
