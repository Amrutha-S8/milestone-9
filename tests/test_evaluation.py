"""
Comprehensive unit tests for the StayZa Evaluation Engine.
Tests: Engine, WER, Latency, Language Score, Pass/Fail Logic, Reports, Evaluation APIs.
"""

import os

import pytest
from fastapi.testclient import TestClient

from datasets.loader import DatasetLoader
from evaluation.accuracy import IntentAccuracyEvaluator
from evaluation.completion import FLOW_SCENARIOS, FlowCompletionEvaluator
from evaluation.config import EvaluationConfig, EvaluationThresholds, ScoreWeights
from evaluation.engine import EvaluationEngine
from evaluation.latency import LatencyProfiler
from evaluation.reports import EvaluationReportGenerator
from evaluation.score import LanguageQualityScore
from evaluation.status import LanguageStatusEvaluator
from evaluation.wer import WEREvaluator
from languages.english.flow import EnglishLanguageFlow
from languages.hindi.flow import HindiLanguageFlow
from languages.registry import LanguageRegistry
from main import app

# ═════════════════════════════════════════════════════════════════════════════=
# TEST 1: Evaluation Config
# ═════════════════════════════════════════════════════════════════════════════=

class TestEvaluationConfig:
    def test_default_thresholds(self):
        config = EvaluationConfig()
        assert config.thresholds.accuracy_min == 0.95
        assert config.thresholds.wer_max == 0.05
        assert config.thresholds.flow_completion_min == 0.95
        assert config.thresholds.latency_max_ms == 500.0

    def test_custom_thresholds(self):
        thresholds = EvaluationThresholds(accuracy_min=0.90, wer_max=0.08)
        config = EvaluationConfig(thresholds=thresholds)
        assert config.thresholds.accuracy_min == 0.90
        assert config.thresholds.wer_max == 0.08

    def test_score_weights_default(self):
        config = EvaluationConfig()
        assert config.weights.accuracy_weight == 0.35
        assert config.weights.wer_weight == 0.25
        assert config.weights.flow_completion_weight == 0.25
        assert config.weights.latency_weight == 0.15

    def test_supported_languages(self):
        config = EvaluationConfig()
        assert "English" in config.supported_languages
        assert "Hindi" in config.supported_languages
        assert "Hinglish" in config.supported_languages
        assert "Telugu" in config.supported_languages
        assert "Marathi" in config.supported_languages
        assert "Malayalam" in config.supported_languages
        assert len(config.supported_languages) == 6

    def test_flow_scenarios(self):
        config = EvaluationConfig()
        expected = ("greeting", "booking", "availability", "price",
                    "cancellation", "modify_booking", "check_status", "goodbye")
        assert config.flow_scenarios == expected


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 2: WER Evaluator
# ═════════════════════════════════════════════════════════════════════════════=

class TestWEREvaluator:
    def test_exact_match(self):
        res = WEREvaluator.calculate("I want to book a room", "I want to book a room")
        assert res["wer"] == 0.0
        assert res["edit_distance"] == 0

    def test_with_substitution(self):
        res = WEREvaluator.calculate("I want to book a room", "I want to reserve a room")
        assert res["wer"] == 0.1667
        assert res["edit_distance"] == 1

    def test_with_deletion(self):
        res = WEREvaluator.calculate("I want to book a room", "I want to book room")
        assert res["wer"] == 0.1667
        assert res["edit_distance"] == 1

    def test_with_insertion(self):
        res = WEREvaluator.calculate("I want to book", "I want to book a room")
        assert res["wer"] == 0.5

    def test_empty_reference(self):
        res = WEREvaluator.calculate("", "hello world")
        assert res["wer"] == 1.0

    def test_both_empty(self):
        res = WEREvaluator.calculate("", "")
        assert res["wer"] == 0.0

    def test_completely_different(self):
        res = WEREvaluator.calculate("hello world", "goodbye")
        assert res["wer"] > 0.0
        assert res["edit_distance"] >= 2

    def test_multilingual_wer(self):
        res = WEREvaluator.calculate(
            "mujhe ek deluxe kamra book karna hai",
            "mujhe ek deluxe room book karna hai"
        )
        assert res["wer"] == 0.1667 or res["wer"] > 0

    def test_evaluate_all(self):
        ref_map = {"English": "hello world", "Hindi": "namaste duniya"}
        hyp_map = {"English": "hello world", "Hindi": "namaste world"}
        results = WEREvaluator.evaluate_all(ref_map, hyp_map)
        assert "per_language" in results
        assert results["per_language"]["English"]["wer"] == 0.0
        assert results["per_language"]["Hindi"]["wer"] > 0.0


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 3: Latency Profiler
# ═════════════════════════════════════════════════════════════════════════════=

class TestLatencyProfiler:
    def test_measure_basic(self):
        profiler = LatencyProfiler()

        def sample_func(a, b):
            return a + b

        res, timing = profiler.measure(sample_func, 10, 20)
        assert res == 30
        assert timing >= 0.0

    def test_get_stats(self):
        profiler = LatencyProfiler()

        def fast_func():
            return 1

        for _ in range(10):
            profiler.measure(fast_func)

        stats = profiler.get_stats()
        assert stats["count"] == 10
        assert stats["avg_ms"] >= 0.0
        assert stats["p50_ms"] >= 0.0
        assert stats["min_ms"] >= 0.0
        assert stats["max_ms"] >= 0.0

    def test_empty_stats(self):
        profiler = LatencyProfiler()
        stats = profiler.get_stats()
        assert stats["count"] == 0
        assert stats["avg_ms"] == 0.0

    def test_measure_language(self):
        profiler = LatencyProfiler()

        def fast_func():
            return 42

        res, _timing = profiler.measure_language(fast_func, "English")
        assert res == 42
        stats = profiler.get_language_stats()
        assert "English" in stats
        assert stats["English"]["count"] == 1

    def test_clear(self):
        profiler = LatencyProfiler()

        def f():
            return 1

        profiler.measure(f)
        assert profiler.get_stats()["count"] == 1
        profiler.clear()
        assert profiler.get_stats()["count"] == 0


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 4: Language Quality Score
# ═════════════════════════════════════════════════════════════════════════════=

class TestLanguageQualityScore:
    def test_perfect_score(self):
        calc = LanguageQualityScore()
        res = calc.calculate("English", intent_accuracy=1.0, wer=0.0, flow_completion=1.0, avg_latency_ms=50)
        assert res["final_score"] > 90.0

    def test_poor_score(self):
        calc = LanguageQualityScore()
        res = calc.calculate("English", intent_accuracy=0.3, wer=0.5, flow_completion=0.3, avg_latency_ms=2000)
        assert res["final_score"] < 50.0

    def test_score_components(self):
        calc = LanguageQualityScore()
        res = calc.calculate("Hindi", intent_accuracy=0.95, wer=0.03, flow_completion=0.98, avg_latency_ms=150)
        assert res["language"] == "Hindi"
        assert res["intent_accuracy_pct"] == 95.0
        assert res["wer_pct"] == 3.0
        assert res["flow_completion_pct"] == 98.0
        assert "accuracy_score" in res
        assert "wer_score" in res
        assert "completion_score" in res
        assert "latency_score" in res
        assert "weights" in res
        assert 0 <= res["final_score"] <= 100.0

    def test_score_cannot_exceed_100(self):
        calc = LanguageQualityScore()
        res = calc.calculate("English", intent_accuracy=1.5, wer=0.0, flow_completion=1.5, avg_latency_ms=0)
        assert res["final_score"] <= 100.0

    def test_custom_weights(self):
        weights = ScoreWeights(accuracy_weight=0.5, wer_weight=0.3, flow_completion_weight=0.1, latency_weight=0.1)
        config = EvaluationConfig(weights=weights)
        calc = LanguageQualityScore(config)
        res = calc.calculate("English", intent_accuracy=1.0, wer=0.0, flow_completion=1.0, avg_latency_ms=50)
        assert res["weights"]["accuracy"] == 0.5


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 5: Pass/Fail Logic
# ═════════════════════════════════════════════════════════════════════════════=

class TestLanguageStatusEvaluator:
    def test_pass(self):
        evaluator = LanguageStatusEvaluator()
        res = evaluator.evaluate("English", accuracy=0.98, wer=0.02, flow_completion=0.99, latency_ms=100)
        assert res["status"] == "PASS"
        assert res["enabled"] is True

    def test_fail(self):
        evaluator = LanguageStatusEvaluator()
        res = evaluator.evaluate("English", accuracy=0.50, wer=0.50, flow_completion=0.40, latency_ms=2000)
        assert res["status"] == "FAIL"
        assert res["enabled"] is False

    def test_warning_low_accuracy(self):
        evaluator = LanguageStatusEvaluator()
        res = evaluator.evaluate("English", accuracy=0.88, wer=0.02, flow_completion=0.99, latency_ms=100)
        assert res["status"] == "WARNING"

    def test_warning_high_latency(self):
        evaluator = LanguageStatusEvaluator()
        res = evaluator.evaluate("English", accuracy=0.98, wer=0.02, flow_completion=0.99, latency_ms=600)
        assert res["status"] == "WARNING"

    def test_edge_cases(self):
        evaluator = LanguageStatusEvaluator()
        res = evaluator.evaluate("English", accuracy=0.95, wer=0.05, flow_completion=0.95, latency_ms=500)
        assert res["status"] in ("PASS", "WARNING")

    def test_custom_thresholds(self):
        thresholds = EvaluationThresholds(
            accuracy_min=0.80, wer_max=0.15,
            flow_completion_min=0.85, latency_max_ms=500
        )
        config = EvaluationConfig(thresholds=thresholds)
        evaluator = LanguageStatusEvaluator(config)
        res = evaluator.evaluate("English", accuracy=0.82, wer=0.12, flow_completion=0.90, latency_ms=300)
        assert res["status"] == "PASS"

    def test_evaluate_all(self):
        evaluator = LanguageStatusEvaluator()
        scores = {
            "English": {"accuracy": 0.98, "wer": 0.02, "flow_completion": 0.99, "latency_ms": 100},
            "Hindi": {"accuracy": 0.80, "wer": 0.15, "flow_completion": 0.80, "latency_ms": 900},
        }
        results = evaluator.evaluate_all(scores)
        assert "per_language" in results
        assert results["per_language"]["English"]["status"] == "PASS"
        assert results["per_language"]["Hindi"]["status"] == "FAIL"


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 6: Evaluation Reports
# ═════════════════════════════════════════════════════════════════════════════=

class TestEvaluationReportGenerator:
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        self.test_reports_dir = "test_reports"
        self.generator = EvaluationReportGenerator(self.test_reports_dir)
        yield
        import shutil
        if os.path.exists(self.test_reports_dir):
            shutil.rmtree(self.test_reports_dir)

    def test_generate_report(self):
        engine_results = {
            "summary": {"total_languages_evaluated": 6},
            "per_language": {},
            "status": {"per_language": {}},
            "latency": {},
            "config": {}
        }
        report = self.generator.generate_report(engine_results, "test_report_001")
        assert report["report_id"] == "test_report_001"
        assert "timestamp" in report
        assert "summary" in report

    def test_save_and_load_report(self):
        engine_results = {
            "summary": {"total_languages_evaluated": 6},
            "per_language": {},
            "status": {"per_language": {}},
            "latency": {},
            "config": {}
        }
        report = self.generator.generate_report(engine_results, "test_save_001")
        path = self.generator.save_report(report)
        assert os.path.exists(path)

        loaded = self.generator.load_report("test_save_001")
        assert loaded is not None
        assert loaded["report_id"] == "test_save_001"

    def test_list_reports(self):
        engine_results = {
            "summary": {"total_languages_evaluated": 6},
            "per_language": {},
            "status": {"per_language": {}},
            "latency": {},
            "config": {}
        }
        r1 = self.generator.generate_report(engine_results, "report_a")
        r2 = self.generator.generate_report(engine_results, "report_b")
        self.generator.save_report(r1)
        self.generator.save_report(r2)
        reports = self.generator.list_reports()
        assert "report_a" in reports
        assert "report_b" in reports

    def test_load_nonexistent_report(self):
        loaded = self.generator.load_report("nonexistent")
        assert loaded is None

    def test_load_latest_report(self):
        engine_results = {
            "summary": {"total_languages_evaluated": 6},
            "per_language": {},
            "status": {"per_language": {}},
            "latency": {},
            "config": {}
        }
        r1 = self.generator.generate_report(engine_results, "report_001")
        r2 = self.generator.generate_report(engine_results, "report_002")
        self.generator.save_report(r1)
        self.generator.save_report(r2)
        latest = self.generator.load_latest_report()
        assert latest["report_id"] == "report_002"

    def test_empty_reports_dir(self):
        empty_gen = EvaluationReportGenerator("empty_test_reports")
        assert empty_gen.list_reports() == []
        import shutil
        if os.path.exists("empty_test_reports"):
            shutil.rmtree("empty_test_reports")


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 7: Flow Completion Scenarios
# ═════════════════════════════════════════════════════════════════════════════=

class TestFlowCompletionEvaluator:
    def test_all_scenarios_defined(self):
        expected_scenarios = [
            "greeting", "booking", "availability", "price",
            "cancellation", "modify_booking", "check_status", "goodbye"
        ]
        for s in expected_scenarios:
            assert s in FLOW_SCENARIOS, f"Missing scenario: {s}"
        assert len(FLOW_SCENARIOS) == 8

    def test_flow_scenario_structure(self):
        for data in FLOW_SCENARIOS.values():
            assert "turns" in data
            assert "expected_final_action" in data
            assert len(data["turns"]) > 0
            assert isinstance(data["expected_final_action"], str)

    def test_evaluate_language_completion(self):
        registry = LanguageRegistry()
        registry.register(EnglishLanguageFlow())

        evaluator = FlowCompletionEvaluator(registry)
        results = evaluator.evaluate_language("English")

        assert results["language"] == "English"
        assert results["total_scenarios"] == 8
        assert 0 <= results["completion_rate"] <= 1.0
        assert "scenarios" in results

    def test_evaluate_all_languages(self):
        registry = LanguageRegistry()
        registry.register(EnglishLanguageFlow())
        registry.register(HindiLanguageFlow())

        evaluator = FlowCompletionEvaluator(registry)
        results = evaluator.evaluate_all()

        assert "per_language" in results
        assert "English" in results["per_language"]
        assert "Hindi" in results["per_language"]


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 8: Intent Accuracy
# ═════════════════════════════════════════════════════════════════════════════=

class TestIntentAccuracyEvaluator:
    def test_evaluate_with_english_benchmark(self):
        registry = LanguageRegistry()
        registry.register(EnglishLanguageFlow())

        loader = DatasetLoader()
        items = [i for i in loader.load() if i.expected_language == "English"]

        evaluator = IntentAccuracyEvaluator(registry)
        results = evaluator.evaluate(items)

        assert results["total_samples"] > 0
        assert "intent_accuracy" in results
        assert "action_accuracy" in results
        assert "per_language" in results
        assert "details" in results

    def test_per_language_breakdown(self):
        registry = LanguageRegistry()
        registry.register(EnglishLanguageFlow())
        registry.register(HindiLanguageFlow())

        loader = DatasetLoader()
        items = loader.load()

        evaluator = IntentAccuracyEvaluator(registry)
        results = evaluator.evaluate(items)

        assert "per_language" in results
        for data in results["per_language"].values():
            assert "total" in data
            assert "correct" in data
            assert "accuracy" in data
            assert 0 <= data["accuracy"] <= 1.0

    def test_evaluate_language_specific(self):
        registry = LanguageRegistry()
        registry.register(HindiLanguageFlow())

        loader = DatasetLoader()
        items = loader.load()

        evaluator = IntentAccuracyEvaluator(registry)
        results = evaluator.evaluate_language(items, "Hindi")

        assert results["language"] == "Hindi"
        assert results["samples"] > 0
        assert 0 <= results["intent_accuracy"] <= 1.0

    def test_empty_items(self):
        registry = LanguageRegistry()
        evaluator = IntentAccuracyEvaluator(registry)
        results = evaluator.evaluate([])
        assert results["accuracy"] == 0.0
        assert results["total"] == 0


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 9: Evaluation Engine (Integration)
# ═════════════════════════════════════════════════════════════════════════════=

class TestEvaluationEngine:
    @pytest.fixture
    def engine(self):
        registry = LanguageRegistry()
        registry.register(EnglishLanguageFlow())
        registry.register(HindiLanguageFlow())
        config = EvaluationConfig()
        return EvaluationEngine(registry=registry, config=config)

    def test_engine_initialization(self, engine):
        assert engine.config is not None
        assert engine.accuracy_evaluator is not None
        assert engine.wer_evaluator is not None
        assert engine.latency_profiler is not None
        assert engine.completion_evaluator is not None
        assert engine.score_calculator is not None
        assert engine.status_evaluator is not None
        assert engine.report_generator is not None

    def test_get_language_status_before_run(self, engine):
        status = engine.get_language_status("English")
        assert status is None

    def test_full_evaluation(self, engine):
        results = engine.run_full_evaluation()

        assert "summary" in results
        assert "per_language" in results
        assert "status" in results
        assert "latency" in results
        assert "accuracy" in results
        assert "wer" in results
        assert "flow_completion" in results
        assert "config" in results
        assert "report_path" in results

        summary = results["summary"]
        assert summary["total_languages_evaluated"] > 0
        assert summary["total_samples"] > 0

    def test_per_language_scores(self, engine):
        results = engine.run_full_evaluation()
        scores = results["per_language"]

        for score_data in scores.values():
            assert "final_score" in score_data
            assert "intent_accuracy_pct" in score_data
            assert "wer_pct" in score_data
            assert "flow_completion_pct" in score_data
            assert "avg_latency_ms" in score_data
            assert 0 <= score_data["final_score"] <= 100.0

    def test_get_last_results(self, engine):
        assert engine.get_last_results() is None
        engine.run_full_evaluation()
        assert engine.get_last_results() is not None

    def test_get_language_status_after_run(self, engine):
        engine.run_full_evaluation()
        status = engine.get_language_status("English")
        assert status is not None
        assert status["language"] == "English"
        assert status["final_score"] > 0
        assert status["status"] in ("PASS", "WARNING", "FAIL")


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 10: Evaluation API Endpoints
# ═════════════════════════════════════════════════════════════════════════════=

class TestEvaluationAPI:
    client = TestClient(app)

    def test_evaluation_run_endpoint(self):
        response = self.client.post("/language/evaluation/run")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "per_language" in data
        assert "report_path" in data
        assert "status" in data

    def test_evaluation_results_endpoint(self):
        self.client.post("/language/evaluation/run")
        response = self.client.get("/language/evaluation/results")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "per_language" in data

    def test_languages_status_endpoint(self):
        self.client.post("/language/evaluation/run")
        response = self.client.get("/language/languages/status")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        for status_data in data.values():
            assert "language" in status_data
            assert "status" in status_data
            assert "enabled" in status_data
            assert "final_score" in status_data

    def test_evaluation_results_before_run(self):
        response = self.client.get("/language/evaluation/results")
        assert response.status_code == 200

    def test_languages_status_response_format(self):
        self.client.post("/language/evaluation/run")
        response = self.client.get("/language/languages/status")
        data = response.json()
        sample = next(iter(data.values()))
        assert "accuracy" in sample or "final_score" in sample


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 11: Edge Cases
# ═════════════════════════════════════════════════════════════════════════════=

class TestEdgeCases:
    def test_evaluate_with_empty_registry(self):
        registry = LanguageRegistry()
        evaluator = IntentAccuracyEvaluator(registry)
        loader = DatasetLoader()
        items = loader.load()
        results = evaluator.evaluate(items)
        # Should not crash, should produce results
        assert results["total_samples"] > 0

    def test_latency_with_noise(self):
        profiler = LatencyProfiler()

        import time
        def noisy_func():
            time.sleep(0.001)
            return 42

        res, timing = profiler.measure(noisy_func)
        assert res == 42
        assert timing >= 1.0

    def test_wer_case_insensitivity(self):
        res = WEREvaluator.calculate("HELLO WORLD", "hello world")
        assert res["wer"] == 0.0

    def test_score_with_zero_latency(self):
        calc = LanguageQualityScore()
        res = calc.calculate("English", intent_accuracy=1.0, wer=0.0, flow_completion=1.0, avg_latency_ms=0)
        assert res["final_score"] > 95.0

    def test_report_with_custom_dir(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = EvaluationReportGenerator(tmpdir)
            results = {
                "summary": {"total_languages_evaluated": 6},
                "per_language": {},
                "status": {"per_language": {}},
                "latency": {},
                "config": {}
            }
            report = gen.generate_report(results, "custom_report")
            path = gen.save_report(report)
            assert os.path.exists(path)


# ═════════════════════════════════════════════════════════════════════════════=
# TEST 12: Flow Scenarios Coverage
# ═════════════════════════════════════════════════════════════════════════════=

class TestFlowScenarios:
    def test_all_required_flows_exist(self):
        required = ["greeting", "booking", "availability", "price",
                    "cancellation", "modify_booking", "check_status", "goodbye"]
        for flow in required:
            assert flow in FLOW_SCENARIOS, f"Required flow '{flow}' not defined"

    def test_each_scenario_has_turns(self):
        for name, data in FLOW_SCENARIOS.items():
            assert len(data["turns"]) >= 2, f"Scenario {name} needs at least 2 turns"

    def test_greeting_flow(self):
        assert FLOW_SCENARIOS["greeting"]["expected_final_action"] == "ask_how_to_help"

    def test_goodbye_flow(self):
        assert FLOW_SCENARIOS["goodbye"]["expected_final_action"] == "end_conversation"

    def test_booking_flow(self):
        assert FLOW_SCENARIOS["booking"]["expected_final_action"] == "ask_checkin_date"

    def test_cancellation_flow(self):
        assert FLOW_SCENARIOS["cancellation"]["expected_final_action"] == "confirm_cancellation"
