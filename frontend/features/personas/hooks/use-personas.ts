'use client';

import { getPersonas } from '@/features/personas/api/personas-api';
import { useAIFeature } from '@/lib/use-ai-feature';
import type { AudienceAnalysisPayload } from '@/features/executive-summary/types';

export function usePersonas(jobId: number) {
  return useAIFeature<AudienceAnalysisPayload>(jobId, getPersonas, 'Failed to load audience personas.');
}
