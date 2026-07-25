import logging
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Float,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from storage.config import PostgresConfig

logger = logging.getLogger("stayza.storage.postgres")

Base = declarative_base()


class StoredEvaluationReport(Base):
    __tablename__ = "evaluation_reports"
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String(255), unique=True, nullable=False, index=True)
    engine_version = Column(String(50), nullable=True)
    total_languages = Column(Integer, default=0)
    total_samples = Column(Integer, default=0)
    overall_accuracy = Column(Float, default=0.0)
    languages_passed = Column(Integer, default=0)
    languages_warning = Column(Integer, default=0)
    languages_failed = Column(Integer, default=0)
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)


class StoredLanguageScore(Base):
    __tablename__ = "language_scores"
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False, index=True)
    intent_accuracy = Column(Float, default=0.0)
    wer = Column(Float, default=0.0)
    flow_completion = Column(Float, default=0.0)
    avg_latency_ms = Column(Float, default=0.0)
    final_score = Column(Float, default=0.0)
    status = Column(String(20), default="UNKNOWN")
    evaluated_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)


class StoredBenchmarkResult(Base):
    __tablename__ = "benchmark_results"
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False, index=True)
    total_items = Column(Integer, default=0)
    correct_intents = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)


class StoredLatencyHistory(Base):
    __tablename__ = "latency_history"
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(50), nullable=False, index=True)
    operation = Column(String(100), nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC), nullable=False)


class PostgresStorage:
    def __init__(self, config: PostgresConfig | None = None):
        self._config = config or PostgresConfig()
        self._engine = create_engine(
            self._config.url,
            pool_size=self._config.pool_size,
            max_overflow=self._config.max_overflow,
            pool_pre_ping=True,
        )
        self._session_factory = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        Base.metadata.create_all(bind=self._engine)
        logger.info("PostgresStorage initialized url=%s pool=%d", self._config.url, self._config.pool_size)

    @property
    def engine(self):
        return self._engine

    def session(self):
        return self._session_factory()

    def save_evaluation_report(self, report_data: dict) -> int:
        summary = report_data.get("summary", {})
        with self.session() as session:
            record = StoredEvaluationReport(
                report_id=report_data.get("report_id", ""),
                engine_version=report_data.get("engine_version", "1.0.0"),
                total_languages=summary.get("total_languages_evaluated", 0),
                total_samples=summary.get("total_samples", 0),
                overall_accuracy=summary.get("overall_accuracy", 0.0),
                languages_passed=summary.get("languages_passed", 0),
                languages_warning=summary.get("languages_warning", 0),
                languages_failed=summary.get("languages_failed", 0),
                data=report_data,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def save_language_scores(self, language: str, scores: dict) -> int:
        with self.session() as session:
            record = StoredLanguageScore(
                language=language,
                intent_accuracy=scores.get("intent_accuracy_pct", 0) / 100.0,
                wer=scores.get("wer_pct", 0) / 100.0,
                flow_completion=scores.get("flow_completion_pct", 0) / 100.0,
                avg_latency_ms=scores.get("avg_latency_ms", 0),
                final_score=scores.get("final_score", 0),
                status=scores.get("status", "UNKNOWN"),
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def save_benchmark_result(self, language: str, result: dict) -> int:
        with self.session() as session:
            record = StoredBenchmarkResult(
                language=language,
                total_items=result.get("total_samples", 0),
                correct_intents=result.get("correct_intents", 0),
                accuracy=result.get("accuracy", 0.0),
                data=result,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def record_latency(self, language: str, operation: str, latency_ms: float) -> int:
        with self.session() as session:
            record = StoredLatencyHistory(
                language=language,
                operation=operation,
                latency_ms=latency_ms,
            )
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def get_latest_evaluation_report(self) -> dict | None:
        with self.session() as session:
            record = session.query(StoredEvaluationReport).order_by(StoredEvaluationReport.created_at.desc()).first()
            if record:
                return {"id": record.id, "report_id": record.report_id, "data": record.data}
            return None

    def get_language_score_history(self, language: str, limit: int = 50) -> list[dict]:
        with self.session() as session:
            records = (
                session.query(StoredLanguageScore)
                .filter(StoredLanguageScore.language == language)
                .order_by(StoredLanguageScore.evaluated_at.desc())
                .limit(limit)
                .all()
            )
            return [{"id": r.id, "final_score": r.final_score, "status": r.status, "evaluated_at": r.evaluated_at.isoformat()} for r in records]

    def get_latency_statistics(self, language: str | None = None) -> dict:
        with self.session() as session:
            query = session.query(StoredLatencyHistory)
            if language:
                query = query.filter(StoredLatencyHistory.language == language)
            records = query.all()
            if not records:
                return {"count": 0, "avg_ms": 0.0, "min_ms": 0.0, "max_ms": 0.0}
            latencies = [r.latency_ms for r in records]
            return {
                "count": len(latencies),
                "avg_ms": round(sum(latencies) / len(latencies), 2),
                "min_ms": round(min(latencies), 2),
                "max_ms": round(max(latencies), 2),
            }
