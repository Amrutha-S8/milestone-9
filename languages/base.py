"""
Abstract Base Language Flow Interface for StayZa.

Design Rationale:
- Clean Architecture / Strategy Pattern: Every language module (English, Hindi, Telugu, Marathi, Malayalam)
  implements this standard interface.
- Decouples API endpoints from language-specific NLP/state algorithms.
- Enables seamless plug-and-play addition of new languages without modifying route logic.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class FlowResult:
    """
    Standard outcome returned by any language flow processing an utterance.
    """
    language: str
    intent: str
    confidence: float
    next_action: str
    slots: Dict[str, Any] = field(default_factory=dict)
    raw_text: str = ""


class BaseLanguageFlow(ABC):
    """
    Abstract contract for all language flow implementations in StayZa.
    """

    @property
    @abstractmethod
    def language_name(self) -> str:
        """Returns the canonical language name (e.g. 'English', 'Hindi')."""
        pass

    @property
    @abstractmethod
    def language_code(self) -> str:
        """Returns the ISO 639-1 language code (e.g. 'en', 'hi')."""
        pass

    @abstractmethod
    def detect_confidence(self, text: str) -> float:
        """
        Calculates how confident this module is that the text is in its language (0.0 - 1.0).
        Used by LanguageRegistry to auto-detect language when not explicitly provided.
        """
        pass

    @abstractmethod
    def analyze_intent(self, text: str) -> Tuple[str, float, Dict[str, Any]]:
        """
        Classifies intent and extracts relevant slots from utterance text.
        
        Returns:
            Tuple[intent_name, confidence_score, extracted_slots_dict]
        """
        pass

    @abstractmethod
    def determine_next_action(self, intent: str, current_state: Optional[str] = None, slots: Optional[Dict[str, Any]] = None) -> str:
        """
        Determines the state transition / next dialog action based on intent and optional state.
        """
        pass

    def process(self, text: str, current_state: Optional[str] = None) -> FlowResult:
        """
        Full pipeline wrapper for language analysis.
        """
        intent, confidence, slots = self.analyze_intent(text)
        next_action = self.determine_next_action(intent, current_state, slots)
        
        return FlowResult(
            language=self.language_name,
            intent=intent,
            confidence=round(confidence, 2),
            next_action=next_action,
            slots=slots,
            raw_text=text
        )
