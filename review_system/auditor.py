"""
Native Review System for StayZa Milestone 9.

Design Rationale:
- Quality Assurance & Monitoring: Logs low-confidence (<0.70) utterances, fallback responses,
  and failed intent classifications.
- Provides native review endpoints and memory buffer for human reviewer annotation.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import threading


class ReviewAuditor:
    """
    In-memory and file-backed auditor for flagging voice utterances requiring manual review.
    """

    def __init__(self, confidence_threshold: float = 0.70):
        self.confidence_threshold = confidence_threshold
        self._review_queue: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def inspect_and_log(
        self,
        text: str,
        language: str,
        intent: str,
        confidence: float,
        next_action: str,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Evaluates analysis result and logs to review queue if confidence is below threshold or intent is unknown.
        
        Returns:
            True if flagged for review, False otherwise.
        """
        needs_review = confidence < self.confidence_threshold or intent == "unknown"

        if needs_review:
            entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "session_id": session_id,
                "text": text,
                "language": language,
                "intent": intent,
                "confidence": confidence,
                "next_action": next_action,
                "reason": "low_confidence" if confidence < self.confidence_threshold else "unknown_intent",
                "reviewed": False,
                "reviewer_notes": None
            }
            with self._lock:
                self._review_queue.append(entry)

        return needs_review

    def get_flagged_utterances(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns flagged entries requiring reviewer attention."""
        with self._lock:
            return list(self._review_queue[-limit:])

    def clear_queue(self) -> None:
        """Clears the review queue."""
        with self._lock:
            self._review_queue.clear()


# Global auditor instance
review_auditor = ReviewAuditor(confidence_threshold=0.70)
