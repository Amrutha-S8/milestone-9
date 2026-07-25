"""
Entity Extraction Regex & Lexicon Rules for StayZa Hotel Domain.
"""

import re

ROOM_TYPES = [
    "deluxe", "suite", "executive", "presidential", "standard", "king", "single", "double", "twin"
]

NUMBER_WORD_MAP = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "एक": 1, "दो": 2, "तीन": 3, "चार": 4, "పాంచ్": 5
}

DATE_KEYWORD_PATTERNS = [
    r"\b(today|tomorrow|yesterday)\b",
    r"\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    r"\b(\d{1,2}(?:st|nd|rd|th)?\s+(?:january|february|march|april|may|june|july|august|september|october|november|december))\b",
    r"\b(next week|this weekend)\b"
]

BOOKING_ID_PATTERNS = [
    r"\b(?:bk|id|ref|booking)\s*#?\s*([a-z0-9\-]+)\b",
    r"\b([a-z]{2}\-?\d{4,6})\b"
]

GUEST_PATTERNS = [
    r"\b(\d+|one|two|three|four|five)\s*(?:adults?|guests?|people|persons?|people|लोग|लोगो|పేరు)\b",
    r"\bfor\s+(\d+|one|two|three|four|five)\b"
]

BUDGET_PATTERNS = [
    r"\b(?:under|below|less than|\$|₹|rs\.?|rupees)\s*(\d+)\b",
    r"\b(\d+)\s*(?:rupees|usd|\$|₹)\b"
]
