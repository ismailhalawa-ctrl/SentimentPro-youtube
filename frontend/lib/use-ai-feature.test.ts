import { act, renderHook, waitFor } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { ApiError } from './api-client';
import { useAIFeature } from './use-ai-feature';

describe('useAIFeature', () => {
  it('starts in the loading state and resolves to ok with data', async () => {
    const fetcher = vi.fn().mockResolvedValue({ status: 'ok', data: { value: 42 }, reason: null });
    const { result } = renderHook(() => useAIFeature(1, fetcher, 'fallback'));

    expect(result.current.status).toBe('loading');
    expect(result.current.isLoading).toBe(true);

    await waitFor(() => expect(result.current.status).toBe('ok'));
    expect(result.current.data).toEqual({ value: 42 });
    expect(result.current.isLoading).toBe(false);
  });

  it('passes through unavailable status and reason from the response', async () => {
    const fetcher = vi.fn().mockResolvedValue({
      status: 'unavailable',
      data: null,
      reason: 'No API key configured.',
    });
    const { result } = renderHook(() => useAIFeature(1, fetcher, 'fallback'));

    await waitFor(() => expect(result.current.status).toBe('unavailable'));
    expect(result.current.reason).toBe('No API key configured.');
    expect(result.current.data).toBeNull();
  });

  it('uses the ApiError message when the fetcher throws an ApiError', async () => {
    const fetcher = vi.fn().mockRejectedValue(new ApiError('Rate limit exceeded.', 429));
    const { result } = renderHook(() => useAIFeature(1, fetcher, 'fallback message'));

    await waitFor(() => expect(result.current.status).toBe('error'));
    expect(result.current.reason).toBe('Rate limit exceeded.');
  });

  it('falls back to the provided message when a non-ApiError is thrown', async () => {
    const fetcher = vi.fn().mockRejectedValue(new TypeError('network down'));
    const { result } = renderHook(() => useAIFeature(1, fetcher, 'Failed to load the report.'));

    await waitFor(() => expect(result.current.status).toBe('error'));
    expect(result.current.reason).toBe('Failed to load the report.');
  });

  it('calls the fetcher again when refresh is invoked', async () => {
    const fetcher = vi.fn().mockResolvedValue({ status: 'ok', data: { value: 1 }, reason: null });
    const { result } = renderHook(() => useAIFeature(7, fetcher, 'fallback'));

    await waitFor(() => expect(result.current.status).toBe('ok'));
    expect(fetcher).toHaveBeenCalledTimes(1);
    expect(fetcher).toHaveBeenCalledWith(7);

    await act(async () => {
      await result.current.refresh();
    });
    expect(fetcher).toHaveBeenCalledTimes(2);
  });

  it('re-fetches automatically when jobId changes', async () => {
    const fetcher = vi.fn().mockResolvedValue({ status: 'ok', data: { value: 1 }, reason: null });
    const { rerender } = renderHook(({ jobId }) => useAIFeature(jobId, fetcher, 'fallback'), {
      initialProps: { jobId: 1 },
    });

    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(1));

    rerender({ jobId: 2 });
    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(2));
    expect(fetcher).toHaveBeenLastCalledWith(2);
  });

  it('does not re-fetch when an inline fetcher function is passed with the same jobId', async () => {
    const spy = vi.fn().mockResolvedValue({ status: 'ok', data: null, reason: null });
    const { rerender } = renderHook(({ jobId }) => useAIFeature(jobId, (id) => spy(id), 'fallback'), {
      initialProps: { jobId: 1 },
    });

    await waitFor(() => expect(spy).toHaveBeenCalledTimes(1));

    rerender({ jobId: 1 });
    await new Promise((resolve) => setTimeout(resolve, 10));
    expect(spy).toHaveBeenCalledTimes(1);
  });
});
