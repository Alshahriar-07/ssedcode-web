#!/usr/bin/env python3
"""Build script: generates all site pages from a shared shell + per-page content.
Run:  python scripts/build-pages.py   (from D:/Seedcode-cli.io)
Keeps every page's <head>, nav, footer, background and script tags consistent.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://seedcode-cli.vercel.app"
GH = "https://github.com/Alshahriar-07/seedcode-cli"
PF = "https://alshahriarsayon.vercel.app/"
MEGA = "https://mega.nz/file/pIU0HaJB#nX8HW3f6hBtan1nHuwvzaWujChjtpw8eA6zYFH0NZRQ"

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
    "html.sc-seen .splash,html.sc-seen .intro{display:none}"
    "@media (prefers-reduced-motion:reduce){.splash{display:none}}"
)

# Inline head script: on repeat visits, tag <html> before first paint so the
# splash and intro are display:none instantly — no flash, no JS wait.
SEEN_GATE_JS = (
    "try{if(sessionStorage.getItem('sc-intro'))document.documentElement.classList.add('sc-seen')}catch(e){}"
)
DL_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/></svg>'
COPY_BTN = '''<button class="copy-btn" data-copy="{cmd}" aria-label="Copy command"><svg class="icon-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg><svg class="icon-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg><span class="copy-label">Copy</span></button>'''

NAV_ITEMS = [
    ("index.html", "Home"), ("features.html", "Features"),
    ("cli/", "CLI Simulator", True),
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
    kw = keywords or "Seed Code CLI, seedcode cli, AI CLI, terminal AI assistant, AI coding assistant, OpenRouter CLI, Ollama CLI, developer AI tools"
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
  <meta name="author" content="Al Shahriar Sowan">
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
        <p class="footer-credit">Designed &amp; Developed by <strong>Eagox Studio</strong><br>
          Creator — <a href="{PF}" target="_blank" rel="noopener">Al Shahriar Sowan</a> · <a href="{GH}" target="_blank" rel="noopener">GitHub</a></p>
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
        <a href="cli/" class="footer-sim-link">Interactive CLI Simulator <span aria-hidden="true">→</span></a>
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
      <p>Crafted for the terminal · v1.0.0 · <a href="{GH}/blob/main/LICENSE" rel="noopener">MIT License</a></p>
    </div>
  </footer>

  <a href="cli/" class="cli-fab" aria-label="Open the live CLI simulator">
    <span class="cli-fab-icon">🖥</span> Live CLI
  </a>

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
    title="Seed Code CLI — The Beautiful AI Coding Assistant for Your Terminal",
    desc="Seed Code CLI is a fast, elegant AI coding assistant for your terminal. Connect to OpenRouter, AeroLink, FreeModel, and Ollama with streaming responses and cross-platform support. Free and open source.",
    transition="wipe", enter="zoom",
    extra_head="""  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Seed Code CLI",
    "operatingSystem": "Windows, Linux, macOS",
    "applicationCategory": "DeveloperApplication",
    "description": "The beautiful AI coding assistant for your terminal.",
    "url": "https://seedcode-cli.vercel.app/",
    "image": "https://seedcode-cli.vercel.app/img/logo.png",
    "softwareVersion": "1.0.0",
    "license": "https://github.com/Alshahriar-07/seedcode-cli/blob/main/LICENSE",
    "author": { "@type": "Person", "name": "Al Shahriar Sowan", "url": "https://alshahriarsayon.vercel.app/" },
    "publisher": { "@type": "Organization", "name": "Eagox Studio" },
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
    "downloadUrl": "https://seedcode-cli.vercel.app/Files/SeedCodeSetup.exe"
  }
  </script>
""",
    body=f"""    <!-- Intro boot sequence (splash is injected at body level by shell()) -->
    <div class="intro" aria-hidden="true">
      <div class="intro-stage">
        <span class="intro-logo-wrap"><img src="img/seedcode.ico" alt="" class="intro-logo" width="92" height="92"></span>
        <div class="intro-name"><span class="intro-name-text"></span><span class="t-cursor-i"></span></div>
        <div class="intro-boot"></div>
        <div class="intro-progress">
          <span class="intro-progress-bar"><span class="intro-progress-fill"></span></span>
          <span class="intro-progress-pct">0%</span>
        </div>
      </div>
      <button class="intro-skip" type="button">Skip Intro <kbd>Esc</kbd></button>
    </div>

    <!-- Hero -->
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-copy build-in">
          <div class="hero-badges">
            <span class="badge badge-accent"><span class="badge-dot"></span>Open Source</span>
            <span class="badge">v1.0.0</span>
            <span class="badge">MIT License</span>
          </div>
          <h1 class="words visible">The AI coding assistant, inside your <span class="accent-word">terminal</span>.</h1>
          <p class="hero-sub">Fast, elegant, and built for developers. Connect to <strong>OpenRouter</strong>, <strong>AeroLink</strong>, <strong>FreeModel</strong>, or run fully local with <strong>Ollama</strong> — with streaming responses and a terminal experience polished down to the last character.</p>
          <div class="hero-actions">
            <a href="Files/SeedCodeSetup.exe" download="SeedCodeSetup.exe" class="btn btn-primary btn-lg" data-magnetic>{DL_ICON} Download for Windows</a>
            <a href="quickstart.html" class="btn btn-secondary btn-lg" data-magnetic>Quick Start</a>
          </div>
          <div class="install-card">
            <code>pip install seedcode-cli</code>
            {COPY_BTN.format(cmd="pip install seedcode-cli")}
          </div>
        </div>

        <div class="terminal-frame">
          <div class="terminal">
            <div class="terminal-bar">
              <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
              <span class="terminal-title">seedcode — live simulator</span>
              <span></span>
            </div>
            <div class="terminal-body" data-minisim role="img" aria-label="Live mini simulator automatically typing Seed Code CLI commands and answers"></div>
          </div>
          <div class="term-continue">
            <a href="cli/" class="btn btn-secondary btn-block" data-magnetic>Continue in the Full CLI Simulator</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive CLI Simulator -->
    <section class="section sim-section">
      <div class="container">
        <div class="sim-banner reveal-scale">
          <div class="sim-banner-copy">
            <span class="eyebrow">🖥 Interactive CLI Simulator</span>
            <h2 data-chars>Experience the real Seed Code terminal directly in your browser.</h2>
            <ul class="sim-points">
              <li><span class="c-ok">✓</span> No installation.</li>
              <li><span class="c-ok">✓</span> No account.</li>
              <li><span class="c-ok">✓</span> 100% Offline Demo.</li>
            </ul>
            <div class="hero-actions">
              <a href="cli/" class="btn btn-primary btn-lg" data-magnetic>Launch Simulator</a>
            </div>
          </div>
          <div class="sim-banner-term" aria-hidden="true">
            <div class="terminal">
              <div class="terminal-bar">
                <div class="terminal-dots"><span class="dot dot-red"></span><span class="dot dot-yellow"></span><span class="dot dot-green"></span></div>
                <span class="terminal-title">seedcode — simulator</span>
                <span></span>
              </div>
              <div class="terminal-body terminal-body-sm" data-simpreview></div>
            </div>
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
          <div class="stat"><span class="stat-num"><span class="counter" data-target="4">0</span></span><span class="stat-label">Providers supported</span></div>
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
          <p>Streaming AI, hundreds of models, and a terminal UI that feels first-class.</p>
        </div>
        <div class="feature-grid stagger reveal">
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg></div>
            <h3>Streaming Responses</h3>
            <p>Tokens render the instant they arrive — no waiting spinner, even over SSH.</p>
          </article>
          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M6.5 17l4-5.5M17.5 17l-4-5.5"/></svg></div>
            <h3>Any Provider</h3>
            <p>OpenRouter, ZenMux, AeroLink — or fully local and private with Ollama.</p>
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

    <!-- CTA -->
    <section class="section-tight">
      <div class="container">
        <div class="cta reveal-scale">
          <h2>Your terminal deserves better.</h2>
          <p>Install Seed Code CLI and start shipping with AI — beautifully.</p>
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
    ("Modern CLI", "A thoughtfully designed command-line interface with crisp layouts, subtle color, and zero clutter.",
     '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3"/><path d="M13 15h4"/>'),
    ("Streaming Responses", "Tokens render the instant they arrive. Watch answers form in real time with no waiting spinner.",
     '<path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/>'),
    ("OpenRouter Support", "Access hundreds of models through OpenRouter with a single API key, including free-tier models.",
     '<circle cx="12" cy="5" r="2.5"/><circle cx="5" cy="19" r="2.5"/><circle cx="19" cy="19" r="2.5"/><path d="M12 7.5v4M6.5 17l4-5.5M17.5 17l-4-5.5"/>'),
    ("Ollama — Fully Local", "Run models on your own machine with Ollama — private, offline-friendly, and no API key required.",
     '<rect x="4" y="4" width="16" height="16" rx="3"/><circle cx="12" cy="11" r="3.5"/><path d="M9 20v-1.5M15 20v-1.5"/>'),
    ("FreeModel & AeroLink", "Start instantly with FreeModel's zero-billing setup, or connect through AeroLink for low-latency regional endpoints.",
     '<path d="M20 12V8a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12"/><path d="M6 10h.01M10 10h.01"/><path d="m17 15 2 2 4-4"/>'),
    ("Markdown Rendering", "Rich Markdown rendered directly in your terminal — headings, lists, tables, and links included.",
     '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/>'),
    ("Syntax Highlighting", "Code blocks are highlighted for dozens of languages, so answers read like your editor.",
     '<path d="m8 6-6 6 6 6"/><path d="m16 6 6 6-6 6"/>'),
    ("Cross Platform", "One tool, everywhere you work. Native support for Windows, Linux, and macOS.",
     '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>'),
    ("Fast Startup", "Cold start in milliseconds. Seed Code is ready before your terminal finishes drawing the prompt.",
     '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>'),
    ("Configuration System", "A simple, versionable config file for providers, models, themes, and keybindings — with a guided wizard.",
     '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>'),
    ("Open Source", "MIT licensed and developed in the open. Read the source, file issues, and ship improvements.",
     '<path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.4 5.4 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/>'),
    ("Beautiful Terminal UX", "Every pixel of output is considered — from progress states to panels to the blinking cursor.",
     '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>'),
]
_feat_cards = "\n".join(
    f'''          <article class="feature-card" data-tilt>
            <div class="feature-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{icon}</svg></div>
            <h3>{name}</h3>
            <p>{desc}</p>
          </article>''' for name, desc, icon in _feat)

PAGES["features.html"] = dict(
    title="Features — Seed Code CLI | Streaming AI, Providers, Terminal UX",
    desc="Everything a terminal-native developer needs: streaming responses, OpenRouter and Ollama support, Markdown rendering, syntax highlighting, themes, and cross-platform support.",
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
        <div class="sim-feature reveal-scale" data-tilt>
          <div>
            <span class="eyebrow">🖥 Interactive CLI Simulator</span>
            <h2>Experience Seed Code before downloading.</h2>
            <p>A full terminal simulation in your browser — boot sequence, real commands, natural-language questions, themes, even matrix mode. No install, no account, 100% offline.</p>
          </div>
          <a href="cli/" class="btn btn-primary btn-lg" data-magnetic>Launch <span aria-hidden="true">→</span></a>
        </div>
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
    desc="Install Seed Code CLI with pip or uv, configure a provider with the guided wizard, and launch your first AI session — all in under a minute.",
    transition="circle", enter="blur",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Quick Start</span>
        <h1 data-chars>Up and running in seconds</h1>
        <p>Three commands from zero to your first AI conversation. Zero configuration required to start.</p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="quickstart-grid">
          <div class="qs-steps reveal-left">
            <div class="qs-step">
              <span class="qs-num">1</span>
              <div class="qs-body">
                <h3>Install</h3>
                {code_block("pip install seedcode-cli")}
                <p class="qs-note">Prefer isolation? <code>uv tool install seedcode-cli</code> works too.</p>
              </div>
            </div>
            <div class="qs-step">
              <span class="qs-num">2</span>
              <div class="qs-body">
                <h3>Configure a provider</h3>
                {code_block("seedcode config")}
                <p class="qs-note">The wizard walks you through providers and stores your key in <code>~/.seedcode/config.toml</code>.</p>
              </div>
            </div>
            <div class="qs-step">
              <span class="qs-num">3</span>
              <div class="qs-body">
                <h3>Launch</h3>
                {code_block("seedcode")}
              </div>
            </div>
          </div>
          <div class="cmd-panel reveal-right">
            <h3>Every command</h3>
            <table class="cmd-table">
              <tbody>
                <tr><td><code>seedcode</code></td><td>Launch the interactive assistant</td></tr>
                <tr><td><code>seedcode chat</code></td><td>Start a focused chat session</td></tr>
                <tr><td><code>seedcode config</code></td><td>Providers, keys, and themes wizard</td></tr>
                <tr><td><code>seedcode doctor</code></td><td>Diagnose your setup in one pass</td></tr>
                <tr><td><code>seedcode models</code></td><td>Browse every available model</td></tr>
                <tr><td><code>seedcode update</code></td><td>Update to the latest release</td></tr>
              </tbody>
            </table>
            <a href="docs.html" class="link-arrow">Full documentation <span aria-hidden="true">→</span></a>
          </div>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container container-narrow">
        <div class="callout reveal"><strong>Verify:</strong> run <code>seedcode --version</code> — expected output <code>seedcode v1.0.0</code>. Something off? <code>seedcode doctor</code> checks everything in one pass.</div>
      </div>
    </section>""",
)

# ════════════════════════ DOWNLOAD ════════════════════════
PAGES["download.html"] = dict(
    title="Download — Seed Code CLI for Windows, Linux & macOS",
    desc="Download Seed Code CLI: standalone Windows installer, ZIP package for Linux and macOS via MEGA, or install with pip / uv on any platform with Python 3.9+.",
    transition="wipe", enter="zoom",
    body=f"""    <section class="page-hero">
      <div class="container">
        <span class="eyebrow">Download</span>
        <h1 data-chars>Get Seed Code CLI</h1>
        <p>Latest release: <strong>v1.0.0</strong> · Every option gets you the same beautiful terminal experience.</p>
        <div class="hero-actions">
          <a href="Files/SeedCodeSetup.exe" download="SeedCodeSetup.exe" class="btn btn-primary btn-lg" data-magnetic>{DL_ICON} Download for Windows</a>
          <a href="{GH}/releases" class="btn btn-secondary btn-lg" target="_blank" rel="noopener" data-magnetic>All releases</a>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="sim-strip reveal">
          <p><strong>Don't want to install yet?</strong> Try the Interactive CLI Simulator.</p>
          <a href="cli/" class="btn btn-secondary" data-magnetic>Launch Simulator <span aria-hidden="true">→</span></a>
        </div>
        <div class="download-grid stagger reveal">
          <article class="dl-card" data-tilt>
            <div class="dl-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 5.5 10.5 4.4v7.1H3V5.5zM3 12.5h7.5v7.1L3 18.5v-6zM11.5 4.2 21 3v8.5h-9.5V4.2zM11.5 12.5H21V21l-9.5-1.2v-7.3z"/></svg></div>
            <h3>Windows</h3>
            <p>A guided setup wizard for Windows Terminal, PowerShell, and cmd — no Python required.</p>
            <a class="btn btn-primary btn-block" href="Files/SeedCodeSetup.exe" download="SeedCodeSetup.exe">{DL_ICON} SeedCodeSetup.exe</a>
            <span class="dl-meta">~22 MB · standalone installer</span>
          </article>
          <article class="dl-card" data-tilt>
            <div class="dl-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3"/><path d="M13 15h4"/></svg></div>
            <h3>Linux</h3>
            <p>Includes the complete SeedBot CLI package for Linux and macOS.</p>
            <a class="btn btn-secondary btn-block" href="{MEGA}" target="_blank" rel="noopener" title="For Linux and macOS users, download the ZIP package from MEGA.">
              <span class="mega-badge" aria-hidden="true">M</span> Download ZIP (Linux &amp; macOS)
            </a>
            <span class="dl-meta">Hosted on MEGA · opens in a new tab</span>
          </article>
          <article class="dl-card" data-tilt>
            <div class="dl-icon"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M17.05 12.54c-.03-2.71 2.21-4.01 2.31-4.07-1.26-1.84-3.22-2.09-3.91-2.12-1.66-.17-3.25.98-4.09.98-.85 0-2.15-.96-3.54-.93-1.82.03-3.5 1.06-4.43 2.69-1.9 3.28-.48 8.12 1.34 10.78.9 1.3 1.98 2.76 3.39 2.71 1.36-.05 1.88-.88 3.52-.88 1.65 0 2.11.88 3.55.85 1.47-.02 2.4-1.32 3.29-2.63a11.8 11.8 0 0 0 1.5-3.06c-.04-.01-2.87-1.1-2.93-4.32zM14.36 4.6c.75-.91 1.25-2.17 1.11-3.43-1.08.04-2.38.72-3.15 1.62-.7.8-1.3 2.09-1.14 3.32 1.2.09 2.43-.61 3.18-1.51z"/></svg></div>
            <h3>macOS</h3>
            <p>Includes the complete SeedBot CLI package for Linux and macOS.</p>
            <a class="btn btn-secondary btn-block" href="{MEGA}" target="_blank" rel="noopener" title="For Linux and macOS users, download the ZIP package from MEGA.">
              <span class="mega-badge" aria-hidden="true">M</span> Download ZIP (Linux &amp; macOS)
            </a>
            <span class="dl-meta">Hosted on MEGA · opens in a new tab</span>
          </article>
          <article class="dl-card dl-card-accent" data-tilt>
            <span class="dl-tag">Recommended</span>
            <div class="dl-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M12 2C8.7 2 8 3.5 8 5v2h4v1H5.5C4 8 3 9.2 3 11.5S4 15 5.5 15H8v-2.5C8 10.6 9.6 9 11.5 9h4C17 9 18 8 18 6.5v-1.5C18 3.3 16.5 2 12 2zM10 4.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/><path d="M12 22c3.3 0 4-1.5 4-3v-2h-4v-1h6.5c1.5 0 2.5-1.2 2.5-3.5S20 9 18.5 9H16v2.5c0 1.9-1.6 3.5-3.5 3.5h-4C7 15 6 16 6 17.5v1.5C6 20.7 7.5 22 12 22zm2-2.5a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/></svg></div>
            <h3>pip / uv</h3>
            <p>Works on every platform with Python 3.9+. Easiest to keep updated with <code>seedcode update</code>.</p>
            {code_block("pip install seedcode-cli", small=True)}
            <span class="dl-meta">Isolated install: <code>uv tool install seedcode-cli</code></span>
          </article>
        </div>
        <p class="dl-footnote reveal">Verify with <code>seedcode --version</code> · All releases on <a href="{GH}/releases" rel="noopener">GitHub</a> and <a href="https://pypi.org/project/seedcode-cli/" rel="noopener">PyPI</a>.</p>
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
    ("Configuration", "A guided wizard for providers, API keys, and defaults.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode config\n'), ('t-label', 'Provider   › '), ('t-value', 'OpenRouter\n'),
        ('t-label', 'Model      › '), ('t-value', 'GLM 5.2\n'), ('t-label', 'Theme      › '), ('t-value', 'Midnight\n'),
        ('t-ok', '✓ Saved to ~/.seedcode/config.toml')]),
    ("Diagnostics", "Panels, tables, and progress states that feel native.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode doctor\n'), ('t-ok', '✓ '), ('t-value', 'Python 3.12 detected\n'),
        ('t-ok', '✓ '), ('t-value', 'API key configured\n'), ('t-ok', '✓ '), ('t-value', 'Network reachable (82 ms)\n'),
        ('t-dim', '6/6 checks passed')]),
    ("Themes", "Ship-ready themes tuned for contrast and long sessions.", [
        ('t-prompt', '$ '), ('t-cmd', 'seedcode config theme\n'), ('t-value', '● Midnight   (active)\n'),
        ('t-dim', '○ Paper\n○ Ember\n○ Terminal Classic')]),
    ("Settings", "Everything lives in one clean, versionable TOML file.", [
        ('t-prompt', '$ '), ('t-cmd', 'cat ~/.seedcode/config.toml\n'), ('t-dim', '[provider]\n'),
        ('t-value', 'name = "openrouter"\nmodel = "glm-5.2"\n'), ('t-dim', 'stream = true')]),
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
    desc="Seed Code CLI documentation: installation, every command, configuration, providers (OpenRouter, ZenMux, AeroLink, Ollama), and troubleshooting.",
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
          <p><strong>New here?</strong> Launch the CLI Simulator first.</p>
          <a href="cli/" class="btn btn-secondary" data-magnetic>Launch Simulator <span aria-hidden="true">→</span></a>
        </div>

        <section id="installation">
          <h2>Installation</h2>
          <h3>pip (all platforms)</h3>
          <p>Requires Python 3.9 or newer. Installs straight from PyPI.</p>
          <pre><code><span class="pre-comment"># Install and launch</span>
<span class="pre-accent">$</span> pip install seedcode-cli
<span class="pre-accent">$</span> seedcode

<span class="pre-comment"># Verify</span>
<span class="pre-accent">$</span> seedcode --version
seedcode v1.0.0</code></pre>
          <h3>uv (isolated tool)</h3>
          <pre><code><span class="pre-accent">$</span> uv tool install seedcode-cli</code></pre>
          <h3>Windows installer</h3>
          <p>A standalone setup wizard — no Python required. <a href="Files/SeedCodeSetup.exe" download="SeedCodeSetup.exe">Download SeedCodeSetup.exe</a>.</p>
          <h3>Linux &amp; macOS ZIP</h3>
          <p>Grab the packaged ZIP from <a href="{MEGA}" target="_blank" rel="noopener">MEGA</a> — it includes the complete package for both platforms.</p>
          <div class="callout"><strong>Tip:</strong> whichever method you choose, <code>seedcode doctor</code> confirms everything is in place.</div>
        </section>

        <section id="configuration">
          <h2>Configuration</h2>
          <p>Seed Code stores its settings in a single TOML file at <code>~/.seedcode/config.toml</code>. Run <code>seedcode config</code> for the guided wizard, or edit the file directly.</p>
          <pre><code><span class="pre-comment"># ~/.seedcode/config.toml</span>
[provider]
name = "openrouter"
model = "glm-5.2"
stream = true

[appearance]
theme = "midnight"        <span class="pre-comment"># midnight | paper | ember | terminal-classic</span>
markdown = true</code></pre>
          <h3>API keys</h3>
          <p>Keys are stored securely by the config wizard. For CI and containers, the <code>SEEDCODE_API_KEY</code> environment variable takes precedence over the config file.</p>
        </section>

        <section id="providers">
          <h2>Providers</h2>
          <table class="docs-table">
            <thead><tr><th>Provider</th><th>Best for</th><th>Config value</th></tr></thead>
            <tbody>
              <tr><td>OpenRouter</td><td>Hundreds of models, including free tiers</td><td><code>openrouter</code></td></tr>
              <tr><td>ZenMux</td><td>Unified routing with automatic failover</td><td><code>zenmux</code></td></tr>
              <tr><td>AeroLink</td><td>Low-latency, regional endpoints</td><td><code>aerolink</code></td></tr>
              <tr><td>Ollama</td><td>Fully local, private, no API key</td><td><code>ollama</code></td></tr>
            </tbody>
          </table>
          <p>Browse availability any time with <code>seedcode models</code> — 312+ models on OpenRouter, 47+ of them free.</p>
        </section>

        <section id="commands">
          <h2>Commands</h2>
          <table class="docs-table">
            <thead><tr><th>Command</th><th>Description</th></tr></thead>
            <tbody>
              <tr><td><code>seedcode</code></td><td>Launch the interactive assistant in your current directory</td></tr>
              <tr><td><code>seedcode chat</code></td><td>Start a focused chat session with your configured model</td></tr>
              <tr><td><code>seedcode config</code></td><td>Open the configuration wizard for providers, keys, and themes</td></tr>
              <tr><td><code>seedcode doctor</code></td><td>Diagnose your setup — keys, connectivity, and environment</td></tr>
              <tr><td><code>seedcode models</code></td><td>Browse and search every model available on your provider</td></tr>
              <tr><td><code>seedcode update</code></td><td>Update Seed Code CLI to the latest release in place</td></tr>
            </tbody>
          </table>
        </section>

        <section id="examples">
          <h2>Examples</h2>
          <h3>One-shot prompts</h3>
          <pre><code><span class="pre-accent">$</span> seedcode "write a haiku about git"
branches drift apart
a merge brings them home again
conflicts, then release</code></pre>
          <h3>Health check</h3>
          <pre><code><span class="pre-accent">$</span> seedcode doctor
✓ Python 3.12 detected
✓ API key configured
✓ Network reachable (82 ms)
6/6 checks passed · environment healthy</code></pre>
        </section>

        <section id="troubleshooting">
          <h2>Troubleshooting</h2>
          <ul>
            <li><strong>Command not found</strong> — make sure your Python scripts directory is on PATH, or reinstall with <code>uv tool install seedcode-cli</code>.</li>
            <li><strong>Auth errors</strong> — re-run <code>seedcode config</code> or check <code>SEEDCODE_API_KEY</code>.</li>
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
    desc="Seed Code CLI version history and roadmap: what shipped in v1.0.0 and what's coming — plugins, MCP, voice, memory, desktop app, and agent mode.",
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
            <h3>v1.0.0 <span class="tag tag-latest">Latest</span> <span class="changelog-date">2026</span></h3>
            <ul>
              <li><strong>CLI</strong> — the full interactive command-line experience, shipped and stable</li>
              <li><strong>Streaming</strong> — real-time token streaming across every supported provider</li>
              <li><strong>Themes</strong> — Midnight, Paper, Ember, and Terminal Classic with careful contrast tuning</li>
              <li><strong>Configuration</strong> — a complete configuration system with a guided setup wizard</li>
              <li><strong>Providers</strong> — OpenRouter, ZenMux, AeroLink, and local Ollama</li>
            </ul>
          </div>

          <h2 class="timeline-heading reveal">Upcoming</h2>
          <div class="timeline-item reveal"><h3>Plugins <span class="tag tag-soon">Planned</span></h3><p>Extend Seed Code with community-built commands and renderers.</p></div>
          <div class="timeline-item reveal"><h3>MCP <span class="tag tag-soon">Planned</span></h3><p>Model Context Protocol support for tools and external context.</p></div>
          <div class="timeline-item reveal"><h3>Voice <span class="tag tag-soon">Planned</span></h3><p>Talk to your terminal — dictate prompts and hear responses.</p></div>
          <div class="timeline-item reveal"><h3>Memory <span class="tag tag-soon">Planned</span></h3><p>Persistent, local-first memory across sessions and projects.</p></div>
          <div class="timeline-item reveal"><h3>Desktop App <span class="tag tag-soon">Planned</span></h3><p>The Seed Code experience in a native desktop shell.</p></div>
          <div class="timeline-item reveal"><h3>Agent Mode <span class="tag tag-soon">Planned</span></h3><p>Multi-step autonomous coding with plan, execute, and review.</p></div>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="cta reveal-scale">
          <h2>Help shape the roadmap.</h2>
          <p>Feature requests, bug reports, and pull requests are all welcome.</p>
          <div class="hero-actions">
            <a href="{GH}" class="btn btn-primary btn-lg" rel="noopener" data-magnetic>Contribute on GitHub</a>
            <a href="download.html" class="btn btn-secondary btn-lg" data-magnetic>Get Seed Code CLI</a>
          </div>
        </div>
      </div>
    </section>""",
)

# ════════════════════════ FAQ ════════════════════════
_faqs = [
    ("Is Seed Code free?", "Yes. Seed Code CLI is free and open source under the MIT license. You only pay your AI provider for model usage — and through OpenRouter you can use many models entirely for free."),
    ("Can I install using pip?", "Yes. Run <code>pip install seedcode-cli</code> with Python 3.9 or newer, then launch it with the <code>seedcode</code> command from any terminal."),
    ("Can I install using uv?", "Yes. Run <code>uv tool install seedcode-cli</code> to install it as an isolated tool with uv. This keeps Seed Code out of your project environments and makes updates instant."),
    ("Does it support Windows?", "Fully. Seed Code runs natively on Windows (including Windows Terminal and PowerShell), plus Linux and macOS. Windows users can also download the standalone SeedCodeSetup.exe installer from the <a href='download.html'>download page</a>."),
    ("Which providers are supported?", "Seed Code supports OpenRouter, ZenMux, and AeroLink out of the box, plus fully local models through Ollama. Through OpenRouter alone you get access to hundreds of models, including free-tier options."),
    ("How do I configure my API key?", "Run <code>seedcode config</code> and the setup wizard will walk you through choosing a provider and storing your API key securely in <code>~/.seedcode/config.toml</code>. You can also set the <code>SEEDCODE_API_KEY</code> environment variable."),
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
    desc="Quick answers about Seed Code CLI: installation with pip and uv, pricing, Windows support, providers, and API key configuration.",
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
    desc="The story behind Seed Code CLI: built by Al Shahriar Sowan and published by Eagox Studio to make the terminal the best place to work with AI.",
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
        <p>Every pixel of output is considered — streaming that renders tokens the instant they arrive, Markdown and syntax highlighting that read like your editor, themes tuned for long sessions, and a configuration system that stays out of your way. Fast cold starts, no telemetry, MIT licensed.</p>
        <h2>The team</h2>
        <p>Seed Code CLI is designed and developed by <strong>Eagox Studio</strong>, created by <a href="{PF}" target="_blank" rel="noopener">Al Shahriar Sowan</a> — a developer who cares deeply about tools that feel as good as they function. See the <a href="portfolio.html">portfolio</a> for more of his work.</p>
        <div class="callout"><strong>Open source:</strong> the entire project is developed in the open on <a href="{GH}" rel="noopener">GitHub</a>. Issues, ideas, and pull requests are always welcome.</div>
      </div>
    </section>""",
)

# ════════════════════════ PORTFOLIO ════════════════════════
PAGES["portfolio.html"] = dict(
    title="Al Shahriar Sowan — Developer Portfolio | Creator of Seed Code CLI",
    desc="Al Shahriar Sowan is a developer and founder of Eagox Studio, creator of Seed Code CLI. Projects, skills, experience, and contact.",
    transition="circle", enter="zoom",
    body=f"""    <section class="pf-hero">
      <div class="container">
        <div class="pf-avatar reveal-scale visible">AS</div>
        <h1 data-chars>Al Shahriar Sowan</h1>
        <span class="pf-role">Developer · Founder, Eagox Studio</span>
        <p>Building developer tools that feel as good as they function. Creator of Seed Code CLI — the beautiful AI coding assistant for the terminal.</p>
        <div class="pf-links">
          <a href="{PF}" class="btn btn-primary" target="_blank" rel="noopener" data-magnetic>Visit Portfolio Site</a>
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
            <p>An AI coding assistant for the terminal with streaming responses, multi-provider support, and a polished TUI. Python · MIT licensed.</p>
            <a href="{GH}" class="link-arrow" rel="noopener">View on GitHub <span aria-hidden="true">→</span></a>
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
            <a href="{PF}" class="link-arrow" target="_blank" rel="noopener">Learn more <span aria-hidden="true">→</span></a>
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
            <p>Built an AI terminal assistant from scratch: provider integrations, streaming engine, theming system, and cross-platform packaging.</p>
          </div>
          <div class="timeline-item reveal">
            <h3>Independent Developer <span class="changelog-date">Earlier</span></h3>
            <p>Web experiences, automation, and open-source contributions — learning by shipping.</p>
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
        <p>The built-in diagnostics check your Python version, API key, network, and terminal capabilities in one pass.</p>
        <pre><code><span class="pre-accent">$</span> seedcode doctor</code></pre>
        <h2>2. Check the docs &amp; FAQ</h2>
        <ul>
          <li><a href="docs.html">Documentation</a> — installation, commands, configuration, providers</li>
          <li><a href="faq.html">FAQ</a> — installation methods, pricing, platform support</li>
          <li><a href="quickstart.html">Quick Start</a> — zero to first session in under a minute</li>
        </ul>
        <h2>3. Ask the community</h2>
        <ul>
          <li><strong>Bugs &amp; feature requests</strong> — <a href="{GH}/issues" rel="noopener">GitHub Issues</a></li>
          <li><strong>Releases</strong> — <a href="{GH}/releases" rel="noopener">GitHub Releases</a> · <a href="https://pypi.org/project/seedcode-cli/" rel="noopener">PyPI</a></li>
          <li><strong>The maintainer</strong> — <a href="{PF}" rel="noopener">Al Shahriar Sowan</a> (Eagox Studio)</li>
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
          <li><strong>API keys</strong> are stored locally in <code>~/.seedcode/config.toml</code> on your machine and are only sent to the provider you configured.</li>
          <li><strong>Prompts and responses</strong> travel directly between your machine and your chosen AI provider (OpenRouter, ZenMux, AeroLink, or your local Ollama instance). There are no Seed Code servers in between.</li>
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
        <p>Seed Code CLI is open-source software released under the <a href="{GH}/blob/main/LICENSE" rel="noopener">MIT License</a>. You may use, copy, modify, and distribute it in accordance with that license.</p>
        <h2>No warranty</h2>
        <p>The software is provided <strong>"as is"</strong>, without warranty of any kind, express or implied. The authors and Eagox Studio are not liable for any claim, damages, or other liability arising from its use.</p>
        <h2>AI providers</h2>
        <p>Seed Code CLI connects to third-party AI providers using credentials you supply. Your use of those providers — including costs, rate limits, and acceptable-use policies — is governed by their own terms of service. You are responsible for reviewing the output of AI models before relying on it.</p>
        <h2>This website</h2>
        <p>Content on this site is provided for information about the project. Downloads are provided in good faith; verify checksums where available.</p>
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
          <a href="cli/" class="btn btn-secondary btn-lg" data-magnetic>Lost? Launch the CLI Simulator instead</a>
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
    <lastmod>2026-07-18</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{'1.0' if p == 'index.html' else '0.7'}</priority>
  </url>""" for p in PAGES if p != "404.html")
    urls += f"""
  <url>
    <loc>{SITE}/cli/</loc>
    <lastmod>2026-07-18</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>"""
    (ROOT / "sitemap.xml").write_text(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
""", encoding="utf-8")
    print("wrote sitemap.xml")


if __name__ == "__main__":
    main()
