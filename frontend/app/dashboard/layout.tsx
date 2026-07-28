'use client';

import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import { AlertCircle, Loader2 } from 'lucide-react';
import { AuthProvider, useAuth } from '@/features/auth/auth-provider';
import { Button } from '@/components/ui/button';
import { DashboardSidebar } from '@/components/dashboard/dashboard-sidebar';
import { DashboardTopbar } from '@/components/dashboard/dashboard-topbar';
import { MobileSidebar } from '@/components/dashboard/mobile-sidebar';
import { ToastProvider } from '@/components/ui/toast-provider';
import { useLanguage } from '@/lib/i18n/language-provider';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <ToastProvider>
        <DashboardShell>{children}</DashboardShell>
      </ToastProvider>
    </AuthProvider>
  );
}

function DashboardShell({ children }: { children: React.ReactNode }) {
  const { user, isLoading, error, retry } = useAuth();
  const [isMobileNavOpen, setIsMobileNavOpen] = useState(false);
  const { t } = useLanguage();

  if (error) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-3 bg-background-base px-4">
        <AlertCircle className="h-6 w-6 text-feedback-danger" />
        <p className="max-w-sm text-center text-sm text-text-secondary">{error}</p>
        <Button variant="secondary" size="sm" onClick={retry}>
          Try again
        </Button>
      </div>
    );
  }

  if (isLoading || !user) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-3 bg-background-base">
        <Loader2 className="h-6 w-6 animate-spin text-brand-400" />
        <p className="text-sm text-text-secondary">{t('dashboardShell.loadingSession')}</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-background-base">
      <DashboardSidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        <DashboardTopbar user={user} onOpenMobileNav={() => setIsMobileNavOpen(true)} />
        <main className="flex-1 p-4 sm:p-6 lg:p-8">{children}</main>
      </div>

      <AnimatePresence>
        {isMobileNavOpen && <MobileSidebar onClose={() => setIsMobileNavOpen(false)} />}
      </AnimatePresence>
    </div>
  );
}
