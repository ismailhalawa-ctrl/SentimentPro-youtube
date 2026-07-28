from app.ai.scoring.audience_intelligence_scorer import compute_scores
from app.ai.tools._shared import resolve_owned_job
from app.ai.tools.base import Tool
from app.ai.tools.context import ToolContext
from app.ai.tools.registry import register_tool
from app.services import analysis_service
from app.services.insights_service import get_job_insights

_MAX_JOBS_LIMIT = 50


def _total_comments(summary) -> int:
    if summary is None:
        return 0
    return summary.positive_count + summary.neutral_count + summary.negative_count


async def _list_my_jobs(args: dict, ctx: ToolContext) -> dict:
    try:
        limit = max(1, min(int(args.get("limit", 10)), _MAX_JOBS_LIMIT))
    except (TypeError, ValueError):
        limit = 10

    jobs = analysis_service.list_jobs(ctx.db, owner_id=ctx.user_id, limit=limit)
    summaries = analysis_service.get_sentiment_summaries_for_jobs(ctx.db, [job.id for job in jobs])

    return {
        "jobs": [
            {
                "job_id": job.id,
                "video_title": job.video_title,
                "video_id": job.video_id,
                "status": job.status.value,
                "created_at": job.created_at.isoformat(),
                "comment_count": _total_comments(summaries.get(job.id)),
            }
            for job in jobs
        ]
    }


register_tool(
    Tool(
        name="list_my_jobs",
        description=(
            "List the current user's analyzed YouTube videos, most recent first, "
            "with basic status and comment counts."
        ),
        input_schema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": f"Maximum number of jobs to return (1-{_MAX_JOBS_LIMIT}).",
                    "default": 10,
                }
            },
            "required": [],
        },
        handler=_list_my_jobs,
        cost_tier="free",
    )
)


async def _get_video_metadata(args: dict, ctx: ToolContext) -> dict:
    job = resolve_owned_job(args, ctx)
    if isinstance(job, dict):
        return job

    return {
        "job_id": job.id,
        "video_title": job.video_title,
        "video_id": job.video_id,
        "video_url": job.video_url,
        "video_thumbnail_url": job.video_thumbnail_url,
        "duration": None,
        "status": job.status.value,
        "analyzed_at": job.created_at.isoformat(),
    }


register_tool(
    Tool(
        name="get_video_metadata",
        description=(
            "Get title, URL, thumbnail, status, and analysis date for one of the "
            "user's analyzed videos. 'duration' is always null — this app does not "
            "currently fetch or store video duration."
        ),
        input_schema={
            "type": "object",
            "properties": {"job_id": {"type": "integer", "description": "The analysis job id."}},
            "required": ["job_id"],
        },
        handler=_get_video_metadata,
        cost_tier="free",
    )
)


async def _get_job_sentiment_summary(args: dict, ctx: ToolContext) -> dict:
    job = resolve_owned_job(args, ctx)
    if isinstance(job, dict):
        return job

    summary = analysis_service.get_sentiment_summary(ctx.db, job_id=job.id)
    return {
        "job_id": job.id,
        "positive_count": summary.positive_count,
        "neutral_count": summary.neutral_count,
        "negative_count": summary.negative_count,
        "average_confidence": summary.average_confidence,
        "spam_count": summary.spam_count,
        "sarcasm_count": summary.sarcasm_count,
    }


register_tool(
    Tool(
        name="get_job_sentiment_summary",
        description=(
            "Get the sentiment breakdown (positive/neutral/negative counts, average "
            "confidence, spam/sarcasm counts) for one analyzed video."
        ),
        input_schema={
            "type": "object",
            "properties": {"job_id": {"type": "integer", "description": "The analysis job id."}},
            "required": ["job_id"],
        },
        handler=_get_job_sentiment_summary,
        cost_tier="free",
    )
)


async def _get_job_health_scores(args: dict, ctx: ToolContext) -> dict:
    job = resolve_owned_job(args, ctx)
    if isinstance(job, dict):
        return job

    scores = compute_scores(ctx.db, job.id)
    if scores is None:
        return {"error": "This job has no analyzable comments yet."}

    return {
        "job_id": job.id,
        "satisfaction_score": scores.satisfaction_score,
        "community_health_score": scores.community_health_score,
        "loyalty_score": scores.loyalty_score,
    }


register_tool(
    Tool(
        name="get_job_health_scores",
        description=(
            "Get deterministic satisfaction, community-health, and loyalty scores "
            "(0-100) for one analyzed video. Computed from existing data, requires "
            "no AI provider key."
        ),
        input_schema={
            "type": "object",
            "properties": {"job_id": {"type": "integer", "description": "The analysis job id."}},
            "required": ["job_id"],
        },
        handler=_get_job_health_scores,
        cost_tier="free",
    )
)


async def _get_rule_based_highlights(args: dict, ctx: ToolContext) -> dict:
    job = resolve_owned_job(args, ctx)
    if isinstance(job, dict):
        return job

    summary = analysis_service.get_sentiment_summary(ctx.db, job_id=job.id)
    insights = get_job_insights(ctx.db, job_id=job.id, summary=summary)
    return {"job_id": job.id, "insights": insights.insights}


register_tool(
    Tool(
        name="get_rule_based_highlights",
        description=(
            "Get free, non-AI bullet-point highlights about one video's comment "
            "section (overall tone, engagement level, spam ratio, etc). Always "
            "available even with no AI provider key configured."
        ),
        input_schema={
            "type": "object",
            "properties": {"job_id": {"type": "integer", "description": "The analysis job id."}},
            "required": ["job_id"],
        },
        handler=_get_rule_based_highlights,
        cost_tier="free",
    )
)


async def _get_job_language_breakdown(args: dict, ctx: ToolContext) -> dict:
    job = resolve_owned_job(args, ctx)
    if isinstance(job, dict):
        return job

    summary = analysis_service.get_sentiment_summary(ctx.db, job_id=job.id)
    return {
        "job_id": job.id,
        "arabic_count": summary.arabic_count,
        "english_count": summary.english_count,
        "mixed_count": summary.mixed_count,
        "other_count": summary.other_count,
    }


register_tool(
    Tool(
        name="get_job_language_breakdown",
        description="Get the Arabic/English/mixed/other language distribution of comments for one analyzed video.",
        input_schema={
            "type": "object",
            "properties": {"job_id": {"type": "integer", "description": "The analysis job id."}},
            "required": ["job_id"],
        },
        handler=_get_job_language_breakdown,
        cost_tier="free",
    )
)
