"""
Comprehensive test suite for StayZa Native Review System.
Covers Review APIs, Approval Workflow, Rating System, Reports, and Analytics.
"""

import os

# Must set before importing app to affect middleware initialization
os.environ.setdefault("STAYZA_RATE_LIMIT_MAX", "100000")
os.environ.setdefault("STAYZA_DISABLE_API_AUTH", "true")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from review_system.database import Base, get_db
from review_system.models import (
    Approval,
    ApprovalHistory,
    Conversation,
    Rating,
    Review,
    Reviewer,
)

engine = create_engine("sqlite:///./test_reviews.db", connect_args={"check_same_thread": False})
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


@pytest.fixture
def db():
    db = TestingSessionLocal()
    yield db
    db.close()


@pytest.fixture
def sample_reviewer(db):
    reviewer = Reviewer(name="Ravi Sharma", languages=["English", "Hindi"])
    db.add(reviewer)
    db.commit()
    db.refresh(reviewer)
    return reviewer


@pytest.fixture
def sample_conversation(db, sample_reviewer):
    conv = Conversation(
        conversation_id="conv_test_001",
        reviewer_id=sample_reviewer.id,
        language="English",
        original_text="I need a deluxe room for 2 adults",
        normalized_text="i need a deluxe room for 2 adults",
        detected_language="English",
        detected_intent="booking",
        entities={"room_type": "deluxe", "guests": 2},
        expected_intent="booking",
        evaluation_score=95.0,
        latency_ms=120.0,
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


@pytest.fixture
def sample_review(db, sample_conversation, sample_reviewer):
    review = Review(
        conversation_id=sample_conversation.id,
        reviewer_id=sample_reviewer.id,
        feedback="Good pronunciation, intent was correct.",
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    rating = Rating(
        review_id=review.id,
        pronunciation=8.5,
        language_accuracy=9.0,
        intent_accuracy=8.0,
        naturalness=7.5,
        conversation_quality=8.5,
        overall_rating=8.3,
    )
    db.add(rating)
    db.commit()

    approval = Approval(
        review_id=review.id,
        status="Approved",
        reviewer_notes="Well done.",
        approved_by="Admin",
    )
    db.add(approval)
    db.commit()

    return review


# ══════════════════════════════════════════════════════════════════════════════
# TASK 10 — Review API Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestReviewAPIs:

    def test_create_reviewer(self, client):
        response = client.post("/reviews/reviewers", json={
            "name": "Priya Patel",
            "languages": ["Hindi", "Marathi"],
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Priya Patel"
        assert "Hindi" in data["languages"]
        assert data["id"] > 0

    def test_list_reviewers(self, client, sample_reviewer):
        response = client.get("/reviews/reviewers")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Ravi Sharma"

    def test_create_conversation(self, client, sample_reviewer):
        response = client.post("/reviews/conversations", json={
            "conversation_id": "conv_002",
            "reviewer_id": sample_reviewer.id,
            "language": "Hindi",
            "original_text": "मुझे एक डीलक्स कमरा चाहिए",
            "normalized_text": "mujhe ek deluxe kamra chahiye",
            "detected_language": "Hindi",
            "detected_intent": "booking",
            "entities": {"room_type": "deluxe"},
            "expected_intent": "booking",
            "evaluation_score": 92.0,
            "latency_ms": 150.0,
        })
        assert response.status_code == 201
        data = response.json()
        assert data["conversation_id"] == "conv_002"
        assert data["language"] == "Hindi"

    def test_create_review(self, client, sample_conversation, sample_reviewer):
        response = client.post("/reviews/create", json={
            "conversation_id": sample_conversation.id,
            "reviewer_id": sample_reviewer.id,
            "feedback": "Excellent handling of booking intent.",
            "ratings": {
                "pronunciation": 9.0,
                "language_accuracy": 9.5,
                "intent_accuracy": 9.0,
                "naturalness": 8.5,
                "conversation_quality": 9.0,
                "overall_rating": 9.0,
            },
            "approval": {
                "status": "Pending",
                "reviewer_notes": "Awaiting final check.",
                "approved_by": None,
            },
        })
        assert response.status_code == 201
        data = response.json()
        assert data["conversation_id"] == sample_conversation.id
        assert data["ratings"]["overall_rating"] == 9.0
        assert data["approval"]["status"] == "Pending"

    def test_create_review_missing_conversation(self, client):
        response = client.post("/reviews/create", json={
            "conversation_id": 999,
            "feedback": "Test",
        })
        assert response.status_code == 404

    def test_list_reviews(self, client, sample_review):
        response = client.get("/reviews?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["page"] == 1
        assert len(data["reviews"]) == 1
        assert data["reviews"][0]["id"] == sample_review.id

    def test_get_review_by_id(self, client, sample_review):
        response = client.get(f"/reviews/{sample_review.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_review.id
        assert data["feedback"] == "Good pronunciation, intent was correct."
        assert data["ratings"]["pronunciation"] == 8.5
        assert data["approval"]["status"] == "Approved"

    def test_get_review_not_found(self, client):
        response = client.get("/reviews/999")
        assert response.status_code == 404

    def test_update_review(self, client, sample_review):
        response = client.put(f"/reviews/{sample_review.id}", json={
            "feedback": "Updated: Excellent work on pronunciation.",
            "ratings": {
                "pronunciation": 9.5,
                "language_accuracy": 9.0,
                "intent_accuracy": 8.5,
                "naturalness": 8.0,
                "conversation_quality": 9.0,
                "overall_rating": 8.8,
            },
            "approval": {
                "status": "Approved",
                "reviewer_notes": "All good after re-evaluation.",
                "approved_by": "Senior Reviewer",
            },
        })
        assert response.status_code == 200
        data = response.json()
        assert data["feedback"] == "Updated: Excellent work on pronunciation."
        assert data["ratings"]["pronunciation"] == 9.5
        assert data["approval"]["status"] == "Approved"

    def test_update_review_not_found(self, client):
        response = client.put("/reviews/999", json={"feedback": "Test"})
        assert response.status_code == 404

    def test_delete_review(self, client, sample_review):
        response = client.delete(f"/reviews/{sample_review.id}")
        assert response.status_code == 204

    def test_delete_review_not_found(self, client):
        response = client.delete("/reviews/999")
        assert response.status_code == 404

    def test_get_reviews_by_language(self, client, sample_review):
        response = client.get("/reviews/language/English")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_get_reviews_by_language_empty(self, client):
        response = client.get("/reviews/language/Telugu")
        assert response.status_code == 200
        data = response.json()
        assert data == []


# ══════════════════════════════════════════════════════════════════════════════
# TASK 10 — Approval Workflow Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestApprovalWorkflow:

    def test_approval_statuses(self, client, sample_conversation, sample_reviewer):
        statuses = ["Pending", "Approved", "Rejected", "Needs Improvement"]
        for status in statuses:
            response = client.post("/reviews/create", json={
                "conversation_id": sample_conversation.id,
                "reviewer_id": sample_reviewer.id,
                "feedback": f"Test review with status {status}",
                "approval": {
                    "status": status,
                    "reviewer_notes": f"Status set to {status}",
                },
            })
            assert response.status_code == 201
            assert response.json()["approval"]["status"] == status

    def test_approval_history_tracked(self, client, db, sample_conversation, sample_reviewer):
        resp = client.post("/reviews/create", json={
            "conversation_id": sample_conversation.id,
            "reviewer_id": sample_reviewer.id,
            "feedback": "Testing approval history",
            "approval": {
                "status": "Pending",
                "reviewer_notes": "Initial review",
            },
        })
        review_id = resp.json()["id"]

        client.put(f"/reviews/{review_id}", json={
            "approval": {
                "status": "Approved",
                "reviewer_notes": "Approved after checking.",
                "approved_by": "Admin",
            },
        })

        approval = db.query(Approval).filter(Approval.review_id == review_id).first()
        history = db.query(ApprovalHistory).filter(
            ApprovalHistory.approval_id == approval.id
        ).order_by(ApprovalHistory.changed_at).all()

        assert len(history) >= 2
        assert history[0].previous_status == "None"
        assert history[0].new_status == "Pending"
        assert history[1].previous_status == "Pending"
        assert history[1].new_status == "Approved"

    def test_invalid_approval_status(self, client, sample_conversation):
        response = client.post("/reviews/create", json={
            "conversation_id": sample_conversation.id,
            "approval": {"status": "InvalidStatus"},
        })
        assert response.status_code == 422


# ══════════════════════════════════════════════════════════════════════════════
# TASK 10 — Rating System Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestRatingSystem:

    def test_rating_categories_present(self, client, sample_conversation, sample_reviewer):
        response = client.post("/reviews/create", json={
            "conversation_id": sample_conversation.id,
            "reviewer_id": sample_reviewer.id,
            "feedback": "Testing all rating categories.",
            "ratings": {
                "pronunciation": 7.0,
                "language_accuracy": 8.0,
                "intent_accuracy": 9.0,
                "naturalness": 6.5,
                "conversation_quality": 8.0,
                "overall_rating": 7.7,
            },
        })
        assert response.status_code == 201
        ratings_data = response.json()["ratings"]
        assert ratings_data["pronunciation"] == 7.0
        assert ratings_data["language_accuracy"] == 8.0
        assert ratings_data["intent_accuracy"] == 9.0
        assert ratings_data["naturalness"] == 6.5
        assert ratings_data["conversation_quality"] == 8.0
        assert ratings_data["overall_rating"] == 7.7

    def test_rating_bounds_validation(self, client, sample_conversation):
        response = client.post("/reviews/create", json={
            "conversation_id": sample_conversation.id,
            "ratings": {
                "pronunciation": 15.0,
                "language_accuracy": 8.0,
                "intent_accuracy": 9.0,
                "naturalness": 6.5,
                "conversation_quality": 8.0,
                "overall_rating": 7.7,
            },
        })
        assert response.status_code == 422

    def test_rating_update(self, client, sample_review):
        response = client.put(f"/reviews/{sample_review.id}", json={
            "ratings": {
                "pronunciation": 10.0,
                "language_accuracy": 10.0,
                "intent_accuracy": 10.0,
                "naturalness": 10.0,
                "conversation_quality": 10.0,
                "overall_rating": 10.0,
            },
        })
        assert response.status_code == 200
        assert response.json()["ratings"]["overall_rating"] == 10.0


# ══════════════════════════════════════════════════════════════════════════════
# TASK 10 — Analytics Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestReviewAnalytics:

    def test_analytics_endpoint(self, client, sample_review):
        response = client.get("/reviews/analytics")
        assert response.status_code == 200
        data = response.json()
        assert data["total_reviews"] >= 1
        assert data["average_rating"] > 0
        assert "language_breakdown" in data
        assert "reviewer_statistics" in data
        assert "approval_rate" in data
        assert "rejection_rate" in data

    def test_analytics_language_breakdown(self, client, sample_review):
        response = client.get("/reviews/analytics")
        data = response.json()
        assert "English" in data["language_breakdown"]
        english_stats = data["language_breakdown"]["English"]
        assert english_stats["average_rating"] > 0
        assert english_stats["review_count"] >= 1

    def test_analytics_reviewer_stats(self, client, sample_review, sample_reviewer):
        response = client.get("/reviews/analytics")
        data = response.json()
        assert data["reviewer_statistics"]["total_reviewers"] >= 1

    def test_analytics_empty(self, client):
        response = client.get("/reviews/analytics")
        assert response.status_code == 200
        data = response.json()
        assert data["total_reviews"] == 0
        assert data["average_rating"] == 0.0


# ══════════════════════════════════════════════════════════════════════════════
# TASK 10 — Reports Tests
# ══════════════════════════════════════════════════════════════════════════════


class TestReviewReports:

    def test_generate_report(self, client, sample_review):
        response = client.get("/reviews/reports/generate")
        assert response.status_code == 200
        data = response.json()
        assert data["report_id"].startswith("report_")
        assert data["total_reviews"] >= 1
        assert "analytics" in data
        assert len(data["recent_reviews"]) >= 1

    def test_report_structure(self, client, sample_review):
        response = client.get("/reviews/reports/generate")
        data = response.json()
        assert "generated_at" in data
        assert "report_id" in data
        assert "total_reviews" in data
        assert "analytics" in data
        assert "recent_reviews" in data
        assert data["analytics"]["total_reviews"] >= 1
        assert data["analytics"]["average_rating"] > 0

    def test_report_without_reviews(self, client):
        response = client.get("/reviews/reports/generate")
        assert response.status_code == 200
        data = response.json()
        assert data["total_reviews"] == 0
