'use client';

import { useEffect, useRef, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { ChevronDown, LogOut, Settings } from 'lucide-react';
import Link from 'next/link';
import { useLogout } from '@/features/auth/hooks/use-logout';
import { useLanguage } from '@/lib/i18n/language-provider';
import type { User } from '@/features/auth/types';

function getInitials(fullName: string): string {
  const parts = fullName.trim().split(/\s+/);
  const initials = parts.slice(0, 2).map((p) => p[0]?.toUpperCase() ?? '');
  return initials.join('') || '?';
}

export function UserMenu({ user }: { user: User }) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const { logout, isLoading } = useLogout();
  const { t } = useLanguage();

  useEffect(() => {
    if (!isOpen) return;

    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }

    function handleEscape(e: KeyboardEvent) {
      if (e.key === 'Escape') setIsOpen(false);
    }

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen]);

  return (
    <div ref={menuRef} className="relative">
      <button
        onClick={() => setIsOpen((v) => !v)}
        aria-expanded={isOpen}
        aria-haspopup="menu"
        className="flex items-center gap-2 rounded-md p-1.5 transition-colors hover:bg-background-elevated"
      >
        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-500/15 text-sm font-semibold text-brand-400">
          {getInitials(user.full_name)}
        </span>
        <span className="hidden text-sm font-medium text-text-primary sm:block">
          {user.full_name}
        </span>
        <ChevronDown
          className={`h-4 w-4 text-text-muted transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
        />
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            role="menu"
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 top-full z-50 mt-2 w-56 overflow-hidden rounded-lg border border-border-default bg-background-elevated shadow-lg"
          >
            <div className="border-b border-border-subtle px-4 py-3">
              <p className="truncate text-sm font-medium text-text-primary">{user.full_name}</p>
              <p className="truncate text-xs text-text-muted">{user.email}</p>
            </div>
            <div className="p-1.5">
              <Link
                href="/dashboard/settings"
                role="menuitem"
                onClick={() => setIsOpen(false)}
                className="flex items-center gap-2.5 rounded-sm px-3 py-2 text-sm text-text-secondary transition-colors hover:bg-background-surface hover:text-text-primary"
              >
                <Settings className="h-4 w-4" />
                {t('common.settings')}
              </Link>
              <button
                role="menuitem"
                onClick={() => logout()}
                disabled={isLoading}
                className="flex w-full items-center gap-2.5 rounded-sm px-3 py-2 text-left text-sm text-feedback-danger transition-colors hover:bg-feedback-danger/10 disabled:opacity-50"
              >
                <LogOut className="h-4 w-4" />
                {isLoading ? t('common.loggingOut') : t('common.logOut')}
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
