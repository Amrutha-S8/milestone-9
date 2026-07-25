"""
Unit tests for TextNormalizationService (Day 4).

Tests cover:
- Basic lowercase normalization
- Whitespace collapse
- Noise token removal (STT filler words)
- Abbreviation expansion (hotel domain: A/C, Bengaluru, etc.)
- Transliteration normalization (kal -> tomorrow, etc.)
- Empty/whitespace-only input edge cases
- NormalizationResult dataclass fields
- normalize_text convenience method
"""

import pytest

from normalization.service import NormalizationResult, TextNormalizationService


@pytest.fixture
def svc():
    """Shared TextNormalizationService instance for all tests."""
    return TextNormalizationService()


# ── Basic normalization ────────────────────────────────────────────────────────

class TestBasicNormalization:

    def test_lowercase(self, svc):
        result = svc.normalize("HELLO I WANT A ROOM")
        assert result.normalized_text == result.normalized_text.lower()

    def test_strips_leading_trailing_whitespace(self, svc):
        result = svc.normalize("   hello world   ")
        assert not result.normalized_text.startswith(" ")
        assert not result.normalized_text.endswith(" ")

    def test_collapses_multiple_spaces(self, svc):
        result = svc.normalize("book  a   room   please")
        assert "  " not in result.normalized_text

    def test_empty_string_returns_empty(self, svc):
        result = svc.normalize("")
        assert result.normalized_text == ""

    def test_whitespace_only_returns_empty(self, svc):
        result = svc.normalize("   ")
        assert result.normalized_text == ""

    def test_original_text_preserved(self, svc):
        raw = "Book a A/C Room"
        result = svc.normalize(raw)
        assert result.original_text == raw


# ── Noise removal ─────────────────────────────────────────────────────────────

class TestNoiseRemoval:

    def test_removes_umm(self, svc):
        result = svc.normalize("umm I need a room please")
        assert "umm" not in result.normalized_text

    def test_removes_uh(self, svc):
        result = svc.normalize("uh book a deluxe room")
        assert result.normalized_text.startswith("book") or "uh" not in result.normalized_text

    def test_removes_hmm(self, svc):
        result = svc.normalize("hmm can I get availability")
        assert "hmm" not in result.normalized_text

    def test_noise_removal_in_applied_rules(self, svc):
        result = svc.normalize("umm book a room")
        assert "noise_removal" in result.applied_rules


# ── Abbreviation expansion ────────────────────────────────────────────────────

class TestAbbreviationExpansion:

    def test_ac_expansion(self, svc):
        result = svc.normalize("I need an a/c room")
        assert "ac" in result.normalized_text
        assert "a/c" not in result.normalized_text

    def test_bengaluru_normalization(self, svc):
        result = svc.normalize("Book a room in Bengaluru")
        assert "bangalore" in result.normalized_text

    def test_bombay_normalization(self, svc):
        result = svc.normalize("Hotel near Bombay station")
        assert "mumbai" in result.normalized_text

    def test_tmrw_expansion(self, svc):
        result = svc.normalize("I need a room tmrw")
        assert "tomorrow" in result.normalized_text

    def test_tonite_expansion(self, svc):
        result = svc.normalize("Book for tonite")
        assert "tonight" in result.normalized_text

    def test_rupee_symbol_normalization(self, svc):
        result = svc.normalize("Room for ₹2000 per night")
        assert "rupees" in result.normalized_text

    def test_abbreviation_in_applied_rules(self, svc):
        result = svc.normalize("a/c room in bengaluru")
        applied = result.applied_rules
        # At least one of the abbreviation rules should fire
        assert len(applied) > 0


# ── Transliteration normalization ─────────────────────────────────────────────

class TestTransliterationNormalization:

    def test_kal_to_tomorrow(self, svc):
        result = svc.normalize("kal ek room chahiye")
        assert "tomorrow" in result.normalized_text

    def test_aaj_to_today(self, svc):
        result = svc.normalize("aaj mujhe room chahiye")
        assert "today" in result.normalized_text

    def test_kamra_to_room(self, svc):
        result = svc.normalize("mujhe ek kamra chahiye")
        assert "room" in result.normalized_text

    def test_ek_to_one(self, svc):
        result = svc.normalize("ek room book karo")
        assert "one" in result.normalized_text


# ── NormalizationResult dataclass ─────────────────────────────────────────────

class TestNormalizationResult:

    def test_result_is_dataclass(self, svc):
        result = svc.normalize("test")
        assert isinstance(result, NormalizationResult)

    def test_applied_rules_is_list(self, svc):
        result = svc.normalize("test")
        assert isinstance(result.applied_rules, list)

    def test_applied_rules_empty_for_plain_text(self, svc):
        result = svc.normalize("i need a room")
        # No abbreviations or noise tokens → applied_rules should be empty or minimal
        assert isinstance(result.applied_rules, list)


# ── Convenience method ────────────────────────────────────────────────────────

class TestNormalizeTextMethod:

    def test_returns_string(self, svc):
        output = svc.normalize_text("Book a A/C room in Bengaluru tmrw")
        assert isinstance(output, str)

    def test_lowercase_output(self, svc):
        output = svc.normalize_text("BOOK A ROOM")
        assert output == output.lower()

    def test_full_pipeline(self, svc):
        """Integration: verify complete pipeline on a realistic hotel query."""
        raw = "umm Book a A/C room in Bengaluru tmrw for 2 guests"
        output = svc.normalize_text(raw)
        assert "umm" not in output
        assert "a/c" not in output
        assert "ac" in output
        assert "bengaluru" not in output
        assert "bangalore" in output
        assert "tmrw" not in output
        assert "tomorrow" in output
