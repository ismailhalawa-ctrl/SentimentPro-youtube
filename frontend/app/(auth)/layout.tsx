import Link from 'next/link';
import { Sparkles } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden px-4 py-12">
      <div className="bg-radial-glow pointer-events-none absolute inset-0" />

      <div className="relative w-full max-w-md">
        <Link href="/" className="mb-8 flex items-center justify-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-brand">
            <Sparkles className="h-4 w-4 text-text-primary" />
          </span>
          <span className="text-base font-semibold text-text-primary">
            Sentiment<span className="text-brand-400">PRO</span>
          </span>
        </Link>

        <Card variant="glass" className="p-8">
          <CardContent className="p-0">{children}</CardContent>
        </Card>

        <p className="mt-6 text-center text-xs text-text-muted">
          By continuing, you agree to our{' '}
          <Link href="/terms" className="text-text-secondary hover:text-text-primary">
            Terms of Service
          </Link>{' '}
          and{' '}
          <Link href="/privacy" className="text-text-secondary hover:text-text-primary">
            Privacy Policy
          </Link>
          .
        </p>
      </div>
    </div>
  );
}