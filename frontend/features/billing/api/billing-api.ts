import { apiClient } from '@/lib/api-client';

export interface SubscriptionStatus {
  tier: string;
  status: string;
  current_period_end: string | null;
}

export function getSubscriptionStatus(): Promise<SubscriptionStatus> {
  return apiClient<SubscriptionStatus>('/api/v1/billing/subscription', { method: 'GET' });
}

export function createCheckoutSession(): Promise<{ checkout_url: string }> {
  return apiClient<{ checkout_url: string }>('/api/v1/billing/checkout-session', { method: 'POST' });
}

export function createPortalSession(): Promise<{ portal_url: string }> {
  return apiClient<{ portal_url: string }>('/api/v1/billing/portal-session', { method: 'POST' });
}
