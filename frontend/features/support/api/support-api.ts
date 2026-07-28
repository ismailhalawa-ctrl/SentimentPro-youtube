import { apiClient } from '@/lib/api-client';

export interface SupportMessagePayload {
  name: string;
  email: string;
  message: string;
}

export function submitContactMessage(payload: SupportMessagePayload): Promise<{ message: string }> {
  return apiClient<{ message: string }>('/api/v1/support/contact', {
    method: 'POST',
    body: payload,
  });
}
