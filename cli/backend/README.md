# CLI Simulator backend

Minimal, dependency-free AI backend for the Seed Code CLI Simulator.
One OpenRouter key (server-side only), one default free model, no auth,
no accounts, no database.

## Architecture

```
cli/backend/chat-core.js   shared logic: system prompt, model, sanitizer,
                           OpenRouter call — used by BOTH entry points
cli/backend/server.js      local dev server (Node, :8787) — also serves /cli
/api/chat.js               Vercel serverless function (production)
```

The frontend (`cli/script.js`) auto-detects its environment — no edits needed:

| Where the page runs                  | Endpoint used                        |
|--------------------------------------|--------------------------------------|
| `localhost` / `127.0.0.1` (any port) | `http://localhost:8787/api/chat`     |
| Served by this backend on `:8787`    | `/api/chat` (same origin)            |
| Any deployed domain (Vercel)         | `/api/chat` (serverless function)    |

## Development

Requires Node 18+.

```bash
# terminal 1 — the site
python -m http.server 8000

# terminal 2 — the AI backend
cd cli/backend
cp .env.example .env      # paste your OpenRouter key into .env
node server.js            # → http://localhost:8787
```

Open http://localhost:8000/cli/ — questions are answered via `:8787`
(CORS is open on the API routes).

## Production (Vercel)

Nothing to configure in code. Vercel picks up `/api/chat.js` automatically.
Set the env var in the Vercel project settings:

```
OPENROUTER_API_KEY = sk-or-v1-...
```

Optionally `SEEDCODE_MODEL` to override the default free model.

## Endpoints

- `POST /api/chat` — `{ messages: [{role, content}, …] }` → `{ reply }`
  History comes from the browser session (sessionStorage), capped and
  sanitized server-side (last 20 messages, 4 KB each, roles whitelisted).
- `GET /api/health` — dev server only, liveness check.

## Failure behavior

Missing key → 503, upstream error → 502 — both with the message
"The Seed Code Assistant is temporarily unavailable. Please try again in a
few moments." The frontend shows it and falls back to built-in offline
answers; errors are logged server-side, never silently swallowed.

## Notes

- `server.js` refuses to serve anything inside `backend/`, so `.env` can
  never leak through the static file route.
- `.env` is gitignored; use `.env.example` as the template.
