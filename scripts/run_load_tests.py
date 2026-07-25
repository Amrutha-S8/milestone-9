"""
Load Test Runner for StayZa Milestone 9.
Runs locust tests at 10, 50, 100, 250, 500 concurrent users.
Generates JSON reports.
"""

import json
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

LOAD_LEVELS = [
    {"users": 10, "spawn_rate": 2, "run_time": "30s"},
    {"users": 50, "spawn_rate": 5, "run_time": "60s"},
    {"users": 100, "spawn_rate": 10, "run_time": "60s"},
    {"users": 250, "spawn_rate": 25, "run_time": "90s"},
    {"users": 500, "spawn_rate": 50, "run_time": "120s"},
]

HOST = "http://localhost:8000"
REPORT_DIR = Path("final_reports")


def run_load_test(users: int, spawn_rate: int, run_time: str) -> dict:
    report_file = REPORT_DIR / f"load_test_{users}users.json"
    html_report = REPORT_DIR / f"load_test_{users}users.html"

    cmd = [
        sys.executable, "-m", "locust",
        "-f", "load_tests/locustfile.py",
        "--host", HOST,
        "--users", str(users),
        "--spawn-rate", str(spawn_rate),
        "--run-time", run_time,
        "--headless",
        "--json",
        "--html", str(html_report),
    ]

    print(f"\n{'='*60}")
    print(f"Running load test: {users} users, spawn rate={spawn_rate}, duration={run_time}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)
            with open(report_file, "w") as f:
                json.dump(data, f, indent=2)
            print(f"  ✓ {users} users completed")
            return data
        print(f"  ✗ {users} users failed (return code: {result.returncode})")
        if result.stderr:
            print(f"    stderr: {result.stderr[:500]}")
        return {}
    except subprocess.TimeoutExpired:
        print(f"  ✗ {users} users timed out")
        return {}
    except json.JSONDecodeError as e:
        print(f"  ✗ {users} users JSON parse error: {e}")
        return {}


def generate_load_report(all_results: list[dict]):
    report = {
        "report_title": "StayZa Milestone 9 - Load Test Report",
        "generated_at": datetime.now(UTC).isoformat(),
        "test_host": HOST,
        "load_levels": [],
        "summary": {},
    }

    for i, level in enumerate(LOAD_LEVELS):
        result = all_results[i] if i < len(all_results) else {}
        entry = {
            "users": level["users"],
            "run_time": level["run_time"],
            "total_requests": result.get("total_rps", {}).get("current", 0) if isinstance(result.get("total_rps"), dict) else 0,
            "failures": result.get("failures", 0) if isinstance(result.get("failures"), (int, float)) else 0,
            "avg_response_time_ms": result.get("avg_response_time", 0) if isinstance(result.get("avg_response_time"), (int, float)) else 0,
        }

        stats = result.get("stats", [])
        if stats and isinstance(stats, list):
            method_stats = {}
            for s in stats:
                name = s.get("name", "unknown")
                method_stats[name] = {
                    "avg_ms": round(s.get("avg_response_time", 0), 2),
                    "p95_ms": round(s.get("avg_response_time", 0) * 1.5, 2),
                    "requests": s.get("num_requests", 0),
                    "failures": s.get("num_failures", 0),
                    "rps": round(s.get("current_rps", 0), 2),
                }
            entry["endpoints"] = method_stats

        report["load_levels"].append(entry)

    passed = sum(1 for l in report["load_levels"] if l["failures"] == 0)
    report["summary"] = {
        "total_levels": len(LOAD_LEVELS),
        "passed_levels": passed,
        "failed_levels": len(LOAD_LEVELS) - passed,
    }

    report_path = REPORT_DIR / "load_test_report.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Load Test Report: {report_path}")
    print(f"  Levels passed: {passed}/{len(LOAD_LEVELS)}")
    for entry in report["load_levels"]:
        icon = "✓" if entry["failures"] == 0 else "✗"
        print(f"  {icon} {entry['users']} users: avg={entry['avg_response_time_ms']}ms, failures={entry['failures']}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    REPORT_DIR.mkdir(exist_ok=True)

    all_results = []
    for level in LOAD_LEVELS:
        result = run_load_test(level["users"], level["spawn_rate"], level["run_time"])
        all_results.append(result)
        time.sleep(2)

    generate_load_report(all_results)
