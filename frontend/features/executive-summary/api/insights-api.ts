import { apiClient } from '@/lib/api-client';
import type { AIFeatureResponse } from '@/features/executive-summary/types';

export function getInsight<T>(jobId: number, capability: string): Promise<AIFeatureResponse<T>> {
  return apiClient<AIFeatureResponse<T>>(`/api/v1/analysis/jobs/${jobId}/ai-insights/${capability}`, {
    method: 'GET',
  });
}

export function getCommentInsight<T>(jobId: number, capability: string): Promise<AIFeatureResponse<T>> {
  return apiClient<AIFeatureResponse<T>>(
    `/api/v1/analysis/jobs/${jobId}/comment-insights/${capability}`,
    { method: 'GET' }
  );
}
