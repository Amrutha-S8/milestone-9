import json
import logging
from datetime import datetime, timezone
from typing import Any, Optional

from storage.config import S3Config

logger = logging.getLogger("stayza.storage.s3")


class S3ObjectStorage:
    def __init__(self, config: Optional[S3Config] = None):
        self._config = config or S3Config()
        self._client = None

    def _get_client(self):
        if self._client is not None:
            return self._client
        try:
            import boto3
        except ImportError:
            raise RuntimeError("boto3 is not installed. Install with: pip install boto3")
        session = boto3.Session(
            aws_access_key_id=self._config.access_key,
            aws_secret_access_key=self._config.secret_key,
            region_name=self._config.region,
        )
        self._client = session.client(
            "s3",
            endpoint_url=self._config.endpoint,
            config=boto3.session.Config(signature_version="s3v4"),
        )
        self._ensure_bucket()
        return self._client

    def _ensure_bucket(self):
        try:
            self._client.head_bucket(Bucket=self._config.bucket)
        except Exception:
            self._client.create_bucket(Bucket=self._config.bucket)
            logger.info("Created S3 bucket '%s'", self._config.bucket)

    def put_json(self, key: str, data: Any) -> str:
        client = self._get_client()
        body = json.dumps(data, indent=2, default=str)
        client.put_object(Bucket=self._config.bucket, Key=key, Body=body, ContentType="application/json")
        logger.info("S3 stored key='%s' bucket='%s'", key, self._config.bucket)
        return key

    def get_json(self, key: str) -> Optional[Any]:
        client = self._get_client()
        try:
            response = client.get_object(Bucket=self._config.bucket, Key=key)
            return json.loads(response["Body"].read().decode("utf-8"))
        except client.exceptions.NoSuchKey:
            return None

    def put_bytes(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        client = self._get_client()
        client.put_object(Bucket=self._config.bucket, Key=key, Body=data, ContentType=content_type)
        return key

    def list_keys(self, prefix: str = "") -> list[str]:
        client = self._get_client()
        response = client.list_objects_v2(Bucket=self._config.bucket, Prefix=prefix)
        return [obj["Key"] for obj in response.get("Contents", [])]

    def delete_key(self, key: str) -> bool:
        client = self._get_client()
        try:
            client.delete_object(Bucket=self._config.bucket, Key=key)
            return True
        except Exception as e:
            logger.error("S3 delete failed key='%s': %s", key, e)
            return False

    def save_evaluation_report(self, report_data: dict) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        key = f"evaluation/reports/report_{timestamp}.json"
        return self.put_json(key, report_data)

    def save_review_report(self, report_data: dict) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        key = f"review/reports/report_{timestamp}.json"
        return self.put_json(key, report_data)
