# Deployment

## Prerequisites

- A running SQL Server instance (Azure SQL, a managed VM, or self-hosted) reachable from wherever the backend container runs. This stack does not containerize SQL Server — it is expected to be an external, backed-up, managed database.
- `backend/.env` populated from `backend/.env.example` with real production values (`ENVIRONMENT=production`, a strong `JWT_SECRET_KEY` — the app refuses to start in production with a weak or default one — and real provider/API keys).
- `frontend/.env.local` (or build-time `NEXT_PUBLIC_API_URL`) pointing at the backend's public URL.
- `DATABASE_URL` must use SQL Server authentication (`mssql+pyodbc://user:password@host:1433/db?...`) or Azure AD authentication, **not** `Trusted_Connection=yes`. Windows Integrated/Kerberos authentication has no credentials to present from inside a Linux container and fails immediately with `SSPI Provider: No credentials were supplied` — confirmed by actually running the built backend image against this project's dev database. If your local `.env` currently uses `Trusted_Connection=yes` (common for same-machine SQL Server dev setups), swap in a SQL login before deploying.

## Local stack

```
docker compose up --build
```

This builds and runs `redis`, `backend` (port 8000), and `frontend` (port 3000). Database migrations run automatically on backend container start (`alembic upgrade head`) before uvicorn starts.

If your SQL Server runs on the host machine rather than in a container, use `host.docker.internal` instead of `localhost` in `DATABASE_URL` on Docker Desktop (Mac/Windows) — `localhost` inside the container refers to the container itself, not the host.

## Architecture notes relevant to scaling

- The backend loads all three sentiment models into process memory at startup and is written as a single-process, multi-threaded service (`torch.set_num_threads` sized to available CPU cores). Running multiple worker **processes** behind one container would multiply memory usage by the model set for no throughput benefit under this design — scale by running more container **replicas** behind a load balancer instead, not by adding `--workers` to uvicorn.
- Rate limiting (`slowapi`) uses Redis when `REDIS_URL` is set (as it is by default in `docker-compose.yml`) so limits are shared correctly across replicas. Without Redis, each replica tracks its own in-memory counters, which under-enforces limits once you run more than one replica.
- `onnx_models` and `chroma_data` are named volumes so downloaded ONNX weights and the local vector index persist across container restarts instead of re-downloading/rebuilding every deploy.

## Backups

Nothing in this repo backs up the database — that is the managed SQL Server provider's responsibility (e.g., Azure SQL point-in-time restore, automated snapshots on a managed VM). Before going live, confirm:
- Automated backups are enabled on the SQL Server instance with a retention window appropriate to the business.
- A restore has actually been tested at least once, not just configured.

`chroma_data` (the RAG vector index) is rebuildable from the database's comment data and does not need independent backup, but losing it means the Universal Audience Assistant will re-index on next use rather than serving instantly.

## Health checks

`GET /health` on the backend reports `{"status": "ok", "checks": {"database": "ok", "models": "ok"}}` with HTTP 200 when healthy, or `503` with `"status": "degraded"` if the database is unreachable or a sentiment model failed to load — use this for load balancer / orchestrator health checks, not a bare TCP check.
