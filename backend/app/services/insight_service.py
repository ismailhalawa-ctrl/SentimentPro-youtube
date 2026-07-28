import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.ai.chains.audience_analysis_chain import generate_audience_analysis
from app.ai.chains.audience_intelligence_chain import generate_audience_intelligence_narrative
from app.ai.chains.executive_summary_chain import generate_executive_summary
from app.ai.chains.faq_generation_chain import generate_faqs
from app.ai.chains.topic_clustering_chain import generate_topic_clusters
from app.ai.interfaces.capability import Capability
from app.ai.interfaces.errors import ProviderCallError, ProviderNotConfiguredError
from app.ai.scoring.audience_intelligence_scorer import compute_scores
from app.models.analysis_job import AnalysisJob
from app.models.job_insight import JobInsight
from app.schemas.ai_insights import AIFeatureResponse, AudienceIntelligenceScorePayload
from app.services import ai_usage_service
from app.services.ai_usage_service import UsageLimitExceededError
from app.services.billing_service import get_tier

logger = logging.getLogger(__name__)

_CHAINS = {
    Capability.EXECUTIVE_SUMMARY: generate_executive_summary,
    Capability.AUDIENCE_ANALYSIS: generate_audience_analysis,
    Capability.FAQ_GENERATION: generate_faqs,
    Capability.TOPIC_CLUSTERING: generate_topic_clusters,
}

_NOT_CONFIGURED_REASON = (
    "This feature requires an AI provider API key (OpenAI or Gemini) to be configured on the server."
)


async def get_or_generate_insight(
    db: Session, job: AnalysisJob, capability: Capability, user_id: int
) -> AIFeatureResponse:
    chain = _CHAINS.get(capability)
    if chain is None:
        return AIFeatureResponse(status="error", reason="Unknown insight capability.")

    existing = (
        db.query(JobInsight)
        .filter(JobInsight.job_id == job.id, JobInsight.capability == capability.value)
        .order_by(JobInsight.created_at.desc())
        .first()
    )
    if existing is not None:
        return AIFeatureResponse(status="ok", data=existing.result_json)

    try:
        ai_usage_service.check_usage_limit(db, user_id, tier=get_tier(db, user_id))
    except UsageLimitExceededError as exc:
        return AIFeatureResponse(status="rate_limited", reason=exc.reason)

    try:
        result = await chain(job.id, db, video_title=job.video_title)
    except ProviderNotConfiguredError:
        return AIFeatureResponse(status="unavailable", reason=_NOT_CONFIGURED_REASON)
    except (ProviderCallError, LookupError) as exc:
        logger.exception("AI insight generation failed for job %s capability %s", job.id, capability.value)
        return AIFeatureResponse(status="error", reason=str(exc))

    if result.label == "no_comments":
        return AIFeatureResponse(status="error", reason="This job has no analyzable comments yet.")
    if result.label == "parse_error":
        return AIFeatureResponse(
            status="error",
            reason="The AI provider returned a response that could not be parsed.",
        )

    db.add(
        JobInsight(
            job_id=job.id,
            capability=capability.value,
            provider_id=result.provider_id,
            mode=result.mode.value,
            headline_label=result.label,
            headline_score=result.confidence,
            result_json=result.data,
        )
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = (
            db.query(JobInsight)
            .filter(JobInsight.job_id == job.id, JobInsight.capability == capability.value)
            .order_by(JobInsight.created_at.desc())
            .first()
        )
        if existing is not None:
            return AIFeatureResponse(status="ok", data=existing.result_json)
        raise

    ai_usage_service.record_usage(db, user_id, capability.value, 0, 0)

    return AIFeatureResponse(status="ok", data=result.data)


async def get_or_generate_audience_intelligence(
    db: Session, job: AnalysisJob, user_id: int
) -> AIFeatureResponse:
    existing = (
        db.query(JobInsight)
        .filter(
            JobInsight.job_id == job.id,
            JobInsight.capability == Capability.AUDIENCE_INTELLIGENCE_SCORE.value,
        )
        .order_by(JobInsight.created_at.desc())
        .first()
    )
    if existing is not None:
        return AIFeatureResponse(status="ok", data=existing.result_json)

    scores = compute_scores(db, job.id)
    if scores is None:
        return AIFeatureResponse(status="error", reason="This job has no analyzable comments yet.")

    scores_only_data = {"scores": scores.model_dump(), "emerging_trends": [], "growth_opportunities": []}

    try:
        ai_usage_service.check_usage_limit(db, user_id, tier=get_tier(db, user_id))
    except UsageLimitExceededError as exc:
        return AIFeatureResponse(status="rate_limited", data=scores_only_data, reason=exc.reason)

    try:
        narrative_result = await generate_audience_intelligence_narrative(
            job.id, db, scores, video_title=job.video_title
        )
    except ProviderNotConfiguredError:
        return AIFeatureResponse(status="partial", data=scores_only_data, reason=_NOT_CONFIGURED_REASON)
    except (ProviderCallError, LookupError) as exc:
        logger.exception("Audience intelligence narrative failed for job %s", job.id)
        return AIFeatureResponse(status="partial", data=scores_only_data, reason=str(exc))

    if narrative_result.label in ("no_comments", "parse_error"):
        return AIFeatureResponse(
            status="partial",
            data=scores_only_data,
            reason="The AI provider returned a response that could not be parsed.",
        )

    payload = AudienceIntelligenceScorePayload(
        scores=scores,
        emerging_trends=narrative_result.data.get("emerging_trends", []),
        growth_opportunities=narrative_result.data.get("growth_opportunities", []),
    )

    db.add(
        JobInsight(
            job_id=job.id,
            capability=Capability.AUDIENCE_INTELLIGENCE_SCORE.value,
            provider_id=narrative_result.provider_id,
            mode=narrative_result.mode.value,
            headline_label="generated",
            headline_score=None,
            result_json=payload.model_dump(),
        )
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = (
            db.query(JobInsight)
            .filter(
                JobInsight.job_id == job.id,
                JobInsight.capability == Capability.AUDIENCE_INTELLIGENCE_SCORE.value,
            )
            .order_by(JobInsight.created_at.desc())
            .first()
        )
        if existing is not None:
            return AIFeatureResponse(status="ok", data=existing.result_json)
        raise

    ai_usage_service.record_usage(db, user_id, Capability.AUDIENCE_INTELLIGENCE_SCORE.value, 0, 0)

    return AIFeatureResponse(status="ok", data=payload.model_dump())
