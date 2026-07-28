function resolveApiBaseUrl(): string {
  if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL;
  if (typeof window !== 'undefined') return `${window.location.protocol}//${window.location.hostname}:8000`;
  return 'http://localhost:8000';
}

export const API_BASE_URL = resolveApiBaseUrl();

export class ApiError extends Error {
  status: number;
  detail?: Record<string, unknown>;

  constructor(message: string, status: number, detail?: Record<string, unknown>) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.detail = detail;
  }
}

interface RequestOptions extends Omit<RequestInit, 'body'> {
  body?: unknown;
}

export async function apiClient<TResponse>(
  path: string,
  { body, headers, ...options }: RequestOptions = {}
): Promise<TResponse> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let message = 'Something went wrong. Please try again.';
    let detail: Record<string, unknown> | undefined;
    try {
      const errorBody = await response.json();
      if (typeof errorBody?.detail === 'string') {
        message = errorBody.detail;
      } else if (Array.isArray(errorBody?.detail)) {
        const messages = errorBody.detail
          .map((item: { msg?: string }) =>
            typeof item?.msg === 'string' ? item.msg.replace(/^Value error, /, '') : null
          )
          .filter((msg: string | null): msg is string => Boolean(msg));
        if (messages.length > 0) message = messages.join(' ');
      } else if (errorBody?.detail && typeof errorBody.detail === 'object') {
        detail = errorBody.detail;
        if (detail && typeof detail.message === 'string') message = detail.message;
      }
    } catch {}
    throw new ApiError(message, response.status, detail);
  }

  if (response.status === 204) {
    return undefined as TResponse;
  }

  return response.json() as Promise<TResponse>;
}