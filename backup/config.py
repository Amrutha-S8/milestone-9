import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BackupConfig:
    backup_dir: Path = field(default_factory=lambda: Path(os.getenv("STAYZA_BACKUP_DIR", "backup")))
    max_backups: int = field(default_factory=lambda: int(os.getenv("STAYZA_MAX_BACKUPS", "30")))
    compress: bool = field(default_factory=lambda: os.getenv("STAYZA_BACKUP_COMPRESS", "true").lower() == "true")
    include_database: bool = field(default_factory=lambda: os.getenv("STAYZA_BACKUP_DB", "true").lower() == "true")
    include_reports: bool = field(default_factory=lambda: os.getenv("STAYZA_BACKUP_REPORTS", "true").lower() == "true")
    include_config: bool = field(default_factory=lambda: os.getenv("STAYZA_BACKUP_CONFIG", "true").lower() == "true")
    include_languages: bool = field(default_factory=lambda: os.getenv("STAYZA_BACKUP_LANGUAGES", "true").lower() == "true")
