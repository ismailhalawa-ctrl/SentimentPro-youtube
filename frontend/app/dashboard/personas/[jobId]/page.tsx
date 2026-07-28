'use client';

import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Activity, Loader2, Sparkles, Users } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { FeatureUnavailableCard } from '@/components/ai/feature-unavailable-card';
import { useAnalysisJobDetail } from '@/features/analysis/hooks/use-analysis-job-detail';
import { usePersonas } from '@/features/personas/hooks/use-personas';

export default function PersonasPage() {
  const params = useParams<{ jobId: string }>();
  const router = useRouter();
  const jobId = Number(params.jobId);

  const { job } = useAnalysisJobDetail(jobId);
  const { data, status, reason, isLoading } = usePersonas(jobId);

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
        <h1 className="text-2xl font-semibold text-text-primary">Personas</h1>
        <p className="mt-1 text-sm text-text-secondary">
          {job?.video_title ?? 'Viewer segments and behavior patterns for this audience.'}
        </p>
      </div>

      {isLoading ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Building audience personas…
          </CardContent>
        </Card>
      ) : status === 'unavailable' ? (
        <FeatureUnavailableCard reason={reason} />
      ) : status === 'error' || !data ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">
            {reason ?? 'Failed to build audience personas.'}
          </CardContent>
        </Card>
      ) : (
        <div className="flex flex-col gap-6">
          <Card variant="glass" className="p-5">
            <CardContent className="flex flex-col gap-3 p-0">
              <div className="flex items-center gap-2 text-sm font-medium text-text-primary">
                <Sparkles className="h-4 w-4 text-brand-400" />
                Audience personality
              </div>
              <p className="text-sm leading-relaxed text-text-secondary">{data.personality_profile}</p>
            </CardContent>
          </Card>

          {data.viewer_segments.length > 0 && (
            <div>
              <p className="mb-3 text-sm font-medium text-text-muted">Viewer segments</p>
              <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                {data.viewer_segments.map((segment, i) => (
                  <Card key={i} variant="glass" className="p-5">
                    <CardContent className="flex flex-col gap-2 p-0">
                      <div className="flex items-center justify-between gap-3">
                        <div className="flex items-center gap-2 text-sm font-medium text-text-primary">
                          <Users className="h-4 w-4 text-brand-400" />
                          {segment.name}
                        </div>
                        <span className="text-xs text-text-muted">{segment.estimated_share}</span>
                      </div>
                      <p className="text-sm leading-relaxed text-text-secondary">{segment.description}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>
          )}

          {data.behavior_notes.length > 0 && (
            <Card variant="glass" className="p-5">
              <CardContent className="flex flex-col gap-3 p-0">
                <div className="flex items-center gap-2 text-sm font-medium text-text-primary">
                  <Activity className="h-4 w-4 text-feedback-info" />
                  Behavior notes
                </div>
                <ul className="flex flex-col gap-2">
                  {data.behavior_notes.map((note, i) => (
                    <li key={i} className="text-sm text-text-secondary">
                      {note}
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
