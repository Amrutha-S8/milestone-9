"""
Pronunciation Dictionary Engine for StayZa Milestone 9.

Design Rationale:
- Prepares phonetic transcriptions and ARPAbet/IPA pronunciations.
- Essential for Milestone 8 Text-to-Speech (TTS) clarity, especially for brand names like 'StayZa'
  and domain terms like 'Concierge' or Indian language proper nouns.
- Supports language-specific lookups for multilingual TTS.
"""

import json
from pathlib import Path
from typing import Any


class PronunciationDictionary:
    """
    Manager for hotel domain pronunciation lexicons.
    Supports language-specific phonetic lookups across 6 Indian languages.
    """

    def __init__(self, lexicon_path: str | None = None):
        if lexicon_path is None:
            lexicon_path = str(Path(__file__).parent / "lexicon.json")
        
        self.lexicon_path = lexicon_path
        self._lexicon: dict[str, dict[str, Any]] = {}
        self.load_lexicon()

    def load_lexicon(self) -> None:
        """Loads pronunciation lexicon from JSON file."""
        if Path(self.lexicon_path).exists():
            with Path(self.lexicon_path).open(encoding="utf-8") as f:
                self._lexicon = json.load(f)

    def lookup(self, word: str) -> dict[str, Any] | None:
        """Look up phonetic details for a target word."""
        return self._lexicon.get(word.lower().strip())

    def lookup_language(self, word: str, language: str = "English") -> dict[str, Any] | None:
        """Look up phonetic details for a word in a specific language."""
        word_key = word.lower().strip()
        entry = self._lexicon.get(word_key)
        if entry is None:
            return None
            
        lang_key = f"{language.lower()}_alternatives"
        phonetic_key = f"{language.lower()}_phonetic"
        
        result = dict(entry)
        if phonetic_key in entry:
            result["phonetic_spelling"] = entry[phonetic_key]
        if lang_key in entry:
            result["alternatives"] = entry[lang_key]
            
        return result

    def get_ssml_phoneme(self, word: str, language: str = "English") -> str:
        """
        Returns SSML <phoneme> tag for TTS engines if available in lexicon,
        otherwise returns original word. Supports language-specific phonemes.
        """
        entry = self.lookup_language(word, language)
        if entry and "ipa" in entry:
            return f'<phoneme alphabet="ipa" ph="{entry["ipa"]}">{word}</phoneme>'
        return word

    def apply_phonetic_normalization(self, text: str, language: str = "English") -> str:
        """
        Replaces domain keywords with phonetic hints if needed for speech synthesis.
        Uses language-specific phonetic spellings when available.
        """
        words = text.split()
        normalized_words = []
        for w in words:
            clean_w = w.strip(".,!?").lower()
            entry = self.lookup_language(clean_w, language)
            if entry and "phonetic_spelling" in entry:
                normalized_words.append(entry["phonetic_spelling"])
            else:
                normalized_words.append(w)
        return " ".join(normalized_words)

    def get_alternatives(self, word: str) -> list:
        """Get alternative spellings for a word."""
        entry = self.lookup(word)
        if entry and "alternatives" in entry:
            return entry["alternatives"]
        return []

    def get_language_alternatives(self, word: str, language: str) -> list:
        """Get language-specific alternative spellings for a word."""
        entry = self.lookup(word)
        if entry:
            lang_key = f"{language.lower()}_alternatives"
            if lang_key in entry:
                return entry[lang_key]
        return []

    def search_by_domain(self, domain: str) -> dict[str, dict[str, Any]]:
        """Search all lexicon entries by domain category."""
        return {
            word: entry for word, entry in self._lexicon.items()
            if entry.get("domain") == domain
        }


# Global instance
pronunciation_dict = PronunciationDictionary()
