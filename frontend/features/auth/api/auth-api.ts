import { apiClient } from '@/lib/api-client';
import type { LoginPayload, RegisterPayload, User } from '@/features/auth/types';

export function loginRequest(payload: LoginPayload): Promise<User> {
  return apiClient<User>('/api/v1/auth/login', {
    method: 'POST',
    body: payload,
  });
}

export function registerRequest(payload: RegisterPayload): Promise<User> {
  return apiClient<User>('/api/v1/auth/register', {
    method: 'POST',
    body: payload,
  });
}

export function meRequest(): Promise<User> {
  return apiClient<User>('/api/v1/auth/me', { method: 'GET' });
}

export function logoutRequest(): Promise<void> {
  return apiClient<void>('/api/v1/auth/logout', { method: 'POST' });
}

export function updateProfileRequest(payload: { full_name: string }): Promise<User> {
  return apiClient<User>('/api/v1/users/me', {
    method: 'PATCH',
    body: payload,
  });
}

export function forgotPasswordRequest(email: string): Promise<{ message: string }> {
  return apiClient<{ message: string }>('/api/v1/auth/forgot-password', {
    method: 'POST',
    body: { email },
  });
}

export function resetPasswordRequest(token: string, newPassword: string): Promise<{ message: string }> {
  return apiClient<{ message: string }>('/api/v1/auth/reset-password', {
    method: 'POST',
    body: { token, new_password: newPassword },
  });
}

export function deleteAccountRequest(payload: { password?: string; confirmation?: string }): Promise<void> {
  return apiClient<void>('/api/v1/users/me', {
    method: 'DELETE',
    body: payload,
  });
}