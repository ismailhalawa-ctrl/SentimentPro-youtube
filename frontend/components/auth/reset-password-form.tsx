'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';
import { AlertCircle, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { FormField } from '@/components/forms/form-field';
import { PasswordInput } from '@/components/forms/password-input';
import { PasswordStrength } from '@/components/forms/password-strength';
import { useResetPassword } from '@/features/auth/hooks/use-reset-password';

interface FormErrors {
  password?: string;
  confirmPassword?: string;
}

export function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const token = searchParams.get('token');

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<FormErrors>({});
  const { resetPassword, isLoading, error, isSuccess } = useResetPassword();

  if (!token) {
    return (
      <div className="flex flex-col items-center gap-3 text-center">
        <span className="flex h-12 w-12 items-center justify-center rounded-full bg-feedback-danger/15 text-feedback-danger">
          <AlertCircle className="h-6 w-6" />
        </span>
        <p className="text-base font-semibold text-text-primary">Missing reset token</p>
        <p className="max-w-xs text-sm text-text-secondary">
          This link is missing its reset token. Request a new one from the forgot-password page.
        </p>
        <Link href="/forgot-password" className="mt-2 text-sm font-medium text-brand-400 hover:text-brand-500">
          Request a new link
        </Link>
      </div>
    );
  }

  if (isSuccess) {
    return (
      <div className="flex flex-col items-center gap-3 text-center">
        <span className="flex h-12 w-12 items-center justify-center rounded-full bg-sentiment-positive/15 text-sentiment-positive">
          <CheckCircle2 className="h-6 w-6" />
        </span>
        <p className="text-base font-semibold text-text-primary">Password reset</p>
        <p className="max-w-xs text-sm text-text-secondary">
          Your password has been updated. You can log in with your new password now.
        </p>
        <Link href="/login" className="mt-2 w-full">
          <Button variant="primary" size="lg" className="w-full">
            Go to Log In
          </Button>
        </Link>
      </div>
    );
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    const nextErrors: FormErrors = {};
    if (!password) nextErrors.password = 'Password is required.';
    else if (password.length < 8) nextErrors.password = 'Password must be at least 8 characters.';
    if (confirmPassword !== password) nextErrors.confirmPassword = 'Passwords do not match.';

    setErrors(nextErrors);
    if (Object.keys(nextErrors).length > 0) return;

    resetPassword(token as string, password);
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

      <FormField label="New Password" htmlFor="reset-password-new" error={errors.password}>
        <div className="flex flex-col gap-2.5">
          <PasswordInput
            placeholder="Create a new password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            state={errors.password ? 'error' : 'default'}
            autoComplete="new-password"
            autoFocus
          />
          <PasswordStrength password={password} />
        </div>
      </FormField>

      <FormField
        label="Confirm New Password"
        htmlFor="reset-password-confirm"
        error={errors.confirmPassword}
      >
        <PasswordInput
          placeholder="Re-enter your new password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          state={errors.confirmPassword ? 'error' : 'default'}
          autoComplete="new-password"
        />
      </FormField>

      <Button type="submit" variant="primary" size="lg" isLoading={isLoading} className="w-full">
        Reset Password
      </Button>
    </form>
  );
}
