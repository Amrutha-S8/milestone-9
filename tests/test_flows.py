"""
Unit tests for multi-language JSON-driven flow engine.
"""

from languages.english.flow import EnglishLanguageFlow
from languages.hindi.flow import HindiLanguageFlow
from languages.hinglish.flow import HinglishLanguageFlow
from languages.malayalam.flow import MalayalamLanguageFlow
from languages.marathi.flow import MarathiLanguageFlow
from languages.registry import LanguageRegistry
from languages.telugu.flow import TeluguLanguageFlow


def setup_registry() -> LanguageRegistry:
    reg = LanguageRegistry()
    reg.register(EnglishLanguageFlow())
    reg.register(HindiLanguageFlow())
    reg.register(HinglishLanguageFlow())
    reg.register(TeluguLanguageFlow())
    reg.register(MarathiLanguageFlow())
    reg.register(MalayalamLanguageFlow())
    return reg


def test_telugu_flow_processing():
    reg = setup_registry()
    res = reg.detect_and_process("మాకు ఒక గది కావాలి")
    assert res.language == "Telugu"
    assert res.intent == "booking"
    assert res.next_action == "ask_checkin_date"


def test_hindi_flow_processing():
    reg = setup_registry()
    res = reg.detect_and_process("मुझे एक कमरा बुक करना है")
    assert res.language == "Hindi"
    assert res.intent == "booking"
    assert res.next_action == "ask_checkin_date"


def test_hinglish_flow_processing():
    reg = setup_registry()
    res = reg.detect_and_process("mujhe ek room book karna hai")
    assert res.language == "Hinglish"
    assert res.intent == "booking"
    assert res.next_action == "ask_checkin_date"


def test_marathi_flow_processing():
    reg = setup_registry()
    res = reg.detect_and_process("मला एक रूम हवी आहे")
    assert res.language == "Marathi"
    assert res.intent == "booking"


def test_malayalam_flow_processing():
    reg = setup_registry()
    res = reg.detect_and_process("ഞങ്ങൾക്ക് ഒരു മുറി വേണം")
    assert res.language == "Malayalam"
    assert res.intent == "booking"
