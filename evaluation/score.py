"""
Language Quality Score Calculator.
Combines Intent Accuracy, WER, Flow Completion, and Latency into one final score (0-100).
"""

from typing import Any

from evaluation.config import EvaluationConfig


class LanguageQualityScore:

    def __init__(self, config: EvaluationConfig = None):
        self.config = config or EvaluationConfig()
        self.weights = self.config.weights

    def calculate(
        self,
        language: str,
        intent_accuracy: float,
        wer: float,
        flow_completion: float,
        avg_latency_ms: float
    ) -> dict[str, Any]:
        accuracy_score = intent_accuracy * 100.0
        wer_score = max(0.0, (1.0 - wer) * 100.0)
        completion_score = flow_completion * 100.0
        latency_score = max(0.0, 100.0 - (avg_latency_ms / 10.0))

        weighted_score = (
            accuracy_score * self.weights.accuracy_weight +
            wer_score * self.weights.wer_weight +
            completion_score * self.weights.flow_completion_weight +
            latency_score * self.weights.latency_weight
        )

        final_score = min(round(weighted_score, 1), 100.0)

        return {
            "language": language,
            "intent_accuracy_pct": round(intent_accuracy * 100.0, 1),
            "wer_pct": round(wer * 100.0, 1),
            "flow_completion_pct": round(flow_completion * 100.0, 1),
            "avg_latency_ms": round(avg_latency_ms, 2),
            "accuracy_score": round(accuracy_score, 1),
            "wer_score": round(wer_score, 1),
            "completion_score": round(completion_score, 1),
            "latency_score": round(latency_score, 1),
            "weights": {
                "accuracy": self.weights.accuracy_weight,
                "wer": self.weights.wer_weight,
                "completion": self.weights.flow_completion_weight,
                "latency": self.weights.latency_weight
            },
            "final_score": final_score
        }
