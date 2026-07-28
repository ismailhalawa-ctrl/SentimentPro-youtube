'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';
import { DASHBOARD_NAV_ITEMS } from '@/config/dashboard-nav-items';
import { useLanguage } from '@/lib/i18n/language-provider';

export function DashboardSidebar() {
  const pathname = usePathname();
  const { t } = useLanguage();

  const handleLogoClick = (e: React.MouseEvent) => {
    if (pathname === '/dashboard') {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <aside className="hidden w-64 shrink-0 flex-col border-r border-border-subtle bg-background-surface/40 backdrop-blur-md lg:flex">
      <Link
        href="/dashboard"
        onClick={handleLogoClick}
        className="flex h-16 items-center gap-2 border-b border-border-subtle px-6"
      >
        <span className="flex h-8 w-8 items-center justify-center rounded-md bg-gradient-brand">
          <Sparkles className="h-4 w-4 text-text-primary" />
        </span>
        <span className="text-base font-semibold text-text-primary">
          Sentiment<span className="text-brand-400">PRO</span>
        </span>
      </Link>

      <nav className="flex flex-1 flex-col gap-1 p-4">
        {DASHBOARD_NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                'flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors duration-150',
                isActive
                  ? 'bg-brand-500/15 text-brand-400'
                  : 'text-text-secondary hover:bg-background-elevated hover:text-text-primary'
              )}
            >
              <Icon className="h-4 w-4" />
              {t(item.labelKey)}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}