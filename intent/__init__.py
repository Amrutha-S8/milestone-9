"""
Intent Package Initialization.
"""
from intent.classifier import intent_classifier, IntentClassifier
from intent.base import BaseIntentClassifier

__all__ = ["intent_classifier", "IntentClassifier", "BaseIntentClassifier"]
