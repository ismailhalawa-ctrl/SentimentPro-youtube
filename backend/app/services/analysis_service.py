import asyncio
import contextlib
import logging
import time
from collections import defaultdict
from collections.abc import Callable
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.result import AnalysisResult
from app.ai.pipelines.analysis_pipeline import is_trivial_comment, local_heuristic_result, should_escalate
from app.ai.pipelines.decision_policy import resolve_final
from app.ai.postprocessors.confidence_calibrator import resolve_sentiment_decision
from app.ai.preprocessors.language_detector import detect_language
from app.ai.preprocessors.semantic_canonicalizer import canonical_signature
from app.ai.preprocessors.text_cleaner import clean_text
from app.ai.rules.emoji_boost import is_engagement_comment
from app.ai.rules.signal_bundle import SignalBundle, extract_signals
from app.ai.rules.spam_detector import detect_spam
from app.ai.tasks.capability_task import run_capability_batch
from app.core.config import settings
from app.database.session import SessionLocal
from app.models.analysis_job import AnalysisJob, AnalysisJobStatus
from app.models.comment_analysis import CommentAnalysis
from app.models.comment_analysis_result import CommentAnalysisResult
from app.models.job_insight import JobInsight
from app.schemas.analysis import CreateAnalysisJobRequest, SentimentSummary
from app.services.embedding_service import index_job_comments
from app.services.youtube_service import (
    YouTubeApiError,
    extract_video_id,
    fetch_comments,
    fetch_video_info,
)

logger = logging.getLogger(__name__)

BATCH_SIZE = settings.fast_mode_batch_size


_PREPASS_PROGRESS_START = 30
_PREPASS_PROGRESS_END = 70
_REFINE_PROGRESS_END = 95


def _format_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m {secs}s" if secs else f"{minutes}m"
    return f"{secs}s"


def _confidence_bucket(confidence: float | None) -> str:
    if confidence is None:
        return "unknown"
    if confidence < settings.hybrid_escalation_confidence_threshold:
        return "low"
    if confidence < 0.85:
        return "medium"
    return "high"


def _uncertainty_score(bundle: SignalBundle, result: AnalysisResult) -> float:
    score = 0.0
    all_probs = (result.data or {}).get("all_probs")
    if all_probs and len(all_probs) >= 2:
        ranked = sorted(all_probs.values(), reverse=True)
        score += max(0.0, 1.0 - (ranked[0] - ranked[1]))
    else:
        score += 0.5

    if bundle.opinion_polarity is not None and bundle.opinion_polarity != result.label:
        score += 1.0
    if bundle.mixed_opinion:
        score += 0.5
    if bundle.contrast_detected:
        score += 0.3

    if bundle.is_sarcasm:
        score += 0.5

    if len(bundle.cleaned_text.split()) > 40:
        score += 0.3

    return score


def _select_llm_sample(
    rows: list[CommentAnalysis],
    fast_results: dict[int, AnalysisResult],
    bundle_cache: dict[int, SignalBundle],
    sample_size: int,
) -> set[int]:
    if len(rows) <= sample_size:
        return {row.id for row in rows}

    strata: dict[tuple, list[CommentAnalysis]] = defaultdict(list)
    for row in rows:
        result = fast_results[row.id]
        strata[(result.label, _confidence_bucket(result.confidence), row.language or "other")].append(row)

    total = len(rows)
    min_per_stratum = settings.llm_sample_min_per_stratum
    chosen: set[int] = set()
    for members in strata.values():
        ranked_members = sorted(
            members,
            key=lambda row: _uncertainty_score(bundle_cache[row.id], fast_results[row.id]),
            reverse=True,
        )
        share = max(min_per_stratum, round(sample_size * len(members) / total))
        for row in ranked_members[: min(share, len(members))]:
            chosen.add(row.id)
    return chosen


def _write_comment_result(
    db: Session,
    job: AnalysisJob,
    signature_groups: dict[str, list[CommentAnalysis]],
    signature_cache: dict[int, str],
    bundle_cache: dict[int, SignalBundle],
    is_engagement_flags: dict[int, bool],
    confidence_threshold: float,
    row: CommentAnalysis,
    result: AnalysisResult,
    tag: dict,
) -> int:
    group = signature_groups[signature_cache[row.id]]
    all_probs = (result.data or {}).get("all_probs")
    base_data = {k: v for k, v in (result.data or {}).items() if k != "all_probs"}
    for member in group:
        label, confidence, adjustment_meta = resolve_sentiment_decision(
            result.label or "neutral",
            result.confidence if result.confidence is not None else 0.5,
            all_probs,
            bundle_cache[member.id],
            is_spam=False,
            is_engagement=is_engagement_flags[member.id],
            confidence_threshold=confidence_threshold,
        )
        db.add(
            CommentAnalysisResult(
                job_id=job.id,
                comment_id=member.id,
                capability=result.capability.value,
                provider_id=result.provider_id,
                mode=result.mode.value,
                label=label,
                confidence=confidence,
                processing_time_ms=result.processing_time_ms,
                result_json={**base_data, **tag, **adjustment_meta},
            )
        )
    return len(group)


def _compute_aggregate_stats(rows: list[CommentAnalysis], fast_results: dict[int, AnalysisResult]) -> dict:
    total = len(rows)
    if total == 0:
        return {
            "total_comments": 0,
            "positive_pct": 0,
            "neutral_pct": 0,
            "negative_pct": 0,
            "top_language": "unknown",
        }

    label_counts: dict[str, int] = defaultdict(int)
    language_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        label_counts[fast_results[row.id].label or "neutral"] += 1
        language_counts[row.language or "other"] += 1

    top_language = max(language_counts, key=lambda lang: language_counts[lang])
    return {
        "total_comments": total,
        "positive_pct": round(100 * label_counts["positive"] / total, 1),
        "neutral_pct": round(100 * label_counts["neutral"] / total, 1),
        "negative_pct": round(100 * label_counts["negative"] / total, 1),
        "top_language": top_language,
    }


def _extract_batch_ai_insights(wave_results: list[list[AnalysisResult]]) -> list[str] | None:
    found: list[str] | None = None
    for batch in wave_results:
        for result in batch:
            if result.data and "_batch_ai_insights" in result.data:
                insights = result.data.pop("_batch_ai_insights")
                if found is None:
                    found = insights
    return found


def _save_dynamic_ai_insights(
    db: Session, job: AnalysisJob, insights: list[str], provider_id: str, mode: AnalysisMode
) -> None:
    db.add(
        JobInsight(
            job_id=job.id,
            capability=Capability.DYNAMIC_AI_INSIGHTS.value,
            provider_id=provider_id,
            mode=mode.value,
            result_json={"insights": insights},
        )
    )


def _group_rows_by_signature(
    rows: list[CommentAnalysis], signature_cache: dict[int, str]
) -> dict[str, list[CommentAnalysis]]:
    groups: dict[str, list[CommentAnalysis]] = {}
    for row in rows:
        groups.setdefault(signature_cache[row.id], []).append(row)
    return groups


_cancellation_events: dict[int, asyncio.Event] = {}
# job runs in its own thread/loop (BackgroundTasks + asyncio.run), /cancel
# hits a different thread. asyncio.Event.set() from a foreign thread doesn't
# reliably wake a waiter on another loop, need call_soon_threadsafe or the
# mid-wave interrupt is flaky (is_set() poll at wave boundaries still works,
# that's just a bool read). tracking each job's loop so we can do that.
_cancellation_loops: dict[int, asyncio.AbstractEventLoop] = {}


def _register_job_for_cancellation(job_id: int) -> asyncio.Event:
    event = _cancellation_events.setdefault(job_id, asyncio.Event())
    _cancellation_loops[job_id] = asyncio.get_running_loop()
    return event


def request_job_cancellation(job_id: int) -> bool:
    event = _cancellation_events.setdefault(job_id, asyncio.Event())
    loop = _cancellation_loops.get(job_id)
    if loop is not None:
        loop.call_soon_threadsafe(event.set)
    else:
        # no loop registered yet = job hasn't started waiting, direct set()
        # is fine here (is_set() will read True once it checks)
        event.set()
    return True


_LANGUAGE_COUNT_FIELD = {
    "ar": "arabic_count",
    "en": "english_count",
    "mixed": "mixed_count",
    "other": "other_count",
}


def create_job(db: Session, owner_id: int, payload: CreateAnalysisJobRequest) -> AnalysisJob:
    video_id = extract_video_id(payload.url)
    if video_id is None:
        raise ValueError("Enter a valid YouTube video URL.")

    job = AnalysisJob(
        owner_id=owner_id,
        video_url=payload.url,
        video_id=video_id,
        status=AnalysisJobStatus.PENDING,
        progress_percentage=0,
        options_json=payload.model_dump(),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def get_job(db: Session, job_id: int, owner_id: int) -> AnalysisJob | None:
    return db.query(AnalysisJob).filter(AnalysisJob.id == job_id, AnalysisJob.owner_id == owner_id).first()


def list_jobs(db: Session, owner_id: int, limit: int = 50, offset: int = 0) -> list[AnalysisJob]:
    return (
        db.query(AnalysisJob)
        .filter(AnalysisJob.owner_id == owner_id)
        .order_by(AnalysisJob.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


async def delete_job(db: Session, job: AnalysisJob) -> None:
    from app.models.chat import ChatMessage, ChatSession
    from app.models.embedding_index import EmbeddingIndex
    from app.models.job_insight import JobInsight
    from app.services.embedding_service import collection_name_for_job

    job_id = job.id

    if job.status in (AnalysisJobStatus.PENDING, AnalysisJobStatus.PROCESSING):
        request_job_cancellation(job_id)

    try:
        from app.ai.rag.vector_store_registry import get_vector_store

        await get_vector_store().delete_collection(collection_name_for_job(job_id))
    except Exception:
        logger.exception("Failed to purge vector index for job %s (deletion continues)", job_id)

    session_ids = [row.id for row in db.query(ChatSession.id).filter(ChatSession.job_id == job_id).all()]
    if session_ids:
        db.query(ChatMessage).filter(ChatMessage.session_id.in_(session_ids)).delete(
            synchronize_session=False
        )
    db.query(ChatSession).filter(ChatSession.job_id == job_id).delete(synchronize_session=False)
    db.query(CommentAnalysisResult).filter(CommentAnalysisResult.job_id == job_id).delete(
        synchronize_session=False
    )
    db.query(JobInsight).filter(JobInsight.job_id == job_id).delete(synchronize_session=False)
    db.query(EmbeddingIndex).filter(EmbeddingIndex.job_id == job_id).delete(synchronize_session=False)
    db.query(CommentAnalysis).filter(CommentAnalysis.job_id == job_id).delete(synchronize_session=False)
    db.query(AnalysisJob).filter(AnalysisJob.id == job_id).delete(synchronize_session=False)
    db.commit()

    logger.info("Deleted analysis job %s", job_id)


async def clear_all_jobs(db: Session, owner_id: int) -> int:
    job_ids = [row.id for row in db.query(AnalysisJob.id).filter(AnalysisJob.owner_id == owner_id).all()]
    for job_id in job_ids:
        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
        if job is not None:
            await delete_job(db, job)
    return len(job_ids)


def _apply_sentiment_counts(summary: SentimentSummary, label: str, count: int) -> None:
    if label == "positive":
        summary.positive_count = count
    elif label == "negative":
        summary.negative_count = count
    elif label == "neutral":
        summary.neutral_count = count


def get_sentiment_summaries_for_jobs(db: Session, job_ids: list[int]) -> dict[int, SentimentSummary]:
    if not job_ids:
        return {}

    summaries: dict[int, SentimentSummary] = {job_id: SentimentSummary() for job_id in job_ids}

    sentiment_rows = (
        db.query(
            CommentAnalysisResult.job_id,
            CommentAnalysisResult.label,
            func.count(),
            func.avg(CommentAnalysisResult.confidence),
        )
        .filter(
            CommentAnalysisResult.job_id.in_(job_ids),
            CommentAnalysisResult.capability == Capability.SENTIMENT.value,
        )
        .group_by(CommentAnalysisResult.job_id, CommentAnalysisResult.label)
        .all()
    )
    weighted_sums: dict[int, float] = {job_id: 0.0 for job_id in job_ids}
    totals: dict[int, int] = {job_id: 0 for job_id in job_ids}
    for job_id, label, count, avg_confidence in sentiment_rows:
        _apply_sentiment_counts(summaries[job_id], label, count)
        if avg_confidence is not None:
            weighted_sums[job_id] += avg_confidence * count
            totals[job_id] += count
    for job_id, summary in summaries.items():
        if totals[job_id] > 0:
            summary.average_confidence = weighted_sums[job_id] / totals[job_id]

    _apply_flag_counts(db, job_ids, summaries, Capability.SPAM, "spam", "spam_count")
    _apply_flag_counts(db, job_ids, summaries, Capability.SARCASM, "sarcastic", "sarcasm_count")
    _apply_language_counts(db, job_ids, summaries)

    return summaries


def _apply_flag_counts(
    db: Session,
    job_ids: list[int],
    summaries: dict[int, SentimentSummary],
    capability: Capability,
    positive_label: str,
    field_name: str,
) -> None:
    rows = (
        db.query(CommentAnalysisResult.job_id, func.count())
        .filter(
            CommentAnalysisResult.job_id.in_(job_ids),
            CommentAnalysisResult.capability == capability.value,
            CommentAnalysisResult.label == positive_label,
        )
        .group_by(CommentAnalysisResult.job_id)
        .all()
    )
    for job_id, count in rows:
        setattr(summaries[job_id], field_name, count)


def _apply_language_counts(db: Session, job_ids: list[int], summaries: dict[int, SentimentSummary]) -> None:
    rows = (
        db.query(CommentAnalysis.job_id, CommentAnalysis.language, func.count())
        .filter(CommentAnalysis.job_id.in_(job_ids), CommentAnalysis.language.isnot(None))
        .group_by(CommentAnalysis.job_id, CommentAnalysis.language)
        .all()
    )
    for job_id, language, count in rows:
        field_name = _LANGUAGE_COUNT_FIELD.get(language)
        if field_name:
            setattr(summaries[job_id], field_name, count)


def get_sentiment_summary(db: Session, job_id: int) -> SentimentSummary:
    return get_sentiment_summaries_for_jobs(db, [job_id])[job_id]


def run_analysis_job(job_id: int) -> None:
    db = SessionLocal()
    try:
        asyncio.run(_run_analysis_job(db, job_id))
    except Exception as e:
        logger.exception("Analysis job %s failed", job_id)
        job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
        if job:
            job.status = AnalysisJobStatus.FAILED
            job.error_message = str(e)[:1024]
            db.commit()
    finally:
        db.close()


async def _run_analysis_job(db: Session, job_id: int) -> None:
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()
    if job is None:
        logger.error("Analysis job %s not found when background task started", job_id)
        return

    cancel_event = _register_job_for_cancellation(job.id)
    try:
        await _run_analysis_job_body(db, job, cancel_event)
    finally:
        _cancellation_events.pop(job.id, None)
        _cancellation_loops.pop(job.id, None)


def _cancel_job(db: Session, job: AnalysisJob) -> None:
    job.status = AnalysisJobStatus.CANCELLED
    job.current_step = None
    db.commit()
    logger.info("Analysis job %s cancelled by user request", job.id)


async def _run_sentiment_waves(
    db: Session,
    job: AnalysisJob,
    cancel_event: asyncio.Event,
    rows: list[CommentAnalysis],
    bundle_cache: dict[int, SignalBundle],
    mode: AnalysisMode,
    wave_size: int,
    sub_batch_size: int,
    on_wave: Callable[[list[list[CommentAnalysis]], list[list[AnalysisResult]]], None],
    aggregate_stats: dict | None = None,
) -> bool:
    for wave_start in range(0, len(rows), wave_size):
        if cancel_event.is_set():
            _cancel_job(db, job)
            return False

        wave_slice = rows[wave_start : wave_start + wave_size]
        wave_batches = [wave_slice[i : i + sub_batch_size] for i in range(0, len(wave_slice), sub_batch_size)]

        gather_task = asyncio.ensure_future(
            asyncio.gather(
                *[
                    run_capability_batch(
                        texts=[bundle_cache[row.id].cleaned_text for row in batch],
                        capability=Capability.SENTIMENT,
                        mode=mode,
                        aggregate_stats=aggregate_stats,
                    )
                    for batch in wave_batches
                ]
            )
        )
        cancel_wait_task = asyncio.ensure_future(cancel_event.wait())
        wait_tasks: set[asyncio.Future[Any]] = {gather_task, cancel_wait_task}
        try:
            await asyncio.wait(wait_tasks, return_when=asyncio.FIRST_COMPLETED)
        finally:
            if not cancel_wait_task.done():
                cancel_wait_task.cancel()

        if not gather_task.done():
            gather_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await gather_task
            _cancel_job(db, job)
            return False

        wave_results = gather_task.result()
        on_wave(wave_batches, wave_results)

    return True


async def _run_fast_prepass(
    db: Session,
    job: AnalysisJob,
    cancel_event: asyncio.Event,
    rows: list[CommentAnalysis],
    bundle_cache: dict[int, SignalBundle],
    progress_start: int,
    progress_end: int,
) -> dict[int, AnalysisResult] | None:
    fast_results: dict[int, AnalysisResult] = {}
    total_rows = len(rows)
    phase_start = time.monotonic()

    def _collect(wave_batches: list[list[CommentAnalysis]], wave_results: list[list]) -> None:
        for batch, results in zip(wave_batches, wave_results, strict=True):
            for row, result in zip(batch, results, strict=True):
                fast_results[row.id] = result

        done = len(fast_results)
        elapsed = time.monotonic() - phase_start
        rate = done / elapsed if elapsed > 0 else 0.0
        eta_suffix = ""
        if rate > 0 and done < total_rows:
            eta_suffix = f" · ~{_format_duration((total_rows - done) / rate)} remaining"

        fraction = done / max(total_rows, 1)
        job.current_step = (
            f"Pre-analyzing comments locally ({done:,}/{total_rows:,} · {rate:.0f}/sec{eta_suffix})"
        )
        job.progress_percentage = progress_start + int(fraction * (progress_end - progress_start))
        db.commit()

    completed = await _run_sentiment_waves(
        db,
        job,
        cancel_event,
        rows,
        bundle_cache,
        AnalysisMode.FAST,
        wave_size=BATCH_SIZE * settings.fast_mode_concurrent_batches,
        sub_batch_size=BATCH_SIZE,
        on_wave=_collect,
    )
    return fast_results if completed else None


async def _run_analysis_job_body(db: Session, job: AnalysisJob, cancel_event: asyncio.Event) -> None:
    job.status = AnalysisJobStatus.PROCESSING
    job.current_step = "Fetching video details and comments"
    job.progress_percentage = 5
    db.commit()

    options = job.options_json
    requested = options.get("max_comments", 100)

    video_info_task = asyncio.create_task(fetch_video_info(job.video_id))
    comments_task = asyncio.create_task(
        fetch_comments(
            video_id=job.video_id,
            max_results=requested,
            order=options.get("order", "relevance"),
            include_replies=False,
            page_token=None,
            cancel_event=cancel_event,
        )
    )

    try:
        video_info = await video_info_task
        job.video_title = video_info["title"]
        job.video_thumbnail_url = video_info["thumbnail_url"]
    except YouTubeApiError:
        pass

    job.current_step = "Fetching comments"
    job.progress_percentage = 10
    db.commit()

    try:
        comments_result = await comments_task
    except YouTubeApiError as e:
        job.status = AnalysisJobStatus.FAILED
        job.error_message = e.message
        db.commit()
        return

    if cancel_event.is_set():
        _cancel_job(db, job)
        return

    fetched = comments_result["total_fetched"]
    job.total_fetched_comments = fetched
    if fetched < requested and not comments_result["has_more"]:
        logger.info(
            "Job %s: requested %d comments, YouTube returned %d (no more pages available)",
            job.id,
            requested,
            fetched,
        )

    comment_rows: list[CommentAnalysis] = []
    for c in comments_result["comments"]:
        row = CommentAnalysis(
            job_id=job.id,
            youtube_comment_id=c["comment_id"],
            author_display_name=c["author_display_name"],
            text=c["text_display"],
            like_count=c["like_count"],
            published_at=c["published_at"],
            is_reply=c["is_reply"],
        )
        db.add(row)
        comment_rows.append(row)

    job.current_step = "Detecting spam, sarcasm, and language"
    job.progress_percentage = 20
    db.commit()
    for row in comment_rows:
        db.refresh(row)

    is_spam_flags: dict[int, bool] = {}
    is_engagement_flags: dict[int, bool] = {}
    signal_bundle_cache: dict[int, SignalBundle] = {}
    signature_cache: dict[int, str] = {}
    for row in comment_rows:
        cleaned = clean_text(row.text)
        row.language = detect_language(cleaned)

        is_spam, spam_reason = detect_spam(row.text)
        is_spam_flags[row.id] = is_spam
        db.add(
            CommentAnalysisResult(
                job_id=job.id,
                comment_id=row.id,
                capability=Capability.SPAM.value,
                provider_id="rule-based",
                mode=AnalysisMode.FAST.value,
                label="spam" if is_spam else "clean",
                confidence=None,
                result_json={"reason": spam_reason} if spam_reason else {},
            )
        )

        bundle = extract_signals(cleaned, row.language)
        signal_bundle_cache[row.id] = bundle
        db.add(
            CommentAnalysisResult(
                job_id=job.id,
                comment_id=row.id,
                capability=Capability.SARCASM.value,
                provider_id="rule-based",
                mode=AnalysisMode.FAST.value,
                label="sarcastic" if bundle.is_sarcasm else "not_sarcastic",
                confidence=None,
                result_json={},
            )
        )

        is_engagement_flags[row.id] = is_engagement_comment(cleaned)
        signature_cache[row.id] = canonical_signature(row.text)

    db.commit()

    mode_str = options.get("mode", "fast")
    mode = {"smart": AnalysisMode.SMART, "hybrid": AnalysisMode.HYBRID}.get(mode_str, AnalysisMode.FAST)
    confidence_threshold = options.get("confidence_threshold", 0.55)

    job.current_step = "Running sentiment analysis"
    job.progress_percentage = 30
    db.commit()

    analyzable_rows = [row for row in comment_rows if not is_spam_flags[row.id]]
    spam_rows = [row for row in comment_rows if is_spam_flags[row.id]]

    job.total_cleaned_comments = len(analyzable_rows)

    for row in spam_rows:
        db.add(
            CommentAnalysisResult(
                job_id=job.id,
                comment_id=row.id,
                capability=Capability.SENTIMENT.value,
                provider_id="rule-based",
                mode=mode.value,
                label="neutral",
                confidence=1.0,
                result_json={},
            )
        )

    total = len(analyzable_rows)
    processed = 0

    signature_groups = _group_rows_by_signature(analyzable_rows, signature_cache)

    duplicate_count = total - len(signature_groups)
    if duplicate_count:
        logger.info(
            "Job %s: %d/%d comments are exact or near-duplicates of another comment "
            "(%d unique clusters to analyze)",
            job.id,
            duplicate_count,
            total,
            len(signature_groups),
        )

    unique_rows = sorted((rows[0] for rows in signature_groups.values()), key=lambda row: len(row.text))

    smart_sampling_active = mode == AnalysisMode.SMART and len(unique_rows) > settings.smart_mode_sample_size
    smart_aggregate_stats: dict | None = None
    ai_insights_saved = False

    if smart_sampling_active:
        job.current_step = f"Pre-analyzing {len(unique_rows):,} unique comments locally"
        db.commit()

        fast_results = await _run_fast_prepass(
            db,
            job,
            cancel_event,
            unique_rows,
            signal_bundle_cache,
            _PREPASS_PROGRESS_START,
            _PREPASS_PROGRESS_END,
        )
        if fast_results is None:
            return

        smart_aggregate_stats = _compute_aggregate_stats(unique_rows, fast_results)

        sample_size = settings.smart_mode_sample_size
        sampled_ids = _select_llm_sample(unique_rows, fast_results, signal_bundle_cache, sample_size)
        sampled_rows = [row for row in unique_rows if row.id in sampled_ids]
        unsampled_rows = [row for row in unique_rows if row.id not in sampled_ids]

        logger.info(
            "Job %s: SMART sampling — %d/%d unique comments (%.1f%%) sent to the LLM in one batch, "
            "the rest resolved from the local FAST-mode pass",
            job.id,
            len(sampled_rows),
            len(unique_rows),
            100 * len(sampled_rows) / max(len(unique_rows), 1),
        )

        for row in unsampled_rows:
            processed += _write_comment_result(
                db,
                job,
                signature_groups,
                signature_cache,
                signal_bundle_cache,
                is_engagement_flags,
                confidence_threshold,
                row,
                fast_results[row.id],
                {"llm_tier": "fast_only"},
            )
        job.current_step = f"Refining {len(sampled_rows):,} comments with the LLM"
        job.progress_percentage = _PREPASS_PROGRESS_END
        db.commit()

        unique_rows = sampled_rows

    hybrid_capped_active = mode == AnalysisMode.HYBRID

    if hybrid_capped_active:
        job.current_step = f"Pre-analyzing {len(unique_rows):,} unique comments locally"
        db.commit()

        fast_results = await _run_fast_prepass(
            db,
            job,
            cancel_event,
            unique_rows,
            signal_bundle_cache,
            _PREPASS_PROGRESS_START,
            _PREPASS_PROGRESS_END,
        )
        if fast_results is None:
            return

        hybrid_aggregate_stats = _compute_aggregate_stats(unique_rows, fast_results)

        escalation_candidates = []
        trivial_escalated = []
        for row in unique_rows:
            result = fast_results[row.id]
            if should_escalate(result, signal_bundle_cache[row.id]):
                if is_trivial_comment(signal_bundle_cache[row.id].cleaned_text):
                    trivial_escalated.append(row)
                else:
                    escalation_candidates.append(row)

        sample_size = settings.hybrid_llm_sample_size
        sampled_ids = _select_llm_sample(
            escalation_candidates, fast_results, signal_bundle_cache, sample_size
        )
        sampled_rows = [row for row in escalation_candidates if row.id in sampled_ids]
        capped_out_rows = [row for row in escalation_candidates if row.id not in sampled_ids]

        logger.info(
            "Job %s: HYBRID capped escalation — %d/%d unique comments flagged, %d sent to the LLM "
            "in one batch, %d resolved locally, %d beyond the cap kept their FAST result",
            job.id,
            len(escalation_candidates) + len(trivial_escalated),
            len(unique_rows),
            len(sampled_rows),
            len(trivial_escalated),
            len(capped_out_rows),
        )

        job.current_step = f"Refining {len(sampled_rows):,} borderline comments with the LLM"
        job.progress_percentage = _PREPASS_PROGRESS_END
        db.commit()

        for row in trivial_escalated:
            fast_result = fast_results[row.id]
            merged = resolve_final(
                fast_result,
                local_heuristic_result(
                    signal_bundle_cache[row.id].cleaned_text, fast_result, Capability.SENTIMENT
                ),
                settings.hybrid_decision_policy,
            )
            processed += _write_comment_result(
                db,
                job,
                signature_groups,
                signature_cache,
                signal_bundle_cache,
                is_engagement_flags,
                confidence_threshold,
                row,
                merged,
                {"llm_tier": "local_heuristic"},
            )

        flagged_ids = {row.id for row in escalation_candidates} | {row.id for row in trivial_escalated}
        non_escalated_rows = [row for row in unique_rows if row.id not in flagged_ids]
        for row in non_escalated_rows + capped_out_rows:
            processed += _write_comment_result(
                db,
                job,
                signature_groups,
                signature_cache,
                signal_bundle_cache,
                is_engagement_flags,
                confidence_threshold,
                row,
                fast_results[row.id],
                {"llm_tier": "fast_only"},
            )
        db.commit()

        def _merge_llm_results(wave_batches: list[list[CommentAnalysis]], wave_results: list[list]) -> None:
            nonlocal processed, ai_insights_saved

            if not ai_insights_saved:
                insights = _extract_batch_ai_insights(wave_results)
                if insights:
                    provider_id = next(
                        (r.provider_id for batch in wave_results for r in batch if r.provider_id), "unknown"
                    )
                    _save_dynamic_ai_insights(db, job, insights, provider_id, AnalysisMode.HYBRID)
                    ai_insights_saved = True

            for batch, results in zip(wave_batches, wave_results, strict=True):
                for row, llm_result in zip(batch, results, strict=True):
                    merged = resolve_final(fast_results[row.id], llm_result, settings.hybrid_decision_policy)
                    processed += _write_comment_result(
                        db,
                        job,
                        signature_groups,
                        signature_cache,
                        signal_bundle_cache,
                        is_engagement_flags,
                        confidence_threshold,
                        row,
                        merged,
                        {"llm_tier": "llm_sampled"},
                    )
            job.current_step = "Finalizing results"
            job.progress_percentage = _REFINE_PROGRESS_END
            db.commit()

        sample_cap = max(len(sampled_rows), 1)
        completed = await _run_sentiment_waves(
            db,
            job,
            cancel_event,
            sampled_rows,
            signal_bundle_cache,
            AnalysisMode.SMART,
            wave_size=sample_cap,
            sub_batch_size=sample_cap,
            on_wave=_merge_llm_results,
            aggregate_stats=hybrid_aggregate_stats,
        )
        if not completed:
            return

        unique_rows = []

    if mode == AnalysisMode.FAST:
        wave_size = BATCH_SIZE * settings.fast_mode_concurrent_batches
        sub_batch_size = BATCH_SIZE
    else:
        wave_size = settings.llm_batch_classification_size * settings.llm_max_concurrent_batches
        sub_batch_size = wave_size

    phase_start = time.monotonic()

    def _write_sentiment_results(wave_batches: list[list[CommentAnalysis]], wave_results: list[list]) -> None:
        nonlocal processed, ai_insights_saved

        if not ai_insights_saved:
            insights = _extract_batch_ai_insights(wave_results)
            if insights:
                provider_id = next(
                    (r.provider_id for batch in wave_results for r in batch if r.provider_id), "unknown"
                )
                _save_dynamic_ai_insights(db, job, insights, provider_id, mode)
                ai_insights_saved = True

        for batch, results in zip(wave_batches, wave_results, strict=True):
            for representative_row, result in zip(batch, results, strict=True):
                tag = {"llm_tier": "llm_sampled"} if smart_sampling_active else {}
                processed += _write_comment_result(
                    db,
                    job,
                    signature_groups,
                    signature_cache,
                    signal_bundle_cache,
                    is_engagement_flags,
                    confidence_threshold,
                    representative_row,
                    result,
                    tag,
                )

        elapsed = time.monotonic() - phase_start
        rate = processed / elapsed if elapsed > 0 else 0.0
        eta_suffix = ""
        if rate > 0 and processed < total:
            eta_suffix = f" · ~{_format_duration((total - processed) / rate)} remaining"

        job.current_step = (
            f"Running sentiment analysis ({processed:,}/{total:,} comments · {rate:.0f}/sec{eta_suffix})"
        )
        job.progress_percentage = 30 + int((processed / max(total, 1)) * 65)
        db.commit()

    completed = await _run_sentiment_waves(
        db,
        job,
        cancel_event,
        unique_rows,
        signal_bundle_cache,
        mode,
        wave_size=wave_size,
        sub_batch_size=sub_batch_size,
        on_wave=_write_sentiment_results,
        aggregate_stats=smart_aggregate_stats,
    )
    if not completed:
        return

    job.status = AnalysisJobStatus.COMPLETED
    job.current_step = None
    job.progress_percentage = 100
    db.commit()

    try:
        await index_job_comments(job.id, db)
    except Exception:
        logger.exception("Embedding indexing failed for job %s (analysis job itself succeeded)", job.id)
