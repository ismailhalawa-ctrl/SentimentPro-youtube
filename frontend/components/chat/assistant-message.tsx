import { Bot, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import { CitationBadge } from '@/components/chat/citation-badge';
import { ToolActivityIndicator } from '@/components/chat/tool-activity-indicator';
import type { AssistantMessage as AssistantMessageType } from '@/features/audience-assistant/types';

export function AssistantMessageBubble({ message }: { message: AssistantMessageType }) {
  const isUser = message.role === 'user';

  return (
    <div className={cn('flex gap-3', isUser && 'flex-row-reverse')}>
      <span
        className={cn(
          'flex h-8 w-8 shrink-0 items-center justify-center rounded-full',
          isUser ? 'bg-brand-500/20 text-brand-400' : 'bg-background-surface text-text-secondary'
        )}
      >
        {isUser ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
      </span>
      <div className={cn('flex max-w-[75%] flex-col gap-2', isUser && 'items-end')}>
        <div
          className={cn(
            'rounded-lg px-4 py-2.5 text-sm leading-relaxed',
            isUser ? 'bg-brand-500 text-text-primary' : 'bg-background-surface text-text-primary'
          )}
        >
          {message.content}
        </div>
        {message.citations_json.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {message.citations_json.map((citation) => (
              <CitationBadge key={`${citation.job_id}-${citation.comment_id}`} citation={citation} />
            ))}
          </div>
        )}
        {!isUser && <ToolActivityIndicator trace={message.tool_calls_json} />}
      </div>
    </div>
  );
}
