'use client';

import { motion } from 'framer-motion';
import { Ban, CheckCircle2, Loader2, XCircle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import type { AnalysisJob } from '@/features/analysis/types';

interface AnalysisProgressProps {
  job: AnalysisJob;
  label: string;
  onCancel?: () => void;
  isCancelling?: boolean;
}

export function AnalysisProgress({ job, label, onCancel, isCancelling }: AnalysisProgressProps) {
  const isFailed = job.status === 'failed';
  const isCancelled = job.status === 'cancelled';
  const isRunning = job.status === 'pending' || job.status === 'processing';

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <div className="flex items-center justify-between">
          <p className="text-sm font-medium text-text-muted">{label}</p>
          <span className="text-sm font-medium text-text-primary">{job.progress_percentage}%</span>
        </div>

        <div className="h-2 w-full overflow-hidden rounded-full bg-background-elevated">
          <motion.div
            className={cn(
              'h-full rounded-full',
              isFailed || isCancelled ? 'bg-feedback-danger' : 'bg-gradient-brand'
            )}
            initial={{ width: 0 }}
            animate={{ width: `${job.progress_percentage}%` }}
            transition={{ duration: 0.4, ease: 'easeOut' }}
          />
        </div>

        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            {isFailed ? (
              <XCircle className="h-4 w-4 shrink-0 text-feedback-danger" />
            ) : isCancelled ? (
              <Ban className="h-4 w-4 shrink-0 text-feedback-danger" />
            ) : job.status === 'completed' ? (
              <CheckCircle2 className="h-4 w-4 shrink-0 text-sentiment-positive" />
            ) : (
              <Loader2 className="h-4 w-4 shrink-0 animate-spin text-brand-400" />
            )}
            <span className={cn('text-sm', (isFailed || isCancelled) && 'text-feedback-danger', !isFailed && !isCancelled && 'text-text-primary')}>
              {isFailed
                ? job.error_message || 'Analysis failed.'
                : isCancelled
                  ? 'Analysis cancelled.'
                  : job.current_step || 'Starting…'}
            </span>
          </div>

          {isRunning && onCancel && (
            <Button variant="destructive" size="sm" onClick={onCancel} isLoading={isCancelling}>
              <Ban className="h-3.5 w-3.5" /> Cancel Analysis
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
