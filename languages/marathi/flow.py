"""
Marathi Language Flow implementation.
"""

from pathlib import Path

from languages.json_flow import JSONLanguageFlow


class MarathiLanguageFlow(JSONLanguageFlow):
    """Marathi Language Flow Engine using flow.json."""

    def __init__(self):
        json_path = Path(__file__).parent / "flow.json"
        super().__init__(json_file_path=json_path)
