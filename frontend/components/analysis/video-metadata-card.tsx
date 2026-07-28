import { Eye, ThumbsUp, MessageSquareText, Calendar, ShieldAlert } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { VideoInfo } from '../../features/youtube/types';

function formatCount(count: number): string {
  if (count >= 1_000_000) return `${(count / 1_000_000).toFixed(1)}M`;
  if (count >= 1_000) return `${(count / 1_000).toFixed(1)}K`;
  return count.toLocaleString();
}

function formatDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  } catch {
    return iso;
  }
}

export function VideoMetadataCard({ video }: { video: VideoInfo }) {
  return (
    <Card variant="glass" className="p-5">
      <CardContent className="flex flex-col gap-4 p-0 sm:flex-row">
        <div className="h-32 w-full shrink-0 overflow-hidden rounded-md border border-border-subtle bg-background-surface sm:w-48">
          {video.thumbnail_url ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={video.thumbnail_url}
              alt={video.title}
              className="h-full w-full object-cover"
            />
          ) : null}
        </div>

        <div className="flex flex-1 flex-col justify-center gap-1.5">
          <p className="text-sm font-semibold text-text-primary">{video.title}</p>
          <p className="text-sm text-text-secondary">{video.channel_title}</p>

          <div className="mt-1 flex flex-wrap items-center gap-4 text-xs text-text-muted">
            <span className="flex items-center gap-1.5">
              <Calendar className="h-3.5 w-3.5" />
              {formatDate(video.published_at)}
            </span>
            <span className="flex items-center gap-1.5">
              <Eye className="h-3.5 w-3.5" />
              {formatCount(video.view_count)} views
            </span>
            <span className="flex items-center gap-1.5">
              <ThumbsUp className="h-3.5 w-3.5" />
              {formatCount(video.like_count)}
            </span>
            <span className="flex items-center gap-1.5">
              <MessageSquareText className="h-3.5 w-3.5" />
              {formatCount(video.comment_count)} comments
            </span>
          </div>

          {(!video.comments_enabled || video.region_restricted) && (
            <div className="mt-1 flex flex-wrap gap-2">
              {!video.comments_enabled && (
                <Badge status="warning">
                  <ShieldAlert className="mr-1 h-3 w-3" />
                  Comments disabled
                </Badge>
              )}
              {video.region_restricted && <Badge status="warning">Region restricted</Badge>}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
