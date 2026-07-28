from sqlalchemy.orm import Session

from app.ai.chains._shared import run_job_level_chain
from app.ai.interfaces.capability import Capability
from app.ai.interfaces.result import AnalysisResult
from app.schemas.ai_insights import TopicClusteringPayload


async def generate_topic_clusters(job_id: int, db: Session, video_title: str | None = None) -> AnalysisResult:
    return await run_job_level_chain(
        job_id, db, Capability.TOPIC_CLUSTERING, TopicClusteringPayload, video_title
    )
