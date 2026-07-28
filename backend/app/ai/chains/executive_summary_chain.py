import logging

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.ai.chains._shared import get_dominant_language, get_job_comment_texts
from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.result import AnalysisResult
from app.ai.providers.provider_registry import resolve_provider
from app.schemas.ai_insights import ExecutiveSummaryPayload

logger = logging.getLogger(__name__)

_REPAIR_NOTE = (
    "\n\n[SYSTEM NOTE: your previous response for this exact input was not "
    "valid JSON matching the required schema. Respond again with ONLY a "
    "valid JSON object matching the schema described above — no prose, no "
    "markdown code fences.]"
)


async def generate_executive_summary(
    job_id: int, db: Session, video_title: str | None = None
) -> AnalysisResult:
    texts = get_job_comment_texts(db, job_id)
    if not texts:
        return AnalysisResult(
            capability=Capability.EXECUTIVE_SUMMARY,
            provider_id="none",
            mode=AnalysisMode.SMART,
            label="no_comments",
            confidence=None,
            data={},
        )

    comments_blob = "\n".join(texts)
    provider = resolve_provider(Capability.EXECUTIVE_SUMMARY, AnalysisMode.SMART, "auto")
    response_language = get_dominant_language(db, job_id)

    result = await provider.run(
        comments_blob, video_title=video_title or "this video", response_language=response_language
    )
    payload = _try_validate(result.data)

    if payload is None:
        logger.warning("Executive summary for job %s: invalid response, retrying once", job_id)
        result = await provider.run(
            comments_blob + _REPAIR_NOTE,
            video_title=video_title or "this video",
            response_language=response_language,
        )
        payload = _try_validate(result.data)

    if payload is None:
        logger.warning(
            "Executive summary for job %s: invalid response after repair retry, giving up",
            job_id,
        )
        result.label = "parse_error"
        return result

    result.label = payload.overall_sentiment_label
    result.data = payload.model_dump()
    return result


def _try_validate(data: dict) -> ExecutiveSummaryPayload | None:
    try:
        return ExecutiveSummaryPayload.model_validate(data)
    except ValidationError:
        return None
