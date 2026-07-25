"""
FastAPI Router for StayZa Native Review System.
"""


from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from review_system.analytics import AnalyticsEngine
from review_system.database import get_db
from review_system.reports import ReportGenerator
from review_system.schemas import (
    ApprovalResponse,
    ConversationCreate,
    ConversationResponse,
    RatingResponse,
    ReviewAnalytics,
    ReviewCreate,
    ReviewerCreate,
    ReviewerResponse,
    ReviewListResponse,
    ReviewReport,
    ReviewResponse,
    ReviewUpdate,
)
from review_system.service import ReviewService

router = APIRouter(prefix="/reviews", tags=["Native Review System"])


def get_service(db: Session = Depends(get_db)) -> ReviewService:
    return ReviewService(db)


# ── Reviewer Endpoints ────────────────────────────────────────────────────────


@router.post(
    "/reviewers",
    response_model=ReviewerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Reviewer",
    description="Register a new native language reviewer.",
)
def create_reviewer(
    data: ReviewerCreate,
    service: ReviewService = Depends(get_service),
) -> ReviewerResponse:
    reviewer = service.create_reviewer(data)
    return ReviewerResponse(
        id=reviewer.id,
        name=reviewer.name,
        languages=reviewer.languages,
        created_at=reviewer.created_at.isoformat() if reviewer.created_at else None,
    )


@router.get(
    "/reviewers",
    response_model=list[ReviewerResponse],
    summary="List Reviewers",
    description="Get all registered reviewers.",
)
def list_reviewers(
    service: ReviewService = Depends(get_service),
) -> list[ReviewerResponse]:
    reviewers = service.get_all_reviewers()
    return [
        ReviewerResponse(
            id=r.id,
            name=r.name,
            languages=r.languages,
            created_at=r.created_at.isoformat() if r.created_at else None,
        )
        for r in reviewers
    ]


# ── Conversation Endpoints ────────────────────────────────────────────────────


@router.post(
    "/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Conversation",
    description="Store a conversation for review.",
)
def create_conversation(
    data: ConversationCreate,
    service: ReviewService = Depends(get_service),
) -> ConversationResponse:
    conv = service.create_conversation(data)
    return ConversationResponse(
        id=conv.id,
        conversation_id=conv.conversation_id,
        reviewer_id=conv.reviewer_id,
        language=conv.language,
        original_text=conv.original_text,
        normalized_text=conv.normalized_text,
        detected_language=conv.detected_language,
        detected_intent=conv.detected_intent,
        entities=conv.entities,
        expected_intent=conv.expected_intent,
        evaluation_score=conv.evaluation_score,
        latency_ms=conv.latency_ms,
        timestamp=conv.timestamp.isoformat() if conv.timestamp else None,
    )


# ── Review CRUD Endpoints ─────────────────────────────────────────────────────


@router.post(
    "/create",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Review",
    description="Create a new review for a conversation with ratings and approval.",
)
def create_review(
    data: ReviewCreate,
    service: ReviewService = Depends(get_service),
) -> ReviewResponse:
    if not service.get_conversation(data.conversation_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation with id {data.conversation_id} not found.",
        )
    review = service.create_review(data)
    return _build_review_response(review)


@router.get(
    "",
    response_model=ReviewListResponse,
    summary="List Reviews",
    description="Get paginated list of all reviews.",
)
def list_reviews(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    service: ReviewService = Depends(get_service),
) -> ReviewListResponse:
    result = service.get_all_reviews(page=page, page_size=page_size)
    return ReviewListResponse(
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        reviews=[_build_review_response(r) for r in result["reviews"]],
    )


@router.get(
    "/language/{language}",
    response_model=list[ReviewResponse],
    summary="Get Reviews by Language",
    description="Get all reviews for conversations in a specific language.",
)
def get_reviews_by_language(
    language: str,
    service: ReviewService = Depends(get_service),
) -> list[ReviewResponse]:
    reviews = service.get_reviews_by_language(language)
    return [_build_review_response(r) for r in reviews]


# ── Analytics & Reports (must be before /{review_id} to avoid path conflicts) ──


@router.get(
    "/analytics",
    response_model=ReviewAnalytics,
    summary="Review Analytics",
    description="Get analytics including average ratings, language breakdown, reviewer stats, and approval rates.",
)
def get_review_analytics(
    service: ReviewService = Depends(get_service),
) -> ReviewAnalytics:
    db = service.db
    engine = AnalyticsEngine(db)
    return engine.generate_analytics()


@router.get(
    "/reports/generate",
    response_model=ReviewReport,
    summary="Generate Review Report",
    description="Generate and store a JSON review report with full analytics.",
)
def generate_review_report(
    service: ReviewService = Depends(get_service),
) -> ReviewReport:
    db = service.db
    engine = AnalyticsEngine(db)
    analytics = engine.generate_analytics()
    generator = ReportGenerator(db)
    return generator.generate_report(analytics)


# ── Review Single-Resource Endpoints (must be after analytics/reports) ────────


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Get Review",
    description="Get a single review by ID.",
)
def get_review(
    review_id: int,
    service: ReviewService = Depends(get_service),
) -> ReviewResponse:
    review = service.get_review(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found.",
        )
    return _build_review_response(review)


@router.put(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Update Review",
    description="Update feedback, ratings, and approval status for a review.",
)
def update_review(
    review_id: int,
    data: ReviewUpdate,
    service: ReviewService = Depends(get_service),
) -> ReviewResponse:
    review = service.update_review(review_id, data)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found.",
        )
    return _build_review_response(review)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Review",
    description="Delete a review and its associated ratings and approvals.",
)
def delete_review(
    review_id: int,
    service: ReviewService = Depends(get_service),
) -> None:
    if not service.delete_review(review_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with id {review_id} not found.",
        )


# ── Helpers ───────────────────────────────────────────────────────────────────


def _build_review_response(review) -> ReviewResponse:
    conv = review.conversation
    conv_resp = (
        ConversationResponse(
            id=conv.id,
            conversation_id=conv.conversation_id,
            reviewer_id=conv.reviewer_id,
            language=conv.language,
            original_text=conv.original_text,
            normalized_text=conv.normalized_text,
            detected_language=conv.detected_language,
            detected_intent=conv.detected_intent,
            entities=conv.entities,
            expected_intent=conv.expected_intent,
            evaluation_score=conv.evaluation_score,
            latency_ms=conv.latency_ms,
            timestamp=conv.timestamp.isoformat() if conv.timestamp else None,
        )
        if conv
        else None
    )

    reviewer = review.reviewer
    rev_resp = (
        ReviewerResponse(
            id=reviewer.id,
            name=reviewer.name,
            languages=reviewer.languages,
            created_at=reviewer.created_at.isoformat() if reviewer.created_at else None,
        )
        if reviewer
        else None
    )

    ratings = review.ratings
    rat_resp = (
        RatingResponse(
            id=ratings.id,
            review_id=ratings.review_id,
            pronunciation=ratings.pronunciation,
            language_accuracy=ratings.language_accuracy,
            intent_accuracy=ratings.intent_accuracy,
            naturalness=ratings.naturalness,
            conversation_quality=ratings.conversation_quality,
            overall_rating=ratings.overall_rating,
        )
        if ratings
        else None
    )

    approval = review.approvals
    app_resp = (
        ApprovalResponse(
            id=approval.id,
            review_id=approval.review_id,
            status=approval.status,
            reviewer_notes=approval.reviewer_notes,
            approved_by=approval.approved_by,
            created_at=approval.created_at.isoformat() if approval.created_at else None,
            updated_at=approval.updated_at.isoformat() if approval.updated_at else None,
        )
        if approval
        else None
    )

    return ReviewResponse(
        id=review.id,
        conversation_id=review.conversation_id,
        reviewer_id=review.reviewer_id,
        feedback=review.feedback,
        reviewer_feedback=review.reviewer_feedback,
        created_at=review.created_at.isoformat() if review.created_at else None,
        updated_at=review.updated_at.isoformat() if review.updated_at else None,
        conversation=conv_resp,
        reviewer=rev_resp,
        ratings=rat_resp,
        approval=app_resp,
    )
