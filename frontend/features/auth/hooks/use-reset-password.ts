'use client';

import { useState } from 'react';
import { resetPasswordRequest } from '@/features/auth/api/auth-api';
import { ApiError } from '@/lib/api-client';

export function useResetPassword() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  async function resetPassword(token: string, newPassword: string) {
    setIsLoading(true);
    setError(null);
    try {
      await resetPasswordRequest(token, newPassword);
      setIsSuccess(true);
    } catch (err) {
      setError(
        err instanceof ApiError ? err.message : 'Failed to reset password. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  }

  return { resetPassword, isLoading, error, isSuccess };
}
