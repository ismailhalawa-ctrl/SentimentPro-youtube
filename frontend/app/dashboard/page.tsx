'use client';

import { useAuth } from '@/features/auth/auth-provider';
import { WelcomeBanner } from '@/components/dashboard/welcome-banner';
import { QuickActions } from '@/components/dashboard/quick-actions';
import { StatisticsOverview } from '@/components/dashboard/statistics-overview';
import { RecentAnalyses } from '@/components/dashboard/recent-analyses';
import { ActivityTimeline } from '@/components/dashboard/activity-timeline';

export default function DashboardPage() {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <div className="flex flex-col gap-8">
      <WelcomeBanner user={user} />
      <QuickActions />
      <StatisticsOverview />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <RecentAnalyses />
        </div>
        <ActivityTimeline />
      </div>
    </div>
  );
}
