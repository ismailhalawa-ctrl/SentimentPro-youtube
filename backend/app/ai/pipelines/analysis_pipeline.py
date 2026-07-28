import logging
import unicodedata
from typing import cast

from app.ai.interfaces.capability import AnalysisMode, Capability
from app.ai.interfaces.errors import ProviderCallError, ProviderNotConfiguredError
from app.ai.interfaces.result import AnalysisResult
from app.ai.pipelines.decision_policy import resolve_final
from app.ai.postprocessors.result_normalizer import normalize_result
from app.ai.preprocessors.language_detector import detect_language
from app.ai.preprocessors.text_cleaner import clean_text
from app.ai.providers.provider_registry import resolve_provider
from app.ai.rules.emoji_sets import NEGATIVE_EMOJIS, POSITIVE_EMOJIS
from app.ai.rules.signal_bundle import SignalBundle, extract_signals
from app.ai.rules.target_scope import TARGET_AMBIGUOUS
from app.core.config import settings

logger = logging.getLogger(__name__)

_FALLBACK_LANGUAGE = {"other": "en"}


async def run_analysis(
    text: str,
    capability: Capability,
    mode: AnalysisMode,
) -> AnalysisResult:
    cleaned = clean_text(text)
    language = detect_language(cleaned)

    if mode == AnalysisMode.HYBRID:
        return await _run_hybrid(cleaned, capability, language)

    if language == "mixed" and capability != Capability.SENTIMENT:
        return (await _resolve_mixed_batch([cleaned], capability, mode))[0]

    provider = resolve_provider(capability, mode, _FALLBACK_LANGUAGE.get(language, language))
    result = await provider.run(cleaned, capability=capability, language=language)
    return normalize_result(result)


async def run_analysis_batch(
    texts: list[str],
    capability: Capability,
    mode: AnalysisMode,
    aggregate_stats: dict | None = None,
) -> list[AnalysisResult]:
    if mode == AnalysisMode.HYBRID:
        return await _run_hybrid_batch(texts, capability)

    cleaned_texts = [clean_text(t) for t in texts]

    groups: dict[str, list[int]] = {}
    for i, t in enumerate(cleaned_texts):
        language = detect_language(t)
        groups.setdefault(language, []).append(i)

    results: list[AnalysisResult | None] = [None] * len(texts)

    mixed_indices = groups.pop("mixed", []) if capability != Capability.SENTIMENT else []
    if mixed_indices:
        mixed_texts = [cleaned_texts[i] for i in mixed_indices]
        mixed_results = await _resolve_mixed_batch(mixed_texts, capability, mode)
        for idx, result in zip(mixed_indices, mixed_results, strict=True):
            results[idx] = result

    for language, indices in groups.items():
        provider = resolve_provider(capability, mode, _FALLBACK_LANGUAGE.get(language, language))
        group_texts = [cleaned_texts[i] for i in indices]
        group_results = await provider.run_batch(
            group_texts, capability=capability, language=language, aggregate_stats=aggregate_stats
        )
        for idx, result in zip(indices, group_results, strict=True):
            results[idx] = normalize_result(result)

    if any(result is None for result in results):
        raise RuntimeError("run_analysis_batch left some comments unprocessed.")
    return cast(list[AnalysisResult], results)


async def _resolve_mixed_batch(
    texts: list[str], capability: Capability, mode: AnalysisMode
) -> list[AnalysisResult]:
    ar_provider = resolve_provider(capability, mode, "ar")
    en_provider = resolve_provider(capability, mode, "en")

    ar_results = await ar_provider.run_batch(texts, capability=capability, language="ar")
    en_results = await en_provider.run_batch(texts, capability=capability, language="en")

    resolved: list[AnalysisResult] = []
    for ar_result, en_result in zip(ar_results, en_results, strict=True):
        if ar_result.label == en_result.label:
            confidence = None
            if ar_result.confidence is not None and en_result.confidence is not None:
                confidence = round((ar_result.confidence + en_result.confidence) / 2, 3)
            winner = ar_result
        elif (ar_result.confidence or 0) >= (en_result.confidence or 0):
            winner, confidence = ar_result, ar_result.confidence
        else:
            winner, confidence = en_result, en_result.confidence

        resolved.append(
            normalize_result(
                AnalysisResult(
                    capability=capability,
                    provider_id=f"{ar_result.provider_id}+{en_result.provider_id}",
                    mode=winner.mode,
                    label=winner.label,
                    confidence=confidence,
                    processing_time_ms=winner.processing_time_ms,
                    data={
                        "ar": {"label": ar_result.label, "confidence": ar_result.confidence},
                        "en": {"label": en_result.label, "confidence": en_result.confidence},
                    },
                    raw_output=winner.raw_output,
                )
            )
        )
    return resolved


_LONG_COMMENT_WORD_THRESHOLD = 60

_HEAVY_EMOJI_MINIMUM = 5


_LOW_MARGIN_ESCALATION_THRESHOLD = 0.20


def _model_margin(fast_result: AnalysisResult) -> float | None:
    all_probs = (fast_result.data or {}).get("all_probs")
    if not all_probs or len(all_probs) < 2:
        return None
    ranked = sorted(all_probs.values(), reverse=True)
    return ranked[0] - ranked[1]


def should_escalate(fast_result: AnalysisResult, bundle: SignalBundle | None = None) -> bool:
    if (
        fast_result.confidence is not None
        and fast_result.confidence < settings.hybrid_escalation_confidence_threshold
    ):
        return True

    margin = _model_margin(fast_result)
    if margin is not None and margin < _LOW_MARGIN_ESCALATION_THRESHOLD:
        return True

    if bundle is None:
        return False

    if bundle.opinion_polarity is not None and bundle.opinion_polarity != fast_result.label:
        return True

    if settings.hybrid_escalate_on_mixed_language and bundle.language == "mixed":
        return True

    if settings.hybrid_escalate_on_sarcasm and bundle.is_sarcasm:
        return True

    if settings.hybrid_escalate_on_heavy_emoji:
        if bundle.emoji_pos >= _HEAVY_EMOJI_MINIMUM or bundle.emoji_neg >= _HEAVY_EMOJI_MINIMUM:
            return True
        if bundle.emoji_pos > 0 and bundle.emoji_neg > 0:
            return True

    if len(bundle.cleaned_text.split()) > _LONG_COMMENT_WORD_THRESHOLD:
        return True

    if bundle.contrast_detected:
        return True

    if any(span.target == TARGET_AMBIGUOUS and span.polarity is not None for span in bundle.spans):
        return True

    if bundle.emotion_only and fast_result.label != "neutral":
        return True

    return bool(bundle.mixed_opinion)


_TRIVIAL_MAX_WORDS = 3

_EMOJI_UNICODE_CATEGORY = "So"
_ZERO_WIDTH_JOINER = chr(0x200D)
_VARIATION_SELECTOR_16 = chr(0xFE0F)
_EMOJI_JOINER_CHARS = {_ZERO_WIDTH_JOINER, _VARIATION_SELECTOR_16}


def _is_emoji_only(text: str) -> bool:
    saw_emoji = False
    for ch in text:
        if ch.isspace():
            continue
        if ch in _EMOJI_JOINER_CHARS:
            continue
        if unicodedata.category(ch) == _EMOJI_UNICODE_CATEGORY:
            saw_emoji = True
            continue
        return False
    return saw_emoji


def is_trivial_comment(text: str) -> bool:
    return len(text.split()) < _TRIVIAL_MAX_WORDS or _is_emoji_only(text)


def local_heuristic_result(text: str, fast_result: AnalysisResult, capability: Capability) -> AnalysisResult:
    if capability != Capability.SENTIMENT:
        return fast_result

    pos_count = sum(text.count(e) for e in POSITIVE_EMOJIS)
    neg_count = sum(text.count(e) for e in NEGATIVE_EMOJIS)
    if pos_count == 0 and neg_count == 0:
        return fast_result
    if pos_count > 0 and neg_count > 0:
        return fast_result

    return AnalysisResult(
        capability=capability,
        provider_id="heuristic-short-circuit",
        mode=AnalysisMode.FAST,
        label="positive" if pos_count > neg_count else "negative",
        confidence=0.75,
        processing_time_ms=0.0,
        data={"short_circuit": True, "reason": "trivial_comment_emoji_signal"},
    )


async def _run_hybrid(text: str, capability: Capability, language: str) -> AnalysisResult:
    if language == "mixed":
        fast_result = (await _resolve_mixed_batch([text], capability, AnalysisMode.FAST))[0]
    else:
        effective_language = _FALLBACK_LANGUAGE.get(language, language)
        fast_provider = resolve_provider(capability, AnalysisMode.FAST, effective_language)
        fast_result = normalize_result(
            await fast_provider.run(text, capability=capability, language=language)
        )

    bundle = extract_signals(text, language) if capability == Capability.SENTIMENT else None
    if not should_escalate(fast_result, bundle):
        return fast_result

    if is_trivial_comment(text):
        return normalize_result(
            resolve_final(
                fast_result,
                local_heuristic_result(text, fast_result, capability),
                settings.hybrid_decision_policy,
            )
        )

    try:
        effective_language = _FALLBACK_LANGUAGE.get(language, language)
        smart_provider = resolve_provider(capability, AnalysisMode.SMART, effective_language)
        smart_result = normalize_result(
            await smart_provider.run(text, capability=capability, language=language)
        )
    except (LookupError, ProviderNotConfiguredError, ProviderCallError) as exc:
        logger.warning(
            "HYBRID escalation skipped for capability=%s language=%s: %s",
            capability.value,
            language,
            exc,
        )
        return fast_result

    return normalize_result(resolve_final(fast_result, smart_result, settings.hybrid_decision_policy))


async def _run_hybrid_batch(texts: list[str], capability: Capability) -> list[AnalysisResult]:
    cleaned_texts = [clean_text(t) for t in texts]
    languages = [detect_language(t) for t in cleaned_texts]

    fast_results = await run_analysis_batch(texts, capability, AnalysisMode.FAST)

    bundles: list[SignalBundle | None] = (
        [extract_signals(text, language) for text, language in zip(cleaned_texts, languages, strict=True)]
        if capability == Capability.SENTIMENT
        else [None] * len(cleaned_texts)
    )

    escalate_indices = [
        i
        for i, (fast_result, bundle) in enumerate(zip(fast_results, bundles, strict=True))
        if should_escalate(fast_result, bundle)
    ]

    if not escalate_indices:
        return fast_results

    final_results = list(fast_results)

    still_escalating: list[int] = []
    for i in escalate_indices:
        if is_trivial_comment(cleaned_texts[i]):
            heuristic_result = local_heuristic_result(cleaned_texts[i], fast_results[i], capability)
            final_results[i] = normalize_result(
                resolve_final(fast_results[i], heuristic_result, settings.hybrid_decision_policy)
            )
        else:
            still_escalating.append(i)

    if not still_escalating:
        return final_results

    escalated_texts = [cleaned_texts[i] for i in still_escalating]

    try:
        smart_provider = resolve_provider(capability, AnalysisMode.SMART, "auto")
        smart_results = await smart_provider.run_batch(
            escalated_texts, capability=capability, language="auto"
        )
        smart_results = [normalize_result(r) for r in smart_results]
    except (LookupError, ProviderNotConfiguredError, ProviderCallError) as exc:
        logger.warning(
            "HYBRID batch escalation skipped for capability=%s (%d comments would have escalated): %s",
            capability.value,
            len(still_escalating),
            exc,
        )
        return final_results

    for idx, smart_result in zip(still_escalating, smart_results, strict=True):
        final_results[idx] = normalize_result(
            resolve_final(fast_results[idx], smart_result, settings.hybrid_decision_policy)
        )
    return final_results
