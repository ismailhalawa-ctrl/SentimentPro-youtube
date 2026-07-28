'use client';

import { useMemo, useState } from 'react';
import { Heart, Smile, Frown, ThumbsUp } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { cn } from '@/lib/utils';
import { sanitizeCommentText } from '@/lib/sanitize-comment-text';
import type { CommentEntry } from '@/features/analysis/types';

interface TopCommentsPanelProps {
  comments: CommentEntry[];
}

const TABS = [
  { key: 'positive', label: 'Top Positive', icon: Smile },
  { key: 'negative', label: 'Top Negative', icon: Frown },
  { key: 'liked', label: 'Most Liked', icon: ThumbsUp },
] as const;
type TabKey = (typeof TABS)[number]['key'];

function CommentCard({ comment }: { comment: CommentEntry }) {
  const borderColor =
    comment.sentiment === 'positive'
      ? 'border-l-sentiment-positive'
      : comment.sentiment === 'negative'
        ? 'border-l-sentiment-negative'
        : 'border-l-sentiment-neutral';

  return (
    <div className={cn('border-l-4 rounded-r-md bg-background-surface/60 px-4 py-3', borderColor)}>
      <p className="text-xs font-medium text-text-secondary">{comment.author}</p>
      <p className="mt-1 text-sm text-text-primary">{sanitizeCommentText(comment.text)}</p>
      <p className="mt-2 text-xs text-text-muted">
        <Heart className="mr-1 inline h-3 w-3" />
        {comment.likes.toLocaleString()} likes
        {comment.confidence !== null && ` · ${Math.round(comment.confidence * 100)}% confidence`}
      </p>
    </div>
  );
}

export function TopCommentsPanel({ comments }: TopCommentsPanelProps) {
  const [activeTab, setActiveTab] = useState<TabKey>('positive');

  const lists = useMemo(() => {
    const clean = comments.filter((c) => !c.is_spam);
    return {
      positive: [...clean.filter((c) => c.sentiment === 'positive')].sort((a, b) => b.likes - a.likes).slice(0, 10),
      negative: [...clean.filter((c) => c.sentiment === 'negative')].sort((a, b) => b.likes - a.likes).slice(0, 10),
      liked: [...clean].sort((a, b) => b.likes - a.likes).slice(0, 10),
    };
  }, [comments]);

  const activeList = lists[activeTab];

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <p className="text-sm font-medium text-text-muted">Top Comments</p>

        <div className="flex gap-1 rounded-md bg-background-surface p-1">
          {TABS.map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setActiveTab(key)}
              className={cn(
                'flex flex-1 items-center justify-center gap-1.5 rounded-sm px-3 py-2 text-sm font-medium transition-colors',
                activeTab === key
                  ? 'bg-brand-500 text-text-primary'
                  : 'text-text-secondary hover:text-text-primary'
              )}
            >
              <Icon className="h-3.5 w-3.5" />
              {label}
            </button>
          ))}
        </div>

        <div className="flex flex-col gap-2.5">
          {activeList.length === 0 ? (
            <p className="py-8 text-center text-sm text-text-muted">No comments found for this category.</p>
          ) : (
            activeList.map((comment) => <CommentCard key={comment.id} comment={comment} />)
          )}
        </div>
      </CardContent>
    </Card>
  );
}
