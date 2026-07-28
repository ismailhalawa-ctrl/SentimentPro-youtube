from app.ai.tools.context import ToolContext
from app.models.analysis_job import AnalysisJob
from app.services import analysis_service

NOT_FOUND_ERROR = {"error": "Job not found or not accessible."}


def resolve_owned_job(args: dict, ctx: ToolContext) -> AnalysisJob | dict:
    job_id = ctx.target_job_id if ctx.target_job_id is not None else args.get("job_id")
    if job_id is None:
        return {"error": "job_id is required."}

    try:
        job_id = int(job_id)
    except (TypeError, ValueError):
        return {"error": "job_id must be an integer."}

    job = analysis_service.get_job(ctx.db, job_id=job_id, owner_id=ctx.user_id)
    if job is None:
        return dict(NOT_FOUND_ERROR)

    return job
