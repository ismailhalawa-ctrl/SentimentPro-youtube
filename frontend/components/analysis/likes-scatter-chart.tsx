'use client';

import { useMemo, useState } from 'react';
import { Heart, ThumbsDown, TrendingUp } from 'lucide-react';
import {
  CartesianGrid,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
  ZAxis,
} from 'recharts';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { colors } from '@/styles/design-tokens';
import { sanitizeCommentText } from '@/lib/sanitize-comment-text';
import type { CommentEntry, CommentSentiment } from '@/features/analysis/types';

interface LikesScatterChartProps {
  comments: CommentEntry[];
}

type ScatterFilter = 'all' | CommentSentiment;

const FILTERS: { key: ScatterFilter; label: string }[] = [
  { key: 'all', label: 'Show All' },
  { key: 'positive', label: 'Positive Only' },
  { key: 'negative', label: 'Negative Only' },
  { key: 'neutral', label: 'Neutral Only' },
];

interface ScatterPoint {
  likesDisplay: number;
  likes: number;
  confidence: number;
  sentiment: CommentSentiment;
  author: string;
  text: string;
}

function average(values: number[]): number {
  return values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;
}

export function LikesScatterChart({ comments }: LikesScatterChartProps) {
  const [filter, setFilter] = useState<ScatterFilter>('all');

  const analyzable = useMemo(
    () => comments.filter((c) => !c.is_spam && c.sentiment && c.confidence !== null),
    [comments]
  );

  const filtered = useMemo(
    () => (filter === 'all' ? analyzable : analyzable.filter((c) => c.sentiment === filter)),
    [analyzable, filter]
  );

  const points: ScatterPoint[] = useMemo(
    () =>
      filtered.map((c) => ({
        likesDisplay: c.likes + 1,
        likes: c.likes,
        confidence: c.confidence as number,
        sentiment: c.sentiment as CommentSentiment,
        author: c.author,
        text: c.text,
      })),
    [filtered]
  );

  const { avgLikesPositive, avgLikesNegative, engagementRatio } = useMemo(() => {
    const positive = average(analyzable.filter((c) => c.sentiment === 'positive').map((c) => c.likes));
    const negative = average(analyzable.filter((c) => c.sentiment === 'negative').map((c) => c.likes));
    return {
      avgLikesPositive: positive,
      avgLikesNegative: negative,
      engagementRatio: negative > 0 ? positive / negative : 0,
    };
  }, [analyzable]);

  const xTicks = useMemo(() => {
    if (points.length === 0) return undefined;
    const maxLikesDisplay = Math.max(...points.map((p) => p.likesDisplay));
    const candidates = [1, 10, 100, 1000, 10000, 100000, 1000000];
    const withinRange = candidates.filter((tick) => tick <= maxLikesDisplay);
    return Array.from(new Set([...withinRange, Math.ceil(maxLikesDisplay)])).sort((a, b) => a - b);
  }, [points]);

  const bySentiment: Record<CommentSentiment, ScatterPoint[]> = useMemo(
    () => ({
      positive: points.filter((p) => p.sentiment === 'positive'),
      negative: points.filter((p) => p.sentiment === 'negative'),
      neutral: points.filter((p) => p.sentiment === 'neutral'),
    }),
    [points]
  );

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <div>
          <p className="text-sm font-medium text-text-muted">Likes vs. Sentiment Confidence</p>
          <p className="mt-1 text-xs text-text-muted">
            Showing {points.length.toLocaleString()} comment{points.length === 1 ? '' : 's'}
          </p>
        </div>

        <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
          {FILTERS.map(({ key, label }) => (
            <Button
              key={key}
              variant={filter === key ? 'primary' : 'secondary'}
              size="sm"
              onClick={() => setFilter(key)}
            >
              {label}
            </Button>
          ))}
        </div>

        {points.length === 0 ? (
          <p className="py-10 text-center text-sm text-text-muted">No comments match this filter.</p>
        ) : (
          <div className="h-96 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 16, right: 24, left: 0, bottom: 8 }}>
                <CartesianGrid stroke={colors.border.subtle} strokeWidth={1} />
                <XAxis
                  type="number"
                  dataKey="likesDisplay"
                  scale="log"
                  domain={['auto', 'auto']}
                  ticks={xTicks}
                  allowDuplicatedCategory={false}
                  name="Likes"
                  tick={{ fill: colors.text.secondary, fontSize: 11 }}
                  tickFormatter={(value) => Number(value).toLocaleString()}
                  label={{ value: 'Likes (log scale)', position: 'insideBottom', offset: -4, fill: colors.text.muted, fontSize: 11 }}
                />
                <YAxis
                  type="number"
                  dataKey="confidence"
                  domain={[0, 1]}
                  tickFormatter={(value) => `${Math.round(Number(value) * 100)}%`}
                  tick={{ fill: colors.text.secondary, fontSize: 11 }}
                  label={{ value: 'Confidence', angle: -90, position: 'insideLeft', fill: colors.text.muted, fontSize: 11 }}
                />
                <ZAxis range={[40, 220]} />
                <ReferenceLine y={0.66} stroke={colors.sentiment.positive} strokeDasharray="4 4" strokeOpacity={0.5} />
                <ReferenceLine y={0.33} stroke={colors.sentiment.negative} strokeDasharray="4 4" strokeOpacity={0.5} />
                <Tooltip
                  cursor={{ strokeDasharray: '3 3' }}
                  formatter={(value, name) => {
                    if (name === 'confidence') return [`${Math.round(Number(value) * 100)}%`, 'Confidence'];
                    return [value, name];
                  }}
                  content={({ active, payload }) => {
                    if (!active || !payload?.length) return null;
                    const p = payload[0].payload as ScatterPoint;
                    return (
                      <div
                        className="max-w-xs rounded-md border p-3 text-xs"
                        style={{
                          backgroundColor: colors.background.elevated,
                          borderColor: colors.border.default,
                          color: colors.text.primary,
                        }}
                      >
                        <p className="font-medium">{p.author}</p>
                        <p className="mt-1 line-clamp-3 text-text-secondary">{sanitizeCommentText(p.text)}</p>
                        <p className="mt-1.5 text-text-muted">
                          {p.likes.toLocaleString()} likes · {Math.round(p.confidence * 100)}% confidence
                        </p>
                      </div>
                    );
                  }}
                />
                <Scatter
                  name="Positive"
                  data={bySentiment.positive}
                  fill={colors.sentiment.positive}
                  fillOpacity={0.75}
                />
                <Scatter
                  name="Negative"
                  data={bySentiment.negative}
                  fill={colors.sentiment.negative}
                  fillOpacity={0.75}
                />
                <Scatter
                  name="Neutral"
                  data={bySentiment.neutral}
                  fill={colors.sentiment.neutral}
                  fillOpacity={0.75}
                />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        )}

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
          <div className="rounded-md p-4 text-center" style={{ backgroundColor: `${colors.sentiment.positive}1A` }}>
            <Heart className="mx-auto h-5 w-5" style={{ color: colors.sentiment.positive }} />
            <p className="mt-1.5 text-xl font-semibold" style={{ color: colors.sentiment.positive }}>
              {avgLikesPositive.toFixed(1)}
            </p>
            <p className="text-xs text-text-muted">Avg. Likes (Positive)</p>
          </div>
          <div className="rounded-md p-4 text-center" style={{ backgroundColor: `${colors.sentiment.negative}1A` }}>
            <ThumbsDown className="mx-auto h-5 w-5" style={{ color: colors.sentiment.negative }} />
            <p className="mt-1.5 text-xl font-semibold" style={{ color: colors.sentiment.negative }}>
              {avgLikesNegative.toFixed(1)}
            </p>
            <p className="text-xs text-text-muted">Avg. Likes (Negative)</p>
          </div>
          <div className="rounded-md p-4 text-center" style={{ backgroundColor: 'rgba(99,102,241,0.1)' }}>
            <TrendingUp className="mx-auto h-5 w-5 text-brand-400" />
            <p className="mt-1.5 text-xl font-semibold text-brand-400">{engagementRatio.toFixed(1)}x</p>
            <p className="text-xs text-text-muted">Positive / Negative Ratio</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
