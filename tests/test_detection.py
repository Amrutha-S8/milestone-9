"""
Unit tests for Language Detection Service.
"""

from detection.detector import LanguageDetector


def test_detect_telugu_spec_example():
    detector = LanguageDetector()
    res = detector.detect("మాకు ఒక గది కావాలి")
    assert res["language"] == "Telugu"
    assert res["confidence"] >= 0.95


def test_detect_hindi_devanagari():
    detector = LanguageDetector()
    res = detector.detect("मुझे एक कमरा बुक करना है")
    assert res["language"] == "Hindi"
    assert res["confidence"] >= 0.95


def test_detect_hinglish_roman():
    detector = LanguageDetector()
    res = detector.detect("mujhe ek room book karna hai bhai")
    assert res["language"] == "Hinglish"
    assert res["confidence"] >= 0.80


def test_detect_english_ascii():
    detector = LanguageDetector()
    res = detector.detect("I want to book a room")
    assert res["language"] == "English"
    assert res["confidence"] >= 0.90


def test_detect_malayalam_script():
    detector = LanguageDetector()
    res = detector.detect("ഞങ്ങൾക്ക് ഒരു മുറി വേണം")
    assert res["language"] == "Malayalam"
    assert res["confidence"] >= 0.95


def test_detect_marathi_script():
    detector = LanguageDetector()
    res = detector.detect("मला एक रूम हवी आहे")
    assert res["language"] == "Marathi"
    assert res["confidence"] >= 0.85
