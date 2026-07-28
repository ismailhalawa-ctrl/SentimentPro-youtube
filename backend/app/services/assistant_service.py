import asyncio
import logging
from collections import OrderedDict
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.ai.agents.audience_assistant_agent import run_agent_turn
from app.ai.interfaces.errors import ProviderCallError, ProviderNotConfiguredError
from app.ai.tools import ToolContext
from app.core.config import settings
from app.models.assistant import AssistantMessage, AssistantSession
from app.schemas.assistant import AssistantMessageResponse, SendAssistantMessageResponse
from app.services import ai_usage_service
from app.services.ai_usage_service import UsageLimitExceededError
from app.services.billing_service import get_tier

logger = logging.getLogger(__name__)

_NOT_CONFIGURED_REASON = (
    "This feature requires an AI provider API key (OpenAI or Gemini) to be configured on the server."
)

_TITLE_MAX_LEN = 80

_AI_USAGE_CAPABILITY = "audience_assistant"

_MAX_CACHED_SESSION_LOCKS = 5_000

_session_locks: "OrderedDict[int, asyncio.Lock]" = OrderedDict()


def _get_session_lock(session_id: int) -> asyncio.Lock:
    lock = _session_locks.get(session_id)
    if lock is not None:
        _session_locks.move_to_end(session_id)
        return lock

    if len(_session_locks) >= _MAX_CACHED_SESSION_LOCKS:
        _session_locks.popitem(last=False)

    lock = asyncio.Lock()
    _session_locks[session_id] = lock
    return lock


def create_session(db: Session, user_id: int) -> AssistantSession:
    session = AssistantSession(user_id=user_id, title=None)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db: Session, session_id: int, user_id: int) -> AssistantSession | None:
    return (
        db.query(AssistantSession)
        .filter(AssistantSession.id == session_id, AssistantSession.user_id == user_id)
        .first()
    )


def list_sessions(db: Session, user_id: int, limit: int = 50, offset: int = 0) -> list[AssistantSession]:
    return (
        db.query(AssistantSession)
        .filter(AssistantSession.user_id == user_id)
        .order_by(AssistantSession.updated_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def delete_session(db: Session, session: AssistantSession) -> None:
    db.delete(session)
    db.commit()


async def send_assistant_message(
    db: Session, session: AssistantSession, user_id: int, question: str, job_id: int | None = None
) -> SendAssistantMessageResponse:
    try:
        ai_usage_service.check_usage_limit(db, user_id, tier=get_tier(db, user_id))
    except UsageLimitExceededError as exc:
        return SendAssistantMessageResponse(status="rate_limited", reason=exc.reason, message=None)

    async with _get_session_lock(session.id):
        recent_messages = (
            db.query(AssistantMessage)
            .filter(AssistantMessage.session_id == session.id)
            .order_by(AssistantMessage.created_at.desc())
            .limit(settings.audience_assistant_history_limit)
            .all()
        )
        history = [{"role": m.role, "content": m.content} for m in reversed(recent_messages)]

        user_message = AssistantMessage(
            session_id=session.id, role="user", content=question, citations_json=[], tool_calls_json=[]
        )
        db.add(user_message)

        if session.title is None:
            session.title = question[:_TITLE_MAX_LEN]
        session.updated_at = datetime.now(UTC)

        db.commit()

        ctx = ToolContext(user_id=user_id, db=db, target_job_id=job_id)

        try:
            result = await run_agent_turn(question, history, ctx)
        except ProviderNotConfiguredError:
            return SendAssistantMessageResponse(
                status="unavailable", reason=_NOT_CONFIGURED_REASON, message=None
            )
        except (ProviderCallError, LookupError) as exc:
            logger.exception("Audience assistant turn failed for session %s", session.id)
            return SendAssistantMessageResponse(status="error", reason=str(exc), message=None)

        assistant_message = AssistantMessage(
            session_id=session.id,
            role="assistant",
            content=result.answer,
            citations_json=result.citations,
            tool_calls_json=result.tool_trace,
        )
        db.add(assistant_message)
        session.updated_at = datetime.now(UTC)
        db.commit()
        db.refresh(assistant_message)

        ai_usage_service.record_usage(db, user_id, _AI_USAGE_CAPABILITY, result.tokens_in, result.tokens_out)

        return SendAssistantMessageResponse(
            status="ok", reason=None, message=AssistantMessageResponse.model_validate(assistant_message)
        )
