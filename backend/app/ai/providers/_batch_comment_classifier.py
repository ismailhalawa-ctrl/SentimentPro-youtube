import json
import logging
from collections.abc import Awaitable, Callable

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.result import AnalysisResult

logger = logging.getLogger(__name__)


def _degraded_result(capability: Capability, provider_id: str, mode: AnalysisMode) -> AnalysisResult:
    return AnalysisResult(
        capability=capability,
        provider_id=provider_id,
        mode=mode,
        label=None,
        confidence=None,
        data={"batch_degraded": True},
    )


async def run_batch_classification_chunk(
    chunk: list[str],
    capability: Capability,
    provider_id: str,
    mode: AnalysisMode,
    build_prompt: Callable[..., list[dict]],
    call_llm: Callable[[list[dict]], Awaitable[str]],
    **kwargs,
) -> list[AnalysisResult]:
    messages = build_prompt(chunk, **kwargs)

    try:
        raw_content = await call_llm(messages)
    except Exception:
        logger.exception(
            "Batch %s call failed for %s after retries — degrading %d comments",
            capability.value,
            provider_id,
            len(chunk),
        )
        return [_degraded_result(capability, provider_id, mode) for _ in chunk]

    try:
        parsed = json.loads(raw_content)
    except json.JSONDecodeError:
        logger.warning(
            "Batch %s response for %s was not valid JSON — degrading %d comments",
            capability.value,
            provider_id,
            len(chunk),
        )
        return [_degraded_result(capability, provider_id, mode) for _ in chunk]

    ai_insights: list[str] | None = None
    if isinstance(parsed, list):
        items = parsed
    elif isinstance(parsed, dict) and isinstance(parsed.get("comments"), list):
        items = parsed["comments"]
        raw_insights = parsed.get("ai_insights")
        if isinstance(raw_insights, list):
            cleaned = [s.strip() for s in raw_insights if isinstance(s, str) and s.strip()]
            ai_insights = cleaned[:6] if cleaned else None
    else:
        logger.warning(
            "Batch %s response for %s was not a recognized JSON shape — degrading %d comments",
            capability.value,
            provider_id,
            len(chunk),
        )
        return [_degraded_result(capability, provider_id, mode) for _ in chunk]

    by_index: dict[int, dict] = {}
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("index"), int):
            by_index[item["index"]] = item

    results: list[AnalysisResult] = []
    missing = 0
    for i in range(len(chunk)):
        item = by_index.get(i)
        if item is None:
            missing += 1
            results.append(_degraded_result(capability, provider_id, mode))
            continue
        confidence = item.get("confidence")
        results.append(
            AnalysisResult(
                capability=capability,
                provider_id=provider_id,
                mode=mode,
                label=item.get("label"),
                confidence=confidence if isinstance(confidence, int | float) else None,
                data=item,
                raw_output={"content": raw_content},
            )
        )

    if missing:
        logger.warning(
            "Batch %s response for %s was missing %d/%d comments — those degraded to neutral",
            capability.value,
            provider_id,
            missing,
            len(chunk),
        )

    if ai_insights and results:
        results[0].data = {**results[0].data, "_batch_ai_insights": ai_insights}

    return results
