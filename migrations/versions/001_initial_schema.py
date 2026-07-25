from collections.abc import Sequence
from datetime import UTC, datetime

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade():
    op.create_table(
        "evaluation_reports",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("report_id", sa.String(255), unique=True, nullable=False, index=True),
        sa.Column("engine_version", sa.String(50), nullable=True),
        sa.Column("total_languages", sa.Integer(), default=0),
        sa.Column("total_samples", sa.Integer(), default=0),
        sa.Column("overall_accuracy", sa.Float(), default=0.0),
        sa.Column("languages_passed", sa.Integer(), default=0),
        sa.Column("languages_warning", sa.Integer(), default=0),
        sa.Column("languages_failed", sa.Integer(), default=0),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), default=lambda: datetime.now(UTC)),
    )
    op.create_table(
        "language_scores",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("language", sa.String(50), nullable=False, index=True),
        sa.Column("intent_accuracy", sa.Float(), default=0.0),
        sa.Column("wer", sa.Float(), default=0.0),
        sa.Column("flow_completion", sa.Float(), default=0.0),
        sa.Column("avg_latency_ms", sa.Float(), default=0.0),
        sa.Column("final_score", sa.Float(), default=0.0),
        sa.Column("status", sa.String(20), default="UNKNOWN"),
        sa.Column("evaluated_at", sa.DateTime(), default=lambda: datetime.now(UTC)),
    )
    op.create_table(
        "benchmark_results",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("language", sa.String(50), nullable=False, index=True),
        sa.Column("total_items", sa.Integer(), default=0),
        sa.Column("correct_intents", sa.Integer(), default=0),
        sa.Column("accuracy", sa.Float(), default=0.0),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), default=lambda: datetime.now(UTC)),
    )
    op.create_table(
        "latency_history",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("language", sa.String(50), nullable=False, index=True),
        sa.Column("operation", sa.String(100), nullable=False),
        sa.Column("latency_ms", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), default=lambda: datetime.now(UTC)),
    )


def downgrade():
    op.drop_table("latency_history")
    op.drop_table("benchmark_results")
    op.drop_table("language_scores")
    op.drop_table("evaluation_reports")
