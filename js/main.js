/* ============================================================
   Seed Code CLI — main.js · cinematic engine
   ------------------------------------------------------------
   · Splash screen (home, once/session) → straight to the page
   · Cinematic page transitions (wipe / slide / circle variants)
   · Lenis smooth scrolling + GSAP ScrollTrigger (CDN, guarded —
     everything degrades to native behavior if they fail to load)
   · Mouse spotlight · magnetic buttons
   · 3D tilt + pointer glow · ripple · parallax
   · Scroll reveal / stagger / counters · scripted terminal
   · Navbar state · mobile nav · copy buttons · docs sidebar
   All effects are transform/opacity, rAF-driven, paused when
   hidden, and disabled under prefers-reduced-motion.
   ============================================================ */

(function () {
  "use strict";

  const motionOK = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const desktop = window.innerWidth >= 900;

  /* ============================================================
     Motion libraries — Lenis + GSAP are lazy-loaded after first
     paint (see loadMotionLibs at the bottom) so they never block
     startup. Until they land: native scrolling + CSS reveals.
     ============================================================ */
  let lenis = null;
  let gsapOK = false;
  document.documentElement.classList.add("no-lenis");

  function initMotionLibs() {
    if (motionOK && desktop && typeof window.Lenis === "function") {
      document.documentElement.classList.remove("no-lenis");
      lenis = new window.Lenis({ lerp: 0.11, wheelMultiplier: 1, smoothWheel: true });
      const raf = (t) => { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
    }
    gsapOK = motionOK && window.gsap && window.ScrollTrigger;
    if (gsapOK) {
      window.gsap.registerPlugin(window.ScrollTrigger);
      if (lenis) lenis.on("scroll", window.ScrollTrigger.update);
    }
    initParallax();
    if (gsapOK) initGsapReveals();
  }

  /* ============================================================
     Splash screen (home only, once per session)
     splash: CSS-animated from first paint (see inline head CSS);
     JS only cycles the status text and ends it ~1.3s after
     navigation start, then hands off straight to the homepage —
     the UI builds itself beneath the splash's blur fade.
     Repeat visits: the inline head script tags <html>.sc-seen so
     the splash is display:none before paint — here we just
     remove it.
     ============================================================ */
  const splash = document.querySelector(".splash");
  if (splash) {
    const seen = sessionStorage.getItem("sc-intro");
    if (seen || !motionOK) {
      splash.remove();
      document.querySelectorAll(".build-in").forEach((el) => el.classList.add("built"));
    } else {
      document.body.style.overflow = "hidden";

      const reveal = () => {
        document.querySelector("main")?.classList.add("cinema-in");
        document.querySelectorAll(".build-in").forEach((el) => el.classList.add("built"));
      };

      let finished = false;
      const finish = () => {
        if (finished) return;
        finished = true;
        sessionStorage.setItem("sc-intro", "1");
        splash.classList.add("done");                      // soft blur hand-off
        setTimeout(() => splash.remove(), 500);
        reveal();                                          // homepage builds beneath the fade
        document.body.style.overflow = "";                 // scrolling unlocked right away
      };

      // splash: already animating via CSS since first paint — JS only
      // cycles the status text and hands off ~1.3s after nav start.
      const statusEl = splash.querySelector(".splash-status-text");
      const wait = (ms) => new Promise((r) => setTimeout(r, ms));
      (async () => {
        const elapsed = performance.now();                 // time already on screen
        const remaining = Math.max(0, 1300 - elapsed);
        const step = remaining / 3;
        for (const s of ["Loading components...", "Preparing interface...", "Ready."]) {
          if (finished) return;
          await wait(step);
          if (statusEl) statusEl.textContent = s;
        }
        finish();
      })();

      setTimeout(finish, 4000);                            // hard cap: splash ~1.3s
    }
  } else {
    document.querySelectorAll(".build-in").forEach((el) => el.classList.add("built"));
  }

  /* ============================================================
     Page transitions — intercept internal nav links
     ============================================================ */
  const overlay = document.querySelector(".pt-overlay");
  if (overlay) {
    // entering: play reveal if we arrived via a transition
    if (motionOK && sessionStorage.getItem("sc-nav")) {
      sessionStorage.removeItem("sc-nav");
      overlay.classList.add("enter");
      overlay.addEventListener("animationend", () => overlay.classList.remove("enter"), { once: true });
    }

    // leaving
    if (motionOK) {
      document.addEventListener("click", (e) => {
        const a = e.target.closest("a");
        if (!a) return;
        const href = a.getAttribute("href") || "";
        if (
          a.target === "_blank" || a.hasAttribute("download") ||
          href.startsWith("#") || href.startsWith("http") ||
          href.startsWith("mailto:") || e.metaKey || e.ctrlKey || e.shiftKey
        ) return;
        e.preventDefault();
        sessionStorage.setItem("sc-nav", "1");
        overlay.classList.add("leave");
        setTimeout(() => { window.location.href = href; }, 640);
      });
    }
  }

  /* ============================================================
     Scroll progress
     ============================================================ */
  const progressBar = document.querySelector(".scroll-progress");
  if (progressBar) {
    let ticking = false;
    const update = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progressBar.style.transform = `scaleX(${max > 0 ? window.scrollY / max : 0})`;
      ticking = false;
    };
    window.addEventListener("scroll", () => {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ============================================================
     Navbar state + active link + mobile nav
     ============================================================ */
  const navWrap = document.querySelector(".nav-wrap");
  if (navWrap) {
    const setNav = () => navWrap.classList.toggle("scrolled", window.scrollY > 12);
    window.addEventListener("scroll", setNav, { passive: true });
    setNav();

    const here = location.pathname.split("/").pop() || "index.html";
    navWrap.querySelectorAll(".nav-links a:not(.btn)").forEach((a) => {
      const target = (a.getAttribute("href") || "").split("#")[0];
      if (target === here) a.classList.add("nav-active");
    });
  }

  const toggle = document.querySelector(".nav-toggle");
  const links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", () => {
      const open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.addEventListener("click", (e) => {
      if (e.target.closest("a")) {
        links.classList.remove("open");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ============================================================
     Mouse spotlight
     ============================================================ */
  const spotlight = document.querySelector(".bg-spotlight");
  if (spotlight && motionOK && finePointer) {
    let tx = window.innerWidth / 2, ty = window.innerHeight * 0.3;
    let x = tx, y = ty, raf = 0;
    const tick = () => {
      x += (tx - x) * 0.09;
      y += (ty - y) * 0.09;
      spotlight.style.transform = `translate3d(${x - 380}px, ${y - 380}px, 0)`;
      if (Math.abs(tx - x) > 0.5 || Math.abs(ty - y) > 0.5) raf = requestAnimationFrame(tick);
      else raf = 0;
    };
    window.addEventListener("pointermove", (e) => {
      tx = e.clientX; ty = e.clientY;
      if (!raf) raf = requestAnimationFrame(tick);
    }, { passive: true });
  }

  /* ============================================================
     Magnetic buttons
     ============================================================ */
  if (motionOK && finePointer) {
    document.querySelectorAll("[data-magnetic]").forEach((el) => {
      const strength = 0.32;
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        el.style.transform =
          `translate(${(e.clientX - (r.left + r.width / 2)) * strength}px, ${(e.clientY - (r.top + r.height / 2)) * strength}px)`;
      });
      el.addEventListener("pointerleave", () => { el.style.transform = ""; });
    });
  }

  /* ============================================================
     Ripple
     ============================================================ */
  document.querySelectorAll(".btn").forEach((btn) => {
    btn.addEventListener("pointerdown", (e) => {
      if (!motionOK) return;
      const r = btn.getBoundingClientRect();
      const ripple = document.createElement("span");
      ripple.className = "ripple";
      const size = Math.max(r.width, r.height) * 2.2;
      ripple.style.width = ripple.style.height = size + "px";
      ripple.style.left = (e.clientX - r.left - size / 2) + "px";
      ripple.style.top = (e.clientY - r.top - size / 2) + "px";
      btn.appendChild(ripple);
      ripple.addEventListener("animationend", () => ripple.remove());
    });
  });

  /* ============================================================
     3D tilt + pointer-tracked glow
     ============================================================ */
  if (motionOK && finePointer) {
    document.querySelectorAll("[data-tilt]").forEach((card) => {
      let raf = 0, rx = 0, ry = 0, trx = 0, try_ = 0;
      const render = () => {
        rx += (trx - rx) * 0.18;
        ry += (try_ - ry) * 0.18;
        card.style.transform = `perspective(800px) rotateX(${rx}deg) rotateY(${ry}deg) translateY(-3px)`;
        if (Math.abs(trx - rx) > 0.02 || Math.abs(try_ - ry) > 0.02) raf = requestAnimationFrame(render);
        else raf = 0;
      };
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        try_ = ((e.clientX - r.left) / r.width - 0.5) * 7;
        trx = (0.5 - (e.clientY - r.top) / r.height) * 7;
        card.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100) + "%");
        card.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100) + "%");
        if (!raf) raf = requestAnimationFrame(render);
      });
      card.addEventListener("pointerleave", () => {
        trx = 0; try_ = 0;
        if (!raf) raf = requestAnimationFrame(render);
        setTimeout(() => { card.style.transform = ""; }, 260);
      });
    });
  }

  /* ============================================================
     Parallax — GSAP if available, else rAF fallback
     (called from initMotionLibs once libraries have loaded)
     ============================================================ */
  function initParallax() {
    const parallaxEls = document.querySelectorAll("[data-parallax]");
    if (!parallaxEls.length || !motionOK || !desktop) return;
    if (gsapOK) {
      parallaxEls.forEach((el) => {
        const speed = parseFloat(el.getAttribute("data-parallax")) || 0.15;
        window.gsap.to(el, {
          yPercent: speed * -100,
          ease: "none",
          scrollTrigger: { trigger: el, start: "top bottom", end: "bottom top", scrub: 0.6 },
        });
      });
    } else {
      let ticking = false;
      const update = () => {
        parallaxEls.forEach((el) => {
          const speed = parseFloat(el.getAttribute("data-parallax")) || 0.15;
          const r = el.getBoundingClientRect();
          const mid = r.top + r.height / 2 - window.innerHeight / 2;
          el.style.transform = `translate3d(0, ${mid * -speed}px, 0)`;
        });
        ticking = false;
      };
      window.addEventListener("scroll", () => {
        if (!ticking) { ticking = true; requestAnimationFrame(update); }
      }, { passive: true });
      update();
    }
  }

  /* ============================================================
     Custom cursor — dot + trailing glow ring (desktop only)
     ============================================================ */
  if (motionOK && finePointer && desktop) {
    const dot = document.createElement("div");
    dot.className = "cursor-dot";
    const ring = document.createElement("div");
    ring.className = "cursor-ring";
    document.body.append(dot, ring);
    document.body.classList.add("has-cursor");

    let mx = -100, my = -100, rx = -100, ry = -100, raf = 0;
    const tick = () => {
      rx += (mx - rx) * 0.16;
      ry += (my - ry) * 0.16;
      dot.style.transform = `translate3d(${mx - 3}px, ${my - 3}px, 0)`;
      const half = ring.offsetWidth / 2;
      ring.style.transform = `translate3d(${rx - half}px, ${ry - half}px, 0)`;
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    window.addEventListener("pointermove", (e) => { mx = e.clientX; my = e.clientY; }, { passive: true });
    document.addEventListener("pointerover", (e) => {
      ring.classList.toggle("hovering", !!e.target.closest("a, button, summary"));
    }, { passive: true });
    document.addEventListener("visibilitychange", () => {
      if (document.hidden) { cancelAnimationFrame(raf); raf = 0; }
      else if (!raf) raf = requestAnimationFrame(tick);
    });
  }

  /* ============================================================
     GSAP char-level headline reveals + pinned sections
     (called from initMotionLibs once GSAP has loaded)
     ============================================================ */
  function initGsapReveals() {
    // Character stagger on [data-chars] headlines
    document.querySelectorAll("[data-chars]").forEach((el) => {
      const split = [];
      el.childNodes.forEach((node) => {
        if (node.nodeType === 3) {
          for (const ch of node.textContent) {
            if (/\s/.test(ch)) split.push(document.createTextNode(ch));
            else {
              const s = document.createElement("span");
              s.style.display = "inline-block";
              s.textContent = ch;
              split.push(s);
            }
          }
        } else {
          // keep accent spans whole but make them animatable
          node.style.display = "inline-block";
          split.push(node.cloneNode(true));
        }
      });
      el.textContent = "";
      split.forEach((n) => el.appendChild(n));
      const chars = el.querySelectorAll("span");
      window.gsap.from(chars, {
        yPercent: 110, opacity: 0, rotateZ: 4,
        duration: 0.7, ease: "back.out(1.6)", stagger: 0.022,
        scrollTrigger: { trigger: el, start: "top 88%", once: true },
      });
    });

    // Section heads: blur-dissolve timeline
    document.querySelectorAll(".gsap-head").forEach((el) => {
      window.gsap.from(el.children, {
        y: 34, opacity: 0, filter: "blur(8px)",
        duration: 0.9, ease: "power3.out", stagger: 0.12,
        scrollTrigger: { trigger: el, start: "top 85%", once: true },
      });
    });

    // Pinned hero terminal zoom-out on scroll (home)
    if (desktop) {
      const heroTerm = document.querySelector(".hero .terminal-frame");
      if (heroTerm) {
        window.gsap.fromTo(heroTerm, { scale: 1 }, {
          scale: 0.94, opacity: 0.65, ease: "none",
          scrollTrigger: { trigger: ".hero", start: "bottom 70%", end: "bottom 10%", scrub: 0.5 },
        });
      }
      // Pinned stats band: numbers scale up while pinned briefly
      const statsBand = document.querySelector(".stats[data-pin]");
      if (statsBand) {
        window.gsap.fromTo(statsBand.querySelectorAll(".stat-num"),
          { scale: 0.92 },
          { scale: 1, ease: "none",
            scrollTrigger: { trigger: statsBand, start: "top 80%", end: "top 30%", scrub: 0.4 } });
      }
    }
  }

  /* ============================================================
     Copy-to-clipboard
     ============================================================ */
  document.querySelectorAll(".copy-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const text = btn.getAttribute("data-copy");
      if (!text) return;
      const done = () => {
        btn.classList.add("copied");
        const label = btn.querySelector(".copy-label");
        const prev = label ? label.textContent : null;
        if (label) label.textContent = "Copied!";
        setTimeout(() => {
          btn.classList.remove("copied");
          if (label && prev) label.textContent = prev;
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
      } else fallbackCopy(text, done);
    });
  });

  function fallbackCopy(text, done) {
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed";
    ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand("copy"); done(); } catch (e) { /* unavailable */ }
    document.body.removeChild(ta);
  }

  /* ============================================================
     Counters
     ============================================================ */
  function animateCounter(el) {
    const target = parseFloat(el.getAttribute("data-target")) || 0;
    if (!motionOK) { el.textContent = String(target); return; }
    const dur = 1500, start = performance.now();
    const tick = (now) => {
      const t = Math.min((now - start) / dur, 1);
      el.textContent = String(Math.round(target * (1 - Math.pow(1 - t, 3))));
      if (t < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  /* ============================================================
     Word stagger + scroll reveal
     ============================================================ */
  document.querySelectorAll(".words").forEach((el) => {
    if (!motionOK) return;
    const nodes = [];
    el.childNodes.forEach((node) => {
      if (node.nodeType === 3) {
        node.textContent.split(/(\s+)/).forEach((part) => {
          if (/^\s+$/.test(part)) nodes.push(document.createTextNode(part));
          else if (part) {
            const s = document.createElement("span");
            s.className = "w";
            s.textContent = part;
            nodes.push(s);
          }
        });
      } else nodes.push(node.cloneNode(true));
    });
    el.textContent = "";
    nodes.forEach((n) => el.appendChild(n));
    el.querySelectorAll(".w").forEach((w, i) => w.style.transitionDelay = (i * 55) + "ms");
  });

  const revealEls = document.querySelectorAll(".reveal, .reveal-scale, .reveal-blur, .reveal-left, .reveal-right, .stagger, .words");
  function activate(el) {
    el.classList.add("visible");
    el.querySelectorAll(".counter").forEach(animateCounter);
  }
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { activate(entry.target); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    revealEls.forEach((el) => {
      if (el.classList.contains("visible")) el.querySelectorAll(".counter").forEach(animateCounter);
      else io.observe(el);
    });
  } else revealEls.forEach(activate);

  /* ============================================================
     Hero mini-simulator — auto-types real Seed Code commands and
     streams compact answers, then loops. Powers the animated
     terminal in the hero via [data-minisim].
     ============================================================ */
  const MINISIM = [
    { cmd: "help", out: [
      ["c", "Seed Code CLI — v6.2.5 commands"],
      ["g", "  /provider  /model  /apikey  /settings  /doctor"],
      ["g", "  /mode  /codemode  /assist  /tools  /index  /history"],
      ["d", "  …or ask a natural question."],
    ]},
    { cmd: "features", out: [
      ["ok", "Streaming responses with live markdown + highlighting"],
      ["ok", "Six providers · Default · OpenRouter · FreeModel · Ollama"],
      ["ok", "Code Mode + /assist desktop control"],
      ["ok", "One-line installers for Windows & Linux · no Python"],
    ]},
    { cmd: "what is seed code", out: [
      ["r2", "Seed Code CLI is an AI coding assistant that lives in"],
      ["r2", "your terminal — streaming answers from the provider"],
      ["r2", "of your choice, rendered beautifully."],
    ]},
    { cmd: "why is it free", out: [
      ["r2", "Start instantly on the built-in Default provider —"],
      ["r2", "no API key needed. 45+ models are free via OpenRouter,"],
      ["r2", "FreeModel keys are free too, or run Ollama locally."],
    ]},
    { cmd: "/assist", out: [
      ["ok", "Assist Mode ON — AI + computer control"],
      ["g", "  AI · files · terminal · git · browser · keyboard"],
      ["g", "  mouse · windows · vision · OCR · automation"],
      ["d", "  /assist off returns to plain chat."],
    ]},
  ];

  function runMiniSim(el, script, opts) {
    const speed = opts?.speed || 1;
    const wait = (ms) => new Promise((r) => setTimeout(r, ms * speed));
    const CLS = { c: "t-cmd", g: "t-value", d: "t-dim", ok: "t-value", r2: "t-resp" };
    const cursor = document.createElement("span");
    cursor.className = "t-cursor";
    let started = false;

    const line = (parent) => {
      const d = document.createElement("div");
      d.className = "t-line";
      el.appendChild(d);
      el.scrollTop = el.scrollHeight;
      return d;
    };
    const span = (cls, text) => {
      const s = document.createElement("span");
      s.className = cls; s.textContent = text;
      return s;
    };

    async function loop() {
      if (!motionOK) {
        // static render of first item
        const first = script[0];
        const l = line();
        l.append(span("t-prompt", "❯ "), span("t-cmd", first.cmd));
        first.out.forEach(([k, t]) => {
          const o = line();
          if (k === "ok") o.append(span("t-ok", "✓ "));
          o.append(span(CLS[k], t));
        });
        return;
      }
      for (;;) {
        el.textContent = "";
        for (const item of script) {
          const l = line();
          l.append(span("t-prompt", "❯ "));
          l.appendChild(cursor);
          const target = span("t-cmd", "");
          l.insertBefore(target, cursor);
          for (const ch of item.cmd) {
            target.textContent += ch;
            el.scrollTop = el.scrollHeight;
            await wait(34 + Math.random() * 40);
          }
          await wait(300);
          for (const [k, t] of item.out) {
            const o = line();
            o.appendChild(cursor);
            if (k === "ok") o.insertBefore(span("t-ok", "✓ "), cursor);
            const os = span(CLS[k], "");
            o.insertBefore(os, cursor);
            for (const word of t.split(/(?<=\s)/)) {
              os.textContent += word;
              el.scrollTop = el.scrollHeight;
              await wait(20);
            }
            await wait(90);
          }
          await wait(1000);
        }
        await wait(600);
      }
    }

    const start = () => { if (!started) { started = true; loop(); } };
    if ("IntersectionObserver" in window) {
      const obs = new IntersectionObserver((entries) => {
        if (entries.some((e) => e.isIntersecting)) { start(); obs.disconnect(); }
      }, { threshold: 0.2 });
      obs.observe(el);
    } else start();
  }

  const miniEl = document.querySelector("[data-minisim]");
  if (miniEl) runMiniSim(miniEl, MINISIM);

  /* ============================================================
     Docs sidebar highlight
     ============================================================ */
  const sidebarLinks = document.querySelectorAll(".docs-sidebar a[href^='#']");
  const sections = Array.from(sidebarLinks)
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);
  if ("IntersectionObserver" in window && sections.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        sidebarLinks.forEach((a) => {
          a.classList.toggle("active", a.getAttribute("href") === "#" + entry.target.id);
        });
      });
    }, { rootMargin: "-15% 0px -70% 0px" });
    sections.forEach((s) => io.observe(s));
  }

  /* ============================================================
     Lazy-load motion libraries (Lenis + GSAP) after first paint —
     they enhance scrolling/reveals but must never block startup.
     Waits for idle time (or 1.2s), then injects the CDN scripts
     and wires everything up via initMotionLibs().
     ============================================================ */
  function loadMotionLibs() {
    if (!motionOK) return;                 // reduced motion: skip entirely
    const inject = (src) => new Promise((resolve) => {
      const s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = resolve;                 // offline → graceful CSS-only fallback
      document.head.appendChild(s);
    });
    Promise.all([
      inject("https://cdn.jsdelivr.net/npm/lenis@1.1.14/dist/lenis.min.js"),
      // ScrollTrigger must execute after GSAP core → chained
      inject("https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js")
        .then(() => inject("https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js")),
    ]).then(initMotionLibs);
  }
  if ("requestIdleCallback" in window) requestIdleCallback(loadMotionLibs, { timeout: 1200 });
  else setTimeout(loadMotionLibs, 350);
})();
