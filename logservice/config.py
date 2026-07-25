import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LoggingConfig:
    log_dir: Path = field(default_factory=lambda: Path(os.getenv("STAYZA_LOG_DIR", "logs")))

    def __post_init__(self):
        if isinstance(self.log_dir, str):
            self.log_dir = Path(self.log_dir)
    max_bytes: int = field(default_factory=lambda: int(os.getenv("STAYZA_LOG_MAX_BYTES", str(10 * 1024 * 1024))))
    backup_count: int = field(default_factory=lambda: int(os.getenv("STAYZA_LOG_BACKUP_COUNT", "10")))
    level: str = field(default_factory=lambda: os.getenv("STAYZA_LOG_LEVEL", "INFO"))
    format: str = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
