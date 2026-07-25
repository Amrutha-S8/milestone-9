"""
Reusable Entity Extractor Module for StayZa.

Design Rationale:
- Extracts structured entity slots (room_type, guests, check_in, check_out, budget, booking_id, guest_name).
- Modular, thread-safe, and independent of specific language flow controllers.
"""

import re
from typing import Any

from entities.rules import (
    BOOKING_ID_PATTERNS,
    BUDGET_PATTERNS,
    DATE_KEYWORD_PATTERNS,
    GUEST_PATTERNS,
    NUMBER_WORD_MAP,
    ROOM_TYPES,
)


class EntityExtractor:
    """
    Extracts hotel booking entities from text.
    """

    def extract(self, text: str) -> dict[str, Any]:
        """Extract entities dict from user utterance.
        
        Example Input:
            "I need a deluxe room for 2 adults tomorrow."
            
        Example Output:
            {
              "room_type": "deluxe",
              "guests": 2,
              "check_in": "tomorrow"
            }
        """
        clean_text = text.lower().strip()
        entities: dict[str, Any] = {}

        if not clean_text:
            return entities

        # 1. Room Type Entity
        for rt in ROOM_TYPES:
            if rt in clean_text:
                entities["room_type"] = rt.capitalize()
                break

        # 2. Guests Entity
        for g_pat in GUEST_PATTERNS:
            match = re.search(g_pat, clean_text)
            if match:
                raw_g = match.group(1).lower()
                if raw_g.isdigit():
                    entities["guests"] = int(raw_g)
                elif raw_g in NUMBER_WORD_MAP:
                    entities["guests"] = NUMBER_WORD_MAP[raw_g]
                break

        # 3. Check-in Date Entity
        for d_pat in DATE_KEYWORD_PATTERNS:
            match = re.search(d_pat, clean_text)
            if match:
                entities["check_in"] = match.group(1).lower()
                break

        # 4. Booking ID Entity
        for b_pat in BOOKING_ID_PATTERNS:
            match = re.search(b_pat, clean_text)
            if match:
                entities["booking_id"] = match.group(1).upper()
                break

        # 5. Budget Entity
        for bg_pat in BUDGET_PATTERNS:
            match = re.search(bg_pat, clean_text)
            if match:
                entities["budget"] = f"${match.group(1)}"
                break

        return entities


# Global singleton instance
entity_extractor = EntityExtractor()
