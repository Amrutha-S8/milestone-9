import logging
import logging.handlers
import os
from pathlib import Path
from typing import Literal

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_DIR = Path("logs/evaluation")
MAX_BYTES = 10 * 1024 * 1024
BACKUP_COUNT = 10


class IntegrationLogger:
    def __init__(
        self,
        name: str = "stayza.integration",
        level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
        log_dir: str | Path | None = None,
        console: bool = True,
    ):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))
        self._logger.handlers.clear()
        self._logger.propagate = False

        log_path = Path(log_dir) if log_dir else DEFAULT_LOG_DIR
        log_path.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_path / "integration.log",
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        self._logger.addHandler(file_handler)

        error_handler = logging.handlers.RotatingFileHandler(
            filename=log_path / "integration.error.log",
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT,
            encoding="utf-8",
        )
        error_handler.setLevel(logging.WARNING)
        error_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
        self._logger.addHandler(error_handler)

        if console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, level.upper(), logging.INFO))
            console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
            self._logger.addHandler(console_handler)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def debug(self, msg: str, *args, **extra):
        self._logger.debug(msg, *args)

    def info(self, msg: str, *args, **extra):
        self._logger.info(msg, *args)

    def warning(self, msg: str, *args, **extra):
        self._logger.warning(msg, *args)

    def error(self, msg: str, *args, **extra):
        self._logger.error(msg, *args)

    def critical(self, msg: str, *args, **extra):
        self._logger.critical(msg, *args)

    def request(self, method: str, path: str, status: int, duration_ms: float, **extra):
        self._logger.info("REQUEST %s %s -> %d (%.1fms)", method, path, status, duration_ms)

    def evaluation_result(self, run_id: str, passed: bool, language: str, **extra):
        level = logging.INFO if passed else logging.WARNING
        self._logger.log(level, "EVALUATION run=%s language=%s passed=%s", run_id, language, passed)

    def performance(self, operation: str, duration_ms: float, **extra):
        self._logger.debug("PERF %s %.1fms", operation, duration_ms)


_default_logger: IntegrationLogger | None = None


def get_integration_logger(
    level: str | None = None,
    log_dir: str | Path | None = None,
) -> IntegrationLogger:
    global _default_logger
    if _default_logger is None:
        env_level = os.getenv("INTEGRATION_LOG_LEVEL", "INFO")
        env_dir = os.getenv("INTEGRATION_LOG_DIR")
        _default_logger = IntegrationLogger(
            level=level or env_level,
            log_dir=Path(log_dir) if log_dir else (Path(env_dir) if env_dir else None),
        )
    return _default_logger
