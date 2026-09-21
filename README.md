# Seed Code CLI — Cinematic Website

Official multi-page website for **Seed Code CLI v6.2.5**, the beautiful AI coding
assistant for the terminal. Built by **Al Shahriar Sayon**
(https://alshahriarsayon.vercel.app/) · Part of the **Eagox Studio** ecosystem
(https://eagoxstudio.vercel.app/).

A desktop-first cinematic experience: splash screen, a quiet layered background
(subtle grid, soft radial lighting, vignette, film grain), GSAP character-level
animation, cinematic page transitions, custom cursor, and a fully scripted
interactive terminal.

## Structure

```
ssedcode-web/
├── index.html        # Home — splash, hero + terminal, stats, teaser, CTA
├── features.html     # 12 feature cards, tilt + glow
├── quickstart.html   # 3-step guide + command panel (official install commands)
├── download.html     # Official Windows irm|iex and Linux curl|bash installers
├── docs.html         # Sidebar docs: install, config, providers, commands
├── gallery.html      # 6 mini-terminal session screens
├── changelog.html    # Timeline: v6.2.5 shipped + roadmap
├── faq.html          # Accordion + FAQPage JSON-LD
├── about.html        # Project story, Eagox Studio
├── portfolio.html    # Al Shahriar Sayon — projects, skills, experience, contact
├── support.html      # Help paths, community links
├── privacy.html      # No-telemetry policy
├── terms.html        # MIT terms
├── 404.html          # Glitch 404
├── css/style.css     # Design system + motion layer
├── js/main.js        # Cinematic engine (splash, transitions, GSAP, cursor, terminal…)
├── scripts/build-pages.py  # Page generator — edit content here, then re-run
├── img/              # seedcode.ico (brand — do not replace), logo.svg/png
├── site.webmanifest · sitemap.xml · robots.txt · google*.html
```

## Editing pages

Pages share one shell (head/nav/footer/background/scripts) defined in
`scripts/build-pages.py`. Edit content there and regenerate:

```bash
python scripts/build-pages.py
```

Hand-editing the generated HTML works too, but the build script is the source
of truth for anything shared — including the version constant (`VERSION`), the
official install commands (`WIN_CMD` / `LINUX_CMD`), the release URL, and the
author/company links.

## Loading flow

`index.html` shows the splash screen (logo + tagline + status, ~1.3s, once per
session via the `sc-intro` sessionStorage key), then hands off straight to the
homepage — the UI builds itself beneath the splash's blur fade. There is no
second loading screen. Internal navigation keeps the cinematic page-transition
system (wipe / slide / circle overlays in `.pt-overlay`).

## Motion stack

- **Lenis** — smooth scrolling (CDN, desktop only)
- **GSAP + ScrollTrigger** — char/word reveals, blur dissolves, pinned scrub
- Background is pure CSS — subtle terminal grid, soft radial green lighting,
  gentle vignette, and low-opacity noise. No particles, no WebGL.
- All CDN libraries are *guarded*: if any fails to load, the site falls back to
  native scrolling and CSS reveals. Everything honors `prefers-reduced-motion`.

## Local preview

```bash
python -m http.server 8080 --directory <path-to-this-folder>
```

Note: the splash plays once per browser session (sessionStorage key
`sc-intro`); clear it or use a fresh tab to replay.

## Deployment

Static files, no build step required for deploys. Canonical domain:
`https://seedcode-web.vercel.app/` — update in `scripts/build-pages.py`,
then regenerate, if the domain changes.
