---
layout: default
title: "프롬프트 라이브러리"
permalink: /prompts/
description: "교육 현장에서 바로 쓰는 큐레이션 AI 프롬프트. prompts.chat(CC0)의 프롬프트를 교사 실무에 맞춰 한국어로 번안해 카테고리·키워드로 탐색한다."
---

<style>
  /* ===== 프롬프트 라이브러리 — 사이트 테마(다크/라이트) 대응 스코프 스타일 ===== */
  #pl-app {
    --pl-card: #2c313d;
    --pl-card-hover: #333a48;
    --pl-border: rgba(255,255,255,0.11);
    --pl-border-strong: rgba(255,255,255,0.2);
    --pl-text: #eaeaea;
    --pl-muted: #9aa4b2;
    --pl-faint: #7c8593;
    --pl-accent: #2ec4cc;
    --pl-accent-ink: #14232b;
    --pl-accent-soft: rgba(46,196,204,0.14);
    --pl-accent-line: rgba(46,196,204,0.4);
    --pl-chip: rgba(255,255,255,0.055);
    --pl-panel: rgba(255,255,255,0.025);
    --pl-code: #1c2029;
    --pl-shadow: 0 6px 20px rgba(0,0,0,0.35);

    max-width: 1180px;
    margin: 0 auto;
    padding: 1.4em 1.4em 4em;
    color: var(--pl-text);
    font-family: -apple-system, "Pretendard", "Segoe UI", "Malgun Gothic", sans-serif;
    word-break: keep-all;
    overflow-wrap: break-word;
  }
  #pl-app [hidden] { display: none !important; }
  html[data-theme="light"] #pl-app {
    --pl-card: #ffffff;
    --pl-card-hover: #f7f9fb;
    --pl-border: #e4e8ee;
    --pl-border-strong: #cdd4de;
    --pl-text: #252a34;
    --pl-muted: #5a6472;
    --pl-faint: #838d9b;
    --pl-accent: #0090b0;
    --pl-accent-ink: #ffffff;
    --pl-accent-soft: rgba(0,120,200,0.08);
    --pl-accent-line: rgba(0,120,200,0.3);
    --pl-chip: #eef2f6;
    --pl-panel: #f7f9fb;
    --pl-code: #f4f6f9;
    --pl-shadow: 0 6px 20px rgba(30,40,60,0.09);
  }

  #pl-app .pl-hero { margin-bottom: 1.4em; }
  #pl-app .pl-hero h1 { font-size: 1.85em; margin: 0 0 .25em; line-height: 1.2; }
  #pl-app .pl-hero p { color: var(--pl-muted); margin: 0 0 .6em; font-size: .98em; }
  #pl-app .pl-cc0 {
    display: inline-flex; align-items: center; gap: .4em;
    font-size: .8em; color: var(--pl-faint);
    background: var(--pl-panel); border: 1px solid var(--pl-border);
    padding: .3em .7em; border-radius: 999px;
  }
  #pl-app .pl-cc0 a { color: var(--pl-accent); text-decoration: none; }
  #pl-app .pl-cc0 a:hover { text-decoration: underline; }

  #pl-app .pl-controls { margin: 1.2em 0 .4em; }
  #pl-app .pl-search {
    width: 100%; box-sizing: border-box;
    background: var(--pl-card); color: var(--pl-text);
    border: 1px solid var(--pl-border-strong); border-radius: 10px;
    padding: .7em .9em; font-size: 1em; margin-bottom: .9em;
  }
  #pl-app .pl-search::placeholder { color: var(--pl-faint); }
  #pl-app .pl-search:focus { outline: none; border-color: var(--pl-accent); }

  #pl-app .pl-pills { display: flex; flex-wrap: wrap; gap: .45em; margin-bottom: .5em; }
  #pl-app .pl-pill {
    cursor: pointer; user-select: none;
    background: var(--pl-chip); color: var(--pl-muted);
    border: 1px solid var(--pl-border); border-radius: 999px;
    padding: .38em .85em; font-size: .86em; transition: all .12s ease;
  }
  #pl-app .pl-pill:hover { border-color: var(--pl-accent-line); color: var(--pl-text); }
  #pl-app .pl-pill.is-on {
    background: var(--pl-accent); color: var(--pl-accent-ink);
    border-color: var(--pl-accent); font-weight: 600;
  }
  #pl-app .pl-pill .pl-ct { opacity: .7; font-size: .9em; margin-left: .25em; }

  #pl-app .pl-count { color: var(--pl-faint); font-size: .84em; margin: .3em 0 1em; }

  #pl-app .pl-grid {
    display: grid; gap: 1em;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
  #pl-app .pl-card {
    background: var(--pl-card); border: 1px solid var(--pl-border);
    border-radius: 14px; padding: 1.1em 1.15em; box-shadow: var(--pl-shadow);
    display: flex; flex-direction: column; transition: border-color .12s ease;
  }
  #pl-app .pl-card:hover { border-color: var(--pl-accent-line); }
  #pl-app .pl-cat {
    align-self: flex-start; font-size: .74em; font-weight: 600;
    color: var(--pl-accent); background: var(--pl-accent-soft);
    border: 1px solid var(--pl-accent-line); border-radius: 6px;
    padding: .18em .5em; margin-bottom: .55em;
  }
  #pl-app .pl-card h3 { font-size: 1.12em; margin: 0 0 .4em; line-height: 1.3; }
  #pl-app .pl-desc { color: var(--pl-muted); font-size: .92em; margin: 0 0 .7em; line-height: 1.55; }
  #pl-app .pl-tags { display: flex; flex-wrap: wrap; gap: .35em; margin-bottom: .85em; }
  #pl-app .pl-tag { font-size: .76em; color: var(--pl-faint); background: var(--pl-chip); border-radius: 5px; padding: .16em .45em; }

  #pl-app .pl-actions { display: flex; flex-wrap: wrap; gap: .5em; margin-top: auto; align-items: center; }
  #pl-app .pl-btn {
    cursor: pointer; font-size: .85em; font-family: inherit;
    border-radius: 8px; padding: .45em .8em; transition: all .12s ease;
    border: 1px solid var(--pl-accent); background: var(--pl-accent); color: var(--pl-accent-ink); font-weight: 600;
  }
  #pl-app .pl-btn:hover { filter: brightness(1.08); }
  #pl-app .pl-btn.pl-ghost { background: transparent; color: var(--pl-accent); }
  #pl-app .pl-btn.pl-ghost:hover { background: var(--pl-accent-soft); }
  #pl-app .pl-by { font-size: .78em; color: var(--pl-faint); margin-left: auto; }
  #pl-app .pl-by a { color: var(--pl-faint); text-decoration: none; }
  #pl-app .pl-by a:hover { color: var(--pl-accent); text-decoration: underline; }

  /* 복사되는 한글 프롬프트 — 읽기 좋은 본문 스타일(강조 테두리) */
  #pl-app .pl-ko {
    margin-top: .8em; background: var(--pl-accent-soft); border: 1px solid var(--pl-accent-line);
    border-radius: 8px; padding: .85em; font-size: .92em; color: var(--pl-text);
    line-height: 1.65; white-space: pre-wrap; word-break: break-word;
    max-height: 340px; overflow-y: auto;
  }
  #pl-app .pl-en {
    margin-top: .8em; background: var(--pl-code); border: 1px solid var(--pl-border);
    border-radius: 8px; padding: .8em; font-size: .82em; color: var(--pl-muted);
    white-space: pre-wrap; word-break: break-word; max-height: 260px; overflow-y: auto;
    font-family: "SFMono-Regular", "Consolas", "Menlo", monospace;
  }
  #pl-app .pl-empty { color: var(--pl-muted); text-align: center; padding: 3em 1em; }

  @media (max-width: 600px) {
    #pl-app .pl-grid { grid-template-columns: 1fr; }
    #pl-app .pl-hero h1 { font-size: 1.5em; }
  }
</style>

<div id="pl-app">
  <div class="pl-hero">
    <h1>프롬프트 라이브러리</h1>
    <p>수업 설계·평가·문서·소통에 바로 쓰는 큐레이션 AI 프롬프트. 카드를 복사해 챗GPT·Claude·Gemini에 붙여넣으면 된다.</p>
    <span class="pl-cc0">출처: <a href="https://prompts.chat/" target="_blank" rel="noopener">prompts.chat</a> · CC0 1.0 퍼블릭 도메인 · 교육 맥락으로 한국어 번안</span>
  </div>

  <div class="pl-controls">
    <input id="pl-search" class="pl-search" type="search" placeholder="제목·설명·프롬프트 내용으로 검색…" autocomplete="off">
    <div id="pl-pills" class="pl-pills"></div>
  </div>
  <div id="pl-count" class="pl-count"></div>
  <div id="pl-grid" class="pl-grid"></div>
</div>

{% raw %}
<script>
(function () {
  var app = document.getElementById('pl-app');
  if (!app) return;
  var searchEl = document.getElementById('pl-search');
  var pillsEl = document.getElementById('pl-pills');
  var gridEl = document.getElementById('pl-grid');
  var countEl = document.getElementById('pl-count');

  var DATA = [], CATS = [], activeCat = '전체', query = '';

  function esc(s) {
    return (s || '').replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function matches(p) {
    if (activeCat !== '전체' && p.category !== activeCat) return false;
    if (query) {
      var hay = (p.title_ko + ' ' + p.desc_ko + ' ' + p.prompt_ko + ' ' + (p.tags || []).join(' ')).toLowerCase();
      if (hay.indexOf(query) === -1) return false;
    }
    return true;
  }

  function renderPills() {
    var counts = { '전체': DATA.length };
    CATS.forEach(function (c) { counts[c] = 0; });
    DATA.forEach(function (p) { counts[p.category] = (counts[p.category] || 0) + 1; });
    var order = ['전체'].concat(CATS);
    pillsEl.innerHTML = order.map(function (c) {
      var on = c === activeCat ? ' is-on' : '';
      return '<span class="pl-pill' + on + '" data-cat="' + esc(c) + '">' + esc(c) +
        '<span class="pl-ct">' + (counts[c] || 0) + '</span></span>';
    }).join('');
    Array.prototype.forEach.call(pillsEl.querySelectorAll('.pl-pill'), function (el) {
      el.addEventListener('click', function () {
        activeCat = el.getAttribute('data-cat');
        renderPills(); renderGrid();
      });
    });
  }

  function cardHTML(p) {
    var tags = (p.tags || []).map(function (t) { return '<span class="pl-tag">#' + esc(t) + '</span>'; }).join('');
    var c = (p.contributor || '').trim();
    var by = (c && c.indexOf('@') === -1 && c.indexOf(' ') === -1) ? '<span class="pl-by">기여: <a href="https://github.com/' + esc(c) + '" target="_blank" rel="noopener">' + esc(c) + '</a></span>' : '';
    return '<div class="pl-card">' +
      '<span class="pl-cat">' + esc(p.category) + '</span>' +
      '<h3>' + esc(p.title_ko) + '</h3>' +
      '<p class="pl-desc">' + esc(p.desc_ko) + '</p>' +
      '<div class="pl-tags">' + tags + '</div>' +
      '<div class="pl-actions">' +
        '<button class="pl-btn" data-copy="' + esc(p.id) + '">프롬프트 복사</button>' +
        '<button class="pl-btn pl-ghost" data-ko="' + esc(p.id) + '">프롬프트 보기</button>' +
        '<button class="pl-btn pl-ghost" data-en="' + esc(p.id) + '">영어 원문</button>' +
        by +
      '</div>' +
      '<div class="pl-ko" id="ko-' + esc(p.id) + '" hidden>' + esc(p.prompt_ko) + '</div>' +
      '<pre class="pl-en" id="en-' + esc(p.id) + '" hidden>' + esc(p.prompt_en) + '</pre>' +
    '</div>';
  }

  function renderGrid() {
    var list = DATA.filter(matches);
    countEl.textContent = list.length + '개 프롬프트' + (activeCat !== '전체' ? ' · ' + activeCat : '') + (query ? ' · "' + query + '"' : '');
    if (!list.length) {
      gridEl.innerHTML = '<div class="pl-empty">조건에 맞는 프롬프트가 없다. 검색어나 카테고리를 바꿔보라.</div>';
      return;
    }
    gridEl.innerHTML = list.map(cardHTML).join('');
    var byId = {};
    DATA.forEach(function (p) { byId[p.id] = p; });

    Array.prototype.forEach.call(gridEl.querySelectorAll('[data-copy]'), function (btn) {
      btn.addEventListener('click', function () {
        var id = btn.getAttribute('data-copy');
        var p = byId[id];
        var txt = p.prompt_ko || p.prompt_en;
        // 복사한 내용을 바로 볼 수 있도록 한글 프롬프트를 자동으로 펼친다
        var koEl = document.getElementById('ko-' + id);
        var koBtn = gridEl.querySelector('[data-ko="' + id + '"]');
        var reveal = function () {
          if (koEl && koEl.hasAttribute('hidden')) {
            koEl.removeAttribute('hidden');
            if (koBtn) koBtn.textContent = '접기';
          }
        };
        var done = function () {
          reveal();
          btn.textContent = '복사됨 ✓';
          setTimeout(function () { btn.textContent = '프롬프트 복사'; }, 1400);
        };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(txt).then(done, function () { fallbackCopy(txt); done(); });
        } else { fallbackCopy(txt); done(); }
      });
    });
    Array.prototype.forEach.call(gridEl.querySelectorAll('[data-ko]'), function (btn) {
      btn.addEventListener('click', function () {
        var el = document.getElementById('ko-' + btn.getAttribute('data-ko'));
        var show = el.hasAttribute('hidden');
        if (show) { el.removeAttribute('hidden'); btn.textContent = '접기'; }
        else { el.setAttribute('hidden', ''); btn.textContent = '프롬프트 보기'; }
      });
    });
    Array.prototype.forEach.call(gridEl.querySelectorAll('[data-en]'), function (btn) {
      btn.addEventListener('click', function () {
        var pre = document.getElementById('en-' + btn.getAttribute('data-en'));
        var show = pre.hasAttribute('hidden');
        if (show) { pre.removeAttribute('hidden'); btn.textContent = '원문 닫기'; }
        else { pre.setAttribute('hidden', ''); btn.textContent = '영어 원문'; }
      });
    });
  }

  function fallbackCopy(txt) {
    var ta = document.createElement('textarea');
    ta.value = txt; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    document.body.removeChild(ta);
  }

  searchEl.addEventListener('input', function () {
    query = searchEl.value.trim().toLowerCase();
    renderGrid();
  });

  fetch('/assets/prompt-library.json')
    .then(function (r) { return r.json(); })
    .then(function (doc) {
      DATA = doc.prompts || [];
      CATS = (doc.meta && doc.meta.categories) || [];
      renderPills();
      renderGrid();
    })
    .catch(function () {
      gridEl.innerHTML = '<div class="pl-empty">프롬프트 데이터를 불러오지 못했다.</div>';
    });
})();
</script>
{% endraw %}
