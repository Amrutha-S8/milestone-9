"""
Analytics engine for StayZa Native Review System.
Generates per-language ratings, reviewer stats, and approval rates.
"""

from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from review_system.models import Approval, Conversation, Rating, Review, Reviewer


class AnalyticsEngine:

    def __init__(self, db: Session):
        self.db = db

    def generate_analytics(self) -> dict[str, Any]:
        total_reviews = self.db.query(Review).count()
        avg_rating = self._average_overall_rating()
        language_breakdown = self._language_breakdown()
        reviewer_stats = self._reviewer_statistics()
        approval_stats = self._approval_statistics()
        rating_dist = self._rating_distribution()

        total_approvals = sum(
            approval_stats[status] for status in ("approved", "rejected", "needs_improvement", "pending")
        )
        approval_rate = (
            round((approval_stats["approved"] / total_approvals) * 100, 2)
            if total_approvals > 0
            else 0.0
        )
        rejection_rate = (
            round((approval_stats["rejected"] / total_approvals) * 100, 2)
            if total_approvals > 0
            else 0.0
        )
        needs_improvement_rate = (
            round((approval_stats["needs_improvement"] / total_approvals) * 100, 2)
            if total_approvals > 0
            else 0.0
        )
        pending_rate = (
            round((approval_stats["pending"] / total_approvals) * 100, 2)
            if total_approvals > 0
            else 0.0
        )

        return {
            "average_rating": avg_rating,
            "total_reviews": total_reviews,
            "language_breakdown": language_breakdown,
            "reviewer_statistics": reviewer_stats,
            "approval_rate": approval_rate,
            "rejection_rate": rejection_rate,
            "needs_improvement_rate": needs_improvement_rate,
            "pending_rate": pending_rate,
            "rating_distribution": rating_dist,
        }

    def _average_overall_rating(self) -> float:
        result = self.db.query(func.avg(Rating.overall_rating)).scalar()
        return round(result, 2) if result else 0.0

    def _language_breakdown(self) -> dict[str, Any]:
        languages = self.db.query(
            Conversation.language,
            func.count(Review.id).label("review_count"),
            func.avg(Rating.overall_rating).label("avg_rating"),
            func.avg(Rating.pronunciation).label("avg_pronunciation"),
            func.avg(Rating.language_accuracy).label("avg_language_accuracy"),
            func.avg(Rating.intent_accuracy).label("avg_intent_accuracy"),
            func.avg(Rating.naturalness).label("avg_naturalness"),
            func.avg(Rating.conversation_quality).label("avg_conversation_quality"),
        ).select_from(Review).join(
            Conversation, Review.conversation_id == Conversation.id
        ).outerjoin(
            Rating, Rating.review_id == Review.id
        ).group_by(Conversation.language).all()

        breakdown = {}
        for lang in languages:
            breakdown[lang.language] = {
                "review_count": lang.review_count,
                "average_rating": round(lang.avg_rating, 2) if lang.avg_rating else 0.0,
                "average_pronunciation": round(lang.avg_pronunciation, 2) if lang.avg_pronunciation else 0.0,
                "average_language_accuracy": round(lang.avg_language_accuracy, 2) if lang.avg_language_accuracy else 0.0,
                "average_intent_accuracy": round(lang.avg_intent_accuracy, 2) if lang.avg_intent_accuracy else 0.0,
                "average_naturalness": round(lang.avg_naturalness, 2) if lang.avg_naturalness else 0.0,
                "average_conversation_quality": round(lang.avg_conversation_quality, 2) if lang.avg_conversation_quality else 0.0,
            }
        return breakdown

    def _reviewer_statistics(self) -> dict[str, Any]:
        stats = self.db.query(
            Reviewer.id,
            Reviewer.name,
            func.count(Review.id).label("review_count"),
            func.avg(Rating.overall_rating).label("avg_rating"),
        ).select_from(Reviewer).outerjoin(
            Review, Review.reviewer_id == Reviewer.id
        ).outerjoin(
            Rating, Rating.review_id == Review.id
        ).group_by(Reviewer.id).all()

        return {
            "total_reviewers": len(stats),
            "per_reviewer": [
                {
                    "id": s.id,
                    "name": s.name,
                    "review_count": s.review_count,
                    "average_rating": round(s.avg_rating, 2) if s.avg_rating else 0.0,
                }
                for s in stats
            ],
        }

    def _approval_statistics(self) -> dict[str, int]:
        counts = self.db.query(
            Approval.status,
            func.count(Approval.id).label("count"),
        ).group_by(Approval.status).all()

        result = {"approved": 0, "rejected": 0, "needs_improvement": 0, "pending": 0}
        for row in counts:
            key = row.status.lower().replace(" ", "_")
            result[key] = row.count
        return result

    def _rating_distribution(self) -> dict[str, float]:
        ratings = self.db.query(Rating.overall_rating).all()
        if not ratings:
            return {"0-2": 0.0, "2-4": 0.0, "4-6": 0.0, "6-8": 0.0, "8-10": 0.0}

        buckets = {"0-2": 0, "2-4": 0, "4-6": 0, "6-8": 0, "8-10": 0}
        for (r,) in ratings:
            if r < 2:
                buckets["0-2"] += 1
            elif r < 4:
                buckets["2-4"] += 1
            elif r < 6:
                buckets["4-6"] += 1
            elif r < 8:
                buckets["6-8"] += 1
            else:
                buckets["8-10"] += 1

        total = len(ratings)
        return {k: round((v / total) * 100, 2) for k, v in buckets.items()}
