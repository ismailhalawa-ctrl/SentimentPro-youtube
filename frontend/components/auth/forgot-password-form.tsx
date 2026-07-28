'use client';

import { useState } from 'react';
import Link from 'next/link';
import { AlertCircle, ArrowLeft, MailCheck } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { FormField } from '@/components/forms/form-field';
import { useForgotPassword } from '@/features/auth/hooks/use-forgot-password';

function validateEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function ForgotPasswordForm() {
  const [email, setEmail] = useState('');
  const [validationError, setValidationError] = useState<string | undefined>();
  const { requestReset, isLoading, error, isSuccess } = useForgotPassword();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!email) {
      setValidationError('Email is required.');
      return;
    }
    if (!validateEmail(email)) {
      setValidationError('Enter a valid email address.');
      return;
    }
    setValidationError(undefined);
    requestReset(email);
  }

  if (isSuccess) {
    return (
      <div className="flex flex-col items-center gap-4 text-center">
        <span className="flex h-12 w-12 items-center justify-center rounded-full bg-sentiment-positive/15 text-sentiment-positive">
          <MailCheck className="h-6 w-6" />
        </span>
        <div>
          <p className="text-base font-semibold text-text-primary">Check your inbox</p>
          <p className="mt-1.5 max-w-xs text-sm text-text-secondary">
            If <span className="text-text-primary">{email}</span> is registered, a password reset
            link has been sent. It expires in 1 hour.
          </p>
        </div>
        <Link href="/login" className="mt-2 text-sm font-medium text-brand-400 hover:text-brand-500">
          <ArrowLeft className="mr-1 inline h-3.5 w-3.5" />
          Back to log in
        </Link>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-5">
      {error && (
        <div
          role="alert"
          className="flex items-center gap-2 rounded-sm border border-feedback-danger/30 bg-feedback-danger/10 px-3.5 py-2.5 text-sm text-feedback-danger"
        >
          <AlertCircle className="h-4 w-4 shrink-0" />
          {error}
        </div>
      )}

      <FormField label="Email" htmlFor="forgot-password-email" error={validationError}>
        <Input
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          state={validationError ? 'error' : 'default'}
          autoComplete="email"
          autoFocus
        />
      </FormField>

      <Button type="submit" variant="primary" size="lg" isLoading={isLoading} className="w-full">
        Send Reset Link
      </Button>

      <Link
        href="/login"
        className="flex items-center justify-center gap-1.5 text-sm text-text-secondary hover:text-text-primary"
      >
        <ArrowLeft className="h-3.5 w-3.5" />
        Back to log in
      </Link>
    </form>
  );
}
