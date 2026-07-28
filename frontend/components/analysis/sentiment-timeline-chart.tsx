'use client';

import { useMemo } from 'react';
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import { Card, CardContent } from '@/components/ui/card';
import { colors } from '@/styles/design-tokens';
import type { CommentEntry } from '@/features/analysis/types';

interface SentimentTimelineChartProps {
  comments: CommentEntry[];
}

interface TimelinePoint {
  date: string;
  positive: number;
  negative: number;
  neutral: number;
}

function toDateKey(publishedAt: string): string | null {
  const parsed = new Date(publishedAt);
  if (Number.isNaN(parsed.getTime())) return null;
  return parsed.toISOString().slice(0, 10);
}

export function SentimentTimelineChart({ comments }: SentimentTimelineChartProps) {
  const data = useMemo<TimelinePoint[]>(() => {
    const byDate = new Map<string, TimelinePoint>();

    for (const comment of comments) {
      if (!comment.published_at || !comment.sentiment) continue;
      const dateKey = toDateKey(comment.published_at);
      if (!dateKey) continue;

      let point = byDate.get(dateKey);
      if (!point) {
        point = { date: dateKey, positive: 0, negative: 0, neutral: 0 };
        byDate.set(dateKey, point);
      }
      point[comment.sentiment] += 1;
    }

    return [...byDate.values()].sort((a, b) => a.date.localeCompare(b.date));
  }, [comments]);

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="p-0">
        <p className="mb-4 text-sm font-medium text-text-muted">Sentiment Over Time</p>
        {data.length < 2 ? (
          <p className="py-10 text-center text-sm text-text-muted">
            Not enough date spread in these comments to chart a timeline.
          </p>
        ) : (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
                <CartesianGrid vertical={false} stroke={colors.border.subtle} strokeWidth={1} />
                <XAxis
                  dataKey="date"
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: colors.text.secondary, fontSize: 11 }}
                />
                <YAxis
                  allowDecimals={false}
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: colors.text.secondary, fontSize: 11 }}
                  width={28}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: colors.background.elevated,
                    border: `1px solid ${colors.border.default}`,
                    borderRadius: '0.5rem',
                    color: colors.text.primary,
                    fontSize: '0.875rem',
                  }}
                />
                <Legend
                  wrapperStyle={{ fontSize: 12, color: colors.text.secondary }}
                  iconType="circle"
                  iconSize={8}
                />
                <Line
                  type="monotone"
                  dataKey="positive"
                  name="Positive"
                  stroke={colors.sentiment.positive}
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="negative"
                  name="Negative"
                  stroke={colors.sentiment.negative}
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="neutral"
                  name="Neutral"
                  stroke={colors.sentiment.neutral}
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
