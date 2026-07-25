import json
import logging
from typing import Optional

from providers.base import LLMProvider, LLMResult
from providers.config import GPT4oConfig

logger = logging.getLogger("stayza.providers.llm.gpt4o")

_INTENT_SYSTEM_PROMPT = """You are a multilingual hotel booking intent classifier.
Analyze the user's utterance and respond with JSON:
{
  "intent": "greeting|booking|availability|price_enquiry|cancellation|modify_booking|check_status|goodbye|unknown",
  "confidence": 0.0-1.0,
  "language": "detected language",
  "entities": { ... }
}
Respond with ONLY the JSON object."""


class GPT4oProvider(LLMProvider):
    def __init__(self, config: Optional[GPT4oConfig] = None):
        self._config = config or GPT4oConfig()

    def name(self) -> str:
        return "gpt-4o"

    def is_available(self) -> bool:
        return bool(self._config.api_key)

    def analyze(self, text: str, language: Optional[str] = None, **kwargs) -> LLMResult:
        import time
        start = time.perf_counter()

        try:
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError(f"OpenAI SDK not installed: {e}")

        client = OpenAI(api_key=self._config.api_key, base_url=self._config.endpoint)
        response = client.chat.completions.create(
            model=self._config.model,
            messages=[
                {"role": "system", "content": _INTENT_SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)

        duration_ms = (time.perf_counter() - start) * 1000
        return LLMResult(
            text=text,
            intent=parsed.get("intent", "unknown"),
            confidence=parsed.get("confidence", 0.0),
            duration_ms=round(duration_ms, 2),
            raw_response=parsed,
        )
