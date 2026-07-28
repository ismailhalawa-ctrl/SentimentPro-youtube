# Architecture

## Overview

SentimentPRO is a two-service application: a FastAPI backend and a Next.js frontend, backed by SQL Server and (optionally) Redis. A user submits a YouTube video URL; the backend fetches its comments, runs them through a sentiment/spam/sarcasm pipeline, and the frontend renders the results as an interactive dashboard with on-demand AI-generated insights and a RAG chat assistant.

```
┌─────────────┐      HTTP (cookie auth)      ┌──────────────┐
│   Next.js    │ ───────────────────────────▶ │   FastAPI     │
│  (frontend)  │ ◀─────────────────────────── │  (backend)    │
└─────────────┘                               └──────┬───────┘
                                                       │
                        ┌──────────────────────────────┼──────────────────────────┐
                        │                              │                          │
                 ┌──────▼──────┐              ┌────────▼────────┐        ┌────────▼────────┐
                 │  SQL Server  │              │  Local models    │        │  Optional LLMs   │
                 │ (users, jobs,│              │  MARBERT/RoBERTa │        │  OpenAI / Gemini │
                 │  comments,   │              │  (ONNX, CPU)     │        │  (SMART/HYBRID,  │
                 │  insights)   │              └─────────────────┘        │  no key needed    │
                 └──────────────┘                                        │  for FAST mode)    │
                                                                          └────────────────────┘
                        │                              │
                 ┌──────▼──────┐              ┌────────▼────────┐
                 │    Redis     │              │  Chroma (RAG     │
                 │ (rate limit) │              │  vector store)   │
                 └──────────────┘              └─────────────────┘
```

## Backend (`backend/app/`)

- **`api/v1/`** — route handlers (auth, users, youtube, analysis, ai_insights, audience_assistant, billing, support). See [API.md](API.md).
- **`core/`** — settings (`config.py`, pydantic-settings), JWT (`security.py`), rate limiting, security headers, request IDs.
- **`database/`** — SQLAlchemy engine/session setup.
- **`models/`** — SQLAlchemy ORM models (see [Database schema](#database-schema) below).
- **`schemas/`** — Pydantic request/response models.
- **`services/`** — business logic: job lifecycle, comment extraction, embeddings, chat, exports, auth, billing.
- **`ai/`** — the sentiment/insight engine, described in detail below.

### The `ai/` package

This is where the actual analysis logic lives, organized by pipeline stage:

| Folder | Responsibility |
|---|---|
| `interfaces/` | `Capability` enum, `AnalysisMode`, provider ABC, result/error types |
| `providers/` | One class per model/LLM combination, registered via `@register_provider` |
| `pipelines/` | Orchestrates FAST/SMART/HYBRID analysis and mode-selection policy |
| `preprocessors/` | Text cleaning, language detection |
| `rules/` | Deterministic spam/sarcasm detection, emoji handling, lexicons |
| `postprocessors/` | Confidence calibration, result normalization |
| `prompts/` | One prompt-builder module per AI capability |
| `chains/` | Job-level LLM call + persistence, one per capability |
| `embeddings/` | Embedding provider abstraction (local `sentence-transformers` or OpenAI) |
| `rag/` | Vector store abstraction (Chroma default; Qdrant/Pinecone optional) + retriever |
| `agents/` | The RAG chat agent (comment Q&A over retrieved context) |
| `scoring/` | Deterministic Audience Intelligence scoring |

**Provider registry pattern**: `@register_provider("id")` registers a singleton into a global dict. `resolve_provider(capability, mode, language)` filters by capability/mode/language, preferring an available provider (has an API key configured) but falling back gracefully otherwise — this is how SMART/HYBRID features degrade to a typed "unavailable" response instead of crashing when no LLM key is set.

### Analysis pipeline (URL → insights)

1. `POST /analysis/jobs` creates an `AnalysisJob` (`pending`) and schedules `run_analysis_job` via FastAPI `BackgroundTasks`.
2. The background task fetches video info + comments concurrently from the YouTube Data API, persisting each comment as a `CommentAnalysis` row.
3. A rule-based pass (no model) runs first: language detection, spam, sarcasm — written immediately.
4. A sentiment pass runs next, mode-dependent (see below). Comments are deduplicated by exact text first, so identical comments are only classified once.
5. Progress updates incrementally; cancellation is checked between batches via a per-job `asyncio.Event`.
6. On completion, comment embeddings are indexed into a per-job Chroma collection as a best-effort tail step (failure here doesn't fail the job — only delays chat availability for that job).
7. Job-level AI features (executive summary, personas, FAQs, topics, audience intelligence) and per-comment extraction (complaints, suggestions) are generated lazily on first dashboard visit, then cached.

### Analysis modes

| Mode | How it works | API key needed? |
|---|---|---|
| **FAST** | Local MARBERT (Arabic) / RoBERTa (English) models only, ONNX-quantized, batched | No |
| **SMART** | Every deduplicated comment sent to the configured LLM (OpenAI/Gemini), batched | Yes |
| **HYBRID** | FAST result computed first; escalates to the LLM only for low-confidence, mixed-language, sarcastic, or heavy-emoji comments; falls back to FAST silently if the LLM is unavailable | Optional |

### Background jobs

There is no task queue (no Celery/RQ) — analysis jobs run via FastAPI's `BackgroundTasks`, executing in a thread from Starlette's threadpool; each job opens its own DB session and event loop. Cancellation is tracked in an in-memory, per-process dict — this means it doesn't survive a process restart and doesn't coordinate across multiple backend replicas (see [DEPLOYMENT.md](DEPLOYMENT.md) for scaling notes).

### Database schema

Main tables: `users`, `analysis_jobs`, `comment_analyses`, `comment_analysis_results` (one row per comment × capability), `job_insights` (job-level AI results, cached), `embedding_indexes` (bookkeeping only — vectors live in Chroma's own store), `chat_sessions` / `chat_messages`, `subscriptions`, `support_messages`. All managed via SQLAlchemy models + Alembic migrations (`backend/alembic/versions/`).

## Frontend (`frontend/`)

Next.js App Router. `app/(auth)/` and `app/(marketing)/` are route groups for public pages; `app/dashboard/` is the authenticated app.

- **`components/`** — UI primitives (`ui/`) and feature-specific components (`analysis/`, `chat/`, `dashboard/`, `auth/`, `marketing/`, ...).
- **`features/{name}/`** — one folder per domain feature (analysis, auth, chat, executive-summary, complaints, suggestions, faqs, topics, personas, audience-intelligence, billing, settings, youtube), each with thin `api/` fetch wrappers and `hooks/` for data access.
- **`lib/`** — the shared `api-client.ts` fetch wrapper, i18n, utilities.
- **`middleware.ts`** — gates `/dashboard/*` behind the `access_token` cookie; redirects authenticated users away from `/login`/`/register`.

Authentication state is fetched once (via `/auth/me`) in a top-level `AuthProvider` inside `app/dashboard/layout.tsx` and shared through context; there is no client-side token storage (the JWT lives only in the HTTP-only cookie).

## Infrastructure

- **Docker Compose** runs three services: `redis`, `backend` (`:8000`), `frontend` (`:3000`). SQL Server is expected to be external/managed, not containerized.
- **Redis** backs shared rate limiting across replicas; without it, each replica enforces limits independently.
- **CI** (`.github/workflows/ci.yml`) runs a secret scan (gitleaks), lint (ruff/eslint), type checks (mypy/tsc), security scans (bandit, pip-audit, npm audit), the full test suite, and a Docker build + smoke test on every push.

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment notes and scaling considerations.
