from sqlalchemy.orm import Session, aliased

from app.ai.interfaces.capability import Capability
from app.ai.preprocessors.text_cleaner import clean_text, strip_html_for_display
from app.ai.rules.keywords import get_top_words, get_topics
from app.models.comment_analysis import CommentAnalysis
from app.models.comment_analysis_result import CommentAnalysisResult
from app.schemas.analysis import (
    CommentEntry,
    CommentsListResponse,
    InsightsResponse,
    KeywordEntry,
    KeywordsResponse,
    SentimentSummary,
    TopicsResponse,
)


def _job_comments_with_sentiment(db: Session, job_id: int):
    sentiment_result = aliased(CommentAnalysisResult)
    spam_result = aliased(CommentAnalysisResult)

    return (
        db.query(
            CommentAnalysis.text,
            CommentAnalysis.like_count,
            sentiment_result.label,
            spam_result.label,
        )
        .outerjoin(
            sentiment_result,
            (sentiment_result.comment_id == CommentAnalysis.id)
            & (sentiment_result.capability == Capability.SENTIMENT.value),
        )
        .outerjoin(
            spam_result,
            (spam_result.comment_id == CommentAnalysis.id)
            & (spam_result.capability == Capability.SPAM.value),
        )
        .filter(CommentAnalysis.job_id == job_id)
        .all()
    )


def get_job_comment_rows(db: Session, job_id: int):
    sentiment_result = aliased(CommentAnalysisResult)
    spam_result = aliased(CommentAnalysisResult)
    sarcasm_result = aliased(CommentAnalysisResult)

    return (
        db.query(CommentAnalysis, sentiment_result, spam_result, sarcasm_result)
        .outerjoin(
            sentiment_result,
            (sentiment_result.comment_id == CommentAnalysis.id)
            & (sentiment_result.capability == Capability.SENTIMENT.value),
        )
        .outerjoin(
            spam_result,
            (spam_result.comment_id == CommentAnalysis.id)
            & (spam_result.capability == Capability.SPAM.value),
        )
        .outerjoin(
            sarcasm_result,
            (sarcasm_result.comment_id == CommentAnalysis.id)
            & (sarcasm_result.capability == Capability.SARCASM.value),
        )
        .filter(CommentAnalysis.job_id == job_id)
        .order_by(CommentAnalysis.id)
        .all()
    )


def get_job_comments(db: Session, job_id: int) -> CommentsListResponse:
    rows = get_job_comment_rows(db, job_id)

    comments = [
        CommentEntry(
            id=comment.id,
            author=comment.author_display_name,
            text=strip_html_for_display(comment.text),
            likes=comment.like_count,
            published_at=comment.published_at,
            sentiment=sentiment.label if sentiment else None,
            confidence=sentiment.confidence if sentiment else None,
            language=comment.language,
            is_spam=bool(spam and spam.label == "spam"),
            spam_reason=(spam.result_json or {}).get("reason") if spam else None,
            is_sarcasm=bool(sarcasm and sarcasm.label == "sarcastic"),
        )
        for comment, sentiment, spam, sarcasm in rows
    ]
    return CommentsListResponse(comments=comments)


def get_job_keywords(db: Session, job_id: int, top_n: int = 20) -> KeywordsResponse:
    rows = _job_comments_with_sentiment(db, job_id)

    buckets: dict[str, list[str]] = {"positive": [], "negative": [], "neutral": []}
    for text, _likes, sentiment_label, spam_label in rows:
        if spam_label == "spam" or sentiment_label not in buckets:
            continue
        buckets[sentiment_label].append(clean_text(text))

    return KeywordsResponse(
        positive=[KeywordEntry(word=w, count=c) for w, c in get_top_words(buckets["positive"], top_n)],
        negative=[KeywordEntry(word=w, count=c) for w, c in get_top_words(buckets["negative"], top_n)],
        neutral=[KeywordEntry(word=w, count=c) for w, c in get_top_words(buckets["neutral"], top_n)],
    )


def get_job_topics(db: Session, job_id: int) -> TopicsResponse:
    rows = _job_comments_with_sentiment(db, job_id)

    positive_texts, negative_texts = [], []
    for text, _likes, sentiment_label, spam_label in rows:
        if spam_label == "spam":
            continue
        if sentiment_label == "positive":
            positive_texts.append(clean_text(text))
        elif sentiment_label == "negative":
            negative_texts.append(clean_text(text))

    return TopicsResponse(
        positive=get_topics(positive_texts),
        negative=get_topics(negative_texts),
    )


def get_job_insights(db: Session, job_id: int, summary: SentimentSummary) -> InsightsResponse:
    rows = _job_comments_with_sentiment(db, job_id)
    total = summary.positive_count + summary.negative_count + summary.neutral_count
    if total == 0:
        return InsightsResponse(insights=[])

    all_likes = [likes for _t, likes, _s, spam in rows if spam != "spam"]
    positive_likes = [likes for _t, likes, s, spam in rows if s == "positive" and spam != "spam"]
    negative_likes = [likes for _t, likes, s, spam in rows if s == "negative" and spam != "spam"]

    avg_likes = sum(all_likes) / len(all_likes) if all_likes else 0.0
    avg_positive_likes = sum(positive_likes) / len(positive_likes) if positive_likes else 0.0
    avg_negative_likes = sum(negative_likes) / len(negative_likes) if negative_likes else 0.0
    total_engagement = sum(all_likes)

    pos_pct = round(summary.positive_count / total * 100, 1)
    neg_pct = round(summary.negative_count / total * 100, 1)
    spam_ratio = (summary.spam_count / total) * 100
    sarcasm_ratio = (summary.sarcasm_count / total) * 100
    avg_confidence = summary.average_confidence or 0.0

    insights: list[str] = []

    if pos_pct > 75:
        insights.append("🔥 The audience reaction was extremely positive overall.")
    elif pos_pct > 60:
        insights.append("✅ Most viewers reacted positively to the video.")
    elif neg_pct > 50:
        insights.append("⚠️ The video received a significant amount of negative feedback.")
    else:
        insights.append("📊 Audience reactions were relatively balanced.")

    if avg_likes > 50:
        insights.append("🚀 Comments showed very high engagement levels.")
    elif avg_likes > 10:
        insights.append("👍 Viewer engagement was moderate.")
    else:
        insights.append("👀 Most comments received low engagement.")

    if spam_ratio > 15:
        insights.append("🚨 A high percentage of comments were classified as spam.")
    elif spam_ratio > 5:
        insights.append("⚠️ Some suspicious or promotional comments were detected.")

    if sarcasm_ratio > 10:
        insights.append("😏 Sarcastic reactions appeared frequently in the comments.")
    elif sarcasm_ratio > 3:
        insights.append("🙃 A small portion of comments contained sarcasm.")

    if summary.arabic_count > summary.english_count:
        insights.append("🌍 Arabic-speaking viewers dominated the conversation.")
    elif summary.english_count > summary.arabic_count:
        insights.append("🌎 English comments represented the majority of interactions.")

    if avg_positive_likes > avg_negative_likes * 1.5 and avg_negative_likes > 0:
        insights.append("💚 Positive comments attracted significantly more engagement.")
    elif avg_negative_likes > avg_positive_likes * 1.5 and avg_positive_likes > 0:
        insights.append("💥 Negative comments generated stronger audience interaction.")

    if avg_confidence > 0.85:
        insights.append("🎯 The AI model showed very high confidence in sentiment predictions.")
    elif avg_confidence < 0.60:
        insights.append("🤔 Some comments were difficult for the AI to classify accurately.")

    if total_engagement > 5000:
        insights.append("📈 The video generated exceptionally high audience interaction.")
    elif total_engagement > 1000:
        insights.append("📊 The content achieved strong engagement performance.")

    if neg_pct > 35 and sarcasm_ratio > 8:
        insights.append("☠️ The discussion showed signs of heated or toxic interactions.")

    if pos_pct > 70 and spam_ratio < 5:
        insights.append("✨ The community response appeared healthy and genuinely positive.")

    return InsightsResponse(insights=insights)
