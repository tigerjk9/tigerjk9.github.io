---
title: "교사와 학부모를 위한 바이브코딩"
layout: lecture
permalink: /lectures/vibe-coding-teachers-parents/
date: 2026-07-21
author_profile: false
toc: true
toc_sticky: true
header:
  teaser: /assets/lectures/vibe-coding-teachers-parents/cover.jpg
  og_image: /assets/lectures/vibe-coding-teachers-parents/cover.jpg
---

AI에게 자연어로 지시해 소프트웨어를 만드는 바이브코딩을, 교사와 학부모가 코딩 경험 없이 실습으로 익히는 워크숍 자료다. 도구는 Gemini 하나이며, 곱셈 웹앱부터 임시정부 이동경로 지도, 학습지·챗봇까지 수업에 바로 쓰는 결과물을 직접 만든다. 슬라이드 28장 전체를 아래 PDF로 내려받을 수 있고, 주요 슬라이드는 그 아래 갤러리에서 바로 넘겨볼 수 있다.

## 강의 개요

| 항목 | 내용 |
|------|------|
| 원작 워크숍 | math-tong — 「교사와 학부모를 위한 바이브코딩」 |
| 도구 | Gemini(제미나이) — 자연어 대화로 웹앱 생성·수정 |
| 기반 | 책 《교사와 학부모를 위한 바이브 코딩》 (황건호·신종환·김형규·김명휘, 씨마스21) |
| 대상 | 교사 · 학부모 · 비전공 입문자 (코딩 경험 불필요) |
| 분량 | 슬라이드 28장 · 3부 실습 구성 |
| 큐레이션 | 김진관 (닷커넥터) |

## 자료 내려받기

- **[슬라이드 전체 내려받기 (PDF · 28장 · 약 2MB)](/assets/lectures/vibe-coding-teachers-parents/slides.pdf){:target="_blank"}**
- **[편집용 파워포인트 내려받기 (PPTX · 28장 · 약 0.5MB)](/assets/lectures/vibe-coding-teachers-parents/slides.pptx){:target="_blank"}** — 학교·수업에 맞게 자유롭게 수정

## 도입 — 말이 결과를 만든다

바이브코딩의 핵심은 감이 아니라 지시의 구체성이다. 몰라서 못 만드는 것이 아니라 정확히 말하지 못해서 못 만든다. 무엇을 만들지 학년·범위·방식으로 구체화하고, 결과를 보며 증상을 말해 고치고, 색·타이포·톤을 시스템으로 넘기는 세 가지 문법이 전부다. 실습 전에는 Gemini 한도에 대비해 구글 계정을 여유 있게 준비하고, 창 전환·새 채팅 요령은 joo.is/vibe0707 규칙을 따른다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p001.jpg" alt="슬라이드 1 표지">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p002.jpg" alt="슬라이드 2 강의 개요">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p003.jpg" alt="슬라이드 3 바이브코딩이란">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p004.jpg" alt="슬라이드 4 오늘 만들 다섯 가지">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p005.jpg" alt="슬라이드 5 실습 준비물">
</div>

## Part 1 — 곱셈 웹앱

같은 곱셈 앱이라도 대화의 결이 결과물의 격을 가른다. 1단계는 학년·범위·계산 방식을 명시해 기능을 세우고, 2단계는 쓰는 사람을 묘사해 디자인을 맞추며, 3단계는 색상코드·타이포·톤을 표로 정리해 넘겨 완성도를 올린다. 프롬프트를 구조로 다루는 감각을 여기서 익힌다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p006.jpg" alt="슬라이드 6 Part 1 곱셈 웹앱">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p007.jpg" alt="슬라이드 7 1단계 기본 프롬프트">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p008.jpg" alt="슬라이드 8 2단계 취향 반영">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p009.jpg" alt="슬라이드 9 3단계 디자인 시스템">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p010.jpg" alt="슬라이드 10 Part 1 정리">
</div>

## Part 2 — 임시정부 이동경로 지도 웹앱

leaflet.js로 만드는 인터랙티브 역사 지도다. 성취기준 [10한사2-01-05]에서 출발해 상하이부터 충칭까지 여덟 도시를 마커와 빨간 점선으로 잇는다. 지도가 안 나타나면 증상을 그대로 말해 고치고, 반응형으로 다듬은 뒤에는 세 단계 퀴즈로 게임화하고 활동지·루브릭까지 확장한다. 마지막에는 빈칸만 바꾸면 어떤 주제에도 쓰는 재사용 템플릿 프롬프트로 정리한다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p011.jpg" alt="슬라이드 11 Part 2 지도 웹앱">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p012.jpg" alt="슬라이드 12 교육과정 연결">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p013.jpg" alt="슬라이드 13 여덟 도시 경로">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p014.jpg" alt="슬라이드 14 기본 프롬프트">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p015.jpg" alt="슬라이드 15 반복 개선">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p016.jpg" alt="슬라이드 16 대장정 시뮬레이션">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p017.jpg" alt="슬라이드 17 수행평가 확장">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p018.jpg" alt="슬라이드 18 재사용 템플릿">
</div>

## Part 3 — 확장: 학습지·GEMS·튜터·챗봇

한 번 익힌 문법으로 과목과 형식을 넓힌다. 영단어 방탈출 웹앱에 손글씨 노트 디자인을 입히고, 서버 없이 구글 시트로 기록을 저장한다. 정보 교과에서는 설명·체험 두 모드를 갖춘 알고리즘 시각화 튜터를, 이어서 페르소나·모드·시각 피드백·고정 버튼 네 요소로 나만의 재귀함수 챗봇을 만든다. Notion 디자인 프롬프트 갤러리에서 원하는 분위기를 골라 붙이면 톤이 잡힌다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p019.jpg" alt="슬라이드 19 Part 3 확장">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p020.jpg" alt="슬라이드 20 방탈출 웹앱과 디자인">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p021.jpg" alt="슬라이드 21 구글 시트 연동">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p022.jpg" alt="슬라이드 22 알고리즘 시각화 튜터">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p023.jpg" alt="슬라이드 23 나만의 챗봇">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p024.jpg" alt="슬라이드 24 디자인 프롬프트 갤러리">
</div>

## 정리와 다음 걸음

기억할 문법은 네 가지다. 구체화, 반복, 디자인 시스템, 교육과정 연결. 교사는 성취기준에 맞춘 자료를 그날 수업에 맞게 만들고, 학부모는 아이의 취향·수준에 맞춘 앱을 함께 만든다. 도구를 만드는 경험 자체가 가장 좋은 배움이 된다. 이후에는 나만의 주제로 템플릿을 채우고, 개인정보·저작권에 유의해 공유하며 계속 만든다.

<div class="slide-gallery">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p025.jpg" alt="슬라이드 25 왜 교사·학부모가">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p026.jpg" alt="슬라이드 26 핵심 원리 네 가지">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p027.jpg" alt="슬라이드 27 다음 걸음">
<img loading="lazy" src="/assets/lectures/vibe-coding-teachers-parents/slides/p028.jpg" alt="슬라이드 28 출처와 크레딧">
</div>

## 출처와 크레딧

- 원작 워크숍: math-tong — 「교사와 학부모를 위한 바이브코딩」 (Padlet)
- 책: 《교사와 학부모를 위한 바이브 코딩》 황건호·신종환·김형규·김명휘 · 씨마스21
- 프롬프트 갤러리·템플릿: vibecoding25 (Notion)
- 실습 안내: joo.is/vibe0707
- 큐레이션: 김진관 (닷커넥터) — 원작자의 워크숍을 강의 슬라이드로 다시 정리한 버전

{% raw %}
<script>
(function(){
  var imgs = Array.prototype.slice.call(document.querySelectorAll('.slide-gallery img'));
  if(!imgs.length) return;
  var ov = document.createElement('div');
  ov.className = 'slb-overlay';
  ov.innerHTML =
    '<button class="slb-close" aria-label="닫기">×</button>' +
    '<button class="slb-prev" aria-label="이전 슬라이드">‹</button>' +
    '<img alt="확대 슬라이드">' +
    '<button class="slb-next" aria-label="다음 슬라이드">›</button>' +
    '<div class="slb-counter"></div>';
  document.body.appendChild(ov);
  var big = ov.querySelector('img'),
      counter = ov.querySelector('.slb-counter'),
      cur = 0;
  function show(i){ cur = (i + imgs.length) % imgs.length; big.src = imgs[cur].src; counter.textContent = (cur + 1) + ' / ' + imgs.length; }
  function open(i){ show(i); ov.classList.add('open'); document.body.style.overflow = 'hidden'; }
  function close(){ ov.classList.remove('open'); document.body.style.overflow = ''; }
  imgs.forEach(function(im, i){ im.style.cursor = 'zoom-in'; im.addEventListener('click', function(){ open(i); }); });
  ov.querySelector('.slb-close').addEventListener('click', close);
  ov.querySelector('.slb-prev').addEventListener('click', function(e){ e.stopPropagation(); show(cur - 1); });
  ov.querySelector('.slb-next').addEventListener('click', function(e){ e.stopPropagation(); show(cur + 1); });
  ov.addEventListener('click', function(e){ if(e.target === ov) close(); });
  document.addEventListener('keydown', function(e){
    if(!ov.classList.contains('open')) return;
    if(e.key === 'Escape') close();
    else if(e.key === 'ArrowLeft') show(cur - 1);
    else if(e.key === 'ArrowRight') show(cur + 1);
  });
})();
</script>
{% endraw %}
