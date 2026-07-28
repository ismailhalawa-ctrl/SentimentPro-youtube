'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { deleteAccountRequest } from '@/features/auth/api/auth-api';
import { ApiError } from '@/lib/api-client';

export function useDeleteAccount() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function deleteAccount(payload: { password?: string; confirmation?: string }) {
    setIsLoading(true);
    setError(null);

    try {
      await deleteAccountRequest(payload);
      router.push('/');
      router.refresh();
      return true;
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Unable to delete your account. Please try again.');
      return false;
    } finally {
      setIsLoading(false);
    }
  }

  return { deleteAccount, isLoading, error, setError };
}
