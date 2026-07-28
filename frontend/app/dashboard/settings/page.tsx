'use client';

import { useEffect, useState } from 'react';
import { CheckCircle2, Clock, Mail, MessageCircle, ShieldAlert, Sparkles, User as UserIcon } from 'lucide-react';
import { useAuth } from '@/features/auth/auth-provider';
import { useUpdateProfile } from '@/features/auth/hooks/use-update-profile';
import { useDashboardPreferences } from '@/features/settings/use-dashboard-preferences';
import { getNameChangeDaysRemaining } from '@/features/auth/name-change-cooldown';
import {
  createCheckoutSession,
  createPortalSession,
  getSubscriptionStatus,
  type SubscriptionStatus,
} from '@/features/billing/api/billing-api';
import { ApiError } from '@/lib/api-client';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { FormField } from '@/components/forms/form-field';
import { Checkbox } from '@/components/forms/checkbox';
import { ContactForm } from '@/components/contact/contact-form';
import { DeleteAccountModal } from '@/components/auth/delete-account-modal';

export default function SettingsPage() {
  const { user } = useAuth();
  const { updateProfile, isLoading, error, isSuccess } = useUpdateProfile();
  const { preferences, setPreferences } = useDashboardPreferences();

  const [fullName, setFullName] = useState(user?.full_name ?? '');
  const [subscription, setSubscription] = useState<SubscriptionStatus | null>(null);
  const [billingLoading, setBillingLoading] = useState(false);
  const [billingError, setBillingError] = useState<string | null>(null);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);

  useEffect(() => {
    getSubscriptionStatus()
      .then(setSubscription)
      .catch(() => setSubscription(null));
  }, []);

  async function handleUpgrade() {
    setBillingLoading(true);
    setBillingError(null);
    try {
      const { checkout_url } = await createCheckoutSession();
      window.location.href = checkout_url;
    } catch (err) {
      setBillingError(
        err instanceof ApiError ? err.message : 'Unable to start checkout. Please try again.'
      );
      setBillingLoading(false);
    }
  }

  async function handleManageBilling() {
    setBillingLoading(true);
    setBillingError(null);
    try {
      const { portal_url } = await createPortalSession();
      window.location.href = portal_url;
    } catch (err) {
      setBillingError(
        err instanceof ApiError ? err.message : 'Unable to open the billing portal. Please try again.'
      );
      setBillingLoading(false);
    }
  }

  useEffect(() => {
    if (user) setFullName(user.full_name);
  }, [user]);

  if (!user) return null;

  const daysRemaining = getNameChangeDaysRemaining(user.last_name_change);
  const isLocked = daysRemaining > 0;
  const nameChanged = fullName.trim() !== user.full_name && fullName.trim().length > 0;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!nameChanged || isLocked) return;
    updateProfile(fullName.trim());
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-text-primary">Settings</h1>
        <p className="mt-1 text-sm text-text-secondary">Manage your account and dashboard preferences.</p>
      </div>

      <Card variant="glass" className="p-6">
        <CardContent className="flex flex-col gap-5 p-0">
          <p className="text-sm font-medium text-text-muted">Account</p>

          {isLocked && (
            <div className="flex items-start gap-2.5 rounded-md border border-feedback-warning/30 bg-feedback-warning/10 px-3.5 py-3 text-sm text-feedback-warning">
              <Clock className="mt-0.5 h-4 w-4 shrink-0" />
              <span>
                You can change your name again in {daysRemaining} day{daysRemaining !== 1 ? 's' : ''}.
                Names can only be changed once every 60 days.
              </span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="flex flex-col gap-4">
            <FormField label="Full Name" htmlFor="settings-full-name">
              <Input
                type="text"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                disabled={isLocked}
                className="max-w-sm"
              />
            </FormField>

            <div className="flex flex-col gap-1.5">
              <p className="flex items-center gap-1.5 text-sm font-medium text-text-primary">
                <Mail className="h-3.5 w-3.5 text-text-muted" />
                Email
              </p>
              <p className="text-sm text-text-secondary">{user.email}</p>
              <p className="text-xs text-text-muted">Email cannot be changed.</p>
            </div>

            <div className="flex items-center gap-3 pt-1">
              <Button
                type="submit"
                variant="primary"
                size="md"
                isLoading={isLoading}
                disabled={!nameChanged || isLocked}
              >
                {!isLoading && <UserIcon className="h-4 w-4" />} Save Changes
              </Button>
              {isSuccess && (
                <span className="flex items-center gap-1.5 text-sm text-sentiment-positive">
                  <CheckCircle2 className="h-4 w-4" /> Saved
                </span>
              )}
              {error && <span className="text-sm text-feedback-danger">{error}</span>}
            </div>
          </form>
        </CardContent>
      </Card>

      <Card variant="glass" className="p-6">
        <CardContent className="flex flex-col gap-4 p-0">
          <p className="text-sm font-medium text-text-muted">Subscription</p>

          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-2.5">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                <Sparkles className="h-4.5 w-4.5" />
              </span>
              <div>
                <p className="text-sm font-medium capitalize text-text-primary">
                  {subscription?.tier ?? 'free'} plan
                </p>
                <p className="text-xs text-text-muted">
                  {subscription?.tier === 'pro'
                    ? 'Thanks for being a Pro subscriber.'
                    : 'Upgrade for higher AI usage limits.'}
                </p>
              </div>
            </div>

            {subscription?.tier === 'pro' ? (
              <Button variant="secondary" size="sm" isLoading={billingLoading} onClick={handleManageBilling}>
                Manage Billing
              </Button>
            ) : (
              <Button variant="primary" size="sm" isLoading={billingLoading} onClick={handleUpgrade}>
                Upgrade to Pro
              </Button>
            )}
          </div>

          {billingError && <p className="text-sm text-feedback-danger">{billingError}</p>}
        </CardContent>
      </Card>

      <Card variant="glass" className="p-6">
        <CardContent className="flex flex-col gap-4 p-0">
          <p className="text-sm font-medium text-text-muted">Dashboard Preferences</p>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="flex flex-col gap-1.5">
              <label htmlFor="pref-language" className="text-sm font-medium text-text-primary">
                Default Analysis Language
              </label>
              <select
                id="pref-language"
                value={preferences.defaultLanguage}
                onChange={(e) =>
                  setPreferences({
                    ...preferences,
                    defaultLanguage: e.target.value as 'auto' | 'ar' | 'en',
                  })
                }
                className="w-full rounded-sm border border-border-default bg-background-surface px-3.5 py-2.5 text-sm text-text-primary transition-colors duration-150 focus:border-brand-400"
              >
                <option value="auto">Auto Detect</option>
                <option value="ar">Arabic</option>
                <option value="en">English</option>
              </select>
            </div>

            <div className="flex flex-col gap-1.5">
              <label htmlFor="pref-max-comments" className="text-sm font-medium text-text-primary">
                Default Max Comments
              </label>
              <Input
                id="pref-max-comments"
                type="number"
                min={50}
                max={1_000_000}
                step={50}
                value={preferences.defaultMaxComments}
                onChange={(e) =>
                  setPreferences({ ...preferences, defaultMaxComments: Number(e.target.value) })
                }
              />
            </div>
          </div>

          <div className="border-t border-border-subtle pt-4">
            <Checkbox
              id="pref-compact-lists"
              label="Use a more compact layout for the History list"
              checked={preferences.compactLists}
              onChange={(e) => setPreferences({ ...preferences, compactLists: e.target.checked })}
            />
          </div>

          <p className="text-xs text-text-muted">
            Saved on this device — applied automatically next time you start a new analysis.
          </p>
        </CardContent>
      </Card>

      <Card variant="glass" className="p-6">
        <CardContent className="flex flex-col gap-4 p-0">
          <div className="flex items-center gap-2">
            <MessageCircle className="h-4 w-4 text-text-muted" />
            <p className="text-sm font-medium text-text-muted">Contact Us</p>
          </div>
          <p className="text-sm text-text-secondary">
            Questions, feedback, or something not working right? Send us a message directly.
          </p>
          <ContactForm initialName={user.full_name} initialEmail={user.email} hideCard />
        </CardContent>
      </Card>

      <Card variant="glass" className="border-feedback-danger/30 p-6">
        <CardContent className="flex flex-col gap-4 p-0">
          <div className="flex items-center gap-2">
            <ShieldAlert className="h-4 w-4 text-feedback-danger" />
            <p className="text-sm font-medium text-feedback-danger">Danger Zone</p>
          </div>
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-sm font-medium text-text-primary">Delete account</p>
              <p className="mt-1 text-sm text-text-secondary">
                Permanently deletes your account, every analysis job, and all associated data. This
                cannot be undone.
              </p>
            </div>
            <Button variant="destructive" size="sm" onClick={() => setIsDeleteModalOpen(true)}>
              Delete Account
            </Button>
          </div>
        </CardContent>
      </Card>

      <DeleteAccountModal isOpen={isDeleteModalOpen} user={user} onClose={() => setIsDeleteModalOpen(false)} />
    </div>
  );
}
