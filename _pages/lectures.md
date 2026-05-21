---
title: "강의자료 아카이브"
permalink: /lectures/
layout: single
author_profile: false
toc: false
---

강의자료를 검색·필터·재방문 가능한 형태로 큐레이션한 아카이브.

{% if site.data.lectures.size == 0 %}
<p>아직 등록된 강의가 없습니다.</p>
{% else %}
<div class="lecture-card-grid">
{% for lecture in site.data.lectures %}
  <a href="{{ lecture.hub_url }}" class="lecture-card">
    {% if lecture.thumbnail %}<img src="{{ lecture.thumbnail }}" alt="{{ lecture.title }}">{% endif %}
    <div class="card-title">{{ lecture.title }}</div>
    <div class="card-meta">
      <span>{{ lecture.audience }}</span> · <span>{{ lecture.duration_min }}분</span> · <span>{{ lecture.feature_count }}개 기능</span>
    </div>
  </a>
{% endfor %}
</div>
{% endif %}
