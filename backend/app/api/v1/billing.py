import logging

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.config import settings
from app.database.session import get_db
from app.models.user import User
from app.schemas.billing import CheckoutSessionResponse, PortalSessionResponse, SubscriptionResponse
from app.services.billing_service import (
    BillingNotConfiguredError,
    create_billing_portal_session,
    create_checkout_session,
    get_tier,
    handle_webhook_event,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/subscription", response_model=SubscriptionResponse)
def get_subscription_status(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    from app.services.billing_service import get_subscription

    subscription = get_subscription(db, current_user.id)
    return SubscriptionResponse(
        tier=get_tier(db, current_user.id),
        status=subscription.status if subscription else "active",
        current_period_end=subscription.current_period_end if subscription else None,
    )


@router.post("/checkout-session", response_model=CheckoutSessionResponse)
def create_checkout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        checkout_url = create_checkout_session(
            db,
            current_user,
            success_url=f"{settings.frontend_url}/dashboard/settings?checkout=success",
            cancel_url=f"{settings.frontend_url}/pricing?checkout=cancelled",
        )
    except BillingNotConfiguredError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Subscriptions aren't available yet. Please check back soon.",
        ) from e
    return CheckoutSessionResponse(checkout_url=checkout_url)


@router.post("/portal-session", response_model=PortalSessionResponse)
def create_portal_session(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        portal_url = create_billing_portal_session(
            db, current_user, return_url=f"{settings.frontend_url}/dashboard/settings"
        )
    except BillingNotConfiguredError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)) from e
    return PortalSessionResponse(portal_url=portal_url)


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT)
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(default=""),
    db: Session = Depends(get_db),
):
    payload = await request.body()
    try:
        handle_webhook_event(db, payload, stripe_signature)
    except BillingNotConfiguredError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Stripe is not configured."
        ) from e
    except Exception as e:
        logger.exception("Failed to process Stripe webhook")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook payload.") from e
