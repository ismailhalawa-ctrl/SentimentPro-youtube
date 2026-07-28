import { apiClient, API_BASE_URL } from '@/lib/api-client';
import type {
  AnalysisJob,
  CommentEntry,
  CreateAnalysisJobPayload,
  ExportFormat,
  InsightsResult,
  KeywordsResult,
  TopicsResult,
} from '@/features/analysis/types';

export function createAnalysisJob(payload: CreateAnalysisJobPayload): Promise<AnalysisJob> {
  return apiClient<AnalysisJob>('/api/v1/analysis/jobs', {
    method: 'POST',
    body: payload,
  });
}

export function getAnalysisJob(jobId: number): Promise<AnalysisJob> {
  return apiClient<AnalysisJob>(`/api/v1/analysis/jobs/${jobId}`, { method: 'GET' });
}

export function cancelAnalysisJob(jobId: number): Promise<AnalysisJob> {
  return apiClient<AnalysisJob>(`/api/v1/analysis/jobs/${jobId}/cancel`, { method: 'POST' });
}

export function listAnalysisJobs(): Promise<{ jobs: AnalysisJob[] }> {
  return apiClient<{ jobs: AnalysisJob[] }>('/api/v1/analysis/jobs', { method: 'GET' });
}

export function deleteAnalysisJob(jobId: number): Promise<void> {
  return apiClient<void>(`/api/v1/analysis/jobs/${jobId}`, { method: 'DELETE' });
}

export function clearAllAnalysisJobs(): Promise<{ deleted_count: number }> {
  return apiClient<{ deleted_count: number }>('/api/v1/analysis/jobs/clear-all', { method: 'DELETE' });
}

export function getAnalysisKeywords(jobId: number): Promise<KeywordsResult> {
  return apiClient<KeywordsResult>(`/api/v1/analysis/jobs/${jobId}/keywords`, { method: 'GET' });
}

export function getAnalysisTopics(jobId: number): Promise<TopicsResult> {
  return apiClient<TopicsResult>(`/api/v1/analysis/jobs/${jobId}/topics`, { method: 'GET' });
}

export function getAnalysisInsights(jobId: number): Promise<InsightsResult> {
  return apiClient<InsightsResult>(`/api/v1/analysis/jobs/${jobId}/insights`, { method: 'GET' });
}

export function getAnalysisComments(jobId: number): Promise<{ comments: CommentEntry[] }> {
  return apiClient<{ comments: CommentEntry[] }>(`/api/v1/analysis/jobs/${jobId}/comments`, {
    method: 'GET',
  });
}

const EXPORT_EXTENSIONS: Record<ExportFormat, string> = {
  csv: 'csv',
  excel: 'xlsx',
  pdf: 'pdf',
};

export async function exportAnalysisJob(
  jobId: number,
  format: ExportFormat
): Promise<{ blob: Blob; extension: string }> {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/analysis/jobs/${jobId}/export?format=${format}`,
    { method: 'GET', credentials: 'include' }
  );
  if (!response.ok) {
    throw new Error(`Failed to export analysis as ${format.toUpperCase()}.`);
  }
  return { blob: await response.blob(), extension: EXPORT_EXTENSIONS[format] };
}
