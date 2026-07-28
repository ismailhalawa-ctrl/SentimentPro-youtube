'use client';

import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, Heart, Loader2, Rocket, ShieldCheck, TrendingUp } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { useAnalysisJobDetail } from '@/features/analysis/hooks/use-analysis-job-detail';
import { useAudienceIntelligence } from '@/features/audience-intelligence/hooks/use-audience-intelligence';
import { colors } from '@/styles/design-tokens';

const RADIUS = 42;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

function tierColor(score: number): string {
  if (score >= 70) return colors.feedback.success;
  if (score >= 40) return colors.feedback.warning;
  return colors.feedback.danger;
}

function ScoreGauge({ label, score, icon }: { label: string; score: number; icon: React.ReactNode }) {
  const clamped = Math.max(0, Math.min(100, score));
  const offset = CIRCUMFERENCE - (clamped / 100) * CIRCUMFERENCE;
  const color = tierColor(clamped);

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col items-center gap-3 p-0">
        <div className="relative h-28 w-28">
          <svg viewBox="0 0 100 100" className="h-28 w-28 -rotate-90">
            <circle
              cx="50"
              cy="50"
              r={RADIUS}
              fill="none"
              stroke={colors.background.surface}
              strokeWidth="8"
            />
            <circle
              cx="50"
              cy="50"
              r={RADIUS}
              fill="none"
              stroke={color}
              strokeWidth="8"
              strokeLinecap="round"
              strokeDasharray={CIRCUMFERENCE}
              strokeDashoffset={offset}
              style={{ transition: 'stroke-dashoffset 0.6s ease' }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className="text-2xl font-semibold text-text-primary" style={{ fontVariantNumeric: 'tabular-nums' }}>
              {Math.round(clamped)}
            </span>
            <span className="text-xs text-text-muted">/ 100</span>
          </div>
        </div>
        <div className="flex items-center gap-1.5 text-sm font-medium text-text-primary">
          {icon}
          {label}
        </div>
      </CardContent>
    </Card>
  );
}

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

export default function AudienceIntelligencePage() {
  const params = useParams<{ jobId: string }>();
  const router = useRouter();
  const jobId = Number(params.jobId);

  const { job } = useAnalysisJobDetail(jobId);
  const { data, status, reason, isLoading } = useAudienceIntelligence(jobId);

  if (!Number.isFinite(jobId)) {
    router.replace('/dashboard/history');
    return null;
  }

  const hasScores = status === 'ok' || status === 'partial';

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
        <h1 className="text-2xl font-semibold text-text-primary">Audience Intelligence</h1>
        <p className="mt-1 text-sm text-text-secondary">
          {job?.video_title ?? 'Composite scores and growth signals for this audience.'}
        </p>
      </div>

      {isLoading ? (
        <Card variant="glass" className="p-5">
          <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
            <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
            Computing audience intelligence…
          </CardContent>
        </Card>
      ) : status === 'error' || !data ? (
        <Card variant="glass" className="border-feedback-danger/30 p-5">
          <CardContent className="p-0 text-sm text-feedback-danger">
            {reason ?? 'Failed to compute audience intelligence.'}
          </CardContent>
        </Card>
      ) : (
        <div className="flex flex-col gap-6">
          {hasScores && (
            <div>
              <p className="mb-3 text-xs text-text-muted">
                Deterministic scores computed from this job&apos;s data — always available, no AI
                provider required. The Loyalty Score is a single-video engagement-depth proxy (comment
                length, tenure language, engagement), not true cross-video loyalty history.
              </p>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                <ScoreGauge
                  label="Satisfaction"
                  score={data.scores.satisfaction_score}
                  icon={<Heart className="h-4 w-4 text-sentiment-positive" />}
                />
                <ScoreGauge
                  label="Community Health"
                  score={data.scores.community_health_score}
                  icon={<ShieldCheck className="h-4 w-4 text-feedback-info" />}
                />
                <ScoreGauge
                  label="Loyalty (proxy)"
                  score={data.scores.loyalty_score}
                  icon={<TrendingUp className="h-4 w-4 text-brand-400" />}
                />
              </div>
            </div>
          )}

          {status === 'partial' ? (
            <Card variant="glass" className="p-5">
              <CardContent className="flex items-start gap-3 p-0">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-brand-500/15 text-brand-400">
                  <Rocket className="h-4.5 w-4.5" />
                </span>
                <div className="flex flex-col gap-1">
                  <p className="text-sm font-medium text-text-primary">
                    Emerging trends and growth opportunities aren&apos;t enabled yet
                  </p>
                  <p className="text-sm text-text-secondary">
                    {reason ?? 'This narrative layer requires an AI provider API key to be configured on the server.'}
                  </p>
                </div>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
              <ListSection
                icon={<TrendingUp className="h-4 w-4 text-brand-400" />}
                label="Emerging trends"
                items={data.emerging_trends}
              />
              <ListSection
                icon={<Rocket className="h-4 w-4 text-feedback-success" />}
                label="Growth opportunities"
                items={data.growth_opportunities}
              />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
