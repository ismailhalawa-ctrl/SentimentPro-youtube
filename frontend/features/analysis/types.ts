export type AnalysisJobStatus = 'pending' | 'processing' | 'completed' | 'failed' | 'cancelled';

export interface SentimentSummary {
  positive_count: number;
  neutral_count: number;
  negative_count: number;
  average_confidence: number | null;
  spam_count: number;
  sarcasm_count: number;
  arabic_count: number;
  english_count: number;
  mixed_count: number;
  other_count: number;
}

export interface AnalysisJob {
  id: number;
  status: AnalysisJobStatus;
  progress_percentage: number;
  current_step: string | null;
  error_message: string | null;
  video_url: string;
  video_id: string;
  video_title: string | null;
  video_thumbnail_url: string | null;
  created_at: string;
  sentiment_summary: SentimentSummary | null;
  total_fetched_comments: number | null;
  total_cleaned_comments: number | null;
}

export interface CreateAnalysisJobPayload {
  url: string;
  max_comments?: number;
  language?: 'auto' | 'ar' | 'en';
  confidence_threshold?: number;
  mode?: 'fast' | 'hybrid' | 'smart';
  order?: 'relevance' | 'time';
  keyword_extraction?: boolean;
  generate_report?: boolean;
}

export interface KeywordEntry {
  word: string;
  count: number;
}

export interface KeywordsResult {
  positive: KeywordEntry[];
  negative: KeywordEntry[];
  neutral: KeywordEntry[];
}

export interface TopicsResult {
  positive: Record<string, number>;
  negative: Record<string, number>;
}

export interface InsightsResult {
  insights: string[];
  source: 'ai' | 'rule_based';
}

export type ExportFormat = 'csv' | 'excel' | 'pdf';

export type CommentSentiment = 'positive' | 'negative' | 'neutral';
export type CommentLanguage = 'ar' | 'en' | 'mixed' | 'other';

export interface CommentEntry {
  id: number;
  author: string;
  text: string;
  likes: number;
  published_at: string | null;
  sentiment: CommentSentiment | null;
  confidence: number | null;
  language: CommentLanguage | null;
  is_spam: boolean;
  spam_reason: string | null;
  is_sarcasm: boolean;
}
