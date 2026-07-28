from datetime import UTC, datetime

from sqlalchemy import JSON, BigInteger, DateTime, Float, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

_datetime_type = DateTime().with_variant(mssql.DATETIME2, "mssql")


class JobInsight(Base):
    __tablename__ = "job_insights"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    job_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("analysis_jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    capability: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)

    headline_label: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    headline_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    result_json: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)

    created_at: Mapped[datetime] = mapped_column(
        _datetime_type, default=lambda: datetime.now(UTC), nullable=False
    )

    job = relationship("AnalysisJob", back_populates="insights")

    __table_args__ = (UniqueConstraint("job_id", "capability", name="uq_job_insights_job_capability"),)
