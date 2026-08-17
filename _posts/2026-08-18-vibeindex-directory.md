---
title: "Vibe Index — 바이브 코딩 도구 23만 개를 한 곳에"
date: 2026-08-18 00:13:58 +0900
categories: [바이브코딩, AI]
tags: [바이브코딩, MCP, Claude Code, 스킬, AI도구]
description: "Claude Code용 스킬·MCP 서버·플러그인·마켓플레이스를 한곳에 모은 디렉터리 Vibe Index를 살펴본다."
permalink: /post/vibeindex-directory/
---

Claude Code를 쓰다 보면 금방 벽에 부딪힌다. "이 작업에 딱 맞는 MCP 서버가 있을 텐데"라는 생각이 드는 순간, 검색창을 열고 GitHub와 Reddit을 떠돌기 시작한다. 결국 30분을 쓰고도 제대로 된 도구를 찾지 못한 채 돌아오는 일이 반복된다. 좋은 도구는 분명 있는데, 찾기가 너무 어렵다는 문제다.

[Vibe Index](https://www.vibeindex.ai)는 그 문제에 직접 달려든 사이트다. '혼공 바이브 코딩' 저자 조태호가 만들었고, 이 사이트 자체도 바이브 코딩으로 제작했다.

## 무엇을 모아 놨나

Vibe Index가 다루는 범주는 네 가지다.

- **Skills** — Claude Code에 슬래시 커맨드로 추가하는 작업 단위
- **MCP Servers** — Model Context Protocol 기반 외부 도구 서버
- **Plugins** — AI 어시스턴트 기능을 확장하는 플러그인
- **Marketplaces** — 위 자료들을 유통하는 허브 플랫폼

현재 등록된 자료는 230,921개다. 사이트 메타 설명에 "ultimate directory"라는 표현이 있는데, 숫자만 놓고 보면 과장이 아니다.

## 한글 요약과 Vibe Ranking

단순 나열이 아니라는 점이 이 사이트의 차별점이다. 각 자료에 한글 요약 설명이 붙어 있어 영어 README를 읽지 않아도 쓸모를 파악할 수 있다.

Vibe Ranking은 인기 도구를 500위까지 순위로 보여준다. 트렌딩 항목도 따로 집계한다. 메인 화면에 눈에 띈 항목 몇 가지를 보면 조태호의 기준을 짐작할 수 있다.

andrej-karpathy-skills는 카르파티의 코딩 원칙(Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution) 네 가지를 플러그인으로 구현한 것이다. superpowers는 스펙 우선 설계와 TDD, 서브에이전트 기반 개발을 하나의 워크플로우로 묶었다. Anthropic이 공식 배포한 Git 서버도 있고, Vercel Labs의 스킬 탐색 도구도 있다.

Security Scan 기능은 Cisco와 연계해 도구의 보안 위험을 검사한다. 도구를 설치하기 전에 거르는 단계가 생긴 셈이다.

인터페이스에는 자연어 추천 기능도 있다. "내 프로젝트에 맞는 스킬 추천해줘"라고 입력하면 스킬·MCP·플러그인을 묶어서 제안해 준다. MCP 호환 도구를 검색하고 설치하는 경로도 제공한다.

## 디렉터리가 해결하지 못하는 것

23만 개는 많다. 그리고 그게 문제이기도 하다.

목록이 크다고 큐레이션이 깊은 건 아니다. Vibe Ranking이 인기 순위를 보여줘도, 그 도구가 지금 내 프로젝트에 맞는지는 여전히 직접 써봐야 안다. 한글 요약이 정확한지, 최신 버전을 반영하고 있는지도 보장되지 않는다. 등록 수가 많을수록 품질 분산도 커진다.

취사선택은 결국 사용자 몫이다.

## 바이브 코딩을 시작하는 교사에게

수업에 바이브 코딩을 들여오려는 교사가 가장 먼저 겪는 장벽 중 하나가 도구 탐색이다. Claude Code를 설치했는데 무엇을 더 얹어야 할지 모르겠다는 상황, Vibe Index는 그 출발점으로 쓸 수 있다. 한글 설명이 있으니 영어 장벽도 낮다.

교실에 바로 쓸 수 있는 도구가 있는지 Vibe Ranking 상위 항목부터 살펴보는 것이 가장 빠른 방법이다. 설치 전에 Security Scan을 통과한 도구인지 확인하는 습관도 들여 두면 좋다.

## 출처

- Vibe Index: [https://www.vibeindex.ai](https://www.vibeindex.ai)
