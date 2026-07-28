import { getInsight } from '@/features/executive-summary/api/insights-api';
import type { AIFeatureResponse } from '@/features/executive-summary/types';
import type { TopicClusteringPayload } from '@/features/topics/types';

export function getTopics(jobId: number): Promise<AIFeatureResponse<TopicClusteringPayload>> {
  return getInsight<TopicClusteringPayload>(jobId, 'topic_clustering');
}
