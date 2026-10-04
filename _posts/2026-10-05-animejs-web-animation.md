---
title: "Anime.js, 웹사이트에 움직임을 더하는 자바스크립트 애니메이션 엔진"
date: 2026-10-05 01:14:22 +0900
categories: [기술, 소프트웨어개발]
tags: [Animejs, 자바스크립트, 웹애니메이션, 프론트엔드, UIUX, 개발도구, 오픈소스, 웹개발]
header:
  teaser: /assets/animejs-web-animation-og.jpg
permalink: /post/animejs-web-animation/
---

Anime.js는 웹사이트의 움직임을 만드는 가벼운 자바스크립트 애니메이션 라이브러리다. 이름만 보면 애니메이션 영상을 만드는 도구 같지만, 실제로는 웹 페이지의 버튼, 카드, 텍스트 같은 요소를 움직인다. GitHub 저장소는 별을 약 7.3만 개 받았고, 최신 릴리스는 2026년 6월 22일에 나온 v4.5.0이다.

<figure>
<img src="/assets/animejs-web-animation-og.jpg" alt="Anime.js 공식 사이트 대표 이미지, JavaScript Animation Engine 문구와 기계 부품 선화">
<figcaption>Anime.js 공식 사이트의 대표 이미지. 'JavaScript Animation Engine'이라는 문구 옆에 기계 부품을 그린 선화가 놓여 있다.</figcaption>
</figure>

## Anime.js는 무엇을 움직이나

README는 Anime.js를 빠르고 다목적이며 가벼운 자바스크립트 애니메이션 라이브러리로 소개한다. 단순하면서도 강력한 API 하나로 CSS 속성, SVG, DOM 속성, 자바스크립트 객체를 모두 움직일 수 있다. 무거운 애니메이션 프레임워크를 들이지 않고 랜딩 페이지나 인터랙티브 UI에 움직임을 넣고 싶을 때 특히 쓸모가 있다. 현재 메이저 버전은 V4이고, 설치는 `npm i animejs` 한 줄이면 된다.

## 모듈 구성과 번들 크기

공식 사이트는 Anime.js를 애니메이터를 위한 완전한 도구 상자라고 부른다. 브라우저의 제약에서 벗어나 웹의 무엇이든 하나의 API로 움직이게 한다는 설명이다. 타임라인, 스태거(stagger, 요소마다 시차를 두는 효과), 이징(easing), 반복과 역재생 같은 모션도 비교적 짧은 코드로 구현한다.

기능은 모듈로 나뉘어 있어서 필요한 부분만 가져다 쓰면 번들을 작게 유지할 수 있다. 공식 사이트에 표시된 모듈별 크기는 다음과 같다.

| 모듈 | 크기 | 주요 기능 |
| :--- | :--- | :--- |
| Timer | 5.60 KB | 콜백 예약과 시간 흐름 관리 |
| Animation | +5.20 KB | 핵심 함수 `animate()`로 대상 애니메이션 |
| Timeline | +0.55 KB | 여러 애니메이션의 순서 조율과 콜백 동기화 |
| Animatable | +0.40 KB | 자주 바뀌는 값을 효율적으로 애니메이션 |
| Draggable | +6.41 KB | 요소 드래그, 스냅, 플릭, 던지기 |
| Scroll | +4.30 KB | 스크롤에 맞춘 애니메이션 동기화와 시작 |
| Scope | +0.22 KB | 미디어 쿼리에 반응하는 애니메이션 |
| SVG | 0.35 KB | 도형 모핑, 선 그리기, 모션 경로 |
| Stagger | +0.48 KB | 시간·값·타임라인 위치를 요소마다 엇갈리게 배분 |
| Spring | 0.52 KB | 용수철처럼 튕기는 움직임 |
| WAAPI | 3.50 KB | 브라우저 내장 Web Animations API로 애니메이션 실행 |

사이트에 표시된 전체 번들 크기는 27.13 KB다.

## API 살펴보기

기본 API는 속성별 매개변수, 유연한 키프레임 시스템, 내장 이징 함수를 갖췄다. 변환(transform)은 개별 CSS transform 속성을 섞어 쓰는 합성(composition) API로 다루며, 함수로 계산한 값과 블렌드(blend) 합성을 지원한다.

스크롤 옵저버(Scroll Observer) API는 스크롤에 맞춰 애니메이션을 동기화하거나 시작한다. 여러 동기화 모드와 세밀한 임계값, 콜백 세트를 제공한다. 내장 `stagger` 함수는 시간, 값, 타임라인 위치를 요소마다 엇갈리게 나눠 주어 여러 요소가 차례로 움직이는 효과를 금방 만든다.

SVG 도구는 도형 모핑(shape morphing), 선 그리기(line drawing), 모션 경로(motion path)를 기본으로 지원한다. Draggable API로는 HTML 요소를 끌고, 맞춰 붙이고(snap), 튕기고(flick), 던질 수 있으며, 놓을 때의 움직임에 스프링을 걸 수 있다.

V4는 ES 모듈을 가져와 쓴다. README의 사용 예시는 다음과 같다.

```javascript
import {
  animate,
  stagger,
} from 'animejs';

animate('.square', {
  x: 320,
  rotate: { from: -180 },
  duration: 1250,
  delay: stagger(65, { from: 'center' }),
  ease: 'inOutQuint',
  loop: true,
  alternate: true
});
```

이 코드는 `.square` 클래스 요소들을 x축으로 320px 옮기면서 -180도에서 원래 각도로 회전시킨다. 한 번 움직이는 데 1,250ms가 걸리고, 각 요소는 가운데 요소부터 65ms씩 늦게 출발한다. 이징은 `inOutQuint`이며, `loop: true`와 `alternate: true` 때문에 갔다가 돌아오기를 끝없이 반복한다.

타임라인 API(`createTimeline`)는 여러 애니메이션의 순서를 정밀하게 맞추고 콜백을 동기화한다. Scope API(`createScope`)는 미디어 쿼리에 반응하는 애니메이션을 만들어 화면 방향이나 크기에 따라 움직임을 바꾼다.

## 개발과 지원

Anime.js는 줄리안 가르니에(Julian Garnier)가 만든 MIT 라이선스 오픈소스다. README는 이 프로젝트가 100% 무료이며 후원자들 덕분에 유지된다고 밝히고, GitHub Sponsors로 후원을 받는다. V4 문서는 공식 사이트에, v3에서 v4로 옮기는 마이그레이션 가이드는 GitHub 저장소 위키에 있다.

## 연극의 미장센과 웹 애니메이션

웹 애니메이션은 연극과 영화에서 말하는 미장센(mise-en-scène)과 닮았다. 미장센은 무대 위 배우의 동선, 소품, 조명, 색채를 의도에 맞게 배치해 분위기를 만들고 이야기를 전하는 방식이다. 웹 애니메이션도 사용자의 시선을 이끌고, 중요한 정보를 드러내고, 다음 행동을 유도한다. Anime.js 같은 도구는 화면 위 요소들의 움직임을 안무하듯 짜는 데 쓰인다.

## 출처
- juliangarnier/anime, GitHub 저장소. https://github.com/juliangarnier/anime
- Anime.js 공식 사이트. https://animejs.com
