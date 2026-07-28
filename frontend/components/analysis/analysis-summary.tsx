'use client';

import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { AnalysisOptionsState, Language } from './analysis-options';

const LANGUAGE_LABELS: Record<Language, string> = {
  auto: 'Auto Detect',
  ar: 'Arabic',
  en: 'English',
};

const OPTION_LABELS: { key: keyof AnalysisOptionsState; label: string }[] = [
  { key: 'keywordExtraction', label: 'Keyword Extraction' },
  { key: 'generateReport', label: 'Report Generation' },
];

export function AnalysisSummary({ options }: { options: AnalysisOptionsState }) {
  const enabledOptions = OPTION_LABELS.filter((o) => options[o.key] as boolean);

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <p className="text-sm font-medium text-text-muted">Summary</p>

        <div className="flex flex-col gap-2 text-sm">
          {}
          <div className="flex justify-between">
            <span className="text-text-secondary">Analysis Mode</span>
            <span className="text-text-primary capitalize">{options.mode === 'compare' ? 'Comparison' : 'Single Video'}</span>
          </div>

          {}
          <div className="flex justify-between">
            <span className="text-text-secondary">Max comments</span>
            <span className="text-text-primary">
              {options.analyzeAllComments ? 'All Comments' : options.maxComments.toLocaleString()}
            </span>
          </div>

          {}
          <div className="flex justify-between">
            <span className="text-text-secondary">Sorting Order</span>
            <span className="text-text-primary capitalize">{options.sortOrder === 'relevance' ? 'Top Relevant' : 'Newest First'}</span>
          </div>

          <div className="flex justify-between">
            <span className="text-text-secondary">Language</span>
            <span className="text-text-primary">{LANGUAGE_LABELS[options.language]}</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 border-t border-border-subtle pt-4">
          {}
          {options.includeReplies && (
            <Badge status="success">
              Include Replies
            </Badge>
          )}

          {enabledOptions.length > 0 ? (
            enabledOptions.map((o) => (
              <Badge key={o.key} status="info">
                {o.label}
              </Badge>
            ))
          ) : (
            !options.includeReplies && <p className="text-sm text-text-muted">No optional features enabled.</p>
          )}
        </div>
      </CardContent>
    </Card>
  );
}