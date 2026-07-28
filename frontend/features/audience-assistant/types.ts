export interface AssistantCitation {
  job_id: number;
  comment_id: number;
  text: string;
  author: string;
  like_count: number;
}

export interface ToolCallTrace {
  tool: string;
  status: 'success' | 'error';
  arguments: Record<string, unknown>;
  result_summary: string;
}

export interface AssistantMessage {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  citations_json: AssistantCitation[];
  tool_calls_json: ToolCallTrace[];
  created_at: string;
}

export interface AssistantSession {
  id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
}

export interface AssistantSessionWithMessages extends AssistantSession {
  messages: AssistantMessage[];
}

export type SendAssistantMessageStatus = 'ok' | 'unavailable' | 'error';

export interface SendAssistantMessageResponse {
  status: SendAssistantMessageStatus;
  reason: string | null;
  message: AssistantMessage | null;
}
