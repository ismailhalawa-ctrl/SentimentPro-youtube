'use client';

import { getSuggestions } from '@/features/suggestions/api/suggestions-api';
import { useAIFeature } from '@/lib/use-ai-feature';
import type { CommentExtractionPayload } from '@/features/suggestions/types';

export function useSuggestions(jobId: number) {
  return useAIFeature<CommentExtractionPayload>(jobId, getSuggestions, 'Failed to load the suggestions.');
}
