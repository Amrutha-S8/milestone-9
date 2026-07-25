import logging
from typing import Optional

from providers.base import STTProvider, STTResult
from providers.config import WhisperConfig

logger = logging.getLogger("stayza.providers.stt.whisper")


class WhisperSTTProvider(STTProvider):
    def __init__(self, config: Optional[WhisperConfig] = None):
        self._config = config or WhisperConfig()
        self._model = None

    def name(self) -> str:
        return "whisper"

    def is_available(self) -> bool:
        try:
            import whisper
            return True
        except ImportError:
            return False

    def _load_model(self):
        if self._model is None:
            import whisper
            logger.info("Loading Whisper model size=%s device=%s", self._config.model_size, self._config.device)
            self._model = whisper.load_model(self._config.model_size, device=self._config.device)

    def transcribe(self, audio_data: bytes, language: Optional[str] = None, **kwargs) -> STTResult:
        import time
        import tempfile
        start = time.perf_counter()

        self._load_model()

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_data)
            tmp_path = tmp.name

        try:
            result = self._model.transcribe(tmp_path, language=language, fp16=self._config.compute_type == "float16")
            duration_ms = (time.perf_counter() - start) * 1000
            words = []
            for segment in result.get("segments", []):
                for word_text in segment.get("text", "").split():
                    words.append({
                        "word": word_text,
                        "start": segment.get("start", 0.0),
                        "end": segment.get("end", 0.0),
                        "confidence": segment.get("confidence", 0.0),
                    })

            return STTResult(
                text=result.get("text", "").strip(),
                confidence=result.get("confidence", 0.0),
                language=result.get("language", language or "en"),
                duration_ms=round(duration_ms, 2),
                words=words,
            )
        finally:
            import os
            os.unlink(tmp_path)
