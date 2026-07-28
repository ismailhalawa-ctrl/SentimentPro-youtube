'use client';

import { FileText, Loader2, Video, MessageSquareText, Smile, Gauge } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { EmptyState } from '@/components/dashboard/empty-state';
import { SentimentPieChart } from '@/components/analysis/sentiment-pie-chart';
import { SentimentBarChart } from '@/components/analysis/sentiment-bar-chart';
import { SentimentBreakdownCards } from '@/components/analysis/sentiment-breakdown-cards';
import { ExportMenu } from '@/components/analysis/export-menu';
import { useAnalysisHistory } from '@/features/analysis/hooks/use-analysis-history';
import { aggregateSentimentSummaries, getSentimentTotal } from '@/features/analysis/sentiment-utils';
import type { AnalysisJob } from '@/features/analysis/types';

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' });
  } catch {
    return iso;
  }
}

function ReportKpiCard({
  icon: Icon,
  label,
  value,
}: {
  icon: typeof Video;
  label: string;
  value: string;
}) {
  return (
    <Card variant="glass" className="p-4">
      <CardContent className="flex items-center gap-3 p-0">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
          <Icon className="h-4.5 w-4.5" />
        </span>
        <div className="min-w-0">
          <p className="text-xs text-text-muted">{label}</p>
          <p className="truncate text-lg font-semibold text-text-primary">{value}</p>
        </div>
      </CardContent>
    </Card>
  );
}

function ReportRow({ job }: { job: AnalysisJob }) {
  const total = job.sentiment_summary ? getSentimentTotal(job.sentiment_summary) : 0;

  return (
    <div className="flex flex-col gap-2 py-3 first:pt-0 last:pb-0 sm:flex-row sm:items-center sm:justify-between">
      <div className="min-w-0">
        <p className="truncate text-sm font-medium text-text-primary">
          {job.video_title || job.video_url}
        </p>
        <p className="text-xs text-text-muted">
          {formatDate(job.created_at)} · {total.toLocaleString()} comments
        </p>
      </div>
      <div className="shrink-0">
        <ExportMenu jobId={job.id} filenameHint={`analysis_${job.video_id}`} />
      </div>
    </div>
  );
}

export default function ReportsPage() {
  const { jobs, isLoading, error } = useAnalysisHistory();

  const completedJobs = jobs.filter((j) => j.status === 'completed' && j.sentiment_summary);
  const aggregate =
    completedJobs.length > 0
      ? aggregateSentimentSummaries(completedJobs.map((j) => j.sentiment_summary!))
      : null;
  const totalComments = aggregate ? getSentimentTotal(aggregate) : 0;
  const positivePct =
    aggregate && totalComments > 0 ? Math.round((aggregate.positive_count / totalComments) * 100) : 0;

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold text-text-primary">Reports</h1>
        <p className="mt-1 text-sm text-text-secondary">
          Aggregate metrics across every video you&apos;ve analyzed, with CSV export per report.
        </p>
      </div>

      {isLoading ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Loading reports…
          </CardContent>
        </Card>
      ) : error ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">{error}</CardContent>
        </Card>
      ) : !aggregate ? (
        <Card variant="glass" className="p-5">
          <CardContent className="p-0">
            <EmptyState
              icon={FileText}
              title="No report data yet"
              description="Run and complete at least one analysis to see aggregate reports and CSV exports here."
              actionLabel="Start New Analysis"
              actionHref="/dashboard/new-analysis"
            />
          </CardContent>
        </Card>
      ) : (
        <>
          <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
            <ReportKpiCard icon={Video} label="Videos Analyzed" value={completedJobs.length.toLocaleString()} />
            <ReportKpiCard
              icon={MessageSquareText}
              label="Total Comments"
              value={totalComments.toLocaleString()}
            />
            <ReportKpiCard icon={Smile} label="Overall Positive" value={`${positivePct}%`} />
            <ReportKpiCard
              icon={Gauge}
              label="Avg. Confidence"
              value={
                aggregate.average_confidence !== null
                  ? `${Math.round(aggregate.average_confidence * 100)}%`
                  : '—'
              }
            />
          </div>

          <SentimentBreakdownCards summary={aggregate} />

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <SentimentPieChart summary={aggregate} />
            <SentimentBarChart summary={aggregate} />
          </div>

          <Card variant="glass" className="p-5">
            <CardContent className="flex flex-col gap-0 p-0">
              <p className="mb-2 text-sm font-medium text-text-muted">Per-Video Reports</p>
              <div className="flex flex-col divide-y divide-border-subtle">
                {completedJobs.map((job) => (
                  <ReportRow key={job.id} job={job} />
                ))}
              </div>
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}
