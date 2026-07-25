"""
Flow Completion Evaluator for multi-turn hotel conversation scenarios.
Evaluates all 8 scenarios: greeting, booking, availability, price, cancellation, modify_booking, check_status, goodbye.
"""

from typing import Any

from languages.registry import LanguageRegistry

FLOW_SCENARIOS = {
    "greeting": {
        "turns": ["Hello", "Hi there"],
        "expected_final_action": "ask_how_to_help"
    },
    "booking": {
        "turns": ["I want to book a room", "tomorrow", "2 guests", "deluxe"],
        "expected_final_action": "ask_checkin_date"
    },
    "availability": {
        "turns": ["Are there any rooms available", "tomorrow"],
        "expected_final_action": "ask_stay_dates"
    },
    "price": {
        "turns": ["How much is a room per night", "deluxe suite"],
        "expected_final_action": "provide_rate_card"
    },
    "cancellation": {
        "turns": ["I want to cancel my reservation", "booking id is 12345"],
        "expected_final_action": "confirm_cancellation"
    },
    "modify_booking": {
        "turns": ["I want to modify my booking", "change date to tomorrow"],
        "expected_final_action": "ask_modification_details"
    },
    "check_status": {
        "turns": ["What is my booking status", "booking id 12345"],
        "expected_final_action": "provide_booking_status"
    },
    "goodbye": {
        "turns": ["Goodbye", "Thank you"],
        "expected_final_action": "end_conversation"
    }
}


class FlowCompletionEvaluator:

    def __init__(self, registry: LanguageRegistry):
        self.registry = registry

    def evaluate_dialog_scenario(self, language: str, turns: list[str], expected_final_action: str) -> dict[str, Any]:
        current_state = None
        actions_taken = []

        for utterance in turns:
            res = self.registry.detect_and_process(
                utterance, target_language=language, current_state=current_state
            )
            actions_taken.append(res.next_action)
            current_state = res.next_action

        completed = (actions_taken[-1] == expected_final_action) if actions_taken else False

        return {
            "completed": completed,
            "turns_count": len(turns),
            "expected_final_action": expected_final_action,
            "actual_final_action": actions_taken[-1] if actions_taken else None,
            "flow_path": actions_taken
        }

    def evaluate_language(self, language: str) -> dict[str, Any]:
        scenario_results = {}
        completed_count = 0
        total_scenarios = len(FLOW_SCENARIOS)

        for scenario_name, scenario_data in FLOW_SCENARIOS.items():
            result = self.evaluate_dialog_scenario(
                language=language,
                turns=scenario_data["turns"],
                expected_final_action=scenario_data["expected_final_action"]
            )
            scenario_results[scenario_name] = result
            if result["completed"]:
                completed_count += 1

        completion_rate = round(completed_count / total_scenarios, 4) if total_scenarios > 0 else 0.0

        return {
            "language": language,
            "completion_rate": completion_rate,
            "completed_scenarios": completed_count,
            "total_scenarios": total_scenarios,
            "scenarios": scenario_results
        }

    def evaluate_all(self) -> dict[str, Any]:
        languages = sorted({
            flow.language_name for flow in self.registry._registry.values()
        })
        all_results = {}
        for lang in languages:
            all_results[lang] = self.evaluate_language(lang)
        return {"per_language": all_results}
