"""
Hotel Domain Abbreviation & Normalization Rules for StayZa.

Design Rationale:
- Centralizing normalization mappings in one JSON-like dict makes them easy
  to extend without touching Python code.
- All rules are applied BEFORE intent detection to improve accuracy
  (e.g., "A/C" -> "AC", "Bengaluru" -> "Bangalore").
- Ordering matters: longer keys should be matched first to prevent partial replacements.
"""

from typing import Dict, List, Tuple


# ── Hotel domain abbreviation & alias expansions ──────────────────────────────
# Format: { "raw_form": "normalized_form" }
# Keys are lowercased; matching is case-insensitive.
ABBREVIATION_MAP: Dict[str, str] = {
    # Room type shorthands
    "a/c":          "ac",
    "a.c.":         "ac",
    "ac room":      "ac room",
    "non a/c":      "non ac",
    "non-ac":       "non ac",

    # City aliases (common misspellings / alternate names used in Indian speech)
    "bengaluru":    "bangalore",
    "bengalore":    "bangalore",
    "bombay":       "mumbai",
    "madras":       "chennai",
    "calcutta":     "kolkata",
    "mysore":       "mysuru",
    "pondicherry":  "puducherry",

    # Common hotel service shorthands
    "b&b":          "bed and breakfast",
    "b and b":      "bed and breakfast",
    "ep":           "european plan",
    "ap":           "american plan",
    "cp":           "continental plan",
    "map":          "modified american plan",

    # Booking-related normalizations
    "asap":         "as soon as possible",
    "chk in":       "check in",
    "chk out":      "check out",
    "ck in":        "check in",
    "ck out":       "check out",

    # Number/date colloquialisms
    "tonite":       "tonight",
    "tmrw":         "tomorrow",
    "tom":          "tomorrow",
    "nxt wk":       "next week",

    # Currency normalizations
    "rs ":          "rupees ",
    "rs.":          "rupees",
    "inr":          "rupees",
    "₹":            "rupees ",
}

# ── Transliteration Normalizations (common Hinglish/regional forms -> canonical) ──
TRANSLITERATION_MAP: Dict[str, str] = {
    # Hindi transliterations
    "kal":          "tomorrow",
    "aaj":          "today",
    "parso":        "day after tomorrow",
    "ek":           "one",
    "do":           "two",
    "teen":         "three",
    "char":         "four",
    "paanch":       "five",

    # Common Hindi hotel terms in roman script
    "kamra":        "room",
    "kamre":        "rooms",
    "khana":        "food",
    "nasta":        "breakfast",

    # Telugu romanized terms
    "gadhi":        "room",
    "neeru":        "water",
    "tindi":        "food",

    # Marathi romanized terms
    "kholi":        "room",
    "kholi havi":   "need a room",
    "udya":         "tomorrow",
    "aaj":          "today",

    # Malayalam romanized terms
    "muri":         "room",
    "naale":        "tomorrow",
    "innu":         "today",
}

# ── Noise patterns to strip (regex-safe) ─────────────────────────────────────
# These are STT artifacts, filler words, and punctuation artifacts.
NOISE_TOKENS: List[str] = [
    "umm", "uh", "uhh", "hmm", "hm", "err", "ah", "ah um",
    "like um", "you know", "i mean",
    "...", "…",
]
