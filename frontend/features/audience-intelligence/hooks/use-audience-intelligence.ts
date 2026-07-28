'use client';

import { getAudienceIntelligence } from '@/features/audience-intelligence/api/audience-intelligence-api';
import { useAIFeature } from '@/lib/use-ai-feature';
import type { AudienceIntelligenceScorePayload } from '@/features/audience-intelligence/types';

export function useAudienceIntelligence(jobId: number) {
  return useAIFeature<AudienceIntelligenceScorePayload>(
    jobId,
    getAudienceIntelligence,
    'Failed to load audience intelligence.'
  );
}
