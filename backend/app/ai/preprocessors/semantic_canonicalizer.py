import re

from app.ai.preprocessors.text_cleaner import clean_text

_STOPWORDS_AR = {
    "في",
    "من",
    "على",
    "الى",
    "إلى",
    "عن",
    "مع",
    "هذا",
    "هذه",
    "ذلك",
    "انا",
    "أنا",
    "انت",
    "أنت",
    "هو",
    "هي",
    "و",
    "او",
    "أو",
    "ثم",
    "كان",
    "يكون",
    "ال",
}
_STOPWORDS_EN = {
    "the",
    "a",
    "an",
    "is",
    "are",
    "was",
    "were",
    "this",
    "that",
    "and",
    "or",
    "of",
    "to",
    "in",
    "on",
    "for",
    "it",
    "i",
    "you",
}

_PUNCTUATION_PATTERN = re.compile(r"[^\w\s]", re.UNICODE)
_EMOJI_PATTERN = re.compile(
    "[\U0001f300-\U0001faff\U00002600-\U000027bf\U0001f1e6-\U0001f1ff]+", flags=re.UNICODE
)


def canonical_signature(text: str) -> str:
    cleaned = _EMOJI_PATTERN.sub(" ", clean_text(text).lower())
    cleaned = _PUNCTUATION_PATTERN.sub(" ", cleaned)
    tokens = [t for t in cleaned.split() if t and t not in _STOPWORDS_AR and t not in _STOPWORDS_EN]
    return " ".join(sorted(tokens))
