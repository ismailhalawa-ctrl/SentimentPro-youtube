from app.ai.interfaces.capability import AnalysisMode
from app.ai.interfaces.result import AnalysisResult

_VALID_POLICIES = ("highest_confidence", "llm_priority", "weighted_ensemble")


def resolve_final(
    fast_result: AnalysisResult,
    smart_result: AnalysisResult | None,
    policy: str,
) -> AnalysisResult:
    if smart_result is None:
        return fast_result

    if policy not in _VALID_POLICIES:
        policy = "highest_confidence"

    if policy == "llm_priority":
        label = smart_result.label or fast_result.label
        confidence = (
            smart_result.confidence if smart_result.confidence is not None else fast_result.confidence
        )
    elif policy == "weighted_ensemble":
        if fast_result.label == smart_result.label:
            label = smart_result.label
            fast_conf = fast_result.confidence or 0.0
            smart_conf = smart_result.confidence or 0.0
            confidence = round(fast_conf * 0.35 + smart_conf * 0.65, 3)
        else:
            fast_conf = fast_result.confidence or 0.0
            smart_conf = smart_result.confidence or 0.0
            if smart_conf * 0.65 >= fast_conf * 0.35:
                label, confidence = smart_result.label, smart_conf
            else:
                label, confidence = fast_result.label, fast_conf
    else:
        fast_conf = fast_result.confidence or 0.0
        smart_conf = smart_result.confidence or 0.0
        if smart_conf >= fast_conf:
            label, confidence = smart_result.label, smart_result.confidence
        else:
            label, confidence = fast_result.label, fast_result.confidence

    return AnalysisResult(
        capability=fast_result.capability,
        provider_id=f"{fast_result.provider_id}+{smart_result.provider_id}",
        mode=AnalysisMode.HYBRID,
        label=label,
        confidence=confidence,
        processing_time_ms=(fast_result.processing_time_ms or 0) + (smart_result.processing_time_ms or 0),
        data={
            "fast": {
                "provider_id": fast_result.provider_id,
                "label": fast_result.label,
                "confidence": fast_result.confidence,
                "data": fast_result.data,
            },
            "smart": {
                "provider_id": smart_result.provider_id,
                "label": smart_result.label,
                "confidence": smart_result.confidence,
                "data": smart_result.data,
            },
            "decision_policy": policy,
        },
        raw_output={"fast": fast_result.raw_output, "smart": smart_result.raw_output},
    )
