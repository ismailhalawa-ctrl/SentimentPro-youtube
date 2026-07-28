import logging

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.limiter import limiter
from app.core.security import verify_password
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import DeleteAccountRequest, UserResponse, UserUpdate
from app.services.analysis_service import clear_all_jobs
from app.services.auth_service import NameChangeCooldownError, update_full_name

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.patch("/me", response_model=UserResponse)
def update_current_user(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return update_full_name(db, current_user, payload.full_name)
    except NameChangeCooldownError as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"message": str(e), "days_remaining": e.days_remaining},
        ) from e


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
async def delete_current_user(
    request: Request,
    payload: DeleteAccountRequest,
    response: Response,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.google_id:
        expected = current_user.email.strip().lower()
        if not payload.confirmation or payload.confirmation.strip().lower() != expected:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Type your account email to confirm account deletion.",
            )
    else:
        if not payload.password or not verify_password(payload.password, current_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password.")

    user_id = current_user.id
    await clear_all_jobs(db, user_id)
    db.delete(current_user)
    db.commit()
    response.delete_cookie("access_token")
    logger.info("Account %s deleted by request", user_id)
