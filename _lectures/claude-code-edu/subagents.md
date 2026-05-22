---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-018
feature_name: "Subagents"
title: "Subagents"
track: basic
order: 6
permalink: /lectures/claude-code-edu/subagents/
---

## 정의

Subagents는 메인 세션의 컨텍스트를 오염시키지 않고 별도 컨텍스트 윈도우에서 작업한 뒤 요약만 돌려주는 전문 AI다. `.claude/agents/<name>.md`에 YAML 프론트매터와 본문으로 정의하고, 통계 검토만 잘하는 동료·영문 첨삭만 잘하는 동료를 분리해 둔다.

## 핵심 동작

- 프론트매터 필드. `name`·`description`·`tools`(허용 도구 화이트리스트)·`model`·`mcpServers`·`hooks`·`initialPrompt`(첫 턴 자동 제출)·`skills`(시작 시 풀 콘텐츠 프리로드)
- `isolation: worktree`로 자체 worktree에서 격리 작업 후 변경 없으면 자동 정리
- 호출 방법 두 가지. 자연어 `use the paper-deep-reviewer subagent to check ./drafts/`, 또는 `claude --agent <name>` 메인 스레드 에이전트로 띄우기
- 같은 에이전트를 여러 인스턴스로 동시에 띄울 수 있다

## 사용법

`.claude/agents/paper-deep-reviewer.md`.

```markdown
---
name: paper-deep-reviewer
description: 논문 한 편을 통계·인용·논리 3관점에서 비판적으로 검토. 사용 시점 — 자기 논문 초고를 보내기 전
tools: Read, Grep, Glob
model: opus
isolation: worktree
initialPrompt: "이 폴더의 모든 .md 논문 초고를 찾아 검토 시작"
skills:
  - 활동지요약
---

당신은 IF 10+ 저널 reviewer 2이다. 통계 가정·표본 크기·인용 누락·논리 비약을 지적하라.
```

호출.

```text
/agents
use the paper-deep-reviewer subagent to check ./drafts/
```

## 강사 멘트

> Subagents의 핵심은 컨텍스트 격리다. 통계 검토만 시키는 에이전트를 만들면, 그 에이전트는 통계 말고 다른 맥락이 없으니 더 집중된 답이 나온다. 스킬과의 차이는 — 스킬은 "절차의 재사용", Subagent는 "역할의 분리". 같이 써도 된다. 모범 프롬프트 #2를 그대로 쓴다. `tools` 화이트리스트가 핵심이다 — 통계 검토 에이전트가 파일을 건드리는 일이 없도록 `Read`·`Grep`·`Glob`만 준다. `isolation: worktree`는 메인 세션과 작업 공간을 분리한다. 메인이 오염되지 않는다. user 계층 팁 — 본인 노트북 `~/.claude/agents/`에 두면 어떤 폴더에서든 호출된다. 매번 복사할 필요 없다.

## 실습

`~/.claude/agents/평가루브릭검수자.md`를 만들고 `tools: Read, Grep, Glob`로 권한을 좁힌 뒤, 작성한 평가 루브릭을 그 에이전트에게 검토시킨다. 같은 에이전트의 다른 인스턴스를 동시에 띄워 다른 루브릭을 병렬 검토할 수 있다.

## 활용 시사점

교육 현장에서 Subagents는 다음 세 가지로 활용된다.

- **수업 자료 다관점 검수**. 활동지 한 편을 "학습목표 검수자", "안전 검수자", "차시 분량 검수자" 세 명에게 동시에 보내 결과를 통합한다. 한 사람이 네 관점을 동시에 다 잘 보기는 어렵다 — 분리가 답
- **학생 작품 평가 분리**. 학생 글쓰기를 "내용 검수자", "문법 검수자", "구조 검수자"로 분리 평가하면 한 에이전트의 답이 단순해 정확도가 올라간다
- **isolation: worktree로 메인 세션 보호**. 검수 에이전트가 본인 노트·자료를 만지지 않도록 격리해 두면 안심하고 위임할 수 있다

---

[← 이전 기능](/lectures/claude-code-edu/skills/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/agents-panel/)
