from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class STTResult:
    text: str
    confidence: float
    language: str
    duration_ms: float
    words: list[dict] = field(default_factory=list)


@dataclass
class LLMResult:
    text: str
    intent: str
    confidence: float
    duration_ms: float
    raw_response: dict | None = None


@dataclass
class TTSResult:
    audio_data: bytes
    duration_ms: float
    format: str = "wav"


class STTProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_data: bytes, language: str | None = None, **kwargs) -> STTResult:
        ...

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...


class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, text: str, language: str | None = None, **kwargs) -> LLMResult:
        ...

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...


class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, language: str | None = None, voice: str | None = None, **kwargs) -> TTSResult:
        ...

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...
