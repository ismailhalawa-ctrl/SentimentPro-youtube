import { getCommentInsight } from '@/features/executive-summary/api/insights-api';
import type { AIFeatureResponse } from '@/features/executive-summary/types';
import type { CommentExtractionPayload } from '@/features/suggestions/types';

export function getSuggestions(jobId: number): Promise<AIFeatureResponse<CommentExtractionPayload>> {
  return getCommentInsight<CommentExtractionPayload>(jobId, 'suggestion_extraction');
}
