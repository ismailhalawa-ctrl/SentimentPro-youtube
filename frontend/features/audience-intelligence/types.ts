export interface AudienceIntelligenceScores {
  satisfaction_score: number;
  community_health_score: number;
  loyalty_score: number;
}

export interface AudienceIntelligenceScorePayload {
  scores: AudienceIntelligenceScores;
  emerging_trends: string[];
  growth_opportunities: string[];
}
