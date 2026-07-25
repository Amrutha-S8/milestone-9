"""
Unit tests for pronunciation dictionary and TTS phonetic hints.
"""

from pronunciation.dictionary import PronunciationDictionary


def test_pronunciation_lookup():
    dict_engine = PronunciationDictionary()
    entry = dict_engine.lookup("stayza")
    assert entry is not None
    assert "ipa" in entry
    assert entry["ipa"] == "ˈsteɪ.zə"


def test_ssml_generation():
    dict_engine = PronunciationDictionary()
    ssml = dict_engine.get_ssml_phoneme("stayza")
    assert '<phoneme alphabet="ipa" ph="ˈsteɪ.zə">stayza</phoneme>' in ssml


def test_phonetic_normalization():
    dict_engine = PronunciationDictionary()
    normalized = dict_engine.apply_phonetic_normalization("I booked a deluxe suite at StayZa")
    assert "Deh-luks" in normalized
    assert "Sweet" in normalized
    assert "Stay-zah" in normalized
