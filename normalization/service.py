"""
Text Normalization Service for StayZa Milestone 9.

Design Rationale:
- This service runs as the FIRST step in the NLU pipeline, before language
  detection, intent classification, and entity extraction.
- It handles three categories of preprocessing:
    1. Basic normalization  — lowercase, strip whitespace, collapse spaces.
    2. Noise removal        — strip STT filler words (umm, uh, etc.).
    3. Domain substitution  — apply abbreviation and transliteration mappings.
- All rules live in normalization/rules.py so adding new substitutions
  never requires modifying this service class.
- The service is stateless and thread-safe (no shared mutable state).

Usage:
    from normalization.service import normalization_service
    result = normalization_service.normalize("Book a A/C room in Bengaluru tmrw")
    # result.normalized_text -> "book a ac room in bangalore tomorrow"
"""

import re
from dataclasses import dataclass, field

from normalization.rules import ABBREVIATION_MAP, NOISE_TOKENS, TRANSLITERATION_MAP


@dataclass
class NormalizationResult:
    """
    Holds the output of a normalization pipeline pass.

    Fields:
        original_text:    The raw input text, unchanged.
        normalized_text:  The fully normalized, NLU-ready text.
        applied_rules:    List of substitution keys that were triggered,
                          useful for debugging and audit logs.
    """
    original_text: str
    normalized_text: str
    applied_rules: list[str] = field(default_factory=list)


class TextNormalizationService:
    """
    Preprocessing pipeline that normalizes raw STT/user text
    before the NLU stack (language detection, intent, entities) runs.

    Steps (in order):
        1. Lowercase + strip leading/trailing whitespace.
        2. Remove STT noise tokens (filler words, ellipses).
        3. Apply domain abbreviation expansions (longest match first).
        4. Apply transliteration normalizations (romanized Indian words).
        5. Collapse multiple spaces into one.
    """

    def __init__(self) -> None:
        # Pre-sort abbreviation keys by length descending so longer phrases
        # are matched before substrings (e.g. "non a/c" before "a/c").
        self._abbr_pairs = sorted(
            ABBREVIATION_MAP.items(),
            key=lambda kv: len(kv[0]),
            reverse=True
        )
        self._trans_pairs = sorted(
            TRANSLITERATION_MAP.items(),
            key=lambda kv: len(kv[0]),
            reverse=True
        )
        # Compile noise removal regex once for performance
        noise_pattern = "|".join(
            re.escape(token) for token in sorted(NOISE_TOKENS, key=len, reverse=True)
        )
        self._noise_re = re.compile(rf"\b({noise_pattern})\b", re.IGNORECASE)

    # ──────────────────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────────────────

    def normalize(self, text: str) -> NormalizationResult:
        """
        Runs the full normalization pipeline on input text.

        Args:
            text: Raw utterance from STT or user input.

        Returns:
            NormalizationResult with normalized text and audit trail.

        Example:
            normalize("Book a A/C room in Bengaluru tmrw for 2 guests")
            -> "book a ac room in bangalore tomorrow for 2 guests"
        """
        if not text or not text.strip():
            return NormalizationResult(original_text=text, normalized_text="")

        applied_rules: list[str] = []
        working = text.strip()

        # Step 1: Lowercase
        working = working.lower()

        # Step 2: Remove STT noise tokens
        working = self._remove_noise(working, applied_rules)

        # Step 3: Abbreviation expansions (hotel domain)
        working = self._apply_map(working, self._abbr_pairs, applied_rules)

        # Step 4: Transliteration normalizations (Hinglish/regional)
        working = self._apply_map(working, self._trans_pairs, applied_rules)

        # Step 5: Collapse whitespace
        working = re.sub(r"\s{2,}", " ", working).strip()

        return NormalizationResult(
            original_text=text,
            normalized_text=working,
            applied_rules=applied_rules
        )

    def normalize_text(self, text: str) -> str:
        """
        Convenience method — returns normalized string directly.
        Use this in the API pipeline for minimal overhead.
        """
        return self.normalize(text).normalized_text

    # ──────────────────────────────────────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _remove_noise(self, text: str, applied: list[str]) -> str:
        """Removes STT filler tokens using pre-compiled regex."""
        result = self._noise_re.sub("", text)
        if result != text:
            applied.append("noise_removal")
        return result

    def _apply_map(
        self,
        text: str,
        pairs: list,
        applied: list[str]
    ) -> str:
        """
        Applies substitution pairs to text.
        Pairs are pre-sorted longest-first to prevent partial matches.
        """
        for raw, normalized in pairs:
            # Use word-boundary matching where possible, but for multi-word
            # phrases use simple substring match after lowercasing.
            if raw in text:
                text = text.replace(raw, normalized)
                applied.append(raw)
        return text


# ── Global singleton (shared across the app) ─────────────────────────────────
normalization_service = TextNormalizationService()
