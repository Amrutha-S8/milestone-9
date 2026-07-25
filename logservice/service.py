import logging
import logging.handlers
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from logservice.config import LoggingConfig

LOG_CHANNELS = [
    "application",
    "api",
    "evaluation",
    "error",
    "audit",
]


class LoggingService:
    def __init__(self, config: Optional[LoggingConfig] = None):
        self._config = config or LoggingConfig()
        self._loggers: dict[str, logging.Logger] = {}
        self._ensure_dirs()
        self._init_channels()

    def _ensure_dirs(self):
        for channel in LOG_CHANNELS:
            (self._config.log_dir / channel).mkdir(parents=True, exist_ok=True)

    def _init_channels(self):
        for channel in LOG_CHANNELS:
            logger = logging.getLogger(f"stayza.{channel}")
            logger.setLevel(getattr(logging, self._config.level.upper(), logging.INFO))
            logger.handlers.clear()
            logger.propagate = False

            file_handler = logging.handlers.RotatingFileHandler(
                filename=self._config.log_dir / channel / f"{channel}.log",
                maxBytes=self._config.max_bytes,
                backupCount=self._config.backup_count,
                encoding="utf-8",
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter(self._config.format, datefmt=self._config.date_format))
            logger.addHandler(file_handler)

            if channel == "error":
                error_handler = logging.handlers.RotatingFileHandler(
                    filename=self._config.log_dir / channel / "error.log",
                    maxBytes=self._config.max_bytes,
                    backupCount=self._config.backup_count,
                    encoding="utf-8",
                )
                error_handler.setLevel(logging.WARNING)
                error_handler.setFormatter(logging.Formatter(self._config.format, datefmt=self._config.date_format))
                logger.addHandler(error_handler)

            if channel == "audit":
                audit_handler = logging.handlers.RotatingFileHandler(
                    filename=self._config.log_dir / channel / "audit.log",
                    maxBytes=self._config.max_bytes,
                    backupCount=self._config.backup_count,
                    encoding="utf-8",
                )
                audit_handler.setLevel(logging.INFO)
                audit_handler.setFormatter(logging.Formatter("%(asctime)s | AUDIT | %(message)s", datefmt=self._config.date_format))
                logger.addHandler(audit_handler)

            self._loggers[channel] = logger

    def get_logger(self, channel: str = "application") -> logging.Logger:
        if channel not in self._loggers:
            return self._loggers.get("application", logging.getLogger("stayza"))
        return self._loggers[channel]

    def application(self) -> logging.Logger:
        return self.get_logger("application")

    def api(self) -> logging.Logger:
        return self.get_logger("api")

    def evaluation(self) -> logging.Logger:
        return self.get_logger("evaluation")

    def error(self) -> logging.Logger:
        return self.get_logger("error")

    def audit(self) -> logging.Logger:
        return self.get_logger("audit")

    def log_api_call(self, method: str, path: str, status: int, duration_ms: float, client_ip: str = "unknown"):
        logger = self.api()
        logger.info("API %s %s -> %d (%.1fms) from %s", method, path, status, duration_ms, client_ip)

    def log_evaluation_result(self, run_id: str, language: str, status: str, score: float):
        logger = self.evaluation()
        logger.info("EVAL run=%s language=%s status=%s score=%.1f", run_id, language, status, score)

    def log_audit_event(self, action: str, resource: str, user: str, details: Optional[str] = None):
        logger = self.audit()
        msg = f"action={action} resource={resource} user={user}"
        if details:
            msg += f" details={details}"
        logger.info(msg)

    def log_error(self, component: str, message: str, exc_info: bool = True):
        logger = self.error()
        logger.error("[%s] %s", component, message, exc_info=exc_info)

    def log_application(self, level: str, message: str):
        logger = self.application()
        log_fn = getattr(logger, level.lower(), logger.info)
        log_fn(message)


_service: Optional[LoggingService] = None


def get_logging_service(config: Optional[LoggingConfig] = None) -> LoggingService:
    global _service
    if _service is None:
        _service = LoggingService(config)
    return _service
