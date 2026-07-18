/* ============================================================
   Vercel serverless function — POST /api/chat  (production)
   Thin wrapper only: all AI logic, the system prompt, and the
   model live in /cli/backend/chat-core.js (shared with the
   local dev server at /cli/backend/server.js).

   Set OPENROUTER_API_KEY in the Vercel project env vars.
   The key never reaches the browser.
   ============================================================ */

"use strict";

const { MODEL, UNAVAILABLE, sanitizeMessages, askOpenRouter } = require("../cli/backend/chat-core.js");

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    res.setHeader("Access-Control-Allow-Headers", "Content-Type");
    res.status(204).end();
    return;
  }
  // GET = health/warm-up ping from the frontend on page load — also
  // warms this serverless function so the first prompt is faster.
  if (req.method === "GET") {
    res.setHeader("Cache-Control", "no-store");
    res.status(200).json({ ok: true, model: MODEL(), key: !!process.env.OPENROUTER_API_KEY });
    return;
  }
  if (req.method !== "POST") {
    res.setHeader("Allow", "GET, POST, OPTIONS");
    res.status(405).json({ error: "method not allowed" });
    return;
  }

  const apiKey = process.env.OPENROUTER_API_KEY || "";
  if (!apiKey) { res.status(503).json({ error: UNAVAILABLE }); return; }

  try {
    // Vercel parses JSON bodies automatically; tolerate raw strings too.
    const body = typeof req.body === "string" ? JSON.parse(req.body) : (req.body || {});
    const messages = sanitizeMessages(body.messages);
    if (!messages) { res.status(400).json({ error: "invalid messages" }); return; }
    const reply = await askOpenRouter(messages, apiKey, (...a) => console.log("[/api/chat]", ...a));
    res.setHeader("Cache-Control", "no-store");
    res.status(200).json({ reply });
  } catch (e) {
    // Friendly message to the browser — full detail in the function logs.
    console.error("[/api/chat] FAILED:", e && e.message ? e.message : e);
    if (e && e.body) console.error("[/api/chat] openrouter body:", e.body);
    if (e && e.stack) console.error(e.stack);
    const bad = e instanceof SyntaxError || /invalid/.test(String(e && e.message));
    res.status(bad ? 400 : 502).json({ error: bad ? "bad request" : UNAVAILABLE });
  }
};
