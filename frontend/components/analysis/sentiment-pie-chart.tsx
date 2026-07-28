'use client';

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';
import { Card, CardContent } from '@/components/ui/card';
import { colors } from '@/styles/design-tokens';
import { getSentimentBreakdown, getSentimentTotal } from '@/features/analysis/sentiment-utils';
import type { SentimentSummary } from '@/features/analysis/types';

interface SentimentPieChartProps {
  summary: SentimentSummary;
}

export function SentimentPieChart({ summary }: SentimentPieChartProps) {
  const slices = getSentimentBreakdown(summary);
  const total = getSentimentTotal(summary);

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="p-0">
        <p className="mb-4 text-sm font-medium text-text-muted">Sentiment Distribution</p>
        <div className="relative h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={slices}
                dataKey="value"
                nameKey="label"
                innerRadius={60}
                outerRadius={90}
                paddingAngle={slices.filter((s) => s.value > 0).length > 1 ? 3 : 0}
                stroke="none"
              >
                {slices.map((slice) => (
                  <Cell key={slice.key} fill={slice.color} />
                ))}
              </Pie>
              <Tooltip
                formatter={(value, name) => [`${Number(value).toLocaleString()} comments`, name]}
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
          <div className="pointer-events-none absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-semibold text-text-primary">{total.toLocaleString()}</span>
            <span className="text-xs text-text-muted">comments</span>
          </div>
        </div>
        <div className="mt-2 flex justify-center gap-4">
          {slices.map((slice) => (
            <div key={slice.key} className="flex items-center gap-1.5 text-xs text-text-secondary">
              <span className="h-2 w-2 rounded-full" style={{ backgroundColor: slice.color }} />
              {slice.label} · {slice.percentage}%
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
