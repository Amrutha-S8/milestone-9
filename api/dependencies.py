"""
FastAPI dependency injection module for StayZa Milestone 9.

Exposes singleton services for LanguageRegistry, LanguageDetector, IntentClassifier,
EntityExtractor, SessionManager, EvaluationEngine, and Review System.
"""

from detection.detector import LanguageDetector, language_detector
from entities.extractor import EntityExtractor, entity_extractor
from evaluation.config import EvaluationConfig
from evaluation.engine import EvaluationEngine
from intent.classifier import IntentClassifier, intent_classifier
from languages.english.flow import EnglishLanguageFlow
from languages.hindi.flow import HindiLanguageFlow
from languages.hinglish.flow import HinglishLanguageFlow
from languages.malayalam.flow import MalayalamLanguageFlow
from languages.marathi.flow import MarathiLanguageFlow
from languages.registry import LanguageRegistry, language_registry
from languages.telugu.flow import TeluguLanguageFlow
from normalization.service import TextNormalizationService, normalization_service
from pronunciation.dictionary import PronunciationDictionary, pronunciation_dict
from review_system.auditor import ReviewAuditor, review_auditor
from review_system.database import init_db
from session.manager import SessionManager, session_manager

# Register all language flows into registry
language_registry.register(EnglishLanguageFlow())
language_registry.register(HindiLanguageFlow())
language_registry.register(HinglishLanguageFlow())
language_registry.register(TeluguLanguageFlow())
language_registry.register(MarathiLanguageFlow())
language_registry.register(MalayalamLanguageFlow())

# Evaluation Engine singleton
evaluation_config = EvaluationConfig()
evaluation_engine = EvaluationEngine(
    registry=language_registry, config=evaluation_config
)

# Initialize review database on import
init_db()


def get_language_registry() -> LanguageRegistry:
    return language_registry


def get_language_detector() -> LanguageDetector:
    return language_detector


def get_intent_classifier() -> IntentClassifier:
    return intent_classifier


def get_entity_extractor() -> EntityExtractor:
    return entity_extractor


def get_session_manager() -> SessionManager:
    return session_manager


def get_pronunciation_dict() -> PronunciationDictionary:
    return pronunciation_dict


def get_review_auditor() -> ReviewAuditor:
    return review_auditor


def get_normalization_service() -> TextNormalizationService:
    return normalization_service


def get_evaluation_engine() -> EvaluationEngine:
    return evaluation_engine
