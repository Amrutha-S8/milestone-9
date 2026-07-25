"""
Conversation Session Manager for StayZa.

Design Rationale:
- Thread-safe in-memory session manager (Redis adapter ready).
- Maintains session memory across multi-turn dialogs.
- Accumulates extracted entities so that if user says "I want to book a room" (Turn 1)
  and then "Tomorrow" (Turn 2), the active flow remains 'booking' and check_in='tomorrow' is filled.
"""

from typing import Dict, Any, Optional
import uuid
import threading
from datetime import datetime, timezone
from session.models import SessionState, TurnHistoryItem


class SessionManager:
    """
    Manages multi-turn conversation states and slot memories.
    """

    def __init__(self):
        self._sessions: Dict[str, SessionState] = {}
        self._lock = threading.Lock()

    def get_or_create_session(self, session_id: Optional[str] = None) -> SessionState:
        """Retrieves existing session state or initializes a new session."""
        with self._lock:
            if not session_id or session_id not in self._sessions:
                new_id = session_id or f"sess_{uuid.uuid4().hex[:8]}"
                state = SessionState(session_id=new_id)
                self._sessions[new_id] = state
                return state

            return self._sessions[session_id]

    def update_session_turn(
        self,
        session_id: str,
        user_text: str,
        detected_language: str,
        intent: str,
        next_action: str,
        new_entities: Dict[str, Any]
    ) -> SessionState:
        """
        Updates session state with new turn information, accumulating slots.
        """
        with self._lock:
            state = self._sessions.get(session_id)
            if not state:
                state = SessionState(session_id=session_id)
                self._sessions[session_id] = state

            # Update language
            state.active_language = detected_language

            # Maintain active flow unless explicit new flow or goodbye
            if intent not in ["unknown", "greeting", "goodbye"]:
                state.active_flow = intent
                state.current_intent = intent
            elif intent == "goodbye":
                state.active_flow = None
                state.current_intent = "goodbye"

            # Contextual flow continuation: if current turn is a slot response (e.g. "tomorrow")
            if intent == "unknown" and state.active_flow:
                intent = state.active_flow

            # Merge entities into slot memory
            for k, v in new_entities.items():
                if v is not None:
                    state.slot_memory[k] = v

            state.last_action = next_action
            state.updated_at = datetime.now(timezone.utc).isoformat()

            # Record turn history
            state.history.append(
                TurnHistoryItem(
                    user_text=user_text,
                    detected_language=detected_language,
                    intent=intent,
                    next_action=next_action,
                    entities=new_entities
                )
            )

            return state

    def clear_session(self, session_id: str) -> None:
        """Clears a session."""
        with self._lock:
            self._sessions.pop(session_id, None)


# Global singleton instance
session_manager = SessionManager()
