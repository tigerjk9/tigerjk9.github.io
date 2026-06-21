---
layout: wide
title: "지식 그래프"
permalink: /knowledge-graph/
class: "page--knowledge-graph"
---

<style>
  html, body.page--knowledge-graph {
    background: #0f0f13 !important;
    overflow: hidden;
    margin: 0; padding: 0;
  }
  .page--knowledge-graph .page__inner-wrap,
  .page--knowledge-graph #main {
    margin: 0 !important;
    padding: 0 !important;
    max-width: none !important;
  }
  .page__footer, .page--knowledge-graph .page__title { display: none; }

  /* ── Container ── */
  #kg-container {
    display: flex;
    flex-direction: column;
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    background: #0f0f13;
    font-family: -apple-system, 'Inter', 'Segoe UI', sans-serif;
    color: #c4c4d4;
    position: fixed;
    top: 0; left: 0;
  }

  /* ── Top bar ── */
  #kg-topbar {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 16px;
    background: rgba(15,15,22,0.97);
    border-bottom: 1px solid rgba(139,92,246,0.18);
    z-index: 20;
    flex-shrink: 0;
    flex-wrap: wrap;
  }
  #kg-search {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 6px;
    color: #e2e2f0;
    font-size: 13px;
    padding: 6px 12px;
    width: 200px;
    outline: none;
    transition: border-color 0.2s;
  }
  #kg-search::placeholder { color: #6a6a85; }
  #kg-search:focus { border-color: rgba(139,92,246,0.7); box-shadow: 0 0 0 2px rgba(139,92,246,0.2); }

  #kg-filters {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
    flex: 1;
  }
  .kg-filter-btn {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 5px;
    color: #b9b9d0;
    font-size: 12px;
    padding: 4px 10px;
    cursor: pointer;
    transition: all 0.18s;
    white-space: nowrap;
  }
  .kg-filter-btn:hover { background: rgba(139,92,246,0.12); color: #e2e2f0; }
  .kg-filter-btn:focus-visible { outline: 2px solid #a78bfa; outline-offset: 1px; }
  .kg-filter-btn.active {
    background: rgba(139,92,246,0.18) !important;
    border-color: rgba(139,92,246,0.6) !important;
    color: #f0f0ff !important;
  }
  .kg-filter-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 5px;
    vertical-align: middle;
  }
  #kg-stat {
    font-size: 11px;
    color: #7a7a98;
    margin-left: auto;
    white-space: nowrap;
  }

  /* ── Main area ── */
  #kg-main {
    display: flex;
    flex: 1;
    overflow: hidden;
    position: relative;
  }
  #kg-graph-wrap {
    flex: 1;
    position: relative;
    overflow: hidden;
  }
  #kg-svg {
    width: 100%;
    height: 100%;
    display: block;
  }

  /* ── Loader ── */
  .kg-loader {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    z-index: 50;
  }
  .kg-loader-ring {
    width: 40px; height: 40px;
    border: 3px solid rgba(139,92,246,0.15);
    border-top-color: #a78bfa;
    border-radius: 50%;
    animation: kg-spin 0.9s linear infinite;
    margin: 0 auto 12px;
  }
  .kg-loader p { color: #6a6a85; font-size: 12px; margin: 0; }
  @keyframes kg-spin { to { transform: rotate(360deg); } }

  /* ── Info panel ── */
  #kg-panel {
    width: 312px;
    flex-shrink: 0;
    background: rgba(15,15,22,0.98);
    border-left: 1px solid rgba(139,92,246,0.2);
    display: none;
    flex-direction: column;
    gap: 12px;
    padding: 18px 16px;
    overflow-y: auto;
    z-index: 10;
  }
  #kg-panel-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 8px;
  }
  #kg-panel-title {
    font-size: 15px;
    font-weight: 600;
    color: #f0f0ff;
    line-height: 1.45;
    flex: 1;
    margin: 0;
  }
  #kg-panel-close {
    background: none;
    border: none;
    color: #7a7a98;
    font-size: 22px;
    cursor: pointer;
    padding: 0 4px;
    line-height: 1;
    flex-shrink: 0;
  }
  #kg-panel-close:hover { color: #a78bfa; }
  #kg-panel-close:focus-visible { outline: 2px solid #a78bfa; border-radius: 4px; }
  #kg-panel-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  #kg-panel-cat {
    display: inline-block;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 3px;
    border: 1px solid;
    font-weight: 500;
  }
  #kg-panel-date { font-size: 11px; color: #6a6a85; }
  #kg-panel-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
  }
  .kg-tag {
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 3px;
    border: 1px solid;
    color: #b9b9d0;
    border-color: rgba(139,92,246,0.3);
    background: rgba(139,92,246,0.06);
  }
  #kg-panel-excerpt {
    font-size: 13px;
    color: #9a9ab8;
    line-height: 1.65;
    margin: 0;
    border-top: 1px solid rgba(139,92,246,0.12);
    padding-top: 10px;
  }
  .kg-related-title {
    font-size: 11px;
    font-weight: 600;
    color: #a78bfa;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
    border-top: 1px solid rgba(139,92,246,0.12);
    padding-top: 10px;
  }
  .kg-related-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 6px 6px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    color: #9a9ab8;
    transition: all 0.15s;
    line-height: 1.4;
  }
  .kg-related-item:hover { background: rgba(139,92,246,0.1); color: #f0f0ff; }
  .kg-related-item:focus-visible { outline: 2px solid #a78bfa; }
  .kg-related-badge {
    font-size: 10px;
    background: rgba(139,92,246,0.2);
    color: #c4b5fd;
    border-radius: 3px;
    padding: 1px 5px;
    flex-shrink: 0;
    margin-top: 1px;
    white-space: nowrap;
  }
  .kg-related-shared {
    display: block;
    font-size: 10px;
    color: #6a6a85;
    margin-top: 2px;
  }
  #kg-panel-link {
    display: inline-block;
    margin-top: 4px;
    padding: 8px 14px;
    background: rgba(139,92,246,0.14);
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 5px;
    color: #c4b5fd;
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.18s;
    align-self: flex-start;
  }
  #kg-panel-link:hover { background: rgba(139,92,246,0.24); border-color: rgba(139,92,246,0.7); }
  #kg-panel-link:focus-visible { outline: 2px solid #a78bfa; outline-offset: 2px; }

  /* ── Tooltip ── */
  #kg-tooltip {
    position: fixed;
    background: rgba(15,15,22,0.97);
    border: 1px solid rgba(139,92,246,0.35);
    border-radius: 5px;
    color: #f0f0ff;
    font-size: 12px;
    padding: 5px 10px;
    pointer-events: none;
    display: none;
    z-index: 200;
    max-width: 260px;
    line-height: 1.4;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
  }

  /* ── Hub node labels (always-on for high-degree) ── */
  .kg-hub-label {
    pointer-events: none;
    fill: #d8d8ec;
    font-size: 10px;
    paint-order: stroke;
    stroke: #0f0f13;
    stroke-width: 3px;
    stroke-linejoin: round;
  }

  /* ── Nav buttons ── */
  #kg-nav {
    position: absolute;
    bottom: 16px;
    left: 16px;
    display: flex;
    gap: 6px;
    z-index: 30;
  }
  .kg-nav-btn {
    background: rgba(15,15,22,0.92);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 6px;
    color: #c4b5fd;
    font-size: 12px;
    padding: 6px 12px;
    cursor: pointer;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    backdrop-filter: blur(10px);
    transition: all 0.18s;
    font-family: inherit;
  }
  .kg-nav-btn:hover { background: rgba(139,92,246,0.15); border-color: rgba(139,92,246,0.5); }
  .kg-nav-btn:focus-visible { outline: 2px solid #a78bfa; outline-offset: 1px; }

  #kg-reset {
    position: absolute;
    bottom: 16px;
    right: 16px;
    z-index: 30;
  }

  /* ── Community label chips (노드 위에서도 또렷하게) ── */
  .kg-comm-label { cursor: pointer; }
  .kg-comm-label text { paint-order: stroke; }
  .kg-comm-label:hover rect { fill-opacity: 0.96; }

  /* ── Hint ── */
  #kg-hint {
    position: absolute;
    top: 12px; left: 50%;
    transform: translateX(-50%);
    font-size: 11px;
    color: #6a6a85;
    background: rgba(15,15,22,0.6);
    padding: 4px 12px;
    border-radius: 12px;
    z-index: 25;
    pointer-events: none;
    transition: opacity 0.4s;
  }

  /* ── Mobile ── */
  @media (max-width: 680px) {
    #kg-panel {
      position: absolute;
      bottom: 0; left: 0; right: 0;
      width: 100%;
      max-height: 58vh;
      border-left: none;
      border-top: 1px solid rgba(139,92,246,0.25);
      box-shadow: 0 -8px 24px rgba(0,0,0,0.5);
    }
    #kg-search { width: 130px; }
    #kg-stat { display: none; }
    #kg-panel-close { font-size: 28px; padding: 0 8px; }
    .kg-related-item { padding: 9px 6px; }
  }

  /* ── Reduced motion ── */
  @media (prefers-reduced-motion: reduce) {
    .kg-loader-ring { animation: none; }
    .kg-nav-btn, .kg-filter-btn, #kg-panel-link { transition: none; }
  }
</style>

<script src="https://unpkg.com/d3@7.9.0/dist/d3.min.js"></script>

<div id="kg-container">

  <div id="kg-topbar">
    <input id="kg-search" type="text" placeholder="포스트 또는 태그 검색..." aria-label="포스트 또는 태그 검색">
    <div id="kg-filters" role="group" aria-label="주제 필터">
      <button class="kg-filter-btn active" data-cat="all">전체</button>
    </div>
    <span id="kg-stat" aria-live="polite"></span>
  </div>

  <div id="kg-main">
    <div id="kg-graph-wrap">
      <div class="kg-loader" id="kg-spinner">
        <div class="kg-loader-ring"></div>
        <p>그래프 로딩 중...</p>
      </div>
      <svg id="kg-svg" role="application" aria-label="포스트 지식 그래프. 노드는 글, 연결선은 공유 태그 기반 관계."></svg>
      <div id="kg-hint">노드를 클릭해 연관 글을 탐색하세요</div>
      <div id="kg-nav">
        <a href="/" class="kg-nav-btn">&#127968; 홈</a>
        <button class="kg-nav-btn" onclick="history.back()">&#8592; 이전</button>
      </div>
      <div id="kg-reset">
        <button class="kg-nav-btn" id="kg-reset-btn" title="전체 보기 (R)" aria-label="전체 보기로 초기화">&#8635; 전체</button>
      </div>
    </div>

    <div id="kg-panel" role="dialog" aria-label="포스트 정보">
      <div id="kg-panel-header">
        <h3 id="kg-panel-title"></h3>
        <button id="kg-panel-close" title="닫기 (Esc)" aria-label="패널 닫기">&#215;</button>
      </div>
      <div id="kg-panel-meta">
        <span id="kg-panel-cat"></span>
        <span id="kg-panel-date"></span>
      </div>
      <div id="kg-panel-tags"></div>
      <p id="kg-panel-excerpt"></p>
      <div id="kg-panel-related"></div>
      <a id="kg-panel-link" href="#" target="_blank" rel="noopener">읽기 &#8594;</a>
    </div>
  </div>

</div>

<div id="kg-tooltip"></div>

<script>
(function () {
  'use strict';

  // ─────────────────────────────────────────────────────────────
  // CONFIG — 색·임계값·물리 상수 한곳에 모음 (유지보수성)
  // ─────────────────────────────────────────────────────────────
  const CONFIG = {
    TOP_K: 8,            // 노드당 유지할 최대 연결 수 (가지치기)
    MIN_COMMUNITY: 5,    // 이 미만 크기 군집은 '기타'로 묶음
    NODE_R_MIN: 4,       // 최소 노드 반경
    NODE_R_MAX: 17,      // 허브 노드 최대 반경
    HUB_LABELS: 14,      // 라벨을 상시 표시할 상위 degree 노드 수
    LABEL_TAGS: 2,       // 군집 자동 라벨에 쓸 대표 태그 수
    FADE_OP: 0.07,       // 비강조 노드 투명도
    FOCUS_SCALE: 1.9,    // 검색/필터 포커스 줌 배율
    OTHER: '기타',
    // 군집(커뮤니티) 색 — 사람이 정한 카테고리가 아니라 연결 구조에서 탐지한 군집에 부여
    PALETTE: ['#8b5cf6','#06b6d4','#10b981','#f97316','#ec4899','#f59e0b',
              '#3b82f6','#ef4444','#84cc16','#a855f7','#14b8a6','#eab308',
              '#fb923c','#60a5fa','#e879f9','#f43f5e'],
    OTHER_COLOR: '#6b6b8a'
  };

  const REDUCED = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const dur = (ms) => REDUCED ? 0 : ms;

  const wrap    = document.getElementById('kg-graph-wrap');
  const svgEl   = document.getElementById('kg-svg');
  const spinner = document.getElementById('kg-spinner');
  const panel   = document.getElementById('kg-panel');
  const tooltip = document.getElementById('kg-tooltip');
  const hint    = document.getElementById('kg-hint');

  let W = wrap.clientWidth;
  let H = wrap.clientHeight;

  const svg = d3.select(svgEl).attr('width', W).attr('height', H);
  const g   = svg.append('g').attr('id', 'kg-root');

  const zoom = d3.zoom()
    .scaleExtent([0.12, 6])
    .on('zoom', (e) => g.attr('transform', e.transform));
  svg.call(zoom).on('dblclick.zoom', null);

  const gLinks     = g.append('g').attr('id', 'links');
  const gNodes     = g.append('g').attr('id', 'nodes');
  const gHubLabels = g.append('g').attr('id', 'hub-labels');
  const gLabels    = g.append('g').attr('id', 'cluster-labels');

  fetch('/knowledge-graph.json')
    .then((r) => r.json())
    .then((data) => init(data))
    .catch((err) => {
      console.error('Graph load error:', err);
      spinner.innerHTML = '<p>그래프를 불러오지 못했습니다.</p>';
    });

  // ─────────────────────────────────────────────────────────────
  // Edge construction (client-side): 태그 IDF 가중 + 노드당 top-K
  //   - 흔한 태그(AI 등)는 IDF가 낮아 약한 연결, 희귀 태그 공유는 강한 연결
  //   - 빌드 시 O(N^2) Liquid 루프를 제거하고 여기서 한 번만 계산
  // ─────────────────────────────────────────────────────────────
  function buildEdges(nodes) {
    const N = nodes.length;
    const df = new Map();
    nodes.forEach((n) => {
      new Set(n.tags || []).forEach((t) => df.set(t, (df.get(t) || 0) + 1));
    });
    const idf = new Map();
    df.forEach((c, t) => idf.set(t, Math.log(N / c)));

    const tag2idx = new Map();
    const cat2idx = new Map();
    nodes.forEach((n, i) => {
      new Set(n.tags || []).forEach((t) => {
        if (!tag2idx.has(t)) tag2idx.set(t, []);
        tag2idx.get(t).push(i);
      });
      if (!cat2idx.has(n.group)) cat2idx.set(n.group, []);
      cat2idx.get(n.group).push(i);
    });

    const kept = new Map(); // "a-b" -> weight
    for (let a = 0; a < N; a++) {
      const cand = new Map();
      new Set(nodes[a].tags || []).forEach((t) => {
        const w = idf.get(t);
        tag2idx.get(t).forEach((b) => {
          if (b !== a) cand.set(b, (cand.get(b) || 0) + w);
        });
      });
      if (cand.size === 0) {
        // 카테고리 fallback — 공유 태그가 없는 글의 고립 방지
        (cat2idx.get(nodes[a].group) || [])
          .filter((b) => b !== a).slice(0, 2)
          .forEach((b) => cand.set(b, 0.01));
      }
      [...cand.entries()].sort((x, y) => y[1] - x[1]).slice(0, CONFIG.TOP_K)
        .forEach(([b, w]) => {
          const key = a < b ? a + '-' + b : b + '-' + a;
          if (!kept.has(key) || kept.get(key) < w) kept.set(key, w);
        });
    }

    const edges = [];
    kept.forEach((w, key) => {
      const parts = key.split('-');
      edges.push({ source: +parts[0], target: +parts[1], weight: w });
    });
    return { idf, edges };
  }

  // ─────────────────────────────────────────────────────────────
  // Community detection (Louvain, 가중 모듈러리티 최적화)
  //   사람이 정한 카테고리(대부분 'AI'로 쏠림) 대신, 실제 연결 구조에서
  //   함께 묶이는 글들을 군집으로 찾아 색·라벨을 부여한다. 결정적(노드 순서 고정).
  // ─────────────────────────────────────────────────────────────
  function louvain(N, edges, passes) {
    passes = passes || 10;
    const adj0 = Array.from({ length: N }, () => []);
    const k0 = new Array(N).fill(0);
    let m2 = 0;
    edges.forEach((e) => {
      adj0[e.source].push([e.target, e.weight]);
      adj0[e.target].push([e.source, e.weight]);
      k0[e.source] += e.weight; k0[e.target] += e.weight; m2 += 2 * e.weight;
    });
    if (m2 === 0) return Array.from({ length: N }, (_, i) => i);

    function runLevel(n, adj, k) {
      const comm = Array.from({ length: n }, (_, i) => i);
      const commTot = k.slice();
      let improved = true, guard = 0;
      while (improved && guard++ < 50) {
        improved = false;
        for (let v = 0; v < n; v++) {
          const cv = comm[v];
          commTot[cv] -= k[v];
          const neigh = new Map();
          for (const [u, w] of adj[v]) if (u !== v) neigh.set(comm[u], (neigh.get(comm[u]) || 0) + w);
          let bestC = cv, bestGain = 0;
          neigh.forEach((wIn, c) => {
            const gain = wIn - commTot[c] * k[v] / m2;
            if (gain > bestGain + 1e-12) { bestGain = gain; bestC = c; }
          });
          comm[v] = bestC; commTot[bestC] += k[v];
          if (bestC !== cv) improved = true;
        }
      }
      return comm;
    }

    let curN = N, curAdj = adj0, curK = k0;
    let mapping = Array.from({ length: N }, (_, i) => i);
    for (let p = 0; p < passes; p++) {
      const comm = runLevel(curN, curAdj, curK);
      const uniq = new Map();
      comm.forEach((c) => { if (!uniq.has(c)) uniq.set(c, uniq.size); });
      const comm2 = comm.map((c) => uniq.get(c));
      const newN = uniq.size;
      mapping = mapping.map((m) => comm2[m]);
      if (newN === curN) break;
      const sAdj = Array.from({ length: newN }, () => new Map());
      for (let a = 0; a < curN; a++) {
        const ca = comm2[a];
        for (const [b, w] of curAdj[a]) sAdj[ca].set(comm2[b], (sAdj[ca].get(comm2[b]) || 0) + w);
      }
      const nAdj = Array.from({ length: newN }, () => []);
      const sK = new Array(newN).fill(0);
      for (let ca = 0; ca < newN; ca++) sAdj[ca].forEach((w, cb) => { nAdj[ca].push([cb, w]); sK[ca] += w; });
      curN = newN; curAdj = nAdj; curK = sK;
    }
    return mapping;
  }

  function init(data) {
    const nodes = (data.nodes || []).map((n, i) => Object.assign({ idx: i }, n));
    if (!nodes.length) { spinner.innerHTML = '<p>표시할 글이 없습니다.</p>'; return; }

    // ── Build edges (tag IDF) + degree ──
    const { idf, edges } = buildEdges(nodes);
    nodes.forEach((n) => { n.degree = 0; });
    edges.forEach((e) => { nodes[e.source].degree++; nodes[e.target].degree++; });

    const maxDeg = Math.max(1, d3.max(nodes, (n) => n.degree));
    const rScale = d3.scaleSqrt().domain([0, maxDeg])
      .range([CONFIG.NODE_R_MIN, CONFIG.NODE_R_MAX]);
    nodes.forEach((n) => { n.r = rScale(n.degree); });

    // ── Community detection (Louvain) → node.comm ──
    const rawComm = louvain(nodes.length, edges);
    const rawSize = new Map();
    rawComm.forEach((c) => rawSize.set(c, (rawSize.get(c) || 0) + 1));
    // 큰 군집만 색을 부여하고 작은 군집은 '기타'로 묶음 (크기순 재번호)
    const bigComms = [...rawSize.entries()]
      .filter(([, s]) => s >= CONFIG.MIN_COMMUNITY)
      .sort((a, b) => b[1] - a[1]).map(([c]) => c);
    const commId = new Map();
    bigComms.forEach((c, i) => commId.set(c, i));
    nodes.forEach((n, i) => {
      n.comm = commId.has(rawComm[i]) ? commId.get(rawComm[i]) : CONFIG.OTHER;
    });

    // ── Community auto-labels: 군집내 (태그빈도 × IDF) 상위 태그 ──
    const commTags = new Map();
    const commSize = new Map();
    nodes.forEach((n) => {
      commSize.set(n.comm, (commSize.get(n.comm) || 0) + 1);
      let m = commTags.get(n.comm); if (!m) { m = new Map(); commTags.set(n.comm, m); }
      new Set(n.tags || []).forEach((t) => m.set(t, (m.get(t) || 0) + (idf.get(t) || 0)));
    });
    const commLabel = new Map();
    commTags.forEach((m, c) => {
      if (c === CONFIG.OTHER) { commLabel.set(c, CONFIG.OTHER); return; }
      const top = [...m.entries()].sort((a, b) => b[1] - a[1])
        .slice(0, CONFIG.LABEL_TAGS).map(([t]) => t);
      commLabel.set(c, top.join(', ') || ('군집 ' + (c + 1)));
    });

    // ── Color by community ──
    const color = (c) => c === CONFIG.OTHER ? CONFIG.OTHER_COLOR
      : CONFIG.PALETTE[c % CONFIG.PALETTE.length];
    const cCount = (c) => commSize.get(c) || 0;

    // ── Community list (size desc, OTHER last) ──
    const communities = bigComms.map((_, i) => i);
    if (commSize.has(CONFIG.OTHER)) communities.push(CONFIG.OTHER);

    // ── Seed positions per community (seeding only — no fixed bubbles) ──
    const cr = Math.min(W, H) * 0.34;
    const seed = new Map();
    communities.forEach((c, i) => {
      const a = (2 * Math.PI * i / communities.length) - Math.PI / 2;
      seed.set(c, { x: W / 2 + cr * Math.cos(a), y: H / 2 + cr * Math.sin(a) });
    });
    nodes.forEach((n) => {
      const s = seed.get(n.comm) || { x: W / 2, y: H / 2 };
      n.x = s.x + (Math.random() - 0.5) * 80;
      n.y = s.y + (Math.random() - 0.5) * 80;
    });

    // 군집 centroid(동적) — 라벨 위치 + 약한 응집력에 사용
    const centroid = new Map();
    function updateCentroids() {
      const sx = new Map(), sy = new Map(), cn = new Map();
      nodes.forEach((n) => {
        sx.set(n.comm, (sx.get(n.comm) || 0) + n.x);
        sy.set(n.comm, (sy.get(n.comm) || 0) + n.y);
        cn.set(n.comm, (cn.get(n.comm) || 0) + 1);
      });
      cn.forEach((cnt, c) => centroid.set(c, { x: sx.get(c) / cnt, y: sy.get(c) / cnt }));
    }

    // ── Links (forceLink target; always rendered, faint) ──
    const linkLines = gLinks.selectAll('line').data(edges).join('line')
      .attr('stroke', 'rgba(167,139,250,0.5)')
      .attr('stroke-opacity', 0.12)
      .attr('stroke-width', (e) => 0.4 + Math.min(e.weight, 6) * 0.18);

    // ── Nodes ──
    const nodeCircles = gNodes.selectAll('circle').data(nodes).join('circle')
      .attr('r', (n) => n.r)
      .attr('fill', (n) => color(n.comm))
      .attr('fill-opacity', 0.88)
      .attr('stroke', (n) => color(n.comm))
      .attr('stroke-width', 1)
      .attr('stroke-opacity', 0.5)
      .style('cursor', 'pointer');
    nodeCircles.append('title').text((n) => n.label); // 네이티브 접근성 툴팁

    // ── Hub labels (top-degree, always visible) ──
    const hubNodes = [...nodes].sort((a, b) => b.degree - a.degree).slice(0, CONFIG.HUB_LABELS);
    const hubLabels = gHubLabels.selectAll('text').data(hubNodes).join('text')
      .attr('class', 'kg-hub-label')
      .attr('text-anchor', 'middle')
      .text((n) => n.label.length > 18 ? n.label.slice(0, 17) + '…' : n.label);

    // ── Community labels (centroid, dynamic) — 배경 칩으로 노드 위에서도 또렷 ──
    const commLabelSel = gLabels.selectAll('g.kg-comm-label').data(communities)
      .join((enter) => {
        const gg = enter.append('g').attr('class', 'kg-comm-label');
        gg.append('rect');
        gg.append('text');
        return gg;
      })
      .on('click', (e, c) => { e.stopPropagation(); setFilterBtnActive(c); activateFilter(c); });
    commLabelSel.select('text')
      .attr('text-anchor', 'middle').attr('dominant-baseline', 'middle')
      .attr('fill', (c) => color(c))
      .attr('font-size', '12.5px').attr('font-weight', '700')
      .text((c) => `${commLabel.get(c)} (${cCount(c)})`);
    // 텍스트 크기에 맞춰 배경 칩(rect) 치수 설정
    commLabelSel.each(function (c) {
      const bb = this.querySelector('text').getBBox();
      const px = 9, py = 4;
      d3.select(this).select('rect')
        .attr('x', bb.x - px).attr('y', bb.y - py)
        .attr('width', bb.width + px * 2).attr('height', bb.height + py * 2)
        .attr('rx', 6)
        .attr('fill', 'rgba(15,15,22,0.82)').attr('fill-opacity', 0.82)
        .attr('stroke', color(c)).attr('stroke-opacity', 0.55).attr('stroke-width', 1);
    });

    // ── Simulation: forceLink makes connected posts attract ──
    const linkForce = d3.forceLink(edges)
      .id((n) => n.idx)
      .distance((e) => Math.max(28, 120 - e.weight * 9))
      .strength(0.25);

    // 같은 군집을 동적 중심으로 끌어 영역을 또렷하게 한다(연결력 위에 보조).
    function clusterForce(alpha) {
      updateCentroids();
      nodes.forEach((n) => {
        const c = centroid.get(n.comm); if (!c) return;
        n.vx += (c.x - n.x) * 0.08 * alpha;
        n.vy += (c.y - n.y) * 0.08 * alpha;
      });
    }

    const sim = d3.forceSimulation(nodes)
      .force('link', linkForce)
      .force('charge', d3.forceManyBody().strength(-26))
      .force('collide', d3.forceCollide((n) => n.r + 2).strength(0.85).iterations(2))
      .force('cluster', clusterForce)
      .stop();

    // 전체 노드가 뷰포트에 들어오도록 bounding box 기준 zoom 맞춤
    function fitToView(padding) {
      padding = padding || 60;
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      nodes.forEach((n) => {
        if (n.x < minX) minX = n.x; if (n.x > maxX) maxX = n.x;
        if (n.y < minY) minY = n.y; if (n.y > maxY) maxY = n.y;
      });
      const gw = (maxX - minX) || 1, gh = (maxY - minY) || 1;
      const scale = Math.min(W / (gw + padding * 2), H / (gh + padding * 2), 1.2);
      const tx = W / 2 - (minX + maxX) / 2 * scale;
      const ty = H / 2 - (minY + maxY) / 2 * scale;
      svg.transition().duration(dur(450))
        .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(scale));
    }

    // pre-warm: 깜빡임 없이 안정 위치를 먼저 계산한 뒤 한 번에 렌더 + 전체 맞춤
    const warm = REDUCED ? 80 : 300;
    for (let i = 0; i < warm; i++) sim.tick();
    tick();
    fitToView(60);
    spinner.style.display = 'none';
    setTimeout(() => { if (hint) hint.style.opacity = '0'; }, 2500);

    sim.on('tick', tick); // 드래그 시 재가동용 핸들러

    function tick() {
      linkLines
        .attr('x1', (e) => e.source.x).attr('y1', (e) => e.source.y)
        .attr('x2', (e) => e.target.x).attr('y2', (e) => e.target.y);
      nodeCircles.attr('cx', (n) => n.x).attr('cy', (n) => n.y);
      hubLabels.attr('x', (n) => n.x).attr('y', (n) => n.y - n.r - 3);
      // 군집 라벨 칩을 군집 무게중심에 동적으로 배치
      commLabelSel.attr('transform', (c) => {
        const ct = centroid.get(c) || { x: 0, y: 0 };
        return `translate(${ct.x},${ct.y})`;
      });
    }

    // ── Drag ──
    nodeCircles.call(d3.drag()
      .on('start', (e, n) => { if (!e.active) sim.alphaTarget(0.12).restart(); n.fx = n.x; n.fy = n.y; })
      .on('drag', (e, n) => { n.fx = e.x; n.fy = e.y; })
      .on('end', (e, n) => { if (!e.active) sim.alphaTarget(0); n.fx = null; n.fy = null; }));

    // ── Tooltip ──
    nodeCircles
      .on('mousemove', (e, n) => {
        tooltip.style.display = 'block';
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top = (e.clientY - 6) + 'px';
        tooltip.textContent = n.label;
      })
      .on('mouseleave', () => { tooltip.style.display = 'none'; });

    // ── State ──
    let activeNode = null;
    let activeFilter = 'all';
    let currentFilterOpacity = () => 1;

    const neighborsOf = (node) => {
      const ids = new Set([node.idx]);
      edges.forEach((e) => {
        if (e.source.idx === node.idx) ids.add(e.target.idx);
        else if (e.target.idx === node.idx) ids.add(e.source.idx);
      });
      return ids;
    };

    // ── Node click ──
    nodeCircles.on('click', (e, node) => {
      e.stopPropagation();
      tooltip.style.display = 'none';
      if (activeNode === node) { deselect(); return; }
      activeNode = node;
      showPanel(node);
      highlightNode(node);
    });
    svg.on('click', () => deselect());

    function deselect() {
      clearHighlight(); panel.style.display = 'none'; activeNode = null;
    }

    function showPanel(node) {
      const col = color(node.comm);
      document.getElementById('kg-panel-title').textContent = node.label;
      const catEl = document.getElementById('kg-panel-cat');
      catEl.textContent = commLabel.get(node.comm) || CONFIG.OTHER; // 군집 라벨
      catEl.style.color = col; catEl.style.borderColor = col + '60'; catEl.style.background = col + '1f';
      document.getElementById('kg-panel-date').textContent =
        (node.date || '') + (node.group ? ' · ' + node.group : ''); // 날짜 + 원 카테고리

      document.getElementById('kg-panel-tags').innerHTML =
        (node.tags || []).map((t) => `<span class="kg-tag">${esc(t)}</span>`).join('');
      document.getElementById('kg-panel-excerpt').textContent = node.excerpt || '';

      // 연관 글: 이 노드의 엣지를 가중치순 — 공유 태그도 노출
      const rel = edges
        .filter((e) => e.source.idx === node.idx || e.target.idx === node.idx)
        .map((e) => {
          const other = e.source.idx === node.idx ? e.target : e.source;
          const shared = (node.tags || []).filter((t) => (other.tags || []).includes(t));
          return { other, weight: e.weight, shared };
        })
        .sort((a, b) => b.weight - a.weight).slice(0, 6);

      const relEl = document.getElementById('kg-panel-related');
      if (rel.length) {
        relEl.innerHTML = '<div class="kg-related-title">연관 글</div>' + rel.map((r) =>
          `<div class="kg-related-item" tabindex="0" data-idx="${r.other.idx}">
             <span class="kg-related-badge">${r.shared.length || '~'}</span>
             <span>${esc(r.other.label)}
               ${r.shared.length ? `<span class="kg-related-shared">공유: ${esc(r.shared.slice(0,4).join(', '))}</span>` : ''}
             </span>
           </div>`).join('');
        relEl.querySelectorAll('.kg-related-item').forEach((el) => {
          const go = () => focusNode(nodes[+el.dataset.idx]);
          el.addEventListener('click', go);
          el.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') go(); });
        });
      } else { relEl.innerHTML = ''; }

      document.getElementById('kg-panel-link').href = node.url;
      panel.style.display = 'flex';
    }

    function highlightNode(node) {
      const ids = neighborsOf(node);
      nodeCircles
        .attr('opacity', (n) => ids.has(n.idx) ? 1 : CONFIG.FADE_OP);
      linkLines
        .attr('stroke-opacity', (e) =>
          (e.source.idx === node.idx || e.target.idx === node.idx) ? 0.7 : 0.02);
      hubLabels.attr('opacity', (n) => ids.has(n.idx) ? 1 : CONFIG.FADE_OP);
    }

    function clearHighlight() {
      nodeCircles.attr('opacity', currentFilterOpacity);
      linkLines.attr('stroke-opacity', 0.12);
      hubLabels.attr('opacity', 1);
    }

    // 특정 노드로 카메라 이동 + 선택
    function focusNode(node) {
      activeNode = node; showPanel(node); highlightNode(node);
      const sc = CONFIG.FOCUS_SCALE;
      svg.transition().duration(dur(600)).call(
        zoom.transform,
        d3.zoomIdentity.translate(W / 2 - node.x * sc, H / 2 - node.y * sc).scale(sc)
      );
    }

    // ── Filter buttons (군집 단위) ──
    const filterContainer = document.getElementById('kg-filters');
    communities.forEach((c) => {
      const btn = document.createElement('button');
      btn.className = 'kg-filter-btn';
      btn.dataset.cat = String(c);
      btn.innerHTML = `<span class="kg-filter-dot" style="background:${color(c)}"></span>${esc(commLabel.get(c))} (${cCount(c)})`;
      filterContainer.appendChild(btn);
    });
    document.querySelectorAll('.kg-filter-btn').forEach((btn) => {
      btn.addEventListener('click', () => { setFilterBtnActive(btn.dataset.cat); activateFilter(btn.dataset.cat); });
    });

    function setFilterBtnActive(cat) {
      document.querySelectorAll('.kg-filter-btn').forEach((b) =>
        b.classList.toggle('active', b.dataset.cat === String(cat)));
    }

    function activateFilter(cat) {
      const catStr = String(cat);
      activeFilter = catStr; deselect();
      if (catStr === 'all') {
        currentFilterOpacity = () => 1;
        nodeCircles.attr('opacity', 1);
        commLabelSel.attr('opacity', 1);
        fitToView(60);
      } else {
        currentFilterOpacity = (n) => String(n.comm) === catStr ? 1 : CONFIG.FADE_OP;
        nodeCircles.attr('opacity', currentFilterOpacity);
        commLabelSel.attr('opacity', (c) => String(c) === catStr ? 1 : 0.3);
        const target = communities.find((c) => String(c) === catStr);
        const ctr = centroid.get(target);
        if (ctr) {
          const sc = CONFIG.FOCUS_SCALE;
          svg.transition().duration(dur(600)).call(
            zoom.transform,
            d3.zoomIdentity.translate(W / 2 - ctr.x * sc, H / 2 - ctr.y * sc).scale(sc));
        }
      }
    }

    // ── Search (with camera focus on matches) ──
    const searchInput = document.getElementById('kg-search');
    let searchTimer = null;
    searchInput.addEventListener('input', () => {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(runSearch, 180);
    });
    function runSearch() {
      const q = searchInput.value.trim().toLowerCase();
      if (!q) { nodeCircles.attr('opacity', currentFilterOpacity); return; }
      const matched = [];
      nodeCircles.attr('opacity', (n) => {
        if (activeFilter !== 'all' && String(n.comm) !== activeFilter) return CONFIG.FADE_OP;
        const m = n.label.toLowerCase().includes(q) ||
          (n.tags || []).some((t) => t.toLowerCase().includes(q));
        if (m) matched.push(n);
        return m ? 1 : CONFIG.FADE_OP;
      });
      if (matched.length) {
        const mx = d3.mean(matched, (n) => n.x), my = d3.mean(matched, (n) => n.y);
        const sc = matched.length === 1 ? CONFIG.FOCUS_SCALE : 1.3;
        svg.transition().duration(dur(500)).call(
          zoom.transform,
          d3.zoomIdentity.translate(W / 2 - mx * sc, H / 2 - my * sc).scale(sc));
      }
    }

    // ── Reset ──
    function resetAll() {
      setFilterBtnActive('all'); activateFilter('all');
      searchInput.value = '';
    }
    document.getElementById('kg-reset-btn').addEventListener('click', resetAll);
    document.getElementById('kg-panel-close').addEventListener('click', deselect);

    // ── Keyboard ──
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (panel.style.display === 'flex') deselect();
        else if (document.activeElement === searchInput) { searchInput.value = ''; runSearch(); searchInput.blur(); }
      } else if (e.key === 'r' && document.activeElement !== searchInput) {
        resetAll();
      } else if (e.key === '/' && document.activeElement !== searchInput) {
        e.preventDefault(); searchInput.focus();
      }
    });

    // ── Stats / legend summary ──
    document.getElementById('kg-stat').textContent =
      `${nodes.length}개 글 · ${edges.length}개 연결 · ${communities.length}개 군집`;

    // ── Resize ──
    let resizeTimer = null;
    const ro = new ResizeObserver(() => {
      W = wrap.clientWidth; H = wrap.clientHeight;
      svg.attr('width', W).attr('height', H);
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(() => { if (activeFilter === 'all' && !activeNode) fitToView(60); }, 200);
    });
    ro.observe(wrap);
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, (c) =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }
})();
</script>
