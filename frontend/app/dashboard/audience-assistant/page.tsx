'use client';

import { Suspense, useEffect, useRef, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { Bot, Loader2, MessageSquarePlus, Sparkles, Trash2 } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ConfirmModal } from '@/components/ui/confirm-modal';
import { AssistantMessageBubble } from '@/components/chat/assistant-message';
import { ChatInput } from '@/components/chat/chat-input';
import { FocusAreaSelect } from '@/components/chat/focus-area-select';
import { useAudienceAssistant } from '@/features/audience-assistant/hooks/use-audience-assistant';
import { cn } from '@/lib/utils';
import type { AssistantSession } from '@/features/audience-assistant/types';

const SUGGESTED_PROMPTS = [
  'What are the most common complaints across my channel?',
  'Compare my last two videos.',
  'Give me content strategy advice based on my audience.',
  'Which of my videos has the healthiest comment section?',
];

function formatSessionDate(iso: string): string {
  try {
    return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  } catch {
    return iso;
  }
}

function SessionListItem({
  session,
  isActive,
  onSelect,
  onRequestDelete,
}: {
  session: AssistantSession;
  isActive: boolean;
  onSelect: () => void;
  onRequestDelete: () => void;
}) {
  return (
    <div
      className={cn(
        'group flex items-center gap-1 rounded-md px-3 py-2.5 text-sm transition-colors',
        isActive
          ? 'bg-brand-500/15 text-brand-400'
          : 'text-text-secondary hover:bg-background-elevated hover:text-text-primary'
      )}
    >
      <button type="button" onClick={onSelect} className="min-w-0 flex-1 text-left">
        <p className="truncate font-medium">{session.title || 'New conversation'}</p>
        <p className="text-xs text-text-muted">{formatSessionDate(session.updated_at)}</p>
      </button>
      <button
        type="button"
        onClick={onRequestDelete}
        aria-label="Delete conversation"
        className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md text-text-muted opacity-0 transition-opacity hover:bg-feedback-danger/10 hover:text-feedback-danger group-hover:opacity-100"
      >
        <Trash2 className="h-3.5 w-3.5" />
      </button>
    </div>
  );
}

export default function AudienceAssistantPage() {
  return (
    <Suspense fallback={<AudienceAssistantFallback />}>
      <AudienceAssistantView />
    </Suspense>
  );
}

function AudienceAssistantFallback() {
  return (
    <div className="flex h-[calc(100vh-8rem)] items-center justify-center">
      <Loader2 className="h-5 w-5 animate-spin text-brand-400" />
    </div>
  );
}

function AudienceAssistantView() {
  const {
    sessions,
    isLoadingSessions,
    sessionsError,
    activeSessionId,
    messages,
    isLoadingMessages,
    sessionError,
    isSending,
    sendError,
    startNewSession,
    selectSession,
    removeSession,
    send,
    focusableJobs,
    focusJobId,
    setFocusJobId,
    focusOnJob,
  } = useAudienceAssistant();

  const searchParams = useSearchParams();
  const appliedJobIdParam = useRef(false);

  const [deleteTarget, setDeleteTarget] = useState<AssistantSession | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    if (appliedJobIdParam.current) return;
    const jobIdParam = searchParams.get('jobId');
    if (!jobIdParam) return;
    const jobId = Number(jobIdParam);
    if (!Number.isFinite(jobId)) return;

    appliedJobIdParam.current = true;
    void focusOnJob(jobId);
  }, [searchParams, focusOnJob]);

  const focusedJob = focusableJobs.find((job) => job.id === focusJobId) ?? null;

  async function handleConfirmDelete() {
    if (!deleteTarget) return;
    setIsDeleting(true);
    await removeSession(deleteTarget.id);
    setIsDeleting(false);
    setDeleteTarget(null);
  }

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-6">
      <Card variant="glass" className="hidden w-72 shrink-0 flex-col overflow-hidden p-0 md:flex">
        <div className="border-b border-border-subtle p-4">
          <Button variant="secondary" size="sm" className="w-full" onClick={() => void startNewSession()}>
            <MessageSquarePlus className="h-3.5 w-3.5" /> New Chat
          </Button>
        </div>
        <div className="flex-1 overflow-y-auto p-2">
          {isLoadingSessions ? (
            <div className="flex items-center justify-center gap-2 p-4 text-xs text-text-secondary">
              <Loader2 className="h-3.5 w-3.5 animate-spin" /> Loading…
            </div>
          ) : sessionsError ? (
            <p className="p-3 text-xs text-feedback-danger">{sessionsError}</p>
          ) : sessions.length === 0 ? (
            <p className="p-3 text-xs text-text-muted">No conversations yet — start one below.</p>
          ) : (
            <div className="flex flex-col gap-0.5">
              {sessions.map((session) => (
                <SessionListItem
                  key={session.id}
                  session={session}
                  isActive={session.id === activeSessionId}
                  onSelect={() => void selectSession(session.id)}
                  onRequestDelete={() => setDeleteTarget(session)}
                />
              ))}
            </div>
          )}
        </div>
      </Card>

      <Card variant="glass" className="flex flex-1 flex-col overflow-hidden p-0">
        <div className="border-b border-border-subtle p-5">
          <h1 className="flex items-center gap-2 text-xl font-semibold text-text-primary">
            <Bot className="h-5 w-5 text-brand-400" /> Channel Assistant
          </h1>
          <p className="mt-1 text-sm text-text-secondary">
            {focusedJob
              ? `Focused on "${focusedJob.video_title || focusedJob.video_url}" — questions are answered from this video's comments only.`
              : "Ask about any of your analyzed videos, compare them, or get general content strategy advice."}
          </p>
          <div className="mt-3">
            <FocusAreaSelect jobs={focusableJobs} value={focusJobId} onChange={setFocusJobId} disabled={isSending} />
          </div>
        </div>

        {isLoadingMessages ? (
          <div className="flex flex-1 items-center justify-center">
            <CardContent className="flex items-center gap-2.5 p-0 text-sm text-text-secondary">
              <Loader2 className="h-4 w-4 animate-spin text-brand-400" />
              Loading conversation…
            </CardContent>
          </div>
        ) : sessionError ? (
          <div className="flex flex-1 items-center justify-center p-5">
            <CardContent className="p-0 text-sm text-feedback-danger">{sessionError}</CardContent>
          </div>
        ) : (
          <>
            <div ref={scrollRef} className="flex-1 overflow-y-auto p-5">
              {messages.length === 0 ? (
                <div className="flex h-full flex-col items-center justify-center gap-4 text-center">
                  <Bot className="h-8 w-8 text-text-muted" />
                  <p className="max-w-sm text-sm text-text-muted">
                    Ask anything about your channel — across every video you&apos;ve analyzed.
                  </p>
                  <div className="flex flex-wrap justify-center gap-2 px-4">
                    {SUGGESTED_PROMPTS.map((prompt) => (
                      <button
                        key={prompt}
                        type="button"
                        onClick={() => void send(prompt)}
                        className="rounded-full border border-border-default px-3 py-1.5 text-xs text-text-secondary transition-colors hover:border-brand-400 hover:text-text-primary"
                      >
                        <Sparkles className="mr-1.5 inline h-3 w-3 text-brand-400" />
                        {prompt}
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex flex-col gap-5">
                  {messages.map((message) => (
                    <AssistantMessageBubble key={message.id} message={message} />
                  ))}
                  {isSending && (
                    <div className="flex items-center gap-2 text-xs text-text-muted">
                      <Sparkles className="h-3.5 w-3.5 animate-pulse text-brand-400" />
                      Thinking…
                    </div>
                  )}
                </div>
              )}
            </div>
            <div className="border-t border-border-subtle p-4">
              {sendError && <p className="mb-2 text-xs text-feedback-danger">{sendError}</p>}
              <ChatInput onSend={(question) => void send(question)} disabled={isSending} />
            </div>
          </>
        )}
      </Card>

      <ConfirmModal
        isOpen={deleteTarget !== null}
        title="Delete this conversation?"
        description={`This permanently deletes "${
          deleteTarget?.title || 'this conversation'
        }" and all of its messages. This can't be undone.`}
        confirmLabel="Delete"
        variant="danger"
        isConfirming={isDeleting}
        onConfirm={handleConfirmDelete}
        onClose={() => !isDeleting && setDeleteTarget(null)}
      />
    </div>
  );
}
