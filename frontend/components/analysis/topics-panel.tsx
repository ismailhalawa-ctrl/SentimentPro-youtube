'use client';

import { Card, CardContent } from '@/components/ui/card';

interface TopicsPanelProps {
  positive: Record<string, number>;
  negative: Record<string, number>;
}

function TopicList({ label, topics, color }: { label: string; topics: Record<string, number>; color: string }) {
  const entries = Object.entries(topics);

  return (
    <Card variant="glass" className="p-4">
      <CardContent className="p-0">
        <p className="mb-3 text-sm font-medium text-text-muted">{label}</p>
        {entries.length === 0 ? (
          <p className="py-6 text-center text-sm text-text-muted">No clear topics identified.</p>
        ) : (
          <div className="flex flex-col divide-y divide-border-subtle">
            {entries.map(([topic, count]) => (
              <div key={topic} className="flex items-center justify-between py-2 text-sm">
                <span className="text-text-primary">{topic}</span>
                <span className="rounded-full px-2 py-0.5 text-xs font-medium" style={{ backgroundColor: `${color}26`, color }}>
                  {count} mentions
                </span>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function TopicsPanel({ positive, negative }: TopicsPanelProps) {
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
      <TopicList label="Positive Topics" topics={positive} color="#22C55E" />
      <TopicList label="Negative Topics" topics={negative} color="#EF4444" />
    </div>
  );
}
