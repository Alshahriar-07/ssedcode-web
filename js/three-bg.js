/* ============================================================
   Seed Code CLI — three-bg.js
   WebGL background: particle field + network lines, depth fog,
   mouse-parallax camera with breathing zoom, scroll drift.
   Desktop only. Sets window.__SC_THREE on success so main.js
   skips its 2D canvas fallback. Silently no-ops when Three.js
   fails to load (offline), WebGL is unavailable, motion is
   reduced, or the viewport is small.
   ============================================================ */

(function () {
  "use strict";

  const motionOK = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!motionOK || window.innerWidth < 900 || typeof window.THREE === "undefined") return;

  const canvas = document.querySelector(".bg-three");
  if (!canvas) return;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false, powerPreference: "low-power" });
  } catch (e) { return; }

  window.__SC_THREE = true;

  const DPR = Math.min(window.devicePixelRatio || 1, 1.75);
  renderer.setPixelRatio(DPR);

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x09090b, 0.016);

  const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 200);
  camera.position.set(0, 0, 42);

  const group = new THREE.Group();
  scene.add(group);

  /* ---------- Particle field ---------- */
  const COUNT = 700;
  const positions = new Float32Array(COUNT * 3);
  const colors = new Float32Array(COUNT * 3);
  const green = new THREE.Color(0x22c55e);
  const white = new THREE.Color(0xfafafa);

  for (let i = 0; i < COUNT; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 130;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 75;
    positions[i * 3 + 2] = (Math.random() - 0.55) * 60;
    const c = Math.random() < 0.3 ? green : white;
    colors[i * 3] = c.r; colors[i * 3 + 1] = c.g; colors[i * 3 + 2] = c.b;
  }

  const pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute("position", new THREE.BufferAttribute(positions, 3));
  pGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));

  const pMat = new THREE.PointsMaterial({
    size: 0.16, vertexColors: true, transparent: true, opacity: 0.7,
    depthWrite: false, sizeAttenuation: true,
  });
  group.add(new THREE.Points(pGeo, pMat));

  /* ---------- Network lines between near pairs ---------- */
  const linePos = [];
  const MAX_LINKS = 150;
  let links = 0;
  for (let i = 0; i < COUNT && links < MAX_LINKS; i += 2) {
    for (let j = i + 1; j < Math.min(i + 26, COUNT); j++) {
      const dx = positions[i * 3] - positions[j * 3];
      const dy = positions[i * 3 + 1] - positions[j * 3 + 1];
      const dz = positions[i * 3 + 2] - positions[j * 3 + 2];
      if (dx * dx + dy * dy + dz * dz < 42) {
        linePos.push(
          positions[i * 3], positions[i * 3 + 1], positions[i * 3 + 2],
          positions[j * 3], positions[j * 3 + 1], positions[j * 3 + 2]
        );
        links++;
        break;
      }
    }
  }
  const lGeo = new THREE.BufferGeometry();
  lGeo.setAttribute("position", new THREE.BufferAttribute(new Float32Array(linePos), 3));
  const lMat = new THREE.LineBasicMaterial({ color: 0x22c55e, transparent: true, opacity: 0.09, depthWrite: false });
  group.add(new THREE.LineSegments(lGeo, lMat));

  /* ---------- Camera: mouse parallax + breathing + scroll ---------- */
  let mx = 0, my = 0, cx = 0, cy = 0;
  window.addEventListener("pointermove", (e) => {
    mx = (e.clientX / window.innerWidth - 0.5) * 2;
    my = (e.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  const resize = () => {
    const w = window.innerWidth, h = window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
  };
  resize();
  window.addEventListener("resize", resize, { passive: true });

  let raf = 0;
  const clock = new THREE.Clock();

  const tick = () => {
    const t = clock.getElapsedTime();

    cx += (mx - cx) * 0.04;
    cy += (my - cy) * 0.04;

    camera.position.x = cx * 4.2;
    camera.position.y = -cy * 2.6;
    camera.position.z = 42 + Math.sin(t * 0.28) * 2.2;      // slow breathing zoom
    camera.lookAt(0, 0, 0);

    group.rotation.y = t * 0.022;
    group.rotation.x = Math.sin(t * 0.12) * 0.04;
    group.position.y = window.scrollY * 0.004;               // scroll drift

    renderer.render(scene, camera);
    raf = requestAnimationFrame(tick);
  };
  raf = requestAnimationFrame(tick);

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) { cancelAnimationFrame(raf); raf = 0; }
    else if (!raf) raf = requestAnimationFrame(tick);
  });
})();
