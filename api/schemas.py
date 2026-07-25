"""
Pydantic schemas for StayZa Milestone 9 API.
Day 4: Added normalized_text field and LanguageSupportInfo model.
Day 5: Added evaluation schemas for Evaluation Engine.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    """
    Input schema for language analysis endpoint.
    """
    text: str = Field(
        ...,
        description="Utterance text to analyze for language, intent, entities, and flow action.",
        examples=["I need a deluxe room for 2 adults tomorrow."]
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Unique voice session identifier."
    )
    current_state: Optional[str] = Field(
        default=None,
        description="Current dialog state in conversation flow."
    )


class AnalyzeResponse(BaseModel):
    """
    Upgraded Day 3 response schema:
    {
      "language": "English",
      "intent": "booking",
      "entities": {
        "guests": 2,
        "room_type": "Deluxe"
      },
      "next_action": "ask_checkin_date",
      "confidence": 0.97
    }
    """
    language: str = Field(..., examples=["English"])
    intent: str = Field(..., examples=["booking"])
    entities: Dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted entities (check_in, guests, room_type, budget, booking_id, guest_name).",
        examples=[{"guests": 2, "room_type": "Deluxe"}]
    )
    next_action: str = Field(..., examples=["ask_checkin_date"])
    confidence: float = Field(..., ge=0.0, le=1.0, examples=[0.97])
    flow: Optional[str] = Field(default=None, examples=["booking"])
    session_id: Optional[str] = Field(default=None)
    response_template: Optional[str] = Field(default=None)
    normalized_text: Optional[str] = Field(
        default=None,
        description="Preprocessed text after noise removal and domain normalization."
    )


class LanguageDetectRequest(BaseModel):
    text: str = Field(..., examples=["మాకు ఒక గది కావాలి"])


class LanguageDetectResponse(BaseModel):
    language: str = Field(..., examples=["Telugu"])
    confidence: float = Field(..., examples=[0.98])


class SessionContextResponse(BaseModel):
    session_id: str
    active_language: str
    active_flow: Optional[str] = None
    current_intent: Optional[str] = None
    slot_memory: Dict[str, Any]
    history: list


class LanguageSupportInfo(BaseModel):
    """Metadata about a registered language flow module."""
    code: str = Field(..., examples=["te"])
    name: str = Field(..., examples=["Telugu"])
    status: str = Field(default="active", examples=["active"])
    supported_intents: List[str] = Field(default_factory=list)


class LanguageStatusResponse(BaseModel):
    """Pass/Fail status for a language after evaluation."""
    language: str = Field(..., examples=["English"])
    accuracy: float = Field(..., examples=[98.2])
    wer: float = Field(..., examples=[2.3])
    flow_completion: float = Field(..., examples=[99.1])
    latency: float = Field(..., examples=[185.0])
    final_score: float = Field(..., examples=[97.0])
    status: str = Field(..., examples=["PASS"])
    enabled: bool = Field(..., examples=[True])


class EvaluationRunResponse(BaseModel):
    """Response from running the full evaluation engine."""
    summary: Dict[str, Any]
    per_language: Dict[str, Any]
    report_path: str
    status: Dict[str, Any]


# ══════════════════════════════════════════════════════════════════════════════
# Day 6: Native Review System Schemas
# ══════════════════════════════════════════════════════════════════════════════


class ReviewerSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Ravi Sharma"])
    languages: List[str] = Field(default_factory=list, examples=[["English", "Hindi"]])


class ReviewerResponseSchema(BaseModel):
    id: int
    name: str
    languages: List[str]
    created_at: Optional[str] = None


class ConversationSchema(BaseModel):
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


class ConversationResponseSchema(BaseModel):
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


class RatingSchema(BaseModel):
    pronunciation: float = Field(..., ge=0.0, le=10.0, examples=[8.5])
    language_accuracy: float = Field(..., ge=0.0, le=10.0, examples=[9.0])
    intent_accuracy: float = Field(..., ge=0.0, le=10.0, examples=[8.0])
    naturalness: float = Field(..., ge=0.0, le=10.0, examples=[7.5])
    conversation_quality: float = Field(..., ge=0.0, le=10.0, examples=[8.5])
    overall_rating: float = Field(..., ge=0.0, le=10.0, examples=[8.3])


class RatingResponseSchema(BaseModel):
    id: int
    review_id: int
    pronunciation: float
    language_accuracy: float
    intent_accuracy: float
    naturalness: float
    conversation_quality: float
    overall_rating: float


class ApprovalSchema(BaseModel):
    status: str = Field(..., pattern="^(Pending|Approved|Rejected|Needs Improvement)$", examples=["Pending"])
    reviewer_notes: Optional[str] = None
    approved_by: Optional[str] = None


class ApprovalResponseSchema(BaseModel):
    id: int
    review_id: int
    status: str
    reviewer_notes: Optional[str] = None
    approved_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ReviewCreateSchema(BaseModel):
    conversation_id: int = Field(..., examples=[1])
    reviewer_id: Optional[int] = None
    feedback: Optional[str] = Field(None, examples=["Good pronunciation, but intent was off."])
    reviewer_feedback: Optional[str] = None
    ratings: Optional[RatingSchema] = None
    approval: Optional[ApprovalSchema] = None


class ReviewUpdateSchema(BaseModel):
    feedback: Optional[str] = None
    reviewer_feedback: Optional[str] = None
    ratings: Optional[RatingSchema] = None
    approval: Optional[ApprovalSchema] = None


class ReviewResponseSchema(BaseModel):
    id: int
    conversation_id: int
    reviewer_id: Optional[int] = None
    feedback: Optional[str] = None
    reviewer_feedback: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    conversation: Optional[ConversationResponseSchema] = None
    reviewer: Optional[ReviewerResponseSchema] = None
    ratings: Optional[RatingResponseSchema] = None
    approval: Optional[ApprovalResponseSchema] = None


class ReviewListResponseSchema(BaseModel):
    total: int
    page: int
    page_size: int
    reviews: List[ReviewResponseSchema]


class ReviewAnalyticsSchema(BaseModel):
    average_rating: float
    total_reviews: int
    language_breakdown: Dict[str, Any]
    reviewer_statistics: Dict[str, Any]
    approval_rate: float
    rejection_rate: float
    needs_improvement_rate: float
    pending_rate: float
    rating_distribution: Dict[str, float]


class ReviewReportSchema(BaseModel):
    report_id: str
    generated_at: str
    total_reviews: int
    analytics: ReviewAnalyticsSchema
    recent_reviews: List[ReviewResponseSchema]
