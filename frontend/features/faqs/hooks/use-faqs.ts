'use client';

import { getFAQs } from '@/features/faqs/api/faqs-api';
import { useAIFeature } from '@/lib/use-ai-feature';
import type { FAQPayload } from '@/features/faqs/types';

export function useFAQs(jobId: number) {
  return useAIFeature<FAQPayload>(jobId, getFAQs, 'Failed to load the FAQs.');
}
