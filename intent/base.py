"""
Abstract Base Intent Classifier Interface for StayZa.

Design Rationale:
- Strategy / Open-Closed Principle: Provides standard classification interface.
- ML / LLM Pluggability: Rule or pattern classifiers can be seamlessly replaced with
  fine-tuned Transformers (BERT/RoBERTa) or LLM embeddings without modifying application API or flows.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Dict, Any, Optional


class BaseIntentClassifier(ABC):
    """
    Abstract contract for intent classification engines.
    """

    @abstractmethod
    def classify(self, text: str, language: Optional[str] = None) -> Tuple[str, float]:
        """
        Classifies input text into one of the supported intents.
        
        Returns:
            Tuple[intent_name, confidence_score]
        """
        pass
