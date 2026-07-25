"""
JSON Report Generator for StayZa Native Review System.
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from review_system.models import Review, Rating, Approval, Conversation, Reviewer


REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "review_data", "reports")


class ReportGenerator:

    def __init__(self, db: Session):
        self.db = db
        os.makedirs(REPORT_DIR, exist_ok=True)

    def generate_report(self, analytics: Dict[str, Any]) -> Dict[str, Any]:
        recent_reviews = self._get_recent_reviews(limit=10)
        report_id = f"report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"

        report = {
            "report_id": report_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_reviews": analytics["total_reviews"],
            "analytics": analytics,
            "recent_reviews": recent_reviews,
        }

        filepath = os.path.join(REPORT_DIR, f"{report_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, default=str)

        return report

    def _get_recent_reviews(self, limit: int = 10) -> List[Dict[str, Any]]:
        reviews = (
            self.db.query(Review)
            .order_by(desc(Review.created_at))
            .limit(limit)
            .all()
        )

        result = []
        for review in reviews:
            conv = review.conversation
            ratings = review.ratings
            approval = review.approvals
            reviewer = review.reviewer

            result.append({
                "id": review.id,
                "conversation_id": review.conversation_id,
                "reviewer_id": review.reviewer_id,
                "feedback": review.feedback,
                "reviewer_feedback": review.reviewer_feedback,
                "created_at": review.created_at.isoformat() if review.created_at else None,
                "updated_at": review.updated_at.isoformat() if review.updated_at else None,
                "conversation": {
                    "id": conv.id,
                    "conversation_id": conv.conversation_id,
                    "language": conv.language,
                    "original_text": conv.original_text,
                    "normalized_text": conv.normalized_text,
                    "detected_language": conv.detected_language,
                    "detected_intent": conv.detected_intent,
                    "expected_intent": conv.expected_intent,
                    "evaluation_score": conv.evaluation_score,
                    "latency_ms": conv.latency_ms,
                } if conv else None,
                "reviewer": {
                    "id": reviewer.id,
                    "name": reviewer.name,
                    "languages": reviewer.languages,
                } if reviewer else None,
                "ratings": {
                    "id": ratings.id,
                    "review_id": ratings.review_id,
                    "pronunciation": ratings.pronunciation,
                    "language_accuracy": ratings.language_accuracy,
                    "intent_accuracy": ratings.intent_accuracy,
                    "naturalness": ratings.naturalness,
                    "conversation_quality": ratings.conversation_quality,
                    "overall_rating": ratings.overall_rating,
                } if ratings else None,
                "approval": {
                    "id": approval.id,
                    "review_id": approval.review_id,
                    "status": approval.status,
                    "reviewer_notes": approval.reviewer_notes,
                    "approved_by": approval.approved_by,
                } if approval else None,
            })

        return result