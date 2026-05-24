---
title: "강의자료 아카이브"
permalink: /lectures/
layout: single
author_profile: false
toc: false
---

개발자·연구자 원본 자료를 **교실 어휘로 다시 적은** 교육자 큐레이션 아카이브.  
원작자의 통찰은 그대로, 사례·과제·체크리스트는 학교 현장 맥락으로 재배치한 버전을 모은다.

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
      <span>{{ lecture.audience }}</span> · <span>{{ lecture.duration_min }}분</span> · <span>{{ lecture.feature_count }}개 기능</span>
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
