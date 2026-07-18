/* ============================================================
   Seed Code CLI Simulator — backend/chat-core.js
   Shared AI logic used by BOTH entry points:
     · backend/server.js  — local dev server (python-frontend
       on :8000 talks to this on :8787)
     · /api/chat.js       — Vercel serverless function (prod)
   One OpenRouter key (env, server-side only), one default FREE
   model, no selectors, no auth.
   ============================================================ */

"use strict";

/* ---------- model selection with automatic fallback ----------
   OpenRouter free models come and go (404 when de-listed, 429
   when the upstream provider is saturated). Instead of failing,
   we walk this chain until one answers. Verified against the
   live /models list on 2026-07-19. SEEDCODE_MODEL (if set) is
   always tried first. */
const FREE_MODELS = [
  "meta-llama/llama-3.3-70b-instruct:free",   // default — best quality when not saturated
  "openai/gpt-oss-20b:free",                  // reliable, ~5s (reasoning model)
  "qwen/qwen3-next-80b-a3b-instruct:free",
  "google/gemma-4-31b-it:free",
  "meta-llama/llama-3.2-3b-instruct:free",
  "nvidia/nemotron-3-super-120b-a12b:free",   // slow — last resort
];

const MODEL = () => process.env.SEEDCODE_MODEL || FREE_MODELS[0];

const modelChain = () => [...new Set([MODEL(), ...FREE_MODELS])];

const UNAVAILABLE = "The Seed Code Assistant is temporarily unavailable. Please try again in a few moments.";

const SYSTEM_PROMPT = `You are the Seed Code Assistant, running inside the Seed Code CLI Simulator — a terminal on the official Seed Code CLI website.

Seed Code CLI facts (your primary knowledge — prefer these over anything else):
- Seed Code CLI is a free, open-source (MIT) AI coding assistant that runs in the terminal. Tagline: "Plant ideas. Grow code."
- Created by Al Shahriar Sowan, designed & developed by Eagox Studio. Portfolio: https://alshahriarsayon.vercel.app/ · GitHub: https://github.com/Alshahriar-07/seedcode-cli
- Current version: v1.0.0. Runs on Windows, Linux, and macOS. Requires Python 3.9+ when installed via pip.
- Install: "pip install seedcode-cli" (any platform) or "uv tool install seedcode-cli" (isolated). Windows users can use the standalone SeedCodeSetup.exe installer (no Python needed) from the download page. Linux/macOS also have a ZIP package.
- Providers: OpenRouter (312+ models, 47+ free), ZenMux (unified routing with failover), AeroLink (low-latency regional endpoints), and Ollama (fully local, private, no API key).
- Commands: seedcode (launch), seedcode chat, seedcode config (guided provider/key/theme wizard), seedcode doctor (diagnostics), seedcode models (browse models), seedcode update.
- Configuration lives in ~/.seedcode/config.toml. The SEEDCODE_API_KEY environment variable overrides the config file.
- Features: streaming responses, Markdown rendering, syntax highlighting, themes (Midnight, Paper, Ember, Terminal Classic), fast startup, cross-platform, no telemetry.
- Roadmap: Plugins, MCP, Voice, Memory, Desktop App, Agent Mode.
- Troubleshooting: "command not found" → check PATH or reinstall with uv; auth errors → re-run seedcode config or check SEEDCODE_API_KEY; garbled output → use a truecolor terminal. "seedcode doctor" checks everything.

Your role:
1. Answer questions about Seed Code CLI: installation, features, documentation, troubleshooting.
2. Answer basic programming questions helpfully and correctly.
3. Hold simple, natural conversations.

Style: you are inside a terminal. Be concise — a few short lines or a small list. Plain text only: no Markdown headers, no bold/italic markers, no HTML. Code and commands on their own lines. If unsure about a Seed Code detail, say so and point to the docs or GitHub rather than inventing it.`;

/* Sanitize history from the browser: roles + strings only, capped. */
function sanitizeMessages(raw) {
  if (!Array.isArray(raw)) return null;
  const out = [];
  for (const m of raw.slice(-20)) {
    if (!m || (m.role !== "user" && m.role !== "assistant")) continue;
    if (typeof m.content !== "string" || !m.content.trim()) continue;
    out.push({ role: m.role, content: m.content.slice(0, 4000) });
  }
  return out.length ? out : null;
}

/* One attempt against one model. Returns the reply string.
   Throws with the COMPLETE OpenRouter response body on failure. */
async function tryModel(model, messages, apiKey, log) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), 45_000);
  const t0 = Date.now();
  try {
    const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      signal: ctrl.signal,
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://seedcode-cli.vercel.app/cli/",
        "X-Title": "Seed Code CLI Simulator",
      },
      body: JSON.stringify({
        model,
        messages: [{ role: "system", content: SYSTEM_PROMPT }, ...messages],
        max_tokens: 700,
        temperature: 0.6,
      }),
    });
    const bodyText = await res.text();
    const ms = Date.now() - t0;
    if (!res.ok) {
      // 401/402/403/404/429/500… — log the complete body, never truncate away the reason
      log(`  ✗ ${model} → HTTP ${res.status} (${ms}ms)`);
      log(`    response body: ${bodyText}`);
      const err = new Error(`openrouter ${res.status} on ${model}`);
      err.status = res.status;
      err.body = bodyText;
      throw err;
    }
    let data;
    try { data = JSON.parse(bodyText); }
    catch (e) {
      log(`  ✗ ${model} → HTTP 200 but non-JSON body (${ms}ms): ${bodyText.slice(0, 500)}`);
      throw new Error(`non-json completion from ${model}`);
    }
    const msg = data?.choices?.[0]?.message;
    // Reasoning models (e.g. gpt-oss) may return empty content with the
    // answer only in msg.reasoning — treat empty content as a failure so
    // the chain moves on, but accept content when present.
    const reply = typeof msg?.content === "string" ? msg.content.trim() : "";
    if (!reply) {
      log(`  ✗ ${model} → HTTP 200 but empty content (${ms}ms). message: ${JSON.stringify(msg).slice(0, 400)}`);
      const err = new Error(`empty completion from ${model}`);
      err.body = bodyText;
      throw err;
    }
    log(`  ✓ ${model} → HTTP 200 (${ms}ms), ${reply.length} chars`);
    return reply;
  } finally {
    clearTimeout(timer);
  }
}

/* Walk the free-model chain until one answers.
   `log` defaults to console.error so nothing is ever swallowed. */
async function askOpenRouter(messages, apiKey, log = (...a) => console.error(...a)) {
  const chain = modelChain();
  const errors = [];
  for (const model of chain) {
    try {
      return await tryModel(model, messages, apiKey, log);
    } catch (e) {
      errors.push(`${model}: ${e.message}`);
      // 401/402/403 are key/account problems — retrying other models won't help
      if (e.status === 401 || e.status === 402 || e.status === 403) {
        log(`  ✗ auth/billing error (${e.status}) — aborting fallback chain`);
        log(e.stack);
        throw e;
      }
      // 404 (de-listed) / 429 (saturated) / 5xx / empty → try next model
    }
  }
  const err = new Error(`all models failed:\n  ${errors.join("\n  ")}`);
  log(err.stack);
  throw err;
}

module.exports = { MODEL, FREE_MODELS, modelChain, UNAVAILABLE, SYSTEM_PROMPT, sanitizeMessages, askOpenRouter, tryModel };
