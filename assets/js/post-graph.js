/* ==========================================================================
   포스트 미니 그래프 뷰 (Quartz 스타일 로컬 그래프)
   우측 사이드바 "On this page" 위에 현재 글 + 관련 글 top-8을 표시한다.
   데이터: /knowledge-graph.json (노드만). 엣지는 지식그래프 페이지와 동일한
   태그 IDF 가중 스코어링을 현재 글 기준으로 축소 계산 (D3 의존성 없음).
   가독성: 컨테이너 실측 폭으로 viewBox를 1:1 px 매핑(스케일 블러 방지),
   라벨 halo(paint-order stroke) + 상하 플립 충돌 회피.
   ========================================================================== */

(function () {
  var root = document.getElementById('post-graph');
  var canvas = document.getElementById('post-graph-canvas');
  if (!root || !canvas || !window.__currentPost) return;

  var MAX_NEIGHBORS = 8;   // 지식그래프 TOP_K와 동일
  var H = 240;             // 캔버스 높이(px)

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
  function layout(local, edges, W) {
    var cx = W / 2, cy = H / 2 - 8;
    var maxW = edges.reduce(function (m, e) { return Math.max(m, e.w); }, 0.01);
    var ring = Math.min(W, H) / 2 - 40;
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
          var f = 2600 / d2, dist = Math.sqrt(d2);
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
        var rest = 58 + (1 - e.w / maxW) * 30;
        var f = (dist - rest) * 0.03;
        var fx = (dx / dist) * f, fy = (dy / dist) * f;
        na.vx += fx; na.vy += fy;
        nb.vx -= fx; nb.vy -= fy;
      });
      // 중심 인력 + 적분
      local.forEach(function (d) {
        if (d.center) { d.x = cx; d.y = cy; d.vx = 0; d.vy = 0; return; }
        d.vx += (cx - d.x) * 0.01;
        d.vy += (cy - d.y) * 0.01;
        d.vx *= 0.85; d.vy *= 0.85;
        d.x = Math.max(18, Math.min(W - 18, d.x + d.vx));
        d.y = Math.max(20, Math.min(H - 34, d.y + d.vy));
      });
    }
    // 라벨 충돌 회피 — 가까운 라벨은 노드 위쪽으로 플립
    var nb2 = local.filter(function (d) { return !d.center; });
    nb2.sort(function (a, b) { return a.x - b.x; });
    for (var m = 0; m < nb2.length; m++) {
      for (var n2 = m + 1; n2 < nb2.length; n2++) {
        var ddx = Math.abs(nb2[n2].x - nb2[m].x);
        var ddy = Math.abs(nb2[n2].y - nb2[m].y);
        if (ddx < 78 && ddy < 15 && !nb2[m].flip && !nb2[n2].flip) nb2[n2].flip = true;
      }
    }
    return maxW;
  }

  function render(local, edges, maxW, W) {
    var NS = 'http://www.w3.org/2000/svg';
    var svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 ' + W + ' ' + H);
    svg.setAttribute('class', 'pg-svg');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', '이 글과 연결된 글 그래프');

    edges.forEach(function (e) {
      var norm = e.w / maxW;
      var line = document.createElementNS(NS, 'line');
      line.setAttribute('x1', local[e.a].x); line.setAttribute('y1', local[e.a].y);
      line.setAttribute('x2', local[e.b].x); line.setAttribute('y2', local[e.b].y);
      line.setAttribute('class', 'pg-edge');
      line.setAttribute('stroke-width', (1 + 1.4 * norm).toFixed(2));
      line.style.opacity = (0.4 + 0.35 * norm).toFixed(2);
      svg.appendChild(line);
    });

    local.forEach(function (d) {
      var g = document.createElementNS(NS, 'g');
      g.setAttribute('class', d.center ? 'pg-node pg-node--center' : 'pg-node');
      var circle = document.createElementNS(NS, 'circle');
      circle.setAttribute('cx', d.x); circle.setAttribute('cy', d.y);
      circle.setAttribute('r', d.center ? 8 : 5.5);
      var label = document.createElementNS(NS, 'text');
      label.setAttribute('x', d.x);
      label.setAttribute('y', d.center ? d.y + 20 : (d.flip ? d.y - 11 : d.y + 17));
      label.setAttribute('class', 'pg-label');
      label.setAttribute('text-anchor', 'middle');
      var t = d.node.label || '';
      label.textContent = t.length > 12 ? t.slice(0, 12) + '…' : t;
      var title = document.createElementNS(NS, 'title');
      title.textContent = t;
      g.appendChild(title); g.appendChild(circle); g.appendChild(label);
      if (!d.center) {
        g.addEventListener('click', function () { location.href = d.node.url; });
      }
      svg.appendChild(g);
    });

    canvas.appendChild(svg);
  }

  function init() {
    var rect = canvas.getBoundingClientRect();
    var W = Math.round(rect.width) || 0;
    if (W < 180) W = 220; // 측정 실패·숨김 상태 fallback

    fetch('/knowledge-graph.json')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var g = buildLocalGraph(data.nodes || []);
        if (!g) { root.style.display = 'none'; return; }
        var maxW = layout(g.local, g.edges, W);
        render(g.local, g.edges, maxW, W);
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
