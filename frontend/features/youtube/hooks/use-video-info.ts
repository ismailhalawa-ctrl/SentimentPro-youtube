'use client';

import { useEffect, useState } from 'react';
import { videoInfoRequest } from '../api/youtube-api';
import { ApiError } from '@/lib/api-client';
import type { VideoInfo } from '../types';

const DEBOUNCE_MS = 500;

interface UseVideoInfoResult {
  data: VideoInfo | null;
  isLoading: boolean;
  error: string | null;
}

export function useVideoInfo(url: string): UseVideoInfoResult {
  const [data, setData] = useState<VideoInfo | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!url || !url.trim()) {
      setData(null);
      setError(null);
      setIsLoading(false);
      return;
    }

    let isCancelled = false;
    setIsLoading(true);
    setError(null);

    const timer = setTimeout(() => {
      videoInfoRequest(url)
        .then((result) => {
          if (!isCancelled) {
            setData(result);
          }
        })
        .catch((err) => {
          if (isCancelled) return;
          setData(null);

          const backendMessage = err?.response?.data?.detail;
          if (backendMessage) {
            setError(backendMessage);
          } else {
            setError(err instanceof ApiError ? err.message : 'Unable to fetch video info.');
          }
        })
        .finally(() => {
          if (!isCancelled) {
            setIsLoading(false);
          }
        });
    }, DEBOUNCE_MS);

    return () => {
      isCancelled = true;
      clearTimeout(timer);
    };
  }, [url]);

  return { data, isLoading, error };
}