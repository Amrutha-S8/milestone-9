import json
import logging
import os
import shutil
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from backup.config import BackupConfig

logger = logging.getLogger("stayza.backup")


class BackupService:
    def __init__(self, config: Optional[BackupConfig] = None):
        self._config = config or BackupConfig()
        self._config.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, label: str = "auto") -> Path:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        backup_name = f"stayza_backup_{timestamp}_{label}"
        backup_path = self._config.backup_dir / backup_name
        backup_path.mkdir(parents=True, exist_ok=True)

        manifest = {
            "backup_name": backup_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "label": label,
            "contents": [],
        }

        if self._config.include_database:
            db_files = self._backup_database(backup_path)
            manifest["contents"].extend(db_files)

        if self._config.include_reports:
            report_files = self._backup_reports(backup_path)
            manifest["contents"].extend(report_files)

        if self._config.include_config:
            config_files = self._backup_config(backup_path)
            manifest["contents"].extend(config_files)

        if self._config.include_languages:
            lang_files = self._backup_languages(backup_path)
            manifest["contents"].extend(lang_files)

        manifest_path = backup_path / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        if self._config.compress:
            archive_path = self._compress_backup(backup_path)
            shutil.rmtree(backup_path)
            logger.info("Backup created: %s (compressed)", archive_path)
            return archive_path

        logger.info("Backup created: %s", backup_path)
        return backup_path

    def _backup_database(self, backup_path: Path) -> list[str]:
        files = []
        for db_path in ["review_data/reviews.db", "test_reviews.db", "stayza.db"]:
            if os.path.exists(db_path):
                shutil.copy2(db_path, backup_path / os.path.basename(db_path))
                files.append(os.path.basename(db_path))
        return files

    def _backup_reports(self, backup_path: Path) -> list[str]:
        files = []
        reports_dir = Path("reports")
        if reports_dir.exists():
            dest = backup_path / "reports"
            shutil.copytree(reports_dir, dest)
            files.append("reports")
        review_reports_dir = Path("review_data/reports")
        if review_reports_dir.exists():
            dest = backup_path / "review_reports"
            shutil.copytree(review_reports_dir, dest)
            files.append("review_reports")
        return files

    def _backup_config(self, backup_path: Path) -> list[str]:
        files = []
        config_files = ["requirements.txt", ".env.example"]
        for cf in config_files:
            if os.path.exists(cf):
                shutil.copy2(cf, backup_path / cf)
                files.append(cf)
        return files

    def _backup_languages(self, backup_path: Path) -> list[str]:
        files = []
        lang_dir = Path("datasets")
        if lang_dir.exists():
            dest = backup_path / "datasets"
            shutil.copytree(lang_dir, dest)
            files.append("datasets")
        flow_dir = Path("languages")
        if flow_dir.exists():
            dest = backup_path / "languages"
            shutil.copytree(flow_dir, dest)
            files.append("languages")
        return files

    def _compress_backup(self, backup_path: Path) -> Path:
        archive_path = backup_path.parent / f"{backup_path.name}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            tar.add(backup_path, arcname=backup_path.name)
        return archive_path

    def list_backups(self) -> list[dict]:
        backups = []
        for entry in sorted(self._config.backup_dir.iterdir(), reverse=True):
            if entry.name.endswith(".tar.gz") or entry.is_dir():
                size = entry.stat().st_size if entry.is_file() else self._dir_size(entry)
                backups.append({
                    "name": entry.name,
                    "size_bytes": size,
                    "size_human": self._human_size(size),
                    "is_compressed": entry.name.endswith(".tar.gz"),
                })
        return backups

    def cleanup_old_backups(self, max_backups: Optional[int] = None):
        max_b = max_backups or self._config.max_backups
        backups = self.list_backups()
        if len(backups) <= max_b:
            return
        for old in backups[max_b:]:
            path = self._config.backup_dir / old["name"]
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            logger.info("Removed old backup: %s", old["name"])

    @staticmethod
    def _dir_size(path: Path) -> int:
        total = 0
        for entry in path.rglob("*"):
            if entry.is_file():
                total += entry.stat().st_size
        return total

    @staticmethod
    def _human_size(size_bytes: int) -> str:
        for unit in ("B", "KB", "MB", "GB"):
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}TB"


class RestoreService:
    def __init__(self, backup_dir: Optional[Path] = None):
        self._backup_dir = Path(backup_dir) if backup_dir else Path("backup")

    def list_available(self) -> list[dict]:
        service = BackupService(BackupConfig(backup_dir=self._backup_dir))
        return service.list_backups()

    def restore(self, backup_name: str, target_dir: Optional[Path] = None) -> Path:
        backup_path = self._backup_dir / backup_name
        restore_dir = Path(target_dir or ".")

        if backup_name.endswith(".tar.gz"):
            import tempfile
            with tempfile.TemporaryDirectory() as tmp:
                with tarfile.open(backup_path, "r:gz") as tar:
                    tar.extractall(tmp)
                extracted = Path(tmp) / backup_name.replace(".tar.gz", "")
                return self._restore_from_dir(extracted, restore_dir)
        elif backup_path.is_dir():
            return self._restore_from_dir(backup_path, restore_dir)
        else:
            raise FileNotFoundError(f"Backup not found: {backup_name}")

    def _restore_from_dir(self, source: Path, target: Path) -> Path:
        manifest_path = source / "manifest.json"
        if manifest_path.exists():
            with open(manifest_path) as f:
                manifest = json.load(f)
            logger.info("Restoring backup: %s", manifest.get("backup_name", "unknown"))

        for item in source.iterdir():
            if item.name == "manifest.json":
                continue
            dest = target / item.name
            if item.is_dir():
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest)
            logger.info("Restored: %s -> %s", item.name, dest)

        logger.info("Restore complete from: %s", source)
        return target
