# 🎯 SentimentPRO — YouTube Comment Sentiment Analyzer

**AI-powered platform for analyzing YouTube comments using NLP and Transformer models.**

SentimentPRO helps content creators understand their audience without reading thousands of comments manually. Paste a video URL and get a full sentiment breakdown, spam/sarcasm/language detection, AI-generated executive summaries, audience personas, complaint/suggestion mining, FAQs, topic clusters, an "audience health" score, and a RAG-based chat assistant to ask free-form questions about that video's comments — all through an interactive dashboard.

[![CI](https://github.com/ismailhalawa-ctrl/SentimentPro-youtube/actions/workflows/ci.yml/badge.svg)](https://github.com/ismailhalawa-ctrl/SentimentPro-youtube/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📸 Preview

<!-- Add screenshots to a docs/screenshots/ folder and update the paths below. -->

### 🏠 Landing Page
![Landing Page](docs/screenshots/landing.png)
*(add screenshot here)*

### 📊 Analytics Dashboard
![Dashboard](docs/screenshots/dashboard.png)
*(add screenshot here)*

### 💬 Comment Explorer
![Comment Explorer](docs/screenshots/comments.png)
*(add screenshot here)*

### 🤖 AI Assistant (RAG Chat)
![AI Assistant](docs/screenshots/assistant.png)
*(add screenshot here)*

---

## ✨ Features

### 🤖 Sentiment Analysis
- Arabic sentiment analysis using **MARBERT**
- English sentiment analysis using **RoBERTa**
- Mixed-language support with per-comment language detection
- Confidence scoring on every result
- Emoji-aware sentiment adjustments

### 🌍 Language Detection
- Arabic, English, mixed Arabic/English, and other languages

### 🚨 Spam Detection
- Promotional comments, suspicious links, phone numbers, WhatsApp spam, and repeated/boilerplate content

### 😏 Sarcasm Detection
- Emoji-based and rule-based sarcasm recognition, contradiction/contrast detection

### 📊 Interactive Dashboard
- Sentiment distribution, language distribution, sentiment timeline, likes-vs-sentiment scatter, keyword panel, top comments, paginated comment explorer with filters

### 🧠 AI-Powered Insights
*(on-demand, cached, degrades gracefully without an API key — never a hard failure)*
- Executive summaries
- Audience personas / segments
- Complaint extraction
- Suggestion & feature-request extraction
- FAQ generation
- Topic clustering
- Deterministic + LLM-narrated **Audience Intelligence score**

### 💬 RAG Chat Assistant
- Ask free-form questions about a video's comments; answers are grounded in vector search over the actual comments, with citations back to the source

### 📄 Export Reports
- CSV, Excel, and PDF

### 🔐 Authentication
- Email/password and Google OAuth, JWT session cookies, password reset

### 📚 Analysis History
- Per-user history of past analyses, backed by SQL Server

### ⚡ Three Analysis Modes

| Mode | How it works | Requires an API key? |
|---|---|---|
| **FAST** | Local models only (MARBERT/RoBERTa), batched, optionally ONNX-quantized | No |
| **SMART** | Every (deduplicated) comment sent to the configured LLM | Yes |
| **HYBRID** | FAST result first, escalates uncertain/ambiguous comments to the LLM | Optional (falls back to FAST) |

---

## 🛠️ Technologies Used

**Backend** — Python, FastAPI, SQLAlchemy 2.0, SQL Server (pyodbc), Alembic, Pydantic v2, python-jose / passlib (JWT auth), slowapi (Redis-backed rate limiting)

**AI / ML** — PyTorch, Hugging Face Transformers, MARBERT (Arabic), RoBERTa (English), optional ONNX Runtime, OpenAI & Gemini (optional LLM providers), `sentence-transformers` (embeddings), ChromaDB (vector store, with optional Qdrant/Pinecone)

**Frontend** — Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4, Recharts, Framer Motion

**Infra** — Docker, Docker Compose, Redis, GitHub Actions CI/CD

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/ismailhalawa-ctrl/SentimentPro-youtube.git
cd SentimentPro-youtube
```

### Quick start (Docker Compose — recommended)

```bash
cp backend/.env.example backend/.env   # fill in DATABASE_URL, JWT_SECRET_KEY, YOUTUBE_API_KEY, etc.
docker compose up --build
```

This builds and runs Redis, the backend (`:8000`), and the frontend (`:3000`). Database migrations run automatically on backend startup. See [DEPLOYMENT.md](DEPLOYMENT.md) for production notes.

### Manual setup

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env                              # fill in required values
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

### Environment variables

At minimum, `backend/.env` needs a real `DATABASE_URL`, a strong `JWT_SECRET_KEY`, and a `YOUTUBE_API_KEY` (YouTube Data API v3, from Google Cloud Console). `OPENAI_API_KEY` / `GEMINI_API_KEY` are optional — without them the app runs fully in FAST mode. See `backend/.env.example` for the complete, documented list.

---

## 🗄️ Database Setup

The app uses **SQL Server**, managed entirely through **SQLAlchemy models + Alembic migrations** — no manual schema setup needed.

```bash
# 1. Create an empty database
CREATE DATABASE SentimentPRO;

# 2. Point DATABASE_URL at it in backend/.env, then apply all migrations
cd backend
alembic upgrade head
```

This creates the full schema (users, analysis jobs, comment analyses/results, job insights, embedding indexes, chat sessions/messages, etc.) in one step. See `backend/alembic/versions/` for the full migration history.

---

## 📁 Project Structure

```
.
├── backend/            FastAPI app (app/ai, app/api, app/models, app/services, tests/, alembic/)
├── frontend/            Next.js app (app/, components/, features/, lib/)
├── scripts/             Docker smoke test, production-readiness check
├── .github/workflows/   CI pipeline (lint, type-check, security scan, tests, docker build)
├── docker-compose.yml
├── DEPLOYMENT.md
└── README.md
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for architecture notes, scaling considerations, and health checks.

---

## 🧪 Testing

```bash
# Backend
cd backend && pytest tests/ -v --cov=app

# Frontend
cd frontend && npm run test:coverage
```

CI runs lint (ruff/eslint), type checks (mypy/tsc), security scans (gitleaks, bandit, pip-audit, npm audit), the full test suite, and a Docker build + smoke test on every push.

---

## 🚀 Roadmap

- 📧 Real email delivery for password reset (currently logged server-side only)
- 📈 Horizontally-scalable job cancellation (currently in-memory, single-process)
- 🔑 Per-user LLM cost/quota controls
- 🌐 Additional embedding/vector-store and LLM provider options

---

## 📄 License

Released under the [MIT License](LICENSE) — free to use, modify, and distribute, with attribution.

---

## 👤 Author

**Ismail Halawa**

- **GitHub :** [@ismailhalawa-ctrl](https://github.com/ismailhalawa-ctrl)
- **LinkedIn :** [Ismail Halawa](https://www.linkedin.com/in/ismail-halawa-987aa52ab/)
- **Email :** [ismaeelhalawa2003@gmail.com](mailto:ismaeelhalawa2003@gmail.com)

---

## ⭐ Project Highlights

- AI-powered sentiment analysis with Arabic and English support
- Spam and sarcasm detection
- LLM-generated audience insights and a RAG chat assistant
- Interactive analytics dashboard with CSV/Excel/PDF export
- Full CI/CD: linting, type checks, security scans, tests, and Docker build on every push
- Production-oriented architecture with authentication, rate limiting, and database migrations
