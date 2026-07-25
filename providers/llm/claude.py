import json
import logging

from providers.base import LLMProvider, LLMResult
from providers.config import ClaudeConfig

logger = logging.getLogger("stayza.providers.llm.claude")

_INTENT_PROMPT = """Analyze this hotel booking utterance and return ONLY JSON:
{
  "intent": "greeting|booking|availability|price_enquiry|cancellation|modify_booking|check_status|goodbye|unknown",
  "confidence": 0.0-1.0,
  "language": "detected language",
  "entities": {}
}"""


class ClaudeProvider(LLMProvider):
    def __init__(self, config: ClaudeConfig | None = None):
        self._config = config or ClaudeConfig()

    def name(self) -> str:
        return "claude"

    def is_available(self) -> bool:
        return bool(self._config.api_key)

    def analyze(self, text: str, language: str | None = None, **kwargs) -> LLMResult:
        import time
        start = time.perf_counter()

        try:
            import anthropic
        except ImportError as e:
            raise RuntimeError(f"Anthropic SDK not installed: {e}")

        client = anthropic.Anthropic(api_key=self._config.api_key)
        response = client.messages.create(
            model=self._config.model,
            max_tokens=256,
            system=_INTENT_PROMPT,
            messages=[{"role": "user", "content": text}],
        )
        content = response.content[0].text.strip()
        parsed = json.loads(content)

        duration_ms = (time.perf_counter() - start) * 1000
        return LLMResult(
            text=text,
            intent=parsed.get("intent", "unknown"),
            confidence=parsed.get("confidence", 0.0),
            duration_ms=round(duration_ms, 2),
            raw_response=parsed,
        )
