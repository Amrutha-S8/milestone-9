import logging

from providers.base import TTSProvider, TTSResult
from providers.config import OpenAITTSConfig

logger = logging.getLogger("stayza.providers.tts.openai")


class OpenAITTSProvider(TTSProvider):
    def __init__(self, config: OpenAITTSConfig | None = None):
        self._config = config or OpenAITTSConfig()

    def name(self) -> str:
        return "openai_tts"

    def is_available(self) -> bool:
        return bool(self._config.api_key)

    def synthesize(self, text: str, language: str | None = None, voice: str | None = None, **kwargs) -> TTSResult:
        import time
        start = time.perf_counter()

        try:
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError(f"OpenAI SDK not installed: {e}")

        client = OpenAI(api_key=self._config.api_key)
        response = client.audio.speech.create(
            model=self._config.model,
            voice=voice or self._config.voice,
            input=text,
        )
        audio_data = response.content

        duration_ms = (time.perf_counter() - start) * 1000
        return TTSResult(
            audio_data=audio_data,
            duration_ms=round(duration_ms, 2),
            format="mp3",
        )
