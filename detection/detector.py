"""
Reusable Language Detection Service for StayZa.
"""

from typing import Any

from detection.rules import (
    HINDI_SPECIFIC_KEYWORDS,
    HINGLISH_MARKER_WORDS,
    MARATHI_DISTINCTIVE_CHARS,
    MARATHI_SPECIFIC_KEYWORDS,
    UNICODE_SCRIPT_RANGES,
)


class LanguageDetector:
    """
    Automatic Language Detection Service for StayZa voice platform.
    """

    def detect(self, text: str) -> dict[str, Any]:
        clean_text = text.strip()
        if not clean_text:
            return {"language": "English", "confidence": 0.0}

        telugu_count = 0
        devanagari_count = 0
        malayalam_count = 0
        total_chars = len(clean_text)

        for char in clean_text:
            cp = ord(char)
            if UNICODE_SCRIPT_RANGES["Telugu"][0] <= cp <= UNICODE_SCRIPT_RANGES["Telugu"][1]:
                telugu_count += 1
            elif UNICODE_SCRIPT_RANGES["Devanagari"][0] <= cp <= UNICODE_SCRIPT_RANGES["Devanagari"][1]:
                devanagari_count += 1
            elif UNICODE_SCRIPT_RANGES["Malayalam"][0] <= cp <= UNICODE_SCRIPT_RANGES["Malayalam"][1]:
                malayalam_count += 1

        # 1. Native Script Matches
        if telugu_count / total_chars > 0.3:
            conf = min(0.98, round(0.85 + (telugu_count / total_chars) * 0.13, 2))
            return {"language": "Telugu", "confidence": conf}

        if malayalam_count / total_chars > 0.3:
            conf = min(0.98, round(0.85 + (malayalam_count / total_chars) * 0.13, 2))
            return {"language": "Malayalam", "confidence": conf}

        if devanagari_count / total_chars > 0.3:
            is_marathi = any(c in clean_text for c in MARATHI_DISTINCTIVE_CHARS)
            if not is_marathi:
                m_hits = sum(1 for m_kw in MARATHI_SPECIFIC_KEYWORDS if m_kw in clean_text)
                h_hits = sum(1 for h_kw in HINDI_SPECIFIC_KEYWORDS if h_kw in clean_text)
                if m_hits > h_hits:
                    is_marathi = True

            lang = "Marathi" if is_marathi else "Hindi"
            conf = min(0.98, round(0.85 + (devanagari_count / total_chars) * 0.13, 2))
            return {"language": lang, "confidence": conf}

        # 2. Roman Script (English vs Hinglish)
        words = [w.lower().strip(".,!?") for w in clean_text.split()]
        hinglish_hits = sum(1 for w in words if w in HINGLISH_MARKER_WORDS)

        if len(words) > 0 and (hinglish_hits / len(words) >= 0.15 or hinglish_hits >= 1):
            conf = min(0.96, round(0.70 + (hinglish_hits / max(1, len(words))) * 0.30, 2))
            return {"language": "Hinglish", "confidence": conf}

        return {"language": "English", "confidence": 0.95}


language_detector = LanguageDetector()
