'use client';

import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { PasswordInput } from '@/components/forms/password-input';
import { FormField } from '@/components/forms/form-field';
import { useDeleteAccount } from '@/features/auth/hooks/use-delete-account';
import type { User } from '@/features/auth/types';

interface DeleteAccountModalProps {
  isOpen: boolean;
  user: User;
  onClose: () => void;
}

export function DeleteAccountModal({ isOpen, user, onClose }: DeleteAccountModalProps) {
  const [password, setPassword] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const { deleteAccount, isLoading, error, setError } = useDeleteAccount();

  const isGoogleAccount = Boolean(user.google_id);
  const canSubmit = isGoogleAccount
    ? confirmation.trim().toLowerCase() === user.email.toLowerCase()
    : password.length > 0;

  useEffect(() => {
    if (!isOpen) return;
    setPassword('');
    setConfirmation('');
    setError(null);
  }, [isOpen, setError]);

  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && !isLoading) onClose();
    };
    document.addEventListener('keydown', handleKeyDown);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [isOpen, isLoading, onClose]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!canSubmit) return;
    await deleteAccount(isGoogleAccount ? { confirmation } : { password });
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="fixed inset-0 z-[100] bg-background-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
          />
          <div
            className="fixed inset-0 z-[100] flex items-center justify-center p-4"
            onClick={() => !isLoading && onClose()}
          >
            <motion.div
              role="alertdialog"
              aria-modal="true"
              aria-labelledby="delete-account-title"
              initial={{ opacity: 0, scale: 0.95, y: 8 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 8 }}
              transition={{ duration: 0.15 }}
              onClick={(e) => e.stopPropagation()}
              className="w-full max-w-md rounded-lg border border-border-default bg-background-elevated p-5 shadow-lg"
            >
              <div className="flex items-start gap-3">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-feedback-danger/15 text-feedback-danger">
                  <AlertTriangle className="h-4 w-4" />
                </span>
                <div className="min-w-0 flex-1 pt-1">
                  <h2 id="delete-account-title" className="text-base font-semibold text-text-primary">
                    Delete your account
                  </h2>
                  <p className="mt-1.5 text-sm text-text-secondary">
                    This permanently deletes your account, every analysis job, and all associated data.
                    This cannot be undone.
                  </p>
                </div>
              </div>

              <form onSubmit={handleSubmit} className="mt-5 flex flex-col gap-4">
                {isGoogleAccount ? (
                  <FormField
                    label={`Type "${user.email}" to confirm`}
                    htmlFor="delete-confirmation"
                  >
                    <Input
                      type="text"
                      value={confirmation}
                      onChange={(e) => setConfirmation(e.target.value)}
                      placeholder={user.email}
                      autoComplete="off"
                    />
                  </FormField>
                ) : (
                  <FormField label="Confirm your password" htmlFor="delete-password">
                    <PasswordInput
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Your current password"
                      autoComplete="current-password"
                    />
                  </FormField>
                )}

                {error && (
                  <p role="alert" className="text-sm text-feedback-danger">
                    {error}
                  </p>
                )}

                <div className="mt-1 flex justify-end gap-2.5">
                  <Button type="button" variant="ghost" size="sm" onClick={onClose} disabled={isLoading}>
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    variant="destructive"
                    size="sm"
                    isLoading={isLoading}
                    disabled={!canSubmit}
                  >
                    Delete my account
                  </Button>
                </div>
              </form>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}
