"""
Pydantic schemas for StayZa Native Review System.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ReviewerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Ravi Sharma"])
    languages: List[str] = Field(default_factory=list, examples=[["English", "Hindi"]])


class ReviewerResponse(BaseModel):
    id: int
    name: str
    languages: List[str]
    created_at: Optional[str] = None


class ConversationCreate(BaseModel):
    conversation_id: str = Field(..., examples=["conv_001"])
    reviewer_id: Optional[int] = None
    language: str = Field(..., examples=["English"])
    original_text: str = Field(..., examples=["I need a deluxe room for 2 adults"])
    normalized_text: Optional[str] = None
    detected_language: Optional[str] = None
    detected_intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    expected_intent: Optional[str] = None
    evaluation_score: Optional[float] = None
    latency_ms: Optional[float] = None


class ConversationResponse(BaseModel):
    id: int
    conversation_id: str
    reviewer_id: Optional[int] = None
    language: str
    original_text: str
    normalized_text: Optional[str] = None
    detected_language: Optional[str] = None
    detected_intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None
    expected_intent: Optional[str] = None
    evaluation_score: Optional[float] = None
    latency_ms: Optional[float] = None
    timestamp: Optional[str] = None


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
    reviewer_notes: Optional[str] = None
    approved_by: Optional[str] = None


class ApprovalResponse(BaseModel):
    id: int
    review_id: int
    status: str
    reviewer_notes: Optional[str] = None
    approved_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ApprovalHistoryResponse(BaseModel):
    id: int
    approval_id: int
    reviewer_id: Optional[int] = None
    previous_status: str
    new_status: str
    notes: Optional[str] = None
    changed_at: Optional[str] = None


class ReviewCreate(BaseModel):
    conversation_id: int = Field(..., examples=[1])
    reviewer_id: Optional[int] = None
    feedback: Optional[str] = Field(None, examples=["Good pronunciation, but intent was off."])
    reviewer_feedback: Optional[str] = None
    ratings: Optional[RatingCreate] = None
    approval: Optional[ApprovalCreate] = None


class ReviewUpdate(BaseModel):
    feedback: Optional[str] = None
    reviewer_feedback: Optional[str] = None
    ratings: Optional[RatingCreate] = None
    approval: Optional[ApprovalCreate] = None


class ReviewResponse(BaseModel):
    id: int
    conversation_id: int
    reviewer_id: Optional[int] = None
    feedback: Optional[str] = None
    reviewer_feedback: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    conversation: Optional[ConversationResponse] = None
    reviewer: Optional[ReviewerResponse] = None
    ratings: Optional[RatingResponse] = None
    approval: Optional[ApprovalResponse] = None


class ReviewListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    reviews: List[ReviewResponse]


class ReviewAnalytics(BaseModel):
    average_rating: float
    total_reviews: int
    language_breakdown: Dict[str, Any]
    reviewer_statistics: Dict[str, Any]
    approval_rate: float
    rejection_rate: float
    needs_improvement_rate: float
    pending_rate: float
    rating_distribution: Dict[str, float]


class ReviewReport(BaseModel):
    report_id: str
    generated_at: str
    total_reviews: int
    analytics: ReviewAnalytics
    recent_reviews: List[ReviewResponse]