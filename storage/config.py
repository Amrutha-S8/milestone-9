import os
from dataclasses import dataclass, field


@dataclass
class PostgresConfig:
    host: str = field(default_factory=lambda: os.getenv("PGHOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("PGPORT", "5432")))
    database: str = field(default_factory=lambda: os.getenv("PGDATABASE", "stayza"))
    user: str = field(default_factory=lambda: os.getenv("PGUSER", "stayza"))
    password: str = field(default_factory=lambda: os.getenv("PGPASSWORD", ""))
    pool_size: int = field(default_factory=lambda: int(os.getenv("PG_POOL_SIZE", "10")))
    max_overflow: int = field(default_factory=lambda: int(os.getenv("PG_MAX_OVERFLOW", "20")))

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class S3Config:
    endpoint: str = field(default_factory=lambda: os.getenv("S3_ENDPOINT", "https://s3.amazonaws.com"))
    access_key: str = field(default_factory=lambda: os.getenv("S3_ACCESS_KEY", ""))
    secret_key: str = field(default_factory=lambda: os.getenv("S3_SECRET_KEY", ""))
    region: str = field(default_factory=lambda: os.getenv("S3_REGION", "us-east-1"))
    bucket: str = field(default_factory=lambda: os.getenv("S3_BUCKET", "stayza-reports"))
    secure: bool = field(default_factory=lambda: os.getenv("S3_SECURE", "true").lower() == "true")
