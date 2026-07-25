"""
Conversation State Data Models.
"""

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class TurnHistoryItem(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    user_text: str
    detected_language: str
    intent: str
    next_action: str
    entities: dict[str, Any] = Field(default_factory=dict)


class SessionState(BaseModel):
    """
    Session memory representation for multi-turn conversation tracking.
    """
    session_id: str
    active_language: str = "English"
    active_flow: str | None = None
    current_intent: str | None = None
    last_action: str | None = None
    slot_memory: dict[str, Any] = Field(default_factory=dict)
    history: list[TurnHistoryItem] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
