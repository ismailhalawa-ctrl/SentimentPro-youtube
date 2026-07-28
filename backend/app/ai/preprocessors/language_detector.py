import re

_ARABIC_CHAR_RE = re.compile(r"[؀-ۿ]")
_LATIN_CHAR_RE = re.compile(r"[a-zA-Z]")
_URL_RE = re.compile(r"http\S+")
_MENTION_RE = re.compile(r"[@#]\S+")

_ARABIZI_TOKEN_RE = re.compile(r"\b[a-zA-Z]*[2356789][a-zA-Z]+\b|\b[a-zA-Z]+[2356789][a-zA-Z]*\b")


def detect_arabizi(text: str) -> bool:
    return len(_ARABIZI_TOKEN_RE.findall(text)) >= 2


def detect_language(text: str) -> str:
    text = _URL_RE.sub("", text)
    text = _MENTION_RE.sub("", text)

    arabic = len(_ARABIC_CHAR_RE.findall(text))
    latin = len(_LATIN_CHAR_RE.findall(text))
    total = arabic + latin

    if total == 0:
        return "other"

    ratio = arabic / total
    if ratio >= 0.7:
        return "ar"
    if ratio <= 0.25:
        return "mixed" if detect_arabizi(text) else "en"
    return "mixed"
