'use client';

import { useEffect, useState } from 'react';
import { API_BASE_URL } from '@/lib/api-client';

export function GoogleSignInButton() {
  const [href, setHref] = useState<string | undefined>(undefined);

  useEffect(() => {
    setHref(`${API_BASE_URL}/api/v1/auth/google/login`);
  }, []);

  return (
    <a
      href={href}
      className="flex w-full items-center justify-center gap-2.5 rounded-full border border-border-default bg-background-surface px-6 py-3 text-sm font-medium text-text-primary transition-colors hover:bg-background-elevated"
    >
      <svg viewBox="0 0 24 24" className="h-4.5 w-4.5" aria-hidden="true">
        <path
          fill="#4285F4"
          d="M23.52 12.27c0-.85-.08-1.67-.22-2.45H12v4.64h6.47a5.53 5.53 0 0 1-2.4 3.63v3h3.87c2.27-2.09 3.58-5.17 3.58-8.82Z"
        />
        <path
          fill="#34A853"
          d="M12 24c3.24 0 5.96-1.07 7.94-2.91l-3.87-3c-1.08.72-2.45 1.15-4.07 1.15-3.13 0-5.78-2.11-6.73-4.96H1.28v3.11A11.997 11.997 0 0 0 12 24Z"
        />
        <path
          fill="#FBBC05"
          d="M5.27 14.28A7.2 7.2 0 0 1 4.89 12c0-.79.14-1.56.38-2.28V6.61H1.28A11.997 11.997 0 0 0 0 12c0 1.94.46 3.77 1.28 5.39l3.99-3.11Z"
        />
        <path
          fill="#EA4335"
          d="M12 4.77c1.76 0 3.35.61 4.6 1.8l3.43-3.43C17.95 1.19 15.24 0 12 0 7.31 0 3.26 2.69 1.28 6.61l3.99 3.11C6.22 6.88 8.87 4.77 12 4.77Z"
        />
      </svg>
      Continue with Google
    </a>
  );
}
