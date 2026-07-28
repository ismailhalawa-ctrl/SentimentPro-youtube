'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { registerRequest, loginRequest } from '@/features/auth/api/auth-api';
import { ApiError } from '@/lib/api-client';
import type { RegisterPayload } from '@/features/auth/types';

export function useRegister() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  async function register(payload: RegisterPayload) {
    setIsLoading(true);
    setError(null);

    try {
      await registerRequest(payload);

      await loginRequest({
        email: payload.email,
        password: payload.password,
      });

      setIsSuccess(true);

      router.push('/dashboard');
      router.refresh();
    } catch (err) {
      setError(
        err instanceof ApiError ? err.message : 'Unable to create your account. Please try again.'
      );
    } finally {
      setIsLoading(false);
    }
  }

  return { register, isLoading, error, isSuccess };
}