from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_integration_analyze_endpoint():
    response = client.post("/api/v1/analyze", json={
        "text": "book a room for two nights",
        "language": "en-IN",
    })
    assert response.status_code == 200
    data = response.json()
    assert "utterance_id" in data
    assert data["word_error_rate"] >= 0.0


def test_integration_analyze_with_entities():
    response = client.post("/api/v1/analyze", json={
        "text": "book a deluxe room",
        "language": "en-IN",
        "entities": {"room_type": "deluxe"},
        "critical_fields": {"date": "2026-08-01"},
        "intent_label": "book_room",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["intent_correct"] is True
    assert data["entities_correct"] == 1
    assert data["critical_fields_correct"] == 1


def test_integration_analyze_empty_text():
    response = client.post("/api/v1/analyze", json={
        "text": "",
        "language": "en-IN",
    })
    assert response.status_code == 400


def test_integration_analyze_text_too_long():
    response = client.post("/api/v1/analyze", json={
        "text": "x" * 10001,
        "language": "en-IN",
    })
    assert response.status_code == 400


def test_integration_evaluate_endpoint():
    response = client.post("/api/v1/evaluate", json={
        "count": 10,
    })
    assert response.status_code == 200
    data = response.json()
    assert "run_id" in data
    assert data["status"] in ("completed", "partial", "failed")


def test_integration_languages_endpoint():
    response = client.get("/api/v1/languages")
    assert response.status_code == 200
    data = response.json()
    assert "languages" in data
    assert data["total"] >= 6


def test_integration_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_integration_api_routes_accessible():
    endpoints = [
        ("POST", "/api/v1/analyze", {"text": "test", "language": "en-IN"}),
        ("POST", "/api/v1/evaluate", {"count": 5}),
        ("GET", "/api/v1/languages", None),
        ("GET", "/api/v1/health", None),
    ]
    for method, path, body in endpoints:
        if method == "GET":
            resp = client.get(path)
        else:
            resp = client.post(path, json=body or {})
        assert resp.status_code in (200, 400, 422), f"{method} {path} returned {resp.status_code}"
