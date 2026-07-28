'use client';

import { useState } from 'react';
import { updateProfileRequest } from '@/features/auth/api/auth-api';
import { useAuth } from '@/features/auth/auth-provider';
import { ApiError } from '@/lib/api-client';

export function useUpdateProfile() {
  const { setUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  async function updateProfile(fullName: string) {
    setIsLoading(true);
    setError(null);
    setIsSuccess(false);
    try {
      const updated = await updateProfileRequest({ full_name: fullName });
      setUser(updated);
      setIsSuccess(true);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Failed to update profile.');
    } finally {
      setIsLoading(false);
    }
  }

  return { updateProfile, isLoading, error, isSuccess };
}
