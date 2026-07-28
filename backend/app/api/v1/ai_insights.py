from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.ai.interfaces.capability import Capability
from app.api.v1.deps import get_current_user
from app.core.limiter import limiter
from app.database.session import get_db
from app.models.user import User
from app.schemas.ai_insights import AIFeatureResponse
from app.services.analysis_service import get_job
from app.services.comment_extraction_service import get_or_generate_extraction
from app.services.insight_service import get_or_generate_audience_intelligence, get_or_generate_insight

router = APIRouter(prefix="/analysis", tags=["ai-insights"])


@router.get("/jobs/{job_id}/ai-insights/{capability}", response_model=AIFeatureResponse)
@limiter.limit("30/minute")
async def get_ai_insight(
    request: Request,
    job_id: int,
    capability: Capability,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")

    return await get_or_generate_insight(db, job, capability, current_user.id)


@router.get("/jobs/{job_id}/comment-insights/{capability}", response_model=AIFeatureResponse)
@limiter.limit("30/minute")
async def get_comment_insight(
    request: Request,
    job_id: int,
    capability: Capability,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")

    return await get_or_generate_extraction(db, job, capability, current_user.id)


@router.get("/jobs/{job_id}/audience-intelligence", response_model=AIFeatureResponse)
@limiter.limit("30/minute")
async def get_audience_intelligence(
    request: Request,
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    job = get_job(db, job_id=job_id, owner_id=current_user.id)
    if job is None:
        raise HTTPException(status_code=404, detail="Analysis job not found.")

    return await get_or_generate_audience_intelligence(db, job, current_user.id)
