'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { loginRequest } from '@/features/auth/api/auth-api';
import { ApiError } from '@/lib/api-client';
import type { LoginPayload } from '@/features/auth/types';

export function useLogin() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  async function login(payload: LoginPayload) {
    setIsLoading(true);
    setError(null);

    try {
      await loginRequest(payload);
      setIsSuccess(true);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Unable to log in. Please try again.');
    } finally {
      setIsLoading(false);
    }
  }

  return { login, isLoading, error, isSuccess };
}