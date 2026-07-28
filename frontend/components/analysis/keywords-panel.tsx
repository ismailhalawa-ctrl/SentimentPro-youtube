'use client';

import { Bar, BarChart, CartesianGrid, LabelList, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Card, CardContent } from '@/components/ui/card';
import { colors } from '@/styles/design-tokens';
import type { KeywordEntry } from '@/features/analysis/types';

interface KeywordColumnProps {
  label: string;
  entries: KeywordEntry[];
  color: string;
}

function KeywordColumn({ label, entries, color }: KeywordColumnProps) {
  const chartData = [...entries].slice(0, 10).reverse();

  return (
    <Card variant="glass" className="p-4">
      <CardContent className="p-0">
        <p className="mb-3 text-sm font-medium text-text-muted">{label}</p>
        {chartData.length === 0 ? (
          <p className="py-8 text-center text-sm text-text-muted">No keywords found.</p>
        ) : (
          <div style={{ height: Math.max(chartData.length * 28, 120) }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ left: 0, right: 24 }}>
                <CartesianGrid horizontal={false} stroke={colors.border.subtle} strokeWidth={1} />
                <XAxis type="number" hide />
                <YAxis
                  type="category"
                  dataKey="word"
                  width={90}
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: colors.text.secondary, fontSize: 12 }}
                />
                <Tooltip
                  cursor={{ fill: colors.background.elevated }}
                  formatter={(value) => [`${Number(value).toLocaleString()} mentions`, undefined]}
                  labelFormatter={() => ''}
                  contentStyle={{
                    backgroundColor: colors.background.elevated,
                    border: `1px solid ${colors.border.default}`,
                    borderRadius: '0.5rem',
                    color: colors.text.primary,
                    fontSize: '0.875rem',
                  }}
                />
                <Bar dataKey="count" barSize={14} radius={[0, 4, 4, 0]} fill={color}>
                  <LabelList
                    dataKey="count"
                    position="right"
                    formatter={(value) => Number(value).toLocaleString()}
                    fill={colors.text.secondary}
                    fontSize={11}
                  />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

interface KeywordsPanelProps {
  positive: KeywordEntry[];
  negative: KeywordEntry[];
  neutral: KeywordEntry[];
}

export function KeywordsPanel({ positive, negative, neutral }: KeywordsPanelProps) {
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
      <KeywordColumn label="Positive" entries={positive} color={colors.sentiment.positive} />
      <KeywordColumn label="Negative" entries={negative} color={colors.sentiment.negative} />
      <KeywordColumn label="Neutral" entries={neutral} color={colors.sentiment.neutral} />
    </div>
  );
}
