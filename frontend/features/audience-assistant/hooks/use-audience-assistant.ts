'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import {
  createAssistantSession,
  deleteAssistantSession,
  getAssistantSession,
  listAssistantSessions,
  sendAssistantMessage,
} from '@/features/audience-assistant/api/audience-assistant-api';
import { listAnalysisJobs } from '@/features/analysis/api/analysis-api';
import { ApiError } from '@/lib/api-client';
import type { AssistantMessage, AssistantSession } from '@/features/audience-assistant/types';
import type { AnalysisJob } from '@/features/analysis/types';

export function useAudienceAssistant() {
  const [sessions, setSessions] = useState<AssistantSession[]>([]);
  const [isLoadingSessions, setIsLoadingSessions] = useState(true);
  const [sessionsError, setSessionsError] = useState<string | null>(null);

  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);
  const [messages, setMessages] = useState<AssistantMessage[]>([]);
  const [isLoadingMessages, setIsLoadingMessages] = useState(false);
  const [sessionError, setSessionError] = useState<string | null>(null);

  const [isSending, setIsSending] = useState(false);
  const [sendError, setSendError] = useState<string | null>(null);

  const [focusableJobs, setFocusableJobs] = useState<AnalysisJob[]>([]);
  const [focusJobId, setFocusJobId] = useState<number | null>(null);

  const initialized = useRef(false);

  const selectSession = useCallback(async (sessionId: number) => {
    setActiveSessionId(sessionId);
    setIsLoadingMessages(true);
    setSessionError(null);
    setSendError(null);
    try {
      const full = await getAssistantSession(sessionId);
      setMessages(full.messages);
    } catch (err) {
      setSessionError(err instanceof ApiError ? err.message : 'Failed to load this conversation.');
    } finally {
      setIsLoadingMessages(false);
    }
  }, []);

  useEffect(() => {
    if (initialized.current) return;
    initialized.current = true;

    (async () => {
      try {
        const list = await listAssistantSessions();
        setSessions(list);
        if (list.length > 0) {
          await selectSession(list[0].id);
        }
      } catch (err) {
        setSessionsError(err instanceof ApiError ? err.message : 'Failed to load your conversations.');
      } finally {
        setIsLoadingSessions(false);
      }

      try {
        const { jobs } = await listAnalysisJobs();
        setFocusableJobs(jobs.filter((job) => job.status === 'completed'));
      } catch {
        setFocusableJobs([]);
      }
    })();
  }, [selectSession]);

  const startNewSession = useCallback(async () => {
    try {
      const session = await createAssistantSession();
      setSessions((prev) => [session, ...prev]);
      setActiveSessionId(session.id);
      setMessages([]);
      setSessionError(null);
      setSendError(null);
    } catch (err) {
      setSessionsError(err instanceof ApiError ? err.message : 'Failed to start a new conversation.');
    }
  }, []);

  const focusOnJob = useCallback(
    async (jobId: number) => {
      setFocusJobId(jobId);
      await startNewSession();
    },
    [startNewSession]
  );

  const removeSession = useCallback(
    async (sessionId: number) => {
      try {
        await deleteAssistantSession(sessionId);
        setSessions((prev) => prev.filter((s) => s.id !== sessionId));
        if (activeSessionId === sessionId) {
          setActiveSessionId(null);
          setMessages([]);
        }
      } catch (err) {
        setSessionsError(err instanceof ApiError ? err.message : 'Failed to delete this conversation.');
      }
    },
    [activeSessionId]
  );

  const send = useCallback(
    async (question: string) => {
      if (isSending || !question.trim()) return;

      let sessionId = activeSessionId;
      if (sessionId === null) {
        try {
          const session = await createAssistantSession();
          setSessions((prev) => [session, ...prev]);
          setActiveSessionId(session.id);
          sessionId = session.id;
        } catch (err) {
          setSendError(err instanceof ApiError ? err.message : 'Failed to start a new conversation.');
          return;
        }
      }

      const optimisticUserMessage: AssistantMessage = {
        id: -Date.now(),
        role: 'user',
        content: question,
        citations_json: [],
        tool_calls_json: [],
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, optimisticUserMessage]);
      setIsSending(true);
      setSendError(null);

      try {
        const response = await sendAssistantMessage(sessionId, question, focusJobId);
        if (response.status === 'ok' && response.message) {
          const assistantMessage = response.message;
          setMessages((prev) => [...prev, assistantMessage]);
          setSessions((prev) => {
            const current = prev.find((s) => s.id === sessionId);
            if (!current) return prev;
            const updated = { ...current, title: current.title ?? question.slice(0, 80) };
            return [updated, ...prev.filter((s) => s.id !== sessionId)];
          });
        } else {
          setSendError(response.reason ?? 'The assistant could not answer that.');
        }
      } catch (err) {
        setSendError(err instanceof ApiError ? err.message : 'Failed to send the message.');
      } finally {
        setIsSending(false);
      }
    },
    [activeSessionId, isSending, focusJobId]
  );

  return {
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
  };
}
