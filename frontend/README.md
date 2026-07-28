# Frontend

Next.js (App Router) client for SentimentPRO. See the root [README](../README.md) for project-wide setup.

## Development

```bash
npm install
npm run dev
```

Runs at [http://localhost:3000](http://localhost:3000). Requires the backend API running (see `../backend`) and `NEXT_PUBLIC_API_URL` set in `.env.local` (see `.env.local.example`).

## Scripts

- `npm run dev` — start the dev server
- `npm run build` / `npm run start` — production build/run
- `npm run lint` — ESLint
- `npm run test` / `npm run test:coverage` — Vitest
