/* ==========================================================================
   포스트 미니 그래프 뷰 (Quartz 스타일 로컬 그래프)
   우측 사이드바 "On this page" 위에 현재 글 + 관련 글 top-8을 표시한다.
   데이터: /knowledge-graph.json (노드만). 엣지는 지식그래프 페이지와 동일한
   태그 IDF 가중 스코어링을 현재 글 기준으로 축소 계산 (D3 의존성 없음).
   가독성: 컨테이너 실측 폭으로 viewBox를 1:1 px 매핑(스케일 블러 방지),
   라벨 halo(paint-order stroke) + 4방향(아래/위/좌/우) 그리디 충돌 회피 배치.
   확대: 헤더 돋보기 버튼 → 모달에서 같은 그래프를 대형 캔버스로 재레이아웃.
   ========================================================================== */

(function () {
  var root = document.getElementById('post-graph');
  var canvas = document.getElementById('post-graph-canvas');
  if (!root || !canvas || !window.__currentPost) return;

  var MAX_NEIGHBORS = 8;   // 지식그래프 TOP_K와 동일
  var MINI_H = 240;        // 미니 캔버스 높이(px)

  function normUrl(u) {
    try { u = decodeURIComponent(u); } catch (e) { /* 이중 인코딩 등 — raw 비교 */ }
    return u.replace(/\/+$/, '');
  }

  function buildLocalGraph(nodes) {
    var N = nodes.length;
    var df = new Map();
    nodes.forEach(function (n) {
      new Set(n.tags || []).forEach(function (t) { df.set(t, (df.get(t) || 0) + 1); });
    });
    var idf = new Map();
    df.forEach(function (c, t) { idf.set(t, Math.log(N / c)); });

    var current = normUrl(location.pathname);
    var centerIdx = -1;
    for (var i = 0; i < N; i++) {
      if (normUrl(nodes[i].url) === current) { centerIdx = i; break; }
    }
    if (centerIdx < 0) return null;

    // 현재 글과 태그를 공유하는 후보 스코어링 (지식그래프 buildEdges와 동일 가중)
    var cand = new Map();
    var centerTags = new Set(nodes[centerIdx].tags || []);
    nodes.forEach(function (n, b) {
      if (b === centerIdx) return;
      var w = 0;
      new Set(n.tags || []).forEach(function (t) {
        if (centerTags.has(t)) w += idf.get(t) || 0;
      });
      if (w > 0) cand.set(b, w);
    });
    if (cand.size === 0) {
      // 카테고리 fallback — 지식그래프와 동일 (고립 방지)
      var g = nodes[centerIdx].group, taken = 0;
      for (var j = 0; j < N && taken < 2; j++) {
        if (j !== centerIdx && nodes[j].group === g) { cand.set(j, 0.01); taken++; }
      }
    }
    var neighbors = Array.from(cand.entries())
      .sort(function (x, y) { return y[1] - x[1]; })
      .slice(0, MAX_NEIGHBORS);
    if (neighbors.length === 0) return null;

    // 로컬 노드/엣지 구성 (0 = center)
    var local = [{ node: nodes[centerIdx], center: true }];
    var edges = [];
    neighbors.forEach(function (pair, k) {
      local.push({ node: nodes[pair[0]], center: false });
      edges.push({ a: 0, b: k + 1, w: pair[1] });
    });
    // 이웃끼리의 연결 (노드당 top-2만 유지해 과밀 방지)
    var per = new Map();
    for (var p = 1; p < local.length; p++) {
      var tagsP = new Set(local[p].node.tags || []);
      for (var q = p + 1; q < local.length; q++) {
        var w2 = 0;
        new Set(local[q].node.tags || []).forEach(function (t) {
          if (tagsP.has(t)) w2 += idf.get(t) || 0;
        });
        if (w2 > 0) {
          var e2 = { a: p, b: q, w: w2 };
          if (!per.has(p)) per.set(p, []);
          if (!per.has(q)) per.set(q, []);
          per.get(p).push(e2);
          per.get(q).push(e2);
        }
      }
    }
    var seen = new Set();
    per.forEach(function (list) {
      list.sort(function (x, y) { return y.w - x.w; }).slice(0, 2).forEach(function (e) {
        var key = e.a + '-' + e.b;
        if (!seen.has(key)) { seen.add(key); edges.push(e); }
      });
    });
    return { local: local, edges: edges };
  }

  // 소규모 포스 시뮬레이션 (동기 실행 후 정적 렌더 — 노드 ≤ 9)
  // s: 크기 배율 (미니 1, 모달 ~2). 좌표·간격·충돌 임계가 함께 스케일된다.
  function runLayout(local, edges, W, H, s, opts) {
    var fontPx = opts.large ? 13 : 10.5;
    var cx = W / 2, cy = H / 2 - 8 * s;
    var maxW = edges.reduce(function (m, e) { return Math.max(m, e.w); }, 0.01);
    var ring = Math.min(W, H) / 2 - 40 * s;
    var mx = Math.min(30, 18 * s);
    var myTop = Math.min(30, 20 * s);
    var myBot = Math.min(56, 34 * s);
    local.forEach(function (d, i) {
      if (d.center) { d.x = cx; d.y = cy; }
      else {
        var ang = (i / (local.length - 1)) * Math.PI * 2 + 0.7;
        d.x = cx + Math.cos(ang) * ring;
        d.y = cy + Math.sin(ang) * ring;
      }
      d.vx = 0; d.vy = 0;
    });
    for (var iter = 0; iter < 300; iter++) {
      // 반발력
      for (var a = 0; a < local.length; a++) {
        for (var b = a + 1; b < local.length; b++) {
          var dx = local[b].x - local[a].x, dy = local[b].y - local[a].y;
          var d2 = dx * dx + dy * dy || 1;
          var f = 3000 * s * s / d2, dist = Math.sqrt(d2);
          var fx = (dx / dist) * f, fy = (dy / dist) * f;
          local[a].vx -= fx; local[a].vy -= fy;
          local[b].vx += fx; local[b].vy += fy;
        }
      }
      // 스프링 (가중치 높을수록 짧게)
      edges.forEach(function (e) {
        var na = local[e.a], nb = local[e.b];
        var dx = nb.x - na.x, dy = nb.y - na.y;
        var dist = Math.sqrt(dx * dx + dy * dy) || 1;
        var rest = (58 + (1 - e.w / maxW) * 30) * s;
        var f = (dist - rest) * 0.03;
        var fx = (dx / dist) * f, fy = (dy / dist) * f;
        na.vx += fx; na.vy += fy;
        nb.vx -= fx; nb.vy -= fy;
      });
      // 중심 인력 + 적분
      local.forEach(function (d) {
        if (d.center) { d.x = cx; d.y = cy; d.vx = 0; d.vy = 0; return; }
        d.vx += (cx - d.x) * (0.01 / s);
        d.vy += (cy - d.y) * (0.01 / s);
        d.vx *= 0.85; d.vy *= 0.85;
        d.x = Math.max(mx, Math.min(W - mx, d.x + d.vx));
        d.y = Math.max(myTop, Math.min(H - myBot, d.y + d.vy));
      });
    }
    return maxW;
  }

  // 라벨 4방향(아래/위/오른쪽/왼쪽) 그리디 배치 — 이미 놓인 라벨·경계와의
  // 겹침 비용이 최소인 위치를 선택한다. 중심 라벨을 최우선 배치.
  function placeLabels(local, W, H, opts) {
    var fontPx = opts.large ? 13 : 10.5;
    var grow = 1 + (opts.scale - 1) * 0.55;
    var placed = [];
    function rectFor(d, pos) {
      var t = d.node.label || '';
      var len = Math.min(t.length, opts.trunc) + (t.length > opts.trunc ? 1 : 0);
      var w = len * fontPx * 0.92, h = fontPx * 1.35;
      var r = d.r, cx = d.x, cy = d.y;
      if (pos === 'b') return { x: cx - w / 2, y: cy + r + 4, w: w, h: h, tx: cx, ty: cy + r + 4 + fontPx * 0.95, anchor: 'middle' };
      if (pos === 't') return { x: cx - w / 2, y: cy - r - 4 - h, w: w, h: h, tx: cx, ty: cy - r - 4 - h + fontPx * 0.95, anchor: 'middle' };
      if (pos === 'r') return { x: cx + r + 5, y: cy - h / 2, w: w, h: h, tx: cx + r + 5, ty: cy - h / 2 + fontPx * 0.95, anchor: 'start' };
      return { x: cx - r - 5 - w, y: cy - h / 2, w: w, h: h, tx: cx - r - 5, ty: cy - h / 2 + fontPx * 0.95, anchor: 'end' };
    }
    function overlapArea(a, b) {
      var ox = Math.max(0, Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x));
      var oy = Math.max(0, Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y));
      return ox * oy;
    }
    function outOfBounds(rc) {
      var o = 0;
      if (rc.x < 2) o += 2 - rc.x;
      if (rc.x + rc.w > W - 2) o += rc.x + rc.w - (W - 2);
      if (rc.y < 2) o += 2 - rc.y;
      if (rc.y + rc.h > H - 2) o += rc.y + rc.h - (H - 2);
      return o * 12;
    }
    // 노드 원도 장애물로 등록 — 라벨이 다른 노드 위를 지나지 않게
    local.forEach(function (d) {
      d.r = (d.center ? 8 : 5.5) * grow;
      placed.push({ x: d.x - d.r - 1, y: d.y - d.r - 1, w: (d.r + 1) * 2, h: (d.r + 1) * 2 });
    });
    var order = local.slice().sort(function (a, b) { return (b.center ? 1 : 0) - (a.center ? 1 : 0); });
    order.forEach(function (d) {
      var best = null, bestCost = Infinity;
      ['b', 't', 'r', 'l'].forEach(function (pos) {
        var rc = rectFor(d, pos);
        var cost = outOfBounds(rc);
        placed.forEach(function (pr) { cost += overlapArea(rc, pr); });
        if (cost < bestCost) { bestCost = cost; best = rc; }
      });
      d.lb = best;
      placed.push(best);
    });
  }

  function drawSvg(local, edges, maxW, W, H, opts) {
    var NS = 'http://www.w3.org/2000/svg';
    var grow = 1 + (opts.scale - 1) * 0.55; // 노드·오프셋은 캔버스보다 완만하게 확대
    placeLabels(local, W, H, opts);
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('class', 'pg-svg' + (opts.large ? ' pg-svg--lg' : ''));
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', '이 글과 연결된 글 그래프');

    edges.forEach(function (e) {
      var norm = e.w / maxW;
      var line = document.createElementNS(NS, 'line');
      line.setAttribute('x1', local[e.a].x); line.setAttribute('y1', local[e.a].y);
      line.setAttribute('x2', local[e.b].x); line.setAttribute('y2', local[e.b].y);
      line.setAttribute('class', 'pg-edge');
      line.setAttribute('stroke-width', ((1 + 1.4 * norm) * grow).toFixed(2));
      line.style.opacity = (0.4 + 0.35 * norm).toFixed(2);
      svg.appendChild(line);
    });

    local.forEach(function (d) {
      var g = document.createElementNS(NS, 'g');
      g.setAttribute('class', d.center ? 'pg-node pg-node--center' : 'pg-node');
      var circle = document.createElementNS(NS, 'circle');
      circle.setAttribute('cx', d.x); circle.setAttribute('cy', d.y);
      circle.setAttribute('r', d.r.toFixed(1));
      var label = document.createElementNS(NS, 'text');
      label.setAttribute('x', d.lb.tx.toFixed(1));
      label.setAttribute('y', d.lb.ty.toFixed(1));
      label.setAttribute('class', 'pg-label');
      label.setAttribute('text-anchor', d.lb.anchor);
      var t = d.node.label || '';
      label.textContent = t.length > opts.trunc ? t.slice(0, opts.trunc) + '…' : t;
      var title = document.createElementNS(NS, 'title');
      title.textContent = t;
      g.appendChild(title); g.appendChild(circle); g.appendChild(label);
      if (!d.center) {
        g.addEventListener('click', function () { location.href = d.node.url; });
      }
      svg.appendChild(g);
    });

    return svg;
  }

  // ── 데이터 로드 (미니·모달 공용, 1회 fetch) ──
  var dataPromise = null;
  function ensureGraph() {
    if (!dataPromise) {
      dataPromise = fetch('/knowledge-graph.json')
        .then(function (r) { return r.json(); })
        .then(function (data) { return buildLocalGraph(data.nodes || []); });
    }
    return dataPromise;
  }

  // ── 확대 모달 ──
  var modal = null;
  function buildModal() {
    if (modal) return modal;
    modal = document.createElement('div');
    modal.id = 'pg-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', '그래프 뷰 크게 보기');
    modal.innerHTML =
      '<div class="pg-modal__dialog">' +
        '<div class="pg-modal__header">' +
          '<span class="pg-modal__title"><i class="fas fa-project-diagram"></i> 그래프 뷰 — 이 글과 연결된 글</span>' +
          '<span class="pg-modal__actions">' +
            '<a href="/knowledge-graph/" class="pg-modal__full">전체 그래프 <i class="fas fa-external-link-alt"></i></a>' +
            '<button type="button" class="pg-modal__close" aria-label="닫기"><i class="fas fa-times"></i></button>' +
          '</span>' +
        '</div>' +
        '<div class="pg-modal__canvas"></div>' +
      '</div>';
    document.body.appendChild(modal);
    modal.addEventListener('click', function (e) {
      if (e.target === modal) closeModal();
    });
    modal.querySelector('.pg-modal__close').addEventListener('click', closeModal);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
    });
    return modal;
  }

  function openModal(g) {
    var m = buildModal();
    m.classList.add('open');
    document.body.classList.add('pg-modal-open');
    var canvasEl = m.querySelector('.pg-modal__canvas');
    canvasEl.innerHTML = '';
    var rect = canvasEl.getBoundingClientRect();
    var W = Math.round(rect.width) || 800;
    var H = Math.round(rect.height) || 540;
    var s = Math.max(1.4, Math.min(W, H) / 260);
    var opts = { trunc: 18, scale: s, large: true };
    var maxW = runLayout(g.local, g.edges, W, H, s, opts);
    canvasEl.appendChild(drawSvg(g.local, g.edges, maxW, W, H, opts));
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove('open');
    document.body.classList.remove('pg-modal-open');
  }

  var zoomBtn = document.getElementById('post-graph-zoom');
  if (zoomBtn) {
    zoomBtn.addEventListener('click', function () {
      ensureGraph().then(function (g) {
        if (g) openModal(g);
      }).catch(function () { /* 데이터 실패 시 무동작 (미니 쪽에서 위젯 숨김 처리) */ });
    });
  }

  // ── 미니 그래프 초기화 ──
  function init() {
    ensureGraph()
      .then(function (g) {
        if (!g) { root.style.display = 'none'; return; }
        var rect = canvas.getBoundingClientRect();
        var W = Math.round(rect.width) || 0;
        if (W < 180) W = 220; // 측정 실패·숨김 상태 fallback
        var opts = { trunc: 12, scale: 1, large: false };
        var maxW = runLayout(g.local, g.edges, W, MINI_H, 1, opts);
        canvas.appendChild(drawSvg(g.local, g.edges, maxW, W, MINI_H, opts));
      })
      .catch(function (e) {
        console.error('그래프 뷰 로드 실패:', e);
        root.style.display = 'none';
      });
  }

  // 초기 렌더를 방해하지 않도록 유휴 시간에 로드
  if ('requestIdleCallback' in window) {
    requestIdleCallback(init, { timeout: 2500 });
  } else {
    setTimeout(init, 800);
  }
})();
