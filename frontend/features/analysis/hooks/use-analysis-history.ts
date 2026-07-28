'use client';

import { useCallback, useEffect, useState } from 'react';
import { listAnalysisJobs } from '@/features/analysis/api/analysis-api';
import { ApiError } from '@/lib/api-client';
import type { AnalysisJob } from '@/features/analysis/types';

export function useAnalysisHistory() {
  const [jobs, setJobs] = useState<AnalysisJob[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const { jobs } = await listAnalysisJobs();
      setJobs(jobs);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to load analysis history.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const removeJobLocally = useCallback((jobId: number) => {
    setJobs((current) => current.filter((job) => job.id !== jobId));
  }, []);

  const clearJobsLocally = useCallback(() => {
    setJobs([]);
  }, []);

  return { jobs, isLoading, error, refresh, removeJobLocally, clearJobsLocally };
}
