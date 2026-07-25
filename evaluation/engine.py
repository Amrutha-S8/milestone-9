"""
Central Evaluation Engine for StayZa Milestone 9.
Orchestrates all evaluation metrics across all supported languages.
"""

import time
from typing import Dict, Any, Optional
from languages.registry import LanguageRegistry
from datasets.loader import DatasetLoader
from evaluation.config import EvaluationConfig
from evaluation.accuracy import IntentAccuracyEvaluator
from evaluation.wer import WEREvaluator
from evaluation.latency import LatencyProfiler
from evaluation.completion import FlowCompletionEvaluator
from evaluation.score import LanguageQualityScore
from evaluation.status import LanguageStatusEvaluator
from evaluation.reports import EvaluationReportGenerator


class EvaluationEngine:

    def __init__(
        self,
        registry: LanguageRegistry,
        config: Optional[EvaluationConfig] = None
    ):
        self.registry = registry
        self.config = config or EvaluationConfig()
        self.accuracy_evaluator = IntentAccuracyEvaluator(registry)
        self.wer_evaluator = WEREvaluator()
        self.latency_profiler = LatencyProfiler()
        self.completion_evaluator = FlowCompletionEvaluator(registry)
        self.score_calculator = LanguageQualityScore(self.config)
        self.status_evaluator = LanguageStatusEvaluator(self.config)
        self.report_generator = EvaluationReportGenerator(self.config.reports_dir)
        self.loader = DatasetLoader()
        self._last_results = None

    def run_full_evaluation(self) -> Dict[str, Any]:
        items = self.loader.load()

        accuracy_results = self.accuracy_evaluator.evaluate(items)
        wer_results = self.wer_evaluator.evaluate_all(
            self.config.wer_reference_sentences,
            self.config.wer_hypothesis_sentences
        )
        completion_results = self.completion_evaluator.evaluate_all()

        latency_results = self._profile_latency_per_language(items)

        per_language_data = self._build_per_language_data(
            accuracy_results, wer_results, completion_results, latency_results
        )

        scores = {}
        for lang in per_language_data:
            d = per_language_data[lang]
            scores[lang] = self.score_calculator.calculate(
                language=lang,
                intent_accuracy=d["accuracy"],
                wer=d["wer"],
                flow_completion=d["flow_completion"],
                avg_latency_ms=d["latency_ms"]
            )

        status_results = self.status_evaluator.evaluate_all(
            {
                lang: {
                    "accuracy": scores[lang]["intent_accuracy_pct"] / 100.0,
                    "wer": scores[lang]["wer_pct"] / 100.0,
                    "flow_completion": scores[lang]["flow_completion_pct"] / 100.0,
                    "latency_ms": scores[lang]["avg_latency_ms"]
                }
                for lang in scores
            }
        )

        summary = self._generate_summary(accuracy_results, wer_results, completion_results, scores, status_results)

        engine_results = {
            "summary": summary,
            "per_language": scores,
            "status": status_results,
            "latency": latency_results,
            "accuracy": accuracy_results,
            "wer": wer_results,
            "flow_completion": completion_results,
            "config": {
                "thresholds": {
                    "accuracy_min": self.config.thresholds.accuracy_min,
                    "wer_max": self.config.thresholds.wer_max,
                    "flow_completion_min": self.config.thresholds.flow_completion_min,
                    "latency_max_ms": self.config.thresholds.latency_max_ms
                },
                "weights": {
                    "accuracy": self.config.weights.accuracy_weight,
                    "wer": self.config.weights.wer_weight,
                    "completion": self.config.weights.flow_completion_weight,
                    "latency": self.config.weights.latency_weight
                }
            }
        }

        report = self.report_generator.generate_report(engine_results)
        saved_path = self.report_generator.save_report(report)
        engine_results["report_path"] = saved_path

        self._last_results = engine_results
        return engine_results

    def _profile_latency_per_language(self, items) -> Dict[str, Any]:
        per_language_times = {}
        for item in items:
            target_lang = item.expected_language or "English"
            start = time.perf_counter()
            self.registry.detect_and_process(item.text, target_language=target_lang)
            elapsed = (time.perf_counter() - start) * 1000
            if target_lang not in per_language_times:
                per_language_times[target_lang] = []
            per_language_times[target_lang].append(elapsed)

        results = {}
        for lang, times in per_language_times.items():
            if times:
                results[lang] = {
                    "avg_ms": round(sum(times) / len(times), 2),
                    "min_ms": round(min(times), 2),
                    "max_ms": round(max(times), 2),
                    "count": len(times)
                }
        return {"per_language": results}

    def _build_per_language_data(
        self, accuracy_results, wer_results, completion_results, latency_results
    ) -> Dict[str, Dict[str, float]]:
        data = {}
        all_langs = self.config.supported_languages

        for lang in all_langs:
            acc = 0.0
            if "per_language" in accuracy_results and lang in accuracy_results["per_language"]:
                acc = accuracy_results["per_language"][lang]["accuracy"]

            wer = 1.0
            if "per_language" in wer_results and lang in wer_results["per_language"]:
                wer = wer_results["per_language"][lang]["wer"]

            completion = 0.0
            if "per_language" in completion_results and lang in completion_results["per_language"]:
                completion = completion_results["per_language"][lang]["completion_rate"]

            lat = 9999.0
            if "per_language" in latency_results and lang in latency_results["per_language"]:
                lat = latency_results["per_language"][lang]["avg_ms"]

            data[lang] = {
                "accuracy": acc,
                "wer": wer,
                "flow_completion": completion,
                "latency_ms": lat
            }

        return data

    def _generate_summary(self, accuracy_results, wer_results, completion_results, scores, status_results) -> Dict[str, Any]:
        avg_accuracy = accuracy_results.get("intent_accuracy", 0.0)
        total_samples = accuracy_results.get("total_samples", 0)
        correct_intents = accuracy_results.get("correct_intents", 0)

        passed = sum(1 for s in status_results.get("per_language", {}).values() if s["status"] == "PASS")
        warned = sum(1 for s in status_results.get("per_language", {}).values() if s["status"] == "WARNING")
        failed = sum(1 for s in status_results.get("per_language", {}).values() if s["status"] == "FAIL")

        return {
            "total_languages_evaluated": len(self.config.supported_languages),
            "total_samples": total_samples,
            "correct_intents": correct_intents,
            "overall_accuracy": round(avg_accuracy, 4),
            "languages_passed": passed,
            "languages_warning": warned,
            "languages_failed": failed,
            "timestamp": __import__("time").time()
        }

    def get_last_results(self) -> Optional[Dict[str, Any]]:
        return self._last_results

    def get_language_status(self, language: str) -> Optional[Dict[str, Any]]:
        if self._last_results is None:
            return None
        status = self._last_results.get("status", {}).get("per_language", {})
        scores = self._last_results.get("per_language", {})
        if language not in status and language not in scores:
            return None

        score_data = scores.get(language, {})
        status_data = status.get(language, {})

        return {
            "language": language,
            "accuracy": score_data.get("intent_accuracy_pct", 0.0),
            "wer": score_data.get("wer_pct", 0.0),
            "flow_completion": score_data.get("flow_completion_pct", 0.0),
            "latency": score_data.get("avg_latency_ms", 0.0),
            "final_score": score_data.get("final_score", 0.0),
            "status": status_data.get("status", "UNKNOWN"),
            "enabled": status_data.get("enabled", False)
        }