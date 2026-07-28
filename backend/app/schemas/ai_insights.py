from typing import Any, Literal

from pydantic import BaseModel


class AIFeatureResponse(BaseModel):
    status: Literal["ok", "unavailable", "error", "partial", "rate_limited"]
    data: dict[str, Any] | None = None
    reason: str | None = None


class ViewerSegment(BaseModel):
    name: str
    description: str
    estimated_share: str


class ExecutiveSummaryPayload(BaseModel):
    overview: str
    key_positives: list[str] = []
    key_negatives: list[str] = []
    notable_trends: list[str] = []
    overall_sentiment_label: str = "mixed"


class AudienceAnalysisPayload(BaseModel):
    personality_profile: str
    viewer_segments: list[ViewerSegment] = []
    behavior_notes: list[str] = []
    emotional_trend: str


class FAQEntry(BaseModel):
    question: str
    answer: str
    times_asked_estimate: int = 0


class FAQPayload(BaseModel):
    faqs: list[FAQEntry] = []


class TopicCluster(BaseModel):
    name: str
    description: str
    estimated_share: str
    dominant_sentiment: str = "mixed"


class TopicClusteringPayload(BaseModel):
    topics: list[TopicCluster] = []


class RankedCategory(BaseModel):
    category: str
    count: int
    total_likes: int
    example_comment_ids: list[int] = []


class ExtractedCommentItem(BaseModel):
    comment_id: int
    text: str
    category: str | None = None
    confidence: float | None = None
    is_feature_request: bool | None = None


class CommentExtractionPayload(BaseModel):
    ranked_categories: list[RankedCategory] = []
    items: list[ExtractedCommentItem] = []


class AudienceIntelligenceScores(BaseModel):
    satisfaction_score: float
    community_health_score: float
    loyalty_score: float


class AudienceIntelligenceNarrativePayload(BaseModel):
    emerging_trends: list[str] = []
    growth_opportunities: list[str] = []


class AudienceIntelligenceScorePayload(BaseModel):
    scores: AudienceIntelligenceScores
    emerging_trends: list[str] = []
    growth_opportunities: list[str] = []
