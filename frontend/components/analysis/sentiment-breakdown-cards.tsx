'use client';

import { Smile, Meh, Frown, Gauge, ShieldAlert, Drama, Languages, type LucideIcon } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { getSentimentBreakdown } from '@/features/analysis/sentiment-utils';
import type { SentimentSummary } from '@/features/analysis/types';

interface SentimentBreakdownCardsProps {
  summary: SentimentSummary;
}

const SENTIMENT_ICONS = { positive: Smile, neutral: Meh, negative: Frown } as const;

function MetricCard({
  icon: Icon,
  label,
  value,
  detail,
  color,
}: {
  icon: LucideIcon;
  label: string;
  value: string;
  detail: string;
  color: string;
}) {
  return (
    <Card variant="glass" className="p-4">
      <CardContent className="flex flex-col gap-2 p-0">
        <div className="flex items-center justify-between">
          <span className="text-xs font-medium text-text-muted">{label}</span>
          <span
            className="flex h-7 w-7 items-center justify-center rounded-md"
            style={{ backgroundColor: `${color}26`, color }}
          >
            <Icon className="h-4 w-4" />
          </span>
        </div>
        <p className="text-2xl font-semibold text-text-primary">{value}</p>
        <p className="text-xs text-text-muted">{detail}</p>
      </CardContent>
    </Card>
  );
}

export function SentimentBreakdownCards({ summary }: SentimentBreakdownCardsProps) {
  const slices = getSentimentBreakdown(summary);
  const total = summary.positive_count + summary.negative_count + summary.neutral_count;
  const pct = (n: number) => (total > 0 ? `${Math.round((n / total) * 100)}% of comments` : '—');

  return (
    <div className="flex flex-col gap-4">
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        {slices.map((slice) => {
          const Icon = SENTIMENT_ICONS[slice.key];
          return (
            <MetricCard
              key={slice.key}
              icon={Icon}
              label={slice.label}
              value={slice.value.toLocaleString()}
              detail={`${slice.percentage}% of comments`}
              color={slice.color}
            />
          );
        })}
        <MetricCard
          icon={Gauge}
          label="Avg. Confidence"
          value={summary.average_confidence !== null ? `${Math.round(summary.average_confidence * 100)}%` : '—'}
          detail="model confidence"
          color="#6366F1"
        />
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
        <MetricCard
          icon={ShieldAlert}
          label="Spam"
          value={summary.spam_count.toLocaleString()}
          detail={pct(summary.spam_count)}
          color="#f97316"
        />
        <MetricCard
          icon={Drama}
          label="Sarcasm"
          value={summary.sarcasm_count.toLocaleString()}
          detail={pct(summary.sarcasm_count)}
          color="#a78bfa"
        />
        <MetricCard
          icon={Languages}
          label="Arabic"
          value={summary.arabic_count.toLocaleString()}
          detail={pct(summary.arabic_count)}
          color="#22C55E"
        />
        <MetricCard
          icon={Languages}
          label="English"
          value={summary.english_count.toLocaleString()}
          detail={pct(summary.english_count)}
          color="#3b82f6"
        />
      </div>
    </div>
  );
}
