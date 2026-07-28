'use client';

import { useEffect, useState } from 'react';
import { getAnalysisInsights, getAnalysisKeywords, getAnalysisTopics } from '@/features/analysis/api/analysis-api';
import type { InsightsResult, KeywordsResult, TopicsResult } from '@/features/analysis/types';

export function useAnalysisExtras(jobId: number, enabled: boolean) {
  const [keywords, setKeywords] = useState<KeywordsResult | null>(null);
  const [topics, setTopics] = useState<TopicsResult | null>(null);
  const [insights, setInsights] = useState<InsightsResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!enabled) return;
    let isMounted = true;
    setIsLoading(true);
    setError(null);

    Promise.all([getAnalysisKeywords(jobId), getAnalysisTopics(jobId), getAnalysisInsights(jobId)])
      .then(([k, t, i]) => {
        if (!isMounted) return;
        setKeywords(k);
        setTopics(t);
        setInsights(i);
      })
      .catch(() => {
        if (isMounted) setError('Failed to load keywords and insights.');
      })
      .finally(() => {
        if (isMounted) setIsLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [jobId, enabled]);

  return { keywords, topics, insights, isLoading, error };
}
