import logging

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.orm import Session

from app.api.v1.deps import get_optional_current_user
from app.core.config import settings
from app.core.limiter import limiter
from app.database.session import get_db
from app.models.support_message import SupportMessage
from app.models.user import User
from app.schemas.support import SupportMessageCreate, SupportMessageResponse
from app.services.email_service import (
    EmailNotConfiguredError,
    EmailSendError,
    send_contact_notification_email,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/support", tags=["support"])


def _dispatch_contact_notification(name: str, email: str, message: str) -> None:
    try:
        send_contact_notification_email(name, email, message)
        logger.info("Contact notification email sent for message from %s", email)
    except EmailNotConfiguredError:
        pass
    except EmailSendError:
        logger.error("Failed to deliver contact notification email for message from %s", email)
    except Exception:
        logger.exception("Unexpected error sending contact notification email for message from %s", email)


@router.post("/contact", response_model=SupportMessageResponse)
@limiter.limit("5/minute")
def submit_contact_message(
    request: Request,
    payload: SupportMessageCreate,
    background_tasks: BackgroundTasks,
    current_user: User | None = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
):
    entry = SupportMessage(
        user_id=current_user.id if current_user else None,
        name=payload.name,
        email=payload.email,
        message=payload.message,
    )
    db.add(entry)
    db.commit()

    if settings.support_email:
        background_tasks.add_task(
            _dispatch_contact_notification, payload.name, payload.email, payload.message
        )

    return SupportMessageResponse(message="Thanks for reaching out — we'll get back to you soon.")
