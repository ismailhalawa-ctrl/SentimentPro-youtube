import { ArrowRight, Filter } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import type { AnalysisJob } from '@/features/analysis/types';

export function CommentCleaningBanner({ job }: { job: AnalysisJob }) {
  const { total_fetched_comments, total_cleaned_comments } = job;

  if (total_fetched_comments == null || total_cleaned_comments == null) return null;

  const filteredOut = Math.max(0, total_fetched_comments - total_cleaned_comments);

  return (
    <Card variant="glass" className="p-4">
      <CardContent className="flex flex-wrap items-center gap-x-5 gap-y-2 p-0 text-sm">
        <div className="flex items-center gap-2 text-text-secondary">
          <Filter className="h-4 w-4 shrink-0 text-brand-400" />
          <span>
            <span className="font-semibold text-text-primary">{total_fetched_comments.toLocaleString()}</span>{' '}
            comments fetched
          </span>
        </div>
        <ArrowRight className="h-3.5 w-3.5 shrink-0 text-text-muted" />
        <div className="text-text-secondary">
          <span className="font-semibold text-text-primary">{total_cleaned_comments.toLocaleString()}</span>{' '}
          analyzed after cleaning
        </div>
        {filteredOut > 0 && (
          <span className="rounded-full bg-feedback-warning/10 px-2.5 py-1 text-xs font-medium text-feedback-warning">
            {filteredOut.toLocaleString()} filtered out as spam
          </span>
        )}
      </CardContent>
    </Card>
  );
}
