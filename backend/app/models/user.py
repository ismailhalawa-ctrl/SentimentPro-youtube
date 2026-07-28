from datetime import UTC, datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Index, String, Unicode, text
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

_datetime_type = DateTime().with_variant(mssql.DATETIME2, "mssql")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        _datetime_type, default=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        _datetime_type,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    last_name_change: Mapped[datetime | None] = mapped_column(_datetime_type, nullable=True)

    google_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    reset_token_hash: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    reset_token_expires_at: Mapped[datetime | None] = mapped_column(_datetime_type, nullable=True)

    __table_args__ = (
        Index(
            "ix_users_google_id",
            "google_id",
            unique=True,
            mssql_where=text("google_id IS NOT NULL"),
        ),
    )
