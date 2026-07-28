from datetime import UTC, datetime
from enum import Enum as PyEnum

from sqlalchemy import JSON, BigInteger, DateTime, Enum, ForeignKey, Integer, String, Unicode
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

_datetime_type = DateTime().with_variant(mssql.DATETIME2, "mssql")


class AnalysisJobStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    video_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    video_id: Mapped[str] = mapped_column(String(32), nullable=False)
    video_title: Mapped[str | None] = mapped_column(Unicode(500), nullable=True)
    video_thumbnail_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    status: Mapped[AnalysisJobStatus] = mapped_column(
        Enum(AnalysisJobStatus, native_enum=False, length=20),
        default=AnalysisJobStatus.PENDING,
        nullable=False,
    )
    progress_percentage: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_step: Mapped[str | None] = mapped_column(Unicode(255), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Unicode(1024), nullable=True)

    options_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    total_fetched_comments: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_cleaned_comments: Mapped[int | None] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        _datetime_type, default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        _datetime_type,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    comments: Mapped[list["CommentAnalysis"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
    insights: Mapped[list["JobInsight"]] = relationship(back_populates="job", cascade="all, delete-orphan")
    embedding_index: Mapped["EmbeddingIndex | None"] = relationship(
        back_populates="job", cascade="all, delete-orphan", uselist=False
    )
    chat_sessions: Mapped[list["ChatSession"]] = relationship(
        back_populates="job", cascade="all, delete-orphan"
    )
