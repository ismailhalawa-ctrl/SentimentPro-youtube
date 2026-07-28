'use client';

import { getInsight } from '@/features/executive-summary/api/insights-api';
import { useAIFeature } from '@/lib/use-ai-feature';
import type { ExecutiveSummaryPayload } from '@/features/executive-summary/types';

export function useExecutiveSummary(jobId: number) {
  return useAIFeature<ExecutiveSummaryPayload>(
    jobId,
    (id) => getInsight<ExecutiveSummaryPayload>(id, 'executive_summary'),
    'Failed to load the executive summary.'
  );
}
