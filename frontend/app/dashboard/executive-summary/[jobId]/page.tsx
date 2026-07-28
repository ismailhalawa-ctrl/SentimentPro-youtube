'use client';

import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Loader2, ThumbsDown, ThumbsUp, TrendingUp } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { FeatureUnavailableCard } from '@/components/ai/feature-unavailable-card';
import { useAnalysisJobDetail } from '@/features/analysis/hooks/use-analysis-job-detail';
import { useExecutiveSummary } from '@/features/executive-summary/hooks/use-executive-summary';

const SENTIMENT_LABEL_COLOR: Record<string, string> = {
  positive: 'text-sentiment-positive',
  negative: 'text-sentiment-negative',
  neutral: 'text-sentiment-neutral',
  mixed: 'text-brand-400',
};

function ListSection({
  icon,
  label,
  items,
}: {
  icon: React.ReactNode;
  label: string;
  items: string[];
}) {
  if (items.length === 0) return null;
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-3 p-0">
        <div className="flex items-center gap-2 text-sm font-medium text-text-primary">
          {icon}
          {label}
        </div>
        <ul className="flex flex-col gap-2">
          {items.map((item, i) => (
            <li key={i} className="text-sm text-text-secondary">
              {item}
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}

export default function ExecutiveSummaryPage() {
  const params = useParams<{ jobId: string }>();
  const router = useRouter();
  const jobId = Number(params.jobId);

  const { job } = useAnalysisJobDetail(jobId);
  const { data, status, reason, isLoading } = useExecutiveSummary(jobId);

  if (!Number.isFinite(jobId)) {
    router.replace('/dashboard/history');
    return null;
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link
          href={`/dashboard/history/${jobId}`}
          className="mb-1 flex items-center gap-1.5 text-sm text-text-secondary hover:text-text-primary"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          Back to Analysis
        </Link>
        <h1 className="text-2xl font-semibold text-text-primary">Executive Summary</h1>
        <p className="mt-1 text-sm text-text-secondary">
          {job?.video_title ?? 'AI-generated overview of this analysis.'}
        </p>
      </div>

      {isLoading ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Generating executive summary…
          </CardContent>
        </Card>
      ) : status === 'unavailable' ? (
        <FeatureUnavailableCard reason={reason} />
      ) : status === 'error' || !data ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">
            {reason ?? 'Failed to generate the executive summary.'}
          </CardContent>
        </Card>
      ) : (
        <div className="flex flex-col gap-6">
          <Card variant="glass" className="p-5">
            <CardContent className="flex flex-col gap-3 p-0">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-text-muted">Overall sentiment</span>
                <span
                  className={`text-sm font-semibold capitalize ${
                    SENTIMENT_LABEL_COLOR[data.overall_sentiment_label] ?? 'text-text-primary'
                  }`}
                >
                  {data.overall_sentiment_label}
                </span>
              </div>
              <p className="text-sm leading-relaxed text-text-primary">{data.overview}</p>
            </CardContent>
          </Card>

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <ListSection
              icon={<ThumbsUp className="h-4 w-4 text-sentiment-positive" />}
              label="Key positives"
              items={data.key_positives}
            />
            <ListSection
              icon={<ThumbsDown className="h-4 w-4 text-sentiment-negative" />}
              label="Key negatives"
              items={data.key_negatives}
            />
          </div>

          <ListSection
            icon={<TrendingUp className="h-4 w-4 text-brand-400" />}
            label="Notable trends"
            items={data.notable_trends}
          />
        </div>
      )}
    </div>
  );
}
