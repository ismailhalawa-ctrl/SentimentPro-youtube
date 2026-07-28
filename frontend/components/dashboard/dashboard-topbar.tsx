'use client';

import { Menu } from 'lucide-react';
import { UserMenu } from './user-menu';
import { LanguageToggle } from './language-toggle';
import type { User } from '@/features/auth/types';

interface DashboardTopbarProps {
  user: User;
  onOpenMobileNav: () => void;
}

export function DashboardTopbar({ user, onOpenMobileNav }: DashboardTopbarProps) {
  return (
    <header className="relative z-30 flex h-16 items-center justify-between border-b border-border-subtle bg-background-surface/60 px-4 backdrop-blur-md sm:px-6">
      <button
        onClick={onOpenMobileNav}
        aria-label="Open navigation"
        className="flex items-center justify-center rounded-md p-2 text-text-secondary hover:bg-background-elevated hover:text-text-primary lg:hidden"
      >
        <Menu className="h-5 w-5" />
      </button>

      <div className="hidden lg:block" />

      <div className="flex items-center gap-2">
        <LanguageToggle />
        <UserMenu user={user} />
      </div>
    </header>
  );
}
