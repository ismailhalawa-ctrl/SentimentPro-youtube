'use client';

import { useState } from 'react';
import { CheckCircle2, ChevronDown, ChevronRight, Wrench, XCircle } from 'lucide-react';
import { cn } from '@/lib/utils';
import type { ToolCallTrace } from '@/features/audience-assistant/types';

const TOOL_LABELS: Record<string, string> = {
  list_my_jobs: 'Checked your analyzed videos',
  get_video_metadata: 'Looked up video details',
  get_job_sentiment_summary: 'Checked sentiment breakdown',
  get_job_health_scores: 'Checked audience health scores',
  get_rule_based_highlights: 'Checked quick highlights',
  get_job_language_breakdown: 'Checked language distribution',
  search_comments: 'Searched comments',
};

function describeTool(step: ToolCallTrace): string {
  const label = TOOL_LABELS[step.tool] ?? step.tool;
  const jobId = step.arguments?.job_id;
  if (typeof jobId !== 'number' && typeof jobId !== 'string') return label;
  return `${label} (video #${Math.trunc(Number(jobId))})`;
}

export function ToolActivityIndicator({ trace }: { trace: ToolCallTrace[] | null | undefined }) {
  const [expanded, setExpanded] = useState(false);

  if (!trace || trace.length === 0) return null;

  return (
    <div className="mt-1 max-w-full text-xs text-text-muted">
      <button
        type="button"
        onClick={() => setExpanded((prev) => !prev)}
        className="flex items-center gap-1 rounded-sm px-1 py-0.5 hover:text-text-secondary"
      >
        {expanded ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
        <Wrench className="h-3 w-3" />
        {trace.length === 1 ? '1 tool used' : `${trace.length} tools used`}
      </button>
      {expanded && (
        <ul className="mt-1 flex flex-col gap-1 border-l border-border-subtle pl-3">
          {trace.map((step, index) => (
            <li key={index} className="flex items-start gap-1.5">
              {step.status === 'success' ? (
                <CheckCircle2 className="mt-0.5 h-3 w-3 shrink-0 text-feedback-success" />
              ) : (
                <XCircle className="mt-0.5 h-3 w-3 shrink-0 text-feedback-danger" />
              )}
              <span className={cn(step.status === 'error' && 'text-feedback-danger')}>
                {describeTool(step)}
                {step.status === 'error' && ` — ${step.result_summary}`}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
