'use client';

import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Layers, Loader2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FeatureUnavailableCard } from '@/components/ai/feature-unavailable-card';
import { useAnalysisJobDetail } from '@/features/analysis/hooks/use-analysis-job-detail';
import { useTopics } from '@/features/topics/hooks/use-topics';

export default function TopicsPage() {
  const params = useParams<{ jobId: string }>();
  const router = useRouter();
  const jobId = Number(params.jobId);

  const { job } = useAnalysisJobDetail(jobId);
  const { data, status, reason, isLoading } = useTopics(jobId);

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
        <h1 className="text-2xl font-semibold text-text-primary">Topics</h1>
        <p className="mt-1 text-sm text-text-secondary">
          {job?.video_title ?? 'The main subjects commenters are discussing.'}
        </p>
      </div>

      {isLoading ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Clustering topics…
          </CardContent>
        </Card>
      ) : status === 'unavailable' ? (
        <FeatureUnavailableCard reason={reason} />
      ) : status === 'error' || !data ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">
            {reason ?? 'Failed to cluster topics.'}
          </CardContent>
        </Card>
      ) : data.topics.length === 0 ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Layers className="h-4 w-4" />
            No clear topics emerged from this job&apos;s comments.
          </CardContent>
        </Card>
      ) : (
        <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
          {data.topics.map((topic, i) => (
            <Card key={i} variant="glass" className="p-5">
              <CardContent className="flex flex-col gap-2.5 p-0">
                <div className="flex items-start justify-between gap-3">
                  <p className="text-sm font-medium text-text-primary">{topic.name}</p>
                  <Badge sentiment={topic.dominant_sentiment === 'mixed' ? 'neutral' : topic.dominant_sentiment}>
                    {topic.dominant_sentiment}
                  </Badge>
                </div>
                <p className="text-sm leading-relaxed text-text-secondary">{topic.description}</p>
                <p className="text-xs text-text-muted">{topic.estimated_share}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
