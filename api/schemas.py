"""
Pydantic schemas for StayZa Milestone 9 API.
Day 4: Added normalized_text field and LanguageSupportInfo model.
Day 5: Added evaluation schemas for Evaluation Engine.
"""

from typing import Any

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
    session_id: str | None = Field(
        default=None,
        description="Unique voice session identifier."
    )
    current_state: str | None = Field(
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
    entities: dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted entities (check_in, guests, room_type, budget, booking_id, guest_name).",
        examples=[{"guests": 2, "room_type": "Deluxe"}]
    )
    next_action: str = Field(..., examples=["ask_checkin_date"])
    confidence: float = Field(..., ge=0.0, le=1.0, examples=[0.97])
    flow: str | None = Field(default=None, examples=["booking"])
    session_id: str | None = Field(default=None)
    response_template: str | None = Field(default=None)
    normalized_text: str | None = Field(
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
    active_flow: str | None = None
    current_intent: str | None = None
    slot_memory: dict[str, Any]
    history: list


class LanguageSupportInfo(BaseModel):
    """Metadata about a registered language flow module."""
    code: str = Field(..., examples=["te"])
    name: str = Field(..., examples=["Telugu"])
    status: str = Field(default="active", examples=["active"])
    supported_intents: list[str] = Field(default_factory=list)


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
    summary: dict[str, Any]
    per_language: dict[str, Any]
    report_path: str | None = None
    status: dict[str, Any]


# ══════════════════════════════════════════════════════════════════════════════
# Day 6: Native Review System Schemas
# ══════════════════════════════════════════════════════════════════════════════


class ReviewerSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, examples=["Ravi Sharma"])
    languages: list[str] = Field(default_factory=list, examples=[["English", "Hindi"]])


class ReviewerResponseSchema(BaseModel):
    id: int
    name: str
    languages: list[str]
    created_at: str | None = None


class ConversationSchema(BaseModel):
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


class ConversationResponseSchema(BaseModel):
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
    reviewer_notes: str | None = None
    approved_by: str | None = None


class ApprovalResponseSchema(BaseModel):
    id: int
    review_id: int
    status: str
    reviewer_notes: str | None = None
    approved_by: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class ReviewCreateSchema(BaseModel):
    conversation_id: int = Field(..., examples=[1])
    reviewer_id: int | None = None
    feedback: str | None = Field(None, examples=["Good pronunciation, but intent was off."])
    reviewer_feedback: str | None = None
    ratings: RatingSchema | None = None
    approval: ApprovalSchema | None = None


class ReviewUpdateSchema(BaseModel):
    feedback: str | None = None
    reviewer_feedback: str | None = None
    ratings: RatingSchema | None = None
    approval: ApprovalSchema | None = None


class ReviewResponseSchema(BaseModel):
    id: int
    conversation_id: int
    reviewer_id: int | None = None
    feedback: str | None = None
    reviewer_feedback: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    conversation: ConversationResponseSchema | None = None
    reviewer: ReviewerResponseSchema | None = None
    ratings: RatingResponseSchema | None = None
    approval: ApprovalResponseSchema | None = None


class ReviewListResponseSchema(BaseModel):
    total: int
    page: int
    page_size: int
    reviews: list[ReviewResponseSchema]


class ReviewAnalyticsSchema(BaseModel):
    average_rating: float
    total_reviews: int
    language_breakdown: dict[str, Any]
    reviewer_statistics: dict[str, Any]
    approval_rate: float
    rejection_rate: float
    needs_improvement_rate: float
    pending_rate: float
    rating_distribution: dict[str, float]


class ReviewReportSchema(BaseModel):
    report_id: str
    generated_at: str
    total_reviews: int
    analytics: ReviewAnalyticsSchema
    recent_reviews: list[ReviewResponseSchema]
