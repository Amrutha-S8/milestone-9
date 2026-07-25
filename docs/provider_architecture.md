# StayZa Provider Architecture

## Design Pattern: Adapter + Fallback Chain

The provider system uses the **Adapter Pattern** to wrap third-party AI services behind a unified interface, and the **Chain of Responsibility** pattern for fallback.

## Base Interfaces

```python
class STTProvider(ABC):
    def transcribe(audio_data, language) -> STTResult

class LLMProvider(ABC):
    def analyze(text, language) -> LLMResult

class TTSProvider(ABC):
    def synthesize(text, language, voice) -> TTSResult
```

Each provider implements:
- `name()` — unique identifier
- `is_available()` — checks credentials/config
- The core operation with unified return types

## Fallback Chain

```
FallbackSTT:
  1. Whisper (local whisper.cpp or OpenAI)
  2. Deepgram (nova-2 model)
  3. Google STT (Cloud Speech-to-Text)

FallbackLLM:
  1. GPT-4o (OpenAI / Azure OpenAI)
  2. Claude (Anthropic)

FallbackTTS:
  1. Azure TTS (Cognitive Services)
  2. OpenAI TTS (tts-1 model)
```

## Caching Layer

Each pipeline (STT, LLM, TTS) wraps the fallback chain with a thread-safe LRU cache:
- STT: 60s TTL, keyed by audio hash
- LLM: 120s TTL, keyed by text + language
- TTS: 300s TTL, keyed by text + voice

## Provider Health

The registry exposes `health()` which returns availability of every provider:

```json
{
  "stt": {"whisper": true, "deepgram": false, "google_stt": false},
  "llm": {"gpt-4o": true, "claude": false},
  "tts": {"azure_tts": true, "openai_tts": false}
}
```

## Adding a New Provider

1. Create adapter in `providers/stt/`, `providers/llm/`, or `providers/tts/`
2. Implement base interface with `name()`, `is_available()`, and operation method
3. Add config in `providers/config.py`
4. Register in `providers/registry.py` fallback chain
5. Export in `providers/__init__.py`
