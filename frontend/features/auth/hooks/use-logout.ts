'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { logoutRequest } from '@/features/auth/api/auth-api';

export function useLogout() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  async function logout() {
    setIsLoading(true);
    try {
      await logoutRequest();
    } catch {
    } finally {
      router.push('/login');
    }
  }

  return { logout, isLoading };
}
