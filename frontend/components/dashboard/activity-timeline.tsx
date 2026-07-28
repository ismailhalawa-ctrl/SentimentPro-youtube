'use client';

import { UserPlus, type LucideIcon } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

interface ActivityEntry {
  id: string;
  icon: LucideIcon;
  description: string;
  timestamp: string;
}

const MOCK_ACTIVITY: ActivityEntry[] = [
  {
    id: '1',
    icon: UserPlus,
    description: 'Account created successfully. Welcome to SentimentPRO!',
    timestamp: 'Just now',
  },
];

export function ActivityTimeline() {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <p className="text-sm font-medium text-text-muted">Recent Activity</p>
        <div className="flex flex-col gap-4">
          {MOCK_ACTIVITY.map((activity) => {
            const Icon = activity.icon;
            return (
              <div key={activity.id} className="flex items-start gap-3">
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                  <Icon className="h-3.5 w-3.5" />
                </span>
                <div>
                  <p className="text-sm text-text-secondary">{activity.description}</p>
                  <p className="text-xs text-text-muted">{activity.timestamp}</p>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}