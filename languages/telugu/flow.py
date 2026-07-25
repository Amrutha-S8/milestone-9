"""
Telugu Language Flow implementation.
"""

import os
from languages.json_flow import JSONLanguageFlow


class TeluguLanguageFlow(JSONLanguageFlow):
    """Telugu Language Flow Engine using flow.json."""

    def __init__(self):
        json_path = os.path.join(os.path.dirname(__file__), "flow.json")
        super().__init__(json_file_path=json_path)
