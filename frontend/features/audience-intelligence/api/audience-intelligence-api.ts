import { apiClient } from '@/lib/api-client';
import type { AIFeatureResponse } from '@/features/executive-summary/types';
import type { AudienceIntelligenceScorePayload } from '@/features/audience-intelligence/types';

export function getAudienceIntelligence(
  jobId: number
): Promise<AIFeatureResponse<AudienceIntelligenceScorePayload>> {
  return apiClient<AIFeatureResponse<AudienceIntelligenceScorePayload>>(
    `/api/v1/analysis/jobs/${jobId}/audience-intelligence`,
    { method: 'GET' }
  );
}
