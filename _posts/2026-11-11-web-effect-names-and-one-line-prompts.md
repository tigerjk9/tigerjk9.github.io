---
title: "AI에게 홈페이지 효과를 주문하는 이름과 한 줄 프롬프트 25개"
date: 2026-11-11 14:05:00 +0900
categories: [바이브코딩]
tags: [바이브코딩, 프롬프트엔지니어링, 생성형AI, 디자인, 웹앱]
description: "AI로 홈페이지를 만들 때 화면이 좀 살아 움직이게 해 달라고 쓰면 무엇이 나올지 알 수 없다. 효과의 이름을 부르고 간격, 시간, 크기를 숫자로 적으면 요청이 한 줄로 끝난다. 그대로 붙여 넣을 수 있는 프롬프트 25개를 쓰는 자리별로 묶었다."
permalink: /post/web-effect-names-and-one-line-prompts/
---

AI로 홈페이지를 만들 때 "화면이 좀 살아 움직이게 해 줘"라고 쓰면 무엇이 나올지 알 수 없다. 효과의 이름을 부르고 간격, 시간, 크기를 숫자로 적으면 요청이 한 줄로 끝난다. 결과가 마음에 들지 않을 때도 "간격을 0.08초에서 0.05초로 줄여 줘"처럼 숫자만 바꿔 다시 주문하면 된다.

아래 스물다섯 줄은 그대로 붙여 넣어 쓸 수 있다. 숫자는 출발점이니 화면을 보며 고친다. 구현 수단까지 적은 줄은 AI가 무거운 라이브러리를 끌어오지 않고 브라우저 기본 기능으로 만들게 하려는 것이다.

## 등장

| 번호 | 이름 | 한 줄 프롬프트 | 쓰는 자리 |
|------|------|----------------|-----------|
| 1 | 스태거 등장 (Staggered entrance) | "제목과 문단을 아래에서 위로, 0.08초 간격으로 하나씩 페이드 인해 줘" | 첫 화면의 제목과 소개문 |
| 2 | 스크롤 리빌 (Scroll reveal) | "각 섹션이 화면에 20% 들어오면 아래 24px에서 올라오며 0.6초 동안 나타나게, IntersectionObserver로 한 번만 실행해 줘" | 길게 이어지는 소개 페이지 |
| 3 | 마스크 리빌 (Mask reveal) | "이미지가 왼쪽에서 오른쪽으로 0.8초 동안 닦아 내듯 드러나게, clip-path의 inset()으로 해 줘" | 대표 이미지, 작품 사진 |
| 4 | 카운트업 (Count-up) | "숫자가 화면에 보이면 0부터 목표값까지 1.5초 동안 부드럽게 올라가게 해 줘" | 참여 인원, 누적 건수 |

## 글자

| 번호 | 이름 | 한 줄 프롬프트 | 쓰는 자리 |
|------|------|----------------|-----------|
| 5 | 타이핑 (Typewriter) | "헤드라인을 한 글자씩 타이핑하고, 끝에서 커서가 깜빡이게 해 줘" | 첫 화면 헤드라인 |
| 6 | 텍스트 스크램블 (Text scramble) | "글자가 무작위 문자로 섞이다가 왼쪽부터 원래 글자로 맞춰지게 해 줘" | 짧은 구호, 메뉴 이름 |

글자에만 거는 효과는 종류가 더 많다. 블러 리빌, 형광펜 효과 같은 이름은 [글자 효과 이름 8개](/post/text-effect-names-for-ai-prompting/)에 따로 모아 두었다.

## 배경과 장식

| 번호 | 이름 | 한 줄 프롬프트 | 쓰는 자리 |
|------|------|----------------|-----------|
| 7 | 오로라 그라데이션 (Aurora gradient) | "파란 빛 덩어리 3개가 배경에서 천천히 떠다니게, 블러는 크게 줘" | 첫 화면 배경 |
| 8 | 파티클 네트워크 (Particle network) | "점 80개가 천천히 떠다니고, 가까운 점끼리 선으로 이어지게 canvas로 만들어 줘" | 기술, 연결을 다루는 페이지 배경 |
| 9 | 그레인 텍스처 (Grain texture) | "배경 전체에 SVG feTurbulence로 만든 노이즈를 불투명도 8%로 얹어서 종이 같은 질감을 내 줘" | 밋밋한 단색, 그라데이션 배경 |
| 10 | 무한 마키 (Infinite marquee) | "로고 줄이 끊김 없이 왼쪽으로 흐르다가, 마우스를 올리면 멈추게 해 줘" | 협력 기관 로고, 후기 한 줄 |
| 11 | 라인 드로잉 (Line drawing) | "아이콘 외곽선이 펜으로 그리듯 나타나게, stroke-dashoffset으로 해 줘" | 아이콘, 로고, 손그림 도해 |

## 카드와 마우스

| 번호 | 이름 | 한 줄 프롬프트 | 쓰는 자리 |
|------|------|----------------|-----------|
| 12 | 글래스모피즘 (Glassmorphism) | "카드 배경을 반투명하게, 뒤가 20px 블러로 비치고 얇은 흰 테두리를 넣어 줘" | 사진이나 그라데이션 위에 얹는 카드 |
| 13 | 3D 틸트 카드 (3D tilt card) | "마우스 위치에 따라 카드가 최대 10도 기울고, 빛 반사가 따라오게 해 줘" | 대표 카드 한두 장 |
| 14 | 호버 리프트 (Hover lift) | "카드에 마우스를 올리면 0.2초 동안 6px 떠오르고 그림자가 짙어지게 해 줘" | 누를 수 있는 카드 목록 |
| 15 | 마그네틱 버튼 (Magnetic button) | "커서가 버튼 80px 안에 들어오면 버튼이 커서 쪽으로 최대 12px 끌려오고, 벗어나면 제자리로 돌아가게 해 줘" | 신청하기 같은 핵심 버튼 하나 |
| 16 | 커서 스포트라이트 (Cursor spotlight) | "카드 위에서 커서를 따라다니는 지름 300px짜리 은은한 빛을 radial-gradient로 깔아 줘" | 어두운 배경의 카드 묶음 |
| 17 | 벤토 그리드 (Bento grid) | "기능 소개 6개를 4열 그리드에 크기가 다른 카드로 배치해 줘. 큰 카드는 2칸을 차지하고 간격은 16px, 모서리는 24px로 둥글게" | 기능과 특징을 한눈에 보여 주는 구역 |

## 스크롤

| 번호 | 이름 | 한 줄 프롬프트 | 쓰는 자리 |
|------|------|----------------|-----------|
| 18 | 패럴랙스 (Parallax) | "스크롤할 때 배경 이미지는 본문의 절반 속도로 움직이게 해 줘" | 큰 사진이 깔린 구역 |
| 19 | 스티키 섹션 (Sticky section, 스크롤텔링) | "왼쪽 설명 3단계가 스크롤되는 동안 오른쪽 이미지는 position: sticky로 화면 위에서 80px 떨어진 자리에 고정하고, 단계마다 이미지를 바꿔 줘" | 사용 방법, 과정 설명 |
| 20 | 스크롤 진행 바 (Scroll progress bar) | "화면 맨 위에 높이 3px짜리 막대를 두고, 스크롤한 만큼 왼쪽부터 차오르게 animation-timeline: scroll()로 만들어 줘" | 긴 글, 안내문 |
| 21 | 가로 스크롤 스냅 (Horizontal scroll snap) | "후기 카드 5장을 가로로 넘기게 하고, 손을 떼면 카드 하나씩 가운데에 멈추게 scroll-snap-type: x mandatory로 해 줘" | 후기, 작품 모음 |

## 화면 전환과 상태

| 번호 | 이름 | 한 줄 프롬프트 | 쓰는 자리 |
|------|------|----------------|-----------|
| 22 | 페이지 전환 (View transition) | "다른 페이지로 넘어갈 때 0.3초 동안 앞뒤 화면이 겹치며 바뀌게 View Transitions로 해 줘. 지원하지 않는 브라우저에서는 그냥 넘어가게" | 여러 페이지로 나뉜 사이트 |
| 23 | 아코디언 (Accordion) | "자주 묻는 질문 5개를 details 태그로 만들고, 같은 name을 줘서 하나를 열면 다른 항목은 닫히게 해 줘" | 자주 묻는 질문, 긴 안내 |
| 24 | 다크 모드 토글 (Dark mode toggle) | "오른쪽 위에 다크 모드 토글을 달아 줘. 처음에는 prefers-color-scheme으로 기기 설정을 따르고, 내가 고른 값은 다음 방문에도 유지하고, 색은 0.2초 동안 바뀌게" | 글을 오래 읽는 사이트 |
| 25 | 스켈레톤 로딩 (Skeleton screen) | "데이터를 불러오는 동안 카드 자리에 회색 상자 3개를 먼저 보여 주고, 밝은 띠가 1.5초마다 왼쪽에서 오른쪽으로 지나가게 해 줘" | 목록을 서버에서 받아 오는 화면 |

## 주문할 때 붙이는 조건

효과를 주문한 줄 뒤에 아래 문장을 이어 붙이면 보기에만 좋고 쓰기에는 불편한 화면을 피할 수 있다.

1. "prefers-reduced-motion: reduce인 기기에서는 움직임을 끄고 완성된 상태만 보여 줘." 이 미디어 특성은 사용자가 기기에서 꼭 필요하지 않은 움직임을 줄이도록 설정했는지 알려 준다.
2. "호버와 커서 효과는 @media (hover: hover)일 때만 적용해 줘." 틸트 카드, 마그네틱 버튼, 커서 스포트라이트는 커서가 있어야 동작한다. 손가락으로 누르는 휴대폰에서는 꺼 두는 편이 깔끔하다.
3. "움직이는 속성은 transform과 opacity로 제한해 줘." web.dev는 애니메이션을 되도록 이 두 속성에 한정하고, 레이아웃이나 페인트를 다시 일으키는 속성은 꼭 필요할 때만 움직이라고 권한다. 너비나 여백처럼 레이아웃을 바꾸는 값을 직접 움직이면 매끄럽게 돌기 어렵다.
4. "5초 넘게 저절로 움직이는 것에는 멈춤 버튼을 달아 줘." 마키, 오로라, 파티클처럼 계속 도는 효과가 여기에 든다. 웹 접근성 지침 WCAG 2.2는 자동으로 시작해 5초 넘게 이어지는 움직임을 사용자가 멈추거나 숨길 수 있어야 한다고 정한다(2.2.2, A 등급). 마우스를 올리면 멈추는 방식은 키보드와 터치 사용자에게 닿지 않는다.
5. "지원하지 않는 브라우저에서는 효과 없이 정상으로 보이게 해 줘." `animation-timeline: scroll()`은 MDN이 최근에야 주요 브라우저에서 쓸 수 있게 된 기능으로 분류하며, 오래된 기기에서는 동작하지 않을 수 있다고 적는다. 페이지 사이의 View Transitions는 같은 출처의 문서끼리만 되고, 떠나는 페이지와 도착하는 페이지 양쪽에 `@view-transition { navigation: auto; }` 규칙이 있어야 한다.

스물다섯 개를 한 페이지에 다 넣을 일은 없다. 첫 화면에 쓸 것 하나, 스크롤에 쓸 것 하나를 골라 붙여 넣고, 숫자를 바꿔 가며 원하는 움직임을 찾는다.

## 출처

- MDN Web Docs, Intersection Observer API. https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
- MDN Web Docs, clip-path. https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path
- MDN Web Docs, feTurbulence. https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feTurbulence
- MDN Web Docs, radial-gradient(). https://developer.mozilla.org/en-US/docs/Web/CSS/gradient/radial-gradient
- MDN Web Docs, grid-column. https://developer.mozilla.org/en-US/docs/Web/CSS/grid-column
- MDN Web Docs, position. https://developer.mozilla.org/en-US/docs/Web/CSS/position
- MDN Web Docs, scroll() (animation-timeline). https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline/scroll
- MDN Web Docs, CSS scroll snap. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_snap
- MDN Web Docs, View Transition API와 Using the View Transition API. https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API/Using
- MDN Web Docs, details 요소. https://developer.mozilla.org/en-US/docs/Web/HTML/Element/details
- MDN Web Docs, prefers-color-scheme. https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme
- MDN Web Docs, prefers-reduced-motion. https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- MDN Web Docs, hover 미디어 특성. https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover
- web.dev, CSS 애니메이션 성능 안내(animations guide). https://web.dev/articles/animations-guide
- W3C, Understanding Success Criterion 2.2.2 Pause, Stop, Hide (WCAG 2.2). https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html
