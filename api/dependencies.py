"""
FastAPI dependency injection module for StayZa Milestone 9.
Exposes singleton services for LanguageRegistry, LanguageDetector, IntentClassifier,
EntityExtractor, SessionManager, EvaluationEngine, and Review System.
"""

from languages.registry import language_registry, LanguageRegistry
from languages.english.flow import EnglishLanguageFlow
from languages.hindi.flow import HindiLanguageFlow
from languages.hinglish.flow import HinglishLanguageFlow
from languages.telugu.flow import TeluguLanguageFlow
from languages.marathi.flow import MarathiLanguageFlow
from languages.malayalam.flow import MalayalamLanguageFlow

from detection.detector import language_detector, LanguageDetector
from intent.classifier import intent_classifier, IntentClassifier
from entities.extractor import entity_extractor, EntityExtractor
from session.manager import session_manager, SessionManager
from pronunciation.dictionary import pronunciation_dict, PronunciationDictionary
from normalization.service import normalization_service, TextNormalizationService
from review_system.auditor import review_auditor, ReviewAuditor
from review_system.database import init_db
from evaluation.engine import EvaluationEngine
from evaluation.config import EvaluationConfig

# Register all language flows into registry
language_registry.register(EnglishLanguageFlow())
language_registry.register(HindiLanguageFlow())
language_registry.register(HinglishLanguageFlow())
language_registry.register(TeluguLanguageFlow())
language_registry.register(MarathiLanguageFlow())
language_registry.register(MalayalamLanguageFlow())

# Evaluation Engine singleton
evaluation_config = EvaluationConfig()
evaluation_engine = EvaluationEngine(registry=language_registry, config=evaluation_config)

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