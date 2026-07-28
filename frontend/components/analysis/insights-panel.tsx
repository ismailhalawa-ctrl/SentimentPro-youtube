'use client';

import { Sparkles } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface InsightsPanelProps {
  insights: string[];
  source?: 'ai' | 'rule_based';
}

export function InsightsPanel({ insights, source = 'rule_based' }: InsightsPanelProps) {
  if (insights.length === 0) {
    return (
      <Card variant="glass" className="p-5">
        <CardContent className="p-0 text-sm text-text-muted">
          No insights available for this analysis yet.
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {source === 'ai' ? (
        <Badge status="info" className="w-fit">
          <Sparkles className="h-3 w-3" />
          AI-Powered Insights
        </Badge>
      ) : (
        <Badge status="info" className="w-fit bg-background-elevated text-text-muted">
          Rule-Based Highlights
        </Badge>
      )}
      {insights.map((insight, i) => (
        <Card key={i} variant="glass" className="border-l-4 border-l-brand-500 p-4">
          <CardContent className="p-0 text-sm text-text-primary">{insight}</CardContent>
        </Card>
      ))}
    </div>
  );
}
