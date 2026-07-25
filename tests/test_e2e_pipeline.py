"""
End-to-End Pipeline Validation for StayZa Milestone 9.
Validates the complete processing chain from language detection through evaluation and review.
Generates validation report.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from review_system.database import Base, get_db
from review_system.models import Conversation, Review, Rating, Approval, ApprovalHistory, Reviewer

TEST_DB = "sqlite:///./test_e2e_reviews.db"
engine = create_engine(TEST_DB, connect_args={"check_same_thread": False})
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


class PipelineValidator:
    def __init__(self):
        self.stages: list[dict] = []
        self.start_time = time.perf_counter()

    def record(self, stage: str, status: str, duration_ms: float, details: dict | None = None):
        self.stages.append({
            "stage": stage,
            "status": status,
            "duration_ms": round(duration_ms, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "details": details or {},
        })

    def generate_report(self) -> dict:
        total_duration = (time.perf_counter() - self.start_time) * 1000
        passed = sum(1 for s in self.stages if s["status"] == "PASS")
        failed = sum(1 for s in self.stages if s["status"] == "FAIL")
        return {
            "pipeline": "StayZa Milestone 9 End-to-End Validation",
            "total_stages": len(self.stages),
            "passed": passed,
            "failed": failed,
            "total_duration_ms": round(total_duration, 2),
            "stages": self.stages,
            "overall": "PASS" if failed == 0 else "FAIL",
            "validated_at": datetime.now(timezone.utc).isoformat(),
        }


LANGUAGES = {
    "English": {"text": "I want to book a deluxe room for two guests tomorrow morning", "code": "en"},
    "Hindi": {"text": "mujhe ek deluxe kamra do guest ke liye kal subah book karna hai", "code": "hi"},
    "Hinglish": {"text": "mujhe ek deluxe room do guests ke liye kal subah book karna hai", "code": "hinglish"},
    "Telugu": {"text": "naaku oka deluxe room rendu athithulaku repu podduna kavali", "code": "te"},
    "Marathi": {"text": "mala ek deluxe room dona pahunakarita udya sakali book karaycha ahe", "code": "mr"},
    "Malayalam": {"text": "enikku oru deluxe room randu athithikalkku naale ravile venam", "code": "ml"},
}

INTENTS = ["greeting", "booking", "availability", "price_enquiry", "cancellation", "modify_booking", "check_status", "goodbye"]


class TestEndToEndPipeline:
    def test_full_pipeline_validation(self, client):
        validator = PipelineValidator()

        for lang_name, lang_data in LANGUAGES.items():
            text = lang_data["text"]

            t0 = time.perf_counter()
            resp = client.post("/language/detect", json={"text": text})
            dt = (time.perf_counter() - t0) * 1000
            if resp.status_code == 200:
                data = resp.json()
                validator.record(
                    f"{lang_name}_detection", "PASS", dt,
                    {"detected": data.get("language"), "confidence": data.get("confidence")},
                )
            else:
                validator.record(f"{lang_name}_detection", "FAIL", dt, {"status": resp.status_code})
                continue

            t0 = time.perf_counter()
            resp = client.post("/language/analyze", json={"text": text, "language": lang_name})
            dt = (time.perf_counter() - t0) * 1000
            if resp.status_code == 200:
                data = resp.json()
                validator.record(
                    f"{lang_name}_analyze", "PASS", dt,
                    {
                        "intent": data.get("intent"),
                        "confidence": data.get("confidence"),
                        "entities": data.get("entities"),
                        "next_action": data.get("next_action"),
                    },
                )
            else:
                validator.record(f"{lang_name}_analyze", "FAIL", dt, {"status": resp.status_code})

        t0 = time.perf_counter()
        resp = client.get("/language/supported")
        dt = (time.perf_counter() - t0) * 1000
        if resp.status_code == 200:
            data = resp.json()
            count = len(data) if isinstance(data, list) else len(data.get("languages", []))
            validator.record("supported_languages", "PASS", dt, {"count": count})
        else:
            validator.record("supported_languages", "FAIL", dt)

        t0 = time.perf_counter()
        resp = client.post("/language/evaluation/run")
        dt = (time.perf_counter() - t0) * 1000
        if resp.status_code == 200:
            data = resp.json()
            summary = data.get("summary", {})
            validator.record(
                "evaluation_engine", "PASS", dt,
                {
                    "accuracy": summary.get("overall_accuracy"),
                    "passed": summary.get("languages_passed"),
                    "failed": summary.get("languages_failed"),
                },
            )
        else:
            validator.record("evaluation_engine", "FAIL", dt)

        t0 = time.perf_counter()
        resp = client.get("/reviews/analytics")
        dt = (time.perf_counter() - t0) * 1000
        if resp.status_code == 200:
            validator.record("review_analytics", "PASS", dt)
        else:
            validator.record("review_analytics", "FAIL", dt)

        t0 = time.perf_counter()
        resp = client.get("/monitoring/health")
        dt = (time.perf_counter() - t0) * 1000
        if resp.status_code == 200:
            validator.record("health_check", "PASS", dt)
        else:
            validator.record("health_check", "FAIL", dt)

        t0 = time.perf_counter()
        resp = client.get("/health")
        dt = (time.perf_counter() - t0) * 1000
        if resp.status_code == 200:
            validator.record("legacy_health", "PASS", dt)
        else:
            validator.record("legacy_health", "FAIL", dt)

        report = validator.generate_report()

        report_dir = Path("final_reports")
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / "e2e_validation_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        print(f"\nE2E Validation Report: {report['passed']}/{report['total_stages']} passed, {report['failed']} failed")
        for stage in report["stages"]:
            status_mark = "PASS" if stage["status"] == "PASS" else "FAIL"
            print(f"  [{status_mark}] {stage['stage']} ({stage['duration_ms']}ms)")

        assert report["failed"] == 0, f"E2E validation failed: {report['failed']} stage(s) failed"

    def test_all_language_detection(self, client):
        for lang, data in LANGUAGES.items():
            resp = client.post("/language/detect", json={"text": data["text"]})
            assert resp.status_code == 200, f"{lang} detection failed"
            result = resp.json()
            assert result.get("confidence", 0) > 0.5, f"{lang} confidence too low: {result}"

    def test_all_intent_endpoints(self, client):
        for intent in INTENTS:
            text = f"I want to {intent.replace('_', ' ')}"
            resp = client.post("/language/analyze", json={"text": text})
            assert resp.status_code == 200, f"Intent {intent} failed"

    def test_evaluation_endpoints(self, client):
        resp = client.get("/language/evaluation/results")
        assert resp.status_code in (200, 404)

        resp = client.get("/language/languages/status")
        assert resp.status_code == 200

    def test_review_workflow(self, client):
        resp = client.post("/reviews/reviewers", json={"name": "E2E Tester", "languages": ["English"]})
        assert resp.status_code == 201
        reviewer_id = resp.json()["id"]

        resp = client.post("/reviews/conversations", json={
            "conversation_id": "e2e_conv_001",
            "language": "English",
            "original_text": "I want to book a room",
        })
        assert resp.status_code == 201
        conv_id = resp.json()["id"]

        resp = client.post("/reviews/create", json={
            "conversation_id": conv_id,
            "reviewer_id": reviewer_id,
            "feedback": "E2E test review",
            "ratings": {
                "pronunciation": 8.0,
                "language_accuracy": 8.5,
                "intent_accuracy": 9.0,
                "naturalness": 7.5,
                "conversation_quality": 8.0,
                "overall_rating": 8.2,
            },
            "approval": {"status": "Approved", "reviewer_notes": "E2E approval"},
        })
        assert resp.status_code == 201
        review_id = resp.json()["id"]

        resp = client.get(f"/reviews/{review_id}")
        assert resp.status_code == 200
        assert resp.json()["ratings"]["overall_rating"] == 8.2

    def test_monitoring_endpoints(self, client):
        resp = client.get("/monitoring/metrics")
        assert resp.status_code == 200
        assert "counters" in resp.json()

        resp = client.get("/monitoring/health/live")
        assert resp.status_code == 200

        resp = client.get("/monitoring/health/ready")
        assert resp.status_code == 200

    def test_provider_registry_health(self, client):
        from providers.registry import get_provider_registry
        registry = get_provider_registry()
        health = registry.health()
        assert "stt" in health
        assert "llm" in health
        assert "tts" in health

    def test_security_headers(self, client):
        resp = client.get("/")
        headers = resp.headers
        assert "x-content-type-options" in headers
        assert headers["x-content-type-options"] == "nosniff"
        assert "x-frame-options" in headers
        assert headers["x-frame-options"] == "DENY"
