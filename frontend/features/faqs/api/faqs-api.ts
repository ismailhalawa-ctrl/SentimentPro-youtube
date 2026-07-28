import { getInsight } from '@/features/executive-summary/api/insights-api';
import type { AIFeatureResponse } from '@/features/executive-summary/types';
import type { FAQPayload } from '@/features/faqs/types';

export function getFAQs(jobId: number): Promise<AIFeatureResponse<FAQPayload>> {
  return getInsight<FAQPayload>(jobId, 'faq_generation');
}
