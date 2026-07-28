'use client';

import { Loader2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { SentimentPieChart } from '@/components/analysis/sentiment-pie-chart';
import { SentimentBarChart } from '@/components/analysis/sentiment-bar-chart';
import { SentimentBreakdownCards } from '@/components/analysis/sentiment-breakdown-cards';
import { LanguageDistributionChart } from '@/components/analysis/language-distribution-chart';
import { SentimentTimelineChart } from '@/components/analysis/sentiment-timeline-chart';
import { LikesScatterChart } from '@/components/analysis/likes-scatter-chart';
import { InsightsPanel } from '@/components/analysis/insights-panel';
import { TopCommentsPanel } from '@/components/analysis/top-comments-panel';
import { useAnalysisComments } from '@/features/analysis/hooks/use-analysis-comments';
import { useAnalysisExtras } from '@/features/analysis/hooks/use-analysis-extras';
import type { AnalysisJob } from '@/features/analysis/types';

interface AnalysisResultsBlockProps {
  job: AnalysisJob;
}

export function AnalysisResultsBlock({ job }: AnalysisResultsBlockProps) {
  const isCompleted = job.status === 'completed';
  const { comments, isLoading: isLoadingComments } = useAnalysisComments(job.id, isCompleted);
  const { insights, isLoading: isLoadingInsights } = useAnalysisExtras(job.id, isCompleted);

  if (!job.sentiment_summary) return null;

  return (
    <div className="flex flex-col gap-6">
      <SentimentBreakdownCards summary={job.sentiment_summary} />

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <SentimentPieChart summary={job.sentiment_summary} />
        <SentimentBarChart summary={job.sentiment_summary} />
      </div>

      <LanguageDistributionChart summary={job.sentiment_summary} />

      {isLoadingComments ? (
        <LoadingBlock />
      ) : (
        <>
          <SentimentTimelineChart comments={comments} />
          <LikesScatterChart comments={comments} />
        </>
      )}

      <div>
        <p className="mb-3 text-sm font-medium text-text-muted">AI Insights</p>
        {isLoadingInsights ? <LoadingBlock /> : insights ? <InsightsPanel insights={insights.insights} source={insights.source} /> : null}
      </div>

      {isLoadingComments ? <LoadingBlock /> : <TopCommentsPanel comments={comments} />}
    </div>
  );
}

function LoadingBlock() {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
        <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
        Loading…
      </CardContent>
    </Card>
  );
}
