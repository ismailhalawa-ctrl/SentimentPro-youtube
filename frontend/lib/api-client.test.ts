import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { apiClient, ApiError } from './api-client';

describe('apiClient', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('sends credentials and a JSON content-type header by default', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ ok: true }), { status: 200 }));

    await apiClient('/api/v1/whatever');

    const [, init] = vi.mocked(fetch).mock.calls[0];
    expect(init?.credentials).toBe('include');
    expect((init?.headers as Record<string, string>)['Content-Type']).toBe('application/json');
  });

  it('serializes a body object to JSON', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({}), { status: 200 }));

    await apiClient('/api/v1/whatever', { body: { email: 'a@b.com' } });

    const [, init] = vi.mocked(fetch).mock.calls[0];
    expect(init?.body).toBe(JSON.stringify({ email: 'a@b.com' }));
  });

  it('returns parsed JSON on success', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({ id: 1, name: 'test' }), { status: 200 }));

    const result = await apiClient<{ id: number; name: string }>('/api/v1/whatever');
    expect(result).toEqual({ id: 1, name: 'test' });
  });

  it('returns undefined for a 204 response without attempting to parse a body', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(null, { status: 204 }));

    const result = await apiClient('/api/v1/whatever');
    expect(result).toBeUndefined();
  });

  it('throws an ApiError with a plain string detail message', async () => {
    vi.mocked(fetch).mockResolvedValue(
      new Response(JSON.stringify({ detail: 'Invalid credentials.' }), { status: 401 })
    );

    await expect(apiClient('/api/v1/whatever')).rejects.toMatchObject({
      message: 'Invalid credentials.',
      status: 401,
    });
  });

  it('joins FastAPI-style validation error arrays into one message', async () => {
    vi.mocked(fetch).mockResolvedValue(
      new Response(
        JSON.stringify({
          detail: [{ msg: 'Value error, password must be at least 8 characters' }, { msg: 'field required' }],
        }),
        { status: 422 }
      )
    );

    await expect(apiClient('/api/v1/whatever')).rejects.toThrow(
      'password must be at least 8 characters field required'
    );
  });

  it('extracts a message from a structured object detail and preserves it', async () => {
    vi.mocked(fetch).mockResolvedValue(
      new Response(
        JSON.stringify({ detail: { message: 'Cooldown active.', days_remaining: 3 } }),
        { status: 429 }
      )
    );

    try {
      await apiClient('/api/v1/whatever');
      expect.unreachable();
    } catch (err) {
      expect(err).toBeInstanceOf(ApiError);
      const apiError = err as ApiError;
      expect(apiError.message).toBe('Cooldown active.');
      expect(apiError.detail).toEqual({ message: 'Cooldown active.', days_remaining: 3 });
    }
  });

  it('falls back to a generic message when the error body is not valid JSON', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response('not json', { status: 500 }));

    await expect(apiClient('/api/v1/whatever')).rejects.toMatchObject({
      message: 'Something went wrong. Please try again.',
      status: 500,
    });
  });

  it('rejects with an ApiError instance, not a plain Error', async () => {
    vi.mocked(fetch).mockResolvedValue(new Response(JSON.stringify({}), { status: 400 }));

    await expect(apiClient('/api/v1/whatever')).rejects.toBeInstanceOf(ApiError);
  });
});
