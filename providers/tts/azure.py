import logging

from providers.base import TTSProvider, TTSResult
from providers.config import AzureTTSConfig

logger = logging.getLogger("stayza.providers.tts.azure")


class AzureTTSProvider(TTSProvider):
    def __init__(self, config: AzureTTSConfig | None = None):
        self._config = config or AzureTTSConfig()

    def name(self) -> str:
        return "azure_tts"

    def is_available(self) -> bool:
        return bool(self._config.subscription_key)

    def synthesize(self, text: str, language: str | None = None, voice: str | None = None, **kwargs) -> TTSResult:
        import time
        start = time.perf_counter()

        try:
            import azure.cognitiveservices.speech as speechsdk
        except ImportError as e:
            raise RuntimeError(f"Azure Speech SDK not installed: {e}")

        speech_config = speechsdk.SpeechConfig(
            subscription=self._config.subscription_key,
            region=self._config.region,
        )
        speech_config.speech_synthesis_voice_name = voice or self._config.voice_name

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            duration_ms = (time.perf_counter() - start) * 1000
            return TTSResult(
                audio_data=result.audio_data,
                duration_ms=round(duration_ms, 2),
                format="wav",
            )
        raise RuntimeError(f"Azure TTS synthesis failed: {result.reason}")
