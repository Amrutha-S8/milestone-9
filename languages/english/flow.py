"""
English Language Flow implementation for StayZa hotel voice assistant.

Extends JSONLanguageFlow to load languages/english/flow.json.
"""

import os
from languages.json_flow import JSONLanguageFlow


class EnglishLanguageFlow(JSONLanguageFlow):
    """
    English Language Flow Engine powered by flow.json specification.
    """

    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), "flow.json")
        super().__init__(json_file_path=json_path)
