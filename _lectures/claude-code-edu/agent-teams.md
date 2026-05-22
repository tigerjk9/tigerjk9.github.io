---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-028
feature_name: "Agent Teams (실험 기능)"
title: "Agent Teams (실험 기능)"
track: basic
order: 11
permalink: /lectures/claude-code-edu/agent-teams/
---

## 정의

Agent Teams는 한 lead 세션이 다른 Claude Code 세션 N개(teammates)를 띄우고, 공유 task list·메일박스로 협업하는 실험 기능이다. 서브에이전트와 달리 teammates 간 직접 통신이 가능하다. 환경 변수 한 줄로 켜고 끈다.

## 핵심 동작

- 활성. `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`을 settings.json `env` 또는 환경 변수에 설정. v2.1.32+
- 표시 모드 3종. `in-process`(한 터미널에서 `Shift+Down` 사이클), `tmux/iTerm2`(분할 패널), `auto`(기본 — tmux 안이면 분할)
- 자연어로 팀 만들기. "create an agent team to review PR #142. Spawn three reviewers — security / performance / test coverage"
- Teammates는 본인의 lead 세션과 별도 컨텍스트, 같은 프로젝트 CLAUDE.md·MCP·skills를 자동 로드
- 품질 게이트. `TeammateIdle`·`TaskCreated`·`TaskCompleted` 훅으로 통제
- 상태 저장. `~/.claude/teams/<name>/config.json`, `~/.claude/tasks/<name>/`

## 사용법

settings.json.

```json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```

세션 안에서.

```text
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes. Use Sonnet 4.6.

Spawn a teammate using the security-reviewer agent type to audit the auth module.
```

명령어.

```powershell
claude --teammate-mode in-process
```

## 강사 멘트

> 실험 기능이라 한 번 더 강조한다 — 환경 변수 한 줄로 켜고 끈다. 토큰이 많이 들어서 일상으로 권하지는 않는다. 다만 한 작업을 세 관점에서 동시에 검토할 때 강력하다. 논문을 자주 쓰거나 활동지 다관점 검수가 필요한 사람에게 잘 맞는다. lead가 task list를 만들면 teammate들이 병렬로 처리하고, 통합 보고는 lead가 담당한다. Basic에서는 데모 한 화면만 보여 준다. 실제 시도는 휴식 뒤에 본인 욕심으로. "있다는 것만". 토큰 모니터링은 `/usage`로.

## 활용 시사점

교육 현장에서 Agent Teams는 다음 두 가지로 활용된다.

- **수업 자료 다관점 검수 시뮬레이션**. 활동지 한 편을 "학습목표 검수자", "안전 검수자", "차시 분량 검수자" 세 명이 동시에 검토하고 결과를 통합한다. 단일 Claude나 ChatGPT는 한 시각만 받지만 agent teams는 의도적으로 충돌하는 시각을 부딪쳐 빈 곳을 덜 남긴다
- **베타 기능 — 토큰 모니터링 필수**. 베타라 토큰 소비가 크다. `/usage`로 모니터링하면서 사용하는 것이 안전하다. 처음 한 번은 작은 작업으로 감각만 익히는 것을 권한다

---

[← 이전 기능](/lectures/claude-code-edu/continue-resume/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/claude-rules/)
