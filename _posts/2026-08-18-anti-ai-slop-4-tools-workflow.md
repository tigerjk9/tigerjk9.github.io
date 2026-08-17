---
title: "AI로 만든 사이트가 자꾸 AI 티 나는 이유, 도구 4개 조합으로 끊는 법"
date: 2026-08-18 00:16:30 +0900
categories: [바이브코딩, AI]
tags: [바이브코딩, UIUX, 디자인, 프론트엔드, AI슬롭, ClaudeCode, FramerMotion]
description: "AI 코딩 도구 하나로 다 해결하려 하면 AI 티가 난다. Claude Code, Framer Motion, UI/UX Pro Max, 21st.dev 4가지를 역할별로 나눠 쓰면 결과물이 달라진다."
permalink: /post/anti-ai-slop-4-tools-workflow/
---

AI로 만든 사이트가 자꾸 AI 티 난다. 버튼이 너무 둥글고, 색은 무난하게 파랗고, 모든 요소가 제자리에서 조용히 앉아 있다. 정적이다. 에너지가 없다. 구체적으로 뭐가 문제인지 짚기 어렵지만 보는 순간 안다. "AI가 만들었겠구나."

## 한 도구로 다 하려는 게 문제다

이유는 단순하다. 구현 도구가 디자인 결정까지 내리기 때문이다.

Claude Code(Anthropic이 만든 터미널 기반 에이전틱 코딩 도구)에게 랜딩 페이지를 만들어 달라고 하면 코드는 나온다. 그런데 그 과정에서 색을 고르고, 버튼 radius를 정하고, 여백 크기를 결정하는 것도 모델이 한다. 모델은 훈련 데이터에서 가장 자주 등장한 패턴을 고른다. `padding-4`, `rounded-md`, `text-blue-600`. 틀리지 않다. 그냥 아무 맥락도 없다.

이걸 AI 슬롭이라 부른다. 통계적으로 평균인 디자인. 아무도 기억하지 않는 색 조합과 여백. 모션이 없어 정적이고, 컴포넌트에 개성이 없어 어디서 본 것 같다.

구현과 디자인 판단을 같은 도구에 몰아주면 이렇게 된다. 둘을 분리해야 한다.

## 4개 도구의 역할 분담

| 도구 | 역할 | 핵심 기능 |
|------|------|-----------|
| Claude Code | 구현 | 코드베이스 전체를 읽고 파일을 생성·수정·삭제하는 터미널 에이전트 |
| UI/UX Pro Max | 디자인 기준 주입 | 스타일 67종, 색상 팔레트 161종, UX 가이드라인 99개를 Claude Code에 장착하는 스킬 |
| 21st.dev | UI 컴포넌트 소스 | React 컴포넌트 레지스트리 — 검증된 컴포넌트를 npm처럼 설치 |
| Framer Motion | 모션 레이어 | React 전용 애니메이션 라이브러리 — 레이아웃 전환, 스크롤 반응, 제스처 처리 |

**Claude Code**는 2025년 5월 정식 출시 이후 AI 코딩 도구 중 가장 널리 쓰이는 축에 속한다. 코드베이스 전체를 컨텍스트로 읽고, 자연어 지시로 여러 파일을 동시에 수정한다. 구현 역할은 여기에 맡긴다. 단, 디자인 결정은 맡기지 않는다.

**UI/UX Pro Max**는 Claude Code에 장착하는 스킬이다. nextlevelbuilder가 GitHub에 오픈소스로 공개했고 Claude Code, Cursor, Windsurf 등 15개 이상 도구에서 쓸 수 있다. 스타일 67종(글래스모피즘, 뉴모피즘, 브루탈리즘, Aurora UI 등), 색상 팔레트 161종, 폰트 페어링 57종, UX 가이드라인 99개가 들어 있다. Claude Code가 디자인 결정을 내릴 때 이 기준을 참조한다. "무난한 파란 버튼" 대신 구체적인 스타일 언어가 생긴다.

**21st.dev**는 React 컴포넌트 레지스트리다. Y Combinator 지원을 받았으며 Tailwind CSS와 Radix UI로 만들어진 컴포넌트를 npm처럼 프로젝트에 바로 설치할 수 있다. Claude Code가 버튼이나 모달을 처음부터 짜게 두지 않는다. AI가 순간적으로 지어낸 컴포넌트 대신, 실제로 검증된 코드를 쓴다는 게 핵심이다.

**Framer Motion**은 React 전용 애니메이션 라이브러리다. 2025년 중반 독립 프로젝트로 분리되며 이름이 Motion으로 바뀌었고(패키지는 `motion/react`), 공식 문서는 motion.dev에 있다. 레이아웃 전환, 요소 등장·소멸, 스크롤 반응, 드래그 제스처를 처리한다. AI 코딩 도구는 정적인 페이지를 잘 짠다. 모션은 명시적으로 지시하지 않으면 나오지 않는다.

## 실제 조합 워크플로

순서가 있다. 아무 단계에서나 시작하면 효과가 반감된다.

**1단계 — UI/UX Pro Max 활성화**. 스킬을 Claude Code에 등록한다. 이후 Claude Code는 스타일 결정 시 스킬 내 기준을 참조한다. "글래스모피즘 스타일로 카드 컴포넌트 만들어"라고 하면 임의 해석 대신 스킬이 정의한 글래스모피즘 스펙을 적용한다.

**2단계 — 21st.dev에서 기초 컴포넌트 설치**. 버튼, 내비게이션 바, 폼, 카드 같은 기초 단위는 Claude Code에게 처음부터 짜게 두지 않는다. 21st.dev에서 필요한 컴포넌트를 찾아 프로젝트에 설치한다. 여기서 설치한 컴포넌트가 페이지의 기준선이 된다.

**3단계 — Claude Code로 레이아웃·로직 구현**. 설치한 컴포넌트를 조합하고, 데이터 흐름을 연결하고, 페이지 구조를 완성한다. 디자인 기준은 UI/UX Pro Max가 이미 주입했다.

**4단계 — Framer Motion으로 모션 추가**. 페이지 진입 애니메이션, 카드 hover, 리스트 아이템 등장, 탭 전환을 명시적으로 설계한다. Claude Code에게 Framer Motion 코드를 짜게 해도 되고 직접 작성해도 된다. 중요한 건 모션 설계 자체를 사람이 결정한다는 점이다.

## 한계와 주의

이 조합이 해결하는 건 하나다. AI 도구가 맥락 없이 내리는 디자인 결정을 줄이는 것.

UI/UX Pro Max가 161개 팔레트를 제공해도 어느 걸 고를지는 사람이 판단해야 한다. 21st.dev에 수천 개 컴포넌트가 있어도 어디에 어떤 배치를 쓸지는 경험에서 나온다. Framer Motion이 스크롤 반응을 지원해도 얼마나 강하게, 어느 타이밍에 쓸지는 안목이 결정한다.

도구를 잘 조합한다고 디자인 감각이 생기지는 않는다. 조합은 AI의 무맥락 판단을 줄이는 장치다. 그 이상은 여전히 쓰는 사람의 몫이다.

## 출처

- [Claude Code — Anthropic](https://claude.ai/code)
- [Motion (Framer Motion) 공식 문서](https://motion.dev)
- [21st.dev](https://21st.dev)
- [UI/UX Pro Max — GitHub](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
- [UI Bakery: What is 21st.dev](https://uibakery.io/blog/what-is-21st-dev)
- [21st.dev — Y Combinator](https://www.ycombinator.com/companies/21st)
