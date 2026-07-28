'use client';

import { FilePlus2, Loader2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { EmptyState } from './empty-state';
import { useAnalysisHistory } from '@/features/analysis/hooks/use-analysis-history';
import { getSentimentBreakdown, getSentimentTotal } from '@/features/analysis/sentiment-utils';
import type { AnalysisJob } from '@/features/analysis/types';

const RECENT_LIMIT = 5;

const STATUS_BADGE: Record<AnalysisJob['status'], 'success' | 'info' | 'danger'> = {
  completed: 'success',
  processing: 'info',
  pending: 'info',
  failed: 'danger',
  cancelled: 'danger',
};

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  } catch {
    return iso;
  }
}

export function RecentAnalyses() {
  const { jobs, isLoading } = useAnalysisHistory();
  const recentJobs = jobs.slice(0, RECENT_LIMIT);

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <p className="text-sm font-medium text-text-muted">Recent Analyses</p>

        {isLoading ? (
          <div className="flex items-center gap-2.5 py-6 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Loading…
          </div>
        ) : recentJobs.length === 0 ? (
          <EmptyState
            icon={FilePlus2}
            title="No analyses yet"
            description="Run your first analysis to see sentiment, spam, and keyword insights here."
            actionLabel="Start New Analysis"
            actionHref="/dashboard/new-analysis"
          />
        ) : (
          <div className="flex flex-col divide-y divide-border-subtle">
            {recentJobs.map((job) => {
              const total = job.sentiment_summary ? getSentimentTotal(job.sentiment_summary) : 0;
              const [dominant] =
                job.sentiment_summary && total > 0
                  ? getSentimentBreakdown(job.sentiment_summary).sort((a, b) => b.value - a.value)
                  : [null];

              return (
                <div
                  key={job.id}
                  className="flex flex-col gap-2 py-3 first:pt-0 last:pb-0 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-text-primary">
                      {job.video_title || job.video_url}
                    </p>
                    <p className="text-xs text-text-muted">
                      {formatDate(job.created_at)}
                      {total > 0 && ` · ${total.toLocaleString()} comments`}
                    </p>
                  </div>
                  <div className="flex shrink-0 items-center gap-2">
                    {dominant && <Badge sentiment={dominant.key}>{dominant.label}</Badge>}
                    <Badge status={STATUS_BADGE[job.status]}>{job.status}</Badge>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
