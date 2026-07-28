import type { Metadata } from 'next';
import { PageHero } from '@/components/marketing/page-hero';
import { SectionHeading } from '@/components/ui/section-heading';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { EndpointCard, type EndpointData } from '@/components/api-reference/endpoint-card';

export const metadata: Metadata = {
  title: 'API Reference — SentimentPRO',
  description: 'Endpoints, request payloads, and response shapes for integrating with SentimentPRO.',
};

const JOB_ENDPOINTS: EndpointData[] = [
  {
    method: 'POST',
    path: '/api/v1/analysis/jobs',
    description: 'Submits a YouTube video for analysis. Runs in the background — poll the job (or watch it in the dashboard) for progress.',
    requestBody: `{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "max_comments": 5000,
  "language": "auto",
  "confidence_threshold": 0.55,
  "mode": "hybrid",
  "order": "relevance"
}`,
    response: `{
  "id": 482,
  "status": "pending",
  "progress_percentage": 0,
  "current_step": null,
  "error_message": null,
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "video_id": "dQw4w9WgXcQ",
  "video_title": null,
  "video_thumbnail_url": null,
  "created_at": "2026-07-14T10:32:04Z",
  "sentiment_summary": null
}`,
  },
  {
    method: 'GET',
    path: '/api/v1/analysis/jobs',
    description: 'Lists your analysis jobs, most recent first, with each job\'s sentiment summary attached.',
    response: `{
  "jobs": [
    {
      "id": 482,
      "status": "completed",
      "progress_percentage": 100,
      "video_title": "Never Gonna Give You Up",
      "video_thumbnail_url": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg",
      "created_at": "2026-07-14T10:32:04Z",
      "sentiment_summary": {
        "positive_count": 3120,
        "neutral_count": 980,
        "negative_count": 410,
        "average_confidence": 0.87
      }
    }
  ]
}`,
  },
  {
    method: 'GET',
    path: '/api/v1/analysis/jobs/{job_id}',
    description: 'Fetches a single job\'s current status and, once completed, its full sentiment summary.',
    response: `{
  "id": 482,
  "status": "completed",
  "progress_percentage": 100,
  "current_step": null,
  "error_message": null,
  "video_id": "dQw4w9WgXcQ",
  "video_title": "Never Gonna Give You Up",
  "created_at": "2026-07-14T10:32:04Z",
  "sentiment_summary": {
    "positive_count": 3120,
    "neutral_count": 980,
    "negative_count": 410,
    "average_confidence": 0.87,
    "spam_count": 62,
    "sarcasm_count": 145,
    "arabic_count": 512,
    "english_count": 3890,
    "mixed_count": 108,
    "other_count": 0
  }
}`,
  },
  {
    method: 'POST',
    path: '/api/v1/analysis/jobs/{job_id}/cancel',
    description: 'Cancels a pending or in-progress job at its next safe checkpoint. Already-processed comments are kept, not rolled back.',
    response: `{ "id": 482, "status": "cancelled", "progress_percentage": 63, ... }`,
  },
  {
    method: 'DELETE',
    path: '/api/v1/analysis/jobs/{job_id}',
    description: 'Permanently deletes one job and everything attached to it — comments, insights, chat history, and its vector search index.',
    response: `204 No Content`,
  },
  {
    method: 'DELETE',
    path: '/api/v1/analysis/jobs/clear-all',
    description: 'Permanently deletes every analysis job you own.',
    response: `{ "deleted_count": 7 }`,
  },
];

const INSIGHTS_ENDPOINTS: EndpointData[] = [
  {
    method: 'GET',
    path: '/api/v1/analysis/jobs/{job_id}/keywords',
    description: 'The most frequent keywords, grouped by the sentiment of the comments they appeared in.',
    response: `{
  "positive": [{ "word": "amazing", "count": 214 }],
  "negative": [{ "word": "boring", "count": 38 }],
  "neutral": [{ "word": "video", "count": 512 }]
}`,
  },
  {
    method: 'GET',
    path: '/api/v1/analysis/jobs/{job_id}/topics',
    description: 'Topic clusters extracted from positive and negative comments.',
    response: `{
  "positive": { "production quality": 88, "nostalgia": 61 },
  "negative": { "audio sync": 14 }
}`,
  },
  {
    method: 'GET',
    path: '/api/v1/analysis/jobs/{job_id}/insights',
    description: 'Short, human-readable AI-generated insight statements about the comment set.',
    response: `{
  "insights": [
    "Positive sentiment dominates at 68% of all comments.",
    "A recurring theme is nostalgia for the original release."
  ]
}`,
  },
  {
    method: 'GET',
    path: '/api/v1/analysis/jobs/{job_id}/comments',
    description: 'The full per-comment feed — sentiment, confidence, language, spam and sarcasm flags for every analyzed comment.',
    response: `{
  "comments": [
    {
      "id": 91123,
      "author": "jane_doe",
      "text": "This still holds up!",
      "likes": 412,
      "published_at": "2026-06-02T14:11:00Z",
      "sentiment": "positive",
      "confidence": 0.94,
      "language": "en",
      "is_spam": false,
      "spam_reason": null,
      "is_sarcasm": false
    }
  ]
}`,
  },
  {
    method: 'GET',
    path: '/api/v1/analysis/jobs/{job_id}/export?format=csv',
    description: '`format` is one of `csv`, `excel`, or `pdf`. CSV/Excel return full per-comment data; PDF returns a summary report with charts and insights.',
    response: `200 OK — binary file
Content-Type: text/csv | application/vnd.openxmlformats-... | application/pdf
Content-Disposition: attachment; filename="analysis_..."`,
  },
];

const CHAT_ENDPOINTS: EndpointData[] = [
  {
    method: 'POST',
    path: '/api/v1/chat/jobs/{job_id}/sessions',
    description: 'Starts a new AI assistant chat session scoped to one analysis job.',
    response: `{
  "id": 14,
  "job_id": 482,
  "title": null,
  "created_at": "2026-07-14T11:02:10Z",
  "updated_at": "2026-07-14T11:02:10Z"
}`,
  },
  {
    method: 'GET',
    path: '/api/v1/chat/jobs/{job_id}/sessions',
    description: 'Lists chat sessions for a job.',
    response: `[
  { "id": 14, "job_id": 482, "title": "What are people complaining about?", "created_at": "...", "updated_at": "..." }
]`,
  },
  {
    method: 'GET',
    path: '/api/v1/chat/sessions/{session_id}',
    description: 'Fetches a session along with its full message history.',
    response: `{
  "id": 14,
  "job_id": 482,
  "title": "What are people complaining about?",
  "messages": [
    { "id": 1, "role": "user", "content": "What are people complaining about?", "citations_json": [], "created_at": "..." },
    { "id": 2, "role": "assistant", "content": "A recurring complaint is...", "citations_json": [{ "comment_id": 91123, "text": "...", "author": "jane_doe", "like_count": 412 }], "created_at": "..." }
  ]
}`,
  },
  {
    method: 'POST',
    path: '/api/v1/chat/sessions/{session_id}/messages',
    description: 'Sends a question to the AI assistant. Always returns 200 with a `status` field — "unavailable" covers both "no AI provider configured" and "this job isn\'t indexed yet".',
    requestBody: `{ "question": "What are people complaining about most?" }`,
    response: `{
  "status": "ok",
  "reason": null,
  "message": {
    "id": 2,
    "role": "assistant",
    "content": "A recurring complaint is...",
    "citations_json": [{ "comment_id": 91123, "text": "...", "author": "jane_doe", "like_count": 412 }],
    "created_at": "2026-07-14T11:02:41Z"
  }
}`,
  },
];

export default function ApiReferencePage() {
  return (
    <>
      <PageHero
        eyebrow="For developers"
        title="API Reference"
        description="The exact endpoints, request payloads, and response shapes that power the SentimentPRO dashboard."
      />

      <section className="pb-12">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <Card variant="glass" className="p-6">
            <CardContent className="flex flex-col gap-3 p-0">
              <div className="flex items-center gap-2.5">
                <Badge status="info">Authentication</Badge>
              </div>
              <p className="text-sm text-text-secondary">
                Every endpoint below requires an authenticated session — sign in via{' '}
                <code className="font-mono text-text-primary">POST /api/v1/auth/login</code> (or Google
                OAuth) to receive a session cookie, then include it on subsequent requests. Dedicated
                API-key access for server-to-server integrations is on our roadmap — Enterprise
                customers can <a href="/contact" className="text-brand-400 hover:text-brand-500">contact us</a> for early access.
              </p>
              <p className="text-sm text-text-secondary">
                Base URL: <code className="font-mono text-text-primary">https://api.sentimentpro.app</code>{' '}
                (or your self-hosted backend&rsquo;s URL). All request and response bodies are JSON
                unless noted otherwise.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      <section className="pb-20">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <SectionHeading eyebrow="Resource" title="Analysis Jobs" className="text-left" />
          <div className="mt-8 flex flex-col gap-5">
            {JOB_ENDPOINTS.map((endpoint) => (
              <EndpointCard key={`${endpoint.method}-${endpoint.path}`} endpoint={endpoint} />
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-border-subtle pb-20 pt-20">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <SectionHeading eyebrow="Resource" title="Insights & Export" className="text-left" />
          <div className="mt-8 flex flex-col gap-5">
            {INSIGHTS_ENDPOINTS.map((endpoint) => (
              <EndpointCard key={`${endpoint.method}-${endpoint.path}`} endpoint={endpoint} />
            ))}
          </div>
        </div>
      </section>

      <section className="border-t border-border-subtle pb-24 pt-20">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <SectionHeading eyebrow="Resource" title="AI Chat Assistant" className="text-left" />
          <div className="mt-8 flex flex-col gap-5">
            {CHAT_ENDPOINTS.map((endpoint) => (
              <EndpointCard key={`${endpoint.method}-${endpoint.path}`} endpoint={endpoint} />
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
