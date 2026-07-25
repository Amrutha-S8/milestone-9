import os
from dataclasses import dataclass, field


@dataclass
class WhisperConfig:
    model_size: str = field(default_factory=lambda: os.getenv("WHISPER_MODEL_SIZE", "medium"))
    device: str = field(default_factory=lambda: os.getenv("WHISPER_DEVICE", "cpu"))
    compute_type: str = field(default_factory=lambda: os.getenv("WHISPER_COMPUTE_TYPE", "float16"))


@dataclass
class DeepgramConfig:
    api_key: str = field(default_factory=lambda: os.getenv("DEEPGRAM_API_KEY", ""))
    model: str = field(default_factory=lambda: os.getenv("DEEPGRAM_MODEL", "nova-2-general"))


@dataclass
class GoogleSTTConfig:
    credentials_path: str = field(default_factory=lambda: os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""))


@dataclass
class GPT4oConfig:
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = field(default_factory=lambda: os.getenv("GPT4O_MODEL", "gpt-4o"))
    endpoint: str | None = field(default_factory=lambda: os.getenv("OPENAI_ENDPOINT", None))


@dataclass
class ClaudeConfig:
    api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    model: str = field(default_factory=lambda: os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229"))


@dataclass
class AzureTTSConfig:
    subscription_key: str = field(default_factory=lambda: os.getenv("AZURE_TTS_KEY", ""))
    region: str = field(default_factory=lambda: os.getenv("AZURE_TTS_REGION", "eastus"))
    voice_name: str = field(default_factory=lambda: os.getenv("AZURE_TTS_VOICE", "en-IN-NeerjaNeural"))


@dataclass
class OpenAITTSConfig:
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = field(default_factory=lambda: os.getenv("OPENAI_TTS_MODEL", "tts-1"))
    voice: str = field(default_factory=lambda: os.getenv("OPENAI_TTS_VOICE", "alloy"))


@dataclass
class ProviderConfig:
    whisper: WhisperConfig = field(default_factory=WhisperConfig)
    deepgram: DeepgramConfig = field(default_factory=DeepgramConfig)
    google_stt: GoogleSTTConfig = field(default_factory=GoogleSTTConfig)
    gpt4o: GPT4oConfig = field(default_factory=GPT4oConfig)
    claude: ClaudeConfig = field(default_factory=ClaudeConfig)
    azure_tts: AzureTTSConfig = field(default_factory=AzureTTSConfig)
    openai_tts: OpenAITTSConfig = field(default_factory=OpenAITTSConfig)
