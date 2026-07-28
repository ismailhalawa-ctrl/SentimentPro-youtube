from dataclasses import dataclass

from sqlalchemy.orm import Session


@dataclass(frozen=True)
class ToolContext:
    user_id: int
    db: Session
    target_job_id: int | None = None
