---
layout: default
title: "AI에게 묻기"
permalink: /ask/
description: "AI·교육 논문 리뷰·아티클 140여 편을 근거로 답하는 리서치 어시스턴트. 질문하면 관련 연구의 발견과 시사점을 출처와 함께 알려준다."
---

<style>
  #ask-app {
    --ak-card: #2c313d;
    --ak-border: rgba(255,255,255,0.11);
    --ak-border-strong: rgba(255,255,255,0.2);
    --ak-text: #eaeaea;
    --ak-muted: #9aa4b2;
    --ak-faint: #7c8593;
    --ak-accent: #2ec4cc;
    --ak-accent-ink: #1a2a2b;
    --ak-accent-soft: rgba(46,196,204,0.14);
    --ak-user-bubble: rgba(46,196,204,0.16);
    --ak-panel: rgba(255,255,255,0.03);
    --ak-shadow: 0 6px 20px rgba(0,0,0,0.35);

    max-width: 780px;
    margin: 0 auto;
    padding: 1.6em 1.2em 2em;
    color: var(--ak-text);
    font-family: -apple-system, "Pretendard", "Segoe UI", "Malgun Gothic", sans-serif;
    display: flex; flex-direction: column;
    min-height: calc(100vh - 220px);
    min-height: calc(100dvh - 220px); /* 모바일 주소창 수축 대응 */
    /* 한국어 어절 단위 줄바꿈 — 단어 중간에서 끊기지 않게. 긴 URL 등은 break-word로 방어 */
    word-break: keep-all;
    overflow-wrap: break-word;
  }
  /* hidden 속성 강제 — display를 지정한 컴포넌트가 [hidden]을 이기는 것 차단 */
  #ask-app [hidden] { display: none !important; }
  html[data-theme="light"] #ask-app {
    --ak-card: #ffffff;
    --ak-border: #e4e8ee;
    --ak-border-strong: #cdd4de;
    --ak-text: #252a34;
    --ak-muted: #5a6472;
    --ak-faint: #838d9b;
    --ak-accent: #0078c8;
    --ak-accent-ink: #ffffff;
    --ak-accent-soft: rgba(0,120,200,0.08);
    --ak-user-bubble: rgba(0,120,200,0.09);
    --ak-panel: #f7f9fb;
    --ak-shadow: 0 6px 20px rgba(30,40,60,0.09);
  }

  #ask-app .ak-head { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; flex-wrap: wrap; margin-bottom: 0.4em; }
  #ask-app .ak-head h1 { font-size: 1.55rem; font-weight: 800; margin: 0; letter-spacing: -0.01em; color: var(--ak-text); }
  #ask-app .ak-back { font-size: 0.85rem; color: var(--ak-accent); text-decoration: none; white-space: nowrap; }
  #ask-app .ak-back:hover { text-decoration: underline; color: var(--ak-accent); }
  #ask-app .ak-desc { font-size: 0.9rem; color: var(--ak-muted); line-height: 1.6; margin: 0 0 1.1em; }
  #ask-app .ak-desc b { color: var(--ak-accent); font-weight: 700; }

  /* ── 대화 영역 ── */
  #ak-thread { flex: 1; display: flex; flex-direction: column; gap: 14px; margin-bottom: 1em; }
  #ask-app .ak-msg { max-width: 92%; line-height: 1.7; font-size: 0.93rem; }
  #ask-app .ak-msg-user {
    align-self: flex-end; background: var(--ak-user-bubble);
    border-radius: 14px 14px 3px 14px; padding: 10px 15px; color: var(--ak-text);
    white-space: pre-wrap;
  }
  #ask-app .ak-msg-bot { align-self: flex-start; width: 100%; }
  #ask-app .ak-bot-body {
    background: var(--ak-card); border: 1px solid var(--ak-border);
    border-radius: 3px 14px 14px 14px; padding: 13px 16px; color: var(--ak-text);
  }
  #ask-app .ak-bot-body p { margin: 0 0 0.65em; }
  #ask-app .ak-bot-body p:last-child { margin-bottom: 0; }
  #ask-app .ak-bot-body ul { margin: 0.2em 0 0.7em; padding-left: 1.2em; }
  #ask-app .ak-bot-body li { margin-bottom: 0.35em; }
  #ask-app .ak-bot-body strong { font-weight: 700; }
  #ask-app .ak-cite {
    font-size: 0.72em; font-weight: 700; color: var(--ak-accent);
    text-decoration: none; vertical-align: super; margin: 0 1px;
  }
  #ask-app .ak-cite:hover { text-decoration: underline; color: var(--ak-accent); }

  /* ── 출처 카드 ── */
  #ask-app .ak-sources { display: flex; flex-direction: column; gap: 6px; margin-top: 9px; }
  #ask-app .ak-src {
    display: flex; gap: 9px; align-items: flex-start;
    background: var(--ak-panel); border: 1px solid var(--ak-border);
    border-radius: 9px; padding: 8px 11px; text-decoration: none;
    transition: border-color .15s;
  }
  #ask-app .ak-src:hover { border-color: var(--ak-accent); }
  #ask-app .ak-src-n {
    flex-shrink: 0; font-size: 0.72rem; font-weight: 700;
    background: var(--ak-accent-soft); color: var(--ak-accent);
    border-radius: 5px; padding: 2px 7px; margin-top: 1px;
  }
  #ask-app .ak-src-t { font-size: 0.82rem; color: var(--ak-text); line-height: 1.45; font-weight: 600; }
  #ask-app .ak-src-m { display: block; font-size: 0.72rem; color: var(--ak-faint); font-weight: 400; margin-top: 2px; }

  /* ── 로딩 ── */
  #ask-app .ak-dots { display: inline-flex; gap: 4px; padding: 12px 16px; }
  #ask-app .ak-dots span {
    width: 7px; height: 7px; border-radius: 50%; background: var(--ak-accent);
    animation: ak-bounce 1.2s infinite ease-in-out;
  }
  #ask-app .ak-dots span:nth-child(2) { animation-delay: 0.15s; }
  #ask-app .ak-dots span:nth-child(3) { animation-delay: 0.3s; }
  @keyframes ak-bounce { 0%, 70%, 100% { transform: translateY(0); opacity: .45; } 35% { transform: translateY(-5px); opacity: 1; } }

  /* ── 예시 질문 ── */
  #ak-examples { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 1em; }
  #ask-app .ak-ex {
    background: var(--ak-panel); border: 1px solid var(--ak-border-strong);
    border-radius: 999px; color: var(--ak-muted); font-size: 0.84rem;
    padding: 0.45em 1em; cursor: pointer; font-family: inherit; transition: all .15s;
  }
  #ask-app .ak-ex:hover { color: var(--ak-accent); border-color: var(--ak-accent); }

  /* ── 입력바 ── */
  #ak-inputbar {
    display: flex; gap: 8px; align-items: flex-end;
    background: var(--ak-card); border: 1px solid var(--ak-border-strong);
    border-radius: 14px; padding: 9px 10px 9px 15px;
    position: sticky; bottom: calc(12px + env(safe-area-inset-bottom, 0px));
    box-shadow: var(--ak-shadow);
  }
  #ak-inputbar:focus-within { border-color: var(--ak-accent); }
  #ak-input {
    flex: 1; background: none; border: none; outline: none; resize: none;
    color: var(--ak-text); font-size: 0.95rem; font-family: inherit;
    line-height: 1.55; max-height: 7.5em; padding: 4px 0;
  }
  #ak-input::placeholder { color: var(--ak-faint); }
  #ak-send {
    flex-shrink: 0; background: var(--ak-accent); color: var(--ak-accent-ink);
    border: none; border-radius: 10px; font-size: 0.9rem; font-weight: 700;
    padding: 0.55em 1.1em; cursor: pointer; font-family: inherit; transition: filter .15s;
  }
  #ak-send:hover:not(:disabled) { filter: brightness(1.08); }
  #ak-send:disabled { opacity: 0.45; cursor: default; }

  #ask-app .ak-notice {
    background: var(--ak-panel); border: 1px solid var(--ak-border);
    border-radius: 11px; padding: 14px 16px; font-size: 0.88rem;
    color: var(--ak-muted); line-height: 1.65;
  }
  #ask-app .ak-error { color: #e07a6a; font-size: 0.85rem; padding: 8px 2px; }
  #ask-app .ak-keyform { display: flex; gap: 7px; margin-top: 11px; flex-wrap: wrap; }
  #ask-app .ak-keyform input {
    flex: 1 1 180px; background: var(--ak-card); border: 1px solid var(--ak-border-strong);
    border-radius: 8px; color: var(--ak-text); font-size: 0.88rem;
    padding: 0.5em 0.8em; outline: none; font-family: inherit;
  }
  #ask-app .ak-keyform input:focus { border-color: var(--ak-accent); }
  #ask-app .ak-keyform button {
    background: var(--ak-accent); color: var(--ak-accent-ink); border: none;
    border-radius: 8px; font-size: 0.86rem; font-weight: 700; padding: 0.5em 1em;
    cursor: pointer; font-family: inherit;
  }
  #ask-app .ak-keyerr { color: #e07a6a; font-size: 0.8rem; margin: 6px 0 0; display: none; }
  #ask-app .ak-disclaim { font-size: 0.72rem; color: var(--ak-faint); text-align: center; margin: 0.7em 0 0; }
  #ask-app .ak-notice strong { color: var(--ak-text); }
  #ask-app .ak-lock-meta { font-size: 0.78rem; color: var(--ak-faint); line-height: 1.6; margin: 10px 0 0; }
  #ask-app .ak-lock-meta a, #ask-app .ak-notice a { color: var(--ak-accent); }
  #ask-app .ak-owner-link {
    background: none; border: none; color: var(--ak-faint); font-size: 0.76rem;
    text-decoration: underline; cursor: pointer; padding: 0; margin-top: 13px; font-family: inherit;
  }
  #ask-app .ak-owner-link:hover { color: var(--ak-muted); }
  #ask-app .ak-linkbtn {
    background: none; border: none; color: var(--ak-accent); font-size: inherit;
    text-decoration: underline; cursor: pointer; padding: 0; font-family: inherit;
  }
  #ask-app .ak-keyform button:disabled { opacity: 0.5; cursor: default; }

  @media (max-width: 600px) {
    #ask-app { padding: 0.9em 0.85em 1.2em; }
    #ask-app .ak-head h1 { font-size: 1.35rem; }
    #ask-app .ak-desc { font-size: 0.85rem; }
    #ask-app .ak-msg { max-width: 100%; }
    #ask-app .ak-bot-body { padding: 12px 13px; }
    #ask-app .ak-ex { font-size: 0.82rem; padding: 0.5em 0.9em; }
    /* iOS Safari는 입력 폰트가 16px 미만이면 포커스 시 강제 줌 */
    #ak-input, #ask-app .ak-keyform input { font-size: 16px; }
    #ak-inputbar { bottom: calc(8px + env(safe-area-inset-bottom, 0px)); border-radius: 12px; padding: 8px 8px 8px 13px; }
    #ak-send { padding: 0.6em 1em; }
    #ask-app .ak-src { padding: 9px 10px; }
  }
  @media (prefers-reduced-motion: reduce) {
    #ask-app .ak-dots span { animation: none; }
  }
</style>

<div id="ask-app">
  <div class="ak-head">
    <h1>&#128172; AI에게 묻기</h1>
    <a class="ak-back" href="/research/">&#8592; 리서치 허브</a>
  </div>
  <p class="ak-desc">AI·교육 논문 리뷰·아티클 <b id="ak-total">140여</b>편을 근거로 답하는 리서치 어시스턴트. 답변의 모든 주장에는 근거 논문이 붙는다. 근거가 없으면 없다고 말한다.</p>

  <div id="ak-thread" aria-live="polite"></div>

  <div id="ak-examples"></div>

  <div id="ak-inputbar" hidden>
    <textarea id="ak-input" rows="1" placeholder="예: AI 피드백이 학습에 효과가 있나?" aria-label="질문 입력"></textarea>
    <button id="ak-send" disabled>보내기</button>
  </div>
  <p class="ak-disclaim" id="ak-disclaim" hidden>답변은 블로그의 논문리뷰 범위 안에서 생성된다. 중요한 판단에는 원문을 확인하라.</p>
</div>

<script>
{% raw %}
(function () {
  'use strict';

  var ASK_API = 'https://dotconnector-ask.vercel.app';
  var EXAMPLES = [
    'AI 피드백이 학습에 효과가 있나?',
    '챗GPT가 학생의 비판적 사고를 해치나?',
    'AI 시대 교사의 역할은 어떻게 달라지나?',
    '자기조절학습을 돕는 AI 설계 원칙은?'
  ];

  var thread = document.getElementById('ak-thread');
  var examplesEl = document.getElementById('ak-examples');
  var inputbar = document.getElementById('ak-inputbar');
  var input = document.getElementById('ak-input');
  var sendBtn = document.getElementById('ak-send');
  var disclaim = document.getElementById('ak-disclaim');

  var history = [];   // {role: 'user'|'bot', text}
  var busy = false;

  // 접근 키(주인장) + Gemini API 키(방문자 BYOK) — localStorage, 기기당 1회 입력
  var KEY_STORE = 'dc_ask_key';
  var GKEY_STORE = 'dc_gemini_key';
  var GKEY_RE = /^AIza[0-9A-Za-z_-]{30,80}$/;
  function getKey() { try { return localStorage.getItem(KEY_STORE) || ''; } catch (e) { return ''; } }
  function setKey(v) { try { localStorage.setItem(KEY_STORE, v); } catch (e) {} }
  function getGKey() { try { return localStorage.getItem(GKEY_STORE) || ''; } catch (e) { return ''; } }
  function setGKey(v) { try { localStorage.setItem(GKEY_STORE, v); } catch (e) {} }
  function dropGKey() { try { localStorage.removeItem(GKEY_STORE); } catch (e) {} }
  function keyHeaders(extra) {
    var h = extra || {};
    var k = getKey();
    if (k) h['X-Ask-Key'] = k;
    var g = getGKey();
    if (g) h['X-Gemini-Key'] = g;
    return h;
  }

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  // 답변 렌더: 볼드·불릿 + [n] 인용을 출처 링크로
  function renderAnswer(text, sources) {
    var byN = {};
    (sources || []).forEach(function (s) { byN[s.n] = s; });
    function inline(s) {
      var h = esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
      // [1, 2] → [1][2] 정규화 후 각 [n]을 출처 링크로
      h = h.replace(/\[(\d+(?:\s*,\s*\d+)+)\]/g, function (m, nums) {
        return nums.split(/\s*,\s*/).map(function (n) { return '[' + n + ']'; }).join('');
      });
      h = h.replace(/\[(\d+)\]/g, function (m, n) {
        var src = byN[+n];
        return src ? '<a class="ak-cite" href="' + esc(src.url) + '" title="' + esc(src.title) + '">[' + n + ']</a>' : m;
      });
      return h;
    }
    var lines = text.split('\n'), out = [], listOpen = false;
    function closeList() { if (listOpen) { out.push('</ul>'); listOpen = false; } }
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].trim();
      if (!line) { closeList(); continue; }
      var ml = line.match(/^[*\-]\s+(.+)$/);
      if (ml) { if (!listOpen) { out.push('<ul>'); listOpen = true; } out.push('<li>' + inline(ml[1]) + '</li>'); continue; }
      closeList();
      out.push('<p>' + inline(line) + '</p>');
    }
    closeList();
    return out.join('');
  }

  function addUserMsg(q) {
    var el = document.createElement('div');
    el.className = 'ak-msg ak-msg-user';
    el.textContent = q;
    thread.appendChild(el);
    el.scrollIntoView({ behavior: 'smooth', block: 'end' });
  }

  function addBotMsg(answer, sources) {
    var el = document.createElement('div');
    el.className = 'ak-msg ak-msg-bot';
    var srcHtml = '';
    if (sources && sources.length) {
      srcHtml = '<div class="ak-sources">' + sources.map(function (s) {
        return '<a class="ak-src" href="' + esc(s.url) + '">' +
          '<span class="ak-src-n">[' + s.n + ']</span>' +
          '<span class="ak-src-t">' + esc(s.title) +
          '<span class="ak-src-m">' + esc(s.date) + ' · ' + esc((s.secs || []).join(' · ')) + '</span></span></a>';
      }).join('') + '</div>';
    }
    el.innerHTML = '<div class="ak-bot-body">' + renderAnswer(answer, sources) + '</div>' + srcHtml;
    thread.appendChild(el);
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function addLoading() {
    var el = document.createElement('div');
    el.className = 'ak-msg ak-msg-bot ak-loading';
    el.innerHTML = '<div class="ak-bot-body ak-dots"><span></span><span></span><span></span></div>';
    thread.appendChild(el);
    el.scrollIntoView({ behavior: 'smooth', block: 'end' });
    return el;
  }

  function addError(msg) {
    var el = document.createElement('div');
    el.className = 'ak-error';
    el.textContent = msg;
    thread.appendChild(el);
  }

  function send(q) {
    q = (q || input.value).trim();
    if (!q || busy) return;
    busy = true;
    sendBtn.disabled = true;
    input.value = '';
    autosize();
    examplesEl.style.display = 'none';
    addUserMsg(q);
    var loader = addLoading();

    fetch(ASK_API + '/api/ask', {
      method: 'POST',
      headers: keyHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        q: q,
        history: history.slice(-6).map(function (h) { return { role: h.role === 'bot' ? 'model' : 'user', text: h.text.slice(0, 500) }; })
      })
    }).then(function (r) {
      return r.json().then(function (data) { return { status: r.status, data: data }; });
    }).then(function (res) {
      loader.remove();
      if (res.status === 401) {
        if (res.data && res.data.error === 'bad_gemini_key') {
          dropGKey();
          addError('Gemini API 키가 더 이상 유효하지 않다. 페이지를 새로고침해 키를 다시 입력해 달라.');
        } else {
          try { localStorage.removeItem(KEY_STORE); } catch (e) {}
          addError('접근 키가 더 이상 유효하지 않다. 페이지를 새로고침해 키를 다시 입력해 달라.');
        }
        return;
      }
      if (res.status === 429) {
        addError(res.data.message || '요청이 너무 잦다. 잠시 후 다시 시도해 달라.');
        return;
      }
      if (res.status !== 200 || !res.data.answer) {
        addError(res.data.message || '답변 생성에 실패했다. 잠시 후 다시 시도해 달라.');
        return;
      }
      addBotMsg(res.data.answer, res.data.sources);
      history.push({ role: 'user', text: q });
      history.push({ role: 'bot', text: res.data.answer });
    }).catch(function (err) {
      console.error(err);
      loader.remove();
      addError('네트워크 오류가 발생했다. 잠시 후 다시 시도해 달라.');
    }).finally(function () {
      busy = false;
      sendBtn.disabled = !input.value.trim();
      input.focus();
    });
  }

  function autosize() {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 140) + 'px';
  }

  input.addEventListener('input', function () {
    sendBtn.disabled = !input.value.trim() || busy;
    autosize();
  });
  input.addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); send(); }
  });
  sendBtn.addEventListener('click', function () { send(); });

  // 예시 질문 칩
  EXAMPLES.forEach(function (q) {
    var b = document.createElement('button');
    b.className = 'ak-ex';
    b.textContent = q;
    b.addEventListener('click', function () { send(q); });
    examplesEl.appendChild(b);
  });

  // 서비스 프로브 — 인증되면 채팅 UI, 키 필요하면 잠금 UI, 서비스 없으면 안내
  function unlockUi(h) {
    inputbar.hidden = false;
    disclaim.hidden = false;
    examplesEl.style.display = '';
    document.getElementById('ak-total').textContent = h.posts;
    // 방문자 본인 키로 이용 중이면 표시 + 키 삭제 수단 제공
    if (getGKey() && !document.getElementById('ak-gkey-bar')) {
      var bar = document.createElement('p');
      bar.className = 'ak-disclaim';
      bar.id = 'ak-gkey-bar';
      bar.innerHTML = '내 Gemini 키로 이용 중 (호출량은 내 키의 무료 할당량에서 차감) &#183; <button class="ak-linkbtn" id="ak-gkey-del" type="button">키 삭제</button>';
      disclaim.parentNode.insertBefore(bar, disclaim);
      document.getElementById('ak-gkey-del').addEventListener('click', function () {
        dropGKey();
        location.reload();
      });
    }
    input.focus();
  }

  function lockedUi(h) {
    examplesEl.style.display = 'none';
    if (h && h.posts) document.getElementById('ak-total').textContent = h.posts;
    var byok = Boolean(h && h.byok); // 백엔드가 방문자 키 모드를 지원할 때만 키 입력 UI 노출
    var n = document.createElement('div');
    n.className = 'ak-notice';
    var ownerForm =
      '<div class="ak-keyform" id="ak-owner-form"' + (byok ? ' hidden' : '') + '><input type="password" id="ak-key-in" placeholder="접근 키" aria-label="접근 키 입력">' +
      '<button id="ak-key-btn">확인</button></div>' +
      '<p class="ak-keyerr" id="ak-key-err">키가 일치하지 않는다.</p>';
    if (byok) {
      n.innerHTML = '리서치 어시스턴트는 서버 비용 문제로 <strong>본인의 Gemini API 키</strong>를 넣어 쓰는 방식으로 열려 있다. ' +
        'Google AI Studio에서 무료로 발급받은 키를 입력하면 누구나 바로 대화할 수 있다.' +
        '<div class="ak-keyform"><input type="password" id="ak-gkey-in" placeholder="Gemini API 키 (AIza&#8230;)" aria-label="Gemini API 키 입력">' +
        '<button id="ak-gkey-btn">시작하기</button></div>' +
        '<p class="ak-keyerr" id="ak-gkey-err"></p>' +
        '<p class="ak-lock-meta">키는 지금 쓰는 브라우저에만 저장되고 서버에는 저장되지 않는다. 질문할 때 Gemini 호출에만 쓰인다. ' +
        '<a href="https://aistudio.google.com/apikey" target="_blank" rel="noopener">키 무료 발급 &#8599;</a></p>' +
        '<p class="ak-lock-meta">키 없이도 <a href="/research/">리서치 허브</a>에서 태그·키워드 탐색으로 같은 논문리뷰를 읽을 수 있다.</p>' +
        '<button class="ak-owner-link" id="ak-owner-link" type="button">블로그 주인장이라면 접근 키로 입장</button>' + ownerForm;
    } else {
      n.innerHTML = '리서치 어시스턴트는 API 비용 문제로 현재 <strong>블로그 주인장 전용</strong>으로 운영 중이다. ' +
        '방문자는 <a href="/research/">리서치 허브</a>에서 태그·키워드·카드 탐색으로 같은 논문리뷰를 자유롭게 읽을 수 있다.' + ownerForm;
    }
    thread.appendChild(n);

    // 주인장 접근 키
    var keyIn = document.getElementById('ak-key-in');
    var tryKey = function () {
      var v = keyIn.value.trim();
      if (!v) return;
      setKey(v);
      fetch(ASK_API + '/api/health', { headers: { 'X-Ask-Key': v } })
        .then(function (r) { return r.json(); })
        .then(function (h2) {
          if (h2 && h2.authorized) { n.remove(); unlockUi(h2); }
          else {
            try { localStorage.removeItem(KEY_STORE); } catch (e) {}
            document.getElementById('ak-key-err').style.display = 'block';
          }
        });
    };
    document.getElementById('ak-key-btn').addEventListener('click', tryKey);
    keyIn.addEventListener('keydown', function (ev) { if (ev.key === 'Enter') tryKey(); });

    if (!byok) return;

    document.getElementById('ak-owner-link').addEventListener('click', function () {
      var f = document.getElementById('ak-owner-form');
      f.hidden = !f.hidden;
      if (!f.hidden) keyIn.focus();
    });

    // 방문자 Gemini API 키 — Google에 직접 유효성 확인 (이 확인 요청은 우리 서버를 거치지 않는다)
    var gIn = document.getElementById('ak-gkey-in');
    var gErr = document.getElementById('ak-gkey-err');
    var gBtn = document.getElementById('ak-gkey-btn');
    function gFail(msg) { gErr.textContent = msg; gErr.style.display = 'block'; }
    var tryGKey = function () {
      var v = gIn.value.trim();
      if (!v || gBtn.disabled) return;
      gErr.style.display = 'none';
      if (!GKEY_RE.test(v)) { gFail('Gemini API 키 형식이 아니다. AIza로 시작하는 키를 넣어 달라.'); return; }
      gBtn.disabled = true;
      gBtn.textContent = '확인 중…';
      fetch('https://generativelanguage.googleapis.com/v1beta/models?pageSize=1&key=' + encodeURIComponent(v))
        .then(function (r) {
          if (!r.ok) throw new Error('invalid');
          setGKey(v);
          return fetch(ASK_API + '/api/health', { headers: keyHeaders() }).then(function (r2) { return r2.json(); });
        })
        .then(function (h2) {
          if (h2 && h2.authorized) { n.remove(); unlockUi(h2); }
          else { throw new Error('server'); }
        })
        .catch(function (err) {
          dropGKey();
          gFail(err && err.message === 'invalid'
            ? '키가 유효하지 않다. Google AI Studio에서 발급한 키인지 확인해 달라.'
            : '키 확인에 실패했다. 네트워크 상태를 확인하고 다시 시도해 달라.');
        })
        .finally(function () { gBtn.disabled = false; gBtn.textContent = '시작하기'; });
    };
    gBtn.addEventListener('click', tryGKey);
    gIn.addEventListener('keydown', function (ev) { if (ev.key === 'Enter') tryGKey(); });
  }

  var ctrl = ('AbortController' in window) ? new AbortController() : null;
  var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, 4000) : null;
  fetch(ASK_API + '/api/health', { signal: ctrl ? ctrl.signal : undefined, headers: keyHeaders() })
    .then(function (r) { return r.json(); })
    .then(function (h) {
      if (h && h.ok && h.hasKey && (!h.authRequired || h.authorized)) unlockUi(h);
      else if (h && h.ok && h.authRequired) lockedUi(h);
      else throw new Error('not ready');
    })
    .catch(function () {
      examplesEl.style.display = 'none';
      var n = document.createElement('div');
      n.className = 'ak-notice';
      n.innerHTML = 'AI 어시스턴트가 아직 준비되지 않았다. 그동안 <a href="/research/">리서치 허브</a>에서 태그·키워드로 논문리뷰를 탐색할 수 있다.';
      thread.appendChild(n);
    })
    .finally(function () { if (timer) clearTimeout(timer); });
})();
{% endraw %}
</script>
