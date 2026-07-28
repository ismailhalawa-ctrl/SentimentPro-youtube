from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.v1.deps import get_current_user
from app.core.limiter import limiter
from app.models.user import User
from app.schemas.youtube import (
    CommentsRequest,
    CommentsResponse,
    UrlValidateRequest,
    UrlValidateResponse,
    VideoInfoRequest,
    VideoInfoResponse,
)
from app.services.youtube_service import (
    YouTubeApiError,
    extract_video_id,
    fetch_comments,
    fetch_video_info,
)

router = APIRouter(prefix="/youtube", tags=["youtube"])


@router.post("/validate", response_model=UrlValidateResponse)
def validate_url(
    payload: UrlValidateRequest,
    current_user: User = Depends(get_current_user),
):
    video_id = extract_video_id(payload.url)
    return UrlValidateResponse(is_valid=video_id is not None, video_id=video_id)


@router.post("/video-info", response_model=VideoInfoResponse)
@limiter.limit("20/minute")
async def video_info(
    request: Request,
    payload: VideoInfoRequest,
    current_user: User = Depends(get_current_user),
):
    video_id = extract_video_id(payload.url)
    if video_id is None:
        raise HTTPException(status_code=400, detail="Enter a valid YouTube video URL.")

    try:
        info = await fetch_video_info(video_id)
    except YouTubeApiError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e

    return VideoInfoResponse(**info)


@router.post("/comments", response_model=CommentsResponse)
@limiter.limit("10/minute")
async def comments(
    request: Request,
    payload: CommentsRequest,
    current_user: User = Depends(get_current_user),
):
    video_id = extract_video_id(payload.url)
    if video_id is None:
        raise HTTPException(status_code=400, detail="Enter a valid YouTube video URL.")

    try:
        result = await fetch_comments(
            video_id=video_id,
            max_results=payload.max_results,
            order=payload.order,
            include_replies=payload.include_replies,
            page_token=payload.page_token,
        )
    except YouTubeApiError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message) from e

    return CommentsResponse(**result)
