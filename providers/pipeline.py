import logging
import time
from typing import Optional

from providers.base import STTResult, LLMResult, TTSResult
from providers.registry import ProviderRegistry
from providers.cache import get_cache

logger = logging.getLogger("stayza.providers.pipeline")


class STTPipeline:
    def __init__(self, registry: ProviderRegistry):
        self._registry = registry
        self._cache = get_cache()

    def transcribe(self, audio_data: bytes, language: Optional[str] = None, use_cache: bool = True, **kwargs) -> STTResult:
        cache_key = self._cache.make_key("stt", str(hash(audio_data)), language or "auto")
        if use_cache:
            cached = self._cache.get(cache_key)
            if cached is not None:
                logger.info("STT cache hit language=%s", language)
                return cached
        result = self._registry.stt.transcribe(audio_data, language=language, **kwargs)
        if use_cache:
            self._cache.set(cache_key, result, ttl_seconds=60)
        return result


class LLMPipeline:
    def __init__(self, registry: ProviderRegistry):
        self._registry = registry
        self._cache = get_cache()

    def analyze(self, text: str, language: Optional[str] = None, use_cache: bool = True, **kwargs) -> LLMResult:
        cache_key = self._cache.make_key("llm", text, language or "auto")
        if use_cache:
            cached = self._cache.get(cache_key)
            if cached is not None:
                logger.info("LLM cache hit language=%s", language)
                return cached
        result = self._registry.llm.analyze(text, language=language, **kwargs)
        if use_cache:
            self._cache.set(cache_key, result, ttl_seconds=120)
        return result


class TTSPipeline:
    def __init__(self, registry: ProviderRegistry):
        self._registry = registry
        self._cache = get_cache()

    def synthesize(self, text: str, language: Optional[str] = None, voice: Optional[str] = None, use_cache: bool = True, **kwargs) -> TTSResult:
        cache_key = self._cache.make_key("tts", text, voice or "default")
        if use_cache:
            cached = self._cache.get(cache_key)
            if cached is not None:
                logger.info("TTS cache hit voice=%s", voice)
                return cached
        result = self._registry.tts.synthesize(text, language=language, voice=voice, **kwargs)
        if use_cache:
            self._cache.set(cache_key, result, ttl_seconds=300)
        return result
