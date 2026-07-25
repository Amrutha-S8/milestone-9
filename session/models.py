"""
Conversation State Data Models.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TurnHistoryItem(BaseModel):
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    user_text: str
    detected_language: str
    intent: str
    next_action: str
    entities: Dict[str, Any] = Field(default_factory=dict)


class SessionState(BaseModel):
    """
    Session memory representation for multi-turn conversation tracking.
    """
    session_id: str
    active_language: str = "English"
    active_flow: Optional[str] = None
    current_intent: Optional[str] = None
    last_action: Optional[str] = None
    slot_memory: Dict[str, Any] = Field(default_factory=dict)
    history: List[TurnHistoryItem] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
