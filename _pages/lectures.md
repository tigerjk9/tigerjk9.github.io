---
title: "강의자료 아카이브"
permalink: /lectures/
layout: single
author_profile: false
toc: false
---

## 워크숍 강의

{% if site.data.lectures.size == 0 %}
<p>아직 등록된 강의가 없습니다.</p>
{% else %}
<div class="lecture-card-grid">
{% for lecture in site.data.lectures %}
  <a href="{{ lecture.hub_url }}" class="lecture-card">
    {% if lecture.thumbnail %}<img src="{{ lecture.thumbnail }}" alt="{{ lecture.title }}">{% endif %}
    {% if lecture.curator %}<span class="card-badge">교육자 큐레이션</span>{% endif %}
    <div class="card-title">{{ lecture.title }}</div>
    <div class="card-meta">
      <span>{{ lecture.audience }}</span>{% if lecture.duration_min %} · <span>{{ lecture.duration_min }}분</span>{% endif %}{% if lecture.feature_count %} · <span>{{ lecture.feature_count }}개 기능</span>{% elsif lecture.slide_count %} · <span>{{ lecture.slide_count }}장 · {{ lecture.chapter_count }}챕터</span>{% elsif lecture.chapter_count %} · <span>{{ lecture.chapter_count }}개 장</span>{% endif %}
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

AI 멀티에이전트 집필 파이프라인으로 제작한 교육 도서 원고 7권. 카드를 누르면 웹 도서가 새 탭으로 열린다 (1권은 블로그 안에서 바로 읽는다).

<div class="lecture-card-grid">
{% for book in site.data.books %}
  <a href="{{ book.url }}" class="lecture-card book-card"{% if book.external %} target="_blank" rel="noopener"{% endif %}>
    <img src="{{ book.cover }}" alt="{{ book.title }} 표지">
    {% if book.status == "최신" %}<span class="card-badge">최신</span>
    {% elsif book.status %}<span class="card-badge badge-muted">{{ book.status }}</span>{% endif %}
    <div class="card-id">제{{ book.volume }}권{% if book.external %} · 웹 도서 ↗{% endif %}</div>
    <div class="card-title">{{ book.title }}</div>
    <div class="card-meta">{{ book.audience }}</div>
    <div class="card-meta">{{ book.structure }}</div>
  </a>
{% endfor %}
</div>
