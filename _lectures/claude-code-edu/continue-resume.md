---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-003
feature_name: "--continue 와 --resume"
title: "--continue 와 --resume"
track: basic
order: 10
permalink: /lectures/claude-code-edu/continue-resume/
---

## 정의

`--continue`(`-c`)와 `--resume`(`-r`)은 직전 또는 특정 세션을 ID·이름·검색으로 되살리는 두 플래그다. 회의·수업·이동으로 끊긴 작업을 한 줄에 부활시키는 도구다.

## 핵심 동작

- `--continue`는 현재 디렉터리의 가장 최근 세션을 자동으로 이어 간다
- `--resume`는 ID/이름/피커로 임의 세션을 복구한다
- 세션이 오래되어 다시 읽으면 사용량 한도를 크게 잡아먹을 만큼 크면, 풀 트랜스크립트 대신 "요약본에서 재개" 옵션을 제시한다
- `--name`(`-n`)으로 이름 단 세션은 `--resume <name>`으로 즉시 복귀
- `--fork-session`을 추가하면 같은 시작점에서 새 세션 ID로 분기. "이 시점에서 두 가지 다른 결론을 시도"할 때 사용
- 피커 안에서 `Ctrl+A`는 모든 프로젝트 세션, `Ctrl+W`는 모든 worktree 세션을 펼친다

## 사용법

```powershell
# 시작 시 이름 부여
claude -n 2026-Q2-paper

# 마지막 세션 이어가기
claude --continue

# 이름으로 부활
claude --resume 2026-Q2-paper

# ID로 부활 + 새 세션으로 분기
claude --resume 550e8400-e29b-41d4-a716-446655440000 --fork-session

# 헤드리스에서도 가능
claude --continue -p "Now focus on the database queries"
```

## 강사 멘트

> 분석·수업 준비를 자주 하는 사람의 일상이다. 오전 분석을 오후에 이어 가는 건 매일 일어나는 시나리오다. 매번 처음부터 설명하면 30분이 날아간다. 세션에 이름을 붙이는 습관(`-n`)을 들이면 `--resume`이 편해진다. "2026-Q2-paper" 같은 식이다. `--fork-session`은 같은 시점에서 두 결론을 비교하고 싶을 때 쓴다. 학교 일상 그대로 — 오전에 끊기고, 점심 뒤에 이어 가고, 오후엔 다른 가설로 분기. 한 줄짜리 명령으로 끊긴 맥락을 그대로 이어 가 작업 흐름이 매끄럽다.

## 실습

세션을 `claude -n 2026-Q2-활동지`로 시작해 활동지 1편을 일부 작성한 뒤 `/exit`로 빠져나간다. 다시 `claude --resume 2026-Q2-활동지`로 들어가 같은 맥락이 살아 있는지 확인한다.

## 활용 시사점

교육 현장에서 `--continue`·`--resume`은 다음 세 가지로 활용된다.

- **수업·회의 사이 끊긴 작업 부활**. 오전 활동지 작업 → 1교시 수업 → 오후 이어가기 흐름에서 매번 맥락을 다시 설명할 필요가 없다. `claude -n 2026-Q2-활동지` 한 줄
- **분기 비교**. `--fork-session`으로 "이 시점에서 학생 활동 중심으로 가는 안"과 "교사 시연 중심으로 가는 안"을 분기 비교한다
- **장기 프로젝트 관리**. 연간 평가 계획 같은 장기 작업은 `--name`으로 의미 있는 이름을 붙여 두면 한 학기 뒤에도 한 줄에 부활한다

---

[← 이전 기능](/lectures/claude-code-edu/usage/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/agent-teams/)
