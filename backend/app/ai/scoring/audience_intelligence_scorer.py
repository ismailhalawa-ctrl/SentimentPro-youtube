import math

from sqlalchemy.orm import Session, aliased

from app.ai.interfaces.capability import Capability
from app.models.comment_analysis import CommentAnalysis
from app.models.comment_analysis_result import CommentAnalysisResult
from app.schemas.ai_insights import AudienceIntelligenceScores
from app.services.analysis_service import get_sentiment_summary

_LOYALTY_PHRASES = [
    "been here since",
    "day one",
    "day 1",
    "long time fan",
    "longtime fan",
    "since 20",
    "years now",
    "original fan",
    "watched since",
    "subscribed since",
    "من زمان",
    "من سنين",
    "متابعك من",
    "من البداية",
]

_ENGAGEMENT_REFERENCE_AVG_LIKES = 50


def _matches_loyalty_phrase(text: str) -> bool:
    lowered = text.lower()
    return any(phrase in lowered for phrase in _LOYALTY_PHRASES)


def compute_scores(db: Session, job_id: int) -> AudienceIntelligenceScores | None:
    summary = get_sentiment_summary(db, job_id)
    non_spam_total = (
        summary.positive_count + summary.neutral_count + summary.negative_count - summary.spam_count
    )
    if non_spam_total <= 0:
        return None

    total_comments = non_spam_total + summary.spam_count
    spam_ratio_pct = (summary.spam_count / total_comments) * 100
    sarcasm_ratio_pct = (summary.sarcasm_count / total_comments) * 100

    return AudienceIntelligenceScores(
        satisfaction_score=round(_satisfaction_score(summary, non_spam_total, spam_ratio_pct), 1),
        community_health_score=round(
            _community_health_score(spam_ratio_pct, sarcasm_ratio_pct, summary.average_confidence), 1
        ),
        loyalty_score=round(_loyalty_score(db, job_id), 1),
    )


def _satisfaction_score(summary, non_spam_total: int, spam_ratio_pct: float) -> float:
    net_sentiment = (summary.positive_count - summary.negative_count) / non_spam_total
    score = 50 + 50 * net_sentiment
    score -= min(10.0, spam_ratio_pct * 0.5)
    return max(0.0, min(100.0, score))


def _community_health_score(
    spam_ratio_pct: float, sarcasm_ratio_pct: float, avg_confidence: float | None
) -> float:
    score = 100.0
    score -= min(40.0, spam_ratio_pct * 2)
    score -= min(20.0, max(0.0, sarcasm_ratio_pct - 15) * 1.5)
    if avg_confidence is not None:
        score += min(10.0, avg_confidence * 10)
    return max(0.0, min(100.0, score))


def _loyalty_score(db: Session, job_id: int) -> float:
    spam_result = aliased(CommentAnalysisResult)
    rows = (
        db.query(CommentAnalysis.text, CommentAnalysis.like_count)
        .outerjoin(
            spam_result,
            (spam_result.comment_id == CommentAnalysis.id)
            & (spam_result.capability == Capability.SPAM.value),
        )
        .filter(
            CommentAnalysis.job_id == job_id,
            (spam_result.label != "spam") | (spam_result.label.is_(None)),
        )
        .all()
    )
    if not rows:
        return 0.0

    avg_length = sum(len(text) for text, _likes in rows) / len(rows)
    length_score = min(100.0, (avg_length / 150) * 100)

    phrase_matches = sum(1 for text, _likes in rows if _matches_loyalty_phrase(text))
    phrase_ratio = phrase_matches / len(rows)
    phrase_score = min(100.0, phrase_ratio * 100 * 20)

    avg_likes = sum(likes for _text, likes in rows) / len(rows)
    engagement_score = min(100.0, (math.log1p(avg_likes) / math.log1p(_ENGAGEMENT_REFERENCE_AVG_LIKES)) * 100)

    return 0.4 * phrase_score + 0.35 * length_score + 0.25 * engagement_score
