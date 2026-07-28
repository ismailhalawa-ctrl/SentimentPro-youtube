import Link from 'next/link';
import { SearchX } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-background-base px-4 text-center">
      <span className="flex h-12 w-12 items-center justify-center rounded-full bg-brand-500/15 text-brand-400">
        <SearchX className="h-6 w-6" />
      </span>
      <div className="flex flex-col gap-1.5">
        <h1 className="text-xl font-semibold text-text-primary">Page not found</h1>
        <p className="max-w-sm text-sm text-text-secondary">
          The page you&apos;re looking for doesn&apos;t exist or may have moved.
        </p>
      </div>
      <Link
        href="/"
        className="rounded-md bg-brand-500 px-5 py-2.5 text-sm font-medium text-text-primary transition-colors hover:bg-brand-600"
      >
        Back to home
      </Link>
    </div>
  );
}
