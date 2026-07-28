'use client';

import { useState } from 'react';
import Link from 'next/link';
import { History, Loader2, MessageSquareText, Calendar, ArrowRight, Trash2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ConfirmModal } from '@/components/ui/confirm-modal';
import { useToast } from '@/components/ui/toast-provider';
import { EmptyState } from '@/components/dashboard/empty-state';
import { useAnalysisHistory } from '@/features/analysis/hooks/use-analysis-history';
import { useDashboardPreferences } from '@/features/settings/use-dashboard-preferences';
import { getSentimentBreakdown, getSentimentTotal } from '@/features/analysis/sentiment-utils';
import { clearAllAnalysisJobs, deleteAnalysisJob } from '@/features/analysis/api/analysis-api';
import { ApiError } from '@/lib/api-client';
import type { AnalysisJob } from '@/features/analysis/types';

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return iso;
  }
}

const STATUS_BADGE: Record<AnalysisJob['status'], { status: 'success' | 'info' | 'danger'; label: string }> = {
  completed: { status: 'success', label: 'Completed' },
  processing: { status: 'info', label: 'Processing' },
  pending: { status: 'info', label: 'Pending' },
  failed: { status: 'danger', label: 'Failed' },
  cancelled: { status: 'danger', label: 'Cancelled' },
};

function DominantSentimentBadge({ job }: { job: AnalysisJob }) {
  if (!job.sentiment_summary || getSentimentTotal(job.sentiment_summary) === 0) return null;

  const [dominant] = getSentimentBreakdown(job.sentiment_summary).sort((a, b) => b.value - a.value);
  return <Badge sentiment={dominant.key}>{dominant.percentage}% {dominant.label}</Badge>;
}

function HistoryCard({
  job,
  compact,
  onRequestDelete,
}: {
  job: AnalysisJob;
  compact: boolean;
  onRequestDelete: (job: AnalysisJob) => void;
}) {
  const total = job.sentiment_summary ? getSentimentTotal(job.sentiment_summary) : 0;
  const badge = STATUS_BADGE[job.status];

  return (
    <Card variant="glass" className={compact ? 'p-3' : 'p-5'}>
      <CardContent className="flex flex-col gap-4 p-0 sm:flex-row sm:items-center">
        <div
          className={`shrink-0 overflow-hidden rounded-md border border-border-subtle bg-background-surface ${
            compact ? 'hidden h-12 w-20 sm:block' : 'h-20 w-full sm:w-32'
          }`}
        >
          {job.video_thumbnail_url ? (
            // eslint-disable-next-line @next/next/no-img-element -- external YouTube-hosted thumbnail
            <img
              src={job.video_thumbnail_url}
              alt={job.video_title ?? job.video_url}
              className="h-full w-full object-cover"
            />
          ) : (
            <div className="flex h-full w-full items-center justify-center text-text-muted">
              <History className="h-6 w-6" />
            </div>
          )}
        </div>

        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold text-text-primary">
            {job.video_title || job.video_url}
          </p>
          <div className="mt-1.5 flex flex-wrap items-center gap-3 text-xs text-text-muted">
            <span className="flex items-center gap-1.5">
              <Calendar className="h-3.5 w-3.5" />
              {formatDate(job.created_at)}
            </span>
            {total > 0 && (
              <span className="flex items-center gap-1.5">
                <MessageSquareText className="h-3.5 w-3.5" />
                {total.toLocaleString()} comments
              </span>
            )}
          </div>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            <Badge status={badge.status}>{badge.label}</Badge>
            <DominantSentimentBadge job={job} />
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <Link href={`/dashboard/history/${job.id}`}>
            <Button variant="secondary" size="sm">
              View Details <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </Link>
          <button
            onClick={() => onRequestDelete(job)}
            aria-label={`Delete analysis for ${job.video_title || job.video_url}`}
            className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md text-feedback-danger/80 transition-colors hover:bg-feedback-danger/10 hover:text-feedback-danger"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </CardContent>
    </Card>
  );
}

export default function HistoryPage() {
  const { jobs, isLoading, error, removeJobLocally, clearJobsLocally } = useAnalysisHistory();
  const { preferences } = useDashboardPreferences();
  const { showToast } = useToast();

  const [deleteTarget, setDeleteTarget] = useState<AnalysisJob | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isClearAllOpen, setIsClearAllOpen] = useState(false);
  const [isClearingAll, setIsClearingAll] = useState(false);

  async function handleConfirmDelete() {
    if (!deleteTarget) return;
    setIsDeleting(true);
    try {
      await deleteAnalysisJob(deleteTarget.id);
      removeJobLocally(deleteTarget.id);
      showToast('Analysis deleted.', 'success');
      setDeleteTarget(null);
    } catch (err) {
      showToast(err instanceof ApiError ? err.message : 'Failed to delete analysis.', 'danger');
    } finally {
      setIsDeleting(false);
    }
  }

  async function handleConfirmClearAll() {
    setIsClearingAll(true);
    try {
      const { deleted_count } = await clearAllAnalysisJobs();
      clearJobsLocally();
      showToast(
        deleted_count > 0 ? `Cleared ${deleted_count.toLocaleString()} analyses from your history.` : 'History is already empty.',
        'success'
      );
      setIsClearAllOpen(false);
    } catch (err) {
      showToast(err instanceof ApiError ? err.message : 'Failed to clear history.', 'danger');
    } finally {
      setIsClearingAll(false);
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold text-text-primary">History</h1>
          <p className="mt-1 text-sm text-text-secondary">
            Your past analyses, most recent first.
          </p>
        </div>
        {jobs.length > 0 && (
          <Button variant="ghost" size="sm" onClick={() => setIsClearAllOpen(true)}>
            <Trash2 className="h-3.5 w-3.5" /> Clear All History
          </Button>
        )}
      </div>

      {isLoading ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Loading history…
          </CardContent>
        </Card>
      ) : error ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">{error}</CardContent>
        </Card>
      ) : jobs.length === 0 ? (
        <Card variant="glass" className="p-5">
          <CardContent className="p-0">
            <EmptyState
              icon={History}
              title="No analyses yet"
              description="Run your first analysis to see it listed here with quick access to its results."
              actionLabel="Start New Analysis"
              actionHref="/dashboard/new-analysis"
            />
          </CardContent>
        </Card>
      ) : (
        <div className={`flex flex-col ${preferences.compactLists ? 'gap-2' : 'gap-4'}`}>
          {jobs.map((job) => (
            <HistoryCard
              key={job.id}
              job={job}
              compact={preferences.compactLists}
              onRequestDelete={setDeleteTarget}
            />
          ))}
        </div>
      )}

      <ConfirmModal
        isOpen={deleteTarget !== null}
        title="Delete this analysis?"
        description={`This permanently deletes "${
          deleteTarget?.video_title || deleteTarget?.video_url
        }" and all of its comments, insights, and chat history. This can't be undone.`}
        confirmLabel="Delete"
        variant="danger"
        isConfirming={isDeleting}
        onConfirm={handleConfirmDelete}
        onClose={() => !isDeleting && setDeleteTarget(null)}
      />

      <ConfirmModal
        isOpen={isClearAllOpen}
        title="Clear your entire history?"
        description={
          jobs.length === 1
            ? "This permanently deletes your only analysis and everything attached to it — comments, insights, and chat history. This can't be undone."
            : `This permanently deletes all ${jobs.length.toLocaleString()} of your analyses and everything attached to them — comments, insights, and chat history. This can't be undone.`
        }
        confirmLabel="Clear Everything"
        variant="danger"
        isConfirming={isClearingAll}
        onConfirm={handleConfirmClearAll}
        onClose={() => !isClearingAll && setIsClearAllOpen(false)}
      />
    </div>
  );
}
