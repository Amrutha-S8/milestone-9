"""
Business logic service for StayZa Native Review System.
"""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import desc
from sqlalchemy.orm import Session

from review_system.models import (
    Approval,
    ApprovalHistory,
    Conversation,
    Rating,
    Review,
    Reviewer,
)
from review_system.schemas import (
    ApprovalCreate,
    ConversationCreate,
    RatingCreate,
    ReviewCreate,
    ReviewerCreate,
    ReviewUpdate,
)


class ReviewService:

    def __init__(self, db: Session):
        self.db = db

    # ── Reviewer ──────────────────────────────────────────────────────────────

    def create_reviewer(self, data: ReviewerCreate) -> Reviewer:
        reviewer = Reviewer(name=data.name, languages=data.languages)
        self.db.add(reviewer)
        self.db.commit()
        self.db.refresh(reviewer)
        return reviewer

    def get_reviewer(self, reviewer_id: int) -> Reviewer | None:
        return self.db.query(Reviewer).filter(Reviewer.id == reviewer_id).first()

    def get_all_reviewers(self) -> list[Reviewer]:
        return self.db.query(Reviewer).all()

    # ── Conversation ──────────────────────────────────────────────────────────

    def create_conversation(self, data: ConversationCreate) -> Conversation:
        conv = Conversation(
            conversation_id=data.conversation_id,
            reviewer_id=data.reviewer_id,
            language=data.language,
            original_text=data.original_text,
            normalized_text=data.normalized_text,
            detected_language=data.detected_language,
            detected_intent=data.detected_intent,
            entities=data.entities,
            expected_intent=data.expected_intent,
            evaluation_score=data.evaluation_score,
            latency_ms=data.latency_ms,
        )
        self.db.add(conv)
        self.db.commit()
        self.db.refresh(conv)
        return conv

    def get_conversation(self, conversation_id: int) -> Conversation | None:
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def get_conversations_by_language(self, language: str) -> list[Conversation]:
        return self.db.query(Conversation).filter(Conversation.language == language).all()

    def get_all_conversations(self) -> list[Conversation]:
        return self.db.query(Conversation).all()

    # ── Review ────────────────────────────────────────────────────────────────

    def create_review(self, data: ReviewCreate) -> Review:
        review = Review(
            conversation_id=data.conversation_id,
            reviewer_id=data.reviewer_id,
            feedback=data.feedback,
            reviewer_feedback=data.reviewer_feedback,
        )
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)

        if data.ratings:
            self._create_ratings(review.id, data.ratings)

        if data.approval:
            self._create_approval(review.id, data.approval)

        self.db.refresh(review)
        return review

    def get_review(self, review_id: int) -> Review | None:
        return self.db.query(Review).filter(Review.id == review_id).first()

    def get_all_reviews(
        self, page: int = 1, page_size: int = 20
    ) -> dict[str, Any]:
        total = self.db.query(Review).count()
        offset = (page - 1) * page_size
        reviews = (
            self.db.query(Review)
            .order_by(desc(Review.created_at))
            .offset(offset)
            .limit(page_size)
            .all()
        )
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "reviews": reviews,
        }

    def update_review(self, review_id: int, data: ReviewUpdate) -> Review | None:
        review = self.get_review(review_id)
        if not review:
            return None

        if data.feedback is not None:
            review.feedback = data.feedback
        if data.reviewer_feedback is not None:
            review.reviewer_feedback = data.reviewer_feedback
        review.updated_at = datetime.now(UTC)

        if data.ratings:
            existing = self.db.query(Rating).filter(Rating.review_id == review_id).first()
            if existing:
                self._update_ratings(existing, data.ratings)
            else:
                self._create_ratings(review_id, data.ratings)

        if data.approval:
            existing = self.db.query(Approval).filter(Approval.review_id == review_id).first()
            if existing:
                self._update_approval(existing, data.approval)
            else:
                self._create_approval(review_id, data.approval)

        self.db.commit()
        self.db.refresh(review)
        return review

    def delete_review(self, review_id: int) -> bool:
        review = self.get_review(review_id)
        if not review:
            return False

        self.db.query(Rating).filter(Rating.review_id == review_id).delete()
        self.db.query(ApprovalHistory).filter(
            ApprovalHistory.approval_id.in_(
                self.db.query(Approval.id).filter(Approval.review_id == review_id)
            )
        ).delete(synchronize_session=False)
        self.db.query(Approval).filter(Approval.review_id == review_id).delete()
        self.db.delete(review)
        self.db.commit()
        return True

    def get_reviews_by_language(self, language: str) -> list[Review]:
        return (
            self.db.query(Review)
            .join(Conversation)
            .filter(Conversation.language == language)
            .all()
        )

    # ── Ratings ───────────────────────────────────────────────────────────────

    def _create_ratings(self, review_id: int, data: RatingCreate) -> Rating:
        rating = Rating(
            review_id=review_id,
            pronunciation=data.pronunciation,
            language_accuracy=data.language_accuracy,
            intent_accuracy=data.intent_accuracy,
            naturalness=data.naturalness,
            conversation_quality=data.conversation_quality,
            overall_rating=data.overall_rating,
        )
        self.db.add(rating)
        self.db.commit()

    def _update_ratings(self, rating: Rating, data: RatingCreate) -> None:
        rating.pronunciation = data.pronunciation
        rating.language_accuracy = data.language_accuracy
        rating.intent_accuracy = data.intent_accuracy
        rating.naturalness = data.naturalness
        rating.conversation_quality = data.conversation_quality
        rating.overall_rating = data.overall_rating
        self.db.commit()

    # ── Approval ──────────────────────────────────────────────────────────────

    def _create_approval(self, review_id: int, data: ApprovalCreate) -> Approval:
        approval = Approval(
            review_id=review_id,
            status=data.status,
            reviewer_notes=data.reviewer_notes,
            approved_by=data.approved_by,
        )
        self.db.add(approval)
        self.db.commit()

        history = ApprovalHistory(
            approval_id=approval.id,
            previous_status="None",
            new_status=data.status,
            notes="Initial approval created.",
        )
        self.db.add(history)
        self.db.commit()
        return approval

    def _update_approval(self, approval: Approval, data: ApprovalCreate) -> None:
        previous = approval.status
        if data.status is not None:
            approval.status = data.status
        if data.reviewer_notes is not None:
            approval.reviewer_notes = data.reviewer_notes
        if data.approved_by is not None:
            approval.approved_by = data.approved_by
        approval.updated_at = datetime.now(UTC)
        self.db.commit()

        history = ApprovalHistory(
            approval_id=approval.id,
            previous_status=previous,
            new_status=approval.status,
            notes=data.reviewer_notes,
        )
        self.db.add(history)
        self.db.commit()

    def get_approval_history(self, approval_id: int) -> list[ApprovalHistory]:
        return (
            self.db.query(ApprovalHistory)
            .filter(ApprovalHistory.approval_id == approval_id)
            .order_by(desc(ApprovalHistory.changed_at))
            .all()
        )
