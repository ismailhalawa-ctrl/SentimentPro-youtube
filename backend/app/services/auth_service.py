import logging
import math
from datetime import UTC, datetime, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    generate_secure_token,
    hash_password,
    hash_token,
    verify_password,
)
from app.models.user import User
from app.schemas.user import UserLogin, UserRegister

logger = logging.getLogger(__name__)

NAME_CHANGE_COOLDOWN_DAYS = 60
RESET_TOKEN_TTL_MINUTES = 60


class AuthError(Exception):
    pass


class NameChangeCooldownError(Exception):
    def __init__(self, days_remaining: int):
        self.days_remaining = days_remaining
        super().__init__(
            f"You can change your name again in {days_remaining} day{'s' if days_remaining != 1 else ''}."
        )


def _as_aware_utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo is not None else dt.replace(tzinfo=UTC)


def get_user_by_email(db: Session, email: str) -> User | None:
    normalized_email = email.strip().lower()
    return db.query(User).filter(User.email == normalized_email).first()


def register_user(db: Session, payload: UserRegister) -> User:
    if get_user_by_email(db, payload.email):
        raise AuthError("Email is already registered.")

    user = User(
        full_name=payload.full_name,
        email=payload.email.strip().lower(),
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise AuthError("Email is already registered.") from e
    db.refresh(user)
    return user


def authenticate_user(db: Session, payload: UserLogin) -> User:
    user = get_user_by_email(db, payload.email)

    generic_error = AuthError("Invalid email or password.")

    if not user or not user.is_active:
        raise generic_error
    if not verify_password(payload.password, user.hashed_password):
        raise generic_error

    return user


def create_token_for_user(user: User) -> str:
    return create_access_token(subject=str(user.id))


def update_full_name(db: Session, user: User, new_full_name: str) -> User:
    if user.last_name_change is not None:
        elapsed = datetime.now(UTC) - _as_aware_utc(user.last_name_change)
        remaining = timedelta(days=NAME_CHANGE_COOLDOWN_DAYS) - elapsed
        if remaining > timedelta(0):
            days_remaining = max(1, math.ceil(remaining.total_seconds() / 86400))
            raise NameChangeCooldownError(days_remaining=days_remaining)

    user.full_name = new_full_name
    user.last_name_change = datetime.now(UTC)
    db.commit()
    db.refresh(user)
    return user


def authenticate_google_user(db: Session, *, google_id: str, email: str, full_name: str) -> User | None:
    normalized_email = email.strip().lower()

    user = db.query(User).filter(User.google_id == google_id).first()
    if user:
        return user

    user = get_user_by_email(db, normalized_email)
    if user:
        user.google_id = google_id
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return db.query(User).filter(User.google_id == google_id).first() or get_user_by_email(
                db, normalized_email
            )
        db.refresh(user)
        return user

    user = User(
        full_name=full_name.strip() or normalized_email.split("@")[0],
        email=normalized_email,
        hashed_password=hash_password(generate_secure_token()),
        google_id=google_id,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return db.query(User).filter(User.google_id == google_id).first() or get_user_by_email(
            db, normalized_email
        )
    db.refresh(user)
    return user


def request_password_reset(db: Session, email: str) -> str | None:
    user = get_user_by_email(db, email)
    if not user:
        return None

    raw_token = generate_secure_token()
    user.reset_token_hash = hash_token(raw_token)
    user.reset_token_expires_at = datetime.now(UTC) + timedelta(minutes=RESET_TOKEN_TTL_MINUTES)
    db.commit()
    return raw_token


def reset_password(db: Session, token: str, new_password: str) -> bool:
    token_hash = hash_token(token)
    user = db.query(User).filter(User.reset_token_hash == token_hash).first()

    if not user:
        return False

    is_expired = user.reset_token_expires_at is None or _as_aware_utc(
        user.reset_token_expires_at
    ) < datetime.now(UTC)

    user.reset_token_hash = None
    user.reset_token_expires_at = None

    if is_expired:
        db.commit()
        return False

    user.hashed_password = hash_password(new_password)
    db.commit()
    return True
