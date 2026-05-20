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
  #kg-search::placeholder { color: #555570; }
  #kg-search:focus { border-color: rgba(139,92,246,0.6); }

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
    color: #9090b0;
    font-size: 12px;
    padding: 4px 10px;
    cursor: pointer;
    transition: all 0.18s;
    white-space: nowrap;
  }
  .kg-filter-btn:hover { background: rgba(139,92,246,0.12); color: #c4c4d4; }
  .kg-filter-btn.active {
    background: rgba(139,92,246,0.18) !important;
    border-color: rgba(139,92,246,0.6) !important;
    color: #e2e2f0 !important;
  }
  #kg-stat {
    font-size: 11px;
    color: #555570;
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
  .kg-loader p { color: #555570; font-size: 12px; margin: 0; }
  @keyframes kg-spin { to { transform: rotate(360deg); } }

  /* ── Info panel ── */
  #kg-panel {
    width: 300px;
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
    color: #e2e2f0;
    line-height: 1.45;
    flex: 1;
    margin: 0;
  }
  #kg-panel-close {
    background: none;
    border: none;
    color: #555570;
    font-size: 20px;
    cursor: pointer;
    padding: 0 2px;
    line-height: 1;
    flex-shrink: 0;
  }
  #kg-panel-close:hover { color: #a78bfa; }
  #kg-panel-cat {
    display: inline-block;
    font-size: 11px;
    padding: 2px 8px;
    border-radius: 3px;
    border: 1px solid;
    font-weight: 500;
  }
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
    color: #9090b0;
    border-color: rgba(139,92,246,0.3);
    background: rgba(139,92,246,0.06);
  }
  #kg-panel-excerpt {
    font-size: 13px;
    color: #8888a8;
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
    padding: 5px 6px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    color: #8888a8;
    transition: all 0.15s;
    line-height: 1.4;
  }
  .kg-related-item:hover { background: rgba(139,92,246,0.1); color: #e2e2f0; }
  .kg-related-badge {
    font-size: 10px;
    background: rgba(139,92,246,0.2);
    color: #a78bfa;
    border-radius: 3px;
    padding: 1px 5px;
    flex-shrink: 0;
    margin-top: 1px;
  }
  #kg-panel-link {
    display: inline-block;
    margin-top: 4px;
    padding: 7px 14px;
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 5px;
    color: #a78bfa;
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.18s;
    align-self: flex-start;
  }
  #kg-panel-link:hover { background: rgba(139,92,246,0.22); border-color: rgba(139,92,246,0.7); }

  /* ── Tooltip ── */
  #kg-tooltip {
    position: fixed;
    background: rgba(15,15,22,0.97);
    border: 1px solid rgba(139,92,246,0.35);
    border-radius: 5px;
    color: #e2e2f0;
    font-size: 12px;
    padding: 5px 10px;
    pointer-events: none;
    display: none;
    z-index: 200;
    max-width: 260px;
    line-height: 1.4;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
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
    color: #a78bfa;
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

  /* ── Reset zoom button ── */
  #kg-reset {
    position: absolute;
    bottom: 16px;
    right: 16px;
    z-index: 30;
  }

  /* ── Cluster label SVG text ── */
  .cluster-label { pointer-events: none; }

  /* ── Mobile ── */
  @media (max-width: 680px) {
    #kg-panel {
      position: absolute;
      bottom: 0; left: 0; right: 0;
      width: 100%;
      max-height: 55vh;
      border-left: none;
      border-top: 1px solid rgba(139,92,246,0.25);
    }
    #kg-search { width: 140px; }
  }
</style>

<script src="https://unpkg.com/d3@7.9.0/dist/d3.min.js"></script>

<div id="kg-container">

  <div id="kg-topbar">
    <input id="kg-search" type="text" placeholder="포스트 또는 태그 검색...">
    <div id="kg-filters">
      <button class="kg-filter-btn active" data-cat="all">전체</button>
    </div>
    <span id="kg-stat"></span>
  </div>

  <div id="kg-main">
    <div id="kg-graph-wrap">
      <div class="kg-loader" id="kg-spinner">
        <div class="kg-loader-ring"></div>
        <p>그래프 로딩 중...</p>
      </div>
      <svg id="kg-svg"></svg>
      <div id="kg-nav">
        <a href="/" class="kg-nav-btn">&#127968; 홈</a>
        <button class="kg-nav-btn" onclick="history.back()">&#8592; 이전</button>
      </div>
      <div id="kg-reset">
        <button class="kg-nav-btn" id="kg-reset-btn" title="전체 보기">&#8635; 전체</button>
      </div>
    </div>

    <div id="kg-panel">
      <div id="kg-panel-header">
        <h3 id="kg-panel-title"></h3>
        <button id="kg-panel-close">&#215;</button>
      </div>
      <div><span id="kg-panel-cat"></span></div>
      <div id="kg-panel-tags"></div>
      <p id="kg-panel-excerpt"></p>
      <div id="kg-panel-related"></div>
      <a id="kg-panel-link" href="#" target="_blank">읽기 &#8594;</a>
    </div>
  </div>

</div>

<div id="kg-tooltip"></div>

<script>
(function () {
  const COLORS = {
    'AI':                     '#8b5cf6',
    '교육':                   '#6366f1',
    '학습과학':               '#3b82f6',
    'AI디지털기반교육혁신':   '#f97316',
    '철학':                   '#ec4899',
    '인지과학':               '#f59e0b',
    '바이브코딩':             '#06b6d4',
    '코딩':                   '#10b981',
    'default':                '#6b6b8a'
  };
  const color = (cat) => COLORS[cat] || COLORS.default;

  const NODE_R  = 6;
  const FADE_OP = 0.08;

  const wrap    = document.getElementById('kg-graph-wrap');
  const svgEl   = document.getElementById('kg-svg');
  const spinner = document.getElementById('kg-spinner');
  const panel   = document.getElementById('kg-panel');
  const tooltip = document.getElementById('kg-tooltip');

  let W = wrap.clientWidth;
  let H = wrap.clientHeight;

  const svg = d3.select(svgEl).attr('width', W).attr('height', H);
  const g   = svg.append('g').attr('id', 'kg-root');

  const zoom = d3.zoom()
    .scaleExtent([0.15, 6])
    .on('zoom', (e) => g.attr('transform', e.transform));
  svg.call(zoom).on('dblclick.zoom', null);

  const gClusterBg = g.append('g').attr('id', 'cluster-bg');
  const gLinks     = g.append('g').attr('id', 'links');
  const gNodes     = g.append('g').attr('id', 'nodes');
  const gLabels    = g.append('g').attr('id', 'cluster-labels');

  fetch('/knowledge-graph.json')
    .then((r) => r.json())
    .then((data) => init(data))
    .catch((err) => {
      console.error('Graph load error:', err);
      spinner.style.display = 'none';
    });

  function init(data) {
    const nodes    = data.nodes;
    const rawEdges = data.edges || [];

    const nodeById = new Map(nodes.map((n) => [n.id, n]));

    // edges: keep only those referencing valid nodes, skip cross-cluster if edge value is 0
    const edges = rawEdges
      .filter((e) => nodeById.has(e.from) && nodeById.has(e.to))
      .map((e) => ({ from: e.from, to: e.to, value: e.value || 1 }));

    // ── Cluster setup ──────────────────────────────────────────
    const catSet    = new Set(nodes.map((n) => n.group));
    const categories = [...catSet].sort((a, b) => {
      // sort by known order, unknowns last
      const ord = Object.keys(COLORS);
      const ia = ord.indexOf(a); const ib = ord.indexOf(b);
      return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
    });

    const catCount  = (cat) => nodes.filter((n) => n.group === cat).length;

    // Arrange cluster centers in a circle
    const cr = Math.min(W, H) * 0.32;
    const clusterCenters = {};
    categories.forEach((cat, i) => {
      const angle = (2 * Math.PI * i / categories.length) - Math.PI / 2;
      clusterCenters[cat] = {
        x: W / 2 + cr * Math.cos(angle),
        y: H / 2 + cr * Math.sin(angle),
        count: catCount(cat)
      };
    });

    // Bubble radius: adaptive to count, capped
    const maxCount = Math.max(...categories.map((c) => clusterCenters[c].count));
    const bubbleR  = (cat) => {
      const n = clusterCenters[cat].count;
      return 42 + 110 * Math.sqrt(n / maxCount);
    };

    // ── Initialize node positions near cluster center ───────────
    nodes.forEach((node) => {
      const c = clusterCenters[node.group] || { x: W / 2, y: H / 2 };
      const a = Math.random() * 2 * Math.PI;
      const r = Math.random() * 30;
      node.x = c.x + r * Math.cos(a);
      node.y = c.y + r * Math.sin(a);
    });

    // ── Cluster force ───────────────────────────────────────────
    function clusterForce(alpha) {
      nodes.forEach((node) => {
        const c = clusterCenters[node.group];
        if (!c) return;
        node.vx += (c.x - node.x) * 0.22 * alpha;
        node.vy += (c.y - node.y) * 0.22 * alpha;
      });
    }

    // ── Draw cluster backgrounds ────────────────────────────────
    const clusterBgs = gClusterBg.selectAll('circle')
      .data(categories)
      .join('circle')
      .attr('cx',           (cat) => clusterCenters[cat].x)
      .attr('cy',           (cat) => clusterCenters[cat].y)
      .attr('r',            bubbleR)
      .attr('fill',         (cat) => color(cat))
      .attr('fill-opacity', 0.07)
      .attr('stroke',       (cat) => color(cat))
      .attr('stroke-opacity', 0.22)
      .attr('stroke-width', 1.5)
      .style('cursor', 'pointer')
      .on('click', (e, cat) => {
        e.stopPropagation();
        activateFilter(cat);
        setFilterBtnActive(cat);
      });

    // ── Draw cluster labels ─────────────────────────────────────
    gLabels.selectAll('text')
      .data(categories)
      .join('text')
      .attr('class', 'cluster-label')
      .attr('x',           (cat) => clusterCenters[cat].x)
      .attr('y',           (cat) => clusterCenters[cat].y - bubbleR(cat) + 18)
      .attr('text-anchor', 'middle')
      .attr('fill',        (cat) => color(cat))
      .attr('font-size',   '13px')
      .attr('font-weight', '600')
      .text((cat) => `${cat} (${clusterCenters[cat].count})`);

    // ── Draw link lines (hidden until node selected) ────────────
    const linkLines = gLinks.selectAll('line')
      .data(edges)
      .join('line')
      .attr('stroke',         'rgba(167,139,250,0.25)')
      .attr('stroke-width',   (e) => Math.max(e.value * 0.5, 0.4))
      .style('display',       'none')
      .style('pointer-events','none');

    // ── Draw nodes ──────────────────────────────────────────────
    const nodeCircles = gNodes.selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r',             NODE_R)
      .attr('fill',          (n) => color(n.group))
      .attr('fill-opacity',  0.85)
      .attr('stroke',        (n) => color(n.group))
      .attr('stroke-width',  1)
      .attr('stroke-opacity',0.45)
      .style('cursor',       'pointer');

    // ── Simulation ──────────────────────────────────────────────
    const sim = d3.forceSimulation(nodes)
      .force('cluster', clusterForce)
      .force('collide',  d3.forceCollide(NODE_R + 2).strength(0.88).iterations(2))
      .force('charge',   d3.forceManyBody().strength(-6))
      .alphaDecay(0.022)
      .on('tick', tick)
      .on('end',  () => { spinner.style.display = 'none'; });

    function tick() {
      nodeCircles.attr('cx', (n) => n.x).attr('cy', (n) => n.y);

      // Keep link lines in sync when dragging
      if (activeNode) {
        linkLines
          .filter((e) => e.from === activeNode.id || e.to === activeNode.id)
          .attr('x1', (e) => (nodeById.get(e.from) || {}).x || 0)
          .attr('y1', (e) => (nodeById.get(e.from) || {}).y || 0)
          .attr('x2', (e) => (nodeById.get(e.to)   || {}).x || 0)
          .attr('y2', (e) => (nodeById.get(e.to)   || {}).y || 0);
      }
    }

    // ── Drag ────────────────────────────────────────────────────
    nodeCircles.call(
      d3.drag()
        .on('start', (e, n) => {
          if (!e.active) sim.alphaTarget(0.12).restart();
          n.fx = n.x; n.fy = n.y;
        })
        .on('drag', (e, n) => { n.fx = e.x; n.fy = e.y; })
        .on('end',  (e, n) => {
          if (!e.active) sim.alphaTarget(0);
          n.fx = null; n.fy = null;
        })
    );

    // ── Tooltip ─────────────────────────────────────────────────
    nodeCircles
      .on('mousemove', (e, n) => {
        tooltip.style.display = 'block';
        tooltip.style.left = (e.clientX + 14) + 'px';
        tooltip.style.top  = (e.clientY -  6) + 'px';
        tooltip.textContent = n.label;
      })
      .on('mouseleave', () => { tooltip.style.display = 'none'; });

    // ── Node click ──────────────────────────────────────────────
    let activeNode = null;

    nodeCircles.on('click', (e, node) => {
      e.stopPropagation();
      tooltip.style.display = 'none';
      if (activeNode === node) {
        clearHighlight();
        panel.style.display = 'none';
        activeNode = null;
        return;
      }
      activeNode = node;
      showPanel(node);
      highlightNode(node);
    });

    svg.on('click', () => {
      clearHighlight();
      panel.style.display = 'none';
      activeNode = null;
    });

    function showPanel(node) {
      const col = color(node.group);

      document.getElementById('kg-panel-title').textContent = node.label;

      const catEl = document.getElementById('kg-panel-cat');
      catEl.textContent = node.group;
      catEl.style.color      = col;
      catEl.style.borderColor = col + '50';
      catEl.style.background  = col + '18';

      const tagsEl = document.getElementById('kg-panel-tags');
      tagsEl.innerHTML = (node.tags || [])
        .map((t) => `<span class="kg-tag">${t}</span>`)
        .join('');

      document.getElementById('kg-panel-excerpt').textContent = node.excerpt || '';

      // Related posts: edges connected to this node, sorted by weight
      const related = edges
        .filter((e) => e.from === node.id || e.to === node.id)
        .sort((a, b) => b.value - a.value)
        .slice(0, 6);

      const relEl = document.getElementById('kg-panel-related');
      if (related.length) {
        const items = related.map((e) => {
          const otherId = e.from === node.id ? e.to : e.from;
          const other   = nodeById.get(otherId);
          if (!other) return '';
          return `<div class="kg-related-item" onclick="window.open('${other.url}','_blank')">
            <span class="kg-related-badge">${e.value}</span>
            <span>${other.label}</span>
          </div>`;
        }).join('');
        relEl.innerHTML = `<div class="kg-related-title">연관 글</div>${items}`;
      } else {
        relEl.innerHTML = '';
      }

      const linkEl = document.getElementById('kg-panel-link');
      linkEl.href  = node.url;

      panel.style.display = 'flex';
    }

    function highlightNode(node) {
      const connectedIds = new Set([node.id]);
      edges.forEach((e) => {
        if (e.from === node.id) connectedIds.add(e.to);
        else if (e.to === node.id) connectedIds.add(e.from);
      });

      nodeCircles
        .attr('opacity', (n) => connectedIds.has(n.id) ? 1 : FADE_OP)
        .attr('r',       (n) => n.id === node.id ? NODE_R + 2 : NODE_R);

      linkLines
        .style('display', (e) =>
          (e.from === node.id || e.to === node.id) ? 'block' : 'none'
        )
        .attr('x1', (e) => (nodeById.get(e.from) || {}).x || 0)
        .attr('y1', (e) => (nodeById.get(e.from) || {}).y || 0)
        .attr('x2', (e) => (nodeById.get(e.to)   || {}).x || 0)
        .attr('y2', (e) => (nodeById.get(e.to)   || {}).y || 0);
    }

    function clearHighlight() {
      nodeCircles.attr('opacity', currentFilterOpacity).attr('r', NODE_R);
      linkLines.style('display', 'none');
    }

    // ── Filter ──────────────────────────────────────────────────
    let activeFilter         = 'all';
    let currentFilterOpacity = (_n) => 1;

    // Build filter buttons
    const filterContainer = document.getElementById('kg-filters');
    categories.forEach((cat) => {
      const btn = document.createElement('button');
      btn.className      = 'kg-filter-btn';
      btn.dataset.cat    = cat;
      btn.style.color    = color(cat);
      btn.style.borderColor = color(cat) + '55';
      btn.textContent    = `${cat} (${catCount(cat)})`;
      filterContainer.appendChild(btn);
    });

    document.getElementById('kg-stat').textContent =
      `${nodes.length}개 포스트 · ${categories.length}개 주제`;

    document.querySelectorAll('.kg-filter-btn').forEach((btn) => {
      btn.addEventListener('click', () => {
        const cat = btn.dataset.cat;
        setFilterBtnActive(cat);
        activateFilter(cat);
      });
    });

    function setFilterBtnActive(cat) {
      document.querySelectorAll('.kg-filter-btn').forEach((b) => {
        b.classList.toggle('active', b.dataset.cat === cat);
      });
    }

    function activateFilter(cat) {
      activeFilter = cat;
      clearHighlight();
      panel.style.display = 'none';
      activeNode = null;

      if (cat === 'all') {
        currentFilterOpacity = (_n) => 1;
        nodeCircles.attr('opacity', 1);
        clusterBgs.attr('opacity', 1);
        gLabels.selectAll('text').attr('opacity', 1);
        svg.transition().duration(500)
          .call(zoom.transform, d3.zoomIdentity);
      } else {
        currentFilterOpacity = (n) => n.group === cat ? 1 : FADE_OP;
        nodeCircles.attr('opacity', currentFilterOpacity);
        clusterBgs.attr('opacity', (c) => c === cat ? 1 : 0.25);
        gLabels.selectAll('text').attr('opacity', (c) => c === cat ? 1 : 0.3);

        const c  = clusterCenters[cat];
        const sc = 2.0;
        const tx = W / 2 - c.x * sc;
        const ty = H / 2 - c.y * sc;
        svg.transition().duration(600)
          .call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(sc));
      }
    }

    // ── Search ──────────────────────────────────────────────────
    const searchInput = document.getElementById('kg-search');
    searchInput.addEventListener('input', () => {
      const q = searchInput.value.trim().toLowerCase();
      if (!q) {
        nodeCircles.attr('opacity', currentFilterOpacity);
        return;
      }
      nodeCircles.attr('opacity', (n) => {
        if (activeFilter !== 'all' && n.group !== activeFilter) return FADE_OP;
        const match = n.label.toLowerCase().includes(q) ||
          (n.tags || []).some((t) => t.toLowerCase().includes(q));
        return match ? 1 : FADE_OP;
      });
    });

    // ── Reset zoom ──────────────────────────────────────────────
    document.getElementById('kg-reset-btn').addEventListener('click', () => {
      setFilterBtnActive('all');
      activateFilter('all');
      searchInput.value = '';
    });

    // ── Resize ──────────────────────────────────────────────────
    const ro = new ResizeObserver(() => {
      W = wrap.clientWidth;
      H = wrap.clientHeight;
      svg.attr('width', W).attr('height', H);
    });
    ro.observe(wrap);
  }
})();
</script>
