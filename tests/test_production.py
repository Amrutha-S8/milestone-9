import json
import os
import threading
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from review_system.database import Base, get_db
from review_system.models import Conversation, Review, Rating, Approval, ApprovalHistory, Reviewer

TEST_DATABASE_URL = "sqlite:///./test_production.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def client():
    return TestClient(app)


class TestProviderFailureScenarios:
    def test_provider_registry_empty_stt(self):
        from providers.fallback import FallbackSTT
        with pytest.raises(ValueError, match="At least one STT provider is required"):
            FallbackSTT([])

    def test_provider_registry_empty_llm(self):
        from providers.fallback import FallbackLLM
        with pytest.raises(ValueError, match="At least one LLM provider is required"):
            FallbackLLM([])

    def test_provider_registry_empty_tts(self):
        from providers.fallback import FallbackTTS
        with pytest.raises(ValueError, match="At least one TTS provider is required"):
            FallbackTTS([])

    def test_provider_fallback_all_fail_stt(self):
        from providers.base import STTProvider, STTResult
        from providers.fallback import FallbackSTT

        class FailingProvider(STTProvider):
            def name(self): return "failing"
            def is_available(self): return True
            def transcribe(self, audio_data, language=None, **kwargs):
                raise RuntimeError("Transcription failed")

        fallback = FallbackSTT([FailingProvider()])
        with pytest.raises(RuntimeError, match="All STT providers failed"):
            fallback.transcribe(b"audio data")

    def test_provider_fallback_skip_unavailable(self):
        from providers.base import STTProvider, STTResult
        from providers.fallback import FallbackSTT

        class UnavailableProvider(STTProvider):
            def name(self): return "unavailable"
            def is_available(self): return False
            def transcribe(self, audio_data, language=None, **kwargs):
                raise AssertionError("Should not be called")

        class WorkingProvider(STTProvider):
            def name(self): return "working"
            def is_available(self): return True
            def transcribe(self, audio_data, language=None, **kwargs):
                return STTResult(text="hello", confidence=0.95, language="en", duration_ms=100.0)

        fallback = FallbackSTT([UnavailableProvider(), WorkingProvider()])
        result = fallback.transcribe(b"audio")
        assert result.text == "hello"
        assert result.confidence == 0.95


class TestDatabaseFailureScenarios:
    def test_postgres_connection_string(self):
        from storage.config import PostgresConfig
        config = PostgresConfig(host="testhost", port=5432, database="testdb", user="user", password="pass")
        assert config.url == "postgresql://user:pass@testhost:5432/testdb"

    def test_s3_config_defaults(self):
        from storage.config import S3Config
        config = S3Config()
        assert config.region == "us-east-1"
        assert config.secure is True

    def test_storage_config_creation(self):
        from storage.config import PostgresConfig, S3Config
        pg = PostgresConfig(host="localhost", database="test")
        assert "localhost" in pg.url
        s3 = S3Config(bucket="test-bucket")
        assert s3.bucket == "test-bucket"


class TestCacheFailureScenarios:
    def test_lru_cache_basic(self):
        from providers.cache import LRUCache
        cache = LRUCache(max_size=3, default_ttl_seconds=60)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        assert cache.get("a") == 1
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_lru_cache_eviction(self):
        from providers.cache import LRUCache
        cache = LRUCache(max_size=2, default_ttl_seconds=60)
        cache.set("a", 1)
        cache.set("b", 2)
        cache.set("c", 3)
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_lru_cache_expiry(self):
        from providers.cache import LRUCache
        cache = LRUCache(max_size=10, default_ttl_seconds=0)
        cache.set("a", 1)
        assert cache.get("a") is None

    def test_cache_make_key(self):
        from providers.cache import LRUCache
        cache = LRUCache()
        key = cache.make_key("test", "arg1", lang="en")
        assert isinstance(key, str)
        assert len(key) == 32

    def test_lazy_loader(self):
        from providers.cache import LazyLoader
        call_count = 0

        def loader():
            nonlocal call_count
            call_count += 1
            return {"data": "loaded"}

        lazy = LazyLoader(loader_fn=loader, ttl_seconds=10)
        result1 = lazy.get()
        result2 = lazy.get()
        assert call_count == 1
        assert result1 == {"data": "loaded"}
        assert result2 == {"data": "loaded"}
        lazy.invalidate()
        lazy.get()
        assert call_count == 2

    def test_batched_processor(self):
        from providers.cache import BatchedProcessor
        processor = BatchedProcessor(batch_size=3)
        items = [1, 2, 3, 4, 5, 6, 7]
        results = processor.process(items, lambda batch: [x * 2 for x in batch])
        assert results == [2, 4, 6, 8, 10, 12, 14]


class TestLargeRequestScenarios:
    def test_large_text_input(self, client):
        large_text = "x" * 50000
        response = client.post("/language/detect", json={"text": large_text})
        assert response.status_code in (200, 400, 413, 422)

    def test_concurrent_requests(self, client, sample_reviewer):
        errors = []
        lock = threading.Lock()

        def send_request(idx):
            try:
                resp = client.post("/reviews/conversations", json={
                    "conversation_id": f"conv_concurrent_{idx}",
                    "language": "English",
                    "original_text": "concurrent test",
                })
                if resp.status_code != 201:
                    with lock:
                        errors.append(resp.status_code)
            except Exception as e:
                with lock:
                    errors.append(str(e))

        threads = [threading.Thread(target=send_request, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(errors) == 0, f"Concurrent request errors: {errors}"


class TestUnsupportedLanguageScenarios:
    def test_unsupported_language_detection(self, client):
        response = client.post("/language/detect", json={"text": "Bonjour, je voudrais une chambre"})
        assert response.status_code == 200
        data = response.json()
        assert "language" in data

    def test_unsupported_language_analytics(self, client):
        response = client.get("/reviews/analytics")
        assert response.status_code == 200


class TestSecurityScenarios:
    def test_rate_limiter(self):
        from security import InMemoryRateLimiter
        limiter = InMemoryRateLimiter(max_requests=3, window_seconds=60)
        for _ in range(3):
            allowed, remaining, _ = limiter.check("test_ip")
            assert allowed is True
        allowed, remaining, _ = limiter.check("test_ip")
        assert allowed is False
        assert remaining == 0

    def test_rate_limiter_exceeded(self):
        from security import InMemoryRateLimiter
        limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)
        assert limiter.check("test_ip")[0] is True
        assert limiter.check("test_ip")[0] is True
        assert limiter.check("test_ip")[0] is False

    def test_api_key_auth(self):
        from security import ApiKeyAuth
        auth = ApiKeyAuth(api_keys={"valid-key-123"})
        assert auth.authenticate("valid-key-123") is True
        assert auth.authenticate("wrong-key") is False
        assert auth.authenticate(None) is False

    def test_api_key_auth_no_keys(self):
        from security import ApiKeyAuth
        auth = ApiKeyAuth(api_keys=set())
        assert auth.authenticate(None) is True

    def test_secret_manager(self):
        from providers.secrets import SecretManager
        import os
        os.environ["STAYZA_TEST_VAR"] = "test_value"
        sm = SecretManager(prefix="STAYZA_")
        assert sm.get("TEST_VAR") == "test_value"
        assert sm.get("NONEXISTENT") is None
        assert sm.get_bool("NONEXISTENT", True) is True
        assert sm.get_int("TEST_INT", 42) == 42

    def test_text_validation(self):
        from security import validate_text_length
        from fastapi import HTTPException
        with pytest.raises(HTTPException, match="cannot be empty"):
            validate_text_length("")
        with pytest.raises(HTTPException, match="cannot be empty"):
            validate_text_length("   ")
        with pytest.raises(HTTPException, match="exceeds maximum length"):
            validate_text_length("x" * 20000, max_length=10000)
        assert validate_text_length("hello") == "hello"


class TestMonitoringScenarios:
    def test_metrics_collector(self):
        from monitoring.metrics import MetricsCollector
        mc = MetricsCollector()
        mc.increment("requests")
        mc.increment("requests")
        mc.increment("errors")
        mc.record_latency("api_latency", 150.0)
        mc.record_latency("api_latency", 250.0)
        mc.set_gauge("active_users", 42)

        snapshot = mc.snapshot()
        assert snapshot["counters"]["requests"] == 2
        assert snapshot["counters"]["errors"] == 1
        assert snapshot["histograms"]["api_latency"]["count"] == 2
        assert snapshot["histograms"]["api_latency"]["avg"] == 200.0
        assert snapshot["gauges"]["active_users"] == 42

    def test_histogram_percentiles(self):
        from monitoring.metrics import Histogram
        h = Histogram()
        for v in range(1, 101):
            h.observe(float(v))
        assert h.count == 100
        assert h.p50 == 51.0
        assert h.p95 == 96.0
        assert h.p99 == 100.0

    def test_health_checker(self):
        from monitoring.health import HealthChecker
        hc = HealthChecker()
        hc.register_check("test_ok", lambda: {"status": "healthy"})
        hc.register_check("test_fail", lambda: (_ for _ in ()).throw(RuntimeError("fail")))
        status = hc.status()
        assert status["status"] == "degraded"

    def test_metrics_reset(self):
        from monitoring.metrics import MetricsCollector
        mc = MetricsCollector()
        mc.increment("test", 5)
        assert mc.snapshot()["counters"]["test"] == 5
        mc.reset()
        assert mc.snapshot()["counters"] == {}


class TestBackupScenarios:
    def test_backup_service_creation(self, tmp_path):
        from backup.config import BackupConfig
        from backup.service import BackupService
        config = BackupConfig(backup_dir=tmp_path / "backups", compress=False,
                              include_database=False, include_reports=False,
                              include_config=False, include_languages=False)
        svc = BackupService(config)
        result = svc.create_backup(label="test")
        assert result.exists()
        manifest = result / "manifest.json"
        assert manifest.exists()

    def test_backup_list(self, tmp_path):
        from backup.config import BackupConfig
        from backup.service import BackupService
        config = BackupConfig(backup_dir=tmp_path / "backups", compress=False,
                              include_database=False, include_reports=False,
                              include_config=False, include_languages=False)
        svc = BackupService(config)
        svc.create_backup(label="test1")
        svc.create_backup(label="test2")
        backups = svc.list_backups()
        assert len(backups) == 2

    def test_backup_cleanup(self, tmp_path):
        from backup.config import BackupConfig
        from backup.service import BackupService
        config = BackupConfig(backup_dir=tmp_path / "backups", compress=False, max_backups=2,
                              include_database=False, include_reports=False,
                              include_config=False, include_languages=False)
        svc = BackupService(config)
        b1 = svc.create_backup(label="first")
        b2 = svc.create_backup(label="second")
        assert b2.exists()
        backups = svc.list_backups()
        assert len(backups) == 2


class TestLoggingScenarios:
    def test_logging_service_channels(self):
        from logservice.config import LoggingConfig
        from logservice.service import LoggingService
        import tempfile
        import os
        tmp = tempfile.mkdtemp()
        try:
            config = LoggingConfig(log_dir=tmp)
            svc = LoggingService(config)
            assert svc.application() is not None
            assert svc.api() is not None
            assert svc.evaluation() is not None
            assert svc.error() is not None
            assert svc.audit() is not None
            import logging
            logging.shutdown()
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)

    def test_logging_service_logs(self):
        from logservice.config import LoggingConfig
        from logservice.service import LoggingService
        import tempfile
        from pathlib import Path
        tmp = tempfile.mkdtemp()
        try:
            config = LoggingConfig(log_dir=tmp)
            svc = LoggingService(config)
            svc.log_api_call("POST", "/test", 200, 15.5, "127.0.0.1")
            svc.log_evaluation_result("run_001", "English", "PASS", 95.0)
            svc.log_audit_event("CREATE", "review", "admin")
            svc.log_error("test_component", "Test error message")
            api_log = Path(tmp) / "api" / "api.log"
            assert api_log.exists()
            assert api_log.stat().st_size > 0
            import logging
            logging.shutdown()
        finally:
            import shutil
            shutil.rmtree(tmp, ignore_errors=True)


class TestMigrationScenarios:
    def test_seed_reviewers(self):
        from migrations.seed import seed_reviewers
        db = TestingSessionLocal()
        try:
            reviewers = seed_reviewers(db)
            assert len(reviewers) >= 5
        finally:
            db.close()

    def test_seed_reviewers_idempotent(self):
        from migrations.seed import seed_reviewers
        db = TestingSessionLocal()
        try:
            r1 = seed_reviewers(db)
            r2 = seed_reviewers(db)
            assert len(r1) == len(r2)
        finally:
            db.close()


@pytest.fixture
def sample_reviewer(setup_db):
    from review_system.models import Reviewer
    db = TestingSessionLocal()
    reviewer = Reviewer(name="Test Reviewer", languages=["English"])
    db.add(reviewer)
    db.commit()
    db.refresh(reviewer)
    db.close()
    return reviewer
