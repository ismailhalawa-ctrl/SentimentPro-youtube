'use client';

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { Card, CardContent } from '@/components/ui/card';
import { colors } from '@/styles/design-tokens';
import { getSentimentBreakdown } from '@/features/analysis/sentiment-utils';
import type { SentimentSummary } from '@/features/analysis/types';

interface SentimentBarChartProps {
  summary: SentimentSummary;
}

export function SentimentBarChart({ summary }: SentimentBarChartProps) {
  const slices = getSentimentBreakdown(summary);

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="p-0">
        <p className="mb-4 text-sm font-medium text-text-muted">Comments by Sentiment</p>
        <div className="h-56 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={slices} layout="vertical" margin={{ left: 8, right: 24 }}>
              <CartesianGrid
                horizontal={false}
                stroke={colors.border.subtle}
                strokeWidth={1}
              />
              <XAxis type="number" hide />
              <YAxis
                type="category"
                dataKey="label"
                width={70}
                axisLine={false}
                tickLine={false}
                tick={{ fill: colors.text.secondary, fontSize: 12 }}
              />
              <Tooltip
                cursor={{ fill: colors.background.elevated }}
                formatter={(value) => [`${Number(value).toLocaleString()} comments`, undefined]}
                labelFormatter={() => ''}
                contentStyle={{
                  backgroundColor: colors.background.elevated,
                  border: `1px solid ${colors.border.default}`,
                  borderRadius: '0.5rem',
                  color: colors.text.primary,
                  fontSize: '0.875rem',
                }}
              />
              <Bar dataKey="value" barSize={20} radius={[0, 4, 4, 0]}>
                {slices.map((slice) => (
                  <Cell key={slice.key} fill={slice.color} />
                ))}
                <LabelList
                  dataKey="value"
                  position="right"
                  formatter={(value) => Number(value).toLocaleString()}
                  fill={colors.text.secondary}
                  fontSize={12}
                />
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
