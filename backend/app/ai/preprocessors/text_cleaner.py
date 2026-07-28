import re

_HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
_URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
_TIMESTAMP_PATTERN = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")
_MENTION_PATTERN = re.compile(r"@(\w+)")
_HASHTAG_PATTERN = re.compile(r"#(\w+)")
_ARABIC_DIACRITICS_PATTERN = re.compile("[ؗ-ًؚ-ْٰۖ-ۭ]")
_TATWEEL_PATTERN = re.compile("ـ+")
_ALEF_VARIANTS_PATTERN = re.compile("[آأإٱ]")
_ALEF_MAKSURA_PATTERN = re.compile("ى")
_ELONGATION_PATTERN = re.compile(r"(.)\1{3,}")
_WHITESPACE_PATTERN = re.compile(r"\s+")


def normalize_arabic_letters(text: str) -> str:
    text = _ARABIC_DIACRITICS_PATTERN.sub("", text)
    text = _TATWEEL_PATTERN.sub("", text)
    text = _ALEF_VARIANTS_PATTERN.sub("ا", text)
    text = _ALEF_MAKSURA_PATTERN.sub("ي", text)
    return text


def clean_text(text: str) -> str:
    text = _HTML_TAG_PATTERN.sub(" ", text)
    text = _URL_PATTERN.sub(" http ", text)
    text = _TIMESTAMP_PATTERN.sub(" ", text)
    text = _MENTION_PATTERN.sub(r"\1", text)
    text = _HASHTAG_PATTERN.sub(r"\1", text)
    text = normalize_arabic_letters(text)
    text = _ELONGATION_PATTERN.sub(r"\1\1\1", text)
    text = _WHITESPACE_PATTERN.sub(" ", text)
    return text.strip()


_BR_TAG_PATTERN = re.compile(r"<br\s*/?>", re.IGNORECASE)


def strip_html_for_display(text: str) -> str:
    text = _BR_TAG_PATTERN.sub("\n", text)
    text = _HTML_TAG_PATTERN.sub("", text)
    return text
