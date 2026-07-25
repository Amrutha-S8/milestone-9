# StayZa Milestone 9 — Troubleshooting Guide

## Common Issues

### Application Won't Start

**Symptom:** `ModuleNotFoundError: No module named '...'`

**Solution:**
```bash
pip install -r requirements.txt
```

**Symptom:** `Address already in use`

**Solution:** Port 8000 is occupied. Change port:
```bash
STAYZA_PORT=8001 python main.py
```

### Provider Failures

**Symptom:** `All STT providers failed`

**Solutions:**
- Check `OPENAI_API_KEY` or `DEEPGRAM_API_KEY` env vars
- Verify `WHISPER_MODEL_SIZE` (default: "medium", change to "tiny" for less memory)
- Check internet connectivity for cloud providers
- See provider health: `GET /monitoring/health`

### Database Issues

**Symptom:** `sqlalchemy.exc.OperationalError`

**Solutions:**
- SQLite: Delete `test_reviews.db` or `review_data/reviews.db`
- PostgreSQL: Verify `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`
- Run migrations: `alembic upgrade head`

### Rate Limiting

**Symptom:** `429 Too Many Requests`

**Solutions:**
- Wait for rate limit window to reset
- Increase `STAYZA_RATE_LIMIT_MAX` (default: 100)
- Check `X-RateLimit-Remaining` response headers

### Docker Issues

**Symptom:** `docker: command not found`

**Solution:** Install Docker Desktop from https://www.docker.com/products/docker-desktop

**Symptom:** Port conflict when running `docker compose up`

**Solution:** Change port mapping in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"
```

### Test Failures

**Symptom:** Tests failing with database errors

**Solution:** Tests use `test_reviews.db`. Delete it and re-run:
```bash
rm test_reviews.db
python -m pytest tests/ -v
```

### Performance Issues

**Symptom:** Slow language detection

**Solutions:**
- Reduce `WHISPER_MODEL_SIZE` to "tiny" or "base"
- Enable GPU: set `WHISPER_DEVICE=cuda`
- Check latency: `GET /monitoring/metrics`

## Getting Help

1. Check `/monitoring/health` for service status
2. Check `logs/application/`, `logs/error/` for detailed logs
3. Run the security audit: `python scripts/security_audit.py`
4. Run E2E validation: `python -m pytest tests/test_e2e_pipeline.py -v`
