import re

from app.ai.rules.emoji_sets import SARCASM_EMOJIS, SARCASM_PHRASES

_POSITIVE_WORDS = {
    "amazing",
    "great",
    "perfect",
    "رائع",
    "ممتاز",
    "مبدع",
    "جامد",
    "حلو",
    "منيح",
    "زين",
    "تحفة",
}
_NEGATIVE_WORDS = {
    "سيء",
    "فاشل",
    "زبالة",
    "bad",
    "terrible",
    "awful",
    "وحش",
    "زفت",
    "خايس",
    "تعبان",
}
_REPEATED_HA_AR_RE = re.compile(r"ه{3,}")
_REPEATED_HA_EN_RE = re.compile(r"(ha){3,}")
_ELLIPSIS_NOT_RE = re.compile(r"(\.\.\.|…)\s*not\b")

SARCASM_DETECTION_THRESHOLD = 3


def sarcasm_score(text: str) -> int:
    text = str(text)
    t = text.lower()
    score = 0

    for emoji in SARCASM_EMOJIS:
        if emoji in text:
            score += 2

    for phrase in SARCASM_PHRASES:
        if phrase.lower() in t:
            score += 2

    if "!!!" in text:
        score += 1

    if "???" in text:
        score += 1

    has_positive = any(w in t for w in _POSITIVE_WORDS)
    has_negative = any(w in t for w in _NEGATIVE_WORDS)
    if has_positive and has_negative:
        score += 2

    if _REPEATED_HA_AR_RE.search(t):
        score += 2

    if _REPEATED_HA_EN_RE.search(t):
        score += 2

    if _ELLIPSIS_NOT_RE.search(t):
        score += 2

    return score


def detect_sarcasm(text: str) -> bool:
    return sarcasm_score(text) >= SARCASM_DETECTION_THRESHOLD
