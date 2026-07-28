'use client';

import { useState } from 'react';
import { forgotPasswordRequest } from '@/features/auth/api/auth-api';
import { ApiError } from '@/lib/api-client';

export function useForgotPassword() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  async function requestReset(email: string) {
    setIsLoading(true);
    setError(null);
    try {
      await forgotPasswordRequest(email);
      setIsSuccess(true);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }

  return { requestReset, isLoading, error, isSuccess };
}
