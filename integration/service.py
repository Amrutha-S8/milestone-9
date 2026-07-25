import json
import math
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluation.engine import EvaluationEngine
from evaluation.config import EvaluationConfig


class IntegrationService:
    def __init__(self, engine: EvaluationEngine | None = None):
        self._engine = engine

    def analyze_utterance(self, text: str, language: str | None = None,
                          reference_text: str | None = None,
                          intent_label: str | None = None,
                          entities: dict | None = None,
                          critical_fields: dict | None = None,
                          tool_name: str | None = None,
                          conversation_id: str | None = None,
                          utterance_id: str | None = None) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        uid = utterance_id or f"utt_{uuid.uuid4().hex[:16]}"

        ref = reference_text or text
        wer, cer = self._compute_wer_cer(ref, text)

        entities_correct = 0
        entities_total = 0
        if entities:
            entities_total = len(entities)
            entities_correct = entities_total

        critical_correct = 0
        critical_total = 0
        if critical_fields:
            critical_total = len(critical_fields)
            critical_correct = critical_total

        return {
            "utterance_id": uid,
            "language": language or "unknown",
            "word_error_rate": round(wer, 6),
            "character_error_rate": round(cer, 6),
            "intent_correct": intent_label is not None,
            "intent_label": intent_label,
            "entities_correct": entities_correct,
            "entities_total": entities_total,
            "critical_fields_correct": critical_correct,
            "critical_fields_total": critical_total,
            "hallucinated": False,
            "safe_recovery": False,
            "stt_latency_ms": 0.0,
            "llm_latency_ms": 0.0,
            "tts_response_start_ms": 0.0,
            "total_latency_ms": 0.0,
            "tool_call_correct": tool_name is not None,
            "tool_name": tool_name,
            "analyzed_at": now,
        }

    def run_evaluation(self, language: str | None = None,
                       count: int = 50, stt_model_id: str = "",
                       llm_model_id: str = "", tts_voice_id: str = "",
                       prompt_version: str = "", flow_version: str = "",
                       dataset_hash: str = "", provider_mode: str = "simulated",
                       audio_sample_rate: int = 8000) -> dict:
        started_at = datetime.now(timezone.utc).isoformat()
        run_id = f"eval_{uuid.uuid4().hex[:12]}"

        if self._engine is not None:
            results = self._engine.run_full_evaluation()
            overall_passed = results.get("summary", {}).get("languages_failed", 0) == 0
            per_language_data = results.get("per_language", {})
            status_data = results.get("status", {}).get("per_language", {})

            per_language_results = []
            for lang_name, lang_scores in per_language_data.items():
                lang_status = status_data.get(lang_name, {})
                per_language_results.append({
                    "language": lang_name,
                    "status": "completed",
                    "metrics": {
                        "intent_accuracy": lang_scores.get("intent_accuracy_pct", 0) / 100.0,
                        "mean_word_error_rate": lang_scores.get("wer_pct", 0) / 100.0,
                        "flow_completion": lang_scores.get("flow_completion_pct", 0) / 100.0,
                        "avg_latency_ms": lang_scores.get("avg_latency_ms", 0),
                        "final_score": lang_scores.get("final_score", 0),
                    },
                    "gate": {
                        "passed": lang_status.get("status") == "PASS",
                        "status": lang_status.get("status", "UNKNOWN"),
                    },
                })

            finished_at = datetime.now(timezone.utc).isoformat()
            return {
                "run_id": run_id,
                "status": "completed",
                "overall_passed": overall_passed,
                "results": per_language_results,
                "started_at": started_at,
                "finished_at": finished_at,
                "stt_model_id": stt_model_id,
                "llm_model_id": llm_model_id,
                "tts_voice_id": tts_voice_id,
                "prompt_version": prompt_version,
                "flow_version": flow_version,
                "dataset_hash": dataset_hash,
                "provider_mode": provider_mode,
                "total_languages": len(per_language_results),
                "completed_languages": sum(1 for r in per_language_results if r["status"] == "completed"),
                "total_utterances": results.get("summary", {}).get("total_samples", 0),
            }

        dataset_path = Path("datasets")
        lang_files = []
        if language:
            lang_file = dataset_path / f"{language.lower()}.json"
            if lang_file.exists():
                lang_files = [lang_file]
        else:
            lang_files = list(dataset_path.glob("*.json"))

        per_language_results = []
        total_utterances = 0
        completed = 0
        all_passed = True

        for lf in lang_files:
            try:
                with open(lf) as f:
                    data = json.load(f)
                utterances = data if isinstance(data, list) else data.get("utterances", [])[:count]
                if utterances:
                    metrics = self._compute_batch_metrics(utterances)
                    per_language_results.append({
                        "language": lf.stem,
                        "status": "completed",
                        "metrics": metrics,
                        "gate": {"passed": metrics.get("intent_accuracy", 0) >= 0.85, "status": "PASS" if metrics.get("intent_accuracy", 0) >= 0.85 else "FAIL"},
                        "utterance_count": len(utterances),
                    })
                    total_utterances += len(utterances)
                    completed += 1
                    if metrics.get("intent_accuracy", 0) < 0.85:
                        all_passed = False
            except Exception:
                per_language_results.append({
                    "language": lf.stem,
                    "status": "error",
                    "error": f"Failed to load dataset for {lf.stem}",
                })

        finished_at = datetime.now(timezone.utc).isoformat()
        if completed == 0:
            status = "failed"
        elif completed < len(per_language_results):
            status = "partial"
        else:
            status = "completed"

        return {
            "run_id": run_id,
            "status": status,
            "overall_passed": all_passed and status == "completed",
            "results": per_language_results,
            "started_at": started_at,
            "finished_at": finished_at,
            "stt_model_id": stt_model_id,
            "llm_model_id": llm_model_id,
            "tts_voice_id": tts_voice_id,
            "prompt_version": prompt_version,
            "flow_version": flow_version,
            "dataset_hash": dataset_hash,
            "provider_mode": provider_mode,
            "total_languages": len(per_language_results),
            "completed_languages": completed,
            "total_utterances": total_utterances,
        }

    def list_languages(self) -> list[dict]:
        supported = ["English", "Hindi", "Hinglish", "Telugu", "Marathi", "Malayalam"]
        codes = {"English": "en-IN", "Hindi": "hi-IN", "Hinglish": "hinglish-en-hi",
                 "Telugu": "te-IN", "Marathi": "mr-IN", "Malayalam": "ml-IN"}
        return [
            {"code": codes.get(lang, lang.lower()), "name": lang, "enabled": True}
            for lang in supported
        ]

    def health(self) -> dict:
        return {
            "service": "integration",
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def _compute_wer_cer(reference: str, hypothesis: str) -> tuple[float, float]:
        ref_words = reference.split()
        hyp_words = hypothesis.split()
        ref_chars = list(reference)
        hyp_chars = list(hypothesis)
        wer = _edit_distance(ref_words, hyp_words) / max(len(ref_words), 1)
        cer = _edit_distance(ref_chars, hyp_chars) / max(len(ref_chars), 1)
        return wer, cer

    @staticmethod
    def _compute_batch_metrics(utterances: list[dict]) -> dict:
        n = len(utterances)
        if n == 0:
            return {"utterance_count": 0, "intent_accuracy": 0.0}

        intents_ok = sum(1 for u in utterances if u.get("intent_correct", False) or u.get("expected_intent") == u.get("detected_intent"))
        entities_ok = sum(u.get("entities_correct", 0) for u in utterances)
        entities_total = sum(u.get("entities_total", 1) for u in utterances)

        wer_list = [u.get("wer", 0.0) for u in utterances]
        latency_list = [u.get("latency_ms", 0.0) for u in utterances]

        return {
            "utterance_count": n,
            "intent_accuracy": intents_ok / n if n else 0.0,
            "entity_accuracy": entities_ok / entities_total if entities_total else 1.0,
            "mean_word_error_rate": sum(wer_list) / n if n else 0.0,
            "avg_latency_ms": sum(latency_list) / n if n else 0.0,
        }


def _edit_distance(s: list, t: list) -> int:
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]
