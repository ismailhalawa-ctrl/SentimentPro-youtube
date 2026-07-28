'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { cancelAnalysisJob, getAnalysisJob } from '@/features/analysis/api/analysis-api';
import { ApiError } from '@/lib/api-client';
import type { AnalysisJob } from '@/features/analysis/types';

const POLL_INTERVAL_MS = 1500;

export function useAnalysisJobDetail(jobId: number) {
  const [job, setJob] = useState<AnalysisJob | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCancelling, setIsCancelling] = useState(false);
  const pollTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const isMounted = useRef(true);

  const isFirstFetch = useRef(true);
  const refreshRef = useRef<() => void>(() => {});

  const refresh = useCallback(async () => {
    if (isFirstFetch.current) setIsLoading(true);
    setError(null);
    try {
      const latest = await getAnalysisJob(jobId);
      if (!isMounted.current) return;
      setJob(latest);
      if (latest.status === 'pending' || latest.status === 'processing') {
        if (pollTimer.current) clearTimeout(pollTimer.current);
        pollTimer.current = setTimeout(() => refreshRef.current(), POLL_INTERVAL_MS);
      }
    } catch (err) {
      if (!isMounted.current) return;
      setError(err instanceof ApiError ? err.message : 'Failed to load this analysis.');
    } finally {
      if (isMounted.current) setIsLoading(false);
      isFirstFetch.current = false;
    }
  }, [jobId]);

  useEffect(() => {
    refreshRef.current = refresh;
  });

  useEffect(() => {
    isMounted.current = true;
    isFirstFetch.current = true;
    refresh();
    return () => {
      isMounted.current = false;
      if (pollTimer.current) clearTimeout(pollTimer.current);
    };
  }, [refresh]);

  const cancel = useCallback(async () => {
    if (!job || (job.status !== 'pending' && job.status !== 'processing')) return;
    if (pollTimer.current) clearTimeout(pollTimer.current);
    setIsCancelling(true);
    try {
      const updated = await cancelAnalysisJob(job.id);
      if (!isMounted.current) return;
      setJob(updated);
    } catch (err) {
      if (!isMounted.current) return;
      setError(err instanceof ApiError ? err.message : 'Failed to cancel analysis.');
    } finally {
      if (isMounted.current) setIsCancelling(false);
    }
  }, [job]);

  return { job, isLoading, error, isCancelling, refresh, cancel };
}
