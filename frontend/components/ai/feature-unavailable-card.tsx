import { Sparkles } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

interface FeatureUnavailableCardProps {
  reason?: string | null;
}

export function FeatureUnavailableCard({ reason }: FeatureUnavailableCardProps) {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex items-start gap-3 p-0">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
          <Sparkles className="h-4.5 w-4.5" />
        </span>
        <div className="flex flex-col gap-1">
          <p className="text-sm font-medium text-text-primary">This AI feature isn&apos;t enabled yet</p>
          <p className="text-sm text-text-secondary">
            {reason ?? 'It requires an AI provider API key to be configured on the server.'}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
