'use client';

import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, HelpCircle, Loader2, MessageCircleQuestion } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FeatureUnavailableCard } from '@/components/ai/feature-unavailable-card';
import { useAnalysisJobDetail } from '@/features/analysis/hooks/use-analysis-job-detail';
import { useFAQs } from '@/features/faqs/hooks/use-faqs';

export default function FAQsPage() {
  const params = useParams<{ jobId: string }>();
  const router = useRouter();
  const jobId = Number(params.jobId);

  const { job } = useAnalysisJobDetail(jobId);
  const { data, status, reason, isLoading } = useFAQs(jobId);

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
        <h1 className="text-2xl font-semibold text-text-primary">FAQs</h1>
        <p className="mt-1 text-sm text-text-secondary">
          {job?.video_title ?? 'Questions viewers repeatedly ask about this video.'}
        </p>
      </div>

      {isLoading ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Generating FAQs…
          </CardContent>
        </Card>
      ) : status === 'unavailable' ? (
        <FeatureUnavailableCard reason={reason} />
      ) : status === 'error' || !data ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">
            {reason ?? 'Failed to generate FAQs.'}
          </CardContent>
        </Card>
      ) : data.faqs.length === 0 ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <HelpCircle className="h-4 w-4" />
            No recurring questions were found in this job&apos;s comments.
          </CardContent>
        </Card>
      ) : (
        <div className="flex flex-col gap-4">
          {data.faqs.map((faq, i) => (
            <Card key={i} variant="glass" className="p-5">
              <CardContent className="flex flex-col gap-2.5 p-0">
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-start gap-2.5">
                    <MessageCircleQuestion className="mt-0.5 h-4 w-4 shrink-0 text-brand-400" />
                    <p className="text-sm font-medium text-text-primary">{faq.question}</p>
                  </div>
                  {faq.times_asked_estimate > 0 && (
                    <Badge status="info" className="shrink-0">
                      ~{faq.times_asked_estimate}× asked
                    </Badge>
                  )}
                </div>
                <p className="pl-6.5 text-sm leading-relaxed text-text-secondary">{faq.answer}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
