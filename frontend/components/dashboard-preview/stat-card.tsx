import { LucideIcon } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export interface Stat {
  label: string;
  value: string;
  icon: LucideIcon;
  accentClass: string;
}

export function StatCard({ stat }: { stat: Stat }) {
  const Icon = stat.icon;
  return (
    <Card variant="glass" className="p-4">
      <CardContent className="flex items-center gap-3 p-0">
        <span className={`flex h-9 w-9 items-center justify-center rounded-md bg-background-surface ${stat.accentClass}`}>
          <Icon className="h-4 w-4" />
        </span>
        <div>
          <p className="text-xs text-text-muted">{stat.label}</p>
          <p className="text-xl font-semibold text-text-primary">{stat.value}</p>
        </div>
      </CardContent>
    </Card>
  );
}