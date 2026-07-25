import logging
from typing import Optional

from providers.base import STTProvider, LLMProvider, TTSProvider, STTResult, LLMResult, TTSResult

logger = logging.getLogger("stayza.providers.fallback")


class FallbackSTT:
    def __init__(self, providers: list[STTProvider]):
        if not providers:
            raise ValueError("At least one STT provider is required")
        self._providers = providers

    def transcribe(self, audio_data: bytes, language: Optional[str] = None, **kwargs) -> STTResult:
        last_error = None
        for provider in self._providers:
            try:
                if not provider.is_available():
                    logger.warning("STT provider '%s' not available, skipping", provider.name())
                    continue
                logger.info("STT trying provider='%s' language=%s", provider.name(), language)
                return provider.transcribe(audio_data, language=language, **kwargs)
            except Exception as e:
                last_error = e
                logger.error("STT provider '%s' failed: %s", provider.name(), e)
        raise RuntimeError(f"All STT providers failed. Last error: {last_error}")

    @property
    def providers(self) -> list[STTProvider]:
        return list(self._providers)


class FallbackLLM:
    def __init__(self, providers: list[LLMProvider]):
        if not providers:
            raise ValueError("At least one LLM provider is required")
        self._providers = providers

    def analyze(self, text: str, language: Optional[str] = None, **kwargs) -> LLMResult:
        last_error = None
        for provider in self._providers:
            try:
                if not provider.is_available():
                    logger.warning("LLM provider '%s' not available, skipping", provider.name())
                    continue
                logger.info("LLM trying provider='%s' language=%s", provider.name(), language)
                return provider.analyze(text, language=language, **kwargs)
            except Exception as e:
                last_error = e
                logger.error("LLM provider '%s' failed: %s", provider.name(), e)
        raise RuntimeError(f"All LLM providers failed. Last error: {last_error}")

    @property
    def providers(self) -> list[LLMProvider]:
        return list(self._providers)


class FallbackTTS:
    def __init__(self, providers: list[TTSProvider]):
        if not providers:
            raise ValueError("At least one TTS provider is required")
        self._providers = providers

    def synthesize(self, text: str, language: Optional[str] = None, voice: Optional[str] = None, **kwargs) -> TTSResult:
        last_error = None
        for provider in self._providers:
            try:
                if not provider.is_available():
                    logger.warning("TTS provider '%s' not available, skipping", provider.name())
                    continue
                logger.info("TTS trying provider='%s' language=%s", provider.name(), language)
                return provider.synthesize(text, language=language, voice=voice, **kwargs)
            except Exception as e:
                last_error = e
                logger.error("TTS provider '%s' failed: %s", provider.name(), e)
        raise RuntimeError(f"All TTS providers failed. Last error: {last_error}")

    @property
    def providers(self) -> list[TTSProvider]:
        return list(self._providers)
