import logging
from collections.abc import Callable

from pydantic import BaseModel, ValidationError
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.result import AnalysisResult
from app.ai.providers.provider_registry import resolve_provider
from app.models.comment_analysis import CommentAnalysis
from app.models.comment_analysis_result import CommentAnalysisResult

logger = logging.getLogger(__name__)

_DEFAULT_COMMENT_LIMIT = 200


def get_job_comment_texts(db: Session, job_id: int, limit: int = _DEFAULT_COMMENT_LIMIT) -> list[str]:
    spam_result = aliased(CommentAnalysisResult)
    rows = (
        db.query(CommentAnalysis.text)
        .outerjoin(
            spam_result,
            (spam_result.comment_id == CommentAnalysis.id)
            & (spam_result.capability == Capability.SPAM.value),
        )
        .filter(
            CommentAnalysis.job_id == job_id,
            (spam_result.label != "spam") | (spam_result.label.is_(None)),
        )
        .order_by(CommentAnalysis.like_count.desc())
        .limit(limit)
        .all()
    )
    return [r[0] for r in rows]


def get_dominant_language(db: Session, job_id: int) -> str:
    rows = (
        db.query(CommentAnalysis.language, func.count())
        .filter(CommentAnalysis.job_id == job_id, CommentAnalysis.language.isnot(None))
        .group_by(CommentAnalysis.language)
        .all()
    )
    counts: dict[str, int] = {language: count for language, count in rows if language is not None}
    if counts.get("ar", 0) > counts.get("en", 0):
        return "ar"
    return "en"


_REPAIR_NOTE = (
    "\n\n[SYSTEM NOTE: your previous response for this exact input was not "
    "valid JSON matching the required schema. Respond again with ONLY a "
    "valid JSON object matching the schema described above — no prose, no "
    "markdown code fences.]"
)


async def run_job_level_chain(
    job_id: int,
    db: Session,
    capability: Capability,
    payload_model: type[BaseModel],
    video_title: str | None = None,
    label_fn: Callable[[BaseModel], str] = lambda payload: "generated",
    extra_kwargs: dict | None = None,
) -> AnalysisResult:
    texts = get_job_comment_texts(db, job_id)
    if not texts:
        return AnalysisResult(
            capability=capability,
            provider_id="none",
            mode=AnalysisMode.SMART,
            label="no_comments",
            confidence=None,
            data={},
        )

    comments_blob = "\n".join(texts)
    provider = resolve_provider(capability, AnalysisMode.SMART, "auto")
    response_language = get_dominant_language(db, job_id)
    kwargs = {
        "video_title": video_title or "this video",
        "response_language": response_language,
        **(extra_kwargs or {}),
    }

    result = await provider.run(comments_blob, **kwargs)
    payload = _try_validate(payload_model, result.data)

    if payload is None:
        logger.warning("%s for job %s: invalid response, retrying once", capability.value, job_id)
        result = await provider.run(comments_blob + _REPAIR_NOTE, **kwargs)
        payload = _try_validate(payload_model, result.data)

    if payload is None:
        logger.warning(
            "%s for job %s: invalid response after repair retry, giving up", capability.value, job_id
        )
        result.label = "parse_error"
        return result

    result.label = label_fn(payload)
    result.data = payload.model_dump()
    return result


def _try_validate(payload_model: type[BaseModel], data: dict) -> BaseModel | None:
    try:
        return payload_model.model_validate(data)
    except ValidationError:
        return None
