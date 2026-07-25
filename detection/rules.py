"""
Detection Rules & Lexicon Markers for Indian Languages.

Design Rationale:
- Unicode Range Matching: Instant, sub-millisecond script detection for native Indian scripts:
  - Telugu: U+0C00 - U+0C7F
  - Devanagari (Hindi / Marathi): U+0900 - U+097F
  - Malayalam: U+0D00 - U+0D7F
- Roman Script Analysis: Distinguishes Standard English from Hinglish (Romanized Hindi/Urdu).
"""

UNICODE_SCRIPT_RANGES = {
    "Telugu": (0x0C00, 0x0C7F),
    "Devanagari": (0x0900, 0x097F),
    "Malayalam": (0x0D00, 0x0D7F),
}

MARATHI_DISTINCTIVE_CHARS = {"ळ", "ॲ", "ऑ"}

MARATHI_SPECIFIC_KEYWORDS = [
    "नमस्कार", "हवी", "पाहिजे", "आहे", "करायची", "झाले", "भाडे"
]

HINDI_SPECIFIC_KEYWORDS = [
    "नमस्ते", "मुझे", "चाहिए", "करना", "है", "कमरा", "कीमत", "प्रतिदिन"
]

HINGLISH_MARKER_WORDS = {
    "chahiye", "karna", "karo", "hai", "hoga", "batao", "mera", "meri", "kab", "kitna",
    "paise", "raat", "namaste", "shukriya", "bhai", "karwa", "milega", "aaj", "kal",
    "bhi", "ho", "kaise", "karte", "dijiye", "kijiye", "bataiye", "karana"
}
