import { Bot, LayoutDashboard, FilePlus2, History, FileText, Settings, type LucideIcon } from 'lucide-react';

export interface DashboardNavItem {
  label: string;
  labelKey: string;
  href: string;
  icon: LucideIcon;
}

export const DASHBOARD_NAV_ITEMS: DashboardNavItem[] = [
  { label: 'Dashboard', labelKey: 'nav.dashboard', href: '/dashboard', icon: LayoutDashboard },
  { label: 'New Analysis', labelKey: 'nav.newAnalysis', href: '/dashboard/new-analysis', icon: FilePlus2 },
  { label: 'Channel Assistant', labelKey: 'nav.audienceAssistant', href: '/dashboard/audience-assistant', icon: Bot },
  { label: 'History', labelKey: 'nav.history', href: '/dashboard/history', icon: History },
  { label: 'Reports', labelKey: 'nav.reports', href: '/dashboard/reports', icon: FileText },
  { label: 'Settings', labelKey: 'nav.settings', href: '/dashboard/settings', icon: Settings },
];
