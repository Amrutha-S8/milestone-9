"""
Unit tests for English Language Flow engine and Intent Analyzer.
"""

from languages.english.flow import EnglishLanguageFlow


def test_english_flow_booking():
    flow = EnglishLanguageFlow()
    result = flow.process("I want to book a room")
    assert result.language == "English"
    assert result.intent == "booking"
    assert result.confidence == 0.95
    assert result.next_action == "ask_checkin_date"


def test_english_flow_cancellation():
    flow = EnglishLanguageFlow()
    result = flow.process("Cancel my reservation please")
    assert result.intent == "cancellation"
    assert result.next_action == "ask_booking_id"


def test_english_flow_availability():
    flow = EnglishLanguageFlow()
    result = flow.process("Are there any deluxe rooms available for tomorrow?")
    assert result.intent == "availability"
    assert result.next_action == "ask_stay_dates"
    assert result.slots.get("room_type") == "deluxe"


def test_english_flow_price_enquiry():
    flow = EnglishLanguageFlow()
    result = flow.process("How much does a suite room cost per night?")
    assert result.intent == "price_enquiry"
    assert result.next_action == "provide_rate_card"
    assert result.slots.get("room_type") == "suite"


def test_english_flow_greeting():
    flow = EnglishLanguageFlow()
    result = flow.process("Good morning StayZa")
    assert result.intent == "greeting"
    assert result.next_action == "ask_how_to_help"


def test_english_flow_unknown():
    flow = EnglishLanguageFlow()
    result = flow.process("qwertyuiop 123456")
    assert result.intent == "unknown"
    assert result.next_action == "ask_clarification"
