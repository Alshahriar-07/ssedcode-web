#!/usr/bin/env python3
"""Build script: generates all site pages from a shared shell + per-page content.
Run:  python scripts/build-pages.py   (from D:/Seedcode-cli.io)
Keeps every page's <head>, nav, footer, background and script tags consistent.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://seedcode-web.vercel.app"
GH = "https://github.com/Alshahriar-07/seedcode-cli"
PF = "https://alshahriarsayon.vercel.app/"
STUDIO = "https://eagoxstudio.vercel.app/"
CHAT = "https://seedcode-chat.vercel.app/"
APP = "https://seedcode-app.vercel.app/"
VERSION = "6.2.5"
VER_TAG = "v6.2.5"
RELEASE = f"{GH}/releases/tag/{VER_TAG}"
# Official distribution: the IRM installer system (see IRM_INSTALL/).
WIN_CMD = "irm https://seedcode-cli.vercel.app/install.ps1 | iex"
LINUX_CMD = "curl -fsSL https://seedcode-cli.vercel.app/install.sh | bash"
WIN_INSTALLER = "https://seedcode-cli.vercel.app/install.ps1"
LINUX_INSTALLER = "https://seedcode-cli.vercel.app/install.sh"

GH_ICON = '<svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>'

# Critical inline CSS for the splash — a trimmed copy of the .splash rules in
# css/style.css so the logo animation paints immediately, before the external
# stylesheet arrives. Keep in sync with css/style.css.
SPLASH_CRITICAL_CSS = (
    # no-flash base color goes on body, NOT html: a background on <html> stops
    # body's background propagating to the canvas, which makes body's own
    # opaque background paint OVER the z-index:-1 .bg-layers (grid/lighting).
    "body{background:#09090B}"
    ".splash{position:fixed;inset:0;z-index:520;background:#09090B;display:flex;align-items:center;"
    "justify-content:center;transition:opacity .6s cubic-bezier(.83,0,.17,1),visibility .6s,filter .6s cubic-bezier(.83,0,.17,1)}"
    ".splash.done{opacity:0;visibility:hidden;pointer-events:none;filter:blur(10px)}"
    ".splash-stage{position:relative;text-align:center}"
    ".splash-glow{position:absolute;top:56px;left:50%;width:340px;height:340px;border-radius:50%;"
    "transform:translate(-50%,-50%);background:radial-gradient(circle,rgba(34,197,94,.16) 0%,rgba(34,197,94,.05) 45%,transparent 70%);"
    "filter:blur(24px);animation:splash-fade .9s cubic-bezier(.22,1,.36,1) .1s both}"
    ".splash-logo{position:relative;width:112px;height:112px;border-radius:26px;"
    "filter:drop-shadow(0 0 40px rgba(34,197,94,.35));"
    "animation:splash-logo-in .65s cubic-bezier(.22,1,.36,1) both,splash-float 3s ease-in-out .7s infinite}"
    "@keyframes splash-logo-in{from{opacity:0;transform:scale(.9)}to{opacity:1;transform:scale(1)}}"
    "@keyframes splash-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}"
    "@keyframes splash-fade{from{opacity:0}to{opacity:1}}"
    "@keyframes splash-rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
    ".splash-name{font-family:'Space Grotesk',Inter,sans-serif;font-size:1.55rem;font-weight:700;color:#FAFAFA;"
    "letter-spacing:-.02em;margin-top:24px;animation:splash-rise .55s cubic-bezier(.22,1,.36,1) .15s both}"
    ".splash-tag{font-family:'JetBrains Mono',monospace;font-size:.82rem;color:#A1A1AA;margin-top:8px;"
    "letter-spacing:.02em;animation:splash-rise .55s cubic-bezier(.22,1,.36,1) .25s both}"
    ".splash-status{display:inline-flex;align-items:center;gap:9px;margin-top:30px;min-height:1.4em;"
    "font-family:'JetBrains Mono',monospace;font-size:.74rem;color:#A1A1AA;"
    "animation:splash-fade .5s cubic-bezier(.22,1,.36,1) .35s both}"
    ".splash-spinner{width:11px;height:11px;border-radius:50%;flex:none;border:1.5px solid #3F3F46;"
    "border-top-color:#22C55E;animation:splash-spin .8s linear infinite}"
    "@keyframes splash-spin{to{transform:rotate(360deg)}}"
    "html.sc-seen .splash{display:none}"
    "@media (prefers-reduced-motion:reduce){.splash{display:none}}"
)

# Inline head script: on repeat visits, tag <html> before first paint so the
# splash and intro are display:none instantly — no flash, no JS wait.
SEEN_GATE_JS = (
    "try{if(sessionStorage.getItem('sc-intro'))document.documentElement.classList.add('sc-seen')}catch(e){}"
)
DL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/></svg>'
COPY_BTN = '''<button class="copy-btn" data-copy="{cmd}" aria-label="Copy command"><svg class="icon-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><svg class="icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg><span class="copy-label">Copy</span></button>'''

# Slash commands available inside a `seedcode` session (v6.2.5 registry).
SLASH_COMMANDS = [
    ("/help", "Show available commands"),
    ("/provider", "Switch provider: Default, OpenRouter, FreeModel Claude, FreeModel Codex, AeroLink, Ollama"),
    ("/apikey", "View, replace, remove, or validate the active provider's key"),
    ("/model", "Browse the provider's live model catalogue (Auto on FreeModel)"),
    ("/mode", "Show or switch the mode: chat / assist / code / agent"),
    ("/chat", "Switch to plain Chat Mode"),
    ("/codemode", "Workspace-aware Code Mode (on / off / status)"),
    ("/assist", "Enable Assist Mode: unified AI + computer control"),
    ("/permission", "View or set the permission mode (alias /permissions)"),
    ("/settings", "Open interactive settings (or /settings <name> <value>)"),
    ("/doctor", "Diagnose config, network, and provider health"),
    ("/computer", "Show Computer Engine status and desktop permissions"),
    ("/tools", "List the tools available in Assist Mode"),
    ("/index", "Show a compact tree of the current project"),
    ("/files", "Search project files"),
    ("/history", "List saved conversation sessions"),
    ("/theme", "Pick a colour theme (live preview)"),
    ("/shortcuts", "Show keyboard shortcuts"),
    ("/reset", "Forget the current conversation"),
    ("/clear", "Clear the screen"),
    ("/about", "About Seed Code"),
    ("/version", "Show the version"),
    ("/exit", "Leave the chat — back to the main menu"),
]
_slash_rows = "\n".join(
    f'                <tr><td><code>{cmd}</code></td><td>{desc}</td></tr>'
    for cmd, desc in SLASH_COMMANDS)
_slash_rows_docs = "\n".join(
    f'''              <tr><td><code>{cmd}</code></td><td>{desc}</td></tr>'''
    for cmd, desc in SLASH_COMMANDS)

NAV_ITEMS = [
    ("index.html", "Home"), ("features.html", "Features"),
    ("quickstart.html", "Quick Start"), ("download.html", "Download"),
    ("docs.html", "Docs"), ("faq.html", "FAQ"),
]


def nav_html():
    items = []
    for it in NAV_ITEMS:
        href, label = it[0], it[1]
        is_new = len(it) > 2 and it[2]
        badge = ' <span class="badge-new">NEW</span>' if is_new else ""
        items.append(f'        <li><a href="{href}">{label}{badge}</a></li>')
    return "\n".join(items)


def shell(page, title, desc, body, *, transition="wipe", enter="up", extra_head="", keywords=""):
    nav = nav_html()
    kw = keywords or "Seed Code CLI, seedcode cli, AI CLI, terminal AI assistant, AI coding assistant, Code Mode, Agent Mode, Assist Mode, OpenRouter CLI, Ollama CLI, developer AI tools"
    home = page == "index.html"
    # Home: preload the splash logo, inline the splash-critical CSS, and gate
    # repeat visits before first paint. Order matters: gate script first.
    startup_head = (
        f'  <script>{SEEN_GATE_JS}</script>\n'
        f'  <link rel="preload" href="img/logo.svg" as="image" type="image/svg+xml">\n'
        f'  <style>{SPLASH_CRITICAL_CSS}</style>\n'
    ) if home else ""
    # Splash lives directly under <body> — NOT inside <main class="page-enter">,
    # whose enter animation (opacity/scale) would break position:fixed and hide
    # the splash during the first frames.
    splash_html = ("""  <div class="splash" aria-hidden="true">
    <div class="splash-stage">
      <span class="splash-glow"></span>
      <img src="img/logo.svg" alt="" class="splash-logo" width="112" height="112">
      <div class="splash-name">Seed Code</div>
      <div class="splash-tag">Plant ideas. Grow code.</div>
      <div class="splash-status"><span class="splash-spinner"></span><span class="splash-status-text">Initializing...</span></div>
    </div>
  </div>

""") if home else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{kw}">
  <meta name="author" content="Al Shahriar Sayon">
  <meta name="publisher" content="Eagox Studio">
  <link rel="author" href="{PF}">
  <meta name="robots" content="index, follow">
  <meta name="theme-color" content="#09090B">
  <link rel="canonical" href="{SITE}/{'' if page == 'index.html' else page}">
{startup_head}
  <link rel="icon" href="img/seedcode.ico" sizes="any">
  <link rel="icon" type="image/svg+xml" href="img/logo.svg">
  <link rel="apple-touch-icon" href="img/logo.png">
  <link rel="manifest" href="site.webmanifest">

  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Seed Code CLI">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{SITE}/{'' if page == 'index.html' else page}">
  <meta property="og:image" content="{SITE}/img/logo.png">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}/img/logo.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap"></noscript>
  <link rel="stylesheet" href="css/style.css">
{extra_head}</head>
<body data-transition="{transition}" data-enter="{enter}">
{splash_html}  <a class="skip-link" href="#main">Skip to content</a>

  <div class="scroll-progress" aria-hidden="true"></div>

  <div class="pt-overlay" aria-hidden="true"><div class="pt-b"></div><div class="pt-a"></div></div>

  <div class="bg-layers" aria-hidden="true">
    <div class="bg-spotlight"></div>
    <div class="bg-noise"></div>
  </div>

  <header class="nav-wrap">
    <nav class="nav container" aria-label="Main navigation">
      <a href="index.html" class="logo" aria-label="Seed Code CLI home">
        <img src="img/seedcode.ico" alt="" class="logo-img" width="26" height="26">
        Seed&nbsp;Code&nbsp;<span class="logo-cli">CLI</span>
      </a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
      <ul class="nav-links">
{nav}
        <li><a href="{GH}" class="btn btn-outline" target="_blank" rel="noopener">{GH_ICON} GitHub</a></li>
      </ul>
    </nav>
  </header>

  <main id="main" class="page-enter">
{body}
  </main>

  <footer class="footer">
    <div class="container footer-grid">
      <div>
        <a href="index.html" class="logo">
          <img src="img/seedcode.ico" alt="" class="logo-img" width="26" height="26">
          Seed&nbsp;Code&nbsp;<span class="logo-cli">CLI</span>
        </a>
        <p class="footer-tag">The beautiful AI coding assistant for your terminal. Fast, elegant, and built for developers.</p>
        <p class="footer-credit">Built by <a href="{PF}" target="_blank" rel="noopener"><strong>Al Shahriar Sayon</strong></a> · Part of the <a href="{STUDIO}" target="_blank" rel="noopener">Eagox Studio</a> ecosystem<br>
          <a href="{GH}" target="_blank" rel="noopener">GitHub</a> · <a href="{RELEASE}" target="_blank" rel="noopener">Releases</a> · {VER_TAG}</p>
      </div>
      <nav aria-label="Product">
        <h4>Product</h4>
        <a href="features.html">Features</a>
        <a href="download.html">Download</a>
        <a href="changelog.html">Changelog</a>
        <a href="gallery.html">Gallery</a>
      </nav>
      <nav aria-label="Resources">
        <h4>Resources</h4>
        <a href="docs.html">Documentation</a>
        <a href="quickstart.html">Quick Start</a>
        <a href="{CHAT}" target="_blank" rel="noopener">Seed Code Chat Web <span aria-hidden="true">→</span></a>
        <a href="{APP}" target="_blank" rel="noopener">Seed Code Chat Android <span aria-hidden="true">→</span></a>
        <a href="faq.html">FAQ</a>
        <a href="support.html">Support</a>
      </nav>
      <nav aria-label="Company">
        <h4>Company</h4>
        <a href="about.html">About</a>
        <a href="portfolio.html">Portfolio</a>
        <a href="privacy.html">Privacy</a>
        <a href="terms.html">Terms</a>
      </nav>
    </div>
    <div class="container footer-bottom">
      <p>© 2026 Eagox Studio · Seed Code CLI. All rights reserved.</p>
      <p>Crafted for the terminal · <a href="{RELEASE}" rel="noopener">{VER_TAG}</a> · <a href="{GH}/blob/main/LICENSE" rel="noopener">MIT License</a></p>
    </div>
  </footer>

  <!-- Motion libraries (Lenis, GSAP) are lazy-loaded by main.js after first paint -->
  <script src="js/main.js" defer></script>
</body>
</html>
"""


def code_block(cmd, small=False):
    cls = "code-block code-block-sm" if small else "code-block"
    return f'<div class="{cls}"><code>{cmd}</code>{COPY_BTN.format(cmd=cmd)}</div>'


PAGES = {}

# ════════════════════════ HOME ════════════════════════
PAGES["index.html"] = dict(
    title=f"Seed Code CLI {VER_TAG} — AI Coding Assistant for Your Terminal",
    desc="Seed Code CLI is an AI coding assistant for your terminal with Code Mode, Assist Mode, multiple AI providers, streaming responses, and local Ollama support.",
    transition="wipe", enter="zoom",
    extra_head="""  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Seed Code CLI",
    "operatingSystem": "Windows, Linux, macOS",
    "applicationCategory": "DeveloperApplication",
    "description": "The AI coding assistant for your terminal. Six providers, Code Mode, Agent Mode, /assist desktop control, streaming responses.",
    "url": "https://seedcode-web.vercel.app/",
    "image": "https://seedcode-web.vercel.app/img/logo.png",
    "softwareVersion": "6.2.5",
    "license": "https://github.com/Alshahriar-07/seedcode-cli/blob/main/LICENSE",
    "author": { "@type": "Person", "name": "Al Shahriar Sayon", "url": "https://alshahriarsayon.vercel.app/" },
    "publisher": { "@type": "Organization", "name": "Eagox Studio", "url": "https://eagoxstudio.vercel.app/" },
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
    "downloadUrl": "https://github.com/Alshahriar-07/seedcode-cli/releases/tag/v6.2.5"
  }
  </script>
""",
    body=f"""    <!-- Hero -->
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-copy build-in">
          <div class="hero-badges">
            <span class="badge badge-accent"><span class="badge-dot"></span>{VER_TAG}</span>
            <span class="badge">Works out of the box</span>
            <span class="badge">Windows · Linux</span>
          </div>
          <h1 class="words visible">The AI coding assistant, inside your <span class="accent-word">terminal</span>.</h1>
          <p class="hero-sub">Fast, elegant, and built for developers. Six independent providers — start instantly on <strong>Default</strong> with no API key, or bring your own on <strong>OpenRouter</strong>, <strong>FreeModel</strong>, <strong>AeroLink</strong>, or fully local <strong>Ollama</strong>. Code Mode, Agent Mode, Assist Mode, streaming responses, and a terminal polished down to the last character.</p>
          <div class="hero-actions">
            <a href="download.html" class="btn btn-primary btn-lg" data-magnetic>{DL_ICON} Get Seed Code {VER_TAG}</a>
            <a href="quickstart.html" class="btn btn-secondary btn-lg" data-magnetic>Quick Start</a>
          </div>
          <div class="install-panel">
            <p class="install-hint">Install Seed Code CLI with one command. The installer automatically downloads the latest stable release for your platform.</p>
            <span class="install-os">Windows</span>
            {code_block(WIN_CMD)}
            <span class="install-os">Linux</span>
            {code_block(LINUX_CMD)}
          </div>
        </div>

        <div class="terminal-frame">
          <div class="terminal">
            <div class="terminal-bar">
              <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
              <span class="terminal-title">seedcode — {VER_TAG}</span>
              <span></span>
            </div>
            <div class="terminal-body" data-minisim role="img" aria-label="Live terminal animation automatically typing Seed Code CLI commands and answers"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats -->
    <section class="stats" data-pin aria-label="Project statistics">
      <div class="container">
        <div class="stats-grid stagger reveal">
          <div class="stat"><span class="stat-num"><span class="counter" data-target="312">0</span><span class="stat-suffix">+</span></span><span class="stat-label">Models via OpenRouter</span></div>
          <div class="stat"><span class="stat-num"><span class="counter" data-target="47">0</span><span class="stat-suffix">+</span></span><span class="stat-label">Free-tier models</span></div>
          <div class="stat"><span class="stat-num"><span class="counter" data-target="6">0</span></span><span class="stat-label">Independent providers</span></div>
          <div class="stat"><span class="stat-num"><span class="counter" data-target="3">0</span></span><span class="stat-label">Platforms, one tool</span></div>
        </div>
      </div>
    </section>

    <!-- Feature teaser -->
    <section class="section">
      <div class="container">
        <div class="section-head gsap-head">
          <span class="eyebrow">Why Seed Code</span>
          <h2 data-chars>Built for the shell you live in</h2>
          <p>Streaming AI, six providers, and a terminal UI that feels first-class.</p>
        </div>
        <div class="feature-grid stagger reveal">
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg></div>
            <h3>Streaming Responses</h3>
            <p>Tokens render the instant they arrive — with live Markdown and syntax-highlighted code.</p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M6.5 17l4-5.5M17.5 17l-4-5.5"/></svg></div>
            <h3>Six Independent Providers</h3>
            <p>Default with zero setup, OpenRouter, FreeModel Claude &amp; Codex, AeroLink — or fully local and private with Ollama. Switch with <code>/provider</code>.</p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/></svg></div>
            <h3>Beautiful Output</h3>
            <p>Markdown, syntax highlighting, panels, and progress states — considered down to the cursor.</p>
          </article>
        </div>
        <p class="dl-footnote"><a href="features.html" class="link-arrow">Explore all features <span aria-hidden="true">→</span></a></p>
      </div>
    </section>

    <!-- Modes: Code Mode + Assist Mode -->
    <section class="section-tight">
      <div class="container">
        <div class="section-head gsap-head">
          <span class="eyebrow">Three ways to work</span>
          <h2 data-chars>Code Mode, Agent Mode &amp; <span class="accent-word">/assist</span></h2>
          <p>Seed Code adapts to the task — plain chat, project-aware coding, or desktop control when you need it.</p>
        </div>
        <div class="feature-grid-2 feature-grid stagger reveal">
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m8 6-6 6 6 6"/><path d="m16 6 6 6-6 6"/></svg></div>
            <h3>Code Mode</h3>
            <p>Project-aware coding in your workspace. Enable with <code>/codemode on</code> — persistent <code>.seedcode</code> project memory, an incremental project index, and permission-gated file operations, all from the terminal you already live in.</p>
            <p class="dl-footnote" style="text-align:left;margin-top:18px"><a href="docs.html" class="link-arrow">How it works <span aria-hidden="true">→</span></a></p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/><path d="M9 9.5 11 11l-2 2"/></svg></div>
            <h3>Agent &amp; Assist Mode · <code>/assist</code></h3>
            <p>The agent engine reads, edits, searches, and runs commands in your project — and Assist Mode extends it to your desktop: browser, keyboard, mouse, windows, and vision. Turn it on with <code>/assist on</code>; <code>/permission</code> controls what it may touch.</p>
            <p class="dl-footnote" style="text-align:left;margin-top:18px"><a href="docs.html" class="link-arrow">Learn more <span aria-hidden="true">→</span></a></p>
          </article>
        </div>
      </div>
    </section>

    <!-- AI Providers -->
    <section class="section">
      <div class="container">
        <div class="section-head gsap-head">
          <span class="eyebrow">Six providers, one CLI</span>
          <h2 data-chars>Start instantly. Or bring your own AI.</h2>
          <p>Providers are fully separated — each owns its API key, model, status, and history, so switching never leaks a credential. The built-in <strong>Default</strong> connection needs no API key at all.</p>
        </div>
        <div class="provider-grid stagger reveal">
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg></div>
            <h3>Default <span class="dl-meta">· no API key</span></h3>
            <p>Seed Code's built-in connection and the provider a fresh install ships with. Chat immediately — no key, no signup. Configured independently from OpenRouter.</p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M6.5 17l4-5.5M17.5 17l-4-5.5"/></svg></div>
            <h3>OpenRouter</h3>
            <p>The full model catalogue on your own key. Free and Pro modes — switch with <code>/settings mode free|pro</code>.</p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3v10a4 4 0 0 1-4 4h0"/><path d="M9 13h9"/><path d="M15 3v10"/></svg></div>
            <h3>FreeModel Claude</h3>
            <p>Claude-family models on the FreeModel API. Live catalogue with <code>/model auto</code> selection.</p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8h18"/><path d="M3 16h18"/><path d="M7 3v18"/><path d="M17 3v18"/></svg></div>
            <h3>FreeModel Codex</h3>
            <p>GPT/Codex models on the FreeModel Responses API. Same FreeModel key as Claude — configured independently.</p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3 3 6l3 3"/><path d="M18 3l3 3-3 3"/><path d="M8 13a4 4 0 0 1 8 0"/><path d="M3 21h18"/></svg></div>
            <h3>AeroLink</h3>
            <p>Anthropic-compatible gateway on its own key. Claude-family models, fetched dynamically.</p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="3"/><circle cx="12" cy="11" r="3.5"/><path d="M9 20v-1.5M15 20v-1.5"/></svg></div>
            <h3>Ollama / Local</h3>
            <p>Fully local and private. No API key — uses your installed Ollama models, with a configurable host.</p>
          </article>
        </div>
      </div>
    </section>

    <!-- Seed Code ecosystem -->
    <section class="section-tight">
      <div class="container">
        <div class="section-head gsap-head">
          <span class="eyebrow">Seed Code ecosystem</span>
          <h2 data-chars>Three ways to use Seed Code</h2>
          <p>Powerful in the terminal, light in the browser, and in your pocket on Android — pick the workflow that fits.</p>
        </div>

        <div class="chat-flow chat-flow-3 stagger reveal">
          <div class="chat-flow-card feature-card">
            <span class="chat-flow-tag">Terminal</span>
            <h3>Seed Code CLI</h3>
            <p>AI-powered coding directly in your terminal.</p>
            <a href="download.html" class="link-arrow">Get the CLI <span aria-hidden="true">→</span></a>
          </div>
          <div class="chat-flow-card feature-card">
            <span class="chat-flow-tag">Browser</span>
            <h3>Seed Code Chat Web</h3>
            <p>Lightweight AI chat and coding directly in your browser.</p>
            <a href="{CHAT}" class="link-arrow" target="_blank" rel="noopener">Open Web App <span aria-hidden="true">→</span></a>
          </div>
          <div class="chat-flow-card feature-card">
            <span class="chat-flow-tag">Android</span>
            <h3>Seed Code Chat</h3>
            <p>Your AI assistant on your phone.</p>
            <a href="{APP}" class="link-arrow" target="_blank" rel="noopener">Get the Android app <span aria-hidden="true">→</span></a>
          </div>
        </div>

        <div class="feature-grid-2 feature-grid stagger reveal">
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg></div>
            <h3>Wanna use the lighter version?</h3>
            <p>Seed Code Chat is the lightweight, browser-based way to experience Seed Code — free AI chat and coding with no install and no setup.</p>
            <div class="card-cta"><a href="{CHAT}" class="btn btn-primary" target="_blank" rel="noopener" data-magnetic>Try Seed Code Chat <span aria-hidden="true">→</span></a></div>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3 3 6l3 3"/><path d="M18 3l3 3-3 3"/><path d="M8 13a4 4 0 0 1 8 0"/><path d="M3 21h18"/></svg></div>
            <h3>Wanna use it on the web?</h3>
            <p>A convenient web-based AI chat and coding experience directly from the browser — quick access, easy to try, no CLI setup required for the web experience.</p>
            <div class="card-cta"><a href="{CHAT}" class="btn btn-primary" target="_blank" rel="noopener" data-magnetic>Open Seed Code Chat <span aria-hidden="true">→</span></a></div>
          </article>
        </div>

        <div class="sim-banner reveal-scale">
          <div class="sim-banner-copy">
            <span class="eyebrow">Seed Code Chat</span>
            <h2 data-chars>AI coding chat, straight from your browser.</h2>
            <p>Seed Code Chat is a web-based AI chat &amp; coding experience from the Seed Code ecosystem — ask questions, generate and refine code, and get intelligent AI answers without installing anything.</p>
            <ul class="sim-points">
              <li><span class="c-ok">✓</span> Works in any browser.</li>
              <li><span class="c-ok">✓</span> Quick access — no CLI setup required for the web experience.</li>
              <li><span class="c-ok">✓</span> Free AI chat, easy to try.</li>
            </ul>
            <div class="hero-actions">
              <a href="{CHAT}" class="btn btn-primary btn-lg" target="_blank" rel="noopener" data-magnetic>Try Seed Code Chat <span aria-hidden="true">→</span></a>
            </div>
          </div>
          <div class="sim-banner-term" aria-hidden="true">
            <div class="terminal">
              <div class="terminal-bar">
                <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
                <span class="terminal-title">seedcode chat — browser</span>
                <span></span>
              </div>
              <div class="terminal-body terminal-body-sm">
                <div class="t-line"><span class="t-you">you › </span><span class="t-cmd">write a script that renames files to kebab-case</span></div>
                <div class="t-line"><span class="t-bot-tag">seedcode › </span><span class="t-resp">Here's a clean script — streaming with syntax</span></div>
                <div class="t-line"><span class="t-dim">highlighting, so the code reads like your editor.</span></div>
                <div class="t-line"><span class="t-you">you › </span><span class="t-cmd">add error handling and a dry-run flag</span></div>
                <div class="t-line"><span class="t-bot-tag">seedcode › </span><span class="t-resp">Done — dry-run prints what would change…</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Ecosystem -->
    <section class="section">
      <div class="container">
        <div class="section-head gsap-head">
          <span class="eyebrow">Ecosystem</span>
          <h2 data-chars>One Seed Code ecosystem. Every way you work.</h2>
          <p>Start in the terminal, continue in the browser, and take Seed Code Chat with you on Android.</p>
        </div>
        <div class="feature-grid stagger reveal">
          <article class="feature-card eco-primary" data-tilt>
            <span class="chat-flow-tag">Primary</span>
            <h3>Seed Code CLI</h3>
            <p>Terminal-first AI coding assistant.</p>
            <ul class="sim-points">
              <li><span class="c-ok">▹</span> Code Mode</li>
              <li><span class="c-ok">▹</span> /assist</li>
              <li><span class="c-ok">▹</span> Multiple AI providers</li>
              <li><span class="c-ok">▹</span> Streaming responses</li>
              <li><span class="c-ok">▹</span> Ollama support</li>
            </ul>
            <div class="card-cta"><a href="download.html" class="btn btn-primary" data-magnetic>Explore CLI <span aria-hidden="true">→</span></a></div>
          </article>
          <article class="feature-card" data-tilt>
            <span class="chat-flow-tag">Web</span>
            <h3>Seed Code Chat Web</h3>
            <p>Lightweight AI chat and coding in your browser. No CLI installation required.</p>
            <div class="card-cta"><a href="{CHAT}" class="btn btn-secondary" target="_blank" rel="noopener" data-magnetic>Open Web App <span aria-hidden="true">→</span></a></div>
          </article>
          <article class="feature-card" data-tilt>
            <span class="chat-flow-tag">Android</span>
            <h3>Seed Code Chat</h3>
            <p>Your AI assistant, in your pocket. Code, learn, research, write, and chat from Android.</p>
            <ul class="sim-points">
              <li><span class="c-ok">✓</span> AI-powered chat</li>
              <li><span class="c-ok">✓</span> Coding assistance</li>
              <li><span class="c-ok">✓</span> Markdown &amp; code</li>
              <li><span class="c-ok">✓</span> Custom providers</li>
              <li><span class="c-ok">✓</span> Fast and lightweight</li>
              <li><span class="c-ok">✓</span> Web + Android</li>
            </ul>
            <div class="card-cta"><a href="{APP}" class="btn btn-secondary" target="_blank" rel="noopener" data-magnetic>Get Android App <span aria-hidden="true">→</span></a></div>
          </article>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="section-tight">
      <div class="container">
        <div class="cta reveal-scale">
          <h2>Your terminal deserves better.</h2>
          <p>Install Seed Code CLI {VER_TAG} and start shipping with AI — beautifully.</p>
          <div class="hero-actions">
            <a href="download.html" class="btn btn-primary btn-lg" data-magnetic>Get Seed Code CLI</a>
            <a href="{GH}" class="btn btn-secondary btn-lg" rel="noopener" data-magnetic>Star on GitHub</a>
          </div>
        </div>
      </div>
    </section>""",
)

# ════════════════════════ FEATURES ════════════════════════
_feat = [
    ("Six Independent Providers", "Default (no API key), OpenRouter, FreeModel Claude, FreeModel Codex, AeroLink, and local Ollama — each with its own key, model, and history. Switch anytime with /provider.",
     '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M6.5 17l4-5.5M17.5 17l-4-5.5"/>'),
    ("Works Out of the Box", "The built-in Default provider needs no API key — a fresh install can chat immediately. Bring your own key whenever you want more.",
     '<path d="M20 6 9 17l-5-5"/>'),
    ("Streaming Responses", "Tokens render the instant they arrive — live Markdown and syntax-highlighted code as the answer forms.",
     '<path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/>'),
    ("Live Model Catalogue", "No model is ever hardcoded — browse each provider's live catalogue with /model, or let FreeModel Auto pick the best one per request.",
     '<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>'),
    ("Code Mode", "Workspace-aware coding agent: /codemode on turns your project into the workspace with persistent .seedcode memory, an incremental index, and permission-gated edits.",
     '<path d="m8 6-6 6 6 6"/><path d="m16 6 6 6-6 6"/>'),
    ("Assist Mode · /assist", "The unified AI + computer-control mode: filesystem, terminal, git, browser, keyboard, mouse, windows, vision, and OCR behind one switch.",
     '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>'),
    ("Agent Tools", "The agent reads, edits, searches, and runs commands in your project — /tools lists capabilities, /index shows the project tree, /permission sets access levels.",
     '<path d="M14.7 6.3a4.5 4.5 0 0 0 6 6L14 19l-4.5 1 1-4.5z"/><path d="M7 3h.01M11 3h.01M15 3h.01"/>'),
    ("Git Workflows", "Status, diff, log, commit, push, and pull as first-class agent tools — with read operations safe in every permission mode and mutations gated.",
     '<circle cx="12" cy="12" r="3"/><circle cx="5" cy="5" r="2"/><circle cx="19" cy="5" r="2"/><path d="m7 5h3a2 2 0 0 1 2 2v4M17 7h-3a2 2 0 0 0-2 2"/>'),
    ("Conversation Memory", "Session memory with auto-saved history — /history lists saved conversations per provider, /reset starts fresh.",
     '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>'),
    ("Terminal Control", "Commands stream output live while running, capture stderr, report exit codes, and kill the whole process tree on timeout or Ctrl+C.",
     '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3"/><path d="M13 15h4"/>'),
    ("Permission System", "read_only, workspace, desktop, and full_system levels — every tool call passes the gate, dangerous actions confirm, and .seedcode memory refuses secret-looking fields.",
     '<path d="M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5z"/><path d="m9 12 2 2 4-4"/>'),
    ("Diagnostics", "/doctor checks config, network, and provider health in one pass — with quiet logs at ~/.seedcode/logs/seedcode.log.",
     '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>'),
]
_feat_cards = "\n".join(
    f'''          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{icon}</svg></div>
            <h3>{name}</h3>
            <p>{desc}</p>
          </article>''' for name, desc, icon in _feat)

PAGES["features.html"] = dict(
    title="Features — Seed Code CLI v6.2.5 | Six Providers, Code Mode & Assist Mode",
    desc="Everything a terminal-native developer needs: six independent AI providers (Default needs no key), streaming responses, Code Mode, Agent Mode, /assist desktop control, live model catalogues, and one-command installers for Windows and Linux.",
    transition="slide", enter="up",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Features</span>
        <h1 data-chars>Everything a terminal-native developer needs</h1>
        <p>Considered design meets serious engineering — from first launch to your thousandth session.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="feature-grid stagger reveal">
{_feat_cards}
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="cta reveal-scale">
          <h2>See it in motion.</h2>
          <p>The gallery shows real sessions — chat, streaming, config, and more.</p>
          <div class="hero-actions">
            <a href="gallery.html" class="btn btn-primary btn-lg" data-magnetic>View Gallery</a>
            <a href="quickstart.html" class="btn btn-secondary btn-lg" data-magnetic>Quick Start</a>
          </div>
        </div>
      </div>
    </section>""",
)

# ════════════════════════ QUICK START ════════════════════════
PAGES["quickstart.html"] = dict(
    title="Quick Start — Seed Code CLI | Zero to AI in Seconds",
    desc="Install Seed Code CLI with the official one-line installer for Windows or Linux, launch seedcode, and start your first AI session immediately — no API key needed.",
    transition="circle", enter="blur",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Quick Start</span>
        <h1 data-chars>Up and running in seconds</h1>
        <p>One command to install, one command to launch — and the built-in Default provider needs no API key.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="quickstart-grid">
          <div class="qs-steps reveal-left">
            <div class="qs-step">
              <span class="qs-num">1</span>
              <div class="qs-body">
                <h3>Install — Windows</h3>
                {code_block(WIN_CMD)}
                <p class="qs-note">PowerShell 5.1+. Downloads the official release, verifies its SHA256, installs per-user, and adds <code>seedcode</code> to your PATH.</p>
                <h3 class="qs-linux">Install — Linux</h3>
                {code_block(LINUX_CMD)}
                <p class="qs-note">Any bash shell — also works on macOS.</p>
              </div>
            </div>
            <div class="qs-step">
              <span class="qs-num">2</span>
              <div class="qs-body">
                <h3>Launch</h3>
                {code_block("seedcode")}
                <p class="qs-note">Open a <em>new</em> terminal after installing so PATH changes apply. You land on the startup header and the chat prompt — the built-in Default provider is ready with no API key.</p>
              </div>
            </div>
            <div class="qs-step">
              <span class="qs-num">3</span>
              <div class="qs-body">
                <h3>Go further</h3>
                {code_block("/help")}
                <p class="qs-note">Workspace-aware coding with <code>/codemode on</code>, AI + computer control with <code>/assist</code>, your own AI providers with <code>/provider</code>, and keys with <code>/apikey</code>.</p>
              </div>
            </div>
          </div>
          <div class="cmd-panel reveal-right">
            <h3>Every command</h3>
            <table class="cmd-table">
              <tbody>
{_slash_rows}
              </tbody>
            </table>
            <a href="docs.html" class="link-arrow">Full documentation <span aria-hidden="true">→</span></a>
          </div>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container container-narrow">
        <div class="callout reveal"><strong>Verify:</strong> run <code>seedcode --version</code> — expected output <code>Seed Code CLI 6.2.5</code>. Something off? <code>/doctor</code> checks everything in one pass.</div>
      </div>
    </section>""",
)

# ════════════════════════ DOWNLOAD ════════════════════════
PAGES["download.html"] = dict(
    title=f"Download — Seed Code CLI {VER_TAG} for Windows, Linux & macOS",
    desc="Install Seed Code CLI v6.2.5 with the official one-line installers: irm + iex on Windows PowerShell, curl + bash on Linux and macOS. SHA256-verified official release artifacts, no Python required.",
    transition="wipe", enter="zoom",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Download</span>
        <h1 data-chars>Download Seed Code CLI {VER_TAG}</h1>
        <p>Latest release: <strong><a href="{RELEASE}" target="_blank" rel="noopener">{VER_TAG}</a></strong> · Official one-line installers, verified before they install.</p>
        <div class="hero-actions">
          <a href="{RELEASE}" class="btn btn-primary btn-lg" target="_blank" rel="noopener" data-magnetic>{DL_ICON} Release {VER_TAG}</a>
          <a href="{GH}/releases" class="btn btn-secondary btn-lg" target="_blank" rel="noopener" data-magnetic>View Releases</a>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="download-grid stagger reveal">
          <article class="dl-card dl-card-accent" data-tilt>
            <span class="dl-tag">Official · Recommended</span>
            <div class="dl-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 5.5 10.5 4.4v7.1H3V5.5zM3 12.5h7.5v7.1L3 18.5v-6zM11.5 4.2 21 3v8.5h-9.5V4.2zM11.5 12.5H21V21l-9.5-1.2v-7.3z"/></svg></div>
            <h3>Windows</h3>
            <p>Paste into PowerShell 5.1 or newer. The installer downloads the official release, verifies its SHA256 checksum, installs per-user, adds <code>seedcode</code> to your PATH, and verifies the result.</p>
            {code_block(WIN_CMD, small=True)}
            <span class="dl-meta">No Python required · no administrator rights</span>
          </article>
          <article class="dl-card dl-card-accent" data-tilt>
            <span class="dl-tag">Official · Recommended</span>
            <div class="dl-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3"/><path d="M13 15h4"/></svg></div>
            <h3>Linux &amp; macOS</h3>
            <p>Paste into any bash shell. The installer downloads the official release for your platform, verifies its SHA256 checksum, installs per-user, and verifies the installed command.</p>
            {code_block(LINUX_CMD, small=True)}
            <span class="dl-meta">bash · works on Linux and macOS · current user</span>
          </article>
        </div>
        <p class="dl-footnote reveal">Both commands come straight from the official installer system. Prefer a GUI? Grab <code>SeedCode-CLI-Setup-6.2.5.exe</code> from the <a href="{RELEASE}" rel="noopener">GitHub release</a>.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container container-narrow">
        <div class="callout reveal"><strong>After installing:</strong> open a <em>new</em> terminal (PATH changes only apply to fresh sessions), run <code>seedcode --version</code> — it should print <code>Seed Code CLI 6.2.5</code> — then start with <code>seedcode</code>. The built-in Default provider works immediately, no API key. While you decide, try <a href="{CHAT}" target="_blank" rel="noopener">Seed Code Chat Web</a> or the <a href="{APP}" target="_blank" rel="noopener">Android app</a>.</div>
      </div>
    </section>""",
)

# ════════════════════════ GALLERY ════════════════════════
_screens = [
    ("Chat", "Converse naturally with streaming, Markdown-rendered answers.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode chat\n'), ('t-value', 'You › Explain async generators in Python\n'),
        ('t-dim', 'AI  › An async generator combines async def\n      with yield, producing values you can\n      iterate with async for ...')]),
    ("Streaming", "Watch tokens arrive live, with graceful word wrapping.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode "write a haiku about git"\n'),
        ('t-dim', 'branches drift apart\na merge brings them home again\nconflicts, then release ▌')]),
    ("Configuration", "Per-provider keys, models, and defaults — fully isolated.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode\n'),
        ('t-label', 'you › '), ('t-cmd', '/apikey\n'), ('t-ok', '✓ OpenRouter key saved\n'),
        ('t-ok', '✓ FreeModel key saved\n'), ('t-dim', 'Keys live in ~/.seedcode/config.json')]),
    ("Diagnostics", "Health checks that feel native.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode\n'), ('t-label', 'you › '), ('t-cmd', '/doctor\n'),
        ('t-ok', '✓ '), ('t-value', 'Config valid\n'), ('t-ok', '✓ '), ('t-value', 'Network reachable\n'),
        ('t-ok', '✓ '), ('t-value', 'Provider healthy\n'), ('t-dim', '3/3 checks passed')]),
    ("Themes", "Ship-ready themes tuned for contrast and long sessions.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode\n'), ('t-label', 'you › '), ('t-cmd', '/theme\n'),
        ('t-ok', '✓ Theme set to Ocean\n'), ('t-dim', 'Live preview — Seed Green · Forest · Ocean · Dusk · Ember')]),
    ("Providers", "Six independent backends, zero setup to start.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode\n'), ('t-label', 'you › '), ('t-cmd', '/provider\n'),
        ('t-ok', '▸ Default — built-in, no API key\n'), ('t-dim', '  OpenRouter · FreeModel · AeroLink · Ollama')]),
]

def _mini(parts):
    out = []
    for cls, text in parts:
        for i, seg in enumerate(text.split("\n")):
            if i > 0:
                out.append("</div><div class='terminal-line'>")
            if seg:
                out.append(f"<span class='{cls}'>{seg}</span>")
    return "<div class='terminal-line'>" + "".join(out) + "</div>"

_screen_cards = "\n".join(
    f'''          <article class="screen-card" data-tilt>
            <div class="terminal-mini">
              <div class="terminal-bar"><div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div><span></span><span></span></div>
              <div class="terminal-mini-body">{_mini(parts)}</div>
            </div>
            <h3>{name}</h3>
            <p>{desc}</p>
          </article>''' for name, desc, parts in _screens)

PAGES["gallery.html"] = dict(
    title="Gallery — Seed Code CLI in Action",
    desc="Seed Code CLI in real sessions — chat, streaming, configuration, diagnostics, themes, and settings. Designed down to the last character.",
    transition="circle", enter="zoom",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">In Action</span>
        <h1 data-chars>Designed down to the last character</h1>
        <p>A look at Seed Code in real sessions — chat, streaming, configuration, and more.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="gallery-grid stagger reveal">
{_screen_cards}
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="cta reveal-scale">
          <h2>Try it yourself.</h2>
          <p>One command and you're inside.</p>
          <div class="hero-actions">
            <a href="download.html" class="btn btn-primary btn-lg" data-magnetic>Download</a>
            <a href="quickstart.html" class="btn btn-secondary btn-lg" data-magnetic>Quick Start</a>
          </div>
        </div>
      </div>
    </section>""",
)

# ════════════════════════ DOCS ════════════════════════
PAGES["docs.html"] = dict(
    title="Documentation — Seed Code CLI | Installation, Commands & Configuration",
    desc="Seed Code CLI documentation: official installation for Windows and Linux, every command, configuration, six providers (Default, OpenRouter, FreeModel, AeroLink, Ollama), and troubleshooting.",
    transition="slide", enter="up",
    body=f"""    <div class="container docs-layout">
      <aside class="docs-sidebar" aria-label="Documentation navigation">
        <h4>Getting Started</h4>
        <a href="#installation">Installation</a>
        <a href="#configuration">Configuration</a>
        <a href="#providers">Providers</a>
        <h4>Usage</h4>
        <a href="#commands">Commands</a>
        <a href="#examples">Examples</a>
        <h4>Help</h4>
        <a href="#troubleshooting">Troubleshooting</a>
      </aside>

      <div class="docs-content">
        <h1>Master Seed Code CLI</h1>
        <p class="lead">Everything from your first install to advanced configuration — in one place.</p>

        <div class="sim-strip sim-strip-docs">
          <p><strong>New here?</strong> Try Seed Code Chat in your browser first.</p>
          <a href="{CHAT}" class="btn btn-secondary" target="_blank" rel="noopener" data-magnetic>Try Seed Code Chat <span aria-hidden="true">→</span></a>
        </div>

        <section id="installation">
          <h2>Installation</h2>
          <p>Seed Code CLI is distributed through the official installer system. One command per platform — no Python, no package manager.</p>
          <h3>Windows — PowerShell 5.1+</h3>
          <pre><code><span class="pre-comment"># Install</span>
<span class="pre-accent">PS&gt;</span> {WIN_CMD}

<span class="pre-comment"># Verify (open a new terminal first)</span>
<span class="pre-accent">PS&gt;</span> seedcode --version
Seed Code CLI 6.2.5</code></pre>
          <p>Installs for the current user (no administrator rights), adds <code>seedcode</code> to your user PATH, and verifies the install before finishing. Prefer a GUI? Download <code>SeedCode-CLI-Setup-6.2.5.exe</code> from the <a href="{RELEASE}" rel="noopener">GitHub release</a>.</p>
          <h3>Linux — bash</h3>
          <pre><code><span class="pre-comment"># Install</span>
<span class="pre-accent">$</span> {LINUX_CMD}

<span class="pre-comment"># Verify</span>
<span class="pre-accent">$</span> seedcode --version
Seed Code CLI 6.2.5</code></pre>
          <p>Installs for the current user. The installer downloads the official release for your platform, verifies its SHA256 checksum, and verifies the installed command before it finishes.</p>
          <div class="callout"><strong>Tip:</strong> PATH changes only apply to <em>new</em> terminal sessions. After installing, open a fresh terminal — then <code>/doctor</code> inside a session confirms everything is in place.</div>
        </section>

        <section id="configuration">
          <h2>Configuration</h2>
          <p>Seed Code stores its settings in a single JSON file at <code>~/.seedcode/config.json</code> (owner-only permissions where the OS supports it). Each provider keeps its own entry, so nothing is shared or overwritten.</p>
          <pre><code><span class="pre-comment"># ~/.seedcode/config.json</span>
{{
  "active_provider": "default",
  "providers": {{
    "default":           {{ "api_key": "",          "model": "nvidia/nemotron-3-super-120b-a12b:free" }},
    "openrouter":        {{ "api_key": "sk-or-...", "model": "vendor/model" }},
    "freemodel_claude":  {{ "api_key": "fe_oa_...", "model": "claude-sonnet-4-6" }},
    "freemodel_codex":   {{ "api_key": "fe_oa_...", "model": "auto" }},
    "aerolink":          {{ "api_key": "...",       "model": "..." }},
    "ollama":            {{ "api_key": "",          "model": "llama3.2" }}
  }},
  "ollama_host": "http://localhost:11434",
  "max_tokens": 1024
}}</code></pre>
          <p>Every provider keeps its own isolated entry — saving or switching one provider never reads or writes another's key slot.</p>
          <h3>API keys</h3>
          <p>The built-in <strong>Default</strong> provider needs no API key. Keys for every other provider are only saved after a real authenticated validation. For CI and containers, environment variables override stored keys: <code>OPENROUTER_API_KEY</code>, <code>FREEMODEL_API_KEY</code>, and <code>AEROLINK_API_KEY</code>. Keys are never printed, logged, or included in an error message.</p>
        </section>

        <section id="providers">
          <h2>Providers</h2>
          <p>Six independent backends — each owns its API key, model, connection status, and history. Switch anytime with <code>/provider</code>; the picker groups choices by what they need.</p>
          <table class="docs-table">
            <thead><tr><th>Provider</th><th>API key</th><th>Best for</th><th>Config value</th></tr></thead>
            <tbody>
              <tr><td>Default</td><td>not required</td><td>Chatting immediately on a fresh install — Seed Code's built-in connection</td><td><code>default</code></td></tr>
              <tr><td>OpenRouter</td><td>required</td><td>Full model catalogue — free and Pro modes on one key</td><td><code>openrouter</code></td></tr>
              <tr><td>FreeModel Claude</td><td>required</td><td>Claude-family models, live catalogue, Auto mode</td><td><code>freemodel_claude</code></td></tr>
              <tr><td>FreeModel Codex</td><td>required</td><td>GPT/Codex models on the Responses API</td><td><code>freemodel_codex</code></td></tr>
              <tr><td>AeroLink</td><td>required</td><td>Anthropic-compatible gateway, dynamic model fetch</td><td><code>aerolink</code></td></tr>
              <tr><td>Ollama / Local</td><td>not required</td><td>Fully local, private, runs on this machine</td><td><code>ollama</code></td></tr>
            </tbody>
          </table>
          <p>No model is ever hardcoded — browse any provider's live catalogue with <code>/model</code>. OpenRouter lists 300+ models, 45+ of them free.</p>
        </section>

        <section id="commands">
          <h2>Commands</h2>
          <p>Every command is a slash command, typed inside a <code>seedcode</code> session.</p>
          <table class="docs-table">
            <thead><tr><th>Command</th><th>Description</th></tr></thead>
            <tbody>
{_slash_rows_docs}
            </tbody>
          </table>
        </section>

        <section id="examples">
          <h2>Examples</h2>
          <h3>Code Mode (workspace-aware coding)</h3>
          <pre><code>you › /codemode on
✓ Code Mode ON
  Workspace: ~/projects/my-app
  Index: 128 indexed, 0 unchanged (incremental)
  The agent now consults .seedcode memory + index before touching files.</code></pre>
          <h3>Health check</h3>
          <pre><code><span class="pre-accent">$</span> seedcode
you › /doctor
✓ Config valid
✓ Network reachable
✓ Provider healthy
3/3 checks passed · environment healthy</code></pre>
          <h3>Agent Mode (project tools)</h3>
          <pre><code>you › /agent
✓ Assist Mode ON — the AI can read, edit, search, and run commands

you › /index
▸ src/
  ▸ components/
  ▸ utils/
▸ tests/</code></pre>
          <h3>Assist Mode (computer control)</h3>
          <pre><code>you › /assist on
✓ Assist Mode ON
AI · Filesystem · Terminal · Git · Browser · Keyboard
Mouse · Windows · Vision · OCR · Desktop Automation</code></pre>
        </section>

        <section id="troubleshooting">
          <h2>Troubleshooting</h2>
          <ul>
            <li><strong>Command not found</strong> — open a <em>new</em> terminal; PATH changes only apply to fresh sessions. The installers verify this before they finish.</li>
            <li><strong>"Setup needed" on the header</strong> — the active provider is not usable yet. Run <code>/provider</code> and pick Default (release builds work out of the box) or add a key.</li>
            <li><strong>Auth errors</strong> — re-run the API key flow with <code>/apikey</code>, or set <code>OPENROUTER_API_KEY</code>, <code>FREEMODEL_API_KEY</code>, or <code>AEROLINK_API_KEY</code>.</li>
            <li><strong>Rate limits (429)</strong> — wait and retry; Seed Code honors the provider's <code>Retry-After</code> hint, or switch provider with <code>/provider</code>.</li>
            <li><strong>Garbled output</strong> — use a terminal with truecolor support (Windows Terminal, iTerm2, most modern emulators).</li>
          </ul>
          <p>Still stuck? Visit <a href="support.html">Support</a> or <a href="{GH}/issues" rel="noopener">open an issue</a>.</p>
        </section>
      </div>
    </div>""",
)

# ════════════════════════ CHANGELOG ════════════════════════
PAGES["changelog.html"] = dict(
    title="Changelog & Roadmap — Seed Code CLI",
    desc="Seed Code CLI version history and roadmap: what shipped in v6.2.5 and what's coming — plugins, MCP, voice, memory, and a desktop app.",
    transition="slide", enter="blur",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Changelog</span>
        <h1 data-chars>Shipped &amp; shipping</h1>
        <p>Version history and what's next on the roadmap.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="timeline">
          <h2 class="timeline-heading reveal">Shipped</h2>
          <div class="timeline-item is-current reveal">
            <h3><a href="{RELEASE}" target="_blank" rel="noopener">{VER_TAG}</a> <span class="tag tag-latest">Latest</span> <span class="changelog-date">2026</span></h3>
            <ul>
              <li><strong>Six providers</strong> — the built-in <strong>Default</strong> connection (no API key) joins OpenRouter, FreeModel Claude, FreeModel Codex, AeroLink, and local Ollama as a first-class, fully separated provider</li>
              <li><strong>Works out of the box</strong> — a fresh install ships on Default and can chat immediately, no key or signup</li>
              <li><strong>Assist Mode</strong> — unified AI + computer control: filesystem, terminal, git, browser, keyboard, mouse, windows, vision, OCR, and desktop automation</li>
              <li><strong>Code Mode</strong> — workspace-aware coding with persistent <code>.seedcode</code> project memory, an incremental index, and <code>/codemode on|off|status</code></li>
              <li><strong>Credential isolation</strong> — every provider keeps its own key slot; the built-in credential is never copied into another provider's configuration</li>
              <li><strong>Terminal control</strong> — live streaming output, stderr capture, exit codes, bounded timeouts, and process-tree cancellation</li>
              <li><strong>Installer-based distribution</strong> — official one-line IRM installers for Windows and Linux with SHA256 verification; <code>seedcode --version</code> prints a machine-parseable line</li>
            </ul>
          </div>
          <div class="timeline-item reveal">
            <h3>v6.2.0 <span class="changelog-date">2026</span></h3>
            <ul>
              <li>Code Mode introduced — workspace-aware agent sessions with project memory and incremental indexing</li>
              <li>Unified permission system — read_only / workspace / desktop / full_system levels with per-action confirmation</li>
              <li>Live terminal output streaming and process-tree cancellation</li>
            </ul>
          </div>
          <div class="timeline-item reveal">
            <h3>v1.0.0 <span class="changelog-date">2026</span></h3>
            <ul>
              <li>The original Seed Code CLI launch — interactive terminal experience with streaming responses</li>
              <li>Provider support — OpenRouter, AeroLink, and local Ollama</li>
              <li>Themes — Seed Green, Forest, Ocean, Dusk, Ember, Monochrome</li>
            </ul>
          </div>

          <h2 class="timeline-heading reveal">Upcoming</h2>
          <div class="timeline-item reveal"><h3>Plugins <span class="tag tag-soon">Planned</span></h3><p>Extend Seed Code with community-built commands and renderers.</p></div>
          <div class="timeline-item reveal"><h3>MCP <span class="tag tag-soon">Planned</span></h3><p>Model Context Protocol support for tools and external context.</p></div>
          <div class="timeline-item reveal"><h3>Voice <span class="tag tag-soon">Planned</span></h3><p>Talk to your terminal — dictate prompts and hear responses.</p></div>
          <div class="timeline-item reveal"><h3>Memory <span class="tag tag-soon">Planned</span></h3><p>Long-term, local-first memory that persists across sessions.</p></div>
          <div class="timeline-item reveal"><h3>Desktop App <span class="tag tag-soon">Planned</span></h3><p>The Seed Code experience in a native desktop shell.</p></div>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="cta reveal-scale">
          <h2>Help shape the roadmap.</h2>
          <p>Feature requests and bug reports are always welcome on GitHub.</p>
          <div class="hero-actions">
            <a href="{GH}/issues" class="btn btn-primary btn-lg" rel="noopener" data-magnetic>Open an Issue</a>
            <a href="download.html" class="btn btn-secondary btn-lg" data-magnetic>Get Seed Code CLI</a>
          </div>
        </div>
      </div>
    </section>""",
)

# ════════════════════════ FAQ ════════════════════════
_faqs = [
    ("Is Seed Code free?", "Yes. Seed Code CLI is free, and the built-in Default provider works with no API key at all. You only pay your AI provider for model usage when you bring your own key — and through OpenRouter you can use many models entirely for free."),
    ("How do I install Seed Code CLI?", "On Windows (PowerShell 5.1+): <code>irm https://seedcode-cli.vercel.app/install.ps1 | iex</code>. On Linux (bash): <code>curl -fsSL https://seedcode-cli.vercel.app/install.sh | bash</code>. Both installers download the official release, verify its SHA256 checksum, and verify the install before finishing. Open a new terminal afterwards so PATH changes apply."),
    ("Do I need an API key to start?", "No. Seed Code ships with the built-in Default provider — Seed Code's own connection — which needs no API key. A fresh installation can chat immediately. You can add your own providers anytime with <code>/provider</code>."),
    ("Does it support Windows?", "Fully. Seed Code runs natively on Windows, including Windows Terminal and PowerShell, plus Linux and macOS. The official PowerShell one-liner is the recommended install on Windows; Linux and macOS use the curl one-liner. A graphical <code>SeedCode-CLI-Setup-6.2.5.exe</code> installer is also available from the <a href='https://github.com/Alshahriar-07/seedcode-cli/releases/tag/v6.2.5'>GitHub release</a>."),
    ("Which providers are supported?", "Six: Default (built-in, no key), OpenRouter, FreeModel Claude, FreeModel Codex, AeroLink, and Ollama for fully local models. Each provider is fully independent — its own API key, model, and conversation history — and through the FreeModel providers many models are entirely free."),
    ("How do I configure my API key?", "Run <code>seedcode</code> and use <code>/apikey</code> in the session to add keys for OpenRouter, FreeModel, or AeroLink. Everything is stored locally in <code>~/.seedcode/config.json</code>, one isolated entry per provider. You can also set environment variables like <code>OPENROUTER_API_KEY</code>, <code>FREEMODEL_API_KEY</code>, or <code>AEROLINK_API_KEY</code>."),
]
_faq_items = "\n".join(
    f'''          <details class="faq-item reveal">
            <summary>{q}</summary>
            <p>{a}</p>
          </details>''' for q, a in _faqs)
_faq_ld = ",\n      ".join(
    '{{ "@type": "Question", "name": "{q}", "acceptedAnswer": {{ "@type": "Answer", "text": "{a}" }} }}'.format(
        q=q, a=a.replace('<code>', '').replace('</code>', '').replace("<a href='download.html'>", "").replace("</a>", "").replace('"', "'"))
    for q, a in _faqs)

PAGES["faq.html"] = dict(
    title="FAQ — Seed Code CLI | Installation, Pricing, Platforms & Providers",
    desc="Quick answers about Seed Code CLI: official one-line installers for Windows and Linux, pricing, provider support, and API key configuration.",
    transition="circle", enter="up",
    extra_head=f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {_faq_ld}
    ]
  }}
  </script>
""",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">FAQ</span>
        <h1 data-chars>Frequently asked questions</h1>
        <p>Quick answers about installation, pricing, platforms, and providers.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="faq-list">
{_faq_items}
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="cta reveal-scale">
          <h2>Still have questions?</h2>
          <p>The docs go deeper, and the community is happy to help.</p>
          <div class="hero-actions">
            <a href="docs.html" class="btn btn-primary btn-lg" data-magnetic>Read the docs</a>
            <a href="{GH}/issues" class="btn btn-secondary btn-lg" rel="noopener" data-magnetic>Ask on GitHub</a>
          </div>
        </div>
      </div>
    </section>""",
)

# ════════════════════════ ABOUT ════════════════════════
PAGES["about.html"] = dict(
    title="About — Seed Code CLI & Eagox Studio",
    desc="The story behind Seed Code CLI: built by Al Shahriar Sayon and published by Eagox Studio to make the terminal the best place to work with AI.",
    transition="wipe", enter="blur",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">About</span>
        <h1 data-chars>Crafted for the terminal</h1>
        <p>Why we believe the command line is the best place to work with AI.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container prose">
        <h2>The idea</h2>
        <p>Developers live in the terminal — it's where code is written, tested, shipped, and debugged. Yet most AI tools pull you away from it, into browser tabs and context switches. <strong>Seed Code CLI</strong> was built on a simple belief: AI assistance should come to where you already work, and it should be beautiful when it gets there.</p>
        <h2>The craft</h2>
        <p>Every pixel of output is considered — streaming that renders tokens the instant they arrive, Markdown and syntax highlighting that read like your editor, themes tuned for long sessions, and a configuration system that stays out of your way. Fast cold starts and no telemetry.</p>
        <h2>The team</h2>
        <p>Seed Code CLI is designed and developed by <strong>Eagox Studio</strong>, created by <a href="{PF}" target="_blank" rel="noopener">Al Shahriar Sayon</a> — a developer who cares deeply about tools that feel as good as they function. See the <a href="portfolio.html">portfolio</a> for more of his work, or visit <a href="{STUDIO}" target="_blank" rel="noopener">eagoxstudio.vercel.app</a>.</p>
        <p><strong>Created by:</strong> <a href="{PF}" target="_blank" rel="noopener">Al Shahriar Sayon</a> · <strong>Published by:</strong> <a href="{STUDIO}" target="_blank" rel="noopener">Eagox Studio</a></p>
        <div class="callout"><strong>Official releases:</strong> Seed Code CLI is distributed through the official installer system and <a href="{RELEASE}" rel="noopener">GitHub Releases</a>. Issues and ideas are always welcome.</div>
      </div>
    </section>""",
)

# ════════════════════════ PORTFOLIO ════════════════════════
PAGES["portfolio.html"] = dict(
    title="Al Shahriar Sayon — Developer Portfolio | Creator of Seed Code CLI",
    desc="Al Shahriar Sayon is a developer and founder of Eagox Studio, creator of Seed Code CLI. Projects, skills, experience, and contact.",
    transition="circle", enter="zoom",
    body=f"""    <section class="pf-hero">
      <div class="container">
        <div class="pf-avatar reveal-scale visible">AS</div>
        <h1 data-chars>Al Shahriar Sayon</h1>
        <span class="pf-role">Developer · Founder, <a href="{STUDIO}" target="_blank" rel="noopener">Eagox Studio</a></span>
        <p>Building developer tools that feel as good as they function. Creator of Seed Code CLI — the beautiful AI coding assistant for the terminal.</p>
        <div class="pf-links">
          <a href="{PF}" class="btn btn-primary" target="_blank" rel="noopener" data-magnetic>Visit Portfolio Site</a>
          <a href="{STUDIO}" class="btn btn-secondary" target="_blank" rel="noopener" data-magnetic>Eagox Studio</a>
          <a href="https://github.com/Alshahriar-07" class="btn btn-secondary" target="_blank" rel="noopener" data-magnetic>{GH_ICON} GitHub</a>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="section-head gsap-head">
          <span class="eyebrow">Projects</span>
          <h2>Selected work</h2>
        </div>
        <div class="feature-grid stagger reveal">
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3"/><path d="M13 15h4"/></svg></div>
            <h3>Seed Code CLI</h3>
            <p>An AI coding assistant for the terminal with streaming responses, six independent providers, Code / Agent / Assist modes, and a polished TUI.</p>
            <a href="{RELEASE}" class="link-arrow" rel="noopener">Latest release <span aria-hidden="true">→</span></a>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg></div>
            <h3>This Website</h3>
            <p>The Seed Code CLI site itself — a cinematic, multi-page experience with WebGL background, GSAP motion, and page transitions. Zero frameworks.</p>
            <a href="index.html" class="link-arrow">You're looking at it <span aria-hidden="true">→</span></a>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg></div>
            <h3>Eagox Studio</h3>
            <p>A studio for crafted developer tools and experiences — design-led engineering from idea to launch.</p>
            <a href="{STUDIO}" class="link-arrow" target="_blank" rel="noopener">eagoxstudio.vercel.app <span aria-hidden="true">→</span></a>
          </article>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="section-head gsap-head">
          <span class="eyebrow">Skills</span>
          <h2>Tools of the trade</h2>
        </div>
        <div class="pf-skills reveal">
          <span class="pf-skill">Python</span><span class="pf-skill">JavaScript</span><span class="pf-skill">TypeScript</span>
          <span class="pf-skill">CLI / TUI Design</span><span class="pf-skill">AI Integration</span><span class="pf-skill">OpenRouter</span>
          <span class="pf-skill">Ollama</span><span class="pf-skill">GSAP</span><span class="pf-skill">Three.js</span>
          <span class="pf-skill">UI/UX</span><span class="pf-skill">Git</span><span class="pf-skill">Linux</span>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="section-head gsap-head">
          <span class="eyebrow">Experience</span>
          <h2>Journey</h2>
        </div>
        <div class="timeline pf-exp">
          <div class="timeline-item is-current reveal">
            <h3>Founder — Eagox Studio <span class="changelog-date">Present</span></h3>
            <p>Designing and shipping developer tools, including Seed Code CLI and its full web experience.</p>
          </div>
          <div class="timeline-item reveal">
            <h3>Creator — Seed Code CLI <span class="changelog-date">2026</span></h3>
            <p>Built an AI terminal assistant from scratch: provider integrations, streaming engine, theming system, and installer-based distribution.</p>
          </div>
          <div class="timeline-item reveal">
            <h3>Independent Developer <span class="changelog-date">Earlier</span></h3>
            <p>Web experiences and automation — learning by shipping.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="cta reveal-scale">
          <h2>Let's build something.</h2>
          <p>Reach out through the portfolio site or GitHub.</p>
          <div class="hero-actions">
            <a href="{PF}" class="btn btn-primary btn-lg" target="_blank" rel="noopener" data-magnetic>Contact via Portfolio</a>
            <a href="https://github.com/Alshahriar-07" class="btn btn-secondary btn-lg" target="_blank" rel="noopener" data-magnetic>GitHub Profile</a>
          </div>
        </div>
      </div>
    </section>""",
)

# ════════════════════════ SUPPORT ════════════════════════
PAGES["support.html"] = dict(
    title="Support — Seed Code CLI | Help & Community",
    desc="Get help with Seed Code CLI: built-in diagnostics, documentation, FAQ, GitHub issues, and how to reach the maintainer.",
    transition="slide", enter="up",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Support</span>
        <h1 data-chars>We've got your back</h1>
        <p>Most problems are one command away from a fix.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container prose">
        <h2>1. Run the doctor</h2>
        <p>The built-in <code>/doctor</code> command checks your config, network, and provider health in one pass.</p>
        <pre><code><span class="pre-accent">$</span> seedcode
you › /doctor
✓ Config valid
✓ Network reachable
✓ Provider healthy</code></pre>
        <h2>2. Check the docs &amp; FAQ</h2>
        <ul>
          <li><a href="docs.html">Documentation</a> — installation, commands, configuration, providers</li>
          <li><a href="faq.html">FAQ</a> — installation methods, pricing, platform support</li>
          <li><a href="quickstart.html">Quick Start</a> — zero to first session in under a minute</li>
        </ul>
        <h2>3. Ask the community</h2>
        <ul>
          <li><strong>Bugs &amp; feature requests</strong> — <a href="{GH}/issues" rel="noopener">GitHub Issues</a></li>
          <li><strong>Releases</strong> — <a href="{GH}/releases" rel="noopener">GitHub Releases</a></li>
          <li><strong>The maintainer</strong> — <a href="{PF}" rel="noopener">Al Shahriar Sayon</a> (<a href="{STUDIO}" rel="noopener">Eagox Studio</a>)</li>
        </ul>
        <div class="callout"><strong>Response time:</strong> issues are usually triaged within a couple of days. Clear reproduction steps get the fastest fixes.</div>
      </div>
    </section>""",
)

# ════════════════════════ PRIVACY ════════════════════════
PAGES["privacy.html"] = dict(
    title="Privacy Policy — Seed Code CLI",
    desc="Seed Code CLI privacy policy: no telemetry, no accounts, keys stored locally. Requests go directly to the AI provider you configure.",
    transition="wipe", enter="blur",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Privacy</span>
        <h1 data-chars>Private by design</h1>
        <p>Last updated: July 2026</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container prose">
        <h2>The short version</h2>
        <p>Seed Code CLI collects <strong>nothing</strong>. No telemetry, no analytics, no accounts, no tracking.</p>
        <h2>Your data</h2>
        <ul>
          <li><strong>API keys</strong> are stored locally in <code>~/.seedcode/config.json</code> on your machine and are only sent to the provider you configured.</li>
          <li><strong>Prompts and responses</strong> travel directly between your machine and your chosen AI provider (OpenRouter, FreeModel, AeroLink, or your local Ollama instance); the built-in Default provider speaks to Seed Code's own connection. Your keys are never sent anywhere you have not configured.</li>
          <li><strong>Conversation history</strong>, if enabled, lives only on your machine.</li>
        </ul>
        <h2>Third parties</h2>
        <p>When you use a cloud provider, that provider's own privacy policy applies to the requests you send it. With Ollama, everything stays on your hardware.</p>
        <h2>This website</h2>
        <p>This site is a static site. It sets no cookies and runs no trackers. Fonts and animation libraries are loaded from public CDNs, which may see standard request metadata (IP, user agent) as with any web resource.</p>
        <h2>Contact</h2>
        <p>Questions? Reach the maintainer via <a href="{GH}/issues" rel="noopener">GitHub</a> or the <a href="{PF}" rel="noopener">portfolio site</a>.</p>
      </div>
    </section>""",
)

# ════════════════════════ TERMS ════════════════════════
PAGES["terms.html"] = dict(
    title="Terms of Use — Seed Code CLI",
    desc="Seed Code CLI terms of use: MIT licensed software provided as-is. Your use of AI providers is governed by their own terms.",
    transition="wipe", enter="blur",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Terms</span>
        <h1 data-chars>Terms of use</h1>
        <p>Last updated: July 2026</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container prose">
        <h2>License</h2>
        <p>Seed Code CLI is released under the <a href="{GH}/blob/main/LICENSE" rel="noopener">MIT License</a>. Your use of the software is governed by that license.</p>
        <h2>No warranty</h2>
        <p>The software is provided <strong>"as is"</strong>, without warranty of any kind, express or implied. The authors and Eagox Studio are not liable for any claim, damages, or other liability arising from its use.</p>
        <h2>AI providers</h2>
        <p>Seed Code CLI connects to third-party AI providers (OpenRouter, FreeModel, AeroLink, or your local Ollama) using credentials you supply. The built-in Default provider uses Seed Code's own connection. Your use of cloud providers — including costs, rate limits, and acceptable-use policies — is governed by their own terms of service. You are responsible for reviewing the output of AI models before relying on it.</p>
        <h2>This website</h2>
        <p>Content on this site is provided for information about the product. The official installers verify every download against the release's SHA256 checksums before installing.</p>
        <h2>Changes</h2>
        <p>These terms may be updated as the project evolves; the "last updated" date above reflects the current revision.</p>
      </div>
    </section>""",
)

# ════════════════════════ 404 ════════════════════════
PAGES["404.html"] = dict(
    title="404 — Page Not Found | Seed Code CLI",
    desc="This page could not be found. Return to the Seed Code CLI home page.",
    transition="circle", enter="zoom",
    body=f"""    <section class="page-404">
      <div>
        <div class="code-glitch" aria-hidden="true">404</div>
        <h1>command not found</h1>
        <p><code>seedcode: page does not exist — did you mean <a href="index.html">home</a>?</code></p>
        <div class="hero-actions" style="justify-content:center">
          <a href="index.html" class="btn btn-primary btn-lg" data-magnetic>Back to Home</a>
          <a href="{CHAT}" class="btn btn-secondary btn-lg" target="_blank" rel="noopener" data-magnetic>Try Seed Code Chat <span aria-hidden="true">→</span></a>
        </div>
      </div>
    </section>""",
)


def main():
    for page, cfg in PAGES.items():
        html = shell(
            page,
            cfg["title"],
            cfg["desc"],
            cfg["body"],
            transition=cfg.get("transition", "wipe"),
            enter=cfg.get("enter", "up"),
            extra_head=cfg.get("extra_head", ""),
        )
        (ROOT / page).write_text(html, encoding="utf-8")
        print(f"wrote {page} ({len(html)} bytes)")

    # sitemap
    urls = "\n".join(
        f"""  <url>
    <loc>{SITE}/{'' if p == 'index.html' else p}</loc>
    <lastmod>2026-09-21</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{'1.0' if p == 'index.html' else '0.7'}</priority>
  </url>""" for p in PAGES if p != "404.html")
    (ROOT / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""", encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
