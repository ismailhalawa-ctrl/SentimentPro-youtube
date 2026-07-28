'use client';

import { getComplaints } from '@/features/complaints/api/complaints-api';
import { useAIFeature } from '@/lib/use-ai-feature';
import type { CommentExtractionPayload } from '@/features/complaints/types';

export function useComplaints(jobId: number) {
  return useAIFeature<CommentExtractionPayload>(jobId, getComplaints, 'Failed to load the complaints.');
}
