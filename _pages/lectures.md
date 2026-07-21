---
title: "강의자료 아카이브"
permalink: /lectures/
layout: single
author_profile: false
toc: false
---

## 닷커넥터의 서재 — 출간 도서

교실과 AI를 잇는 기록. 닷커넥터(김진관)가 쓰고 함께 지은 정식 출간 도서 {{ site.data.published_books | size }}권이다. 표지를 누르면 서점 상세 페이지로 이동한다.

<div class="pub-book-grid">
{% for pb in site.data.published_books %}
  {% if pb.url %}<a href="{{ pb.url }}" class="pub-book-card" target="_blank" rel="noopener">{% else %}<div class="pub-book-card">{% endif %}
    <div class="pub-cover"><img src="{{ pb.cover }}" alt="{{ pb.title }} 표지" loading="lazy"></div>
    {% if pb.badge %}<span class="pub-badge">{{ pb.badge }}</span>{% endif %}
    {% if pb.series %}<span class="pub-series">{{ pb.series }}</span>{% elsif pb.edition %}<span class="pub-series">{{ pb.edition }}</span>{% endif %}
    <div class="pub-title">{{ pb.title }}</div>
    {% if pb.subtitle %}<div class="pub-sub">{{ pb.subtitle }}</div>{% endif %}
    <div class="pub-meta">{{ pb.authors }}{% if pb.publisher %} · {{ pb.publisher }}{% endif %}{% if pb.year %} · {{ pb.year }}{% endif %}</div>
    {% if pb.url %}<div class="pub-buy">{{ pb.store }}에서 보기 ↗</div>{% endif %}
  {% if pb.url %}</a>{% else %}</div>{% endif %}
{% endfor %}
</div>

## 워크숍 강의

{% if site.data.lectures.size == 0 %}
<p>아직 등록된 강의가 없습니다.</p>
{% else %}
<div class="lecture-card-grid">
{% for lecture in site.data.lectures %}
  <a href="{% if lecture.locked %}#{% else %}{{ lecture.hub_url }}{% endif %}" class="lecture-card"{% if lecture.locked %} data-locked="{{ lecture.locked_payload }}"{% endif %}>
    {% if lecture.thumbnail %}<img src="{{ lecture.thumbnail }}" alt="{{ lecture.title }}">{% endif %}
    {% if lecture.curator %}<span class="card-badge">교육자 큐레이션</span>{% endif %}
    <div class="card-title">{{ lecture.title }}</div>
    <div class="card-meta">
      <span>{{ lecture.audience }}</span>{% if lecture.duration_min %} · <span>{{ lecture.duration_min }}분</span>{% endif %}{% if lecture.feature_count %} · <span>{{ lecture.feature_count }}개 기능</span>{% elsif lecture.slide_count %} · <span>{{ lecture.slide_count }}장 · {{ lecture.chapter_count }}챕터</span>{% elsif lecture.chapter_count %} · <span>{{ lecture.chapter_count }}개 장</span>{% endif %}{% if lecture.locked %} · <span class="lock-note">비밀번호 보호</span>{% endif %}
    </div>
    {% if lecture.curator %}
    <div class="card-credit">
      <div><span class="credit-label">원작</span> {{ lecture.author }}</div>
      <div><span class="credit-label credit-curator">큐레이션</span> {{ lecture.curator }}</div>
    </div>
    {% elsif lecture.author %}
    <div class="card-credit"><div><span class="credit-label">원작</span> {{ lecture.author }}</div></div>
    {% endif %}
  </a>
{% endfor %}
</div>
{% endif %}

## 도서 원고

<div class="lecture-card-grid">
{% for book in site.data.books %}
  <a href="{% if book.locked %}#{% else %}{{ book.url }}{% endif %}" class="lecture-card book-card"{% if book.locked %} data-locked="{{ book.locked_payload }}"{% elsif book.external %} target="_blank" rel="noopener"{% endif %}>
    <img src="{{ book.cover }}" alt="{{ book.title }} 표지">
    {% if book.status == "최신" %}<span class="card-badge">최신</span>
    {% elsif book.status %}<span class="card-badge badge-muted">{{ book.status }}</span>{% endif %}
    <div class="card-id">제{{ book.volume }}권{% if book.external %} · 웹 도서 ↗{% endif %}{% if book.locked %} · <span class="lock-note">비밀번호 보호</span>{% endif %}</div>
    <div class="card-title">{{ book.title }}</div>
    <div class="card-meta">{{ book.audience }}</div>
    <div class="card-meta">{{ book.structure }}</div>
    {% if book.author %}
    <div class="card-credit"><div><span class="credit-label">저자</span> {{ book.author }}</div></div>
    {% endif %}
  </a>
{% endfor %}
</div>

{% raw %}
<script>
(function () {
  function b64ToBytes(b64) {
    var bin = atob(b64);
    var a = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) a[i] = bin.charCodeAt(i);
    return a;
  }
  document.querySelectorAll('.lecture-card[data-locked]').forEach(function (card) {
    card.addEventListener('click', function (e) {
      e.preventDefault();
      var pw = window.prompt('비공개 자료입니다. 비밀번호를 입력하세요.');
      if (!pw) return;
      pw = pw.replace(/[０-９]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0xFEE0); }).trim();
      var payload = b64ToBytes(card.getAttribute('data-locked'));
      crypto.subtle.digest('SHA-256', new TextEncoder().encode(pw)).then(function (buf) {
        var key = new Uint8Array(buf);
        var out = new Uint8Array(payload.length);
        for (var i = 0; i < payload.length; i++) out[i] = payload[i] ^ key[i % key.length];
        var url = '';
        try { url = new TextDecoder().decode(out); } catch (err) {}
        if (/^https:\/\/[\x21-\x7e]+$/.test(url)) {
          window.open(url, '_blank', 'noopener');
        } else {
          alert('비밀번호가 올바르지 않습니다.');
        }
      });
    });
  });
})();
</script>
{% endraw %}
