'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { AlertCircle } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { FormField } from '@/components/forms/form-field';
import { PasswordInput } from '@/components/forms/password-input';
import { Checkbox } from '@/components/forms/checkbox';
import { GoogleSignInButton } from '@/components/auth/google-sign-in-button';
import { useLogin } from '@/features/auth/hooks/use-login';

interface FormErrors {
  email?: string;
  password?: string;
}

function validateEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

const GOOGLE_ERROR_MESSAGES: Record<string, string> = {
  google_not_configured: 'Google Sign-In is not available right now. Please log in with your email instead.',
  google_auth_failed: 'Google sign-in failed. Please try again.',
  account_disabled: 'This account has been disabled.',
};

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const { login, isLoading, error } = useLogin();
  const searchParams = useSearchParams();
  const googleErrorCode = searchParams.get('error');
  const googleError = googleErrorCode
    ? GOOGLE_ERROR_MESSAGES[googleErrorCode] ?? GOOGLE_ERROR_MESSAGES.google_auth_failed
    : null;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const nextErrors: FormErrors = {};
    if (!email) nextErrors.email = 'Email is required.';
    else if (!validateEmail(email)) nextErrors.email = 'Enter a valid email address.';
    if (!password) nextErrors.password = 'Password is required.';

    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    login({ email, password });
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="flex flex-col gap-5">
      {(error || googleError) && (
        <div
          role="alert"
          className="flex items-center gap-2 rounded-sm border border-feedback-danger/30 bg-feedback-danger/10 px-3.5 py-2.5 text-sm text-feedback-danger"
        >
          <AlertCircle className="h-4 w-4 shrink-0" />
          {error || googleError}
        </div>
      )}

      <GoogleSignInButton />

      <div className="flex items-center gap-3">
        <div className="h-px flex-1 bg-border-subtle" />
        <span className="text-xs uppercase tracking-wide text-text-muted">or</span>
        <div className="h-px flex-1 bg-border-subtle" />
      </div>

      <FormField label="Email" htmlFor="login-email" error={errors.email}>
        <Input
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          state={errors.email ? 'error' : 'default'}
          autoComplete="email"
        />
      </FormField>

      <FormField label="Password" htmlFor="login-password" error={errors.password}>
        <PasswordInput
          placeholder="Enter your password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          state={errors.password ? 'error' : 'default'}
          autoComplete="current-password"
        />
      </FormField>

      <div className="flex items-center justify-between">
        <Checkbox
          id="remember-me"
          label="Remember me"
          checked={rememberMe}
          onChange={(e) => setRememberMe(e.target.checked)}
        />
        <Link href="/forgot-password" className="text-sm text-brand-400 hover:text-brand-500">
          Forgot password?
        </Link>
      </div>

      <Button type="submit" variant="primary" size="lg" isLoading={isLoading} className="w-full">
        Log In
      </Button>

      <p className="text-center text-sm text-text-secondary">
        Don&apos;t have an account?{' '}
        <Link href="/register" className="font-medium text-brand-400 hover:text-brand-500">
          Sign up
        </Link>
      </p>
    </form>
  );
}