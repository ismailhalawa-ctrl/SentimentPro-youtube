'use client';

import { useEffect, useMemo, useState } from 'react';
import { ChevronLeft, ChevronRight, Search } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { colors } from '@/styles/design-tokens';
import { sanitizeCommentText } from '@/lib/sanitize-comment-text';
import { useDebouncedValue } from '@/lib/use-debounced-value';
import type { CommentEntry, CommentLanguage, CommentSentiment } from '@/features/analysis/types';

interface CommentsExplorerProps {
  comments: CommentEntry[];
}

type SentimentFilter = 'all' | CommentSentiment;
type LanguageFilter = 'all' | CommentLanguage;
type SpamFilter = 'all' | 'clean' | 'spam';

const PAGE_SIZE = 100;
const SEARCH_DEBOUNCE_MS = 300;

const LANGUAGE_LABELS: Record<CommentLanguage, string> = {
  ar: 'Arabic',
  en: 'English',
  mixed: 'Mixed',
  other: 'Other',
};

function selectClass() {
  return 'w-full rounded-sm border border-border-default bg-background-surface px-3 py-2 text-sm text-text-primary transition-colors duration-150 focus:border-brand-400';
}

export function CommentsExplorer({ comments }: CommentsExplorerProps) {
  const [sentimentFilter, setSentimentFilter] = useState<SentimentFilter>('all');
  const [languageFilter, setLanguageFilter] = useState<LanguageFilter>('all');
  const [spamFilter, setSpamFilter] = useState<SpamFilter>('all');
  const [minLikes, setMinLikes] = useState(0);
  const [minConfidence, setMinConfidence] = useState(0);
  const [search, setSearch] = useState('');
  const debouncedSearch = useDebouncedValue(search, SEARCH_DEBOUNCE_MS);
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    const query = debouncedSearch.trim().toLowerCase();
    return comments.filter((c) => {
      if (sentimentFilter !== 'all' && c.sentiment !== sentimentFilter) return false;
      if (languageFilter !== 'all' && c.language !== languageFilter) return false;
      if (spamFilter === 'clean' && c.is_spam) return false;
      if (spamFilter === 'spam' && !c.is_spam) return false;
      if (c.likes < minLikes) return false;
      if ((c.confidence ?? 0) < minConfidence) return false;
      if (query && !c.text.toLowerCase().includes(query)) return false;
      return true;
    });
  }, [comments, sentimentFilter, languageFilter, spamFilter, minLikes, minConfidence, debouncedSearch]);

  useEffect(() => {
    setPage(1);
  }, [sentimentFilter, languageFilter, spamFilter, minLikes, minConfidence, debouncedSearch]);

  const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const currentPage = Math.min(page, pageCount);
  const visible = filtered.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);

  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0">
        <p className="text-sm font-medium text-text-muted">Filter Options</p>

        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-5">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-text-secondary">Sentiment</label>
            <select
              value={sentimentFilter}
              onChange={(e) => setSentimentFilter(e.target.value as SentimentFilter)}
              className={selectClass()}
            >
              <option value="all">All</option>
              <option value="positive">Positive</option>
              <option value="negative">Negative</option>
              <option value="neutral">Neutral</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-text-secondary">Language</label>
            <select
              value={languageFilter}
              onChange={(e) => setLanguageFilter(e.target.value as LanguageFilter)}
              className={selectClass()}
            >
              <option value="all">All</option>
              <option value="ar">Arabic</option>
              <option value="en">English</option>
              <option value="mixed">Mixed</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-text-secondary">Spam</label>
            <select
              value={spamFilter}
              onChange={(e) => setSpamFilter(e.target.value as SpamFilter)}
              className={selectClass()}
            >
              <option value="all">All</option>
              <option value="clean">No Spam</option>
              <option value="spam">Spam Only</option>
            </select>
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-text-secondary">Min Likes</label>
            <Input
              type="number"
              min={0}
              value={minLikes}
              onChange={(e) => setMinLikes(Math.max(0, Number(e.target.value)))}
            />
          </div>

          <div className="flex flex-col gap-1.5">
            <label className="text-xs font-medium text-text-secondary">
              Min Confidence — {Math.round(minConfidence * 100)}%
            </label>
            <input
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={minConfidence}
              onChange={(e) => setMinConfidence(Number(e.target.value))}
              className="mt-2.5 w-full accent-brand-500"
            />
          </div>
        </div>

        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" />
          <Input
            type="text"
            placeholder="Search comments…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>

        <div className="flex flex-wrap items-center justify-center gap-2 rounded-md bg-brand-500/15 px-4 py-2 text-center text-sm">
          <span className="font-medium text-brand-400">
            Showing {visible.length === 0 ? 0 : (currentPage - 1) * PAGE_SIZE + 1}–
            {(currentPage - 1) * PAGE_SIZE + visible.length} of {filtered.length.toLocaleString()} matching comments
          </span>
          <span className="text-text-muted">(total: {comments.length.toLocaleString()})</span>
        </div>

        <div className="max-h-[600px] overflow-auto rounded-md border border-border-subtle">
          <table className="w-full text-left text-sm">
            <thead className="sticky top-0 bg-background-surface">
              <tr className="border-b border-border-subtle text-xs uppercase tracking-wide text-text-muted">
                <th className="px-3 py-2.5 font-medium">Author</th>
                <th className="px-3 py-2.5 font-medium">Comment</th>
                <th className="px-3 py-2.5 font-medium">Sentiment</th>
                <th className="px-3 py-2.5 font-medium">Confidence</th>
                <th className="px-3 py-2.5 font-medium">Language</th>
                <th className="px-3 py-2.5 font-medium">Likes</th>
                <th className="px-3 py-2.5 font-medium">Spam</th>
                <th className="px-3 py-2.5 font-medium">Sarcasm</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle">
              {visible.map((c) => (
                <tr key={c.id} className="align-top hover:bg-background-surface/60">
                  <td className="max-w-[120px] truncate px-3 py-2.5 text-text-secondary">{c.author}</td>
                  <td className="max-w-sm px-3 py-2.5 text-text-primary">
                    <span className="line-clamp-2">{sanitizeCommentText(c.text)}</span>
                  </td>
                  <td className="px-3 py-2.5">
                    {c.sentiment ? <Badge sentiment={c.sentiment}>{c.sentiment}</Badge> : '—'}
                  </td>
                  <td className="px-3 py-2.5 tabular-nums text-text-secondary">
                    {c.confidence !== null ? `${Math.round(c.confidence * 100)}%` : '—'}
                  </td>
                  <td className="px-3 py-2.5 text-text-secondary">
                    {c.language ? LANGUAGE_LABELS[c.language] : '—'}
                  </td>
                  <td className="px-3 py-2.5 tabular-nums text-text-secondary">{c.likes.toLocaleString()}</td>
                  <td className="px-3 py-2.5">
                    {c.is_spam ? (
                      <span style={{ color: colors.feedback.warning }}>Yes</span>
                    ) : (
                      <span className="text-text-muted">No</span>
                    )}
                  </td>
                  <td className="px-3 py-2.5">
                    {c.is_sarcasm ? (
                      <span className="text-brand-400">Yes</span>
                    ) : (
                      <span className="text-text-muted">No</span>
                    )}
                  </td>
                </tr>
              ))}
              {visible.length === 0 && (
                <tr>
                  <td colSpan={8} className="px-3 py-10 text-center text-text-muted">
                    No comments match these filters.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        {pageCount > 1 && (
          <div className="flex items-center justify-center gap-3">
            <Button
              variant="secondary"
              size="sm"
              disabled={currentPage <= 1}
              onClick={() => setPage((p) => Math.max(1, p - 1))}
            >
              <ChevronLeft className="h-3.5 w-3.5" /> Previous
            </Button>
            <span className="text-sm text-text-secondary">
              Page {currentPage} of {pageCount}
            </span>
            <Button
              variant="secondary"
              size="sm"
              disabled={currentPage >= pageCount}
              onClick={() => setPage((p) => Math.min(pageCount, p + 1))}
            >
              Next <ChevronRight className="h-3.5 w-3.5" />
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
