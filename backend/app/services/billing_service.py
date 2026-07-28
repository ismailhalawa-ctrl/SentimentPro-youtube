import logging
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.subscription import Subscription
from app.models.user import User

logger = logging.getLogger(__name__)

TIER_FREE = "free"
TIER_PRO = "pro"


class BillingNotConfiguredError(Exception):
    pass


def is_configured() -> bool:
    return bool(settings.stripe_secret_key and settings.stripe_price_id_pro)


def _stripe():
    if not settings.stripe_secret_key:
        raise BillingNotConfiguredError("Stripe is not configured.")

    import stripe

    stripe.api_key = settings.stripe_secret_key
    return stripe


def get_subscription(db: Session, user_id: int) -> Subscription | None:
    return db.query(Subscription).filter(Subscription.user_id == user_id).first()


def get_tier(db: Session, user_id: int) -> str:
    subscription = get_subscription(db, user_id)
    if subscription and subscription.status == "active":
        return subscription.tier
    return TIER_FREE


def create_checkout_session(db: Session, user: User, success_url: str, cancel_url: str) -> str:
    if not is_configured():
        raise BillingNotConfiguredError("Stripe is not configured.")

    stripe = _stripe()
    subscription = get_subscription(db, user.id)

    try:
        customer_id = subscription.stripe_customer_id if subscription else None
        if not customer_id:
            customer = stripe.Customer.create(email=user.email, name=user.full_name)
            customer_id = customer.id

        session = stripe.checkout.Session.create(
            customer=customer_id,
            mode="subscription",
            line_items=[{"price": settings.stripe_price_id_pro, "quantity": 1}],
            success_url=success_url,
            cancel_url=cancel_url,
            client_reference_id=str(user.id),
        )
    except stripe.StripeError as e:
        logger.error("Stripe checkout session creation failed: %s", e)
        raise BillingNotConfiguredError("Subscriptions aren't available yet.") from e

    return session.url


def create_billing_portal_session(db: Session, user: User, return_url: str) -> str:
    if not is_configured():
        raise BillingNotConfiguredError("Stripe is not configured.")

    subscription = get_subscription(db, user.id)
    if not subscription or not subscription.stripe_customer_id:
        raise BillingNotConfiguredError("No billing account found for this user.")

    stripe = _stripe()
    try:
        session = stripe.billing_portal.Session.create(
            customer=subscription.stripe_customer_id, return_url=return_url
        )
    except stripe.StripeError as e:
        logger.error("Stripe billing portal session creation failed: %s", e)
        raise BillingNotConfiguredError("The billing portal isn't available right now.") from e

    return session.url


def _upsert_subscription(
    db: Session,
    *,
    user_id: int,
    tier: str,
    status: str,
    stripe_customer_id: str | None,
    stripe_subscription_id: str | None,
    current_period_end: datetime | None,
) -> None:
    subscription = get_subscription(db, user_id)
    if subscription is None:
        subscription = Subscription(user_id=user_id)
        db.add(subscription)

    subscription.tier = tier
    subscription.status = status
    if stripe_customer_id:
        subscription.stripe_customer_id = stripe_customer_id
    if stripe_subscription_id:
        subscription.stripe_subscription_id = stripe_subscription_id
    subscription.current_period_end = current_period_end
    db.commit()


def handle_webhook_event(db: Session, payload: bytes, signature: str) -> None:
    if not settings.stripe_webhook_secret:
        raise BillingNotConfiguredError("Stripe webhook secret is not configured.")

    stripe = _stripe()
    event = stripe.Webhook.construct_event(payload, signature, settings.stripe_webhook_secret)
    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        user_id = data.get("client_reference_id")
        if not user_id:
            return
        _upsert_subscription(
            db,
            user_id=int(user_id),
            tier=TIER_PRO,
            status="active",
            stripe_customer_id=data.get("customer"),
            stripe_subscription_id=data.get("subscription"),
            current_period_end=None,
        )
    elif event_type in ("customer.subscription.updated", "customer.subscription.deleted"):
        customer_id = data.get("customer")
        subscription = db.query(Subscription).filter(Subscription.stripe_customer_id == customer_id).first()
        if subscription is None:
            return

        status = data.get("status", "canceled")
        period_end_ts = data.get("current_period_end")
        period_end = datetime.fromtimestamp(period_end_ts, tz=UTC) if period_end_ts else None
        subscription.status = "active" if status == "active" else "canceled"
        subscription.tier = TIER_PRO if status == "active" else TIER_FREE
        subscription.current_period_end = period_end
        db.commit()
    else:
        logger.info("Unhandled Stripe webhook event type: %s", event_type)
