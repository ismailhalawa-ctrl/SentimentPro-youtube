import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

const COMMENTS: { text: string; sentiment: 'positive' | 'neutral' | 'negative' }[] = [
  { text: 'This explanation finally made it click for me!', sentiment: 'positive' },
  { text: 'Could you cover the edge cases too?', sentiment: 'neutral' },
  { text: 'Audio was a bit quiet in part 2.', sentiment: 'negative' },
];

export function RecentCommentsCard() {
  return (
    <Card variant="glass" className="p-4">
      <CardContent className="flex flex-col gap-3 p-0">
        <p className="text-xs font-medium text-text-muted">Recent Comments</p>
        {COMMENTS.map((comment, i) => (
          <div key={i} className="flex items-center justify-between gap-3">
            <p className="truncate text-sm text-text-secondary">{comment.text}</p>
            <Badge sentiment={comment.sentiment} className="shrink-0">
              {comment.sentiment}
            </Badge>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}