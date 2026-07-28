import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface Comment {
  text: string;
  sentiment: 'positive' | 'neutral' | 'negative';
  confidence: number;
}

const COMMENTS: Comment[] = [
  { text: 'This tutorial saved me hours of debugging, thank you!', sentiment: 'positive', confidence: 0.96 },
  { text: 'Could you do a follow-up on deployment?', sentiment: 'neutral', confidence: 0.81 },
  { text: 'The pacing in the middle section was too fast.', sentiment: 'negative', confidence: 0.88 },
  { text: 'Best explanation of this topic on YouTube.', sentiment: 'positive', confidence: 0.94 },
];

export function CommentTable() {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <p className="text-sm font-medium text-text-muted">Recent Comments</p>
        <div className="flex flex-col divide-y divide-border-subtle">
          {COMMENTS.map((comment, i) => (
            <div key={i} className="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0">
              <p className="truncate text-sm text-text-secondary">{comment.text}</p>
              <div className="flex shrink-0 items-center gap-2">
                <span className="text-xs text-text-muted">{Math.round(comment.confidence * 100)}%</span>
                <Badge sentiment={comment.sentiment}>{comment.sentiment}</Badge>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}