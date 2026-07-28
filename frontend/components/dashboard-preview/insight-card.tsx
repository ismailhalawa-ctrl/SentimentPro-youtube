import { Sparkles, MessageCircle, TrendingUp } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

const INSIGHTS = [
  {
    icon: MessageCircle,
    title: 'Audience Reaction',
    body: 'Viewers respond positively to clear, step-by-step explanations.',
  },
  {
    icon: TrendingUp,
    title: 'Main Discussion Topics',
    body: 'Setup process, error handling, and deployment come up most often.',
  },
  {
    icon: Sparkles,
    title: 'Suggested Improvement',
    body: 'Consider a shorter recap at the start of longer tutorials.',
  },
];

export function InsightCard() {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <p className="text-sm font-medium text-text-muted">AI Insights</p>
        {INSIGHTS.map((insight) => {
          const Icon = insight.icon;
          return (
            <div key={insight.title} className="flex gap-3">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                <Icon className="h-4 w-4" />
              </span>
              <div>
                <p className="text-sm font-medium text-text-primary">{insight.title}</p>
                <p className="text-sm text-text-secondary">{insight.body}</p>
              </div>
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}