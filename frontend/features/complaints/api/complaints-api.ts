import { getCommentInsight } from '@/features/executive-summary/api/insights-api';
import type { AIFeatureResponse } from '@/features/executive-summary/types';
import type { CommentExtractionPayload } from '@/features/complaints/types';

export function getComplaints(jobId: number): Promise<AIFeatureResponse<CommentExtractionPayload>> {
  return getCommentInsight<CommentExtractionPayload>(jobId, 'complaint_extraction');
}
