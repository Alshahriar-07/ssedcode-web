# Seed Code CLI — Cinematic Website

Official multi-page website for Seed Code CLI, the beautiful AI coding assistant
for the terminal. Designed & developed by **Eagox Studio** · Creator —
**Al Shahriar Sowan** (https://alshahriarsayon.vercel.app/).

A desktop-first cinematic experience: AI boot intro, Three.js WebGL background,
GSAP character-level animation, cinematic page transitions, custom cursor, and a
fully scripted interactive terminal.

## Structure

```
Seedcode-cli.io/
├── index.html        # Home — intro boot sequence, hero + terminal, stats, teaser, CTA
├── features.html     # 12 feature cards, tilt + glow
├── quickstart.html   # 3-step guide + command panel (slide-in left/right)
├── download.html     # Windows .exe, MEGA ZIP (Linux/macOS), pip/uv
├── docs.html         # Sidebar docs: install, config, providers, commands
├── gallery.html      # 6 mini-terminal session screens
├── changelog.html    # Timeline: v1.0.0 shipped + roadmap
├── faq.html          # Accordion + FAQPage JSON-LD
├── about.html        # Project story, Eagox Studio
├── portfolio.html    # Al Shahriar Sowan — projects, skills, experience, contact
├── support.html      # Help paths, community links
├── privacy.html      # No-telemetry policy
├── terms.html        # MIT terms
├── 404.html          # Glitch 404
├── css/style.css     # Design system + motion layer
├── js/main.js        # Cinematic engine (intro, transitions, GSAP, cursor, terminal…)
├── js/three-bg.js    # Three.js particle universe + network lines + camera
├── scripts/build-pages.py  # Page generator — edit content here, then re-run
├── img/              # seedcode.ico (brand — do not replace), logo.svg/png
├── Files/SeedCodeSetup.exe # Windows installer (~22 MB)
├── site.webmanifest · sitemap.xml · robots.txt · google*.html
```

## Editing pages

Pages share one shell (head/nav/footer/background/scripts) defined in
`scripts/build-pages.py`. Edit content there and regenerate:

```bash
python scripts/build-pages.py
```

Hand-editing the generated HTML works too, but the build script is the source
of truth for anything shared.

## Motion stack

- **Lenis** — smooth scrolling (CDN, desktop only)
- **GSAP + ScrollTrigger** — char/word reveals, blur dissolves, pinned scrub
- **Three.js** — 700-particle field, network lines, fog, mouse-parallax camera
- All CDN libraries are *guarded*: if any fails to load, the site falls back to
  native scrolling, CSS reveals, and a 2D canvas particle field. Everything
  honors `prefers-reduced-motion`.

## Local preview

```bash
python -m http.server 8080 --directory D:/Seedcode-cli.io
```

Note: the intro plays once per browser session (sessionStorage key `sc-intro`);
clear it or use a fresh tab to replay.

## Deployment

Static files, no build step required for deploys. Canonical domain:
`https://seedcode-cli.vercel.app/` — update in `scripts/build-pages.py`,
then regenerate, if the domain changes.
