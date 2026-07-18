/* ============================================================
   Seed Code CLI Simulator — script.js
   A complete terminal: boot sequence, command engine, history,
   tab completion, themes, matrix mode, neofetch, scripted demo.
   Natural-language questions go to the Seed Code Assistant via
   the /cli backend (see backend/server.js); built-in offline
   answers remain as a fallback when the backend is unreachable.
   ============================================================ */

(function () {
  "use strict";

  /* ---------- DOM ---------- */
  const screen = document.getElementById("screen");
  const output = document.getElementById("output");
  const inputRow = document.getElementById("input-row");
  const inputText = document.getElementById("input-text");
  const kbd = document.getElementById("kbd");
  const statusLeft = document.getElementById("status-left");
  const matrixCanvas = document.querySelector(".matrix-canvas");

  const motionOK = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const wait = (ms) => new Promise((r) => setTimeout(r, motionOK ? ms : 0));

  /* ---------- state ---------- */
  const state = {
    buffer: "",
    history: [],
    histIdx: -1,
    busy: true,          // true during boot/animations — input locked
    provider: "Not selected",
    backend: "--",
    model: "Not selected",
    status: "Not configured",
    theme: "dark",
  };

  const VERSION = "v1.3.0";
  const GH = "https://github.com/Alshahriar-07/seedcode-cli";
  const PF = "https://alshahriarsayon.vercel.app/";

  /* ============================================================
     Output helpers — esc() everything user-controlled, then
     inject span markup via tokens: {g:text} green, {w:} white,
     {d:} dim, {m:} muted, {y:} yellow, {r:} red, {c:} cyanish,
     {b:} bold, {a:url|label} link
     ============================================================ */
  const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  function markup(safe) {
    return safe
      .replace(/\{a:([^|{}]+)\|([^{}]+)\}/g, '<a class="c-link" href="$1" target="_blank" rel="noopener">$2</a>')
      .replace(/\{g:([^{}]*)\}/g, '<span class="c-green">$1</span>')
      .replace(/\{G:([^{}]*)\}/g, '<span class="c-ghi">$1</span>')
      .replace(/\{w:([^{}]*)\}/g, '<span class="c-white">$1</span>')
      .replace(/\{d:([^{}]*)\}/g, '<span class="c-dim">$1</span>')
      .replace(/\{m:([^{}]*)\}/g, '<span class="c-mut">$1</span>')
      .replace(/\{y:([^{}]*)\}/g, '<span class="c-yel">$1</span>')
      .replace(/\{r:([^{}]*)\}/g, '<span class="c-red">$1</span>')
      .replace(/\{c:([^{}]*)\}/g, '<span class="c-cyanish">$1</span>')
      .replace(/\{b:([^{}]*)\}/g, '<span class="c-bold">$1</span>');
  }

  function block(html, cls) {
    const div = document.createElement("div");
    div.className = "t-block" + (cls ? " " + cls : "");
    div.innerHTML = html;
    output.appendChild(div);
    scrollDown();
    return div;
  }

  const print = (text, cls) => block(markup(esc(text)), cls);
  const printRaw = (tokenText, cls) => block(markup(tokenText), cls);
  const blank = () => print(" ");
  const scrollDown = () => { screen.scrollTop = screen.scrollHeight; };

  /* stream a multi-line answer word-by-word */
  async function stream(tokenText, cls) {
    const div = block("", cls);
    const words = tokenText.split(/(\s+)/);
    let acc = "";
    for (const wd of words) {
      acc += wd;
      div.innerHTML = markup(acc);
      scrollDown();
      if (wd.trim()) await wait(14);
    }
    return div;
  }

  /* thinking spinner */
  async function think(label, ms) {
    const frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
    const div = block(`<span class="spinner">${frames[0]}</span> <span class="c-dim">${esc(label)}</span>`);
    const t0 = performance.now();
    let i = 0;
    while (performance.now() - t0 < (motionOK ? ms : 0)) {
      i = (i + 1) % frames.length;
      div.innerHTML = `<span class="spinner">${frames[i]}</span> <span class="c-dim">${esc(label)}</span>`;
      await wait(66);
    }
    div.remove();
  }

  /* echo the prompt + a command into the scrollback */
  function echoCmd(cmd) {
    printRaw(`{g:seedcode}{d: on }{c:~/projects}{g: ❯} {w:${esc(cmd)}}`);
  }

  /* ============================================================
     Banner — 1:1 recreation of the real CLI startup screen.
     Real <pre> columns inside a CSS grid: every space preserved,
     no divs/spans doing layout. Widths are computed in characters.
     ============================================================ */
  const LOGO = [
    "███████╗███████╗███████╗██████╗      ██████╗ ██████╗ ██████╗ ███████╗",
    "██╔════╝██╔════╝██╔════╝██╔══██╗    ██╔════╝██╔═══██╗██╔══██╗██╔════╝",
    "███████╗█████╗  █████╗  ██║  ██║    ██║     ██║   ██║██║  ██║█████╗  ",
    "╚════██║██╔══╝  ██╔══╝  ██║  ██║    ██║     ██║   ██║██║  ██║██╔══╝  ",
    "███████║███████╗███████╗██████╔╝    ╚██████╗╚██████╔╝██████╔╝███████╗",
    "╚══════╝╚══════╝╚══════╝╚═════╝      ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝",
  ];

  const pad = (s, n) => (s.length > n ? s.slice(0, n) : s + " ".repeat(n - s.length));
  const centerIn = (s, w) => {
    const l = Math.max(0, Math.floor((w - s.length) / 2));
    return pad(" ".repeat(l) + s, w);
  };

  function banner() {
    const W_L = 73;   // left column width (chars)
    const W_R = 44;   // right column width (chars)
    // middle row: "│ " + left + " │ " + right + " │"  = 2+73+3+44+2
    const TOTAL = 2 + W_L + 3 + W_R + 2;

    // left column — logo block centered like the real CLI
    const leftLines = [
      "",
      ...LOGO.map((l) => pad("  " + l, W_L)),
      "",
      centerIn("Plant ideas. Grow code.", W_L),
      "",
      centerIn("Created by Al Shahriar Sowan", W_L),
    ];

    // right column — session panel
    const kv = (k, v) => pad(`${k} : ${v}`, W_R);
    const rightLines = [
      "",
      pad("Current Session", W_R),
      pad("─".repeat(25), W_R),
      "",
      kv("Provider", state.provider),
      kv("Backend ", state.backend),
      kv("Model   ", state.model),
      kv("Status  ", state.status),
      kv("Context ", "--"),
      kv("History ", "Enabled"),
      "",
      "",
    ];
    while (rightLines.length < leftLines.length) rightLines.push("");
    while (leftLines.length < rightLines.length) leftLines.push("");
    const rows = leftLines.length;

    // colorize left: logo lines bright green, text lines muted
    const leftHtml = leftLines
      .map((l, i) => {
        const e = esc(pad(l, W_L));
        return i >= 1 && i <= 6 ? `<span class="c-ghi">${e}</span>` : `<span class="bl-tag">${e}</span>`;
      })
      .join("\n");

    // colorize right: title white, rule dim, values cyanish
    const rightHtml = rightLines
      .map((l, i) => {
        const e = esc(pad(l, W_R));
        if (i === 1) return `<span class="br-title">${e}</span>`;
        if (i === 2) return `<span class="br-rule">${e}</span>`;
        const m = pad(l, W_R).match(/^(\S+\s*) : (.*)$/);
        if (m) return `${esc(m[1])} : <span class="br-val">${esc(m[2])}</span>`;
        return e;
      })
      .join("\n");

    const title = " Seed Code " + VERSION + " ";
    const inner = TOTAL - 2;
    const top = "╭─" + `<span class="bt-title">${esc(title)}</span>` + "─".repeat(Math.max(0, inner - 1 - title.length)) + "╮";
    const bottom = "╰" + "─".repeat(inner) + "╯";
    const col = (s) => Array(rows).fill(s).join("\n");

    const div = document.createElement("div");
    div.className = "t-block banner";
    div.innerHTML =
      `<pre class="banner-top">${top}</pre>` +
      `<div class="banner-mid">` +
      `<pre class="banner-edge">${esc(col("│ "))}</pre>` +
      `<pre class="banner-left">${leftHtml}</pre>` +
      `<pre class="banner-sep">${esc(col(" │ "))}</pre>` +
      `<pre class="banner-right">${rightHtml}</pre>` +
      `<pre class="banner-edge">${esc(col(" │"))}</pre>` +
      `</div>` +
      `<pre class="banner-bottom">${bottom}</pre>`;
    output.appendChild(div);
    scrollDown();
  }

  /* ============================================================
     Command registry
     ============================================================ */
  const COMMANDS = {};
  const cmd = (names, fn, desc) => {
    names.split("|").forEach((n, i) => { COMMANDS[n] = { fn, desc, primary: i === 0 }; });
  };

  const HELP_ROWS = [
    ["help", "Show this help panel"],
    ["about", "What Seed Code CLI is"],
    ["features", "Everything the CLI can do"],
    ["demo", "Run a scripted AI session"],
    ["status", "Current session status"],
    ["provider / model / backend", "Configure the fake session"],
    ["neofetch", "System info, beautifully"],
    ["logo", "The full ASCII logo"],
    ["theme dark|light|hacker", "Switch the terminal theme"],
    ["matrix", "Enter the matrix (again to exit)"],
    ["history / clear / version", "Terminal utilities"],
    ["download / docs / github", "Project links"],
    ["creator / portfolio / credits", "Who built this"],
    ["whoami / date / time / license", "Small utilities"],
    ["roadmap / faq / contact", "Project info"],
    ["exit", "Try it :)"],
  ];

  cmd("help", async () => {
    printRaw(`{w:Seed Code CLI — commands}`);
    blank();
    for (const [c, d] of HELP_ROWS) {
      printRaw(`  {g:${c.padEnd(28)}}{m:${d}}`);
    }
    blank();
    printRaw(`{d:You can also ask natural questions — try }{c:"what is seed code"}{d: or click a chip above.}`);
  }, "Show help");

  cmd("clear|cls", async () => { output.innerHTML = ""; }, "Clear terminal");

  cmd("version|--version|-v", async () => {
    printRaw(`{g:seedcode} {w:${VERSION}} {d:(simulator build — the real CLI ships as v1.0.0)}`);
  }, "Version");

  cmd("about", async () => {
    await stream(`{w:Seed Code CLI} is the beautiful AI coding assistant for your terminal. Fast, elegant, and built for developers — connect to {c:OpenRouter}, {c:ZenMux}, {c:AeroLink}, or run fully local with {c:Ollama}, and get streaming answers with Markdown rendering and syntax highlighting without ever leaving your shell.`);
    blank();
    printRaw(`{d:Free & open source · MIT license · }{a:${GH}|github.com/Alshahriar-07/seedcode-cli}`);
  }, "About");

  cmd("whoami", async () => {
    printRaw(`{c:guest}{d:@}{g:seedcode-simulator}`);
    printRaw(`{d:A curious developer, one command away from a better terminal.}`);
  }, "Who am I");

  cmd("logo|seedcode", async () => {
    blank();
    for (const line of LOGO) { printRaw(`{G:${line}}`, "t-box"); await wait(70); }
    blank();
    printRaw(`{m:${centerIn("Plant ideas. Grow code.", LOGO[0].length)}}`);
    blank();
  }, "ASCII logo");

  cmd("history", async () => {
    if (!state.history.length) { printRaw(`{d:history is empty — type something first.}`); return; }
    state.history.forEach((h, i) => printRaw(`  {d:${String(i + 1).padStart(3)}}  {w:${esc(h)}}`));
  }, "Command history");

  cmd("date", async () => { printRaw(`{c:${new Date().toDateString()}}`); }, "Date");
  cmd("time", async () => { printRaw(`{c:${new Date().toLocaleTimeString()}}`); }, "Time");

  cmd("status", async () => {
    printRaw(`{w:Current Session}`);
    printRaw(`{d:${"─".repeat(25)}}`);
    printRaw(`  {m:Provider :} {c:${state.provider}}`);
    printRaw(`  {m:Backend  :} {c:${state.backend}}`);
    printRaw(`  {m:Model    :} {c:${state.model}}`);
    printRaw(`  {m:Status   :} ${state.status === "Ready" ? "{g:● Ready}" : "{y:○ " + state.status + "}"}`);
    printRaw(`  {m:Context  :} {c:--}`);
    printRaw(`  {m:History  :} {c:Enabled}`);
  }, "Session status");

  cmd("provider", async (args) => {
    const known = { openrouter: "OpenRouter", zenmux: "ZenMux", aerolink: "AeroLink", ollama: "Ollama" };
    if (!args) {
      printRaw(`{w:Available providers}`);
      Object.values(known).forEach((p) => printRaw(`  {g:●} {c:${p}}`));
      blank();
      printRaw(`{d:Select one: }{g:provider openrouter}`);
      return;
    }
    const key = args.toLowerCase().trim();
    if (known[key]) {
      await think("Connecting to " + known[key] + "…", 900);
      state.provider = known[key];
      state.backend = key === "ollama" ? "local" : "cloud";
      state.status = state.model !== "Not selected" ? "Ready" : "Model not selected";
      printRaw(`{g:✓} Provider set to {c:${known[key]}} {d:(${state.backend})}`);
      if (state.model === "Not selected") printRaw(`{d:Now pick a model: }{g:model glm-5.2}`);
    } else {
      printRaw(`{r:✗ Unknown provider:} {w:${esc(args)}} {d:— try openrouter, zenmux, aerolink, or ollama}`);
    }
    updateStatusbar();
  }, "Set provider");

  cmd("model", async (args) => {
    const models = ["glm-5.2", "qwen-max", "llama3", "deepseek-v3", "mistral-large"];
    if (!args) {
      printRaw(`{w:Popular models}`);
      models.forEach((m) => printRaw(`  {g:●} {c:${m}}`));
      blank();
      printRaw(`{d:Select one: }{g:model glm-5.2}`);
      return;
    }
    await think("Loading model card…", 700);
    state.model = args.trim();
    state.status = state.provider !== "Not selected" ? "Ready" : "Provider not selected";
    printRaw(`{g:✓} Model set to {c:${esc(state.model)}}`);
    if (state.provider === "Not selected") printRaw(`{d:Now pick a provider: }{g:provider openrouter}`);
    updateStatusbar();
  }, "Set model");

  cmd("backend", async () => {
    printRaw(`  {m:Backend :} {c:${state.backend}}`);
    printRaw(`{d:The backend follows your provider — cloud for OpenRouter/ZenMux/AeroLink, local for Ollama.}`);
  }, "Backend info");

  cmd("creator", async () => {
    printRaw(`{w:Al Shahriar Sowan} {d:· Developer · Founder of Eagox Studio}`);
    await stream(`{m:Creator of Seed Code CLI — building developer tools that feel as good as they function.}`);
    printRaw(`{d:Portfolio: }{a:${PF}|alshahriarsayon.vercel.app}  {d:· GitHub: }{a:https://github.com/Alshahriar-07|Alshahriar-07}`);
  }, "Creator");

  cmd("portfolio", async () => {
    printRaw(`{g:→} Opening portfolio… {a:${PF}|alshahriarsayon.vercel.app}`);
  }, "Portfolio link");

  cmd("github|repo", async () => {
    printRaw(`{g:→} {a:${GH}|github.com/Alshahriar-07/seedcode-cli}`);
    printRaw(`{d:Stars, issues, and pull requests all welcome.}`);
  }, "GitHub link");

  cmd("download|install", async () => {
    printRaw(`{w:Get Seed Code CLI}`);
    blank();
    printRaw(`  {d:#} {m:Any platform (Python 3.9+)}`);
    printRaw(`  {g:$} {w:pip install seedcode-cli}`);
    blank();
    printRaw(`  {d:#} {m:Isolated install}`);
    printRaw(`  {g:$} {w:uv tool install seedcode-cli}`);
    blank();
    printRaw(`  {d:#} {m:Windows installer (no Python needed)}`);
    printRaw(`  {g:→} {a:../download.html|SeedCodeSetup.exe from the download page}`);
    blank();
    printRaw(`  {d:#} {m:Linux & macOS ZIP}`);
    printRaw(`  {g:→} {a:https://mega.nz/file/pIU0HaJB#nX8HW3f6hBtan1nHuwvzaWujChjtpw8eA6zYFH0NZRQ|Download ZIP from MEGA}`);
  }, "Download");

  cmd("docs|documentation", async () => {
    printRaw(`{g:→} {a:../docs.html|Documentation} {d:· installation, commands, configuration, providers}`);
  }, "Docs");

  cmd("faq", async () => {
    printRaw(`{g:→} {a:../faq.html|FAQ} {d:· pricing, platforms, providers, API keys}`);
  }, "FAQ");

  cmd("contact|support", async () => {
    printRaw(`{w:Get in touch}`);
    printRaw(`  {m:Issues   :} {a:${GH}/issues|GitHub Issues}`);
    printRaw(`  {m:Creator  :} {a:${PF}|Portfolio site}`);
    printRaw(`  {m:Support  :} {a:../support.html|Support page}`);
  }, "Contact");

  cmd("features", async () => {
    const rows = [
      ["Streaming responses", "tokens render the instant they arrive"],
      ["OpenRouter support", "hundreds of models, one API key"],
      ["Ollama — fully local", "private, offline, no API key"],
      ["FreeModel & AeroLink", "zero-billing start, low-latency endpoints"],
      ["Markdown rendering", "headings, lists, tables in the terminal"],
      ["Syntax highlighting", "answers read like your editor"],
      ["Cross platform", "Windows, Linux, macOS"],
      ["Themes", "Midnight, Paper, Ember, Terminal Classic"],
      ["Config system", "one versionable TOML + guided wizard"],
      ["Fast startup", "ready in milliseconds"],
    ];
    printRaw(`{w:Features}`);
    blank();
    for (const [k, v] of rows) {
      printRaw(`  {g:✓} {c:${k.padEnd(22)}}{m:${v}}`);
      await wait(60);
    }
  }, "Features");

  cmd("roadmap", async () => {
    printRaw(`{w:Roadmap}`);
    blank();
    printRaw(`  {g:✓ shipped}  {c:CLI · Streaming · Themes · Configuration · 4 providers}`);
    printRaw(`  {y:◌ planned}  {m:Plugins · MCP · Voice · Memory · Desktop App · Agent Mode}`);
    blank();
    printRaw(`{d:Full details: }{a:../changelog.html|changelog & roadmap}`);
  }, "Roadmap");

  cmd("license", async () => {
    printRaw(`{w:MIT License} {d:© 2026 Eagox Studio · Seed Code CLI}`);
    printRaw(`{d:Free to use, modify, and distribute. }{a:${GH}/blob/main/LICENSE|Read the license}`);
  }, "License");

  cmd("credits", async () => {
    printRaw(`{w:Credits}`);
    printRaw(`  {m:Design & Development :} {c:Eagox Studio}`);
    printRaw(`  {m:Creator              :} {c:Al Shahriar Sowan}`);
    printRaw(`  {m:Typeface             :} {c:JetBrains Mono}`);
    printRaw(`  {m:Powered by           :} {c:HTML · CSS · JavaScript — nothing else}`);
  }, "Credits");

  cmd("exit|quit|logout", async () => {
    printRaw(`{d:There is no escape from the terminal. }{g:;)}`);
    await wait(600);
    printRaw(`{d:(fine — }{a:../index.html|back to the website}{d:)}`);
  }, "Exit");

  cmd("theme", async (args) => {
    const t = (args || "").trim().toLowerCase();
    if (["dark", "light", "hacker"].includes(t)) {
      document.body.dataset.theme = t;
      state.theme = t;
      printRaw(`{g:✓} Theme switched to {c:${t}}`);
    } else {
      printRaw(`{w:Themes:} {c:dark}{d:, }{c:light}{d:, }{c:hacker}`);
      printRaw(`{d:Usage: }{g:theme hacker}`);
    }
  }, "Theme");

  cmd("matrix", async () => {
    const on = document.body.classList.toggle("matrix-on");
    if (on) {
      startMatrix();
      printRaw(`{G:Wake up, Neo…} {d:type }{g:matrix}{d: again to exit.}`);
    } else {
      stopMatrix();
      printRaw(`{d:Back to reality.}`);
    }
  }, "Matrix mode");

  cmd("neofetch|sysinfo", async () => {
    const t = state.theme;
    const art = [
      "      {G:.--.}      ",
      "     {G:/ {} \\\\}     ",
      "    {G:| 🌱 |}    ",
      "     {G:\\\\ __ /}     ",
      "      {G:'--'}      ",
    ];
    const info = [
      `{c:guest}{d:@}{c:seedcode}`,
      `{d:${"─".repeat(22)}}`,
      `{m:OS       :} {w:Seed Code Simulator}`,
      `{m:Host     :} {w:Your Browser}`,
      `{m:Kernel   :} {w:seedcode ${VERSION}}`,
      `{m:Shell    :} {w:zsh (simulated)}`,
      `{m:Theme    :} {w:${t}}`,
      `{m:Provider :} {w:${state.provider}}`,
      `{m:Model    :} {w:${state.model}}`,
      `{m:Uptime   :} {w:${Math.round(performance.now() / 1000)}s}`,
      `{m:License  :} {w:MIT}`,
      ` `,
      `{g:███}{G:███}{y:███}{r:███}{c:███}{w:███}{d:███}`,
    ];
    const lines = Math.max(art.length, info.length);
    for (let i = 0; i < lines; i++) {
      printRaw(`  ${art[i] || " ".repeat(16)}   ${info[i] || ""}`, "t-box");
      await wait(40);
    }
  }, "Neofetch");

  cmd("demo", async () => {
    printRaw(`{d:Running scripted demo — sit back…}`);
    blank();
    await wait(400);
    echoCmd("provider openrouter");
    await think("Connecting to OpenRouter…", 900);
    state.provider = "OpenRouter"; state.backend = "cloud";
    printRaw(`{g:✓} Provider set to {c:OpenRouter} {d:(cloud)}`);
    await wait(350);
    echoCmd("model glm-5.2");
    await think("Loading model card…", 700);
    state.model = "glm-5.2"; state.status = "Ready";
    updateStatusbar();
    printRaw(`{g:✓} Model set to {c:glm-5.2}`);
    await wait(350);
    blank();
    echoCmd('seedcode "Build a REST API using FastAPI"');
    await think("Thinking…", 1200);
    printRaw(`{g:✓} {w:Planning}`);
    await wait(420);
    printRaw(`{g:✓} {w:Writing files}`);
    await wait(420);
    printRaw(`{g:✓} {w:Generating code}`);
    await wait(420);
    printRaw(`{d:──────────────────────────────────────────}`);
    await stream(`{c:from} {w:fastapi} {c:import} {w:FastAPI}\n\n{w:app} = {w:FastAPI}()\n\n{g:@app.get}({y:"/"}) \n{c:async def} {w:root}():\n    {c:return} {{}{y:"message"}: {y:"Hello, Seed Code!"}{}}`, "t-box");
    printRaw(`{d:──────────────────────────────────────────}`);
    printRaw(`{g:✓} {w:Finished in 4.2s} {d:· 62 tokens · streamed}`);
    blank();
    printRaw(`{d:That's the real workflow. }{g:pip install seedcode-cli}{d: to get it.}`);
  }, "Scripted demo");

  /* ============================================================
     Natural-language questions
     ============================================================ */
  const QA = [
    {
      match: /what\s+is\s+seed\s*(code|bot)|what does seed\s*(code|bot) do|^what is cli/,
      answer: async () => {
        await stream(`{w:Seed Code CLI} is an AI coding assistant that lives in your terminal. Ask questions, generate code, debug errors — with {c:streaming responses}, {c:Markdown rendering}, and {c:syntax highlighting}, connected to the AI provider of your choice.`);
        printRaw(`{d:Try }{g:features}{d: or }{g:demo}{d: to see it in action.}`);
      },
    },
    {
      match: /how\s+does\s+seed\s*code\s+work/,
      answer: async () => {
        await stream(`You type a prompt, Seed Code sends it {c:directly} to your configured provider (OpenRouter, ZenMux, AeroLink, or local Ollama), and streams the answer back token-by-token — rendered beautifully in your terminal. No middleman servers, no telemetry.`);
      },
    },
    {
      match: /why\s+is\s+.*free|is\s+it\s+free|price|pricing|cost/,
      answer: async () => {
        await stream(`Seed Code CLI is {g:100% free and open source} under the MIT license. There's nothing to buy — you bring your own provider key, and through {c:OpenRouter} you can use {c:47+ models entirely for free}. With {c:Ollama}, everything runs locally at zero cost.`);
      },
    },
    {
      match: /who\s+(created|made|built)|who is al|about\s+the\s+creator|who is the creator/,
      answer: async () => run("creator"),
    },
    {
      match: /what\s+is\s+eagox/,
      answer: async () => {
        await stream(`{w:Eagox Studio} is the studio behind Seed Code CLI — founded by {c:Al Shahriar Sowan} to build developer tools that feel as good as they function. It designed and developed both the CLI and this website.`);
      },
    },
    {
      match: /provider|what.*(providers|apis).*(supported|available)/,
      answer: async () => {
        printRaw(`{w:Supported providers}`);
        printRaw(`  {g:●} {c:OpenRouter} {d:— hundreds of models, incl. free tiers}`);
        printRaw(`  {g:●} {c:ZenMux}     {d:— unified routing with failover}`);
        printRaw(`  {g:●} {c:AeroLink}   {d:— low-latency regional endpoints}`);
        printRaw(`  {g:●} {c:Ollama}     {d:— fully local & private, no API key}`);
        blank();
        printRaw(`{d:Try one here: }{g:provider openrouter}`);
      },
    },
    {
      match: /can\s+i\s+use\s+openrouter|openrouter\s+setup/,
      answer: async () => {
        await stream(`Yes — {c:OpenRouter} is the flagship provider. One API key unlocks {c:312+ models}, including {c:47+ free-tier} ones. In the real CLI: run {g:seedcode config}, pick OpenRouter, paste your key. Try it here with {g:provider openrouter}.`);
      },
    },
    {
      match: /can\s+i\s+use\s+(claude|gemini|gpt|glm)/,
      answer: async (q) => {
        const m = q.match(/claude|gemini|gpt|glm/)[0].toUpperCase();
        await stream(`Yes — {c:${m}}-family models are available {c:through OpenRouter}, alongside hundreds of others. One key, every model. Run {g:seedcode models} in the real CLI to browse what's live.`);
      },
    },
    {
      match: /how\s+to\s+install|install\s+command|show\s+install/,
      answer: async () => run("download"),
    },
    {
      match: /how\s+to\s+update/,
      answer: async () => {
        printRaw(`  {g:$} {w:seedcode update}     {d:# in-place update}`);
        printRaw(`  {g:$} {w:pip install -U seedcode-cli}     {d:# via pip}`);
      },
    },
    {
      match: /how\s+to\s+uninstall/,
      answer: async () => {
        printRaw(`  {g:$} {w:pip uninstall seedcode-cli}`);
        printRaw(`  {g:$} {w:uv tool uninstall seedcode-cli}`);
        printRaw(`{d:(We'll miss you.)}`);
      },
    },
    {
      match: /operating\s+systems|what\s+os|platforms.*supported|does\s+it\s+support\s+windows|windows|linux|mac/,
      answer: async () => {
        await stream(`Seed Code runs natively on {c:Windows} (Windows Terminal, PowerShell, cmd), {c:Linux} (bash, zsh, fish), and {c:macOS} (Terminal.app, iTerm2, Warp). Windows gets a standalone installer; Linux/macOS a ZIP package or pip.`);
      },
    },
    {
      match: /streaming/,
      answer: async () => {
        await stream(`Yes — {c:streaming is the default}. Tokens render the instant they arrive, exactly like the answers appearing in this simulator. It works across every provider, even over SSH.`);
      },
    },
    {
      match: /open\s+source|is\s+it\s+open/,
      answer: async () => {
        await stream(`Fully. {g:MIT licensed}, developed in the open at {a:${GH}|github.com/Alshahriar-07/seedcode-cli}. Read the source, file issues, ship improvements.`);
      },
    },
    {
      match: /where.*github|github.*link/,
      answer: async () => run("github"),
    },
    {
      match: /how.*contribute/,
      answer: async () => {
        await stream(`Fork the repo, make your change, open a pull request — contributions of every size are welcome. Bug reports and feature ideas go to {a:${GH}/issues|GitHub Issues}. Clear reproduction steps get the fastest reviews.`);
      },
    },
    {
      match: /report\s+bugs?|found\s+a\s+bug/,
      answer: async () => {
        printRaw(`{g:→} {a:${GH}/issues|Open an issue on GitHub} {d:— include your OS, terminal, and }{g:seedcode doctor}{d: output.}`);
      },
    },
    {
      match: /documentation|is\s+there\s+docs/,
      answer: async () => run("docs"),
    },
    {
      match: /roadmap/,
      answer: async () => run("roadmap"),
    },
    {
      match: /show\s+examples?|example/,
      answer: async () => {
        printRaw(`{w:Real-world examples}`);
        blank();
        printRaw(`  {g:$} {w:seedcode "write a haiku about git"}`);
        printRaw(`    {d:branches drift apart / a merge brings them home again / conflicts, then release}`);
        blank();
        printRaw(`  {g:$} {w:seedcode chat}   {d:# interactive session with context}`);
        printRaw(`  {g:$} {w:seedcode doctor} {d:# 6-point health check}`);
        printRaw(`  {g:$} {w:seedcode models} {d:# browse 312+ models}`);
        blank();
        printRaw(`{d:Run }{g:demo}{d: to watch a full session.}`);
      },
    },
    {
      match: /getting\s+started|how\s+do\s+i\s+start|quick\s*start/,
      answer: async () => {
        printRaw(`{w:Getting started — 3 steps}`);
        printRaw(`  {g:1.} {w:pip install seedcode-cli}`);
        printRaw(`  {g:2.} {w:seedcode config}   {d:# guided provider setup}`);
        printRaw(`  {g:3.} {w:seedcode}          {d:# you're in}`);
      },
    },
  ];

  /* ============================================================
     AI assistant — talks ONLY to the backend (which holds the
     OpenRouter key). History lives in sessionStorage for the
     current browser session; no accounts, no database.
     The QA list above remains as an offline fallback.

     Endpoint auto-detection (single, centralized config):
       · localhost / 127.0.0.1  → http://localhost:8787/api/chat
         (python -m http.server 8000 + node backend/server.js)
       · any deployed domain    → /api/chat  (Vercel function)
     No manual edits needed between dev and production.
     ============================================================ */
  const AI_UNAVAILABLE = "The Seed Code Assistant is temporarily unavailable. Please try again in a few moments.";
  const AI = {
    // ── all of this initializes at script load, NOT lazily ──
    endpoint: (() => {
      const h = location.hostname;
      const local = h === "localhost" || h === "127.0.0.1" || h === "[::1]";
      // Dev: unless the page is already served BY the backend (:8787),
      // the API lives on its own port. Prod: same-origin serverless fn.
      if (local && location.port !== "8787") return "http://localhost:8787/api/chat";
      return "/api/chat";
    })(),
    history: (() => {
      try { return JSON.parse(sessionStorage.getItem("sc-sim-chat") || "[]"); }
      catch (e) { return []; }
    })(),
    ready: false,          // flipped by the startup warm-up (or first reply)
    warming: false,
  };

  /* ---------- startup warm-up ----------
     Runs immediately when the simulator loads: pings the backend
     (GET /api/chat = health) so the connection — and on Vercel the
     serverless function — is warm before the first prompt. Retries
     silently in the background with backoff; never blocks the UI,
     and askAI() never waits for it (a prompt always POSTs at once). */
  function warmUpBackend(attempt = 0) {
    if (AI.ready || AI.warming) return;
    AI.warming = true;
    fetch(AI.endpoint, { method: "GET" })
      .then((res) => (res.ok ? res.json() : Promise.reject(new Error("http " + res.status))))
      .then((info) => {
        AI.ready = true;
        AI.warming = false;
        console.log("[seedcode-sim] backend ready", { url: AI.endpoint, info });
      })
      .catch((e) => {
        AI.warming = false;
        console.warn(`[seedcode-sim] backend warm-up attempt ${attempt + 1} failed`, { url: AI.endpoint, error: String(e) });
        setTimeout(() => warmUpBackend(attempt + 1), Math.min(30_000, 2000 * 2 ** attempt));
      });
  }
  warmUpBackend();

  async function askAI(prompt) {
    const messages = [...AI.history, { role: "user", content: prompt }].slice(-20);
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 35_000);
    try {
      let res;
      try {
        res = await fetch(AI.endpoint, {
          method: "POST",
          signal: ctrl.signal,
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ messages }),
        });
      } catch (netErr) {
        // network-level failure (backend down, CORS, DNS, abort)
        console.error("[seedcode-sim] network error", { url: AI.endpoint, error: String(netErr) });
        throw netErr;
      }
      if (!res.ok) {
        const body = await res.text().catch(() => "");
        console.error("[seedcode-sim] /api/chat failed", { url: AI.endpoint, status: res.status, body: body.slice(0, 500) });
        throw new Error("http " + res.status);
      }
      const data = await res.json();
      if (typeof data.reply !== "string" || !data.reply.trim()) {
        console.error("[seedcode-sim] bad reply shape", { url: AI.endpoint, data });
        throw new Error("bad reply");
      }
      AI.history = [...messages, { role: "assistant", content: data.reply }].slice(-20);
      try { sessionStorage.setItem("sc-sim-chat", JSON.stringify(AI.history)); } catch (e) { /* full/blocked */ }
      AI.ready = true;
      return data.reply;
    } catch (e) {
      AI.ready = false;
      warmUpBackend();                       // recover silently in the background
      throw e;
    } finally {
      clearTimeout(timer);
    }
  }

  /* spinner that runs while a promise is in flight */
  async function withSpinner(label, promise) {
    const frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"];
    let i = 0;
    const div = block(`<span class="spinner">${frames[0]}</span> <span class="c-dim">${esc(label)}</span>`);
    const iv = setInterval(() => {
      i = (i + 1) % frames.length;
      div.innerHTML = `<span class="spinner">${frames[i]}</span> <span class="c-dim">${esc(label)}</span>`;
    }, 66);
    try { return await promise; }
    finally { clearInterval(iv); div.remove(); }
  }

  /* stream plain text word-by-word via textContent — AI output is
     never parsed as markup tokens or HTML */
  async function streamText(text) {
    const div = block("");
    const words = text.split(/(\s+)/);
    let acc = "";
    for (const wd of words) {
      acc += wd;
      div.textContent = acc;
      scrollDown();
      if (wd.trim()) await wait(14);
    }
    return div;
  }

  /* offline fallback: unavailable notice + canned answer if we have one */
  async function offlineFallback(lower) {
    printRaw(`{y:⚠ ${esc(AI_UNAVAILABLE)}}`);
    for (const qa of QA) {
      if (qa.match.test(lower)) {
        blank();
        printRaw(`{d:(offline answer)}`);
        await qa.answer(lower);
        return;
      }
    }
    printRaw(`{d:Meanwhile, the built-in commands still work — try }{g:help}{d:, }{g:features}{d:, or }{g:demo}{d:.}`);
  }

  /* ============================================================
     Dispatcher — routing rules:
       1. Exact built-in command (help, demo, matrix, …) → run it.
          These are NEVER sent to the AI.
       2. CLI-syntax-looking input that isn't a command (flags
          like "--foo", or an obvious typo of a known command,
          e.g. "hlep") → "Command not found" + did-you-mean.
       3. Everything else — normal human language ("hi", "how
          are you", "explain recursion") → POST /api/chat.
     ============================================================ */

  /* Strict typo detection: only trap single words that are clearly a
     mistyped command (≤1 edit from one, ≥4 chars, not a real word we
     should chat about). "hlep" → help; "hi"/"hello"/"ok" → AI. */
  function commandTypo(word) {
    if (word.length < 4) return null;                       // "hi", "ok" … → AI
    const names = Object.keys(COMMANDS).filter((n) => COMMANDS[n].primary && !n.startsWith("-"));
    let best = null;
    for (const n of names) {
      const d = levenshtein(word, n);
      if (d === 1 && (!best || n.length > best.length)) best = n;
    }
    return best;
  }

  async function run(raw) {
    const input = raw.trim();
    if (!input) return;

    const [name, ...rest] = input.split(/\s+/);
    const args = rest.join(" ");
    const lower = input.toLowerCase();

    // 1. exact built-in command → never the AI
    if (COMMANDS[name.toLowerCase()]) {
      await COMMANDS[name.toLowerCase()].fn(args);
      return;
    }

    // 2. actual invalid CLI syntax only: unknown flags, or a clear typo
    if (name.startsWith("-")) {
      printRaw(`{r:✗ Unknown flag:} {w:${esc(name)}} {d:— try }{g:help}{d: or }{g:--version}`);
      return;
    }
    if (rest.length === 0) {
      const typo = commandTypo(name.toLowerCase());
      if (typo) {
        printRaw(`{r:✗ Command not found:} {w:${esc(name)}}`);
        printRaw(`{d:Did you mean:} {g:${typo}} {d:— or just ask me a question.}`);
        return;
      }
    }

    // 3. everything else is conversation → the Seed Code Assistant
    try {
      const reply = await withSpinner("Thinking…", askAI(input));
      await streamText(reply);
    } catch (e) {
      await offlineFallback(lower);
    }
  }

  function levenshtein(a, b) {
    const m = a.length, n = b.length;
    const dp = Array.from({ length: m + 1 }, (_, i) => [i, ...Array(n).fill(0)]);
    for (let j = 0; j <= n; j++) dp[0][j] = j;
    for (let i = 1; i <= m; i++)
      for (let j = 1; j <= n; j++)
        dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    return dp[m][n];
  }

  /* ============================================================
     Input handling
     ============================================================ */
  function renderInput(ghost) {
    inputText.innerHTML = esc(state.buffer) + (ghost ? `<span class="ghost">${esc(ghost)}</span>` : "");
  }

  function currentGhost() {
    if (!state.buffer) return "";
    const names = Object.keys(COMMANDS).filter((n) => COMMANDS[n].primary !== false);
    const hit = names.find((n) => n.startsWith(state.buffer.toLowerCase()) && n !== state.buffer.toLowerCase());
    return hit ? hit.slice(state.buffer.length) : "";
  }

  async function submit() {
    const cmdText = state.buffer;
    state.buffer = "";
    renderInput();
    inputRow.hidden = true;
    echoCmd(cmdText);
    if (cmdText.trim()) {
      state.history.push(cmdText);
      state.histIdx = state.history.length;
    }
    state.busy = true;
    try { await run(cmdText); } catch (e) { printRaw(`{r:✗ internal error:} {d:${esc(String(e))}}`); }
    state.busy = false;
    blank();
    inputRow.hidden = false;
    scrollDown();
    kbd.focus({ preventScroll: true });
  }

  document.addEventListener("keydown", (e) => {
    if (e.ctrlKey && e.key.toLowerCase() === "l") {
      e.preventDefault();
      output.innerHTML = "";
      return;
    }
    if (state.busy) return;

    if (e.key === "Enter") { e.preventDefault(); submit(); return; }
    if (e.key === "Backspace") {
      e.preventDefault();
      state.buffer = state.buffer.slice(0, -1);
      renderInput(currentGhost());
      return;
    }
    if (e.key === "ArrowUp") {
      e.preventDefault();
      if (state.histIdx > 0) {
        state.histIdx--;
        state.buffer = state.history[state.histIdx] || "";
        renderInput();
      }
      return;
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      if (state.histIdx < state.history.length) {
        state.histIdx++;
        state.buffer = state.history[state.histIdx] || "";
        renderInput();
      }
      return;
    }
    if (e.key === "Tab") {
      e.preventDefault();
      const ghost = currentGhost();
      if (ghost) { state.buffer += ghost; renderInput(); }
      return;
    }
    if (e.key.length === 1 && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      state.buffer += e.key;
      document.body.classList.add("typing");
      clearTimeout(renderInput._t);
      renderInput._t = setTimeout(() => document.body.classList.remove("typing"), 300);
      renderInput(currentGhost());
      scrollDown();
    }
  });

  // keep hidden input focused so mobile keyboards open
  const refocus = () => { if (document.activeElement !== kbd) kbd.focus({ preventScroll: true }); };
  screen.addEventListener("pointerdown", () => setTimeout(refocus, 0));
  window.addEventListener("load", refocus);

  // double-click a block to copy its text
  output.addEventListener("dblclick", (e) => {
    const blockEl = e.target.closest(".t-block");
    if (!blockEl) return;
    const text = blockEl.innerText;
    const flash = () => {
      blockEl.classList.remove("copied");
      void blockEl.offsetWidth;
      blockEl.classList.add("copied");
    };
    if (navigator.clipboard?.writeText) navigator.clipboard.writeText(text).then(flash).catch(() => {});
    else flash();
  });

  /* chips type the command character by character, then run */
  document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", async () => {
      if (state.busy) return;
      state.busy = true;
      const text = chip.getAttribute("data-cmd");
      state.buffer = "";
      for (const ch of text) {
        state.buffer += ch;
        renderInput();
        scrollDown();
        await wait(26 + Math.random() * 30);
      }
      state.busy = false;
      submit();
    });
  });

  function updateStatusbar() {
    const ready = state.status === "Ready";
    statusLeft.innerHTML =
      `<span class="${ready ? "c-green" : "c-yel"}">●</span> ` +
      (ready ? `${state.provider} · ${state.model}` : "simulator");
  }

  /* ============================================================
     Matrix rain
     ============================================================ */
  let matrixRaf = 0;
  function startMatrix() {
    const ctx = matrixCanvas.getContext("2d");
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const resize = () => {
      matrixCanvas.width = innerWidth * dpr;
      matrixCanvas.height = innerHeight * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };
    resize();
    window.addEventListener("resize", resize, { passive: true });

    const CHARS = "アイウエオカキクケコサシスセソ0123456789$#@ｱｲｳｴｵ<>+-=;:SEEDCODE";
    const fontSize = 15;
    const cols = Math.ceil(innerWidth / fontSize);
    const drops = Array.from({ length: cols }, () => Math.random() * -60);

    const tick = () => {
      ctx.fillStyle = "rgba(5, 5, 6, 0.09)";
      ctx.fillRect(0, 0, innerWidth, innerHeight);
      ctx.font = fontSize + "px monospace";
      for (let i = 0; i < cols; i++) {
        const ch = CHARS[Math.floor(Math.random() * CHARS.length)];
        const y = drops[i] * fontSize;
        ctx.fillStyle = Math.random() < 0.08 ? "#86EFAC" : "#16A34A";
        ctx.fillText(ch, i * fontSize, y);
        if (y > innerHeight && Math.random() > 0.976) drops[i] = 0;
        drops[i]++;
      }
      matrixRaf = requestAnimationFrame(tick);
    };
    if (!matrixRaf) matrixRaf = requestAnimationFrame(tick);
  }
  function stopMatrix() {
    cancelAnimationFrame(matrixRaf);
    matrixRaf = 0;
    matrixCanvas.getContext("2d").clearRect(0, 0, innerWidth, innerHeight);
  }

  /* ============================================================
     Shared site navbar (mobile toggle) — the only site-chrome JS
     this page needs; everything else stays simulator-local.
     ============================================================ */
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector(".nav-links");
  if (navToggle && navLinks) {
    navToggle.addEventListener("click", () => {
      const open = navLinks.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ============================================================
     Boot sequence
     ============================================================ */
  const BOOT = [
    ["Initializing Seed Code…", 300],
    ["Loading modules…", 260],
    ["Loading terminal…", 240],
    ["Checking environment…", 300],
    ["Loading plugins…", 260],
    ["Starting CLI…", 320],
  ];

  (async () => {
    await wait(420);
    for (const [msg, d] of BOOT) {
      const div = printRaw(`{d:[ }{g:••}{d: ]} {m:${msg}}`);
      await wait(d);
      div.innerHTML = markup(`{d:[ }{g:OK}{d: ]} {m:${msg}}`);
    }
    await wait(260);
    printRaw(`{g:Done.}`);
    await wait(420);
    output.innerHTML = "";
    banner();
    blank();
    printRaw(`{d:Type }{g:help}{d: to see every command, or click a suggestion above. Try }{g:demo}{d:, }{g:neofetch}{d:, or }{g:matrix}{d:.}`);
    blank();
    state.busy = false;
    inputRow.hidden = false;
    scrollDown();
    refocus();
  })();
})();
