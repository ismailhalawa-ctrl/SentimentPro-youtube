'use client';

import { getTopics } from '@/features/topics/api/topics-api';
import { useAIFeature } from '@/lib/use-ai-feature';
import type { TopicClusteringPayload } from '@/features/topics/types';

export function useTopics(jobId: number) {
  return useAIFeature<TopicClusteringPayload>(jobId, getTopics, 'Failed to load the topics.');
}
