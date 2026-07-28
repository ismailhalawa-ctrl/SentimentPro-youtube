from datetime import UTC, datetime
from enum import Enum as PyEnum

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

_datetime_type = DateTime().with_variant(mssql.DATETIME2, "mssql")


class EmbeddingIndexStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"


class EmbeddingIndex(Base):
    __tablename__ = "embedding_indexes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    job_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("analysis_jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    embedding_provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    vector_store_provider_id: Mapped[str] = mapped_column(String(64), nullable=False)
    vector_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    status: Mapped[EmbeddingIndexStatus] = mapped_column(
        Enum(EmbeddingIndexStatus, native_enum=False, length=20),
        default=EmbeddingIndexStatus.PENDING,
        nullable=False,
    )
    error_message: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        _datetime_type, default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        _datetime_type,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    job = relationship("AnalysisJob", back_populates="embedding_index")
