---
title: "강의자료 아카이브"
permalink: /lectures/
layout: single
author_profile: false
toc: false
---

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
      <span>{{ lecture.audience }}</span> · <span>{{ lecture.duration_min }}분</span>{% if lecture.feature_count %} · <span>{{ lecture.feature_count }}개 기능</span>{% elsif lecture.slide_count %} · <span>{{ lecture.slide_count }}장 · {{ lecture.chapter_count }}챕터</span>{% endif %}
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
