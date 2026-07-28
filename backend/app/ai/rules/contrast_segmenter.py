from dataclasses import dataclass

from app.ai.rules.arabic_lexicon import analyze_arabic_text
from app.ai.rules.arabizi_lexicon import analyze_arabizi_text
from app.ai.rules.english_lexicon import analyze_english_text
from app.ai.rules.negation import CONTRAST_CONNECTIVES_AR, CONTRAST_CONNECTIVES_EN
from app.ai.rules.target_scope import detect_target_scope

_STRENGTH_RANK = {"weak": 0, "moderate": 1, "strong": 2}


@dataclass(frozen=True)
class OpinionSpan:
    text: str
    polarity: str | None
    strength: str
    category: str | None
    mixed: bool
    target: str


def _connectives_for(language: str) -> list[str]:
    return CONTRAST_CONNECTIVES_EN if language == "en" else CONTRAST_CONNECTIVES_AR


def segment_by_contrast(text: str, language: str) -> list[str]:
    connectives = sorted(_connectives_for(language), key=len, reverse=True)
    lowered = text.lower()
    for connective in connectives:
        idx = lowered.find(connective.lower())
        if idx == -1:
            continue
        pre = text[:idx].strip()
        post = text[idx + len(connective) :].strip()
        if pre and post:
            return [pre, post]
    return [text]


def _lexicon_result(span_text: str, language: str) -> dict:
    if language == "en":
        en = analyze_english_text(span_text)
        az = analyze_arabizi_text(span_text)
        if az["polarity"] is None:
            return en
        if en["polarity"] is None:
            return az
        return en if _STRENGTH_RANK[en["strength"]] >= _STRENGTH_RANK[az["strength"]] else az
    if language == "mixed":
        candidates = [
            analyze_arabic_text(span_text),
            analyze_english_text(span_text),
            analyze_arabizi_text(span_text),
        ]
        matched = [r for r in candidates if r["polarity"] is not None]
        if not matched:
            return candidates[1]
        return max(matched, key=lambda r: _STRENGTH_RANK[r["strength"]])
    return analyze_arabic_text(span_text)


def _build_span(span_text: str, language: str) -> OpinionSpan:
    result = _lexicon_result(span_text, language)
    target, _confidence = detect_target_scope(span_text, language)
    return OpinionSpan(
        text=span_text,
        polarity=result["polarity"],
        strength=result["strength"],
        category=result["category"],
        mixed=result["mixed"],
        target=target,
    )


def analyze_opinion_spans(text: str, language: str) -> list[OpinionSpan]:
    segments = segment_by_contrast(text, language)
    if len(segments) == 1:
        return [_build_span(text, language)]

    post_span = _build_span(segments[1], language)
    if post_span.polarity is None:
        return [_build_span(text, language)]

    pre_span = _build_span(segments[0], language)
    return [pre_span, post_span]
