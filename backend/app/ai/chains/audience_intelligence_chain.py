from sqlalchemy.orm import Session

from app.ai.chains._shared import run_job_level_chain
from app.ai.interfaces.capability import Capability
from app.ai.interfaces.result import AnalysisResult
from app.schemas.ai_insights import AudienceIntelligenceNarrativePayload, AudienceIntelligenceScores


async def generate_audience_intelligence_narrative(
    job_id: int,
    db: Session,
    scores: AudienceIntelligenceScores,
    video_title: str | None = None,
) -> AnalysisResult:
    return await run_job_level_chain(
        job_id,
        db,
        Capability.AUDIENCE_INTELLIGENCE_SCORE,
        AudienceIntelligenceNarrativePayload,
        video_title,
        extra_kwargs={"scores": scores.model_dump()},
    )
