from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Request, status
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session

from app.ai.interfaces.capability import Capability
from app.api.v1.deps import get_current_user
from app.core.limiter import limiter
from app.database.session import get_db
from app.models.analysis_job import AnalysisJobStatus
from app.models.job_insight import JobInsight
from app.models.user import User
from app.schemas.analysis import (
    AnalysisJobListResponse,
    AnalysisJobResponse,
    CommentsListResponse,
    CreateAnalysisJobRequest,
    InsightsResponse,
    KeywordsResponse,
    TopicsResponse,
)
from app.services.analysis_service import (
    clear_all_jobs,
    create_job,
    delete_job,
    get_job,
    get_sentiment_summaries_for_jobs,
    get_sentiment_summary,
    list_jobs,
    request_job_cancellation,
    run_analysis_job,
)
from app.services.export_service import build_csv_export, build_excel_export, build_pdf_export
from app.services.insights_service import (
    get_job_comment_rows,
    get_job_comments,
    get_job_insights,
    get_job_keywords,
    get_job_topics,
)

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/jobs", response_model=AnalysisJobResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("5/minute;30/hour")
def create_analysis_job(
    request: Request,
    payload: CreateAnalysisJobRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        job = create_job(db, owner_id=current_user.id, payload=payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    background_tasks.add_task(run_analysis_job, job.id)

    return AnalysisJobResponse.model_validate(job)


@router.get("/jobs", response_model=AnalysisJobListResponse)
def get_analysis_jobs(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jobs = list_jobs(db, owner_id=current_user.id, limit=limit, offset=offset)
    summaries = get_sentiment_summaries_for_jobs(db, job_ids=[job.id for job in jobs])

    responses = []
    for job in jobs:
        response = AnalysisJobResponse.model_validate(job)
        response.sentiment_summary = summaries.get(job.id)
        responses.append(response)

    return AnalysisJobListResponse(jobs=responses)


@router.get("/jobs/{job_id}", response_model=AnalysisJobResponse)
def get_analysis_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")

    response = AnalysisJobResponse.model_validate(job)
    response.sentiment_summary = get_sentiment_summary(db, job_id=job_id)
    return response


@router.post("/jobs/{job_id}/cancel", response_model=AnalysisJobResponse)
def cancel_analysis_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")

    if job.status not in (AnalysisJobStatus.PENDING, AnalysisJobStatus.PROCESSING):
        raise HTTPException(
            status_code=400,
            detail=f"Job is already {job.status.value} and cannot be cancelled.",
        )

    request_job_cancellation(job_id)
    return AnalysisJobResponse.model_validate(job)


@router.delete("/jobs/clear-all")
async def clear_all_analysis_jobs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted_count = await clear_all_jobs(db, owner_id=current_user.id)
    return {"deleted_count": deleted_count}


@router.delete("/jobs/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")

    await delete_job(db, job)


@router.get("/jobs/{job_id}/keywords", response_model=KeywordsResponse)
def get_analysis_keywords(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")
    return get_job_keywords(db, job_id=job_id)


@router.get("/jobs/{job_id}/topics", response_model=TopicsResponse)
def get_analysis_topics(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")
    return get_job_topics(db, job_id=job_id)


def _resolve_insights(db: Session, job_id: int) -> InsightsResponse:
    dynamic = (
        db.query(JobInsight)
        .filter(JobInsight.job_id == job_id, JobInsight.capability == Capability.DYNAMIC_AI_INSIGHTS.value)
        .order_by(JobInsight.created_at.desc())
        .first()
    )
    if dynamic is not None:
        insights = dynamic.result_json.get("insights", [])
        if insights:
            return InsightsResponse(insights=insights, source="ai")

    summary = get_sentiment_summary(db, job_id=job_id)
    return get_job_insights(db, job_id=job_id, summary=summary)


@router.get("/jobs/{job_id}/insights", response_model=InsightsResponse)
def get_analysis_insights(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")
    return _resolve_insights(db, job_id)


@router.get("/jobs/{job_id}/comments", response_model=CommentsListResponse)
def get_analysis_comments(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")
    return get_job_comments(db, job_id=job_id)


@router.get("/jobs/{job_id}/export")
def export_analysis_job(
    job_id: int,
    format: str = Query(default="csv", pattern="^(csv|excel|pdf)$"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")
    if job.status != AnalysisJobStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Job is {job.status.value} and cannot be exported until it completes.",
        )

    rows = get_job_comment_rows(db, job_id)
    filename_base = f"analysis_{job.video_id}_{job_id}"

    if format == "csv":
        csv_rows = [(comment, sentiment) for comment, sentiment, _spam, _sarcasm in rows]
        content = build_csv_export(job, csv_rows)
        return StreamingResponse(
            iter([content]),
            media_type="text/csv; charset=utf-8",
            headers={"Content-Disposition": f'attachment; filename="{filename_base}.csv"'},
        )

    if format == "excel":
        content = build_excel_export(job, get_sentiment_summary(db, job_id=job_id), rows)
        return Response(
            content=content,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{filename_base}.xlsx"'},
        )

    summary = get_sentiment_summary(db, job_id=job_id)
    insights = _resolve_insights(db, job_id).insights
    content = build_pdf_export(job, summary, insights)
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename_base}.pdf"'},
    )
