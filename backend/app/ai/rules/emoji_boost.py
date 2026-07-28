from app.ai.rules.emoji_sets import (
    AMBIVALENT_EMOJIS,
    ENGAGEMENT_PATTERNS,
    UNAMBIGUOUS_NEGATIVE_EMOJIS,
    UNAMBIGUOUS_POSITIVE_EMOJIS,
)

_BOOST_STRONG = 0.03
_BOOST_WEAK = 0.015

_AMBIVALENT_NO_CONTEXT_WEIGHT = 0.5


def count_emoji_signal(text: str, rule_polarity: str | None) -> tuple[int, int]:
    pos_count = sum(text.count(e) for e in UNAMBIGUOUS_POSITIVE_EMOJIS)
    neg_count = sum(text.count(e) for e in UNAMBIGUOUS_NEGATIVE_EMOJIS)
    ambivalent_count = sum(text.count(e) for e in AMBIVALENT_EMOJIS)

    if ambivalent_count == 0:
        return pos_count, neg_count

    if rule_polarity == "positive":
        pos_count += ambivalent_count
    elif rule_polarity == "negative":
        neg_count += ambivalent_count
    else:
        neg_count += round(ambivalent_count * _AMBIVALENT_NO_CONTEXT_WEIGHT)

    return pos_count, neg_count


def emoji_boost(
    text: str, sentiment: str, score: float, is_engagement: bool = False, rule_polarity: str | None = None
) -> tuple[str, float]:
    if is_engagement:
        return sentiment, score

    pos_count, neg_count = count_emoji_signal(text, rule_polarity)

    if pos_count == 0 and neg_count == 0:
        return sentiment, score

    if sentiment == "positive":
        if pos_count >= 3:
            score = min(score + _BOOST_STRONG, 0.95)
        elif pos_count > 0:
            score = min(score + _BOOST_WEAK, 0.90)

    elif sentiment == "negative":
        if neg_count >= 3:
            score = min(score + _BOOST_STRONG, 0.95)
        elif neg_count > 0:
            score = min(score + _BOOST_WEAK, 0.90)

    return sentiment, round(min(score, 1.0), 3)


def is_engagement_comment(text: str) -> bool:
    text = text.lower().strip()
    return any(p in text for p in ENGAGEMENT_PATTERNS)
