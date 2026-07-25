"""
JSON Report Generator for Evaluation Results.
Stores structured evaluation reports in a reports directory.
"""

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class EvaluationReportGenerator:

    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = reports_dir
        self._ensure_reports_dir()

    def _ensure_reports_dir(self) -> None:
        Path(self.reports_dir).mkdir(parents=True, exist_ok=True)

    def generate_report(
        self,
        engine_results: dict[str, Any],
        report_name: str | None = None
    ) -> dict[str, Any]:
        now = datetime.now(UTC)
        timestamp = now.isoformat()
        return {
            "report_id": report_name or f"eval_{now.strftime('%Y%m%d_%H%M%S')}",
            "timestamp": timestamp,
            "engine_version": "1.0.0",
            "summary": engine_results.get("summary", {}),
            "per_language": engine_results.get("per_language", {}),
            "status": engine_results.get("status", {}),
            "latency": engine_results.get("latency", {}),
            "config": engine_results.get("config", {})
        }

    def save_report(self, report: dict[str, Any]) -> str:
        filename = f"{report['report_id']}.json"
        filepath = Path(self.reports_dir) / filename
        with filepath.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return str(filepath)

    def load_report(self, report_id: str) -> dict[str, Any] | None:
        filepath = Path(self.reports_dir) / f"{report_id}.json"
        if not filepath.exists():
            return None
        with filepath.open(encoding="utf-8") as f:
            return json.load(f)

    def list_reports(self) -> list:
        reports_dir = Path(self.reports_dir)
        if not reports_dir.exists():
            return []
        return [fpath.stem for fpath in sorted(reports_dir.iterdir(), reverse=True) if fpath.suffix == ".json"]

    def load_latest_report(self) -> dict[str, Any] | None:
        reports = self.list_reports()
        if not reports:
            return None
        return self.load_report(reports[0])
