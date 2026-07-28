from dataclasses import dataclass

from app.ai.rules.contrast_segmenter import OpinionSpan, analyze_opinion_spans
from app.ai.rules.emoji_boost import count_emoji_signal
from app.ai.rules.emotion_signals import detect_formulaic_emotion, detect_greeting
from app.ai.rules.intent_detector import detect_intent
from app.ai.rules.sarcasm_detector import SARCASM_DETECTION_THRESHOLD, sarcasm_score
from app.ai.rules.target_scope import TARGET_PERSONAL_LIFE, TARGET_VIDEO

_DOWNGRADE = {"strong": "moderate", "moderate": "weak", "weak": "weak"}


@dataclass(frozen=True)
class SignalBundle:
    cleaned_text: str
    language: str
    intent: str
    spans: list[OpinionSpan]
    contrast_detected: bool
    emotion_only: bool
    emotion_category: str | None
    is_greeting: bool
    opinion_polarity: str | None
    opinion_strength: str
    mixed_opinion: bool
    is_sarcasm: bool
    sarcasm_score: int
    emoji_pos: int
    emoji_neg: int


def _fuse_opinion(spans: list[OpinionSpan]) -> tuple[str | None, str, bool]:
    candidates = [s for s in spans if s.target != TARGET_PERSONAL_LIFE and s.polarity is not None]
    if not candidates:
        return None, "weak", False

    dominant = candidates[-1]
    others = candidates[:-1]
    mixed = any(other.polarity != dominant.polarity for other in others)

    strength = _DOWNGRADE[dominant.strength] if mixed else dominant.strength
    return dominant.polarity, strength, mixed


def extract_signals(cleaned_text: str, language: str) -> SignalBundle:
    spans = analyze_opinion_spans(cleaned_text, language)
    contrast_detected = len(spans) == 2

    opinion_polarity, opinion_strength, mixed_opinion = _fuse_opinion(spans)

    has_emotion, emotion_category = detect_formulaic_emotion(cleaned_text, language)
    video_targeted_opinion = any(span.target == TARGET_VIDEO and span.polarity is not None for span in spans)
    emotion_only = has_emotion and not video_targeted_opinion

    emoji_pos, emoji_neg = count_emoji_signal(cleaned_text, opinion_polarity)
    score = sarcasm_score(cleaned_text)

    return SignalBundle(
        cleaned_text=cleaned_text,
        language=language,
        intent=detect_intent(cleaned_text, language),
        spans=spans,
        contrast_detected=contrast_detected,
        emotion_only=emotion_only,
        emotion_category=emotion_category,
        is_greeting=detect_greeting(cleaned_text),
        opinion_polarity=opinion_polarity,
        opinion_strength=opinion_strength,
        mixed_opinion=mixed_opinion,
        is_sarcasm=score >= SARCASM_DETECTION_THRESHOLD,
        sarcasm_score=score,
        emoji_pos=emoji_pos,
        emoji_neg=emoji_neg,
    )
