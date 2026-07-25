"""
Configuration for StayZa Evaluation Engine.

All thresholds are configurable. Extend this file to add new metrics.
"""

from dataclasses import dataclass, field


@dataclass
class EvaluationThresholds:
    accuracy_min: float = 0.95
    wer_max: float = 0.05
    flow_completion_min: float = 0.95
    latency_max_ms: float = 500.0
    accuracy_warning_min: float = 0.85
    wer_warning_max: float = 0.10
    flow_completion_warning_min: float = 0.85
    latency_warning_max_ms: float = 800.0


@dataclass
class ScoreWeights:
    accuracy_weight: float = 0.35
    wer_weight: float = 0.25
    flow_completion_weight: float = 0.25
    latency_weight: float = 0.15


@dataclass
class EvaluationConfig:
    thresholds: EvaluationThresholds = field(default_factory=EvaluationThresholds)
    weights: ScoreWeights = field(default_factory=ScoreWeights)
    supported_languages: tuple = (
        "English", "Hindi", "Hinglish",
        "Telugu", "Marathi", "Malayalam"
    )
    flow_scenarios: tuple = (
        "greeting", "booking", "availability", "price",
        "cancellation", "modify_booking", "check_status", "goodbye"
    )
    reports_dir: str = "reports"
    wer_reference_sentences: dict[str, str] = field(default_factory=lambda: {
        "English": "I want to book a deluxe room for two guests tomorrow morning",
        "Hindi": "mujhe ek deluxe kamra do guest ke liye kal subah book karna hai",
        "Hinglish": "mujhe ek deluxe room do guests ke liye kal subah book karna hai",
        "Telugu": "naaku oka deluxe room rendu athithulaku repu podduna kavali",
        "Marathi": "mala ek deluxe room dona pahunakarita udya sakali book karaycha ahe",
        "Malayalam": "enikku oru deluxe room randu athithikalkku naale ravile venam",
    })
    wer_hypothesis_sentences: dict[str, str] = field(default_factory=lambda: {
        "English": "I want to book a deluxe room for two guests tomorrow morning",
        "Hindi": "mujhe ek deluxe kamra do guest ke liye kal subah book karna hai",
        "Hinglish": "mujhe ek deluxe room do guest ke liye kal subah karna hai",
        "Telugu": "naaku oka deluxe room rendu athithulaku repu podduna kavali",
        "Marathi": "mala ek deluxe room don pahunakarita udya sakali book karaycha ahe",
        "Malayalam": "enikku oru deluxe room randu athithikalkku naale ravile venam",
    })
