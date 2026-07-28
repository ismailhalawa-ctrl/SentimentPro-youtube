from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database.session import get_db
from app.models.user import User


def get_current_user(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated.",
    )

    if not access_token:
        raise credentials_error

    user_id = decode_access_token(access_token)
    if user_id is None:
        raise credentials_error

    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        raise credentials_error from None

    user = db.query(User).filter(User.id == user_id_int).first()
    if user is None or not user.is_active:
        raise credentials_error

    return user


def get_optional_current_user(
    access_token: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> User | None:
    if not access_token:
        return None

    user_id = decode_access_token(access_token)
    if user_id is None:
        return None

    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError):
        return None

    user = db.query(User).filter(User.id == user_id_int).first()
    if user is None or not user.is_active:
        return None

    return user


def get_display_name(user: User) -> str:
    if user.full_name:
        return user.full_name
    local_part = user.email.split("@")[0]
    return local_part.capitalize()
