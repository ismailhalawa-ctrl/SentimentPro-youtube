'use client';

import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Lightbulb, Wrench } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ExtractionLoadingCard } from '@/components/ai/extraction-loading-card';
import { FeatureUnavailableCard } from '@/components/ai/feature-unavailable-card';
import { useAnalysisJobDetail } from '@/features/analysis/hooks/use-analysis-job-detail';
import { useSuggestions } from '@/features/suggestions/hooks/use-suggestions';
import type { ExtractedCommentItem } from '@/features/suggestions/types';

function SuggestionCard({ item, statusVariant }: { item: ExtractedCommentItem; statusVariant: 'info' | 'success' }) {
  return (
    <Card variant="glass" className="p-4">
      <CardContent className="flex flex-col gap-2 p-0">
        {item.category && (
          <Badge status={statusVariant} className="w-fit">
            {item.category}
          </Badge>
        )}
        <p className="text-sm leading-relaxed text-text-secondary">{item.text}</p>
      </CardContent>
    </Card>
  );
}

export default function SuggestionsPage() {
  const params = useParams<{ jobId: string }>();
  const router = useRouter();
  const jobId = Number(params.jobId);

  const { job } = useAnalysisJobDetail(jobId);
  const { data, status, reason, isLoading } = useSuggestions(jobId);

  if (!Number.isFinite(jobId)) {
    router.replace('/dashboard/history');
    return null;
  }

  const featureRequests = data?.items.filter((item) => item.is_feature_request) ?? [];
  const contentSuggestions = data?.items.filter((item) => !item.is_feature_request) ?? [];

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
        <h1 className="text-2xl font-semibold text-text-primary">Suggestions</h1>
        <p className="mt-1 text-sm text-text-secondary">
          {job?.video_title ?? 'Content ideas and feature requests viewers proposed.'}
        </p>
      </div>

      {isLoading ? (
        <ExtractionLoadingCard label="Mining suggestions…" />
      ) : status === 'unavailable' ? (
        <FeatureUnavailableCard reason={reason} />
      ) : status === 'error' || !data ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">
            {reason ?? 'Failed to mine suggestions.'}
          </CardContent>
        </Card>
      ) : data.items.length === 0 ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Lightbulb className="h-4 w-4" />
            No specific suggestions were found in this job&apos;s comments.
          </CardContent>
        </Card>
      ) : (
        <div className="flex flex-col gap-6">
          <Card variant="glass" className="p-5">
            <CardContent className="flex flex-col gap-3 p-0">
              <p className="text-sm font-medium text-text-muted">Top suggestion categories</p>
              <div className="flex flex-col gap-2.5">
                {data.ranked_categories.slice(0, 8).map((cat) => (
                  <div key={cat.category} className="flex items-center gap-3">
                    <span className="w-40 shrink-0 truncate text-sm text-text-primary" title={cat.category}>
                      {cat.category}
                    </span>
                    <div className="h-2 flex-1 overflow-hidden rounded-full bg-background-surface">
                      <div
                        className="h-full rounded-full bg-brand-400"
                        style={{
                          width: `${Math.max(4, (cat.count / data.ranked_categories[0].count) * 100)}%`,
                        }}
                      />
                    </div>
                    <span className="w-8 shrink-0 text-right text-xs text-text-muted">{cat.count}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {featureRequests.length > 0 && (
            <div className="flex flex-col gap-3">
              <div className="flex items-center gap-2 text-sm font-medium text-text-primary">
                <Wrench className="h-4 w-4 text-feedback-info" />
                Feature requests ({featureRequests.length})
              </div>
              {featureRequests.slice(0, 100).map((item) => (
                <SuggestionCard key={item.comment_id} item={item} statusVariant="info" />
              ))}
            </div>
          )}

          {contentSuggestions.length > 0 && (
            <div className="flex flex-col gap-3">
              <div className="flex items-center gap-2 text-sm font-medium text-text-primary">
                <Lightbulb className="h-4 w-4 text-feedback-success" />
                Content suggestions ({contentSuggestions.length})
              </div>
              {contentSuggestions.slice(0, 100).map((item) => (
                <SuggestionCard key={item.comment_id} item={item} statusVariant="success" />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
