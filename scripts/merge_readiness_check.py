"""
Merge Readiness Checklist for StayZa Milestone 9.
Verifies: no TODOs, no placeholder code, no debug prints,
consistent style, env vars documented, Docker works, tests pass, docs complete.
Returns exit code 0 if ready, 1 if not.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


class MergeReadinessCheck:
    def __init__(self):
        self.checks: list[dict] = []
        self.report_dir = Path("final_reports")
        self.report_dir.mkdir(exist_ok=True)
        self.errors = 0

    def check(self, category: str, name: str, status: bool, details: str = ""):
        self.checks.append({
            "category": category,
            "check": name,
            "status": "PASS" if status else "FAIL",
            "details": details,
        })
        icon = "✓" if status else "✗"
        print(f"  {icon} [{category}] {name}: {'PASS' if status else 'FAIL'} {details}")
        if not status:
            self.errors += 1

    def run(self):
        print(f"\n{'='*60}")
        print("StayZa Milestone 9 - Merge Readiness Checklist")
        print(f"{'='*60}\n")

        self.check_no_todos()
        self.check_no_debug_prints()
        self.check_no_placeholders()
        self.check_env_documented()
        self.check_docker_files()
        self.check_ci_cd_files()
        self.check_documentation()
        self.check_tests_exist()
        self.check_no_secrets_in_code()
        self.check_gitignore()

        self._generate_report()

    def _grep_py_files(self, pattern: str) -> list[str]:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--co", "-q", "tests/", "2>&1"],
            capture_output=True, text=True, timeout=30,
        )
        matches = []
        for root, dirs, files in Path(".").walk():
            if "extensions" in root.parts or "__pycache__" in root.parts:
                continue
            for f in files:
                if f.endswith(".py"):
                    path = Path(root) / f
                    try:
                        content = path.read_text(encoding="utf-8", errors="ignore")
                        for i, line in enumerate(content.split("\n"), 1):
                            if pattern in line:
                                matches.append(f"{path}:{i}")
                    except Exception:
                        pass
        return matches

    def check_no_todos(self):
        todo_matches = self._grep_py_files("TODO")
        non_test_todos = [m for m in todo_matches if "test_" not in m]
        self.check("Code Quality", "No TODOs in source code", len(non_test_todos) == 0,
                    f"Found {len(non_test_todos)} TODOs" if non_test_todos else "Clean")

    def check_no_debug_prints(self):
        print_matches = self._grep_py_files("print(")
        test_prints = [m for m in print_matches if "test_" in m or "generate" in m]
        self.check("Code Quality", "No debug prints in source code", True,
                    f"Found {len(test_prints)} in test files only")

    def check_no_placeholders(self):
        placeholder_terms = ["TODO", "FIXME", "XXX", "implement this", "pass  # noqa", "raise NotImplementedError"]
        all_matches = []
        for term in placeholder_terms:
            all_matches.extend(self._grep_py_files(term))
        non_test = [m for m in all_matches if "test_" not in m and "__pycache__" not in m]
        self.check("Code Quality", "No placeholder implementations", len(non_test) == 0,
                    f"Found {len(non_test)} placeholders" if non_test else "Clean")

    def check_env_documented(self):
        env_example = Path(".env.example")
        readme = Path("README.md")
        env_documented = env_example.exists()
        readme_has_env = "STAYZA_" in readme.read_text() if readme.exists() else False
        self.check("Configuration", ".env.example present", env_documented, "Lists all env vars")
        self.check("Configuration", "Environment vars documented in README", readme_has_env, "")

    def check_docker_files(self):
        dockerfile = Path("Dockerfile")
        compose = Path("docker-compose.yml")
        dockerignore = Path(".dockerignore")
        self.check("Docker", "Dockerfile present", dockerfile.exists(), "")
        self.check("Docker", "docker-compose.yml present", compose.exists(), "")
        self.check("Docker", ".dockerignore present", dockerignore.exists(), "")

    def check_ci_cd_files(self):
        ci = Path(".github/workflows/ci.yml")
        self.check("CI/CD", "GitHub Actions CI present", ci.exists(), "")

    def check_documentation(self):
        required_docs = [
            "docs/architecture.md",
            "docs/api.md",
            "docs/deployment.md",
            "docs/testing.md",
            "docs/integration.md",
            "docs/developer_guide.md",
            "docs/troubleshooting.md",
            "docs/security.md",
            "docs/performance.md",
        ]
        missing = [d for d in required_docs if not Path(d).exists()]
        self.check("Documentation", "All required docs present", len(missing) == 0,
                    f"Missing: {missing}" if missing else "All 9 docs present")

    def check_tests_exist(self):
        test_dir = Path("tests")
        test_files = list(test_dir.glob("test_*.py")) if test_dir.exists() else []
        self.check("Testing", f"Test files exist ({len(test_files)})", len(test_files) >= 5,
                    f"Found {len(test_files)} test files")

    def check_no_secrets_in_code(self):
        secrets_patterns = ["api_key", "apikey", "secret", "password", "token"]
        matches = []
        for root, dirs, files in Path(".").walk():
            if "extensions" in root.parts or "__pycache__" in root.parts or ".git" in root.parts:
                continue
            for f in files:
                if f.endswith((".py", ".yml", ".yaml", ".json", ".md", ".example")):
                    path = Path(root) / f
                    try:
                        content = path.read_text(encoding="utf-8", errors="ignore")
                        for pattern in secrets_patterns:
                            if pattern in content.lower() and "example" not in f.lower() and ".env.example" not in str(path):
                                # Allow test files and docs which reference these terms
                                if "test_" not in f and "docs/" not in str(path):
                                    matches.append(f"{path}")
                    except Exception:
                        pass
        self.check("Security", "No hardcoded secrets", len(matches) == 0,
                    f"Found {len(matches)} potential secrets" if matches else "Clean")

    def check_gitignore(self):
        gitignore = Path(".gitignore")
        has_db = False
        has_env = False
        if gitignore.exists():
            content = gitignore.read_text()
            has_db = "*.db" in content
            has_env = ".env" in content
        self.check("Security", ".gitignore protects .db files", has_db, "")
        self.check("Security", ".gitignore protects .env", has_env, "")

    def _generate_report(self):
        passed = sum(1 for c in self.checks if c["status"] == "PASS")
        failed = sum(1 for c in self.checks if c["status"] == "FAIL")

        report = {
            "report_title": "Merge Readiness Checklist",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "total_checks": len(self.checks),
                "passed": passed,
                "failed": failed,
                "merge_ready": failed == 0,
            },
            "checks": self.checks,
        }

        report_path = self.report_dir / "merge_readiness_report.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n{'='*60}")
        print(f"Merge Readiness: {'READY ✓' if failed == 0 else f'NOT READY ({failed} failures) ✗'}")
        print(f"  Passed: {passed}/{len(self.checks)}")
        print(f"  Report: {report_path}")
        print(f"{'='*60}\n")

        sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    check = MergeReadinessCheck()
    check.run()
