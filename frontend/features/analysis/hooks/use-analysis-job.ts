'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import { cancelAnalysisJob, createAnalysisJob, getAnalysisJob } from '@/features/analysis/api/analysis-api';
import { ApiError } from '@/lib/api-client';
import type { AnalysisJob, CreateAnalysisJobPayload } from '@/features/analysis/types';

const POLL_INTERVAL_MS = 1500;

export function useAnalysisJob() {
  const [job, setJob] = useState<AnalysisJob | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isStarting, setIsStarting] = useState(false);
  const [isCancelling, setIsCancelling] = useState(false);
  const pollTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const isMounted = useRef(true);

  useEffect(() => {
    isMounted.current = true;
    return () => {
      isMounted.current = false;
      if (pollTimer.current) clearTimeout(pollTimer.current);
    };
  }, []);

  async function poll(jobId: number) {
    try {
      const latest = await getAnalysisJob(jobId);
      if (!isMounted.current) return;
      setJob(latest);

      if (latest.status === 'pending' || latest.status === 'processing') {
        pollTimer.current = setTimeout(() => poll(jobId), POLL_INTERVAL_MS);
      }
    } catch (err) {
      if (!isMounted.current) return;
      setError(err instanceof ApiError ? err.message : 'Lost connection while checking analysis status.');
    }
  }

  const start = useCallback(async (payload: CreateAnalysisJobPayload) => {
    setError(null);
    setJob(null);
    setIsStarting(true);
    try {
      const created = await createAnalysisJob(payload);
      if (!isMounted.current) return;
      setJob(created);
      pollTimer.current = setTimeout(() => poll(created.id), POLL_INTERVAL_MS);
    } catch (err) {
      if (!isMounted.current) return;
      setError(err instanceof ApiError ? err.message : 'Failed to start analysis.');
    } finally {
      if (isMounted.current) setIsStarting(false);
    }
  }, []);

  const reset = useCallback(() => {
    if (pollTimer.current) clearTimeout(pollTimer.current);
    setJob(null);
    setError(null);
  }, []);

  const cancel = useCallback(async () => {
    if (!job || (job.status !== 'pending' && job.status !== 'processing')) return;
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

  const isRunning = isStarting || job?.status === 'pending' || job?.status === 'processing';

  return { job, error, isStarting, isCancelling, isRunning, start, cancel, reset };
}
