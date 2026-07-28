'use client';

import { useState } from 'react';
import Link from 'next/link';
import { AlertCircle } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { FormField } from '@/components/forms/form-field';
import { PasswordInput } from '@/components/forms/password-input';
import { PasswordStrength } from '@/components/forms/password-strength';
import { Checkbox } from '@/components/forms/checkbox';
import { GoogleSignInButton } from '@/components/auth/google-sign-in-button';
import { useRegister } from '../../features/auth/hooks/use-register';

interface FormErrors {
  fullName?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
  acceptTerms?: string;
}

function validateEmail(email: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function RegisterForm() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [acceptTerms, setAcceptTerms] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({});
  const { register, isLoading, error } = useRegister();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const nextErrors: FormErrors = {};
    if (!fullName.trim()) nextErrors.fullName = 'Full name is required.';
    if (!email) nextErrors.email = 'Email is required.';
    else if (!validateEmail(email)) nextErrors.email = 'Enter a valid email address.';
    if (!password) nextErrors.password = 'Password is required.';
    else if (password.length < 8) nextErrors.password = 'Password must be at least 8 characters.';
    if (confirmPassword !== password) nextErrors.confirmPassword = 'Passwords do not match.';
    if (!acceptTerms) nextErrors.acceptTerms = 'You must accept the terms to continue.';

    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    register({ full_name: fullName.trim(), email, password });
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

      <GoogleSignInButton />

      <div className="flex items-center gap-3">
        <div className="h-px flex-1 bg-border-subtle" />
        <span className="text-xs uppercase tracking-wide text-text-muted">or</span>
        <div className="h-px flex-1 bg-border-subtle" />
      </div>

      <FormField label="Full Name" htmlFor="register-name" error={errors.fullName}>
        <Input
          type="text"
          placeholder="Jane Doe"
          value={fullName}
          onChange={(e) => setFullName(e.target.value)}
          state={errors.fullName ? 'error' : 'default'}
          autoComplete="name"
        />
      </FormField>

      <FormField label="Email" htmlFor="register-email" error={errors.email}>
        <Input
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          state={errors.email ? 'error' : 'default'}
          autoComplete="email"
        />
      </FormField>

      <div className="flex flex-col gap-2.5">
        <FormField label="Password" htmlFor="register-password" error={errors.password}>
          <PasswordInput
            placeholder="Create a password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            state={errors.password ? 'error' : 'default'}
            autoComplete="new-password"
          />
        </FormField>
        <PasswordStrength password={password} />
      </div>

      <FormField
        label="Confirm Password"
        htmlFor="register-confirm-password"
        error={errors.confirmPassword}
      >
        <PasswordInput
          placeholder="Re-enter your password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          state={errors.confirmPassword ? 'error' : 'default'}
          autoComplete="new-password"
        />
      </FormField>

      <div className="flex flex-col gap-1.5">
        <Checkbox
          id="accept-terms"
          label={
            <>
              I agree to the{' '}
              <Link href="/terms" className="text-brand-400 hover:text-brand-500">
                Terms of Service
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="text-brand-400 hover:text-brand-500">
                Privacy Policy
              </Link>
              .
            </>
          }
          checked={acceptTerms}
          onChange={(e) => setAcceptTerms(e.target.checked)}
        />
        {errors.acceptTerms && (
          <p role="alert" className="text-sm text-feedback-danger">
            {errors.acceptTerms}
          </p>
        )}
      </div>

      <Button type="submit" variant="primary" size="lg" isLoading={isLoading} className="w-full">
        Create Account
      </Button>

      <p className="text-center text-sm text-text-secondary">
        Already have an account?{' '}
        <Link href="/login" className="font-medium text-brand-400 hover:text-brand-500">
          Log in
        </Link>
      </p>
    </form>
  );
}