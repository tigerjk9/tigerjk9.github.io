---
layout: default
title: "AI에게 묻기"
permalink: /ask/
description: "AI·교육 논문리뷰 100여 편을 근거로 답하는 리서치 어시스턴트. 질문하면 관련 연구의 발견과 시사점을 출처와 함께 알려준다."
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
  }
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

  .ak-head { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; flex-wrap: wrap; margin-bottom: 0.4em; }
  .ak-head h1 { font-size: 1.55rem; font-weight: 800; margin: 0; letter-spacing: -0.01em; color: var(--ak-text); }
  .ak-back { font-size: 0.85rem; color: var(--ak-accent); text-decoration: none; white-space: nowrap; }
  .ak-back:hover { text-decoration: underline; color: var(--ak-accent); }
  .ak-desc { font-size: 0.9rem; color: var(--ak-muted); line-height: 1.6; margin: 0 0 1.1em; }
  .ak-desc b { color: var(--ak-accent); font-weight: 700; }

  /* ── 대화 영역 ── */
  #ak-thread { flex: 1; display: flex; flex-direction: column; gap: 14px; margin-bottom: 1em; }
  .ak-msg { max-width: 92%; line-height: 1.7; font-size: 0.93rem; }
  .ak-msg-user {
    align-self: flex-end; background: var(--ak-user-bubble);
    border-radius: 14px 14px 3px 14px; padding: 10px 15px; color: var(--ak-text);
    white-space: pre-wrap; word-break: break-word;
  }
  .ak-msg-bot { align-self: flex-start; width: 100%; }
  .ak-bot-body {
    background: var(--ak-card); border: 1px solid var(--ak-border);
    border-radius: 3px 14px 14px 14px; padding: 13px 16px; color: var(--ak-text);
  }
  .ak-bot-body p { margin: 0 0 0.65em; }
  .ak-bot-body p:last-child { margin-bottom: 0; }
  .ak-bot-body ul { margin: 0.2em 0 0.7em; padding-left: 1.2em; }
  .ak-bot-body li { margin-bottom: 0.35em; }
  .ak-bot-body strong { font-weight: 700; }
  .ak-cite {
    font-size: 0.72em; font-weight: 700; color: var(--ak-accent);
    text-decoration: none; vertical-align: super; margin: 0 1px;
  }
  .ak-cite:hover { text-decoration: underline; color: var(--ak-accent); }

  /* ── 출처 카드 ── */
  .ak-sources { display: flex; flex-direction: column; gap: 6px; margin-top: 9px; }
  .ak-src {
    display: flex; gap: 9px; align-items: flex-start;
    background: var(--ak-panel); border: 1px solid var(--ak-border);
    border-radius: 9px; padding: 8px 11px; text-decoration: none;
    transition: border-color .15s;
  }
  .ak-src:hover { border-color: var(--ak-accent); }
  .ak-src-n {
    flex-shrink: 0; font-size: 0.72rem; font-weight: 700;
    background: var(--ak-accent-soft); color: var(--ak-accent);
    border-radius: 5px; padding: 2px 7px; margin-top: 1px;
  }
  .ak-src-t { font-size: 0.82rem; color: var(--ak-text); line-height: 1.45; font-weight: 600; }
  .ak-src-m { display: block; font-size: 0.72rem; color: var(--ak-faint); font-weight: 400; margin-top: 2px; }

  /* ── 로딩 ── */
  .ak-dots { display: inline-flex; gap: 4px; padding: 12px 16px; }
  .ak-dots span {
    width: 7px; height: 7px; border-radius: 50%; background: var(--ak-accent);
    animation: ak-bounce 1.2s infinite ease-in-out;
  }
  .ak-dots span:nth-child(2) { animation-delay: 0.15s; }
  .ak-dots span:nth-child(3) { animation-delay: 0.3s; }
  @keyframes ak-bounce { 0%, 70%, 100% { transform: translateY(0); opacity: .45; } 35% { transform: translateY(-5px); opacity: 1; } }

  /* ── 예시 질문 ── */
  #ak-examples { display: flex; flex-wrap: wrap; gap: 7px; margin-bottom: 1em; }
  .ak-ex {
    background: var(--ak-panel); border: 1px solid var(--ak-border-strong);
    border-radius: 999px; color: var(--ak-muted); font-size: 0.84rem;
    padding: 0.45em 1em; cursor: pointer; font-family: inherit; transition: all .15s;
  }
  .ak-ex:hover { color: var(--ak-accent); border-color: var(--ak-accent); }

  /* ── 입력바 ── */
  #ak-inputbar {
    display: flex; gap: 8px; align-items: flex-end;
    background: var(--ak-card); border: 1px solid var(--ak-border-strong);
    border-radius: 14px; padding: 9px 10px 9px 15px;
    position: sticky; bottom: 12px; box-shadow: var(--ak-shadow);
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

  .ak-notice {
    background: var(--ak-panel); border: 1px solid var(--ak-border);
    border-radius: 11px; padding: 14px 16px; font-size: 0.88rem;
    color: var(--ak-muted); line-height: 1.65;
  }
  .ak-error { color: #e07a6a; font-size: 0.85rem; padding: 8px 2px; }
  .ak-disclaim { font-size: 0.72rem; color: var(--ak-faint); text-align: center; margin: 0.7em 0 0; }

  @media (max-width: 600px) {
    #ask-app { padding: 1em 0.9em 1.4em; }
    .ak-msg { max-width: 100%; }
  }
  @media (prefers-reduced-motion: reduce) {
    .ak-dots span { animation: none; }
  }
</style>

<div id="ask-app">
  <div class="ak-head">
    <h1>&#128172; AI에게 묻기</h1>
    <a class="ak-back" href="/research/">&#8592; 리서치 허브</a>
  </div>
  <p class="ak-desc">AI·교육 논문리뷰 <b id="ak-total">100여</b> 편을 근거로 답하는 리서치 어시스턴트. 답변의 모든 주장에는 근거 논문이 붙는다. 근거가 없으면 없다고 말한다.</p>

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
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        q: q,
        history: history.slice(-6).map(function (h) { return { role: h.role === 'bot' ? 'model' : 'user', text: h.text.slice(0, 500) }; })
      })
    }).then(function (r) {
      return r.json().then(function (data) { return { status: r.status, data: data }; });
    }).then(function (res) {
      loader.remove();
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

  // 서비스 프로브 — 성공 시 입력 활성화, 실패 시 안내
  var ctrl = ('AbortController' in window) ? new AbortController() : null;
  var timer = ctrl ? setTimeout(function () { ctrl.abort(); }, 4000) : null;
  fetch(ASK_API + '/api/health', { signal: ctrl ? ctrl.signal : undefined })
    .then(function (r) { return r.json(); })
    .then(function (h) {
      if (h && h.ok && h.hasKey) {
        inputbar.hidden = false;
        disclaim.hidden = false;
        document.getElementById('ak-total').textContent = h.posts;
        input.focus();
      } else { throw new Error('not ready'); }
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
