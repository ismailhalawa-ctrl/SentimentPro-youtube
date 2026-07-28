import { apiClient } from '@/lib/api-client';
import type {
  AssistantSession,
  AssistantSessionWithMessages,
  SendAssistantMessageResponse,
} from '@/features/audience-assistant/types';

export function createAssistantSession(): Promise<AssistantSession> {
  return apiClient<AssistantSession>('/api/v1/audience-assistant/sessions', { method: 'POST' });
}

export function listAssistantSessions(limit = 50, offset = 0): Promise<AssistantSession[]> {
  return apiClient<AssistantSession[]>(
    `/api/v1/audience-assistant/sessions?limit=${limit}&offset=${offset}`,
    { method: 'GET' }
  );
}

export function getAssistantSession(sessionId: number): Promise<AssistantSessionWithMessages> {
  return apiClient<AssistantSessionWithMessages>(`/api/v1/audience-assistant/sessions/${sessionId}`, {
    method: 'GET',
  });
}

export function deleteAssistantSession(sessionId: number): Promise<void> {
  return apiClient<void>(`/api/v1/audience-assistant/sessions/${sessionId}`, { method: 'DELETE' });
}

export function sendAssistantMessage(
  sessionId: number,
  question: string,
  jobId?: number | null
): Promise<SendAssistantMessageResponse> {
  return apiClient<SendAssistantMessageResponse>(
    `/api/v1/audience-assistant/sessions/${sessionId}/messages`,
    { method: 'POST', body: { question, job_id: jobId ?? null } }
  );
}
