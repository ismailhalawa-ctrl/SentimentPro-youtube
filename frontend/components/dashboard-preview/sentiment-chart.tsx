'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { Card, CardContent } from '@/components/ui/card';
import { colors } from '@/styles/design-tokens';

const DATA = [
  { name: 'Positive', value: 62, color: colors.sentiment.positive },
  { name: 'Neutral', value: 24, color: colors.sentiment.neutral },
  { name: 'Negative', value: 14, color: colors.sentiment.negative },
];

export function SentimentChart() {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="p-0">
        <p className="mb-4 text-sm font-medium text-text-muted">Sentiment Distribution</p>
        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={DATA}
                dataKey="value"
                nameKey="name"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={3}
                stroke="none"
              >
                {DATA.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: colors.background.elevated,
                  border: `1px solid ${colors.border.default}`,
                  borderRadius: '0.5rem',
                  color: colors.text.primary,
                  fontSize: '0.875rem',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-2 flex justify-center gap-4">
          {DATA.map((entry) => (
            <div key={entry.name} className="flex items-center gap-1.5 text-xs text-text-secondary">
              <span
                className="h-2 w-2 rounded-full"
                style={{ backgroundColor: entry.color }}
              />
              {entry.name}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}