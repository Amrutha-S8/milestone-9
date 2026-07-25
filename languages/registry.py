"""
Central Language Registry for StayZa Milestone 9.

Design Rationale:
- Registry / Factory Pattern: Maintains active language handlers.
- Auto-routing: Automatically detects input language across registered flows or uses target flow.
- Scalability: Day 1 registers EnglishLanguageFlow; Hindi, Telugu, Marathi, Malayalam can be registered with 1 line of code.
"""


from languages.base import BaseLanguageFlow, FlowResult


class LanguageRegistry:
    """
    Registry that holds language flows and handles language selection/detection.
    """

    def __init__(self):
        self._registry: dict[str, BaseLanguageFlow] = {}
        self._default_language: str = "English"

    def register(self, flow: BaseLanguageFlow) -> None:
        """Register a new language flow engine."""
        self._registry[flow.language_name.lower()] = flow
        self._registry[flow.language_code.lower()] = flow

    def get_flow(self, language_identifier: str) -> BaseLanguageFlow | None:
        """Retrieve language flow by name or ISO code."""
        return self._registry.get(language_identifier.lower())

    def list_supported_languages(self) -> list[str]:
        """Returns list of unique registered language names."""
        unique_names = {flow.language_name for flow in self._registry.values()}
        return sorted(unique_names)

    def detect_and_process(self, text: str, target_language: str | None = None, current_state: str | None = None) -> FlowResult:
        """
        Processes text using the specified target language flow, or auto-detects the highest confidence language flow.
        """
        if not text or not text.strip():
            # Fallback for empty utterance
            default_flow = self.get_flow(self._default_language)
            return FlowResult(
                language=self._default_language if default_flow else "Unknown",
                intent="unknown",
                confidence=0.0,
                next_action="ask_clarification",
                slots={},
                raw_text=text
            )

        if target_language:
            flow = self.get_flow(target_language)
            if flow:
                return flow.process(text, current_state)

        # Auto-detect across registered language engines
        best_flow: BaseLanguageFlow | None = None
        best_score: float = -1.0

        # Unique flows to avoid checking aliases twice
        unique_flows = set(self._registry.values())
        for flow in unique_flows:
            score = flow.detect_confidence(text)
            if score > best_score:
                best_score = score
                best_flow = flow

        if best_flow and best_score > 0.1:
            return best_flow.process(text, current_state)

        # Default fallback to English flow
        fallback_flow = self.get_flow(self._default_language)
        if fallback_flow:
            return fallback_flow.process(text, current_state)

        return FlowResult(
            language="English",
            intent="unknown",
            confidence=0.0,
            next_action="ask_clarification",
            slots={},
            raw_text=text
        )


# Global singleton instance
language_registry = LanguageRegistry()
