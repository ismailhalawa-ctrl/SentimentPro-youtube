'use client';

import { useState } from 'react';
import { MessageSquareQuote } from 'lucide-react';
import type { AssistantCitation } from '@/features/audience-assistant/types';

export function CitationBadge({ citation }: { citation: AssistantCitation }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative inline-block">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="inline-flex items-center gap-1 rounded-sm bg-brand-500/15 px-2 py-0.5 text-xs font-medium text-brand-400 hover:bg-brand-500/25"
      >
        <MessageSquareQuote className="h-3 w-3" />
        {citation.author}
      </button>
      {open && (
        <div className="absolute z-10 mt-1.5 w-64 rounded-md border border-border-default bg-background-elevated p-3 text-left shadow-md">
          <p className="text-xs leading-relaxed text-text-secondary">{citation.text}</p>
          <p className="mt-1.5 text-[11px] text-text-muted">
            {citation.author} · {citation.like_count} likes
          </p>
        </div>
      )}
    </div>
  );
}
