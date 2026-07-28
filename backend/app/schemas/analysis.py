from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CreateAnalysisJobRequest(BaseModel):
    url: str
    max_comments: int = Field(default=100, ge=1, le=1_000_000)
    language: str = "auto"
    confidence_threshold: float = Field(default=0.55, ge=0.30, le=0.90)
    mode: Literal["fast", "smart", "hybrid"] = "fast"
    order: Literal["relevance", "time"] = "relevance"
    keyword_extraction: bool = True
    generate_report: bool = False


class SentimentSummary(BaseModel):
    positive_count: int = 0
    neutral_count: int = 0
    negative_count: int = 0
    average_confidence: float | None = None
    spam_count: int = 0
    sarcasm_count: int = 0
    arabic_count: int = 0
    english_count: int = 0
    mixed_count: int = 0
    other_count: int = 0


class AnalysisJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    progress_percentage: int
    current_step: str | None
    error_message: str | None
    video_url: str
    video_id: str
    video_title: str | None = None
    video_thumbnail_url: str | None = None
    created_at: datetime
    sentiment_summary: SentimentSummary | None = None
    total_fetched_comments: int | None = None
    total_cleaned_comments: int | None = None


class AnalysisJobListResponse(BaseModel):
    jobs: list[AnalysisJobResponse]


class KeywordEntry(BaseModel):
    word: str
    count: int


class KeywordsResponse(BaseModel):
    positive: list[KeywordEntry]
    negative: list[KeywordEntry]
    neutral: list[KeywordEntry]


class TopicsResponse(BaseModel):
    positive: dict[str, int]
    negative: dict[str, int]


class InsightsResponse(BaseModel):
    insights: list[str]
    source: Literal["ai", "rule_based"] = "rule_based"


class CommentEntry(BaseModel):
    id: int
    author: str
    text: str
    likes: int
    published_at: str | None
    sentiment: str | None
    confidence: float | None
    language: str | None
    is_spam: bool
    spam_reason: str | None
    is_sarcasm: bool


class CommentsListResponse(BaseModel):
    comments: list[CommentEntry]
