import type { Metadata } from 'next';
import { Suspense } from 'react';
import { Loader2 } from 'lucide-react';
import { LoginForm } from '@/components/auth/login-form';

export const metadata: Metadata = {
  title: 'Log In — SentimentPRO',
};

export default function LoginPage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="text-center">
        <h1 className="text-2xl font-semibold text-text-primary">Welcome back</h1>
        <p className="mt-1 text-sm text-text-secondary">Log in to your account to continue.</p>
      </div>
      {}
      <Suspense
        fallback={
          <div className="flex justify-center py-8">
            <Loader2 className="h-5 w-5 animate-spin text-brand-400" />
          </div>
        }
      >
        <LoginForm />
      </Suspense>
    </div>
  );
}