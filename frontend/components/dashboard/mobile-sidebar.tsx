'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Sparkles, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { DASHBOARD_NAV_ITEMS } from '@/config/dashboard-nav-items';
import { useLanguage } from '@/lib/i18n/language-provider';

export function MobileSidebar({ onClose }: { onClose: () => void }) {
  const pathname = usePathname();
  const { t } = useLanguage();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', handleKeyDown);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [onClose]);

  return (
    <>
      <motion.div
        className="fixed inset-0 z-40 bg-background-overlay lg:hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.2 }}
        onClick={onClose}
      />
      <motion.div
        role="dialog"
        aria-modal="true"
        aria-label="Dashboard navigation"
        initial={{ x: '-100%' }}
        animate={{ x: 0 }}
        exit={{ x: '-100%' }}
        transition={{ type: 'spring', damping: 28, stiffness: 300 }}
        className="fixed left-0 top-0 z-50 flex h-full w-64 flex-col border-r border-border-default bg-background-elevated lg:hidden"
      >
        <div className="flex h-16 items-center justify-between border-b border-border-subtle px-4">
          <Link
            href="/dashboard"
            onClick={(e) => {
              if (pathname === '/dashboard') {
                e.preventDefault();
                window.scrollTo({ top: 0, behavior: 'smooth' });
              }
              onClose();
            }}
            className="flex items-center gap-2"
          >
            <span className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-brand">
              <Sparkles className="h-4 w-4 text-text-primary" />
            </span>
            <span className="text-base font-semibold text-text-primary">
              Sentiment<span className="text-brand-400">PRO</span>
            </span>
          </Link>
          <button
            onClick={onClose}
            aria-label="Close navigation"
            className="rounded-md p-1.5 text-text-secondary hover:bg-background-surface hover:text-text-primary"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="flex flex-1 flex-col gap-1 p-4">
          {DASHBOARD_NAV_ITEMS.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                className={cn(
                  'flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors duration-150',
                  isActive
                    ? 'bg-brand-500/15 text-brand-400'
                    : 'text-text-secondary hover:bg-background-surface hover:text-text-primary'
                )}
              >
                <Icon className="h-4 w-4" />
                {t(item.labelKey)}
              </Link>
            );
          })}
        </nav>
      </motion.div>
    </>
  );
}
