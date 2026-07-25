from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


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
    raw_response: Optional[dict] = None


@dataclass
class TTSResult:
    audio_data: bytes
    duration_ms: float
    format: str = "wav"


class STTProvider(ABC):
    @abstractmethod
    def transcribe(self, audio_data: bytes, language: Optional[str] = None, **kwargs) -> STTResult:
        ...

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...


class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, text: str, language: Optional[str] = None, **kwargs) -> LLMResult:
        ...

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...


class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str, language: Optional[str] = None, voice: Optional[str] = None, **kwargs) -> TTSResult:
        ...

    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def is_available(self) -> bool:
        ...
