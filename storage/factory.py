import logging
import os

from storage.config import PostgresConfig, S3Config
from storage.postgres import PostgresStorage
from storage.s3 import S3ObjectStorage

logger = logging.getLogger("stayza.storage.factory")


class StorageFactory:
    @staticmethod
    def create_postgres(config: PostgresConfig | None = None) -> PostgresStorage:
        return PostgresStorage(config)

    @staticmethod
    def create_s3(config: S3Config | None = None) -> S3ObjectStorage:
        return S3ObjectStorage(config)

    @staticmethod
    def from_env() -> dict:
        storage_type = os.getenv("STORAGE_TYPE", "postgres")
        pg = StorageFactory.create_postgres() if storage_type in ("postgres", "both") else None
        s3 = StorageFactory.create_s3() if storage_type in ("s3", "both") else None
        logger.info("StorageFactory initialized type=%s pg=%s s3=%s", storage_type, pg is not None, s3 is not None)
        return {"postgres": pg, "s3": s3}
