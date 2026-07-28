from datetime import UTC, datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Integer, String, Unicode, UnicodeText
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

_datetime_type = DateTime().with_variant(mssql.DATETIME2, "mssql")


class CommentAnalysis(Base):
    __tablename__ = "comment_analyses"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    job_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("analysis_jobs.id", ondelete="CASCADE"), nullable=False
    )

    youtube_comment_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    author_display_name: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    text: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    like_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    published_at: Mapped[str] = mapped_column(Unicode(64), nullable=True)
    is_reply: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    language: Mapped[str | None] = mapped_column(String(16), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(
        _datetime_type, default=lambda: datetime.now(UTC), nullable=False
    )

    job = relationship("AnalysisJob", back_populates="comments")
    results: Mapped[list["CommentAnalysisResult"]] = relationship(
        back_populates="comment", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_comment_analyses_job_id_like_count", "job_id", "like_count"),)
