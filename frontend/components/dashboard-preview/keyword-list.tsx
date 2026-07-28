import { Card, CardContent } from '@/components/ui/card';

const KEYWORDS = [
  'tutorial pacing',
  'error handling',
  'deployment',
  'clear explanation',
  'setup process',
  'audio quality',
  'follow-up request',
];

export function KeywordList() {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-3 p-0">
        <p className="text-sm font-medium text-text-muted">Extracted Keywords</p>
        <div className="flex flex-wrap gap-2">
          {KEYWORDS.map((keyword) => (
            <span
              key={keyword}
              className="rounded-full border border-border-default bg-background-surface px-3 py-1 text-xs text-text-secondary"
            >
              {keyword}
            </span>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}