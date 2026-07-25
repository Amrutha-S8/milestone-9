"""
JSON Report Generator for Evaluation Results.
Stores structured evaluation reports in a reports directory.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional


class EvaluationReportGenerator:

    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        self._ensure_reports_dir()

    def _ensure_reports_dir(self) -> None:
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_report(
        self,
        engine_results: Dict[str, Any],
        report_name: Optional[str] = None
    ) -> Dict[str, Any]:
        now = datetime.now(timezone.utc)
        timestamp = now.isoformat()
        report = {
            "report_id": report_name or f"eval_{now.strftime('%Y%m%d_%H%M%S')}",
            "timestamp": timestamp,
            "engine_version": "1.0.0",
            "summary": engine_results.get("summary", {}),
            "per_language": engine_results.get("per_language", {}),
            "status": engine_results.get("status", {}),
            "latency": engine_results.get("latency", {}),
            "config": engine_results.get("config", {})
        }
        return report

    def save_report(self, report: Dict[str, Any]) -> str:
        filename = f"{report['report_id']}.json"
        filepath = os.path.join(self.reports_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return filepath

    def load_report(self, report_id: str) -> Optional[Dict[str, Any]]:
        filepath = os.path.join(self.reports_dir, f"{report_id}.json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_reports(self) -> list:
        if not os.path.exists(self.reports_dir):
            return []
        reports = []
        for fname in sorted(os.listdir(self.reports_dir), reverse=True):
            if fname.endswith(".json"):
                reports.append(fname.replace(".json", ""))
        return reports

    def load_latest_report(self) -> Optional[Dict[str, Any]]:
        reports = self.list_reports()
        if not reports:
            return None
        return self.load_report(reports[0])