import logging
from collections import defaultdict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.errors import ProviderCallError, ProviderNotConfiguredError
from app.ai.providers.provider_registry import resolve_provider
from app.models.analysis_job import AnalysisJob
from app.models.comment_analysis import CommentAnalysis
from app.models.comment_analysis_result import CommentAnalysisResult
from app.schemas.ai_insights import (
    AIFeatureResponse,
    CommentExtractionPayload,
    ExtractedCommentItem,
    RankedCategory,
)
from app.services import ai_usage_service
from app.services.ai_usage_service import UsageLimitExceededError
from app.services.billing_service import get_tier
from app.services.comment_query_helpers import get_non_spam_comments

logger = logging.getLogger(__name__)

_NOT_CONFIGURED_REASON = (
    "This feature requires an AI provider API key (OpenAI or Gemini) to be configured on the server."
)

_POSITIVE_LABEL = {
    Capability.COMPLAINT_EXTRACTION: "complaint",
    Capability.SUGGESTION_EXTRACTION: "suggestion",
}

_MAX_EXAMPLE_COMMENT_IDS = 3
_ID_QUERY_CHUNK_SIZE = 1000
_MAX_COMMENTS_TO_MINE = 500


async def get_or_generate_extraction(
    db: Session, job: AnalysisJob, capability: Capability, user_id: int
) -> AIFeatureResponse:
    if capability not in _POSITIVE_LABEL:
        return AIFeatureResponse(status="error", reason="Unknown extraction capability.")

    existing = (
        db.query(CommentAnalysisResult)
        .filter(
            CommentAnalysisResult.job_id == job.id,
            CommentAnalysisResult.capability == capability.value,
        )
        .all()
    )

    if not existing:
        comments = get_non_spam_comments(db, job.id)[:_MAX_COMMENTS_TO_MINE]
        if not comments:
            return AIFeatureResponse(status="error", reason="This job has no analyzable comments yet.")

        try:
            ai_usage_service.check_usage_limit(db, user_id, tier=get_tier(db, user_id))
        except UsageLimitExceededError as exc:
            return AIFeatureResponse(status="rate_limited", reason=exc.reason)

        try:
            provider = resolve_provider(capability, AnalysisMode.SMART, "auto")
            results = await provider.run_batch([comment.text for comment in comments])
        except ProviderNotConfiguredError:
            return AIFeatureResponse(status="unavailable", reason=_NOT_CONFIGURED_REASON)
        except (ProviderCallError, LookupError) as exc:
            logger.exception("Comment extraction failed for job %s capability %s", job.id, capability.value)
            return AIFeatureResponse(status="error", reason=str(exc))

        for comment, result in zip(comments, results, strict=True):
            db.add(
                CommentAnalysisResult(
                    job_id=job.id,
                    comment_id=comment.id,
                    capability=capability.value,
                    provider_id=result.provider_id,
                    mode=result.mode.value,
                    label=result.label,
                    confidence=result.confidence,
                    result_json=result.data,
                )
            )
        try:
            db.commit()
        except IntegrityError:
            db.rollback()

        ai_usage_service.record_usage(db, user_id, capability.value, 0, 0)

        existing = (
            db.query(CommentAnalysisResult)
            .filter(
                CommentAnalysisResult.job_id == job.id,
                CommentAnalysisResult.capability == capability.value,
            )
            .all()
        )

    payload = _build_payload(db, capability, existing)
    return AIFeatureResponse(status="ok", data=payload.model_dump())


def _build_payload(
    db: Session, capability: Capability, rows: list[CommentAnalysisResult]
) -> CommentExtractionPayload:
    positive_label = _POSITIVE_LABEL[capability]
    comment_ids = list({row.comment_id for row in rows})
    comment_rows = []
    for i in range(0, len(comment_ids), _ID_QUERY_CHUNK_SIZE):
        batch = comment_ids[i : i + _ID_QUERY_CHUNK_SIZE]
        comment_rows.extend(
            db.query(CommentAnalysis.id, CommentAnalysis.text, CommentAnalysis.like_count)
            .filter(CommentAnalysis.id.in_(batch))
            .all()
        )
    text_by_id = {row.id: row.text for row in comment_rows}
    likes_by_id = {row.id: row.like_count for row in comment_rows}

    items: list[ExtractedCommentItem] = []
    category_counts: dict[str, int] = defaultdict(int)
    category_likes: dict[str, int] = defaultdict(int)
    category_examples: dict[str, list[int]] = defaultdict(list)

    for row in rows:
        if row.label != positive_label:
            continue
        category = (row.result_json or {}).get("category")
        items.append(
            ExtractedCommentItem(
                comment_id=row.comment_id,
                text=text_by_id.get(row.comment_id, ""),
                category=category,
                confidence=row.confidence,
                is_feature_request=(
                    (row.result_json or {}).get("is_feature_request")
                    if capability == Capability.SUGGESTION_EXTRACTION
                    else None
                ),
            )
        )
        if category:
            category_counts[category] += 1
            category_likes[category] += likes_by_id.get(row.comment_id, 0)
            if len(category_examples[category]) < _MAX_EXAMPLE_COMMENT_IDS:
                category_examples[category].append(row.comment_id)

    items.sort(key=lambda item: likes_by_id.get(item.comment_id, 0), reverse=True)

    ranked_categories = sorted(
        (
            RankedCategory(
                category=category,
                count=count,
                total_likes=category_likes[category],
                example_comment_ids=category_examples[category],
            )
            for category, count in category_counts.items()
        ),
        key=lambda ranked: (ranked.count, ranked.total_likes),
        reverse=True,
    )

    return CommentExtractionPayload(ranked_categories=ranked_categories, items=items)
