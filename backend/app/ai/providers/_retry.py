import asyncio
import logging
from collections.abc import Awaitable, Callable
from typing import TypeVar

from tenacity import AsyncRetrying, RetryCallState, retry_if_exception, stop_after_attempt

logger = logging.getLogger(__name__)

T = TypeVar("T")

_MAX_ATTEMPTS = 4
_FALLBACK_MAX_WAIT_SECONDS = 60


def _extract_retry_delay_seconds(exc: BaseException) -> float | None:
    details = getattr(exc, "details", None)
    if not details:
        return None
    for item in details:
        retry_delay = getattr(item, "retry_delay", None)
        if retry_delay is not None:
            seconds = getattr(retry_delay, "seconds", 0) or 0
            nanos = getattr(retry_delay, "nanos", 0) or 0
            return seconds + nanos / 1e9
    return None


def _is_rate_limit_error(exc: BaseException) -> bool:
    name = type(exc).__name__
    if name in ("ResourceExhausted", "TooManyRequests", "RateLimitError"):
        return True
    return getattr(exc, "status_code", None) == 429 or getattr(exc, "code", None) == 429


def _wait_for_rate_limit(retry_state: RetryCallState) -> float:
    exc = retry_state.outcome.exception() if retry_state.outcome else None
    if exc is not None:
        server_delay = _extract_retry_delay_seconds(exc)
        if server_delay is not None:
            wait_seconds = server_delay + 1
            logger.info(
                "Rate limited (attempt %d/%d) — server requested a %.1fs retry delay, waiting %.1fs",
                retry_state.attempt_number,
                _MAX_ATTEMPTS,
                server_delay,
                wait_seconds,
            )
            return wait_seconds

    fallback = min(_FALLBACK_MAX_WAIT_SECONDS, 2**retry_state.attempt_number)
    logger.info(
        "Rate limited (attempt %d/%d) — no server retry delay available, backing off %.1fs",
        retry_state.attempt_number,
        _MAX_ATTEMPTS,
        fallback,
    )
    return fallback


def rate_limit_retrying() -> AsyncRetrying:
    return AsyncRetrying(
        retry=retry_if_exception(_is_rate_limit_error),
        wait=_wait_for_rate_limit,
        stop=stop_after_attempt(_MAX_ATTEMPTS),
        reraise=True,
    )


CALL_TIMEOUT_SECONDS = 7.0

BATCH_TIMEOUT_PER_ITEM_SECONDS = 0.15


def compute_batch_timeout(item_count: int) -> float:
    return max(CALL_TIMEOUT_SECONDS, BATCH_TIMEOUT_PER_ITEM_SECONDS * item_count)


async def call_with_retry_and_timeout(
    make_call: Callable[[], Awaitable[T]], timeout: float = CALL_TIMEOUT_SECONDS
) -> T:
    async for attempt in rate_limit_retrying():
        with attempt:
            try:
                return await asyncio.wait_for(make_call(), timeout=timeout)
            except TimeoutError:
                logger.warning(
                    "LLM call timed out after %.0fs — falling back to the local model's result",
                    timeout,
                )
                raise
    raise RuntimeError("rate_limit_retrying() exited without returning or raising.")
