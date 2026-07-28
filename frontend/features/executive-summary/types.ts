export type AIFeatureStatus = 'ok' | 'unavailable' | 'error' | 'partial' | 'rate_limited';

export interface AIFeatureResponse<T> {
  status: AIFeatureStatus;
  data: T | null;
  reason: string | null;
}

export interface ExecutiveSummaryPayload {
  overview: string;
  key_positives: string[];
  key_negatives: string[];
  notable_trends: string[];
  overall_sentiment_label: 'positive' | 'neutral' | 'negative' | 'mixed';
}

export interface ViewerSegment {
  name: string;
  description: string;
  estimated_share: string;
}

export interface AudienceAnalysisPayload {
  personality_profile: string;
  viewer_segments: ViewerSegment[];
  behavior_notes: string[];
  emotional_trend: string;
}
