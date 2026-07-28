# Changelog

All notable changes to this project are documented in this file.

## [1.0.0] — Production-ready release

### Core analysis
- Per-comment sentiment analysis (positive/neutral/negative) using local MARBERT (Arabic) and RoBERTa (English) models, ONNX-quantized for CPU inference.
- Spam, sarcasm, and language detection (Arabic/English/mixed/other).
- Three analysis modes: **FAST** (local models only), **SMART** (LLM-powered via OpenAI/Gemini), and **HYBRID** (local-first with selective LLM escalation).

### Dashboards
- Sentiment distribution, language distribution, sentiment timeline, likes-vs-sentiment scatter, keyword panel, top comments, and a paginated/filterable comment explorer.
- CSV, Excel, and PDF export.

### AI-powered insights
- On-demand, cached executive summaries, audience personas/segments, complaint extraction, suggestion/feature-request extraction, FAQ generation, topic clustering, and a deterministic + LLM-narrated Audience Intelligence score.
- All AI features degrade gracefully (typed "unavailable" response, never a hard failure) when no LLM API key is configured.

### Audience Assistant (RAG chat)
- Vector-search-grounded Q&A over a video's comments, with citations back to source comments.
- Chroma as the default embedded vector store, with optional Qdrant/Pinecone backends.

### Authentication & accounts
- Email/password and Google OAuth, JWT session cookies, password reset, name-change cooldown, account deletion with full data cleanup.

### Platform
- SQL Server persistence via SQLAlchemy + Alembic migrations.
- Redis-backed rate limiting (shared correctly across replicas).
- Stripe-based subscription billing (Free/Pro tiers).
- Docker Compose deployment (backend, frontend, Redis).
- Full CI pipeline: secret scanning (gitleaks), lint (ruff/eslint), type checks (mypy/tsc), security scans (bandit, pip-audit, npm audit), automated test suite, and a Docker build + smoke test on every push.

### Known limitations
- Password reset links are logged server-side only (no email delivery integration yet).
- Job cancellation is tracked in-memory per process — doesn't survive restarts or coordinate across multiple backend replicas.
- No per-user LLM cost/quota enforcement beyond a per-job comment cap.
