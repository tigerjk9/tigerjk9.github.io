---
title: "Claude Code 실무 활용 — 교육자 워크숍"
layout: lecture
lecture_slug: claude-code-edu
permalink: /lectures/claude-code-edu/
date: 2026-04-29
author_profile: false
toc: true
toc_sticky: true
---

> **원작자**: 황민호 (Forward Deployed Engineer, Kakao AI Studio) · 2026-04-29  
> 본 자료는 황민호님이 제작한 강의자료를 교육자 대상으로 재구성한 아카이브입니다.

## 강의 개요

Claude Code를 교육 현장에서 실무로 활용하는 방법을 다루는 2시간 워크숍 자료.  
**22개 기능**을 Basic 12개 + Advanced 10개 두 트랙으로 구성한다.

| 항목 | 내용 |
|------|------|
| 대상 | Claude Code를 처음 접하거나 체계적으로 활용하고 싶은 교육자 |
| 시간 | 120분 (Basic 50분 + 휴식 7분 + Advanced 48분 + 종합 9분) |
| 환경 | Windows PowerShell (macOS·Linux 명령 미사용) |
| 산출물 | CLAUDE.md · settings.json deny 룰 · SKILL.md 각 1개 |

## 자료 다운로드

- [슬라이드 보기 (Reveal.js)](/assets/lectures/claude-code-edu/slides.html){:target="_blank"}
- [핸드아웃 (A4 HTML)](/assets/lectures/claude-code-edu/handout.html){:target="_blank"}

## Basic 트랙 (12기능 · 50분)

모든 교육자를 위한 일상 도구.

| # | 기능 | 핵심 메시지 |
|---|------|------------|
| 1 | [CLAUDE.md + @import](/lectures/claude-code-edu/claudemd/) | 매 세션 시스템 프롬프트 복붙을 0으로 |
| 2 | [Auto Memory](/lectures/claude-code-edu/auto-memory/) | 내가 정정한 걸 다음 세션에 기억. 내 디스크 마크다운으로 보관 |
| 3 | [Plan Mode](/lectures/claude-code-edu/plan-mode/) | 변경 전 계획만 받는 안전망 모드 |
| 4 | [Permission Modes (6종)](/lectures/claude-code-edu/permission-modes/) | AI 자율성을 다이얼로 조절 |
| 5 | [Skills (`/skill-name`)](/lectures/claude-code-edu/skills/) | 한 번 정의 후 한 줄 호출 |
| 6 | [Subagents](/lectures/claude-code-edu/subagents/) | 전문 역할 AI를 분리해 병렬 운용 |
| 7 | [`/agents` Library/Running](/lectures/claude-code-edu/agents-panel/) | 서브에이전트 컨트롤 패널 |
| 8 | [`/compact` · `/clear`](/lectures/claude-code-edu/compact-clear/) | 컨텍스트 압축과 초기화 |
| 9 | [`/usage`](/lectures/claude-code-edu/usage/) | 토큰·비용·세션 통계 |
| 10 | [`--continue` · `--resume`](/lectures/claude-code-edu/continue-resume/) | 끊긴 세션 한 줄에 부활 |
| 11 | [Agent Teams](/lectures/claude-code-edu/agent-teams/) | 다수 에이전트 협업 (실험 기능) |
| 12 | [`.claude/rules/` + paths 글롭](/lectures/claude-code-edu/claude-rules/) | 토픽별 룰 자동 로드 |

## Advanced 트랙 (10기능 · 48분)

자동화·외부 연동으로 확장하고 싶은 분을 위한 트랙.

| # | 기능 | 핵심 메시지 |
|---|------|------------|
| 1 | [헤드리스 모드 (`-p` + JSON)](/lectures/claude-code-edu/headless/) | 셸 한 줄로 AI를 파이프라인에 |
| 2 | [Hooks (라이프사이클)](/lectures/claude-code-edu/hooks/) | 30+ 이벤트에 자동 핸들러 부착 |
| 3 | [MCP](/lectures/claude-code-edu/mcp/) | GitHub·Slack·DB 등 외부 시스템 연결 |
| 4 | [Plugins](/lectures/claude-code-edu/plugins/) | 스킬·에이전트·훅을 한 패키지로 배포 |
| 5 | [Routines (클라우드 영구)](/lectures/claude-code-edu/routines/) | 노트북이 꺼져도 도는 무인 작업 |
| 6 | [`/ultrareview` · `/ultraplan`](/lectures/claude-code-edu/ultrareview/) | 다중 에이전트 병렬 검토·계획 |
| 7 | [`/loop`](/lectures/claude-code-edu/loop/) | 한 프롬프트를 인터벌마다 반복 |
| 8 | [`/schedule`](/lectures/claude-code-edu/schedule/) | 자연어로 cron 등록 |
| 9 | [`/effort`](/lectures/claude-code-edu/effort/) | 추론 강도 5단계 조절 |
| 10 | [UX 보조 5종](/lectures/claude-code-edu/ux-helpers/) | `/powerup` · `/focus` · `/copy` 등 |

## 진도 위험 시 압축 우선순위

**절대 보호 (4기능)**: CLAUDE.md · Plan Mode · Permission Modes · Skills  
**자를 수 있는 순서**: Agent Teams → `/agents` → `/compact·/clear` → `/usage` → `--resume`

## 출처

원작: 황민호 (Forward Deployed Engineer, Kakao AI Studio), 2026-04-29  
아카이브 구성: tigerjk9.github.io
