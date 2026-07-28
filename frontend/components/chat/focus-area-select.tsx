'use client';

import { Video } from 'lucide-react';
import { useLanguage } from '@/lib/i18n/language-provider';
import type { AnalysisJob } from '@/features/analysis/types';

interface FocusAreaSelectProps {
  jobs: AnalysisJob[];
  value: number | null;
  onChange: (jobId: number | null) => void;
  disabled?: boolean;
}

export function FocusAreaSelect({ jobs, value, onChange, disabled }: FocusAreaSelectProps) {
  const { t } = useLanguage();

  return (
    <label className="flex items-center gap-2 text-xs text-text-secondary">
      <Video className="h-3.5 w-3.5 shrink-0 text-text-muted" />
      <span className="shrink-0 font-medium">{t('audienceAssistant.focusArea.label')}</span>
      <select
        value={value ?? ''}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value ? Number(e.target.value) : null)}
        className="w-full max-w-[260px] truncate rounded-sm border border-border-default bg-background-surface px-2.5 py-1.5 text-xs text-text-primary transition-colors duration-150 focus:border-brand-400 disabled:cursor-not-allowed disabled:opacity-50"
      >
        <option value="">{t('audienceAssistant.focusArea.allVideos')}</option>
        {jobs.map((job) => (
          <option key={job.id} value={job.id}>
            {job.video_title || job.video_url}
          </option>
        ))}
      </select>
    </label>
  );
}
