import { colors } from '@/styles/design-tokens';
import type { SentimentSummary } from '@/features/analysis/types';

export interface SentimentSlice {
  key: 'positive' | 'neutral' | 'negative';
  label: string;
  value: number;
  percentage: number;
  color: string;
}

const SLICE_META = [
  { key: 'positive' as const, label: 'Positive', color: colors.sentiment.positive },
  { key: 'neutral' as const, label: 'Neutral', color: colors.sentiment.neutral },
  { key: 'negative' as const, label: 'Negative', color: colors.sentiment.negative },
];

export function getSentimentTotal(summary: SentimentSummary): number {
  return summary.positive_count + summary.neutral_count + summary.negative_count;
}

export function aggregateSentimentSummaries(summaries: SentimentSummary[]): SentimentSummary {
  const totals = {
    positive_count: 0,
    neutral_count: 0,
    negative_count: 0,
    spam_count: 0,
    sarcasm_count: 0,
    arabic_count: 0,
    english_count: 0,
    mixed_count: 0,
    other_count: 0,
  };
  let weightedConfidence = 0;
  let confidenceWeight = 0;

  for (const summary of summaries) {
    totals.positive_count += summary.positive_count;
    totals.neutral_count += summary.neutral_count;
    totals.negative_count += summary.negative_count;
    totals.spam_count += summary.spam_count;
    totals.sarcasm_count += summary.sarcasm_count;
    totals.arabic_count += summary.arabic_count;
    totals.english_count += summary.english_count;
    totals.mixed_count += summary.mixed_count;
    totals.other_count += summary.other_count;

    const total = getSentimentTotal(summary);
    if (summary.average_confidence !== null && total > 0) {
      weightedConfidence += summary.average_confidence * total;
      confidenceWeight += total;
    }
  }

  return {
    ...totals,
    average_confidence: confidenceWeight > 0 ? weightedConfidence / confidenceWeight : null,
  };
}

export function getSentimentBreakdown(summary: SentimentSummary): SentimentSlice[] {
  const total = getSentimentTotal(summary);
  const counts: Record<SentimentSlice['key'], number> = {
    positive: summary.positive_count,
    neutral: summary.neutral_count,
    negative: summary.negative_count,
  };

  return SLICE_META.map((meta) => ({
    ...meta,
    value: counts[meta.key],
    percentage: total > 0 ? Math.round((counts[meta.key] / total) * 100) : 0,
  }));
}
