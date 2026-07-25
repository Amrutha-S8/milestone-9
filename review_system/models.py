"""
SQLAlchemy models for StayZa Native Review System.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from review_system.database import Base


class Reviewer(Base):
    __tablename__ = "reviewers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    languages = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    conversations = relationship("Conversation", back_populates="reviewer")
    reviews = relationship("Review", back_populates="reviewer")
    approval_history = relationship("ApprovalHistory", back_populates="reviewer")

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "languages": self.languages,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(255), nullable=False, index=True)
    reviewer_id = Column(Integer, ForeignKey("reviewers.id"), nullable=True)
    language = Column(String(50), nullable=False, index=True)
    original_text = Column(Text, nullable=False)
    normalized_text = Column(Text, nullable=True)
    detected_language = Column(String(50), nullable=True)
    detected_intent = Column(String(100), nullable=True)
    entities = Column(JSON, nullable=True)
    expected_intent = Column(String(100), nullable=True)
    evaluation_score = Column(Float, nullable=True)
    latency_ms = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    reviewer = relationship("Reviewer", back_populates="conversations")
    reviews = relationship("Review", back_populates="conversation")

    def dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "reviewer_id": self.reviewer_id,
            "language": self.language,
            "original_text": self.original_text,
            "normalized_text": self.normalized_text,
            "detected_language": self.detected_language,
            "detected_intent": self.detected_intent,
            "entities": self.entities,
            "expected_intent": self.expected_intent,
            "evaluation_score": self.evaluation_score,
            "latency_ms": self.latency_ms,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("reviewers.id"), nullable=True)
    feedback = Column(Text, nullable=True)
    reviewer_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    conversation = relationship("Conversation", back_populates="reviews")
    reviewer = relationship("Reviewer", back_populates="reviews")
    ratings = relationship("Rating", back_populates="review", uselist=False)
    approvals = relationship("Approval", back_populates="review", uselist=False)

    def dict(self, include_relations=False):
        result = {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "reviewer_id": self.reviewer_id,
            "feedback": self.feedback,
            "reviewer_feedback": self.reviewer_feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        if include_relations:
            result["conversation"] = self.conversation.dict() if self.conversation else None
            result["reviewer"] = self.reviewer.dict() if self.reviewer else None
            result["ratings"] = self.ratings.dict() if self.ratings else None
            result["approvals"] = self.approvals.dict() if self.approvals else None
        return result


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, unique=True)
    pronunciation = Column(Float, nullable=False, default=0.0)
    language_accuracy = Column(Float, nullable=False, default=0.0)
    intent_accuracy = Column(Float, nullable=False, default=0.0)
    naturalness = Column(Float, nullable=False, default=0.0)
    conversation_quality = Column(Float, nullable=False, default=0.0)
    overall_rating = Column(Float, nullable=False, default=0.0)

    review = relationship("Review", back_populates="ratings")

    def dict(self):
        return {
            "id": self.id,
            "review_id": self.review_id,
            "pronunciation": self.pronunciation,
            "language_accuracy": self.language_accuracy,
            "intent_accuracy": self.intent_accuracy,
            "naturalness": self.naturalness,
            "conversation_quality": self.conversation_quality,
            "overall_rating": self.overall_rating,
        }


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False, unique=True)
    status = Column(String(50), nullable=False, default="Pending")
    reviewer_notes = Column(Text, nullable=True)
    approved_by = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    review = relationship("Review", back_populates="approvals")

    def dict(self):
        return {
            "id": self.id,
            "review_id": self.review_id,
            "status": self.status,
            "reviewer_notes": self.reviewer_notes,
            "approved_by": self.approved_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ApprovalHistory(Base):
    __tablename__ = "approval_history"

    id = Column(Integer, primary_key=True, index=True)
    approval_id = Column(Integer, ForeignKey("approvals.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("reviewers.id"), nullable=True)
    previous_status = Column(String(50), nullable=False)
    new_status = Column(String(50), nullable=False)
    notes = Column(Text, nullable=True)
    changed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    reviewer = relationship("Reviewer", back_populates="approval_history")

    def dict(self):
        return {
            "id": self.id,
            "approval_id": self.approval_id,
            "reviewer_id": self.reviewer_id,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "notes": self.notes,
            "changed_at": self.changed_at.isoformat() if self.changed_at else None,
        }