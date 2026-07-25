import logging
from typing import Optional

from providers.base import STTProvider, STTResult
from providers.config import GoogleSTTConfig

logger = logging.getLogger("stayza.providers.stt.google")


class GoogleSTTProvider(STTProvider):
    def __init__(self, config: Optional[GoogleSTTConfig] = None):
        self._config = config or GoogleSTTConfig()

    def name(self) -> str:
        return "google_stt"

    def is_available(self) -> bool:
        if not self._config.credentials_path:
            return False
        import os
        return os.path.exists(self._config.credentials_path)

    def transcribe(self, audio_data: bytes, language: Optional[str] = None, **kwargs) -> STTResult:
        import time
        start = time.perf_counter()

        try:
            from google.cloud import speech
        except ImportError as e:
            raise RuntimeError(f"Google Cloud Speech SDK not installed: {e}")

        client = speech.SpeechClient.from_service_account_file(self._config.credentials_path)
        audio = speech.RecognitionAudio(content=audio_data)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=kwargs.get("sample_rate", 8000),
            language_code=language or "hi-IN",
            model="latest_long",
        )
        response = client.recognize(config=config, audio=audio)

        if not response.results:
            duration_ms = (time.perf_counter() - start) * 1000
            return STTResult(text="", confidence=0.0, language=language or "hi", duration_ms=round(duration_ms, 2))

        best = response.results[0].alternatives[0]
        words = [{"word": w.word, "start": 0.0, "end": 0.0, "confidence": w.confidence}
                 for w in (best.words or [])]
        duration_ms = (time.perf_counter() - start) * 1000
        return STTResult(
            text=best.transcript.strip(),
            confidence=best.confidence,
            language=language or "hi",
            duration_ms=round(duration_ms, 2),
            words=words,
        )
