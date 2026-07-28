'use client';

import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { meRequest } from '@/features/auth/api/auth-api';
import { ApiError } from '@/lib/api-client';
import type { User } from '@/features/auth/types';

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  error: string | null;
  setUser: (user: User) => void;
  retry: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [attempt, setAttempt] = useState(0);

  const retry = useCallback(() => {
    setIsLoading(true);
    setError(null);
    setAttempt((n) => n + 1);
  }, []);

  useEffect(() => {
    let isMounted = true;

    meRequest()
      .then((result) => {
        if (isMounted) setUser(result);
      })
      .catch((err) => {
        if (err instanceof ApiError && err.status === 401) {
          router.replace('/login');
          return;
        }
        if (isMounted) {
          setError(err instanceof ApiError ? err.message : 'Unable to reach the server. Please try again.');
        }
      })
      .finally(() => {
        if (isMounted) setIsLoading(false);
      });

    return () => {
      isMounted = false;
    };
  }, [router, attempt]);

  return (
    <AuthContext.Provider value={{ user, isLoading, error, setUser, retry }}>{children}</AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider (see app/dashboard/layout.tsx).');
  }
  return context;
}
