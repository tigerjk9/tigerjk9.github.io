---
title: "강의자료 아카이브"
permalink: /lectures/
layout: single
author_profile: false
toc: false
standalone: true
---

## 닷커넥터의 서재 <span class="lec-count">{{ site.data.published_books | size }}</span>

<div class="pub-book-grid">
{% for pb in site.data.published_books %}
  {% if pb.url %}<a href="{{ pb.url }}" class="pub-book-card" target="_blank" rel="noopener">{% else %}<div class="pub-book-card">{% endif %}
    <div class="pub-cover"><img src="{{ pb.cover }}" alt="{{ pb.title }} 표지" loading="lazy"></div>
    {% if pb.badge %}<span class="pub-badge">{{ pb.badge }}</span>{% endif %}
    {% if pb.series %}<span class="pub-series">{{ pb.series }}</span>{% elsif pb.edition %}<span class="pub-series">{{ pb.edition }}</span>{% endif %}
    <div class="pub-body">
      <div class="pub-title">{{ pb.title }}</div>
      {% if pb.subtitle %}<div class="pub-sub">{{ pb.subtitle }}</div>{% endif %}
      <div class="pub-meta">{{ pb.authors }}{% if pb.publisher %} · {{ pb.publisher }}{% endif %}{% if pb.year %} · {{ pb.year }}{% endif %}</div>
    </div>
    {% if pb.url %}<div class="pub-buy">{{ pb.store }}에서 보기 <span aria-hidden="true">↗</span></div>{% endif %}
  {% if pb.url %}</a>{% else %}</div>{% endif %}
{% endfor %}
</div>

## 워크숍 강의 <span class="lec-count">{{ site.data.lectures | size }}</span>

{% if site.data.lectures.size == 0 %}
<p class="lec-empty">아직 등록된 강의가 없다.</p>
{% else %}
<div class="lecture-card-grid">
{% for lecture in site.data.lectures %}
  <a href="{% if lecture.locked %}#{% else %}{{ lecture.hub_url }}{% endif %}" class="lecture-card lecture-card--media{% if lecture.locked %} is-locked{% endif %}"{% if lecture.locked %} data-locked="{{ lecture.locked_payload }}"{% endif %}>
    {% if lecture.thumbnail %}<div class="card-thumb"><img src="{{ lecture.thumbnail }}" alt="{{ lecture.title }}" loading="lazy"></div>{% endif %}
    {% if lecture.curator %}<span class="card-badge">교육자 큐레이션</span>{% endif %}
    <div class="card-body">
      <div class="card-title">{{ lecture.title }}</div>
      {% if lecture.subtitle %}<div class="card-sub">{{ lecture.subtitle }}</div>{% endif %}
      <div class="card-meta">
        <span>{{ lecture.audience }}</span>{% if lecture.duration_min %} <span class="dot"></span> <span>{{ lecture.duration_min }}분</span>{% endif %}{% if lecture.feature_count %} <span class="dot"></span> <span>{{ lecture.feature_count }}개 기능</span>{% elsif lecture.slide_count %} <span class="dot"></span> <span>{{ lecture.slide_count }}장 · {{ lecture.chapter_count }}챕터</span>{% elsif lecture.chapter_count %} <span class="dot"></span> <span>{{ lecture.chapter_count }}개 장</span>{% endif %}
      </div>
      {% if lecture.locked %}<div class="lock-note"><i class="fas fa-lock" aria-hidden="true"></i> 비밀번호 보호</div>{% endif %}
    </div>
    {% if lecture.curator %}
    <div class="card-credit">
      <div><span class="credit-label">원작</span> <span class="credit-name">{{ lecture.author }}</span></div>
      <div><span class="credit-label credit-curator">큐레이션</span> <span class="credit-name">{{ lecture.curator }}</span></div>
    </div>
    {% elsif lecture.author %}
    <div class="card-credit"><div><span class="credit-label">원작</span> <span class="credit-name">{{ lecture.author }}</span></div></div>
    {% endif %}
  </a>
{% endfor %}
</div>
{% endif %}

## 도서 원고 <span class="lec-count">{{ site.data.books | size }}</span>

<div class="lecture-card-grid">
{% for book in site.data.books %}
  <a href="{% if book.locked %}#{% else %}{{ book.url }}{% endif %}" class="lecture-card lecture-card--media book-card{% if book.locked %} is-locked{% endif %}"{% if book.locked %} data-locked="{{ book.locked_payload }}"{% elsif book.external %} target="_blank" rel="noopener"{% endif %}>
    <div class="card-thumb"><img src="{{ book.cover }}" alt="{{ book.title }} 표지" loading="lazy"></div>
    {% if book.status == "최신" %}<span class="card-badge">최신</span>
    {% elsif book.status %}<span class="card-badge badge-muted">{{ book.status }}</span>{% endif %}
    <div class="card-body">
      <div class="card-id">제{{ book.volume }}권{% if book.external %} <span class="dot"></span> 웹 도서 ↗{% endif %}</div>
      <div class="card-title">{{ book.title }}</div>
      <div class="card-meta">{{ book.audience }}</div>
      <div class="card-meta">{{ book.structure }}</div>
      {% if book.locked %}<div class="lock-note"><i class="fas fa-lock" aria-hidden="true"></i> 비밀번호 보호</div>{% endif %}
    </div>
    {% if book.author %}
    <div class="card-credit"><div><span class="credit-label">저자</span> <span class="credit-name">{{ book.author }}</span></div></div>
    {% endif %}
  </a>
{% endfor %}
</div>

{% raw %}
<script>
(function () {
  // 잠금 카드 복호화: PBKDF2-HMAC-SHA256(20만회) + AES-256-GCM.
  // payload(base64) = [ver=2][salt:16][iv:12][ciphertext+tag]. 카드마다 salt/iv가 달라
  // 동일 URL이라도 암호문이 다르며, 틀린 비번은 GCM 인증 실패로 복호화 자체가 거부된다.
  function b64ToBytes(b64) {
    var bin = atob(b64);
    var a = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) a[i] = bin.charCodeAt(i);
    return a;
  }
  async function unlock(payloadB64, pw) {
    var raw = b64ToBytes(payloadB64);
    if (raw[0] !== 2) throw new Error('format');
    var salt = raw.slice(1, 17), iv = raw.slice(17, 29), ct = raw.slice(29);
    var pwKey = await crypto.subtle.importKey('raw', new TextEncoder().encode(pw), 'PBKDF2', false, ['deriveKey']);
    var key = await crypto.subtle.deriveKey(
      { name: 'PBKDF2', salt: salt, iterations: 200000, hash: 'SHA-256' },
      pwKey, { name: 'AES-GCM', length: 256 }, false, ['decrypt']);
    var pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: iv }, key, ct);
    return new TextDecoder().decode(pt);
  }
  document.querySelectorAll('.lecture-card[data-locked]').forEach(function (card) {
    card.addEventListener('click', function (e) {
      e.preventDefault();
      var pw = window.prompt('비공개 자료입니다. 비밀번호를 입력하세요.');
      if (!pw) return;
      pw = pw.replace(/[０-９]/g, function (c) { return String.fromCharCode(c.charCodeAt(0) - 0xFEE0); }).trim();
      unlock(card.getAttribute('data-locked'), pw).then(function (url) {
        if (/^https:\/\/[\x21-\x7e]+$/.test(url)) {
          window.open(url, '_blank', 'noopener');
        } else {
          alert('비밀번호가 올바르지 않습니다.');
        }
      }).catch(function () {
        alert('비밀번호가 올바르지 않습니다.');
      });
    });
  });
})();
</script>
{% endraw %}
