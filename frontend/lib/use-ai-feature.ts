'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { ApiError } from '@/lib/api-client';
import type { AIFeatureResponse, AIFeatureStatus } from '@/features/executive-summary/types';

export function useAIFeature<T>(
  jobId: number,
  fetcher: (jobId: number) => Promise<AIFeatureResponse<T>>,
  fallbackErrorMessage: string
) {
  const [data, setData] = useState<T | null>(null);
  const [status, setStatus] = useState<AIFeatureStatus | 'loading'>('loading');
  const [reason, setReason] = useState<string | null>(null);

  const fetcherRef = useRef(fetcher);
  useEffect(() => {
    fetcherRef.current = fetcher;
  });

  const refresh = useCallback(async () => {
    setStatus('loading');
    setReason(null);
    try {
      const response = await fetcherRef.current(jobId);
      setData(response.data);
      setStatus(response.status);
      setReason(response.reason);
    } catch (err) {
      setStatus('error');
      setReason(err instanceof ApiError ? err.message : fallbackErrorMessage);
    }
  }, [jobId, fallbackErrorMessage]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { data, status, reason, isLoading: status === 'loading', refresh };
}
