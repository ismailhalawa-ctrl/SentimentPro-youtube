'use client';

import { Bar, BarChart, CartesianGrid, Cell, LabelList, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Card, CardContent } from '@/components/ui/card';
import { colors } from '@/styles/design-tokens';
import type { SentimentSummary } from '@/features/analysis/types';

interface LanguageDistributionChartProps {
  summary: SentimentSummary;
}

const LANGUAGE_COLOR = '#8B5CF6';

export function LanguageDistributionChart({ summary }: LanguageDistributionChartProps) {
  const data = [
    { language: 'Arabic', count: summary.arabic_count },
    { language: 'English', count: summary.english_count },
    { language: 'Mixed', count: summary.mixed_count },
    { language: 'Other', count: summary.other_count },
  ].filter((d) => d.count > 0);

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="p-0">
        <p className="mb-4 text-sm font-medium text-text-muted">Language Distribution</p>
        {data.length === 0 ? (
          <p className="py-10 text-center text-sm text-text-muted">No language data available.</p>
        ) : (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data} margin={{ top: 16, right: 16, left: 0, bottom: 0 }}>
                <CartesianGrid vertical={false} stroke={colors.border.subtle} strokeWidth={1} />
                <XAxis
                  dataKey="language"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: colors.text.secondary, fontSize: 12 }}
                />
                <YAxis hide />
                <Tooltip
                  cursor={{ fill: colors.background.elevated }}
                  formatter={(value) => [`${Number(value).toLocaleString()} comments`, undefined]}
                  labelFormatter={(label) => String(label)}
                  contentStyle={{
                    backgroundColor: colors.background.elevated,
                    border: `1px solid ${colors.border.default}`,
                    borderRadius: '0.5rem',
                    color: colors.text.primary,
                    fontSize: '0.875rem',
                  }}
                />
                <Bar dataKey="count" barSize={40} radius={[4, 4, 0, 0]}>
                  {data.map((d) => (
                    <Cell key={d.language} fill={LANGUAGE_COLOR} fillOpacity={0.85} />
                  ))}
                  <LabelList
                    dataKey="count"
                    position="top"
                    formatter={(value) => Number(value).toLocaleString()}
                    fill={colors.text.secondary}
                    fontSize={12}
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
