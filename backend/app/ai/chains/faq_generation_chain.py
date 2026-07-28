from sqlalchemy.orm import Session

from app.ai.chains._shared import run_job_level_chain
from app.ai.interfaces.capability import Capability
from app.ai.interfaces.result import AnalysisResult
from app.schemas.ai_insights import FAQPayload


async def generate_faqs(job_id: int, db: Session, video_title: str | None = None) -> AnalysisResult:
    return await run_job_level_chain(job_id, db, Capability.FAQ_GENERATION, FAQPayload, video_title)
