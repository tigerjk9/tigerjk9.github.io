/* 학습과학 아틀라스 v2: three.js 3D 계보 지도 */
(function () {
  'use strict';
  const params = new URLSearchParams(location.search);
  const EMBED = params.get('embed') === '1';
  if (EMBED) document.body.classList.add('embed');
  const SHOT = params.get('shot') === '1';
  if (SHOT) document.body.classList.add('shot');
  const MOBILE = () => innerWidth < 820;

  const CL = window.ATLAS_CLUSTERS, WORKS = window.ATLAS_WORKS, META = window.ATLAS_META || {}, TOURS = window.ATLAS_TOURS || [];
  const ORDER = ['F', 'I', 'N', 'E', 'R', 'S', 'A', 'C', 'M'];
  const cById = {}; CL.forEach(c => { cById[c.id] = c; c.col = new THREE.Color(c.color); c.ord = ORDER.indexOf(c.id); });
  const byId = {};
  WORKS.forEach(w => { byId[w.id] = w; w.meta = META[w.id] || {}; w.in = []; w.out = []; w.cl = cById[w.c]; });
  const seen = new Set();
  const EDGES = window.ATLAS_EDGES.filter(e => byId[e[0]] && byId[e[1]] && !seen.has(e[0] + '>' + e[1]) && seen.add(e[0] + '>' + e[1]))
    .map(([s, t, type, label]) => ({ s: byId[s], t: byId[t], type, label }));
  EDGES.forEach(e => { e.s.out.push(e); e.t.in.push(e); });

  // ---------- helpers ----------
  function rng(seed) { return function () { seed |= 0; seed = seed + 0x6D2B79F5 | 0; let t = Math.imul(seed ^ seed >>> 15, 1 | seed); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  const rand = rng(20261119);
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  const esc = s => String(s).replace(/[&<>"]/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[m]));
  function surname(au) {
    const first = au.split(/,|&| and /)[0].replace(/\(Eds?\.\)/, '').replace(/et al\.?/, '').replace(/\(.*?\)/g, '').trim();
    const parts = first.split(/\s+/).filter(p => !/^(III|II|Jr\.?|Sr\.?)$/.test(p));
    for (let i = 0; i < parts.length - 1; i++) if (/^(van|von|de|der)$/i.test(parts[i])) return parts.slice(i).join(' ');
    return parts[parts.length - 1];
  }
  WORKS.forEach(w => { w.short = surname(w.au) + ' ' + w.y; w.cited = w.meta.cited || 900; });
  const logC = w => Math.log10(Math.max(w.cited, 100));
  WORKS.forEach(w => { w.r = 0.7 + (logC(w) - 2) * 0.72; });
  function lineage(w) {
    const anc = new Set(), des = new Set();
    (function up(n) { n.in.forEach(e => { if (!anc.has(e.s)) { anc.add(e.s); up(e.s); } }); })(w);
    (function down(n) { n.out.forEach(e => { if (!des.has(e.t)) { des.add(e.t); down(e.t); } }); })(w);
    return { anc, des };
  }
  WORKS.forEach(w => { const L = lineage(w); w.nAnc = L.anc.size; w.nDes = L.des.size; const cs = new Set(); w.in.forEach(e => cs.add(e.s.c)); w.out.forEach(e => cs.add(e.t.c)); cs.delete(w.c); w.bridge = cs.size; });
  const toursOf = {}; TOURS.forEach(t => t.steps.forEach(([id], i) => { (toursOf[id] = toursOf[id] || []).push([t, i]); }));

  // ---------- toast ----------
  const toasts = document.getElementById('toasts');
  function toast(html, ms = 3200, color) {
    const d = document.createElement('div'); d.className = 'toast'; d.innerHTML = html; if (color) d.style.borderLeftColor = color;
    toasts.appendChild(d); while (toasts.children.length > 4) toasts.firstChild.remove();
    setTimeout(() => { d.classList.add('out'); setTimeout(() => d.remove(), 500); }, ms);
  }

  // ---------- WebGL check / text version ----------
  function webglOK() { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } }
  if (params.get('text') === '1' || !webglOK()) { renderTextVersion(); return; }

  // ---------- three setup ----------
  const stage = document.getElementById('stage');
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  const DPR = Math.min(devicePixelRatio, 2);
  renderer.setPixelRatio(DPR);
  renderer.setSize(innerWidth, innerHeight);
  renderer.setClearColor(0x05070d);
  stage.appendChild(renderer.domElement);
  const labelRenderer = new THREE.CSS2DRenderer();
  labelRenderer.setSize(innerWidth, innerHeight);
  labelRenderer.domElement.id = 'labels';
  document.body.appendChild(labelRenderer.domElement);

  const scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x05070d, 0.0024);
  const camera = new THREE.PerspectiveCamera(50, innerWidth / innerHeight, 0.1, 3000);
  camera.position.set(0, 70, 190);
  const controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true; controls.dampingFactor = 0.07;
  controls.minDistance = 18; controls.maxDistance = 560;
  controls.autoRotate = true; controls.autoRotateSpeed = 0.3;
  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  const dl = new THREE.DirectionalLight(0xffffff, 0.9); dl.position.set(60, 120, 80); scene.add(dl);

  // bloom
  let composer = null, bloomOn = !MOBILE() && !!THREE.UnrealBloomPass;
  if (THREE.EffectComposer && THREE.UnrealBloomPass) {
    composer = new THREE.EffectComposer(renderer);
    composer.setPixelRatio(DPR); composer.setSize(innerWidth, innerHeight);
    composer.addPass(new THREE.RenderPass(scene, camera));
    composer.addPass(new THREE.UnrealBloomPass(new THREE.Vector2(innerWidth, innerHeight), 0.62, 0.5, 0.22));
  }
  const fxBtn = document.getElementById('fxBtn');
  function setFx(v) { bloomOn = v && !!composer; fxBtn.classList.toggle('on', bloomOn); }
  fxBtn.onclick = () => setFx(!bloomOn); setFx(bloomOn);

  // starfield
  (function () {
    const n = 2400, pos = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      const r = 380 + rand() * 600, th = rand() * Math.PI * 2, ph = Math.acos(2 * rand() - 1);
      pos[i * 3] = r * Math.sin(ph) * Math.cos(th); pos[i * 3 + 1] = r * Math.cos(ph); pos[i * 3 + 2] = r * Math.sin(ph) * Math.sin(th);
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0x8896b8, size: 1.1, transparent: true, opacity: .5, fog: false })));
  })();
  function glowTex() {
    const c = document.createElement('canvas'); c.width = c.height = 128; const x = c.getContext('2d');
    const g = x.createRadialGradient(64, 64, 0, 64, 64, 64);
    g.addColorStop(0, 'rgba(255,255,255,1)'); g.addColorStop(.18, 'rgba(255,255,255,.55)'); g.addColorStop(.5, 'rgba(255,255,255,.12)'); g.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = g; x.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c);
  }
  const GLOW = glowTex();

  // ---------- nodes ----------
  const sphereGeo = new THREE.SphereGeometry(1, 28, 20), bookGeo = new THREE.OctahedronGeometry(1.25, 0);
  const nodeGroup = new THREE.Group(); scene.add(nodeGroup);
  const pickables = [];
  WORKS.forEach(w => {
    const mat = new THREE.MeshStandardMaterial({ color: w.cl.col, emissive: w.cl.col, emissiveIntensity: .5, roughness: .35, metalness: .1, transparent: true, opacity: 1 });
    const m = new THREE.Mesh(w.type === 'book' ? bookGeo : sphereGeo, mat);
    m.scale.setScalar(w.r); m.userData.w = w;
    const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: w.cl.col, transparent: true, opacity: .5, blending: THREE.AdditiveBlending, depthWrite: false }));
    sp.scale.setScalar(w.r * 5.2);
    const g = new THREE.Group(); g.add(m); g.add(sp);
    const div = document.createElement('div'); div.className = 'nlabel' + (w.cited > 9000 ? ' big' : ''); div.textContent = w.short;
    div.addEventListener('click', ev => { ev.stopPropagation(); select(w, true); });
    div.addEventListener('mouseenter', () => hover(w)); div.addEventListener('mouseleave', () => hover(null));
    const lab = new THREE.CSS2DObject(div); lab.position.set(0, w.r + 0.6, 0); g.add(lab);
    nodeGroup.add(g); pickables.push(m);
    Object.assign(w, { g, lab, mesh: m, sprite: sp, labelDiv: div, pos: new THREE.Vector3(), from: new THREE.Vector3(), to: new THREE.Vector3(), visibleYear: true });
  });

  // ---------- layouts ----------
  const LAYOUT = {};
  (function () {
    const R = 104, centers = {};
    CL.forEach(c => { const a = c.ord / CL.length * Math.PI * 2; centers[c.id] = new THREE.Vector3(Math.cos(a) * R, (c.ord % 2 ? 10 : -10), Math.sin(a) * R); });
    const P = WORKS.map(w => centers[w.c].clone().add(new THREE.Vector3((rand() - .5) * 24, (rand() - .5) * 24, (rand() - .5) * 24)));
    const V = WORKS.map(() => new THREE.Vector3());
    const idx = new Map(WORKS.map((w, i) => [w, i])); const tmp = new THREE.Vector3();
    const IT = 380;
    for (let it = 0; it < IT; it++) {
      const alpha = 1 - it / IT;
      for (let i = 0; i < P.length; i++) for (let j = i + 1; j < P.length; j++) {
        tmp.subVectors(P[i], P[j]); const d2 = tmp.lengthSq() + 0.01; const minD = (WORKS[i].r + WORKS[j].r) * 2.4 + 4;
        const f = (WORKS[i].c === WORKS[j].c ? 75 : 150) / d2 + (d2 < minD * minD ? 0.5 : 0);
        tmp.normalize().multiplyScalar(f * alpha); V[i].add(tmp); V[j].sub(tmp);
      }
      EDGES.forEach(e => {
        const i = idx.get(e.s), j = idx.get(e.t); tmp.subVectors(P[j], P[i]); const d = tmp.length() + .01;
        const same = e.s.c === e.t.c, L = same ? 12 : 55, k = same ? 0.028 : 0.0018;
        tmp.multiplyScalar((d - L) / d * k * alpha); V[i].add(tmp); V[j].sub(tmp);
      });
      WORKS.forEach((w, i) => { tmp.subVectors(centers[w.c], P[i]).multiplyScalar(0.075 * alpha); V[i].add(tmp); P[i].add(V[i]); V[i].multiplyScalar(0.55); });
    }
    LAYOUT.cluster = { pos: P, cam: new THREE.Vector3(0, 135, 235), target: new THREE.Vector3(0, -6, 0) };
  })();
  const Y0 = 1880, Y1 = 2027;
  const tx = y => -130 + 260 * Math.pow((y - Y0) / (Y1 - Y0), 1.45);
  const laneY = c => (4 - cById[c].ord) * 14;
  (function () {
    const P = WORKS.map(w => new THREE.Vector3(tx(w.y), laneY(w.c), 0));
    CL.forEach(c => {
      const ws = WORKS.map((w, i) => i).filter(i => WORKS[i].c === c.id).sort((a, b) => WORKS[a].y - WORKS[b].y);
      let prevX = -1e9, k = 0;
      ws.forEach(i => { if (P[i].x - prevX < 5) { k++; const s = (k % 2 ? 1 : -1) * Math.ceil(k / 2); P[i].z = s * 7; P[i].y += s * 1.7; } else k = 0; prevX = P[i].x; });
    });
    LAYOUT.timeline = { pos: P, cam: new THREE.Vector3(-6, 16, 262), target: new THREE.Vector3(-6, 0, 0) };
  })();
  const rr = y => 10 + 102 * Math.pow((y - Y0) / (Y1 - Y0), 1.35);
  (function () {
    const sector = Math.PI * 2 / CL.length, P = WORKS.map(() => new THREE.Vector3());
    CL.forEach(c => {
      const ws = WORKS.map((w, i) => i).filter(i => WORKS[i].c === c.id).sort((a, b) => WORKS[a].y - WORKS[b].y);
      ws.forEach((i, k) => { const w = WORKS[i]; const a = (c.ord + 0.5) * sector + ((k % 6) / 5 - .5) * sector * 0.7; const r = rr(w.y); P[i].set(Math.cos(a) * r, (logC(w) - 2) * 13 - 10, Math.sin(a) * r); });
    });
    LAYOUT.rings = { pos: P, cam: new THREE.Vector3(0, 195, 225), target: new THREE.Vector3(0, -4, 0) };
  })();

  // ---------- decorations per mode ----------
  const deco = { cluster: new THREE.Group(), timeline: new THREE.Group(), rings: new THREE.Group() };
  Object.values(deco).forEach(g => scene.add(g));
  function css2d(html, cls, pos, group) { const d = document.createElement('div'); d.className = cls; d.innerHTML = html; const o = new THREE.CSS2DObject(d); o.position.copy(pos); group.add(o); return o; }
  CL.forEach(c => {
    const pts = WORKS.map((w, i) => w.c === c.id ? LAYOUT.cluster.pos[i] : null).filter(Boolean);
    const ctr = pts.reduce((a, p) => a.add(p), new THREE.Vector3()).divideScalar(pts.length);
    const top = Math.max(...pts.map(p => p.y));
    const out = new THREE.Vector3(ctr.x, 0, ctr.z).normalize().multiplyScalar(16);
    const o = css2d(esc(c.name), 'clabel', new THREE.Vector3(ctr.x + out.x, top + 8, ctr.z + out.z), deco.cluster); o.element.style.color = c.color;
    o.element.style.pointerEvents = 'auto'; o.element.style.cursor = 'pointer'; o.element.title = c.desc;
    o.element.onclick = () => focusOn(c.id);
    const neb = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: c.col, transparent: true, opacity: .09, blending: THREE.AdditiveBlending, depthWrite: false }));
    neb.position.copy(ctr); neb.scale.setScalar(78); deco.cluster.add(neb);
  });
  (function () {
    const g = deco.timeline, pts = [];
    CL.forEach(c => { const y = laneY(c.id); pts.push(-133, y, 0, 133, y, 0); const o = css2d(esc(c.name), 'clabel lane', new THREE.Vector3(-146, y, 0), g); o.element.style.color = c.color; });
    [1885, 1900, 1925, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020].forEach(y => { const x = tx(y); pts.push(x, -60, 0, x, 64, 0); css2d(String(y), 'tick' + (y % 50 === 0 ? ' major' : ''), new THREE.Vector3(x, -66, 0), g); });
    const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
    g.add(new THREE.LineSegments(geo, new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: .06 })));
  })();
  (function () {
    const g = deco.rings;
    [1900, 1950, 1975, 2000, 2025].forEach(y => {
      const r = rr(y), pts = [];
      for (let i = 0; i <= 128; i++) { const a = i / 128 * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(a) * r, -12, Math.sin(a) * r)); }
      g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: y % 50 === 0 ? .14 : .07 })));
      css2d(String(y), 'tick major', new THREE.Vector3(r, -12, 0), g);
    });
    const sector = Math.PI * 2 / CL.length;
    CL.forEach(c => {
      const a0 = c.ord * sector;
      g.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(Math.cos(a0) * 8, -12, Math.sin(a0) * 8), new THREE.Vector3(Math.cos(a0) * 116, -12, Math.sin(a0) * 116)]), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: .06 })));
      const a = (c.ord + .5) * sector; const o = css2d(esc(c.name), 'clabel', new THREE.Vector3(Math.cos(a) * 128, -12, Math.sin(a) * 128), g); o.element.style.color = c.color;
    });
  })();

  // ---------- edges ----------
  const SEG = 28, MID = SEG / 2;
  const edgeGroup = new THREE.Group(); scene.add(edgeGroup);
  const COLOR_C = new THREE.Color('#ff4d6d'), COLOR_X = new THREE.Color('#9be7ff');
  EDGES.forEach(e => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array((SEG + 1) * 3), 3));
    const col = new Float32Array((SEG + 1) * 3);
    for (let i = 0; i <= SEG; i++) { const c = e.type === 'c' ? COLOR_C : e.type === 'x' ? COLOR_X : e.s.cl.col.clone().lerp(e.t.cl.col, i / SEG); col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b; }
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const mat = e.type === 'b'
      ? new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: .28, blending: THREE.AdditiveBlending, depthWrite: false })
      : new THREE.LineDashedMaterial({ vertexColors: true, transparent: true, opacity: .45, dashSize: e.type === 'c' ? 2.2 : .8, gapSize: e.type === 'c' ? 1.4 : 1.2, blending: THREE.AdditiveBlending, depthWrite: false });
    e.line = new THREE.Line(geo, mat); edgeGroup.add(e.line);
    e.pts = new Float32Array((SEG + 1) * 3); e.base = mat.opacity; e.phase = rand(); e.vis = e.base;
  });
  const PPE = 2, pGeo = new THREE.BufferGeometry();
  const pPos = new Float32Array(EDGES.length * PPE * 3), pCol = new Float32Array(EDGES.length * PPE * 3);
  EDGES.forEach((e, i) => { const c = e.type === 'c' ? COLOR_C : e.type === 'x' ? COLOR_X : e.t.cl.col; for (let k = 0; k < PPE; k++) { const j = (i * PPE + k) * 3; pCol[j] = c.r; pCol[j + 1] = c.g; pCol[j + 2] = c.b; } });
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3)); pGeo.setAttribute('color', new THREE.BufferAttribute(pCol, 3));
  scene.add(new THREE.Points(pGeo, new THREE.PointsMaterial({ size: 2.3, map: GLOW, vertexColors: true, transparent: true, opacity: .95, blending: THREE.AdditiveBlending, depthWrite: false })));

  const vM = new THREE.Vector3(), vC = new THREE.Vector3();
  function ctrlPoint(a, b, out) {
    const d = a.distanceTo(b); out.addVectors(a, b).multiplyScalar(.5);
    if (mode === 'timeline') { if (Math.abs(a.y - b.y) < 3) out.y += 4 + d * .16; else out.z += d * .18; }
    else if (mode === 'rings') out.y += 6 + d * .22;
    else { out.y += d * .16; out.add(vM.copy(out).setY(0).multiplyScalar(-.08)); }
    return out;
  }
  function updateEdges() {
    EDGES.forEach(e => {
      const a = e.s.pos, b = e.t.pos; ctrlPoint(a, b, vC);
      const arr = e.line.geometry.attributes.position.array;
      for (let i = 0; i <= SEG; i++) {
        const t = i / SEG, u = 1 - t;
        arr[i * 3] = u * u * a.x + 2 * u * t * vC.x + t * t * b.x;
        arr[i * 3 + 1] = u * u * a.y + 2 * u * t * vC.y + t * t * b.y;
        arr[i * 3 + 2] = u * u * a.z + 2 * u * t * vC.z + t * t * b.z;
      }
      e.pts.set(arr); e.line.geometry.attributes.position.needsUpdate = true; e.line.geometry.computeBoundingSphere();
      if (e.type !== 'b') e.line.computeLineDistances();
      if (e.rl) e.rl.position.set(arr[MID * 3], arr[MID * 3 + 1], arr[MID * 3 + 2]);
    });
    if (tour) buildTourPath();
  }

  // ---------- relation labels (selected node's edges) ----------
  const relGroup = new THREE.Group(); scene.add(relGroup);
  function clearRelLabels() { EDGES.forEach(e => { if (e.rl) { relGroup.remove(e.rl); e.rl.element.remove(); e.rl = null; } }); }
  function makeRelLabels(w) {
    clearRelLabels();
    [...w.in, ...w.out].forEach(e => {
      if (!e.label) return;
      const d = document.createElement('div'); d.className = 'rlabel t-' + e.type; d.textContent = e.label;
      const o = new THREE.CSS2DObject(d); o.position.set(e.pts[MID * 3], e.pts[MID * 3 + 1], e.pts[MID * 3 + 2]);
      relGroup.add(o); e.rl = o;
    });
  }

  // ---------- mode ----------
  let mode = 'cluster', tween = null, camFly = null;
  const camFrom = new THREE.Vector3(), camTo = new THREE.Vector3(), tgtFrom = new THREE.Vector3(), tgtTo = new THREE.Vector3();
  function setDecoVisible() { Object.entries(deco).forEach(([k, g]) => { g.visible = k === mode; g.traverse(o => { if (o.isCSS2DObject) o.visible = k === mode; }); }); }
  function setMode(m, instant, keepCam) {
    mode = m;
    document.querySelectorAll('#modes button').forEach(b => b.classList.toggle('on', b.dataset.mode === m));
    setDecoVisible();
    const L = LAYOUT[m];
    WORKS.forEach((w, i) => { w.from.copy(w.pos); w.to.copy(L.pos[i]); });
    camFrom.copy(camera.position); tgtFrom.copy(controls.target); camTo.copy(L.cam); tgtTo.copy(L.target);
    controls.autoRotate = m !== 'timeline' && !selected && !tour;
    if (instant) { WORKS.forEach(w => { w.pos.copy(w.to); w.g.position.copy(w.pos); }); if (!keepCam) { camera.position.copy(camTo); controls.target.copy(tgtTo); } updateEdges(); tween = null; return; }
    tween = { t0: performance.now(), dur: 1600, cam: !selected && !tour && !keepCam };
  }
  document.querySelectorAll('#modes button').forEach(b => b.onclick = () => setMode(b.dataset.mode));

  // ---------- highlight ----------
  let selected = null, hovered = null, focusCluster = null, filter = null, tour = null;
  function applyHighlight() {
    let nodeOn = null, edgeOn = null, core = new Set();
    if (tour) {
      const ids = tour.t.steps.map(s => byId[s[0]]); nodeOn = new Set(ids); core.add(ids[tour.i]);
      edgeOn = new Set(EDGES.filter(e => nodeOn.has(e.s) && nodeOn.has(e.t)));
    } else if (selected) {
      const { anc, des } = lineage(selected); nodeOn = new Set([selected, ...anc, ...des]); core.add(selected);
      edgeOn = new Set(EDGES.filter(e => ((anc.has(e.s) || e.s === selected) && (anc.has(e.t) || e.t === selected)) || ((des.has(e.t) || e.t === selected) && (des.has(e.s) || e.s === selected))));
    } else if (filter) {
      nodeOn = new Set(filter.set); filter.set.forEach(w => core.add(w));
      edgeOn = new Set(EDGES.filter(e => nodeOn.has(e.s) && nodeOn.has(e.t)));
    } else if (focusCluster) {
      nodeOn = new Set(WORKS.filter(w => w.c === focusCluster)); nodeOn.forEach(w => core.add(w));
      edgeOn = new Set(EDGES.filter(e => e.s.c === focusCluster || e.t.c === focusCluster));
      edgeOn.forEach(e => { nodeOn.add(e.s); nodeOn.add(e.t); });
    }
    const hoverSet = hovered ? new Set([hovered, ...hovered.in.map(e => e.s), ...hovered.out.map(e => e.t)]) : null;
    WORKS.forEach(w => {
      const on = !nodeOn || nodeOn.has(w), isCore = core.has(w) || w === hovered;
      w.on = on;
      w.mesh.material.opacity = on ? 1 : .1; w.mesh.material.emissiveIntensity = isCore ? .85 : .45;
      w.sprite.material.opacity = on ? (isCore ? .8 : .42) : .04;
      w.labelDiv.classList.toggle('dim', !on && !(hoverSet && hoverSet.has(w)));
      w.labelDiv.classList.toggle('hl', isCore || (hoverSet && hoverSet.has(w)) || (!!(selected || tour) && on));
    });
    EDGES.forEach(e => {
      let o = e.base;
      if (edgeOn) o = edgeOn.has(e) ? Math.min(1, e.base * 2.6) : .02;
      if (hovered && (e.s === hovered || e.t === hovered)) o = 1;
      e.line.material.opacity = o; e.vis = o;
    });
    declutterSoon = true;
  }

  // ---------- label declutter ----------
  let declutterSoon = true, frameN = 0;
  const _v = new THREE.Vector3();
  function declutter() {
    const W2 = innerWidth, H2 = innerHeight, items = [];
    WORKS.forEach(w => {
      w.labelDiv.classList.remove('cull');
      if (!w.visibleYear) return;
      _v.copy(w.pos); _v.y += w.r + .6; _v.project(camera);
      if (_v.z > 1 || _v.x < -1.1 || _v.x > 1.1 || _v.y < -1.1 || _v.y > 1.1) return;
      let pr = logC(w);
      if (w === selected || w === hovered || (tour && tour.cur === w)) pr += 100;
      else if (w.labelDiv.classList.contains('hl')) pr += 40;
      else if (w.labelDiv.classList.contains('dim')) pr -= 40;
      const big = w.labelDiv.classList.contains('hl') ? 7.6 : 6.6;
      items.push({ w, x: (_v.x + 1) / 2 * W2, y: (1 - _v.y) / 2 * H2 - 14, hw: w.short.length * big / 2 + 3, hh: 8, pr });
    });
    items.sort((a, b) => b.pr - a.pr);
    const placed = [];
    for (const it of items) {
      let hit = false;
      for (const p of placed) if (Math.abs(it.x - p.x) < it.hw + p.hw && Math.abs(it.y - p.y) < it.hh + p.hh) { hit = true; break; }
      if (hit && it.pr < 100) it.w.labelDiv.classList.add('cull'); else placed.push(it);
    }
  }

  // ---------- panel ----------
  const panel = document.getElementById('panel'), pbody = document.getElementById('pbody');
  function relHtml(list, dir) {
    if (!list.length) return '<p class="none">이 지도 안에는 없음</p>';
    return '<div class="rel">' + list.slice().sort((a, b) => (dir === 'in' ? a.s.y - b.s.y : a.t.y - b.t.y)).map(e => {
      const o = dir === 'in' ? e.s : e.t;
      const tag = e.type === 'c' ? '<span class="t-c">비판</span>' : e.type === 'x' ? '<span class="t-x">다리</span>' : '';
      return `<a data-id="${o.id}" style="--c:${o.cl.color}">${tag}<span>${esc(o.ko)}<br><em>${esc(e.label || '')}</em></span><small>${esc(o.short)}</small></a>`;
    }).join('') + '</div>';
  }
  function showPanel(w) {
    const m = w.meta, links = [];
    if (m.doi) links.push(`<a href="https://doi.org/${esc(m.doi)}" target="_blank" rel="noopener">DOI 원문</a>`);
    if (m.free) links.push(`<a href="${esc(m.free)}" target="_blank" rel="noopener">무료 전문</a>`);
    if (!m.free && w.type === 'book') links.push(`<a href="https://openlibrary.org/search?q=${encodeURIComponent(w.t)}" target="_blank" rel="noopener">Open Library에서 찾기</a>`);
    if (m.pdf && location.protocol === 'file:') links.push(`<a href="${esc(m.pdf)}" target="_blank">내 PC의 원문</a>`);
    links.push(`<a href="https://scholar.google.com/scholar?q=${encodeURIComponent(w.t + ' ' + surname(w.au))}" target="_blank" rel="noopener">Google Scholar</a>`);
    links.push(`<a href="#" id="shareBtn">링크 복사</a>`);
    const typeKo = { paper: '논문', book: '단행본', chapter: '단행본 장' }[w.type] || '논문';
    const tl = (toursOf[w.id] || []).map(([t, i]) => `<a class="tchip" data-tour="${t.id}" data-step="${i}" style="--c:${t.color}">▶ ${esc(t.title)} <small>${i + 1}/${t.steps.length}</small></a>`).join('');
    pbody.innerHTML = `
      <span class="chip" style="--c:${w.cl.color}">● ${esc(w.cl.full)}</span><span class="meta">${w.y} · ${typeKo}${m.cited ? ' · 인용 ' + m.cited.toLocaleString() + '회' : ''}</span>
      <h2>${esc(w.ko)}</h2><p class="orig">${esc(w.t)}</p><p class="au">${esc(w.au)}</p>
      <div class="kws">${(w.kw || []).map(k => `<button data-kw="${esc(k)}">#${esc(k)}</button>`).join('')}</div>
      <div class="sec"><h3>의의</h3><p>${esc(w.sig)}</p></div>
      <div class="sec"><h3>핵심 요약</h3><p>${esc(w.sum)}</p></div>
      <div class="sec easy"><h3>쉽게 말하면</h3><p>${esc(w.easy)}</p></div>
      <div class="sec"><h3>교실에서는</h3><p>${esc(w.cls)}</p></div>
      ${w.note ? `<div class="sec note"><h3>함께 알아 둘 점</h3><p>${esc(w.note)}</p></div>` : ''}
      <div class="sec"><h3>계보</h3><p class="lineage">이 지도에서 조상 연구 <b>${w.nAnc}</b>편, 후손 연구 <b>${w.nDes}</b>편과 이어져 있고, 다른 클러스터 <b>${w.bridge}</b>곳과 직접 연결됩니다.</p></div>
      ${tl ? `<div class="sec"><h3>이 연구가 나오는 투어</h3><div class="tchips">${tl}</div></div>` : ''}
      ${glossOf(w)}
      <div class="sec"><h3>다른 연구까지 이어진 길</h3><div class="pathf inl"><input list="wlist" id="pTo" placeholder="도착 연구 이름이나 저자"><button class="btn" id="pToGo">경로 보기</button></div></div>
      <div class="sec"><h3>영향을 준 연구 (선행)</h3>${relHtml(w.in, 'in')}</div>
      <div class="sec"><h3>영향을 받은 연구 (후속)</h3>${relHtml(w.out, 'out')}</div>
      <div class="links">${links.join('')}</div>`;
    pbody.querySelectorAll('.rel a').forEach(a => a.onclick = () => select(byId[a.dataset.id], true));
    pbody.querySelectorAll('.kws button').forEach(b => b.onclick = () => setFilter(b.dataset.kw));
    pbody.querySelectorAll('.tchip').forEach(a => a.onclick = () => startTour(TOURS.find(t => t.id === a.dataset.tour), +a.dataset.step));
    pbody.querySelectorAll('.gchip').forEach(a => a.onclick = () => openGloss(a.dataset.term));
    const pTo = document.getElementById('pTo'); const goPath = () => { const b = resolveWork(pTo.value); if (!b) { toast('목록에서 연구를 골라 주세요'); return; } startPath(w, b); };
    document.getElementById('pToGo').onclick = goPath; pTo.addEventListener('keydown', e => { if (e.key === 'Enter') goPath(); });
    const sb = document.getElementById('shareBtn');
    sb.onclick = ev => { ev.preventDefault(); const u = location.origin + location.pathname + '#' + w.id; (navigator.clipboard ? navigator.clipboard.writeText(u) : Promise.reject()).then(() => toast('이 연구로 바로 오는 링크를 복사했습니다'), () => prompt('링크', u)); };
    pbody.scrollTop = 0; panel.classList.add('open');
  }
  function flyTo(w, dist) {
    const dir = camera.position.clone().sub(controls.target).normalize();
    camFrom.copy(camera.position); tgtFrom.copy(controls.target);
    tgtTo.copy(w.pos); camTo.copy(w.pos).add(dir.multiplyScalar(dist || (MOBILE() ? 95 : 78)));
    if (MOBILE()) { tgtTo.y -= 16; camTo.y -= 16; }
    else if (tour) { tgtTo.y -= 12; camTo.y -= 12; }
    else if (panel.classList.contains('open')) { const right = new THREE.Vector3().crossVectors(dir, camera.up).normalize(); tgtTo.add(right.clone().multiplyScalar(14)); camTo.add(right.multiplyScalar(14)); }
    camFly = { t0: performance.now(), dur: 1100 };
  }
  function select(w, fly) {
    if (tour && w) endTour(true);
    selected = w; focusCluster = null; filter = null; updateLegend(); renderFilterPill();
    if (!w) { panel.classList.remove('open'); clearRelLabels(); applyHighlight(); controls.autoRotate = mode !== 'timeline'; history.replaceState(null, '', location.pathname + location.search); return; }
    controls.autoRotate = false; showPanel(w); makeRelLabels(w); applyHighlight();
    history.replaceState(null, '', location.pathname + location.search + '#' + w.id);
    if (fly) flyTo(w);
  }
  document.getElementById('closePanel').onclick = () => { if (tour) panel.classList.remove('open'); else select(null); };

  // ---------- filter (keyword/search) ----------
  const pill = document.getElementById('filterPill');
  function setFilterSet(q, set) {
    if (tour) endTour(true);
    selected = null; focusCluster = null; panel.classList.remove('open'); clearRelLabels(); updateLegend();
    filter = set.length ? { q, set } : null; renderFilterPill(); applyHighlight(); hint.style.opacity = 0;
  }
  function setFilter(q) {
    const s = q.toLowerCase();
    const set = WORKS.filter(w => [w.ko, w.t, w.au, (w.kw || []).join(' '), w.sig, w.sum].join(' ').toLowerCase().includes(s));
    if (tour) endTour(true);
    selected = null; focusCluster = null; panel.classList.remove('open'); clearRelLabels(); updateLegend();
    filter = set.length ? { q, set } : null; renderFilterPill(); applyHighlight(); hint.style.opacity = 0;
    if (!set.length) toast(`"${esc(q)}"에 해당하는 연구가 없습니다`);
  }
  function renderFilterPill() {
    if (!filter) { pill.style.display = 'none'; return; }
    pill.innerHTML = `<b>"${esc(filter.q)}"</b> 관련 연구 ${filter.set.length}편 강조 중 <button aria-label="해제">×</button>`; pill.style.display = 'flex';
    pill.querySelector('button').onclick = () => { filter = null; renderFilterPill(); applyHighlight(); };
  }

  // ---------- legend ----------
  const lgList = document.getElementById('lgList');
  lgList.innerHTML = CL.slice().sort((a, b) => a.ord - b.ord).map(c => `<div class="lg" data-c="${c.id}" title="${esc(c.desc)}"><i style="background:${c.color};color:${c.color}"></i><b>${esc(c.name)}</b><em>${WORKS.filter(w => w.c === c.id).length}</em></div>`).join('');
  lgList.querySelectorAll('.lg').forEach(el => el.onclick = () => focusOn(el.dataset.c));
  function focusOn(c) {
    if (tour) endTour(true);
    selected = null; filter = null; panel.classList.remove('open'); clearRelLabels(); renderFilterPill();
    focusCluster = focusCluster === c ? null : c; updateLegend(); applyHighlight();
    if (focusCluster) { const cl = cById[c]; toast(`<b style="color:${cl.color}">${esc(cl.full)}</b><br>${esc(cl.desc)}`, 5200, cl.color); }
  }
  function updateLegend() { lgList.querySelectorAll('.lg').forEach(el => el.classList.toggle('on', el.dataset.c === focusCluster)); }

  // ---------- drawer: list + ranking ----------
  const drawer = document.getElementById('drawer'), dBody = document.getElementById('dBody');
  function renderList() {
    dBody.innerHTML = '<p class="dnote">클러스터별 연구 목록 (연도순)</p>' + CL.slice().sort((a, b) => a.ord - b.ord).map(c =>
      `<h3><i style="background:${c.color}"></i>${esc(c.full)}</h3><p class="dnote">${esc(c.desc)}</p>` +
      WORKS.filter(w => w.c === c.id).sort((a, b) => a.y - b.y).map(w => `<a data-id="${w.id}"><small>${w.y}</small> ${esc(w.ko)} <small>${esc(surname(w.au))}${w.type === 'book' ? ' · 책' : ''}</small></a>`).join('')).join('');
    bindDrawer();
  }
  function rankBlock(title, desc, arr, fmt) {
    return `<h3>${title}</h3><p class="dnote">${desc}</p>` + arr.slice(0, 12).map((w, i) => `<a data-id="${w.id}"><span class="rk">${i + 1}</span><i class="dot" style="background:${w.cl.color}"></i>${esc(w.ko)} <small>${esc(w.short)} · ${fmt(w)}</small></a>`).join('');
  }
  function renderRank() {
    dBody.innerHTML =
      rankBlock('가장 많이 인용된 연구', 'OpenAlex 인용 수 기준', WORKS.slice().sort((a, b) => b.cited - a.cited), w => w.cited.toLocaleString() + '회') +
      rankBlock('가장 긴 후손 계보', '이 지도 안에서 직간접적으로 영향을 받은 후속 연구 수', WORKS.slice().sort((a, b) => b.nDes - a.nDes || b.cited - a.cited), w => '후손 ' + w.nDes + '편') +
      rankBlock('분야를 잇는 다리', '직접 연결된 다른 클러스터 수', WORKS.slice().sort((a, b) => b.bridge - a.bridge || (b.in.length + b.out.length) - (a.in.length + a.out.length)), w => w.bridge + '개 분야') +
      rankBlock('가장 넓은 뿌리', '이 지도 안에서 거슬러 올라가는 조상 연구 수', WORKS.slice().sort((a, b) => b.nAnc - a.nAnc), w => '조상 ' + w.nAnc + '편');
    bindDrawer();
  }
  function bindDrawer() { dBody.querySelectorAll('a[data-id]').forEach(a => a.onclick = () => { select(byId[a.dataset.id], true); if (MOBILE()) drawer.classList.remove('open'); }); }
  const GLOSS = window.ATLAS_GLOSSARY || [];
  function renderGloss() {
    const n = GLOSS.reduce((a, g) => a + g.items.length, 0);
    dBody.innerHTML = `<p class="dnote">핵심 개념 ${n}개. 개념 이름을 누르면 관련 연구가 지도에서 빛납니다.</p>` + GLOSS.map((g, gi) => `<h3>${esc(g.g)}</h3>` + g.items.map((it, ii) => `<div class="gl"><button class="gt" data-g="${gi}" data-i="${ii}">${esc(it.t)}</button> <small>${esc(it.en)}</small><p>${esc(it.d)}</p><div class="glw">${it.w.filter(id => byId[id]).map(id => `<a data-id="${id}" style="--c:${byId[id].cl.color}">${esc(byId[id].short)}</a>`).join('')}</div></div>`).join('')).join('');
    dBody.querySelectorAll('.gt').forEach(b => b.onclick = () => { const it = GLOSS[+b.dataset.g].items[+b.dataset.i]; setFilterSet(it.t, it.w.map(id => byId[id]).filter(Boolean)); toast(`<b>${esc(it.t)}</b> <small>${esc(it.en)}</small><br>${esc(it.d)}`, 6500); if (MOBILE()) drawer.classList.remove('open'); });
    bindDrawer();
  }
  function openGloss(term) {
    drawer.classList.add('open'); document.querySelectorAll('#dTabs button').forEach(x => x.classList.toggle('on', x.dataset.tab === 'gloss')); renderGloss();
    if (term) { const b = [...dBody.querySelectorAll('.gt')].find(x => x.textContent === term); if (b) { b.scrollIntoView({ block: 'center' }); b.click(); b.closest('.gl').classList.add('flash'); } }
  }
  document.querySelectorAll('#dTabs button').forEach(b => b.onclick = () => { document.querySelectorAll('#dTabs button').forEach(x => x.classList.toggle('on', x === b)); (b.dataset.tab === 'rank' ? renderRank : b.dataset.tab === 'gloss' ? renderGloss : renderList)(); dBody.scrollTop = 0; });
  renderList();
  document.getElementById('listBtn').onclick = () => { tourMenu.classList.remove('open'); drawer.classList.toggle('open'); };
  document.getElementById('labelBtn').onclick = () => { document.body.classList.toggle('hide-labels'); document.getElementById('labelBtn').classList.toggle('on', !document.body.classList.contains('hide-labels')); };
  document.getElementById('labelBtn').classList.add('on');
  const legendEl = document.getElementById('legend');
  document.getElementById('legendBtn').onclick = () => legendEl.classList.toggle('open');
  const modal = document.getElementById('modal');
  document.getElementById('aboutBtn').onclick = () => modal.classList.add('open');
  document.getElementById('closeModal').onclick = () => modal.classList.remove('open');
  modal.onclick = e => { if (e.target === modal) modal.classList.remove('open'); };

  // ---------- search ----------
  const sIn = document.getElementById('search'), sRes = document.getElementById('results');
  sIn.addEventListener('input', () => {
    const q = sIn.value.trim().toLowerCase();
    if (!q) { sRes.style.display = 'none'; return; }
    const hits = WORKS.filter(w => [w.ko, w.t, w.au, (w.kw || []).join(' '), String(w.y), w.cl.full].join(' ').toLowerCase().includes(q));
    const deep = WORKS.filter(w => [w.ko, w.t, w.au, (w.kw || []).join(' '), w.sig, w.sum].join(' ').toLowerCase().includes(q));
    const gh = GLOSS.flatMap(g => g.items).filter(it => (it.t + ' ' + it.en).toLowerCase().includes(q)).slice(0, 3);
    sRes.innerHTML = gh.map(it => `<div data-gloss="${esc(it.t)}" class="all">📖 개념 사전: <b>${esc(it.t)}</b> <small>${esc(it.en)}</small></div>`).join('') + (deep.length > 1 ? `<div data-filter="1" class="all">✦ "${esc(sIn.value.trim())}" 관련 연구 ${deep.length}편 모두 지도에서 강조</div>` : '') +
      (hits.length ? hits.slice(0, 12).map(w => `<div data-id="${w.id}"><b style="color:${w.cl.color}">●</b> ${esc(w.ko)}<br><small>${esc(w.short)} · ${esc(w.cl.name)}</small></div>`).join('') : '<div><small>제목·저자·키워드 일치 없음</small></div>');
    sRes.style.display = 'block';
    sRes.querySelectorAll('[data-id]').forEach(d => d.onclick = () => { select(byId[d.dataset.id], true); sRes.style.display = 'none'; sIn.blur(); });
    const fa = sRes.querySelector('[data-filter]'); if (fa) fa.onclick = () => { setFilter(sIn.value.trim()); sRes.style.display = 'none'; sIn.blur(); };
    sRes.querySelectorAll('[data-gloss]').forEach(d => d.onclick = () => { sRes.style.display = 'none'; sIn.blur(); openGloss(d.dataset.gloss); });
  });
  sIn.addEventListener('keydown', e => { if (e.key === 'Enter') { const f = sRes.querySelector('[data-id]') || sRes.querySelector('[data-filter]'); if (f) f.click(); } if (e.key === 'Escape') sRes.style.display = 'none'; });
  document.addEventListener('click', e => { if (!e.target.closest('#searchWrap')) sRes.style.display = 'none'; if (!e.target.closest('#tourMenu') && !e.target.closest('#tourBtn')) tourMenu.classList.remove('open'); });

  // ---------- tours ----------
  const tourMenu = document.getElementById('tourMenu'), tourCard = document.getElementById('tourCard');
  tourMenu.innerHTML = '<div class="pathf"><b>두 연구는 어떻게 이어질까?</b><input list="wlist" id="pA" placeholder="출발 연구 (예: Miller 1956)"><input list="wlist" id="pB" placeholder="도착 연구 (예: Bastani 2025)"><button class="btn primary" id="pGo" style="--c:#ffd166">경로 따라가기</button></div><p class="dnote">계보를 따라 이야기처럼 읽는 투어입니다. ← → 키로도 넘길 수 있습니다.</p>' + TOURS.map(t => `<a data-tour="${t.id}" style="--c:${t.color}"><b>${esc(t.title)}</b><span>${esc(t.intro)}</span><small>${t.steps.length}단계</small></a>`).join('');
  tourMenu.querySelectorAll('a').forEach(a => a.onclick = () => { tourMenu.classList.remove('open'); startTour(TOURS.find(t => t.id === a.dataset.tour), 0); });
  document.getElementById('tourBtn').onclick = ev => { ev.stopPropagation(); drawer.classList.remove('open'); tourMenu.classList.toggle('open'); };
  document.getElementById('pGo').onclick = () => { const a = resolveWork(document.getElementById('pA').value), b = resolveWork(document.getElementById('pB').value); if (!a || !b) { toast('출발 연구와 도착 연구를 목록에서 골라 주세요'); return; } tourMenu.classList.remove('open'); startPath(a, b); };
  // ---------- path finder ----------
  document.getElementById('wlist').innerHTML = WORKS.slice().sort((a, b) => a.y - b.y).map(w => `<option value="${esc(w.short + ' · ' + w.ko)}">`).join('');
  function resolveWork(v) {
    v = (v || '').trim(); if (!v) return null;
    const ex = WORKS.find(w => (w.short + ' · ' + w.ko) === v); if (ex) return ex;
    const s = v.toLowerCase(); return WORKS.find(w => w.short.toLowerCase() === s) || WORKS.find(w => (w.short + ' ' + w.ko + ' ' + w.t).toLowerCase().includes(s)) || null;
  }
  const ADJ = new Map(WORKS.map(w => [w, []])); EDGES.forEach(e => { ADJ.get(e.s).push([e.t, e]); ADJ.get(e.t).push([e.s, e]); });
  function findPath(a, b) {
    const prev = new Map([[a, null]]), q = [a];
    while (q.length) { const n = q.shift(); if (n === b) break; for (const [m, e] of ADJ.get(n)) if (!prev.has(m)) { prev.set(m, [n, e]); q.push(m); } }
    if (!prev.has(b)) return null; const path = []; let cur = b;
    while (cur) { const p = prev.get(cur); path.unshift([cur, p ? p[1] : null]); cur = p ? p[0] : null; }
    return path;
  }
  const firstSentence = s => (s.match(/^.*?다\./) || [s])[0];
  function startPath(a, b) {
    if (a === b) { toast('같은 연구입니다'); return; }
    const p = findPath(a, b); if (!p) { toast('이 지도 안에서는 두 연구가 이어지지 않습니다'); return; }
    const steps = p.map(([w, e], i) => {
      if (i === 0) return [w.id, `출발점. ${firstSentence(w.sig)}`];
      const pv = p[i - 1][0], fwd = e.s === pv, tag = e.type === 'c' ? ' (비판)' : e.type === 'x' ? ' (분야 간 다리)' : '';
      return [w.id, (fwd ? `${pv.short} → 이 연구. ${e.label}${tag}. ` : `이 연구 → ${pv.short}. ${e.label}${tag}. 계보를 거슬러 오르는 연결이다. `) + firstSentence(w.sig)];
    });
    startTour({ id: 'path', title: `${a.short} → ${b.short}, ${p.length - 1}단계로 이어진 길`, color: '#ffd166', steps, mode: mode === 'rings' ? 'cluster' : mode }, 0);
  }
  function glossOf(w) {
    const terms = GLOSS.flatMap(g => g.items).filter(it => it.w.includes(w.id));
    return terms.length ? `<div class="sec"><h3>관련 개념</h3><div class="kws">${terms.map(it => `<button class="gchip" data-term="${esc(it.t)}">📖 ${esc(it.t)}</button>`).join('')}</div></div>` : '';
  }
  let tourLine = null;
  function buildTourPath() {
    if (tourLine) { scene.remove(tourLine); tourLine.geometry.dispose(); }
    if (!tour) return;
    const pts = tour.t.steps.map(s => byId[s[0]].pos.clone());
    const curve = new THREE.CatmullRomCurve3(pts, false, 'centripetal');
    const geo = new THREE.TubeGeometry(curve, pts.length * 24, 0.32, 6, false);
    tourLine = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: new THREE.Color(tour.t.color), transparent: true, opacity: .55, blending: THREE.AdditiveBlending, depthWrite: false }));
    scene.add(tourLine);
  }
  function startTour(t, i) {
    if (!t) return;
    selected = null; filter = null; focusCluster = null; clearRelLabels(); updateLegend(); renderFilterPill(); panel.classList.remove('open');
    tour = { t, i: i || 0 }; controls.autoRotate = false;
    document.body.classList.add('touring');
    if (t.mode && t.mode !== mode) setMode(t.mode, false, true);
    buildTourPath(); showTourStep();
    if (TOURS.includes(t)) history.replaceState(null, '', location.pathname + '?tour=' + t.id + (EMBED ? '&embed=1' : ''));
  }
  function showTourStep() {
    const t = tour.t, [id, text] = t.steps[tour.i], w = byId[id]; tour.cur = w;
    tourCard.style.setProperty('--c', t.color);
    tourCard.innerHTML = `<div class="th"><span>${esc(t.title)}</span><small>${tour.i + 1} / ${t.steps.length}</small><button class="tx" aria-label="투어 종료">×</button></div>
      <div class="tprog">${t.steps.map((s, k) => `<i class="${k === tour.i ? 'on' : k < tour.i ? 'done' : ''}" data-k="${k}"></i>`).join('')}</div>
      <h4><b style="color:${w.cl.color}">●</b> ${esc(w.ko)} <small>${esc(w.short)}</small></h4>
      <p>${esc(text)}</p>
      <div class="tb"><button class="btn" id="tPrev" ${tour.i === 0 ? 'disabled' : ''}>◀ 이전</button><button class="btn" id="tMore">자세히</button><button class="btn primary" id="tNext">${tour.i === t.steps.length - 1 ? '투어 마치기' : '다음 ▶'}</button></div>`;
    tourCard.classList.add('open');
    tourCard.querySelector('.tx').onclick = () => endTour();
    tourCard.querySelector('#tPrev').onclick = () => stepTour(-1);
    tourCard.querySelector('#tNext').onclick = () => stepTour(1);
    tourCard.querySelector('#tMore').onclick = () => { showPanel(w); makeRelLabels(w); };
    tourCard.querySelectorAll('.tprog i').forEach(el => el.onclick = () => { tour.i = +el.dataset.k; showTourStep(); });
    if (panel.classList.contains('open')) { showPanel(w); makeRelLabels(w); } else clearRelLabels();
    applyHighlight();
    const go = () => flyTo(w, MOBILE() ? 105 : 88);
    if (tween) setTimeout(go, Math.max(0, tween.dur - (performance.now() - tween.t0)) + 50); else go();
  }
  function stepTour(d) { if (!tour) return; const n = tour.i + d; if (n >= tour.t.steps.length) { endTour(); toast('투어를 마쳤습니다. 다른 투어도 둘러보세요'); return; } if (n < 0) return; tour.i = n; showTourStep(); }
  function endTour(silent) {
    tour = null; tourCard.classList.remove('open'); document.body.classList.remove('touring'); buildTourPath(); clearRelLabels();
    if (!silent) { panel.classList.remove('open'); applyHighlight(); history.replaceState(null, '', location.pathname + (EMBED ? '?embed=1' : '')); }
  }

  // ---------- year / playback ----------
  const yr = document.getElementById('year'), yrNow = document.getElementById('yearNow'), yrBig = document.getElementById('yearBig'), playBtn = document.getElementById('play');
  let yearCut = 2026, playing = null;
  function setYear(y, announce) {
    const prev = yearCut; yearCut = y; yr.value = y; yrNow.textContent = y; yrBig.textContent = y < 2026 ? y : '';
    WORKS.forEach(w => { w.visibleYear = w.y <= y; w.g.visible = w.visibleYear; w.lab.visible = w.visibleYear; });
    EDGES.forEach(e => e.line.visible = e.s.visibleYear && e.t.visibleYear);
    if (announce) WORKS.filter(w => w.y > prev && w.y <= y).sort((a, b) => b.cited - a.cited).slice(0, 2).forEach(w => toast(`<small>${w.y}</small> <b>${esc(w.ko)}</b><br><small>${esc(w.au.split(/,|&/)[0])} · ${esc(w.cl.name)}</small>`, 3000, w.cl.color));
    declutterSoon = true;
  }
  yr.addEventListener('input', () => { stopPlay(); setYear(+yr.value); });
  function stopPlay() { playing = null; playBtn.textContent = '▶'; }
  playBtn.onclick = () => { if (playing) { stopPlay(); return; } if (tour) endTour(true); setYear(yearCut >= 2026 ? 1880 : yearCut); playing = { t0: performance.now(), from: yearCut }; playBtn.textContent = '❚❚'; };

  // ---------- picking ----------
  const ray = new THREE.Raycaster(), mouse = new THREE.Vector2(), tip = document.getElementById('tip');
  let downAt = null;
  function pick(ev) {
    mouse.x = ev.clientX / innerWidth * 2 - 1; mouse.y = -(ev.clientY / innerHeight) * 2 + 1;
    ray.setFromCamera(mouse, camera);
    const hit = ray.intersectObjects(pickables.filter(m => m.parent.visible), false)[0];
    return hit ? hit.object.userData.w : null;
  }
  function hover(w) { if (hovered === w) return; hovered = w; applyHighlight(); renderer.domElement.style.cursor = w ? 'pointer' : 'grab'; if (!w) tip.style.display = 'none'; }
  renderer.domElement.addEventListener('pointermove', ev => {
    if (ev.pointerType === 'touch') return;
    const w = pick(ev); hover(w);
    if (w) { tip.innerHTML = `<b>${esc(w.ko)}</b><span>${esc(w.short)} · ${esc(w.cl.name)}${w.meta.cited ? ' · 인용 ' + w.meta.cited.toLocaleString() : ''}</span>`; tip.style.display = 'block'; tip.style.left = Math.min(ev.clientX + 14, innerWidth - 290) + 'px'; tip.style.top = (ev.clientY + 14) + 'px'; }
  });
  const hint = document.getElementById('hint');
  renderer.domElement.addEventListener('pointerdown', ev => { downAt = [ev.clientX, ev.clientY]; controls.autoRotate = false; hint.style.opacity = 0; });
  renderer.domElement.addEventListener('pointerup', ev => {
    if (!downAt) return; const moved = Math.hypot(ev.clientX - downAt[0], ev.clientY - downAt[1]); downAt = null;
    if (moved > 6) return;
    const w = pick(ev);
    if (w) select(w, true);
    else if (!tour && (selected || focusCluster || filter)) { focusCluster = null; filter = null; updateLegend(); renderFilterPill(); select(null); }
  });
  setTimeout(() => hint.style.opacity = 0, 8000);
  addEventListener('keydown', e => {
    if (e.target.tagName === 'INPUT') return;
    if (tour && (e.key === 'ArrowRight' || e.key === ' ')) { e.preventDefault(); stepTour(1); }
    else if (tour && e.key === 'ArrowLeft') stepTour(-1);
    else if (e.key === 'Escape') { if (tour) endTour(); else select(null); drawer.classList.remove('open'); modal.classList.remove('open'); tourMenu.classList.remove('open'); }
  });

  // ---------- stats ----------
  const yMin = Math.min(...WORKS.map(w => w.y)), yMax = Math.max(...WORKS.map(w => w.y));
  document.getElementById('stats').textContent = `연구 ${WORKS.length}편 · 영향 관계 ${EDGES.length}개 · 투어 ${TOURS.length}개 · 개념 ${GLOSS.reduce((a, g) => a + g.items.length, 0)}개 · ${yMin}–${yMax}`;
  if (/github\.io$/.test(location.hostname) && !EMBED) {
    const a = document.createElement('a'); a.href = '/post/learning-science-atlas/'; a.className = 'backlink'; a.textContent = '← 닷커넥터 블로그 글 보기';
    document.getElementById('brand').appendChild(a);
  }

  // ---------- loop ----------
  addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight; camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight); labelRenderer.setSize(innerWidth, innerHeight);
    if (composer) composer.setSize(innerWidth, innerHeight);
    document.getElementById('legendBtn').style.display = MOBILE() ? '' : 'none';
    declutterSoon = true;
  });
  dispatchEvent(new Event('resize'));
  let lastCam = new THREE.Vector3();
  function frame(now) {
    if (tween) {
      const t = Math.min(1, (now - tween.t0) / tween.dur), k = ease(t);
      WORKS.forEach(w => { w.pos.lerpVectors(w.from, w.to, k); w.g.position.copy(w.pos); });
      if (tween.cam) { camera.position.lerpVectors(camFrom, camTo, k); controls.target.lerpVectors(tgtFrom, tgtTo, k); }
      updateEdges(); if (t >= 1) { tween = null; if (selected) flyTo(selected); }
    }
    if (camFly) { const t = Math.min(1, (now - camFly.t0) / camFly.dur), k = ease(t); camera.position.lerpVectors(camFrom, camTo, k); controls.target.lerpVectors(tgtFrom, tgtTo, k); if (t >= 1) camFly = null; }
    if (playing) { const y = Math.min(2026, Math.round(playing.from + (now - playing.t0) / 1000 * 6)); if (y !== yearCut) setYear(y, true); if (y >= 2026) stopPlay(); }
    const T = now / 1000;
    EDGES.forEach((e, i) => {
      for (let k = 0; k < PPE; k++) {
        const j = (i * PPE + k) * 3;
        if (!e.line.visible || e.vis < .05) { pPos[j] = pPos[j + 1] = pPos[j + 2] = 1e5; continue; }
        const f = ((T * 0.22 + e.phase + k / PPE) % 1) * SEG, a = Math.floor(f), r = f - a, b = Math.min(SEG, a + 1);
        pPos[j] = e.pts[a * 3] + (e.pts[b * 3] - e.pts[a * 3]) * r; pPos[j + 1] = e.pts[a * 3 + 1] + (e.pts[b * 3 + 1] - e.pts[a * 3 + 1]) * r; pPos[j + 2] = e.pts[a * 3 + 2] + (e.pts[b * 3 + 2] - e.pts[a * 3 + 2]) * r;
      }
    });
    pGeo.attributes.position.needsUpdate = true;
    const pulse = selected || (tour && tour.cur);
    if (pulse) pulse.sprite.scale.setScalar(pulse.r * (5.2 + Math.sin(T * 3) * .9));
    controls.update();
    if (++frameN % 6 === 0 && (declutterSoon || lastCam.distanceToSquared(camera.position) > .01 || tween || camFly)) { declutter(); declutterSoon = false; lastCam.copy(camera.position); }
    if (bloomOn) composer.render(); else renderer.render(scene, camera);
    labelRenderer.render(scene, camera);
    requestAnimationFrame(frame);
  }

  // ---------- quiz (인출 연습 + 분산 재출제) ----------
  const quizEl = document.getElementById('quiz');
  const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  let QZ = null;
  function makeQ(w, avoidKind) {
    const kinds = ['easy', 'cls', 'cluster', 'easy', 'cls'].filter(k => k !== avoidKind);
    const kind = kinds[Math.floor(Math.random() * kinds.length)];
    if (kind === 'cluster') {
      const opts = shuffle([w.cl, ...shuffle(CL.filter(c => c !== w.cl)).slice(0, 3)]);
      return { w, kind, prompt: '이 연구는 어느 클러스터에 속할까요?', body: `「${w.ko}」 ${w.short}`, opts: opts.map(c => ({ label: c.full, color: c.color, ok: c === w.cl })) };
    }
    const pool = WORKS.filter(x => x !== w), same = shuffle(pool.filter(x => x.c === w.c)).slice(0, 2), other = shuffle(pool.filter(x => x.c !== w.c)).slice(0, 3 - same.length);
    const opts = shuffle([w, ...same, ...other]);
    return { w, kind, prompt: kind === 'easy' ? '이 비유는 어떤 연구를 설명할까요?' : '이 교실 적용은 어떤 연구에서 나왔을까요?', body: kind === 'easy' ? w.easy : w.cls, opts: opts.map(x => ({ label: x.ko, sub: x.short, color: x.cl.color, ok: x === w })) };
  }
  function startQuiz(n = 10) {
    if (tour) endTour(true); select(null);
    const ws = shuffle(WORKS.slice()).slice(0, n);
    QZ = { q: ws.map(w => makeQ(w)), i: 0, right: 0, done: 0, missed: new Set(), base: n };
    quizEl.classList.add('open'); showQ();
  }
  function showQ() {
    const q = QZ.q[QZ.i];
    if (!q) return endQuiz();
    quizEl.innerHTML = `<div class="qbox"><div class="qh"><span>인출 연습 퀴즈</span><small>${QZ.i + 1} / ${QZ.q.length} · 정답 ${QZ.right}</small><button class="qx" aria-label="닫기">×</button></div>
      <div class="qprog"><i style="width:${QZ.i / QZ.q.length * 100}%"></i></div>
      <h4>${esc(q.prompt)}</h4><blockquote>${esc(q.body)}</blockquote>
      <div class="qopts">${q.opts.map((o, k) => `<button class="qopt" data-k="${k}" style="--c:${o.color}"><b>${esc(o.label)}</b>${o.sub ? `<small>${esc(o.sub)}</small>` : ''}</button>`).join('')}</div><div class="qexp"></div></div>`;
    quizEl.querySelector('.qx').onclick = () => quizEl.classList.remove('open');
    quizEl.querySelectorAll('.qopt').forEach(b => b.onclick = () => answer(+b.dataset.k));
  }
  function answer(k) {
    const q = QZ.q[QZ.i], ok = q.opts[k].ok; QZ.done++;
    quizEl.querySelectorAll('.qopt').forEach((b, j) => { b.disabled = true; if (q.opts[j].ok) b.classList.add('right'); else if (j === k) b.classList.add('wrong'); });
    if (ok) QZ.right++; else { QZ.missed.add(q.w); QZ.q.splice(Math.min(QZ.q.length, QZ.i + 4), 0, makeQ(q.w, q.kind)); }
    const w = q.w;
    quizEl.querySelector('.qexp').innerHTML = `<p class="${ok ? 'ok' : 'no'}">${ok ? '정답입니다.' : '아쉽습니다. 이 연구는 몇 문제 뒤에 다시 나옵니다.'}</p><p><b style="color:${w.cl.color}">● ${esc(w.ko)}</b> <small>${esc(w.short)} · ${esc(w.cl.name)}</small><br>${esc(w.sig)}</p><div class="tb"><button class="btn" id="qSee">지도에서 보기</button><button class="btn primary" id="qNext" style="--c:#ffd166">다음 ▶</button></div>`;
    document.getElementById('qNext').onclick = () => { QZ.i++; showQ(); };
    document.getElementById('qSee').onclick = () => { quizEl.classList.remove('open'); select(w, true); };
  }
  function endQuiz() {
    const pct = Math.round(QZ.right / Math.max(1, QZ.done) * 100);
    quizEl.innerHTML = `<div class="qbox"><div class="qh"><span>퀴즈 결과</span><button class="qx" aria-label="닫기">×</button></div><h4>${QZ.done}문제 중 ${QZ.right}문제 정답 (${pct}%)</h4>
      <p class="dnote">틀린 연구는 문제 몇 개 뒤에 다시 내는 방식(인출 연습과 분산 효과)으로 복습했습니다. 내일 한 번 더 풀면 훨씬 오래 남습니다.</p>
      ${QZ.missed.size ? `<h5>다시 볼 연구</h5><div class="rel">${[...QZ.missed].map(w => `<a data-id="${w.id}" style="--c:${w.cl.color}"><span>${esc(w.ko)}</span><small>${esc(w.short)}</small></a>`).join('')}</div>` : '<p>모두 맞혔습니다!</p>'}
      <div class="tb"><button class="btn primary" id="qAgain" style="--c:#ffd166">새 퀴즈</button></div></div>`;
    quizEl.querySelector('.qx').onclick = () => quizEl.classList.remove('open');
    document.getElementById('qAgain').onclick = () => startQuiz();
    quizEl.querySelectorAll('.rel a').forEach(a => a.onclick = () => { quizEl.classList.remove('open'); select(byId[a.dataset.id], true); });
  }
  document.getElementById('quizBtn').onclick = () => startQuiz();

  // ---------- first-visit intro ----------
  const introEl = document.getElementById('intro');
  function showIntro() {
    introEl.innerHTML = `<div class="ibox"><h2>학습과학 <span>아틀라스</span></h2>
      <p>1885년 에빙하우스의 망각곡선부터 2025년 AI 튜터 실험까지, 학습과학 연구 ${WORKS.length}편과 그 사이의 영향 관계 ${EDGES.length}개를 별자리처럼 그렸습니다. 별 하나가 연구 한 편이고, 선 위를 흐르는 빛이 영향의 방향입니다.</p>
      <div class="ichoices">
        <button data-a="tour"><b>▶ 투어로 시작</b><span>작업기억에서 인지부하이론까지, 8단계 이야기</span></button>
        <button data-a="free"><b>자유롭게 탐색</b><span>별을 누르면 요약과 계보가 열립니다</span></button>
        <button data-a="gloss"><b>개념 사전</b><span>작업기억, 비계, 어포던스… 핵심 개념 ${GLOSS.reduce((a, g) => a + g.items.length, 0)}개</span></button>
        <button data-a="quiz"><b>퀴즈로 복습</b><span>비유를 보고 연구 맞히기</span></button>
      </div><p class="dnote">드래그로 회전 · 스크롤로 확대 · 언제든 위쪽 버튼으로 돌아올 수 있습니다.</p></div>`;
    introEl.classList.add('open');
    introEl.querySelectorAll('[data-a]').forEach(b => b.onclick = () => {
      introEl.classList.remove('open'); try { localStorage.setItem('lsa_intro_v3', '1'); } catch (e) { }
      const a = b.dataset.a; if (a === 'tour') startTour(TOURS[0], 0); else if (a === 'gloss') openGloss(); else if (a === 'quiz') startQuiz();
    });
    introEl.onclick = e => { if (e.target === introEl) { introEl.classList.remove('open'); try { localStorage.setItem('lsa_intro_v3', '1'); } catch (er) { } } };
  }

  // ---------- init ----------
  const initMode = params.get('mode');
  setMode(LAYOUT[initMode] ? initMode : 'cluster', true);
  applyHighlight();
  requestAnimationFrame(frame);
  const initId = location.hash.slice(1), initTour = params.get('tour'), initCl = params.get('cluster');
  setTimeout(() => {
    if (initTour && TOURS.find(t => t.id === initTour)) startTour(TOURS.find(t => t.id === initTour), 0);
    else if (byId[initId]) select(byId[initId], true);
    else if (initCl && cById[initCl]) focusOn(initCl);
    else if (params.get('quiz') === '1') startQuiz();
    else if (params.get('path') && params.get('path').split(',').every(id => byId[id])) { const [pa, pb] = params.get('path').split(','); startPath(byId[pa], byId[pb]); }
    else if (!SHOT) { let seenIntro = false; try { seenIntro = !!localStorage.getItem('lsa_intro_v3'); } catch (e) { } if (!seenIntro) showIntro(); }
  }, 350);
  function renderTextVersion() {
    document.body.classList.add('nogl');
    const G = window.ATLAS_GLOSSARY || [], el = document.getElementById('nogl');
    const ord = CL.slice().sort((a, b) => 'FICMSREN A'.indexOf(a.id) - 'FICMSREN A'.indexOf(b.id));
    const can3d = webglOK();
    el.innerHTML = `<header><h1>학습과학 <span>아틀라스</span> <small>텍스트 버전</small></h1>
      <p>${can3d ? `<a href="${location.pathname}">3D 지도로 보기</a> · ` : '이 브라우저에서는 3D 지도(WebGL)를 쓸 수 없어 텍스트로 보여 드립니다. · '}연구 ${WORKS.length}편 · 영향 관계 ${EDGES.length}개 · 투어 ${TOURS.length}개</p>
      <nav>${ord.map(c => `<a href="#c-${c.id}" style="color:${c.color}">${esc(c.name)}</a>`).join('')}<a href="#tours">투어</a><a href="#gloss">개념 사전</a></nav></header>` +
      ord.map(c => `<section id="c-${c.id}"><h2 style="color:${c.color}">${esc(c.full)}</h2><p class="cd">${esc(c.desc)}</p>` + WORKS.filter(w => w.c === c.id).sort((a, b) => a.y - b.y).map(w => `<details id="${w.id}"><summary><b>${w.y}</b> ${esc(w.ko)} <small>${esc(w.au)}</small></summary>
        <p class="orig">${esc(w.t)}${w.meta.cited ? ` · 인용 ${w.meta.cited.toLocaleString()}회` : ''}</p>
        <p><b>의의</b> ${esc(w.sig)}</p><p><b>핵심 요약</b> ${esc(w.sum)}</p><p><b>쉽게 말하면</b> ${esc(w.easy)}</p><p><b>교실에서는</b> ${esc(w.cls)}</p>${w.note ? `<p><b>함께 알아 둘 점</b> ${esc(w.note)}</p>` : ''}
        ${w.in.length ? `<p><b>영향을 준 연구</b> ${w.in.map(e => `<a href="#${e.s.id}">${esc(e.s.short)}</a>(${esc(e.label)})`).join(', ')}</p>` : ''}
        ${w.out.length ? `<p><b>영향을 받은 연구</b> ${w.out.map(e => `<a href="#${e.t.id}">${esc(e.t.short)}</a>(${esc(e.label)})`).join(', ')}</p>` : ''}
        <p>${w.meta.doi ? `<a href="https://doi.org/${esc(w.meta.doi)}" target="_blank" rel="noopener">DOI</a> ` : ''}${w.meta.free ? `<a href="${esc(w.meta.free)}" target="_blank" rel="noopener">무료 전문</a>` : ''}</p></details>`).join('') + '</section>').join('') +
      `<section id="tours"><h2>투어</h2>${TOURS.map(t => `<details><summary><b style="color:${t.color}">${esc(t.title)}</b> <small>${esc(t.intro)}</small></summary><ol>${t.steps.map(([id, tx]) => `<li><a href="#${id}">${esc(byId[id].ko)}</a> <small>${esc(byId[id].short)}</small><br>${esc(tx)}</li>`).join('')}</ol></details>`).join('')}</section>` +
      `<section id="gloss"><h2>개념 사전</h2>${G.map(g => `<h3>${esc(g.g)}</h3><dl>${g.items.map(it => `<dt>${esc(it.t)} <small>${esc(it.en)}</small></dt><dd>${esc(it.d)} ${it.w.filter(id => byId[id]).map(id => `<a href="#${id}">${esc(byId[id].short)}</a>`).join(', ')}</dd>`).join('')}</dl>`).join('')}</section>`;
    el.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', () => { const d = document.getElementById(a.getAttribute('href').slice(1)); if (d && d.tagName === 'DETAILS') d.open = true; }));
    const h = location.hash.slice(1); if (h && document.getElementById(h)) { const d = document.getElementById(h); if (d.tagName === 'DETAILS') d.open = true; d.scrollIntoView(); }
  }
  window.ATLAS = { showIntro, startQuiz, openGloss, startPath: (a, b) => startPath(byId[a], byId[b]), select: id => select(byId[id], true), setMode, setYear, startTour: (id, i) => startTour(TOURS.find(t => t.id === id), i || 0), endTour, setFilter, focusOn, setFx, works: WORKS, edges: EDGES };
})();
