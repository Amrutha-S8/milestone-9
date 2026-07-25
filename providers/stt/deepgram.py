import logging
from typing import Optional

from providers.base import STTProvider, STTResult
from providers.config import DeepgramConfig

logger = logging.getLogger("stayza.providers.stt.deepgram")


class DeepgramSTTProvider(STTProvider):
    def __init__(self, config: Optional[DeepgramConfig] = None):
        self._config = config or DeepgramConfig()

    def name(self) -> str:
        return "deepgram"

    def is_available(self) -> bool:
        return bool(self._config.api_key)

    def transcribe(self, audio_data: bytes, language: Optional[str] = None, **kwargs) -> STTResult:
        import time
        start = time.perf_counter()

        try:
            from deepgram import DeepgramClient, PrerecordedOptions
            import httpx
        except ImportError as e:
            raise RuntimeError(f"Deepgram SDK not installed: {e}")

        client = DeepgramClient(api_key=self._config.api_key)
        options = PrerecordedOptions(model=self._config.model, language=language or "hi")
        response = client.listen.rest.v("1").transcribe_file({"buffer": audio_data, "filename": "audio.wav"}, options)

        channel = response.results.channels[0].alternatives[0]
        words = [
            {"word": w.word, "start": w.start, "end": w.end, "confidence": w.confidence}
            for w in (channel.words or [])
        ]
        duration_ms = (time.perf_counter() - start) * 1000
        return STTResult(
            text=channel.transcript.strip(),
            confidence=channel.confidence,
            language=language or "hi",
            duration_ms=round(duration_ms, 2),
            words=words,
        )
