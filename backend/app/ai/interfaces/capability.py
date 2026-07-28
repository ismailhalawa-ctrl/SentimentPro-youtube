from enum import Enum


class Capability(str, Enum):
    SENTIMENT = "sentiment"
    SPAM = "spam"
    SARCASM = "sarcasm"

    EXECUTIVE_SUMMARY = "executive_summary"
    AUDIENCE_ANALYSIS = "audience_analysis"

    COMPLAINT_EXTRACTION = "complaint_extraction"
    SUGGESTION_EXTRACTION = "suggestion_extraction"

    FAQ_GENERATION = "faq_generation"
    TOPIC_CLUSTERING = "topic_clustering"

    AUDIENCE_INTELLIGENCE_SCORE = "audience_intelligence_score"

    AUDIENCE_ASSISTANT = "audience_assistant"

    DYNAMIC_AI_INSIGHTS = "dynamic_ai_insights"


class AnalysisMode(str, Enum):
    FAST = "fast"
    SMART = "smart"
    HYBRID = "hybrid"


class ResultScope(str, Enum):
    PER_COMMENT = "per_comment"
    JOB_LEVEL = "job_level"
    CONVERSATIONAL = "conversational"


CAPABILITY_SCOPE: dict[Capability, ResultScope] = {
    Capability.SENTIMENT: ResultScope.PER_COMMENT,
    Capability.SPAM: ResultScope.PER_COMMENT,
    Capability.SARCASM: ResultScope.PER_COMMENT,
    Capability.EXECUTIVE_SUMMARY: ResultScope.JOB_LEVEL,
    Capability.AUDIENCE_ANALYSIS: ResultScope.JOB_LEVEL,
    Capability.COMPLAINT_EXTRACTION: ResultScope.PER_COMMENT,
    Capability.SUGGESTION_EXTRACTION: ResultScope.PER_COMMENT,
    Capability.FAQ_GENERATION: ResultScope.JOB_LEVEL,
    Capability.TOPIC_CLUSTERING: ResultScope.JOB_LEVEL,
    Capability.AUDIENCE_INTELLIGENCE_SCORE: ResultScope.JOB_LEVEL,
    Capability.AUDIENCE_ASSISTANT: ResultScope.CONVERSATIONAL,
    Capability.DYNAMIC_AI_INSIGHTS: ResultScope.JOB_LEVEL,
}
