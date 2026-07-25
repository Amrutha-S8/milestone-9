"""
Language Pass/Fail/WARNING Status System.
Automatically determines language enablement status based on configurable thresholds.
"""

from typing import Any

from evaluation.config import EvaluationConfig


class LanguageStatusEvaluator:

    def __init__(self, config: EvaluationConfig = None):
        self.config = config or EvaluationConfig()
        self.thresholds = self.config.thresholds

    def evaluate(
        self,
        language: str,
        accuracy: float,
        wer: float,
        flow_completion: float,
        latency_ms: float
    ) -> dict[str, Any]:
        threshold_checks = {
            "accuracy": {
                "value": accuracy,
                "pass_min": self.thresholds.accuracy_min,
                "warning_min": self.thresholds.accuracy_warning_min,
                "pass": accuracy >= self.thresholds.accuracy_min,
                "warning": accuracy >= self.thresholds.accuracy_warning_min
            },
            "wer": {
                "value": wer,
                "pass_max": self.thresholds.wer_max,
                "warning_max": self.thresholds.wer_warning_max,
                "pass": wer <= self.thresholds.wer_max,
                "warning": wer <= self.thresholds.wer_warning_max
            },
            "flow_completion": {
                "value": flow_completion,
                "pass_min": self.thresholds.flow_completion_min,
                "warning_min": self.thresholds.flow_completion_warning_min,
                "pass": flow_completion >= self.thresholds.flow_completion_min,
                "warning": flow_completion >= self.thresholds.flow_completion_warning_min
            },
            "latency": {
                "value": latency_ms,
                "pass_max": self.thresholds.latency_max_ms,
                "warning_max": self.thresholds.latency_warning_max_ms,
                "pass": latency_ms <= self.thresholds.latency_max_ms,
                "warning": latency_ms <= self.thresholds.latency_warning_max_ms
            }
        }

        all_pass = all(check["pass"] for check in threshold_checks.values())
        any_warning_or_pass = all(
            check["pass"] or check["warning"] for check in threshold_checks.values()
        )

        if all_pass:
            status = "PASS"
        elif any_warning_or_pass:
            status = "WARNING"
        else:
            status = "FAIL"

        return {
            "language": language,
            "status": status,
            "enabled": status == "PASS",
            "accuracy_pct": round(accuracy * 100.0, 1),
            "wer_pct": round(wer * 100.0, 1),
            "flow_completion_pct": round(flow_completion * 100.0, 1),
            "latency_ms": round(latency_ms, 2),
            "thresholds": {
                "accuracy_min_pct": self.thresholds.accuracy_min * 100.0,
                "wer_max_pct": self.thresholds.wer_max * 100.0,
                "flow_completion_min_pct": self.thresholds.flow_completion_min * 100.0,
                "latency_max_ms": self.thresholds.latency_max_ms
            },
            "threshold_checks": threshold_checks
        }

    def evaluate_all(self, per_language_scores: dict[str, dict[str, Any]]) -> dict[str, Any]:
        results = {}
        for lang, scores in per_language_scores.items():
            results[lang] = self.evaluate(
                language=lang,
                accuracy=scores.get("accuracy", 0.0),
                wer=scores.get("wer", 1.0),
                flow_completion=scores.get("flow_completion", 0.0),
                latency_ms=scores.get("latency_ms", 9999.0)
            )
        return {"per_language": results}
