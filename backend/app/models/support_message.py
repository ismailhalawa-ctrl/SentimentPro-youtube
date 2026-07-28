from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Unicode
from sqlalchemy.dialects import mssql
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

_datetime_type = DateTime().with_variant(mssql.DATETIME2, "mssql")


class SupportMessage(Base):
    __tablename__ = "support_messages"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )

    name: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Unicode(4000), nullable=False)

    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")

    created_at: Mapped[datetime] = mapped_column(
        _datetime_type, default=lambda: datetime.now(UTC), nullable=False, index=True
    )
