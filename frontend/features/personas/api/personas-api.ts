import { getInsight } from '@/features/executive-summary/api/insights-api';
import type { AIFeatureResponse, AudienceAnalysisPayload } from '@/features/executive-summary/types';

export function getPersonas(jobId: number): Promise<AIFeatureResponse<AudienceAnalysisPayload>> {
  return getInsight<AudienceAnalysisPayload>(jobId, 'audience_analysis');
}
