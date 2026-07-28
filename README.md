# SentimentPRO

AI-powered YouTube comment sentiment analysis platform. Paste a video URL and get a sentiment breakdown, spam/sarcasm/language detection, AI-generated executive summaries, audience personas, complaint/suggestion mining, FAQs, topic clusters, an "audience health" score, and a RAG-based chat assistant for asking free-form questions about that video's comments.

[![CI](https://github.com/ismailhalawa-ctrl/SentimentPRO---YouTube-Analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/ismailhalawa-ctrl/SentimentPRO---YouTube-Analytics/actions/workflows/ci.yml)

## Features

- **Per-comment analysis** — sentiment (positive/neutral/negative), spam flag, sarcasm flag, language detection (Arabic/English/mixed).
- **Dashboards** — sentiment distribution, language distribution, likes-vs-sentiment scatter, sentiment timeline, keyword panel, top comments, paginated comment explorer.
- **Exports** — CSV, Excel, and PDF reports.
- **AI insights** (on-demand, cached, degrade gracefully without an API key) — executive summary, audience personas/segments, complaint extraction, suggestion extraction, FAQ generation, topic clustering, and a deterministic + LLM-narrated audience intelligence score.
- **RAG chat assistant** — vector-search-grounded Q&A over a specific video's comments, with citations back to the source comments.
- **Auth** — email/password and Google OAuth, JWT session cookies, password reset.
- **Analysis history** — per-user job history with delete/clear.

## Tech Stack

**Backend** — FastAPI, SQLAlchemy 2.0, SQL Server (via pyodbc), Alembic migrations, Pydantic v2, JWT auth (python-jose/passlib), slowapi rate limiting (Redis-backed), PyTorch + Transformers.

**Frontend** — Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4, Recharts, Framer Motion.

**AI / ML** — Local sentiment models: MARBERT (Arabic) and RoBERTa (English), optionally ONNX-quantized. Optional LLM providers: OpenAI and Gemini. Embeddings via local `sentence-transformers` (default) or OpenAI embeddings (opt-in). Vector store: Chroma (default), with optional Qdrant/Pinecone backends.

## Analysis Modes

| Mode | How it works | Requires an API key? |
|---|---|---|
| **FAST** | Local models only, batched | No |
| **SMART** | Every comment sent to the configured LLM | Yes |
| **HYBRID** | FAST result first, escalates uncertain/ambiguous comments to the LLM | Optional (falls back to FAST) |

## Getting Started

### Prerequisites

- A running SQL Server instance (local, Azure SQL, or another managed instance).
- Docker and Docker Compose (recommended), or Python 3.13+ and Node 22+ for a manual setup.

### Quick start (Docker Compose)

```bash
cp backend/.env.example backend/.env   # fill in DATABASE_URL, JWT_SECRET_KEY, etc.
docker compose up --build
```

This builds and runs Redis, the backend (`:8000`), and the frontend (`:3000`). Database migrations run automatically on backend startup. See [DEPLOYMENT.md](DEPLOYMENT.md) for production notes.

### Manual setup

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env   # fill in required values
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## Testing

```bash
# Backend
cd backend && pytest tests/ -v --cov=app

# Frontend
cd frontend && npm run test:coverage
```

CI runs lint (ruff/eslint), type checks (mypy/tsc), security scans (gitleaks, bandit, pip-audit, npm audit), the full test suite, and a Docker build + smoke test on every push — see [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## License

All rights reserved — see [LICENSE](LICENSE).
