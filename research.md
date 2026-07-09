---
layout: default
title: "리서치 허브"
permalink: /research/
description: "AI와 교육 논문리뷰를 한곳에서 탐색하는 리서치 허브. 태그·연도·키워드로 걸러 주요 발견과 시사점을 바로 읽는다."
---

<style>
  /* ===== 리서치 허브 — 사이트 테마(다크/라이트) 대응 스코프 스타일 ===== */
  #rh-app {
    /* 다크(기본 스킨) 토큰 */
    --rh-card: #2c313d;
    --rh-card-hover: #333a48;
    --rh-border: rgba(255,255,255,0.11);
    --rh-border-strong: rgba(255,255,255,0.2);
    --rh-text: #eaeaea;
    --rh-muted: #9aa4b2;
    --rh-faint: #7c8593;
    --rh-accent: #2ec4cc;
    --rh-accent-ink: #1a2a2b;
    --rh-accent-soft: rgba(46,196,204,0.14);
    --rh-accent-line: rgba(46,196,204,0.4);
    --rh-chip: rgba(255,255,255,0.055);
    --rh-panel: rgba(255,255,255,0.025);
    --rh-shadow: 0 6px 20px rgba(0,0,0,0.35);

    max-width: 1180px;
    margin: 0 auto;
    padding: 1.6em 1.4em 4em;
    color: var(--rh-text);
    font-family: -apple-system, "Pretendard", "Segoe UI", "Malgun Gothic", sans-serif;
    /* 한국어 어절 단위 줄바꿈 — 문장이 단어 중간에서 끊기지 않게. 긴 URL 등은 break-word로 방어 */
    word-break: keep-all;
    overflow-wrap: break-word;
  }
  /* hidden 속성 강제 — #rh-app .rh-card { display: flex }(1,1,0)가 UA의
     [hidden]{display:none}을 이겨 필터가 무력화되는 것을 차단 */
  #rh-app [hidden] { display: none !important; }
  html[data-theme="light"] #rh-app {
    --rh-card: #ffffff;
    --rh-card-hover: #f7f9fb;
    --rh-border: #e4e8ee;
    --rh-border-strong: #cdd4de;
    --rh-text: #252a34;
    --rh-muted: #5a6472;
    --rh-faint: #838d9b;
    --rh-accent: #0078c8;
    --rh-accent-ink: #ffffff;
    --rh-accent-soft: rgba(0,120,200,0.08);
    --rh-accent-line: rgba(0,120,200,0.35);
    --rh-chip: #eef2f6;
    --rh-panel: #f7f9fb;
    --rh-shadow: 0 6px 20px rgba(30,40,60,0.09);
  }

  /* ── Hero ── */
  #rh-app .rh-hero { position: relative; margin-bottom: 1.6em; display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
  #rh-app .rh-hero::before {
    content: ''; position: absolute; top: -70px; right: -30px;
    width: 380px; height: 240px; border-radius: 50%;
    background: radial-gradient(closest-side, var(--rh-accent-soft), transparent 72%);
    pointer-events: none;
  }
  #rh-app .rh-hero-text { flex: 1 1 30em; }
  #rh-app .rh-eyebrow {
    display: flex; align-items: center; gap: 10px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--rh-accent); margin: 0 0 0.6em;
  }
  #rh-app .rh-eyebrow::after {
    content: ''; height: 1px; width: 42px;
    background: linear-gradient(90deg, var(--rh-accent-line), transparent);
  }
  #rh-app .rh-hero h1 {
    font-size: 2.05rem; font-weight: 800; margin: 0 0 0.35em;
    letter-spacing: -0.015em; line-height: 1.22; color: var(--rh-text);
    text-wrap: balance;
  }
  @supports ((-webkit-background-clip: text) or (background-clip: text)) {
    #rh-app .rh-hero h1 {
      background: linear-gradient(120deg, var(--rh-text) 58%, var(--rh-accent) 100%);
      -webkit-background-clip: text; background-clip: text;
      -webkit-text-fill-color: transparent; color: transparent;
    }
  }
  #rh-app .rh-sub { font-size: 0.98rem; color: var(--rh-muted); margin: 0; line-height: 1.65; max-width: 46em; text-wrap: pretty; }
  #rh-app .rh-sub b { color: var(--rh-accent); font-weight: 700; }
  #rh-app .rh-stats { display: flex; gap: 22px; margin-top: 1.15em; flex-wrap: wrap; }
  #rh-app .rh-stat { display: flex; flex-direction: column; gap: 2px; padding-left: 12px; border-left: 2px solid var(--rh-accent-line); }
  #rh-app .rh-stat b {
    font-size: 1.18rem; font-weight: 800; color: var(--rh-text);
    font-variant-numeric: tabular-nums; letter-spacing: -0.01em; line-height: 1.15;
  }
  #rh-app .rh-stat span { font-size: 0.72rem; color: var(--rh-faint); letter-spacing: 0.02em; }
  #rh-app .rh-ask-cta {
    display: none; align-items: center; gap: 7px; align-self: center;
    background: var(--rh-accent); color: var(--rh-accent-ink);
    font-size: 0.9rem; font-weight: 700; padding: 0.65em 1.1em;
    border-radius: 10px; text-decoration: none; white-space: nowrap;
    opacity: 0; transition: opacity .35s ease, filter .16s;
  }
  #rh-app .rh-ask-cta:hover { filter: brightness(1.08); color: var(--rh-accent-ink); }

  /* ── Toolbar ── */
  #rh-app .rh-toolbar {
    display: flex; gap: 10px; flex-wrap: wrap; align-items: center;
    margin: 1.4em 0 0.9em;
  }
  #rh-app .rh-search-wrap { position: relative; flex: 1 1 240px; min-width: 180px; }
  #rh-search {
    width: 100%; box-sizing: border-box;
    background: var(--rh-card); border: 1px solid var(--rh-border-strong);
    border-radius: 9px; color: var(--rh-text);
    font-size: 0.95rem; padding: 0.62em 0.9em 0.62em 2.2em; outline: none;
    transition: border-color .18s, box-shadow .18s;
  }
  #rh-search::placeholder { color: var(--rh-faint); }
  #rh-search:focus { border-color: var(--rh-accent); box-shadow: 0 0 0 3px var(--rh-accent-soft); }
  #rh-app .rh-search-ico {
    position: absolute; left: 0.75em; top: 50%; transform: translateY(-50%);
    color: var(--rh-faint); pointer-events: none; font-size: 0.95rem;
  }
  #rh-ai-toggle {
    display: none; align-items: center; gap: 6px;
    background: var(--rh-chip); border: 1px solid var(--rh-border-strong);
    border-radius: 9px; color: var(--rh-muted); font-size: 0.85rem; font-weight: 600;
    padding: 0.55em 0.9em; cursor: pointer; font-family: inherit;
    opacity: 0; transition: opacity .35s ease, background .16s, color .16s, border-color .16s;
    white-space: nowrap;
  }
  #rh-ai-toggle:hover { color: var(--rh-text); border-color: var(--rh-accent); }
  #rh-ai-toggle.on {
    background: var(--rh-accent); color: var(--rh-accent-ink); border-color: var(--rh-accent);
  }
  #rh-app .rh-ai-note {
    display: none; font-size: 0.8rem; color: var(--rh-accent);
    margin: 0.2em 0 0; align-items: center; gap: 6px;
  }
  #rh-app .rh-ai-note.show { display: flex; }
  #rh-app .rh-ai-spin {
    width: 12px; height: 12px; border: 2px solid var(--rh-accent-soft);
    border-top-color: var(--rh-accent); border-radius: 50%;
    animation: rh-spin 0.8s linear infinite; display: inline-block;
  }
  @keyframes rh-spin { to { transform: rotate(360deg); } }
  #rh-sort {
    background: var(--rh-card); border: 1px solid var(--rh-border-strong);
    border-radius: 9px; color: var(--rh-text); font-size: 0.9rem;
    padding: 0.62em 0.7em; outline: none; cursor: pointer;
  }
  #rh-sort:focus { border-color: var(--rh-accent); }
  #rh-app .rh-years { display: inline-flex; gap: 4px; background: var(--rh-chip); padding: 3px; border-radius: 9px; }
  #rh-app .rh-year-btn {
    background: none; border: none; color: var(--rh-muted);
    font-size: 0.85rem; padding: 0.4em 0.8em; border-radius: 7px; cursor: pointer;
    transition: all .15s; font-family: inherit;
  }
  #rh-app .rh-year-btn:hover { color: var(--rh-text); }
  #rh-app .rh-year-btn.active { background: var(--rh-accent); color: var(--rh-accent-ink); font-weight: 600; }

  /* ── Tag bar ── */
  #rh-app .rh-tagbar { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 0.6em; align-items: center; }
  #rh-app .rh-tag-btn {
    background: var(--rh-chip); border: 1px solid transparent;
    color: var(--rh-muted); font-size: 0.82rem; padding: 0.32em 0.7em;
    border-radius: 999px; cursor: pointer; transition: all .15s;
    font-family: inherit; white-space: nowrap;
  }
  #rh-app .rh-tag-btn:hover { color: var(--rh-text); border-color: var(--rh-border-strong); }
  #rh-app .rh-tag-btn.active {
    background: var(--rh-accent); color: var(--rh-accent-ink);
    border-color: var(--rh-accent); font-weight: 600;
  }
  #rh-app .rh-tag-btn .rh-tag-n { opacity: 0.6; font-size: 0.88em; margin-left: 3px; }
  #rh-app .rh-tag-more {
    background: none; border: none; color: var(--rh-accent);
    font-size: 0.82rem; cursor: pointer; padding: 0.32em 0.5em; font-family: inherit;
  }

  /* ── Status row ── */
  #rh-app .rh-status {
    display: flex; align-items: center; gap: 12px;
    margin: 0.4em 0 1.1em; font-size: 0.88rem; color: var(--rh-muted);
    border-top: 1px solid var(--rh-border); padding-top: 0.9em;
  }
  #rh-count b { color: var(--rh-text); font-weight: 700; }
  #rh-clear {
    background: none; border: 1px solid var(--rh-border-strong); color: var(--rh-muted);
    font-size: 0.8rem; padding: 0.3em 0.7em; border-radius: 7px; cursor: pointer;
    font-family: inherit; transition: all .15s;
  }
  #rh-clear:hover { color: var(--rh-text); border-color: var(--rh-accent); }

  /* ── Grid ── */
  #rh-app .rh-grid {
    display: grid; gap: 14px;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  }
  #rh-app .rh-card {
    position: relative;
    background: var(--rh-card); border: 1px solid var(--rh-border);
    border-radius: 13px; overflow: hidden; transition: border-color .18s, box-shadow .18s, transform .18s;
    display: flex; flex-direction: column;
  }
  #rh-app .rh-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--rh-accent) 0%, transparent 75%);
    opacity: 0; transition: opacity .18s; pointer-events: none;
  }
  #rh-app .rh-card:hover { border-color: var(--rh-border-strong); box-shadow: var(--rh-shadow); transform: translateY(-2px); }
  #rh-app .rh-card:hover::before, #rh-app .rh-card--open::before { opacity: 1; }
  #rh-app .rh-card--open { border-color: var(--rh-accent-line); box-shadow: var(--rh-shadow); }
  #rh-app .rh-card--open:hover { transform: none; } /* 펼친 카드는 읽는 중 — 들썩임 방지 */

  #rh-app .rh-card-head { padding: 15px 16px; cursor: pointer; }
  #rh-app .rh-card-head:focus-visible { outline: 2px solid var(--rh-accent); outline-offset: -2px; }
  #rh-app .rh-card-meta {
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    font-size: 0.74rem; color: var(--rh-faint); margin-bottom: 7px;
  }
  #rh-app .rh-card-date { font-variant-numeric: tabular-nums; }
  #rh-app .rh-card-src {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.03em;
    padding: 1px 6px; border-radius: 4px;
    background: var(--rh-accent-soft); color: var(--rh-accent);
  }
  #rh-app .rh-card-fmt {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.03em;
    padding: 1px 6px; border-radius: 4px; margin-left: 4px;
    background: var(--rh-chip); color: var(--rh-faint);
    border: 1px solid var(--rh-border);
  }
  #rh-app .rh-card-title {
    font-size: 1.02rem; font-weight: 700; line-height: 1.4; margin: 0 0 8px;
    color: var(--rh-text); letter-spacing: -0.005em; transition: color .15s;
  }
  #rh-app .rh-card-head:hover .rh-card-title { color: var(--rh-accent); }
  #rh-app .rh-card-summary {
    font-size: 0.87rem; color: var(--rh-muted); line-height: 1.62; margin: 0 0 11px;
    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
  }
  #rh-app .rh-card-tags { display: flex; flex-wrap: wrap; gap: 5px; }
  #rh-app .rh-mini-tag {
    font-size: 0.72rem; color: var(--rh-faint);
    background: var(--rh-chip); padding: 1px 8px; border-radius: 999px;
    cursor: pointer; transition: color .15s;
  }
  #rh-app .rh-mini-tag:hover { color: var(--rh-accent); }
  #rh-app .rh-mini-tag.on { color: var(--rh-accent); font-weight: 600; }
  #rh-app .rh-card-expand {
    margin-top: 11px; font-size: 0.8rem; color: var(--rh-accent);
    display: inline-flex; align-items: center; gap: 4px; font-weight: 600;
  }
  #rh-app .rh-card-expand .rh-chev { transition: transform .2s; display: inline-block; }
  #rh-app .rh-card--open .rh-chev { transform: rotate(180deg); }

  /* ── Card body (detail) ── */
  #rh-app .rh-card-body { display: none; padding: 0 16px 16px; }
  #rh-app .rh-card--open .rh-card-body { display: block; }
  #rh-app .rh-sec { border-top: 1px solid var(--rh-border); padding-top: 13px; margin-top: 13px; }
  #rh-app .rh-sec:first-child { border-top: none; padding-top: 4px; margin-top: 0; }
  #rh-app .rh-sec-label {
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.05em;
    color: var(--rh-accent); text-transform: uppercase; margin: 0 0 7px;
  }
  #rh-app .rh-sec-body { font-size: 0.87rem; color: var(--rh-text); line-height: 1.7; }
  #rh-app .rh-sec-body p { margin: 0 0 0.6em; }
  #rh-app .rh-sec-body ul { margin: 0.2em 0 0.7em; padding-left: 1.2em; }
  #rh-app .rh-sec-body li { margin-bottom: 0.4em; }
  #rh-app .rh-sec-body strong { color: var(--rh-text); font-weight: 700; }
  #rh-app .rh-sec-body .rh-sub-h { font-size: 0.85rem; font-weight: 700; color: var(--rh-text); margin: 0.7em 0 0.3em; }
  #rh-app .rh-sec-body .rh-quote {
    border-left: 2px solid var(--rh-accent-line); padding-left: 0.8em;
    color: var(--rh-muted); font-style: italic; margin: 0 0 0.6em;
  }
  #rh-app .rh-sec-body a { color: var(--rh-accent); text-decoration: underline; }
  #rh-app .rh-tbl-wrap { overflow-x: auto; margin: 0.4em 0 0.8em; -webkit-overflow-scrolling: touch; }
  #rh-app .rh-tbl { border-collapse: collapse; font-size: 0.8rem; min-width: 100%; }
  #rh-app .rh-tbl th, #rh-app .rh-tbl td {
    border: 1px solid var(--rh-border); padding: 6px 10px; text-align: left;
    vertical-align: top; line-height: 1.5;
  }
  #rh-app .rh-tbl th { background: var(--rh-accent-soft); color: var(--rh-text); font-weight: 700; white-space: nowrap; }
  #rh-app .rh-tbl td { color: var(--rh-muted); min-width: 7em; }

  #rh-app .rh-source { background: var(--rh-panel); border-radius: 9px; padding: 11px 13px; margin-top: 14px; }
  #rh-app .rh-source-cite { font-size: 0.8rem; color: var(--rh-muted); line-height: 1.55; margin: 0 0 9px; white-space: pre-line; }
  #rh-app .rh-actions { display: flex; flex-wrap: wrap; gap: 8px; }
  #rh-app .rh-btn {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 0.82rem; font-weight: 600; padding: 0.45em 0.9em; border-radius: 8px;
    text-decoration: none; transition: all .16s; cursor: pointer; border: 1px solid transparent;
  }
  #rh-app .rh-btn-primary { background: var(--rh-accent); color: var(--rh-accent-ink); }
  #rh-app .rh-btn-primary:hover { filter: brightness(1.08); }
  #rh-app .rh-btn-ghost { background: none; border-color: var(--rh-border-strong); color: var(--rh-muted); }
  #rh-app .rh-btn-ghost:hover { color: var(--rh-text); border-color: var(--rh-accent); }

  /* ── Empty / loading ── */
  #rh-app .rh-empty, #rh-app .rh-loading { text-align: center; color: var(--rh-faint); padding: 3.5em 1em; font-size: 0.95rem; }

  /* ── Mobile ── */
  @media (max-width: 600px) {
    #rh-app { padding: 1em 0.9em 3em; }
    #rh-app .rh-hero { gap: 10px; margin-bottom: 1.2em; }
    #rh-app .rh-hero::before { top: -50px; right: -60px; width: 260px; height: 180px; }
    #rh-app .rh-hero h1 { font-size: 1.5rem; }
    #rh-app .rh-sub { font-size: 0.92rem; }
    #rh-app .rh-stats { gap: 14px; margin-top: 0.95em; }
    #rh-app .rh-stat { padding-left: 10px; }
    #rh-app .rh-stat b { font-size: 1.05rem; }
    #rh-app .rh-ask-cta { width: 100%; justify-content: center; padding: 0.75em 1em; }
    #rh-app .rh-grid { grid-template-columns: 1fr; gap: 11px; }
    #rh-app .rh-toolbar { gap: 8px; margin-top: 1.1em; }
    #rh-app .rh-search-wrap { flex-basis: 100%; }
    /* iOS Safari는 입력 폰트가 16px 미만이면 포커스 시 강제 줌 */
    #rh-search, #rh-sort { font-size: 16px; }
    #rh-ai-toggle { padding: 0.5em 0.8em; }
    #rh-app .rh-tag-btn { font-size: 0.8rem; padding: 0.38em 0.75em; }
    /* 태그바: 접힌 상태는 한 줄 가로 스크롤 스트립 (화면 절약), 전체 펼침은 줄바꿈 유지 */
    #rh-app .rh-tagbar:not(.rh-tagbar--all) {
      flex-wrap: nowrap; overflow-x: auto; -webkit-overflow-scrolling: touch;
      scrollbar-width: none; padding-bottom: 3px;
      margin-left: -0.9em; margin-right: -0.9em; padding-left: 0.9em; padding-right: 0.9em;
    }
    #rh-app .rh-tagbar:not(.rh-tagbar--all)::-webkit-scrollbar { display: none; }
    #rh-app .rh-card-head { padding: 13px 14px; }
    #rh-app .rh-card-title { font-size: 0.98rem; }
    #rh-app .rh-card-body { padding: 0 14px 14px; }
    #rh-app .rh-btn { padding: 0.55em 1em; }
    #rh-app .rh-actions { gap: 7px; }
    #rh-app .rh-actions .rh-btn { flex: 1 1 auto; justify-content: center; }
  }
  @media (prefers-reduced-motion: reduce) {
    #rh-app .rh-card, #rh-app .rh-tag-btn, #rh-app .rh-year-btn, #rh-app .rh-btn, #rh-app .rh-chev, #rh-app .rh-card-title { transition: none; }
    #rh-app .rh-card:hover { transform: none; }
  }
</style>

<div id="rh-app">
  <header class="rh-hero">
    <div class="rh-hero-text">
      <p class="rh-eyebrow">Dot Connector &#183; Research</p>
      <h1>AI · 교육 리서치 허브</h1>
      <p class="rh-sub">AI와 교육을 다룬 논문 리뷰·아티클 <b id="rh-total">…</b>편을 한곳에 모았다. 태그·연도·키워드로 걸러 <b>주요 발견</b>과 <b>교육적 시사점</b>을 원문까지 가지 않고 바로 읽는다.</p>
      <div class="rh-stats" id="rh-stats" hidden>
        <div class="rh-stat"><b id="rh-stat-count">&#8230;</b><span>논문리뷰</span></div>
        <div class="rh-stat"><b id="rh-stat-src">&#8230;</b><span>원문 링크</span></div>
        <div class="rh-stat"><b id="rh-stat-tags">&#8230;</b><span>태그</span></div>
        <div class="rh-stat"><b id="rh-stat-years">&#8230;</b><span>연도 범위</span></div>
      </div>
    </div>
    <a class="rh-ask-cta" id="rh-ask-cta" href="/ask/">&#128172; AI에게 묻기</a>
  </header>

  <div class="rh-toolbar">
    <div class="rh-search-wrap">
      <span class="rh-search-ico" aria-hidden="true">&#128269;</span>
      <input id="rh-search" type="search" placeholder="제목·발견·태그 검색…" aria-label="논문리뷰 검색" autocomplete="off">
    </div>
    <button id="rh-ai-toggle" aria-pressed="false" title="의미 기반 검색 — 키워드가 달라도 관련 연구를 찾는다">&#10024; AI 검색</button>
    <div class="rh-years" id="rh-years" role="group" aria-label="연도 필터"></div>
    <select id="rh-sort" aria-label="정렬 기준">
      <option value="new">최신순</option>
      <option value="old">오래된순</option>
      <option value="title">제목순</option>
    </select>
  </div>
  <p class="rh-ai-note" id="rh-ai-note"></p>

  <div class="rh-tagbar" id="rh-tagbar" role="group" aria-label="태그 필터"></div>

  <div class="rh-status">
    <span id="rh-count" aria-live="polite"></span>
    <button id="rh-clear" hidden>필터 초기화</button>
  </div>

  <div id="rh-grid" class="rh-grid" aria-live="polite"></div>
  <div id="rh-empty" class="rh-empty" hidden>조건에 맞는 논문리뷰가 없다. 필터를 완화해 보라.</div>
  <div id="rh-loading" class="rh-loading">리서치 데이터를 불러오는 중…</div>
</div>

<script>
{% raw %}
(function () {
  'use strict';

  // AI 검색/질의응답 API (research-ask Vercel 배포 URL — 미배포면 AI 기능 자동 숨김)
  var ASK_API = 'https://dotconnector-ask.vercel.app';
  // gemini-embedding은 무관 질의도 유사도 0.5~0.6이 나온다 → top1 게이트 + 상대 컷으로 판별
  var AI_TOP_GATE = 0.62;     // 최고 유사도가 이 미만이면 관련 없음 처리
  var AI_REL_CUT = 0.08;      // top1 대비 이 이상 떨어지면 제외
  var AI_TOP = 15;            // 시맨틱 검색 최대 표시 수
  // 태그바 기본 노출 개수 — 모바일은 화면을 덜 차지하게 축소
  var TOP_TAGS = (window.innerWidth || 1024) < 600 ? 12 : 24;
  var app = document.getElementById('rh-app');
  var gridEl = document.getElementById('rh-grid');
  var emptyEl = document.getElementById('rh-empty');
  var loadingEl = document.getElementById('rh-loading');
  var searchEl = document.getElementById('rh-search');
  var sortEl = document.getElementById('rh-sort');
  var yearsEl = document.getElementById('rh-years');
  var tagbarEl = document.getElementById('rh-tagbar');
  var countEl = document.getElementById('rh-count');
  var clearEl = document.getElementById('rh-clear');
  var totalEl = document.getElementById('rh-total');

  var state = { q: '', tags: new Set(), year: 'all', sort: 'new', aiMode: false, aiRank: null };
  var cards = [];             // { post, el, body, search, built }
  var showAllTags = false;
  var META = null;
  var aiToggle = document.getElementById('rh-ai-toggle');
  var aiNote = document.getElementById('rh-ai-note');
  var embIndex = null;        // Map<postId, Float32Array> — 첫 AI 검색 때 lazy load

  // display:none → 보이기 전환은 opacity transition이 안 먹으므로 display를 먼저 켜고
  // 한 프레임 뒤에 opacity를 올려 부드럽게 나타나게 한다 (콜드스타트로 늦게 뜨더라도 눈에 띄게)
  function revealAiEl(el) {
    el.style.display = 'inline-flex';
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { el.style.opacity = '1'; });
    });
  }

  // 주인장 접근 키 + 방문자 본인 Gemini 키 — /ask/ 페이지에서 입력하면 같은 localStorage를 공유
  function keyHeaders(extra) {
    var h = extra || {};
    try {
      var k = localStorage.getItem('dc_ask_key');
      if (k) h['X-Ask-Key'] = k;
      var g = localStorage.getItem('dc_gemini_key');
      if (g) h['X-Gemini-Key'] = g;
    } catch (e) {}
    return h;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  // ── 마크다운 라이트 렌더: 볼드·불릿·소제목(####)·인용(>)·표·링크 ──
  function mdLite(raw) {
    if (!raw) return '';
    var lines = raw.split('\n');
    var out = [], listOpen = false;
    function inline(s) {
      return esc(s)
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/\[(.+?)\]\((https?:\/\/[^\s)]+)\)/g,
          '<a href="$2" target="_blank" rel="noopener">$1</a>');
    }
    function closeList() { if (listOpen) { out.push('</ul>'); listOpen = false; } }
    function cells(l) {
      return l.trim().replace(/^\|/, '').replace(/\|\s*$/, '').split('|').map(function (c) { return c.trim(); });
    }
    function isSep(l) { return l.indexOf('-') !== -1 && /^\|?[\s:|-]+\|?$/.test(l.trim()); }
    function renderTable(block) {
      var header = null, start = 0;
      if (block.length >= 2 && isSep(block[1])) { header = cells(block[0]); start = 2; }
      var body = '';
      for (var r = start; r < block.length; r++) {
        if (isSep(block[r])) continue;
        body += '<tr>' + cells(block[r]).map(function (c) { return '<td>' + inline(c) + '</td>'; }).join('') + '</tr>';
      }
      var head = header ? '<thead><tr>' + header.map(function (c) { return '<th>' + inline(c) + '</th>'; }).join('') + '</tr></thead>' : '';
      return '<div class="rh-tbl-wrap"><table class="rh-tbl">' + head + '<tbody>' + body + '</tbody></table></div>';
    }
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!line) { closeList(); continue; }
      if (line.charAt(0) === '|') {                       // 표 블록: 연속 | 라인 수집
        closeList();
        var block = [];
        while (i < lines.length && lines[i].trim().charAt(0) === '|') { block.push(lines[i].trim()); i++; }
        i--;
        out.push(renderTable(block));
        continue;
      }
      var mh = line.match(/^#{3,4}\s+(.+)$/);
      if (mh) { closeList(); out.push('<div class="rh-sub-h">' + inline(mh[1]) + '</div>'); continue; }
      var ml = line.match(/^[*\-]\s+(.+)$/);
      if (ml) { if (!listOpen) { out.push('<ul>'); listOpen = true; } out.push('<li>' + inline(ml[1]) + '</li>'); continue; }
      if (line.charAt(0) === '>') { closeList(); out.push('<p class="rh-quote">' + inline(line.replace(/^>\s?/, '')) + '</p>'); continue; }
      closeList();
      out.push('<p>' + inline(line) + '</p>');
    }
    closeList();
    return out.join('');
  }

  // sections는 [{key, label, body}] 배열 — structured(고정 6섹션)와 article(자유 헤딩) 공용
  function buildDetail(post) {
    var html = '';
    var secs = post.sections || [];
    for (var i = 0; i < secs.length; i++) {
      if (!secs[i].body) continue;
      html += '<div class="rh-sec"><p class="rh-sec-label">' + esc(secs[i].label) +
        '</p><div class="rh-sec-body">' + mdLite(secs[i].body) + '</div></div>';
    }
    var src = post.source || {};
    var srcInner = '';
    if (src.citation) srcInner += '<p class="rh-source-cite">' + esc(src.citation) + '</p>';
    var acts = '';
    if (src.link) {
      var lbl = src.arxiv_id ? 'arXiv 원문' : (src.doi ? 'DOI 원문' : '원문 보기');
      acts += '<a class="rh-btn rh-btn-primary" href="' + esc(src.link) + '" target="_blank" rel="noopener">' + lbl + ' &#8599;</a>';
    }
    acts += '<a class="rh-btn rh-btn-ghost" href="' + esc(post.url) + '">블로그에서 읽기 &#8594;</a>';
    srcInner += '<div class="rh-actions">' + acts + '</div>';
    html += '<div class="rh-source">' + srcInner + '</div>';
    return html;
  }

  function buildCard(post) {
    var el = document.createElement('article');
    el.className = 'rh-card';

    var head = document.createElement('div');
    head.className = 'rh-card-head';
    head.setAttribute('role', 'button');
    head.setAttribute('tabindex', '0');
    head.setAttribute('aria-expanded', 'false');

    var srcBadge = '';
    var s = post.source || {};
    if (s.arxiv_id) srcBadge = '<span class="rh-card-src">arXiv</span>';
    else if (s.doi) srcBadge = '<span class="rh-card-src">DOI</span>';
    if (post.format === 'article') srcBadge += '<span class="rh-card-fmt">아티클</span>';

    var cats = (post.categories || []).slice(0, 2).join(' · ');
    var tagsHtml = (post.tags || []).slice(0, 5).map(function (t) {
      return '<span class="rh-mini-tag" data-tag="' + esc(t) + '">' + esc(t) + '</span>';
    }).join('');

    head.innerHTML =
      '<div class="rh-card-meta">' +
        '<span class="rh-card-date">' + esc(post.date) + '</span>' +
        (cats ? '<span>· ' + esc(cats) + '</span>' : '') +
        srcBadge +
      '</div>' +
      '<h2 class="rh-card-title">' + esc(post.title) + '</h2>' +
      '<p class="rh-card-summary">' + esc(post.summary) + '</p>' +
      '<div class="rh-card-tags">' + tagsHtml + '</div>' +
      '<span class="rh-card-expand"><span class="rh-chev">&#9662;</span> 자세히 보기</span>';

    var body = document.createElement('div');
    body.className = 'rh-card-body';

    el.appendChild(head);
    el.appendChild(body);

    var rec = { post: post, el: el, head: head, body: body, built: false };

    function toggle() {
      var open = el.classList.toggle('rh-card--open');
      head.setAttribute('aria-expanded', open ? 'true' : 'false');
      var lbl = head.querySelector('.rh-card-expand');
      if (open) {
        if (!rec.built) { body.innerHTML = buildDetail(post); rec.built = true; }
        lbl.innerHTML = '<span class="rh-chev">&#9662;</span> 접기';
      } else {
        lbl.innerHTML = '<span class="rh-chev">&#9662;</span> 자세히 보기';
      }
    }
    head.addEventListener('click', function (ev) {
      if (ev.target.classList.contains('rh-mini-tag')) return; // 태그 클릭은 필터
      toggle();
    });
    head.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); toggle(); }
    });
    // 카드 내 미니 태그 클릭 → 해당 태그 필터 토글
    head.querySelectorAll('.rh-mini-tag').forEach(function (mt) {
      mt.addEventListener('click', function (ev) {
        ev.stopPropagation();
        toggleTag(mt.getAttribute('data-tag'));
      });
    });

    rec.search = (post.title + ' ' + post.summary + ' ' + (post.tags || []).join(' ') + ' ' +
      (post.sections || []).map(function (s) { return s.label + ' ' + s.body; }).join(' ')
    ).toLowerCase();
    return rec;
  }

  // ── 필터 적용 ──
  function applyFilters() {
    var q = state.q, tags = state.tags, year = state.year, aiRank = state.aiRank;
    var visible = [];
    for (var i = 0; i < cards.length; i++) {
      var c = cards[i], p = c.post, ok = true;
      if (year !== 'all' && p.year !== year) ok = false;
      if (ok && tags.size) {
        var pt = p.tags || [];
        tags.forEach(function (t) { if (pt.indexOf(t) === -1) ok = false; });
      }
      if (ok) {
        if (aiRank) { if (!aiRank.has(p.id)) ok = false; }        // AI 모드: 의미 유사도 기준
        else if (q && c.search.indexOf(q) === -1) ok = false;      // 일반 모드: 키워드 매칭
      }
      c.el.hidden = !ok;
      if (ok) visible.push(c);
    }
    // 정렬 → DOM 재배치 (요소 재사용, 확장 상태 유지). AI 결과는 유사도순 우선.
    visible.sort(function (a, b) {
      if (aiRank) return aiRank.get(b.post.id) - aiRank.get(a.post.id);
      if (state.sort === 'title') return a.post.title.localeCompare(b.post.title, 'ko');
      if (state.sort === 'old') return a.post.date < b.post.date ? -1 : (a.post.date > b.post.date ? 1 : 0);
      return a.post.date > b.post.date ? -1 : (a.post.date < b.post.date ? 1 : 0);
    });
    var frag = document.createDocumentFragment();
    visible.forEach(function (c) { frag.appendChild(c.el); });
    gridEl.appendChild(frag);

    emptyEl.hidden = visible.length !== 0;
    var filtering = q || tags.size || year !== 'all' || aiRank;
    countEl.innerHTML = '<b>' + visible.length + '</b>편' +
      (filtering ? ' 표시 중 (전체 ' + cards.length + '편)' : '');
    clearEl.hidden = !filtering;
    syncTagButtons();
  }

  function toggleTag(tag) {
    if (state.tags.has(tag)) state.tags.delete(tag); else state.tags.add(tag);
    applyFilters();
  }

  function syncTagButtons() {
    tagbarEl.querySelectorAll('.rh-tag-btn').forEach(function (b) {
      var on = state.tags.has(b.getAttribute('data-tag'));
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    // 카드 내 미니 태그 하이라이트
    gridEl.querySelectorAll('.rh-mini-tag').forEach(function (mt) {
      mt.classList.toggle('on', state.tags.has(mt.getAttribute('data-tag')));
    });
  }

  function renderTagBar() {
    var tags = META.tags || [];
    var shown = showAllTags ? tags : tags.slice(0, TOP_TAGS);
    var html = shown.map(function (t) {
      return '<button class="rh-tag-btn" data-tag="' + esc(t.name) + '" aria-pressed="false">' +
        esc(t.name) + '<span class="rh-tag-n">' + t.count + '</span></button>';
    }).join('');
    if (tags.length > TOP_TAGS) {
      html += '<button class="rh-tag-more">' + (showAllTags ? '접기' : '+ 태그 전체(' + tags.length + ')') + '</button>';
    }
    tagbarEl.innerHTML = html;
    // 모바일 CSS가 접힘/펼침에 따라 가로 스크롤 ↔ 줄바꿈을 전환
    tagbarEl.classList.toggle('rh-tagbar--all', showAllTags);
    tagbarEl.querySelectorAll('.rh-tag-btn').forEach(function (b) {
      b.addEventListener('click', function () { toggleTag(b.getAttribute('data-tag')); });
    });
    var moreBtn = tagbarEl.querySelector('.rh-tag-more');
    if (moreBtn) moreBtn.addEventListener('click', function () { showAllTags = !showAllTags; renderTagBar(); syncTagButtons(); });
  }

  function renderYears() {
    var years = META.years || [];
    var html = '<button class="rh-year-btn active" data-year="all">전체</button>';
    html += years.map(function (y) {
      return '<button class="rh-year-btn" data-year="' + esc(y) + '">' + esc(y) + '</button>';
    }).join('');
    yearsEl.innerHTML = html;
    yearsEl.querySelectorAll('.rh-year-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        state.year = b.getAttribute('data-year');
        yearsEl.querySelectorAll('.rh-year-btn').forEach(function (x) { x.classList.remove('active'); });
        b.classList.add('active');
        applyFilters();
      });
    });
  }

  // ── AI 시맨틱 검색 ──
  function setAiNote(html, spin) {
    if (!html) { aiNote.classList.remove('show'); aiNote.innerHTML = ''; return; }
    aiNote.classList.add('show');
    aiNote.innerHTML = (spin ? '<span class="rh-ai-spin"></span> ' : '') + html;
  }

  function dequantize(b64, scale) {
    var bin = atob(b64);
    var v = new Float32Array(bin.length);
    for (var i = 0; i < bin.length; i++) {
      var x = bin.charCodeAt(i);
      v[i] = (x > 127 ? x - 256 : x) * scale;
    }
    return v;
  }

  function ensureVectors() {
    if (embIndex) return Promise.resolve(embIndex);
    return fetch('/assets/research-emb-posts.json', { cache: 'no-cache' })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        embIndex = new Map();
        (data.items || []).forEach(function (it) {
          embIndex.set(it.id, dequantize(it.v, it.s));
        });
        return embIndex;
      });
  }

  function cosine(a, b) {
    var dot = 0;
    for (var i = 0; i < a.length; i++) dot += a[i] * b[i];
    return dot; // 양쪽 unit vector
  }

  var aiBusy = false;
  function runAiSearch() {
    var q = searchEl.value.trim();
    if (!q) { state.aiRank = null; setAiNote(''); applyFilters(); return; }
    if (aiBusy) return;
    aiBusy = true;
    setAiNote('의미 기반으로 찾는 중&#8230;', true);
    Promise.all([
      ensureVectors(),
      fetch(ASK_API + '/api/embed', {
        method: 'POST',
        headers: keyHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({ q: q })
      }).then(function (r) {
        if (!r.ok) throw new Error('embed ' + r.status);
        return r.json();
      })
    ]).then(function (rs) {
      var vecs = rs[0], qv = new Float32Array(rs[1].vec);
      var scored = [];
      vecs.forEach(function (v, id) { scored.push([id, cosine(qv, v)]); });
      scored.sort(function (a, b) { return b[1] - a[1]; });
      var top1 = scored.length ? scored[0][1] : 0;
      var rank = new Map();
      if (top1 >= AI_TOP_GATE) {
        var cut = top1 - AI_REL_CUT;
        scored.slice(0, AI_TOP).forEach(function (pair) {
          if (pair[1] >= cut) rank.set(pair[0], pair[1]);
        });
      }
      state.aiRank = rank;
      if (!rank.size) {
        setAiNote('이 주제와 의미가 닿는 논문리뷰가 없다. 다른 표현으로 시도하거나 키워드 검색으로 전환해 보라.');
      } else {
        setAiNote('의미 기반 결과 <b>' + rank.size + '</b>편, 유사도순 정렬. 더 깊은 답이 필요하면 <a href="/ask/">AI에게 묻기</a>');
      }
      applyFilters();
    }).catch(function (err) {
      console.error('AI search error:', err);
      state.aiRank = null;
      setAiNote('AI 검색이 응답하지 않아 키워드 검색으로 대신한다.');
      state.q = q.toLowerCase();
      applyFilters();
    }).finally(function () { aiBusy = false; });
  }

  function setAiMode(on) {
    state.aiMode = on;
    aiToggle.classList.toggle('on', on);
    aiToggle.setAttribute('aria-pressed', on ? 'true' : 'false');
    searchEl.placeholder = on ? '질문하듯 검색해 보라 (Enter로 실행)…' : '제목·발견·태그 검색…';
    if (on) {
      state.q = '';
      if (searchEl.value.trim()) runAiSearch();
    } else {
      state.aiRank = null;
      setAiNote('');
      state.q = searchEl.value.trim().toLowerCase();
      applyFilters();
    }
  }

  aiToggle.addEventListener('click', function () { setAiMode(!state.aiMode); });

  // 서비스 가용성 프로브 — 인증된 경우에만 AI UI 노출 (주인장 전용 모드)
  // 미배포·장애·미인증 방문자에게는 조용히 숨김 — 키워드 탐색은 전면 공개 유지
  // 백엔드 /api/health는 콜드스타트 시 데이터 로드 때문에 4초 이상 걸릴 수 있다 —
  // 타임아웃을 짧게 잡으면 응답이 오기 전에 abort돼 버튼이 영영 안 뜨는 것처럼 보인다
  // (실측: 콜드 4.4초, 워밍 후 0.3초 이내). 넉넉히 잡아 이 경합을 없앤다.
  (function probe() {
    var ctrl = ('AbortController' in window) ? new AbortController() : null;
    var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, 9000) : null;
    fetch(ASK_API + '/api/health', { signal: ctrl ? ctrl.signal : undefined, headers: keyHeaders() })
      .then(function (r) { return r.json(); })
      .then(function (h) {
        if (h && h.ok && h.hasKey && (!h.authRequired || h.authorized)) {
          revealAiEl(aiToggle);
          revealAiEl(document.getElementById('rh-ask-cta'));
        } else if (h && h.ok && h.byok) {
          // 미인증 방문자도 /ask/에서 본인 Gemini 키로 이용 가능 — 입구는 열어 둔다
          revealAiEl(document.getElementById('rh-ask-cta'));
        }
      })
      .catch(function () { /* 서비스 없음 — AI UI 숨김 유지 */ })
      .finally(function () { if (timer) clearTimeout(timer); });
  })();

  // ── 이벤트 배선 ──
  var searchTimer = null;
  searchEl.addEventListener('input', function () {
    if (state.aiMode) return; // AI 모드는 Enter로만 실행 (API 절약)
    clearTimeout(searchTimer);
    searchTimer = setTimeout(function () {
      state.q = searchEl.value.trim().toLowerCase();
      applyFilters();
    }, 160);
  });
  searchEl.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter' && state.aiMode) { ev.preventDefault(); runAiSearch(); }
  });
  sortEl.addEventListener('change', function () { state.sort = sortEl.value; applyFilters(); });
  clearEl.addEventListener('click', function () {
    state.q = ''; state.tags.clear(); state.year = 'all'; state.aiRank = null;
    searchEl.value = '';
    setAiNote('');
    yearsEl.querySelectorAll('.rh-year-btn').forEach(function (x) { x.classList.remove('active'); });
    var allBtn = yearsEl.querySelector('[data-year="all"]'); if (allBtn) allBtn.classList.add('active');
    applyFilters();
  });

  // ── 로드 ──
  fetch('/assets/research-db.json', { cache: 'no-cache' })
    .then(function (r) { return r.json(); })
    .then(function (db) {
      META = db.meta || { tags: [], years: [] };
      var posts = db.posts || [];
      totalEl.textContent = (META.count || posts.length);
      // 히어로 통계 — 원문 링크 보유 수·태그 수·연도 범위
      (function fillStats() {
        var statsEl = document.getElementById('rh-stats');
        if (!statsEl) return;
        var linked = 0;
        posts.forEach(function (p) { if (p.source && p.source.link) linked++; });
        var ys = (META.years || []).map(String).slice().sort();
        document.getElementById('rh-stat-count').textContent = META.count || posts.length;
        document.getElementById('rh-stat-src').textContent = linked;
        document.getElementById('rh-stat-tags').textContent = (META.tags || []).length;
        document.getElementById('rh-stat-years').textContent =
          ys.length ? (ys[0] === ys[ys.length - 1] ? ys[0] : ys[0] + '–' + ys[ys.length - 1]) : '—';
        statsEl.hidden = false;
      })();
      renderYears();
      renderTagBar();
      cards = posts.map(buildCard);
      loadingEl.hidden = true;
      applyFilters();
    })
    .catch(function (err) {
      console.error('research-db load error:', err);
      loadingEl.textContent = '리서치 데이터를 불러오지 못했다. 잠시 후 다시 시도하라.';
    });
})();
{% endraw %}
</script>
