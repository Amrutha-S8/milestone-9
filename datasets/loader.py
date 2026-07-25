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
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class BenchmarkItem(BaseModel):
    """Upgraded schema for ground truth evaluation dataset entries."""
    id: str | None = None
    text: str
    expected_language: str | None = "English"
    intent: str | None = None
    expected_intent: str | None = None
    expected_action: str | None = None
    expected_next_action: str | None = None
    entities: dict[str, Any] = Field(default_factory=dict)
    category: str = Field(default="standard")

    def get_intent(self) -> str:
        return self.intent or self.expected_intent or "unknown"

    def get_expected_action(self) -> str:
        return self.expected_action or self.expected_next_action or "ask_clarification"


class DatasetLoader:
    """Loads and validates multi-language benchmark datasets."""

    def __init__(self, dataset_path: str | None = None):
        self.dataset_path = dataset_path

    def load_file(self, file_path: str) -> list[BenchmarkItem]:
        p = Path(file_path)
        if not p.exists():
            return []
        with p.open(encoding="utf-8") as f:
            data = json.load(f)
        items = []
        for idx, item in enumerate(data):
            if "id" not in item:
                item["id"] = f"item_{idx+1}"
            items.append(BenchmarkItem(**item))
        return items

    def load(self) -> list[BenchmarkItem]:
        base_dir = Path(__file__).parent
        files_to_load = [
            base_dir / "english.json",
            base_dir / "hindi.json",
            base_dir / "hinglish.json",
            base_dir / "telugu.json",
            base_dir / "marathi.json",
            base_dir / "malayalam.json",
        ]

        if self.dataset_path:
            files_to_load = [self.dataset_path]

        combined = []
        for fp in files_to_load:
            combined.extend(self.load_file(fp))
        return combined
