import asyncio
import threading
import time

from app.services import analysis_service as svc


def test_cancellation_wakes_a_waiter_on_a_different_thread_promptly():
    # matches real threading: job thread (asyncio.run) vs /cancel's thread
    # (sync route handler). direct Event.set() across threads isn't
    # guaranteed to wake a waiter promptly, that's the bug this guards.
    job_id = 987654321
    result: dict[str, float | None] = {}

    async def job_loop() -> float:
        event = svc._register_job_for_cancellation(job_id)
        start = time.monotonic()
        await asyncio.wait_for(event.wait(), timeout=5)
        return time.monotonic() - start

    def run_job_thread() -> None:
        try:
            result["elapsed"] = asyncio.run(job_loop())
        except TimeoutError:
            result["elapsed"] = None

    thread = threading.Thread(target=run_job_thread)
    thread.start()
    time.sleep(0.3)  # let the job register its loop before cancelling
    try:
        svc.request_job_cancellation(job_id)
        thread.join(timeout=6)
    finally:
        svc._cancellation_events.pop(job_id, None)
        svc._cancellation_loops.pop(job_id, None)

    assert result.get("elapsed") is not None, "cancel_event.wait() never woke up (cross-thread bug regressed)"
    assert result["elapsed"] < 1.0, f"cancellation woke the waiter after {result['elapsed']:.2f}s, expected near-instant"


async def test_cancellation_before_job_registers_is_still_observed():
    # cancel arrives before the job's loop registers, should fall back to
    # direct set() not crash. test is async since
    # _register_job_for_cancellation needs a running loop.
    job_id = 123456789
    try:
        svc.request_job_cancellation(job_id)
        event = svc._register_job_for_cancellation(job_id)
        assert event.is_set()
    finally:
        svc._cancellation_events.pop(job_id, None)
        svc._cancellation_loops.pop(job_id, None)
