'use client';

import { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  AlertTriangle,
  ArrowLeft,
  Bot,
  Calendar,
  ExternalLink,
  Gauge,
  HelpCircle,
  Layers,
  Lightbulb,
  Loader2,
  Sparkles,
  Users,
} from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { AnalysisProgress } from '@/components/analysis/analysis-progress';
import { CommentCleaningBanner } from '@/components/analysis/comment-cleaning-banner';
import { SentimentPieChart } from '@/components/analysis/sentiment-pie-chart';
import { SentimentBarChart } from '@/components/analysis/sentiment-bar-chart';
import { SentimentBreakdownCards } from '@/components/analysis/sentiment-breakdown-cards';
import { LanguageDistributionChart } from '@/components/analysis/language-distribution-chart';
import { SentimentTimelineChart } from '@/components/analysis/sentiment-timeline-chart';
import { LikesScatterChart } from '@/components/analysis/likes-scatter-chart';
import { InsightsPanel } from '@/components/analysis/insights-panel';
import { KeywordsPanel } from '@/components/analysis/keywords-panel';
import { TopicsPanel } from '@/components/analysis/topics-panel';
import { CommentsExplorer } from '@/components/analysis/comments-explorer';
import { TopCommentsPanel } from '@/components/analysis/top-comments-panel';
import { ExportMenu } from '@/components/analysis/export-menu';
import { useAnalysisJobDetail } from '@/features/analysis/hooks/use-analysis-job-detail';
import { useAnalysisExtras } from '@/features/analysis/hooks/use-analysis-extras';
import { useAnalysisComments } from '@/features/analysis/hooks/use-analysis-comments';

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    });
  } catch {
    return iso;
  }
}

const TABS = ['Overview', 'Comments', 'Keywords', 'Insights'] as const;
type Tab = (typeof TABS)[number];

export default function HistoryDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const jobId = Number(params.id);
  const [activeTab, setActiveTab] = useState<Tab>('Overview');

  const { job, isLoading, error, isCancelling, cancel } = useAnalysisJobDetail(jobId);
  const isCompleted = job?.status === 'completed';
  const { keywords, topics, insights, isLoading: isLoadingExtras } = useAnalysisExtras(
    jobId,
    isCompleted
  );
  const { comments, isLoading: isLoadingComments } = useAnalysisComments(jobId, isCompleted);

  if (!Number.isFinite(jobId)) {
    router.replace('/dashboard/history');
    return null;
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-4">
        <div>
          <Link
            href="/dashboard/history"
            className="mb-1 flex items-center gap-1.5 text-sm text-text-secondary hover:text-text-primary"
          >
            <ArrowLeft className="h-3.5 w-3.5" />
            Back to History
          </Link>
          <h1 className="text-2xl font-semibold text-text-primary break-words">
            {job?.video_title || 'Analysis Details'}
          </h1>
          {job && (
            <p className="mt-1 flex items-center gap-1.5 text-sm text-text-secondary">
              <Calendar className="h-3.5 w-3.5" />
              {formatDate(job.created_at)}
            </p>
          )}
        </div>

        {isCompleted && job && (
          <div className="flex flex-wrap gap-2">
            <Link href={`/dashboard/audience-assistant?jobId=${job.id}`}>
              <Button variant="secondary" size="sm">
                <Bot className="h-3.5 w-3.5" /> AI Assistant
              </Button>
            </Link>
            <Link href={`/dashboard/executive-summary/${job.id}`}>
              <Button variant="secondary" size="sm">
                <Sparkles className="h-3.5 w-3.5" /> Executive Summary
              </Button>
            </Link>
            <Link href={`/dashboard/complaints/${job.id}`}>
              <Button variant="secondary" size="sm">
                <AlertTriangle className="h-3.5 w-3.5" /> Complaints
              </Button>
            </Link>
            <Link href={`/dashboard/suggestions/${job.id}`}>
              <Button variant="secondary" size="sm">
                <Lightbulb className="h-3.5 w-3.5" /> Suggestions
              </Button>
            </Link>
            <Link href={`/dashboard/faqs/${job.id}`}>
              <Button variant="secondary" size="sm">
                <HelpCircle className="h-3.5 w-3.5" /> FAQs
              </Button>
            </Link>
            <Link href={`/dashboard/topics/${job.id}`}>
              <Button variant="secondary" size="sm">
                <Layers className="h-3.5 w-3.5" /> Topics
              </Button>
            </Link>
            <Link href={`/dashboard/personas/${job.id}`}>
              <Button variant="secondary" size="sm">
                <Users className="h-3.5 w-3.5" /> Personas
              </Button>
            </Link>
            <Link href={`/dashboard/audience-intelligence/${job.id}`}>
              <Button variant="secondary" size="sm">
                <Gauge className="h-3.5 w-3.5" /> Audience Intelligence
              </Button>
            </Link>
            <a href={job.video_url} target="_blank" rel="noopener noreferrer">
              <Button variant="secondary" size="sm">
                <ExternalLink className="h-3.5 w-3.5" /> Watch
              </Button>
            </a>
            <ExportMenu jobId={job.id} filenameHint={`analysis_${job.video_id}`} />
          </div>
        )}
      </div>

      {isLoading ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Loading analysis…
          </CardContent>
        </Card>
      ) : error || !job ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">
            {error || 'Analysis not found.'}
          </CardContent>
        </Card>
      ) : job.status !== 'completed' ? (
        <AnalysisProgress job={job} label="Analysis Progress" onCancel={cancel} isCancelling={isCancelling} />
      ) : job.sentiment_summary ? (
        <div className="flex flex-col gap-6">
          <div className="flex gap-1 rounded-md bg-background-surface p-1">
            {TABS.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={cn(
                  'flex-1 rounded-sm px-4 py-2 text-sm font-medium transition-colors',
                  activeTab === tab
                    ? 'bg-brand-500 text-text-primary'
                    : 'text-text-secondary hover:text-text-primary'
                )}
              >
                {tab}
              </button>
            ))}
          </div>

          {activeTab === 'Overview' && (
            <div className="flex flex-col gap-6">
              <CommentCleaningBanner job={job} />
              <SentimentBreakdownCards summary={job.sentiment_summary} />
              <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
                <SentimentPieChart summary={job.sentiment_summary} />
                <SentimentBarChart summary={job.sentiment_summary} />
              </div>

              <LanguageDistributionChart summary={job.sentiment_summary} />

              {isLoadingComments ? (
                <LoadingExtras />
              ) : (
                <>
                  <SentimentTimelineChart comments={comments} />
                  <LikesScatterChart comments={comments} />
                </>
              )}

              <div>
                <p className="mb-3 text-sm font-medium text-text-muted">AI Insights</p>
                {isLoadingExtras ? (
                  <LoadingExtras />
                ) : insights ? (
                  <InsightsPanel insights={insights.insights} source={insights.source} />
                ) : null}
              </div>
            </div>
          )}

          {activeTab === 'Comments' &&
            (isLoadingComments ? (
              <LoadingExtras />
            ) : (
              <div className="flex flex-col gap-6">
                <CommentsExplorer comments={comments} />
                <TopCommentsPanel comments={comments} />
              </div>
            ))}

          {activeTab === 'Keywords' &&
            (isLoadingExtras ? (
              <LoadingExtras />
            ) : keywords ? (
              <KeywordsPanel positive={keywords.positive} negative={keywords.negative} neutral={keywords.neutral} />
            ) : null)}

          {activeTab === 'Insights' &&
            (isLoadingExtras ? (
              <LoadingExtras />
            ) : (
              <div className="flex flex-col gap-6">
                {insights && <InsightsPanel insights={insights.insights} source={insights.source} />}
                {topics && <TopicsPanel positive={topics.positive} negative={topics.negative} />}
              </div>
            ))}
        </div>
      ) : null}
    </div>
  );
}

function LoadingExtras() {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
        <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
        Loading…
      </CardContent>
    </Card>
  );
}
