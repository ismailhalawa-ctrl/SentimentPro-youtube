import logging
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.config import settings
from app.core.limiter import limiter
from app.core.security import generate_secure_token
from app.database.session import get_db
from app.models.user import User
from app.schemas.user import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.services.auth_service import (
    AuthError,
    authenticate_google_user,
    authenticate_user,
    create_token_for_user,
    register_user,
    request_password_reset,
    reset_password,
)
from app.services.email_service import EmailNotConfiguredError, EmailSendError, send_password_reset_email

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

COOKIE_MAX_AGE_SECONDS = settings.jwt_access_token_expire_minutes * 60

FORGOT_PASSWORD_MESSAGE = "If that email is registered, a password reset link has been sent."

GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_OAUTH_STATE_COOKIE = "google_oauth_state"
GOOGLE_OAUTH_STATE_MAX_AGE_SECONDS = 300


def _google_redirect_uri() -> str:
    return f"{settings.backend_url}/api/v1/auth/google/callback"


def _set_session_cookie(response: Response, user: User) -> None:
    token = create_token_for_user(user)
    response.set_cookie(
        key="access_token",
        value=token,
        max_age=COOKIE_MAX_AGE_SECONDS,
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, payload: UserRegister, db: Session = Depends(get_db)):
    try:
        user = register_user(db, payload)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return user


@router.post("/login", response_model=UserResponse)
@limiter.limit("10/minute")
def login(request: Request, payload: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, payload)
    except AuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e

    _set_session_cookie(response, user)
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response):
    response.delete_cookie("access_token")


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/google/login")
@limiter.limit("20/minute")
def google_login(request: Request):
    if not settings.google_client_id or not settings.google_client_secret:
        return RedirectResponse(f"{settings.frontend_url}/login?error=google_not_configured")

    state = generate_secure_token()
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": _google_redirect_uri(),
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
    }
    redirect = RedirectResponse(f"{GOOGLE_AUTHORIZATION_ENDPOINT}?{urlencode(params)}")
    redirect.set_cookie(
        key=GOOGLE_OAUTH_STATE_COOKIE,
        value=state,
        max_age=GOOGLE_OAUTH_STATE_MAX_AGE_SECONDS,
        httponly=True,
        secure=settings.is_production,
        samesite="lax",
    )
    return redirect


@router.get("/google/callback")
@limiter.limit("20/minute")
def google_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: Session = Depends(get_db),
):
    def _fail(reason: str) -> RedirectResponse:
        redirect = RedirectResponse(f"{settings.frontend_url}/login?error={reason}")
        redirect.delete_cookie(GOOGLE_OAUTH_STATE_COOKIE)
        return redirect

    expected_state = request.cookies.get(GOOGLE_OAUTH_STATE_COOKIE)

    if error:
        return _fail("google_auth_failed")
    if not settings.google_client_id or not settings.google_client_secret:
        return _fail("google_not_configured")
    if not code or not state or not expected_state or state != expected_state:
        return _fail("google_auth_failed")

    from google.auth.transport import requests as google_requests
    from google.oauth2 import id_token as google_id_token

    try:
        with httpx.Client(timeout=10) as client:
            token_response = client.post(
                GOOGLE_TOKEN_ENDPOINT,
                data={
                    "code": code,
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uri": _google_redirect_uri(),
                    "grant_type": "authorization_code",
                },
            )
        token_response.raise_for_status()
        id_token_str = token_response.json()["id_token"]

        claims = google_id_token.verify_oauth2_token(
            id_token_str, google_requests.Request(), settings.google_client_id
        )
    except Exception:
        logger.exception("Google OAuth callback failed during code exchange or token verification")
        return _fail("google_auth_failed")

    email = claims.get("email")
    if not email or not claims.get("email_verified", False):
        return _fail("google_auth_failed")

    try:
        user = authenticate_google_user(
            db, google_id=claims["sub"], email=email, full_name=claims.get("name", "")
        )
    except Exception:
        logger.exception("Google OAuth callback failed while creating/linking the account")
        return _fail("google_auth_failed")

    if user is None:
        return _fail("google_auth_failed")
    if not user.is_active:
        return _fail("account_disabled")

    redirect = RedirectResponse(f"{settings.frontend_url}/dashboard")
    redirect.delete_cookie(GOOGLE_OAUTH_STATE_COOKIE)
    _set_session_cookie(redirect, user)
    return redirect


def _dispatch_password_reset_email(email: str, reset_link: str) -> None:
    try:
        send_password_reset_email(email, reset_link)
        logger.info("Password reset email sent to %s", email)
    except EmailNotConfiguredError:
        logger.info("Password reset requested for %s: %s", email, reset_link)
    except EmailSendError:
        logger.info("Password reset link for %s (email delivery failed): %s", email, reset_link)
    except Exception:
        logger.exception("Unexpected error sending password reset email to %s", email)
        logger.info("Password reset link for %s (email delivery failed): %s", email, reset_link)


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
@limiter.limit("5/minute")
def forgot_password(
    request: Request,
    payload: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    raw_token = request_password_reset(db, payload.email)
    if raw_token:
        reset_link = f"{settings.frontend_url}/reset-password?token={raw_token}"
        background_tasks.add_task(_dispatch_password_reset_email, payload.email, reset_link)

    return ForgotPasswordResponse(message=FORGOT_PASSWORD_MESSAGE)


@router.post("/reset-password", response_model=ForgotPasswordResponse)
@limiter.limit("10/minute")
def reset_password_route(request: Request, payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    if not reset_password(db, payload.token, payload.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This reset link is invalid or has expired. Request a new one.",
        )
    return ForgotPasswordResponse(message="Your password has been reset. You can now log in.")
