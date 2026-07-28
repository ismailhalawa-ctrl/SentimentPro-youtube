from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.limiter import limiter
from app.database.session import get_db
from app.models.user import User
from app.schemas.assistant import (
    AssistantSessionResponse,
    AssistantSessionWithMessagesResponse,
    SendAssistantMessageRequest,
    SendAssistantMessageResponse,
)
from app.services import assistant_service

router = APIRouter(prefix="/audience-assistant", tags=["audience-assistant"])


@router.post("/sessions", response_model=AssistantSessionResponse)
async def create_assistant_session(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = assistant_service.create_session(db, current_user.id)
    return AssistantSessionResponse.model_validate(session)


@router.get("/sessions", response_model=list[AssistantSessionResponse])
async def list_assistant_sessions(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = assistant_service.list_sessions(db, current_user.id, limit=limit, offset=offset)
    return [AssistantSessionResponse.model_validate(s) for s in sessions]


@router.get("/sessions/{session_id}", response_model=AssistantSessionWithMessagesResponse)
async def get_assistant_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = assistant_service.get_session(db, session_id, current_user.id)
    if session is None:
        raise HTTPException(status_code=404, detail="Assistant session not found.")
    return AssistantSessionWithMessagesResponse.model_validate(session)


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assistant_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = assistant_service.get_session(db, session_id, current_user.id)
    if session is None:
        raise HTTPException(status_code=404, detail="Assistant session not found.")
    assistant_service.delete_session(db, session)


@router.post("/sessions/{session_id}/messages", response_model=SendAssistantMessageResponse)
@limiter.limit("10/minute;60/hour")
async def send_assistant_message(
    request: Request,
    session_id: int,
    payload: SendAssistantMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = assistant_service.get_session(db, session_id, current_user.id)
    if session is None:
        raise HTTPException(status_code=404, detail="Assistant session not found.")
    return await assistant_service.send_assistant_message(
        db, session, current_user.id, payload.question, job_id=payload.job_id
    )
