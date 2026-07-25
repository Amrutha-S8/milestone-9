"""
End-to-End API Integration Tests for StayZa Milestone 9 using FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "uptime_seconds" in data


def test_detect_telugu_endpoint():
    """Test POST /language/detect for Telugu spec example."""
    payload = {"text": "మాకు ఒక గది కావాలి"}
    response = client.post("/language/detect", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "Telugu"
    assert data["confidence"] >= 0.95


def test_analyze_hindi_booking_upgraded_spec():
    """
    Test TASK 5 upgraded spec:
    POST /language/analyze with Hindi text
    Returns:
      {
        "language": "Hindi",
        "intent": "booking",
        "confidence": 0.96,
        "next_action": "ask_checkin_date",
        "flow": "booking"
      }
    """
    payload = {"text": "मुझे एक कमरा बुक करना है"}
    response = client.post("/language/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "Hindi"
    assert data["intent"] == "booking"
    assert data["confidence"] >= 0.90
    assert data["next_action"] == "ask_checkin_date"
    assert data["flow"] == "booking"


def test_analyze_english_booking_exact_spec():
    payload = {"text": "I want to book a room"}
    response = client.post("/language/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "English"
    assert data["intent"] == "booking"
    assert data["confidence"] == 0.95
    assert data["next_action"] == "ask_checkin_date"
    assert data["flow"] == "booking"


def test_analyze_cancellation_utterance():
    payload = {"text": "I want to cancel my reservation"}
    response = client.post("/language/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["language"] == "English"
    assert data["intent"] == "cancellation"
    assert data["flow"] == "cancellation"


def test_list_supported_languages():
    response = client.get("/language/supported")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 6  # English, Hindi, Hinglish, Telugu, Marathi, Malayalam


def test_run_benchmark_evaluation_endpoint():
    response = client.get("/language/evaluate")
    assert response.status_code == 200
    data = response.json()
    assert "intent_accuracy" in data
    assert data["total_samples"] >= 300
