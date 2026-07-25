"""
Pydantic schemas for StayZa Native Review System.
"""

from typing import Any

from pydantic import BaseModel, Field


class ReviewerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Ravi Sharma"])
    languages: list[str] = Field(default_factory=list, examples=[["English", "Hindi"]])


class ReviewerResponse(BaseModel):
    id: int
    name: str
    languages: list[str]
    created_at: str | None = None


class ConversationCreate(BaseModel):
    conversation_id: str = Field(..., examples=["conv_001"])
    reviewer_id: int | None = None
    language: str = Field(..., examples=["English"])
    original_text: str = Field(..., examples=["I need a deluxe room for 2 adults"])
    normalized_text: str | None = None
    detected_language: str | None = None
    detected_intent: str | None = None
    entities: dict[str, Any] | None = None
    expected_intent: str | None = None
    evaluation_score: float | None = None
    latency_ms: float | None = None


class ConversationResponse(BaseModel):
    id: int
    conversation_id: str
    reviewer_id: int | None = None
    language: str
    original_text: str
    normalized_text: str | None = None
    detected_language: str | None = None
    detected_intent: str | None = None
    entities: dict[str, Any] | None = None
    expected_intent: str | None = None
    evaluation_score: float | None = None
    latency_ms: float | None = None
    timestamp: str | None = None


class RatingCreate(BaseModel):
    pronunciation: float = Field(..., ge=0.0, le=10.0, examples=[8.5])
    language_accuracy: float = Field(..., ge=0.0, le=10.0, examples=[9.0])
    intent_accuracy: float = Field(..., ge=0.0, le=10.0, examples=[8.0])
    naturalness: float = Field(..., ge=0.0, le=10.0, examples=[7.5])
    conversation_quality: float = Field(..., ge=0.0, le=10.0, examples=[8.5])
    overall_rating: float = Field(..., ge=0.0, le=10.0, examples=[8.3])


class RatingResponse(BaseModel):
    id: int
    review_id: int
    pronunciation: float
    language_accuracy: float
    intent_accuracy: float
    naturalness: float
    conversation_quality: float
    overall_rating: float


class ApprovalCreate(BaseModel):
    status: str = Field(..., pattern="^(Pending|Approved|Rejected|Needs Improvement)$", examples=["Pending"])
    reviewer_notes: str | None = None
    approved_by: str | None = None


class ApprovalResponse(BaseModel):
    id: int
    review_id: int
    status: str
    reviewer_notes: str | None = None
    approved_by: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ApprovalHistoryResponse(BaseModel):
    id: int
    approval_id: int
    reviewer_id: int | None = None
    previous_status: str
    new_status: str
    notes: str | None = None
    changed_at: str | None = None


class ReviewCreate(BaseModel):
    conversation_id: int = Field(..., examples=[1])
    reviewer_id: int | None = None
    feedback: str | None = Field(None, examples=["Good pronunciation, but intent was off."])
    reviewer_feedback: str | None = None
    ratings: RatingCreate | None = None
    approval: ApprovalCreate | None = None


class ReviewUpdate(BaseModel):
    feedback: str | None = None
    reviewer_feedback: str | None = None
    ratings: RatingCreate | None = None
    approval: ApprovalCreate | None = None


class ReviewResponse(BaseModel):
    id: int
    conversation_id: int
    reviewer_id: int | None = None
    feedback: str | None = None
    reviewer_feedback: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    conversation: ConversationResponse | None = None
    reviewer: ReviewerResponse | None = None
    ratings: RatingResponse | None = None
    approval: ApprovalResponse | None = None


class ReviewListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    reviews: list[ReviewResponse]


class ReviewAnalytics(BaseModel):
    average_rating: float
    total_reviews: int
    language_breakdown: dict[str, Any]
    reviewer_statistics: dict[str, Any]
    approval_rate: float
    rejection_rate: float
    needs_improvement_rate: float
    pending_rate: float
    rating_distribution: dict[str, float]


class ReviewReport(BaseModel):
    report_id: str
    generated_at: str
    total_reviews: int
    analytics: ReviewAnalytics
    recent_reviews: list[ReviewResponse]
