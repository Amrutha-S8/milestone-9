"""
Intent Accuracy & Classification Metrics Evaluator.
Calculates per-language and overall intent accuracy.
"""

from collections.abc import Sequence
from typing import Any

from datasets.loader import BenchmarkItem
from languages.registry import LanguageRegistry


class IntentAccuracyEvaluator:
    """Evaluates classification accuracy per language and overall."""

    def __init__(self, registry: LanguageRegistry):
        self.registry = registry

    def evaluate(self, items: Sequence[BenchmarkItem]) -> dict[str, Any]:
        total = len(items)
        if total == 0:
            return {"accuracy": 0.0, "total": 0, "correct": 0, "per_language": {}}

        correct_intents = 0
        correct_actions = 0
        results_breakdown = []
        per_lang_correct: dict[str, int] = {}
        per_lang_total: dict[str, int] = {}

        for item in items:
            expected_intent = item.get_intent()
            expected_action = item.get_expected_action()
            target_lang = item.expected_language or "English"

            res = self.registry.detect_and_process(item.text, target_language=target_lang)

            intent_match = (res.intent == expected_intent)
            action_match = (res.next_action == expected_action)

            if intent_match:
                correct_intents += 1
            if action_match:
                correct_actions += 1

            per_lang_correct.setdefault(target_lang, 0)
            per_lang_total.setdefault(target_lang, 0)
            per_lang_total[target_lang] += 1
            if intent_match:
                per_lang_correct[target_lang] += 1

            results_breakdown.append({
                "id": item.id,
                "text": item.text,
                "language": target_lang,
                "expected_intent": expected_intent,
                "predicted_intent": res.intent,
                "intent_match": intent_match,
                "expected_action": expected_action,
                "predicted_next_action": res.next_action,
                "confidence": res.confidence
            })

        accuracy = round(correct_intents / total, 4)
        action_accuracy = round(correct_actions / total, 4)

        per_language = {}
        for lang in sorted(per_lang_total.keys()):
            per_language[lang] = {
                "total": per_lang_total[lang],
                "correct": per_lang_correct.get(lang, 0),
                "accuracy": round(per_lang_correct.get(lang, 0) / per_lang_total[lang], 4)
            }

        return {
            "total_samples": total,
            "intent_accuracy": accuracy,
            "action_accuracy": action_accuracy,
            "correct_intents": correct_intents,
            "correct_actions": correct_actions,
            "per_language": per_language,
            "details": results_breakdown
        }

    def evaluate_language(self, items: Sequence[BenchmarkItem], language: str) -> dict[str, Any]:
        filtered = [i for i in items if (i.expected_language or "English") == language]
        result = self.evaluate(filtered)
        return {
            "language": language,
            "samples": result["total_samples"],
            "intent_accuracy": result["intent_accuracy"],
            "action_accuracy": result["action_accuracy"],
            "correct_intents": result["correct_intents"],
            "correct_actions": result["correct_actions"]
        }
