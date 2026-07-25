"""
Dataset loader and validator for StayZa Milestone 9 benchmark datasets.
Supports upgraded Day 3 dataset format:
{
  "text": "I need a deluxe room for 2 adults tomorrow",
  "intent": "booking",
  "entities": {"room_type": "Deluxe", "guests": 2, "check_in": "tomorrow"},
  "expected_action": "ask_checkin_date"
}
"""

import json
import os
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class BenchmarkItem(BaseModel):
    """Upgraded schema for ground truth evaluation dataset entries."""
    id: Optional[str] = None
    text: str
    expected_language: Optional[str] = "English"
    intent: Optional[str] = None
    expected_intent: Optional[str] = None
    expected_action: Optional[str] = None
    expected_next_action: Optional[str] = None
    entities: Dict[str, Any] = Field(default_factory=dict)
    category: str = Field(default="standard")

    def get_intent(self) -> str:
        return self.intent or self.expected_intent or "unknown"

    def get_expected_action(self) -> str:
        return self.expected_action or self.expected_next_action or "ask_clarification"


class DatasetLoader:
    """Loads and validates multi-language benchmark datasets."""

    def __init__(self, dataset_path: Optional[str] = None):
        self.dataset_path = dataset_path

    def load_file(self, file_path: str) -> List[BenchmarkItem]:
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        items = []
        for idx, item in enumerate(data):
            if "id" not in item:
                item["id"] = f"item_{idx+1}"
            items.append(BenchmarkItem(**item))
        return items

    def load(self) -> List[BenchmarkItem]:
        base_dir = os.path.dirname(__file__)
        files_to_load = [
            os.path.join(base_dir, "english.json"),
            os.path.join(base_dir, "hindi.json"),
            os.path.join(base_dir, "hinglish.json"),
            # Day 4: Expanded to cover all 6 supported languages
            os.path.join(base_dir, "telugu.json"),
            os.path.join(base_dir, "marathi.json"),
            os.path.join(base_dir, "malayalam.json"),
        ]

        if self.dataset_path:
            files_to_load = [self.dataset_path]

        combined = []
        for fp in files_to_load:
            combined.extend(self.load_file(fp))
        return combined
