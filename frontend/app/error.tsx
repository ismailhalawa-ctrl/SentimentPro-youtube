'use client';

import { useEffect } from 'react';
import { AlertTriangle } from 'lucide-react';

export default function Error({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background-base px-4 text-center">
      <span className="flex h-12 w-12 items-center justify-center rounded-full bg-feedback-danger/15 text-feedback-danger">
        <AlertTriangle className="h-6 w-6" />
      </span>
      <div className="flex flex-col gap-1.5">
        <h1 className="text-xl font-semibold text-text-primary">Something went wrong</h1>
        <p className="max-w-sm text-sm text-text-secondary">
          An unexpected error occurred. You can try again, or head back to the dashboard.
        </p>
      </div>
      <div className="flex items-center gap-3">
        <button
          onClick={reset}
          className="rounded-md bg-brand-500 px-5 py-2.5 text-sm font-medium text-text-primary transition-colors hover:bg-brand-600"
        >
          Try again
        </button>
        <a
          href="/dashboard"
          className="rounded-md border border-border-default bg-background-elevated px-5 py-2.5 text-sm font-medium text-text-primary transition-colors hover:border-brand-400"
        >
          Go to dashboard
        </a>
      </div>
    </div>
  );
}
