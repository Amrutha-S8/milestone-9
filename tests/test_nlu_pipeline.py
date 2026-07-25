"""
Integration tests for the full NLU pipeline (Day 4).

Tests cover the end-to-end flow:
    Normalization -> Language Detection -> Intent Classification -> Entity Extraction

These tests use real service instances (no mocks) to validate the pipeline
behaves correctly as a system, not just as isolated units.
"""

import pytest
from normalization.service import TextNormalizationService
from detection.detector import LanguageDetector
from intent.classifier import IntentClassifier
from entities.extractor import EntityExtractor


@pytest.fixture(scope="module")
def normalizer():
    return TextNormalizationService()


@pytest.fixture(scope="module")
def detector():
    return LanguageDetector()


@pytest.fixture(scope="module")
def classifier():
    return IntentClassifier()


@pytest.fixture(scope="module")
def extractor():
    return EntityExtractor()


def run_pipeline(normalizer, detector, classifier, extractor, raw_text):
    """
    Executes the full NLU pipeline on raw_text, mirroring what the API does.
    Returns a dict with all intermediate and final results.
    """
    norm = normalizer.normalize(raw_text)
    normalized = norm.normalized_text

    lang_result = detector.detect(normalized)
    intent, confidence = classifier.classify(normalized, language=lang_result["language"])
    entities = extractor.extract(normalized)

    return {
        "original": raw_text,
        "normalized": normalized,
        "language": lang_result["language"],
        "lang_confidence": lang_result["confidence"],
        "intent": intent,
        "intent_confidence": confidence,
        "entities": entities,
    }


# ── English pipeline tests ─────────────────────────────────────────────────────

class TestEnglishPipeline:

    def test_booking_with_abbreviations(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "Book a A/C deluxe room in Bengaluru tmrw for 2 guests"
        )
        assert result["language"] == "English"
        assert result["intent"] == "booking"
        assert "guests" in result["entities"]
        assert result["entities"]["guests"] == 2
        assert "bangalore" in result["normalized"]   # abbreviation was expanded
        assert "tomorrow" in result["normalized"]    # tmrw was expanded

    def test_price_enquiry(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "How much does a deluxe room cost?"
        )
        assert result["intent"] == "price_enquiry"
        assert result["entities"].get("room_type") == "Deluxe"

    def test_cancellation(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "I want to cancel my booking BK-4521"
        )
        assert result["intent"] == "cancellation"
        assert result["entities"].get("booking_id") == "BK-4521"

    def test_greeting(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "Hello, I'd like to contact StayZa"
        )
        assert result["intent"] == "greeting"

    def test_goodbye(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "Thank you, bye"
        )
        assert result["intent"] == "goodbye"

    def test_noise_removal_does_not_break_intent(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "umm uh I need to book a room"
        )
        assert result["intent"] == "booking"

    def test_suite_entity_extraction(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "I want to book a suite room for 3 adults"
        )
        assert result["entities"].get("room_type") is not None
        assert result["entities"].get("guests") == 3


# ── Hindi pipeline tests ───────────────────────────────────────────────────────

class TestHindiPipeline:

    def test_booking_hindi(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "मुझे एक कमरा बुक करना है"
        )
        assert result["intent"] == "booking"

    def test_greeting_hindi(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "नमस्ते"
        )
        assert result["intent"] == "greeting"

    def test_cancellation_hindi(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "मुझे बुकिंग रद्द करनी है"
        )
        assert result["intent"] == "cancellation"


# ── Telugu pipeline tests ──────────────────────────────────────────────────────

class TestTeluguPipeline:

    def test_booking_telugu(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "మాకు ఒక గది కావాలి"
        )
        assert result["intent"] == "booking"

    def test_detection_telugu(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "నమస్కారం, మీ హోటల్‌లో రూమ్ బుక్ చేయాలి"
        )
        assert result["language"] == "Telugu"


# ── Marathi pipeline tests ─────────────────────────────────────────────────────

class TestMarathiPipeline:

    def test_booking_marathi(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "मला एक खोली बुक करायची आहे"
        )
        assert result["intent"] == "booking"

    def test_detection_marathi(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "नमस्कार, मला स्टेझा हॉटेलशी बोलायचे आहे"
        )
        assert result["language"] == "Marathi"


# ── Malayalam pipeline tests ───────────────────────────────────────────────────

class TestMalayalamPipeline:

    def test_booking_malayalam(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "എനിക്ക് ഒരു മുറി ബുക്ക് ചെയ്യണം"
        )
        assert result["intent"] == "booking"

    def test_detection_malayalam(self, normalizer, detector, classifier, extractor):
        result = run_pipeline(
            normalizer, detector, classifier, extractor,
            "നമസ്കാരം, സ്റ്റേഴ്സ ഹോട്ടലിൽ നിന്ന് സംസാരിക്കുന്നു"
        )
        assert result["language"] == "Malayalam"


# ── Entity extraction tests ────────────────────────────────────────────────────

class TestEntityExtraction:

    def test_extracts_room_type_deluxe(self, normalizer, detector, classifier, extractor):
        entities = extractor.extract("book a deluxe room")
        assert entities.get("room_type") == "Deluxe"

    def test_extracts_guests_digit(self, normalizer, detector, classifier, extractor):
        entities = extractor.extract("room for 3 adults")
        assert entities.get("guests") == 3

    def test_extracts_guests_word(self, normalizer, detector, classifier, extractor):
        entities = extractor.extract("room for two people")
        assert entities.get("guests") == 2

    def test_extracts_checkin_tomorrow(self, normalizer, detector, classifier, extractor):
        entities = extractor.extract("check in tomorrow")
        assert entities.get("check_in") == "tomorrow"

    def test_extracts_booking_id(self, normalizer, detector, classifier, extractor):
        entities = extractor.extract("cancel booking BK-4521")
        assert entities.get("booking_id") == "BK-4521"

    def test_extracts_budget(self, normalizer, detector, classifier, extractor):
        entities = extractor.extract("room under 3000 rupees")
        assert "budget" in entities

    def test_no_entities_unknown_text(self, normalizer, detector, classifier, extractor):
        entities = extractor.extract("hello")
        assert isinstance(entities, dict)


# ── Intent confidence tests ────────────────────────────────────────────────────

class TestIntentConfidence:

    def test_confidence_between_0_and_1(self, classifier):
        _, conf = classifier.classify("book a room")
        assert 0.0 <= conf <= 1.0

    def test_unknown_returns_low_confidence(self, classifier):
        _, conf = classifier.classify("xyzzy foobar qwerty")
        assert conf < 0.5

    def test_booking_high_confidence(self, classifier):
        _, conf = classifier.classify("I need to book a deluxe room")
        assert conf >= 0.7

    def test_empty_text_returns_unknown(self, classifier):
        intent, conf = classifier.classify("")
        assert intent == "unknown"
        assert conf == 0.0
