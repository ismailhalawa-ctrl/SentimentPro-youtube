from app.ai.postprocessors.probability_calibration import apply_temperature
from app.ai.rules.emoji_boost import emoji_boost
from app.ai.rules.signal_bundle import SignalBundle
from app.ai.rules.target_scope import TARGET_PERSONAL_LIFE, TARGET_VIDEO

_CALIBRATION_TEMPERATURE = 1.0
_STRENGTH_CONFIDENCE = {"strong": 0.80, "moderate": 0.68, "weak": 0.58}
_STRONG_OVERRIDE_CONFIDENCE = 0.80
_MODERATE_OVERRIDE_CONFIDENCE = 0.68
_MODERATE_OVERRIDE_CEILING = 0.80
_EMOTION_ONLY_CONFIDENCE = 0.75
_PERSONAL_LIFE_CONFIDENCE = 0.70
_SARCASM_FLIP_CONFIDENCE = 0.65
_SARCASM_STRONG_SCORE = 4
_MODEL_HIGH_CONFIDENCE = 0.85
_MODEL_HIGH_MARGIN = 0.5
_MIXED_OPINION_CONFIDENCE = 0.65
_CONTRAST_CONFIDENCE_PENALTY = 0.05
_SOFT_CRITICISM_CATEGORIES = {"constructive_criticism"}
_AGREEMENT_BONUS = 0.10
_CONFIDENCE_FLOOR = 0.5
_CONFIDENCE_CEILING = 0.97
_INTENT_PROTECTED_FROM_NEGATIVE = {"request", "question", "disagreement"}
_INTENT_PROTECTED_CONFIDENCE = 0.55
_REQUEST_ANTICIPATION_CATEGORY = "request_anticipation"
_REQUEST_ANTICIPATION_CONFIDENCE = 0.6
_EMOJI_ONLY_STRONG_COUNT = 3
_EMOJI_ONLY_CONFIDENCE = 0.75


def _compute_margin(all_probs: dict[str, float] | None) -> float | None:
    if not all_probs or len(all_probs) < 2:
        return None
    ranked = sorted(all_probs.values(), reverse=True)
    return round(ranked[0] - ranked[1], 3)


def _is_model_highly_confident(score: float, margin: float | None) -> bool:
    if score < _MODEL_HIGH_CONFIDENCE:
        return False
    return margin is None or margin >= _MODEL_HIGH_MARGIN


def resolve_sentiment_decision(
    model_label: str,
    model_confidence: float,
    all_probs: dict[str, float] | None,
    bundle: SignalBundle,
    *,
    is_spam: bool,
    is_engagement: bool,
    confidence_threshold: float,
) -> tuple[str, float, dict]:
    calibrated_probs = apply_temperature(all_probs, _CALIBRATION_TEMPERATURE) if all_probs else None
    margin = _compute_margin(calibrated_probs)
    meta_base = {
        "margin": margin,
        "rule_category": bundle.spans[-1].category if bundle.spans else None,
        "rule_polarity": bundle.opinion_polarity,
        "intent": bundle.intent,
        "contrast_detected": bundle.contrast_detected,
        "mixed_opinion": bundle.mixed_opinion,
        "sarcasm_score": bundle.sarcasm_score,
    }

    if is_spam:
        return "neutral", 1.0, {**meta_base, "correction": "spam"}

    if calibrated_probs:
        top_label = max(calibrated_probs, key=lambda label: calibrated_probs[label])
        sentiment = top_label
        score = calibrated_probs[top_label]
    else:
        sentiment = model_label or "neutral"
        score = model_confidence if model_confidence is not None else 0.5

    if is_engagement:
        return "neutral", round(max(score, 0.80), 3), {**meta_base, "correction": "engagement"}

    if bundle.is_greeting:
        return "neutral", round(max(score, 0.80), 3), {**meta_base, "correction": "greeting"}

    correction: str | None = None

    has_personal_life_span = any(span.target == TARGET_PERSONAL_LIFE for span in bundle.spans)
    has_video_targeted_opinion = any(
        span.target == TARGET_VIDEO and span.polarity is not None for span in bundle.spans
    )

    if has_personal_life_span and not has_video_targeted_opinion:
        sentiment, score = "neutral", _PERSONAL_LIFE_CONFIDENCE
        correction = "personal_life_scoped_neutral"

    elif bundle.emotion_only:
        sentiment, score = "neutral", _EMOTION_ONLY_CONFIDENCE
        correction = "emotion_only"

    elif bundle.is_sarcasm and sentiment != "negative":
        model_is_highly_confident = _is_model_highly_confident(score, margin)
        sarcasm_evidence_is_strong = bundle.sarcasm_score >= _SARCASM_STRONG_SCORE

        if sarcasm_evidence_is_strong or not model_is_highly_confident:
            sentiment, score = "negative", _SARCASM_FLIP_CONFIDENCE
            correction = "sarcasm_flip"
        else:
            correction = "sarcasm_signal_outweighed_by_model_confidence"

    elif bundle.mixed_opinion or bundle.spans[-1].category in _SOFT_CRITICISM_CATEGORIES:
        sentiment, score = "neutral", _MIXED_OPINION_CONFIDENCE
        correction = "mixed_opinion_neutral"

    elif (
        bundle.opinion_polarity == "positive"
        and bundle.spans
        and bundle.spans[-1].category == _REQUEST_ANTICIPATION_CATEGORY
    ):
        sentiment, score = "neutral", _REQUEST_ANTICIPATION_CONFIDENCE
        correction = "request_anticipation_neutral"

    elif bundle.opinion_polarity is None and bundle.emoji_neg >= _EMOJI_ONLY_STRONG_COUNT and bundle.emoji_pos == 0:
        sentiment, score = "negative", _EMOJI_ONLY_CONFIDENCE
        correction = "emoji_only_negative"

    elif bundle.opinion_polarity is None and bundle.emoji_pos >= _EMOJI_ONLY_STRONG_COUNT and bundle.emoji_neg == 0:
        sentiment, score = "positive", _EMOJI_ONLY_CONFIDENCE
        correction = "emoji_only_positive"

    elif bundle.opinion_polarity is not None:
        agree = sentiment == bundle.opinion_polarity
        strength = bundle.opinion_strength

        if agree:
            score = min(_CONFIDENCE_CEILING, max(score, _STRENGTH_CONFIDENCE[strength]) + _AGREEMENT_BONUS)
            correction = "signals_agree"
        elif sentiment == "neutral" and strength in ("strong", "moderate"):
            sentiment = bundle.opinion_polarity
            score = _STRONG_OVERRIDE_CONFIDENCE if strength == "strong" else _MODERATE_OVERRIDE_CONFIDENCE
            correction = "neutral_promoted"
        elif strength == "strong":
            if _is_model_highly_confident(score, margin):
                correction = "rule_signal_outweighed_by_model_confidence"
            else:
                sentiment, score = bundle.opinion_polarity, _STRONG_OVERRIDE_CONFIDENCE
                correction = "rule_override_strong"
        elif strength == "moderate" and score < _MODERATE_OVERRIDE_CEILING:
            sentiment, score = bundle.opinion_polarity, _MODERATE_OVERRIDE_CONFIDENCE
            correction = "rule_override_moderate"

        if bundle.contrast_detected:
            score = max(score - _CONTRAST_CONFIDENCE_PENALTY, _CONFIDENCE_FLOOR)

    sentiment, score = emoji_boost(
        bundle.cleaned_text, sentiment, score, is_engagement=False, rule_polarity=bundle.opinion_polarity
    )

    strong_negative_rule_signal = bundle.opinion_polarity == "negative" and bundle.opinion_strength in (
        "strong",
        "moderate",
    )
    if (
        sentiment == "negative"
        and bundle.intent in _INTENT_PROTECTED_FROM_NEGATIVE
        and not strong_negative_rule_signal
        and correction != "sarcasm_flip"
    ):
        sentiment, score = "neutral", max(score, _INTENT_PROTECTED_CONFIDENCE)
        correction = "intent_protected_neutral"

    if score < confidence_threshold and correction is None:
        sentiment = "neutral"

    return sentiment, round(score, 3), {**meta_base, "correction": correction}
