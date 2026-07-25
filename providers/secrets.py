import os
import base64
import logging
from typing import Optional

logger = logging.getLogger("stayza.security.secrets")


class SecretManager:
    def __init__(self, prefix: str = "STAYZA_"):
        self._prefix = prefix

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.getenv(f"{self._prefix}{key}", default)

    def get_required(self, key: str) -> str:
        value = self.get(key)
        if not value:
            raise RuntimeError(f"Required secret {self._prefix}{key} is not set")
        return value

    def get_int(self, key: str, default: int = 0) -> int:
        raw = self.get(key, str(default))
        try:
            return int(raw)
        except (ValueError, TypeError):
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        raw = self.get(key, str(default))
        try:
            return float(raw)
        except (ValueError, TypeError):
            return default

    def get_bool(self, key: str, default: bool = False) -> bool:
        raw = self.get(key, str(default)).lower()
        return raw in ("true", "1", "yes", "y")


_secret_manager: Optional[SecretManager] = None


def get_secret_manager(prefix: str = "STAYZA_") -> SecretManager:
    global _secret_manager
    if _secret_manager is None:
        _secret_manager = SecretManager(prefix)
    return _secret_manager
