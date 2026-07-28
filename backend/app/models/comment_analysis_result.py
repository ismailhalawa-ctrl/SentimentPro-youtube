from datetime import UTC, datetime

from sqlalchemy import JSON, BigInteger, DateTime, Float, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

_datetime_type = DateTime().with_variant(mssql.DATETIME2, "mssql")


class CommentAnalysisResult(Base):
    __tablename__ = "comment_analysis_results"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    job_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("analysis_jobs.id"), nullable=False, index=True
    )
    comment_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("comment_analyses.id", ondelete="CASCADE"), nullable=False, index=True
    )

    capability: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)

    label: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    processing_time_ms: Mapped[float | None] = mapped_column(Float, nullable=True)

    result_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        _datetime_type, default=lambda: datetime.now(UTC), nullable=False
    )

    comment = relationship("CommentAnalysis", back_populates="results")

    __table_args__ = (
        Index("ix_comment_results_job_capability", "job_id", "capability"),
        Index("ix_comment_results_job_label", "job_id", "label"),
        UniqueConstraint(
            "job_id", "comment_id", "capability", name="uq_comment_results_job_comment_capability"
        ),
    )
