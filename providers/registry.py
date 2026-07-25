import logging

from providers.config import ProviderConfig
from providers.fallback import FallbackLLM, FallbackSTT, FallbackTTS
from providers.llm.claude import ClaudeProvider
from providers.llm.gpt4o import GPT4oProvider
from providers.stt.deepgram import DeepgramSTTProvider
from providers.stt.google import GoogleSTTProvider
from providers.stt.whisper import WhisperSTTProvider
from providers.tts.azure import AzureTTSProvider
from providers.tts.openai import OpenAITTSProvider

logger = logging.getLogger("stayza.providers.registry")


class ProviderRegistry:
    def __init__(self, config: ProviderConfig | None = None):
        self._config = config or ProviderConfig()
        self._stt = FallbackSTT([
            WhisperSTTProvider(self._config.whisper),
            DeepgramSTTProvider(self._config.deepgram),
            GoogleSTTProvider(self._config.google_stt),
        ])
        self._llm = FallbackLLM([
            GPT4oProvider(self._config.gpt4o),
            ClaudeProvider(self._config.claude),
        ])
        self._tts = FallbackTTS([
            AzureTTSProvider(self._config.azure_tts),
            OpenAITTSProvider(self._config.openai_tts),
        ])

    @property
    def stt(self) -> FallbackSTT:
        return self._stt

    @property
    def llm(self) -> FallbackLLM:
        return self._llm

    @property
    def tts(self) -> FallbackTTS:
        return self._tts

    def health(self) -> dict:
        return {
            "stt": {
                p.name(): p.is_available()
                for p in self._stt.providers
            },
            "llm": {
                p.name(): p.is_available()
                for p in self._llm.providers
            },
            "tts": {
                p.name(): p.is_available()
                for p in self._tts.providers
            },
        }


_registry: ProviderRegistry | None = None


def get_provider_registry(config: ProviderConfig | None = None) -> ProviderRegistry:
    global _registry
    if _registry is None:
        _registry = ProviderRegistry(config)
    return _registry
