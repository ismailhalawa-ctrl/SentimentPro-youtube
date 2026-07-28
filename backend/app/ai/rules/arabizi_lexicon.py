PRAISE_PHRASES_ARABIZI = [
    "tislam eedak",
    "tislam eedik",
    "3ajabny",
    "3ajabni",
    "3ajbatni",
    "m3jab",
    "mu3jab",
    "wa7ashtna",
    "wa7ashtouna",
]

MILD_PRAISE_PHRASES_ARABIZI = [
    "hala fik",
    "7ilw",
]

CRITICISM_PHRASES_ARABIZI = [
    "mesh clear",
    "mesh 3ajb",
    "kalam fadi",
    "mafi fayde",
]

_CATEGORY_PHRASES = {
    "praise": (PRAISE_PHRASES_ARABIZI, "positive", "strong"),
    "mild_praise": (MILD_PRAISE_PHRASES_ARABIZI, "positive", "moderate"),
    "criticism": (CRITICISM_PHRASES_ARABIZI, "negative", "strong"),
}

_STRENGTH_RANK = {"weak": 0, "moderate": 1, "strong": 2}
_DOWNGRADE = {"strong": "moderate", "moderate": "weak", "weak": "weak"}


def analyze_arabizi_text(text: str) -> dict:
    t = text.lower()
    matches: list[tuple[str, str, str]] = []

    for category, (phrases, polarity, strength) in _CATEGORY_PHRASES.items():
        for phrase in phrases:
            if phrase in t:
                matches.append((category, polarity, strength))
                break

    if not matches:
        return {"polarity": None, "strength": "weak", "category": None, "mixed": False}

    has_positive = any(polarity == "positive" for _, polarity, _ in matches)
    has_negative = any(polarity == "negative" for _, polarity, _ in matches)
    mixed = has_positive and has_negative

    category, polarity, strength = max(matches, key=lambda m: _STRENGTH_RANK[m[2]])
    if mixed:
        strength = _DOWNGRADE[strength]

    return {"polarity": polarity, "strength": strength, "category": category, "mixed": mixed}
