from datetime import UTC, datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.ai_usage import AIUsageLog


class UsageLimitExceededError(RuntimeError):
    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


def _day_start(now: datetime) -> datetime:
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def _month_start(now: datetime) -> datetime:
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _usage_totals(db: Session, user_id: int, since: datetime) -> tuple[int, int]:
    request_count, token_total = (
        db.query(
            func.count(AIUsageLog.id),
            func.coalesce(func.sum(AIUsageLog.tokens_in + AIUsageLog.tokens_out), 0),
        )
        .filter(AIUsageLog.user_id == user_id, AIUsageLog.created_at >= since)
        .one()
    )
    return request_count or 0, token_total or 0


def _limits_for_tier(tier: str) -> tuple[int, int, int, int]:
    if tier == "pro":
        return (
            settings.ai_daily_request_limit_pro,
            settings.ai_daily_token_limit_pro,
            settings.ai_monthly_request_limit_pro,
            settings.ai_monthly_token_limit_pro,
        )
    return (
        settings.ai_daily_request_limit,
        settings.ai_daily_token_limit,
        settings.ai_monthly_request_limit,
        settings.ai_monthly_token_limit,
    )


def check_usage_limit(db: Session, user_id: int, tier: str = "free") -> None:
    now = datetime.now(UTC)
    daily_request_limit, daily_token_limit, monthly_request_limit, monthly_token_limit = _limits_for_tier(
        tier
    )

    daily_requests, daily_tokens = _usage_totals(db, user_id, _day_start(now))
    if daily_requests >= daily_request_limit:
        raise UsageLimitExceededError(
            f"You've reached today's limit of {daily_request_limit} AI assistant "
            "messages. Please try again tomorrow."
        )
    if daily_tokens >= daily_token_limit:
        raise UsageLimitExceededError(
            "You've reached today's AI usage budget for this account. Please try again tomorrow."
        )

    monthly_requests, monthly_tokens = _usage_totals(db, user_id, _month_start(now))
    if monthly_requests >= monthly_request_limit:
        raise UsageLimitExceededError(
            f"You've reached this month's limit of {monthly_request_limit} AI assistant messages."
        )
    if monthly_tokens >= monthly_token_limit:
        raise UsageLimitExceededError("You've reached this month's AI usage budget for this account.")


def record_usage(db: Session, user_id: int, capability: str, tokens_in: int, tokens_out: int) -> None:
    db.add(
        AIUsageLog(
            user_id=user_id,
            capability=capability,
            tokens_in=max(tokens_in, 0),
            tokens_out=max(tokens_out, 0),
        )
    )
    db.commit()
