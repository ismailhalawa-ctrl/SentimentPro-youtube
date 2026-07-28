from app.ai.rules.negation import is_negated

INTENSIFIER_MARKERS_EN = [
    "very",
    "extremely",
    "so much",
    "absolutely",
    "incredibly",
    "really",
    "truly",
    "genuinely",
]

PRAISE_PHRASES_EN = [
    "amazing",
    "awesome",
    "great video",
    "well done",
    "fantastic",
    "love this",
    "so good",
    "perfect",
    "excellent",
    "brilliant",
    "nailed it",
    "underrated channel",
    "best explanation",
    "keep it up",
    "keep up the good work",
    "you're the best",
    "so helpful",
    "well explained",
    "great content",
    "top notch",
    "loved this",
    "really enjoyed this",
    "so well made",
    "i like",
    "enjoy",
    "tactical breakdown",
    "this was great",
]

ADMIRATION_PHRASES_EN = [
    "true legend",
    "absolute genius",
    "best creator",
    "such an inspiration",
    "hands down the best",
    "nobody does it like you",
    "goat",
    "king of this niche",
    "greatest of all time",
    "true inspiration",
    "set the bar so high",
    "set the bar high",
]

RELIGIOUS_POSITIVE_PHRASES_EN = [
    "god bless you",
    "may god reward you",
    "praying for your success",
    "blessed content",
    "may allah bless you",
]

LONGING_AFFECTION_PHRASES_EN = [
    "missed your videos",
    "we missed you",
    "glad you're back",
    "welcome back",
]

EARLY_ENGAGEMENT_PHRASES_EN = [
    "first comment",
    "early gang",
    "here before it blew up",
    "watching this in",
]

REQUEST_ANTICIPATION_PHRASES_EN = [
    "please make",
    "could you make",
    "can you cover",
    "make a part two",
    "do a follow up",
    "please explain",
    "would be great if",
    "hoping for more",
    "hoping you",
    "waiting for part two",
]

CRITICISM_PHRASES_EN = [
    "terrible",
    "awful",
    "bad video",
    "waste of time",
    "waste of my time",
    "poorly made",
    "poorly edited",
    "not good",
    "boring",
    "disappointing",
    "low quality",
    "cheap content",
    "misleading",
    "clickbait",
    "factually incorrect",
    "completely wrong",
    "just a copy",
    "unsubscribing",
    "adds nothing new",
    "all over the place",
    "poorly organized",
]

COMPLAINT_PHRASES_EN = [
    "too many ads",
    "audio issues",
    "audio kept cutting out",
    "bad audio quality",
    "video lags",
    "poor editing",
    "rushed editing",
    "hard to follow",
    "no captions",
]

DISAPPOINTMENT_PHRASES_EN = [
    "expected more",
    "expected better",
    "expected so much more",
    "not what I expected",
    "let down",
    "kind of disappointed",
    "not your best work",
]

CONSTRUCTIVE_CRITICISM_PHRASES_EN = [
    "needs work",
    "needs improvement",
    "needs polish",
    "could be better",
    "too long",
    "way too long",
    "too repetitive",
    "way too repetitive",
    "distracting",
    "missed the point",
    "missed the key details",
    "pacing is off",
    "pacing was off",
    "felt rushed",
    "feels rushed",
]

_CATEGORY_PHRASES = {
    "praise": (PRAISE_PHRASES_EN, "positive", "strong"),
    "admiration": (ADMIRATION_PHRASES_EN, "positive", "strong"),
    "religious": (RELIGIOUS_POSITIVE_PHRASES_EN, "positive", "moderate"),
    "longing_affection": (LONGING_AFFECTION_PHRASES_EN, "positive", "strong"),
    "early_engagement": (EARLY_ENGAGEMENT_PHRASES_EN, "positive", "moderate"),
    "request_anticipation": (REQUEST_ANTICIPATION_PHRASES_EN, "positive", "weak"),
    "criticism": (CRITICISM_PHRASES_EN, "negative", "strong"),
    "complaint": (COMPLAINT_PHRASES_EN, "negative", "moderate"),
    "disappointment": (DISAPPOINTMENT_PHRASES_EN, "negative", "strong"),
    "constructive_criticism": (CONSTRUCTIVE_CRITICISM_PHRASES_EN, "negative", "moderate"),
}

_STRENGTH_RANK = {"weak": 0, "moderate": 1, "strong": 2}
_OPPOSITE = {"positive": "negative", "negative": "positive"}
_DOWNGRADE = {"strong": "moderate", "moderate": "weak", "weak": "weak"}


def _has_intensifier(text: str) -> bool:
    return any(marker in text for marker in INTENSIFIER_MARKERS_EN)


def analyze_english_text(text: str) -> dict:
    t = text.lower()
    matches: list[tuple[str, str, str]] = []

    for category, (phrases, polarity, strength) in _CATEGORY_PHRASES.items():
        for phrase in phrases:
            idx = t.find(phrase.lower())
            if idx == -1:
                continue

            effective_polarity = polarity
            effective_strength = strength

            if is_negated(t, idx, "en"):
                effective_polarity = _OPPOSITE[polarity]
                effective_strength = "moderate"
            elif _has_intensifier(t) and effective_strength == "weak":
                effective_strength = "moderate"

            matches.append((category, effective_polarity, effective_strength))
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
