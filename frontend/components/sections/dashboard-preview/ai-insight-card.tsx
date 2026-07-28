import { Sparkles } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

export function AiInsightCard() {
  return (
    <Card variant="glass" className="p-4">
      <CardContent className="flex gap-3 p-0">
        <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-gradient-brand">
          <Sparkles className="h-3.5 w-3.5 text-text-primary" />
        </span>
        <p className="text-sm text-text-secondary">
          Viewers respond strongly to your tutorial pacing. Comments mentioning
          &ldquo;clear explanation&rdquo; rose 18% this week.
        </p>
      </CardContent>
    </Card>
  );
}