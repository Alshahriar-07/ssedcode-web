/* ============================================================
   Seed Code CLI Simulator — backend/server.js
   Local development backend (Node, dependency-free).

   · POST /api/chat   { messages: [{role, content}, …] } → { reply }
   · GET  /api/health → { ok: true }
   · GET  /*          → serves the /cli folder statically too.

   Dev workflow (matches the frontend's auto-detection):
     terminal 1:  python -m http.server 8000   (site)
     terminal 2:  node cli/backend/server.js   (this, on :8787)
   The frontend on localhost:8000 automatically calls
   http://localhost:8787/api/chat — CORS is open below.

   In production (Vercel), /api/chat.js at the repo root serves
   the same endpoint; both share backend/chat-core.js.

   The OpenRouter API key lives ONLY server-side (env var or a
   .env file next to this script). Never sent to the browser.

   Run:   OPENROUTER_API_KEY=sk-or-... node server.js
   Node:  >= 18 (built-in fetch)
   ============================================================ */

"use strict";

const http = require("http");
const fs = require("fs");
const path = require("path");
const { MODEL, modelChain, UNAVAILABLE, sanitizeMessages, askOpenRouter, tryModel } = require("./chat-core.js");

/* ---------- .env loader (tiny, no dependency) ---------- */
const ENV_FILE = path.join(__dirname, ".env");
if (fs.existsSync(ENV_FILE)) {
  for (const line of fs.readFileSync(ENV_FILE, "utf8").split(/\r?\n/)) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)\s*$/);
    if (m && !(m[1] in process.env)) process.env[m[1]] = m[2].replace(/^["']|["']$/g, "");
  }
}

const PORT = Number(process.env.PORT || 8787);
const API_KEY = process.env.OPENROUTER_API_KEY || "";

/* ---------- helpers ---------- */
function json(res, code, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(code, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Cache-Control": "no-store",
  });
  res.end(body);
}

function readBody(req, limit = 64 * 1024) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on("data", (c) => {
      size += c.length;
      if (size > limit) { reject(new Error("payload too large")); req.destroy(); return; }
      chunks.push(c);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

/* ---------- static file serving (the /cli folder) ---------- */
const CLI_ROOT = path.resolve(__dirname, "..");
const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".ico": "image/x-icon",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".webmanifest": "application/manifest+json",
};

function serveStatic(req, res, urlPath) {
  // The simulator references site assets one level up (../img, ../css);
  // allow those specific prefixes, everything else stays inside /cli.
  let base = CLI_ROOT;
  let rel = urlPath;
  if (rel.startsWith("/img/") || rel.startsWith("/css/")) base = path.resolve(CLI_ROOT, "..");
  if (rel === "/") rel = "/index.html";

  const file = path.resolve(base, "." + rel);
  if (!file.startsWith(base) || file.startsWith(__dirname)) {   // no traversal, never serve backend/ (.env!)
    res.writeHead(404); res.end("not found"); return;
  }
  fs.readFile(file, (err, buf) => {
    if (err) { res.writeHead(404); res.end("not found"); return; }
    res.writeHead(200, { "Content-Type": MIME[path.extname(file)] || "application/octet-stream" });
    res.end(buf);
  });
}

/* ---------- server ---------- */
const server = http.createServer(async (req, res) => {
  const urlPath = decodeURIComponent((req.url || "/").split("?")[0]);

  // CORS preflight (for when the frontend is hosted elsewhere)
  if (req.method === "OPTIONS") {
    res.writeHead(204, {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Access-Control-Max-Age": "86400",
    });
    res.end();
    return;
  }

  // GET /api/chat doubles as the health/warm-up ping the frontend
  // sends on page load (same shape as /api/health).
  if (req.method === "GET" && (urlPath === "/api/health" || urlPath === "/api/chat")) {
    json(res, 200, { ok: true, model: MODEL(), key: !!API_KEY });
    return;
  }

  if (req.method === "POST" && urlPath === "/api/chat") {
    const stamp = new Date().toISOString().slice(11, 19);
    console.log(`[${stamp}] POST /api/chat received`);
    if (!API_KEY) {
      console.error(`[${stamp}] ✗ OPENROUTER_API_KEY missing — returning 503`);
      json(res, 503, { error: UNAVAILABLE });
      return;
    }
    try {
      const body = JSON.parse(await readBody(req));
      const messages = sanitizeMessages(body.messages);
      if (!messages) {
        console.error(`[${stamp}] ✗ invalid messages payload:`, JSON.stringify(body).slice(0, 300));
        json(res, 400, { error: "invalid messages" });
        return;
      }
      const last = messages[messages.length - 1];
      console.log(`[${stamp}]   payload: ${messages.length} message(s), last: ${JSON.stringify(last.content.slice(0, 120))}`);
      console.log(`[${stamp}]   model chain: ${modelChain().join(" → ")}`);
      const reply = await askOpenRouter(messages, API_KEY, (...a) => console.log(`[${stamp}]`, ...a));
      console.log(`[${stamp}] → 200 { reply: ${JSON.stringify(reply.slice(0, 80))}… }`);
      json(res, 200, { reply });
    } catch (e) {
      // Friendly message to the browser — the REAL error stays here in the console.
      console.error(`[${stamp}] ✗ /api/chat failed: ${e.message}`);
      if (e.body) console.error(`[${stamp}]   openrouter body: ${e.body}`);
      console.error(e.stack);
      const bad = e instanceof SyntaxError || /payload too large|invalid/.test(String(e.message));
      json(res, bad ? 400 : 502, { error: bad ? "bad request" : UNAVAILABLE });
    }
    return;
  }

  if (req.method === "GET" || req.method === "HEAD") {
    serveStatic(req, res, urlPath);
    return;
  }

  res.writeHead(405, { "Allow": "GET, POST, OPTIONS" });
  res.end();
});

server.listen(PORT, async () => {
  console.log(`Seed Code Simulator backend → http://localhost:${PORT}`);
  console.log(`  Model   : ${MODEL()} (fallbacks: ${modelChain().slice(1).join(", ") || "none"})`);
  console.log(`  API Key : ${API_KEY ? "✓ Loaded" : "✗ Missing"}${API_KEY ? ` (${API_KEY.slice(0, 12)}…, ${API_KEY.length} chars)` : " — set OPENROUTER_API_KEY in .env (chat will return 503)"}`);

  // Startup connection test: one tiny request through the fallback chain.
  if (!API_KEY) return;
  console.log("  Testing OpenRouter connection…");
  try {
    const reply = await askOpenRouter(
      [{ role: "user", content: "Reply with the single word: ok" }],
      API_KEY,
      (...a) => console.log("   ", ...a)
    );
    console.log(`  ✓ Connected to OpenRouter — test reply: ${JSON.stringify(reply.slice(0, 60))}`);
  } catch (e) {
    console.error(`  ✗ Connection failed: ${e.message}`);
    if (e.body) console.error(`    body: ${e.body}`);
  }
});
