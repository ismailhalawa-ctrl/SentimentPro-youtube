'use client';

import { useEffect, useState } from 'react';
import { getAnalysisComments } from '@/features/analysis/api/analysis-api';
import type { CommentEntry } from '@/features/analysis/types';

export function useAnalysisComments(jobId: number, enabled: boolean) {
  const [comments, setComments] = useState<CommentEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled) return;
    let isMounted = true;
    setIsLoading(true);
    setError(null);

    getAnalysisComments(jobId)
      .then((result) => {
        if (isMounted) setComments(result.comments);
      })
      .catch(() => {
        if (isMounted) setError('Failed to load comments.');
      })
      .finally(() => {
        if (isMounted) setIsLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [jobId, enabled]);

  return { comments, isLoading, error };
}
