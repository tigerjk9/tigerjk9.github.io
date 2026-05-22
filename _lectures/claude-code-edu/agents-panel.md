---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-039
feature_name: "/agents Library와 Running"
title: "/agents Library와 Running"
track: basic
order: 7
permalink: /lectures/claude-code-edu/agents-panel/
---

## 정의

`/agents`는 정의된 서브에이전트 목록을 보고, 현재 라이브로 도는 인스턴스를 모니터링·제어하는 통합 인터페이스다. Library 탭에는 모든 정의가, Running 탭에는 살아 있는 인스턴스가 라이브 카운터로 표시된다.

## 핵심 동작

- **Library** 탭. 설정·플러그인·`--agents`로 정의된 모든 서브에이전트 목록. Run / View running instance 액션 제공
- **Running** 탭. 현재 라이브 서브에이전트 세션. `● N running` 카운터가 에이전트 타입 옆에 표시된다
- 같은 자리에서 새 에이전트 만들기(Create New subagent) — 식별자·설명·도구·시스템 프롬프트를 GUI로 입력
- 상태 트래킹. pending → in progress → completed

## 사용법

```text
# 라이브러리 + Running 한 화면
/agents

# 자연어 호출
use the code-reviewer subagent to check the auth module
have the debugger subagent investigate why users can't log in
```

## 강사 멘트

> `/agents`는 Subagents의 관제실이다. 정의된 에이전트 다섯 명이 각각 어디서 뭐 하고 있는지 한 화면에 보인다. Library 탭은 정의된 에이전트 목록, Running 탭은 라이브 카운터. 같은 에이전트 인스턴스를 여러 개 동시에 띄울 수도 있다. 본인 일상에서 자주 호출하는 에이전트가 세 개 이상이 되면 `/agents`의 가치가 살아난다.

## 실습

자기 폴더에서 `/agents`를 호출해 Library에 정의된 에이전트 목록과 Running 탭의 실시간 인스턴스를 한 화면에서 확인한다. 같은 에이전트를 두 인스턴스로 동시에 띄워 카운터가 `● 2 running`으로 바뀌는지 본다.

## 활용 시사점

교육 현장에서 `/agents`는 다음 두 가지로 활용된다.

- **에이전트 컨트롤 패널**. 본인이 정의한 5개 에이전트(reviewer·planner·cleaner·영문첨삭·평가루브릭검수자)가 한 화면에 모인다. 추상 개념이던 서브에이전트가 "지금 일하고 있는 동료들 목록"으로 시각화된다
- **병렬 검수 모니터링**. 활동지 5편을 5개 에이전트 인스턴스로 동시에 검수할 때, Running 탭에서 진행 상황을 한눈에 본다

---

[← 이전 기능](/lectures/claude-code-edu/subagents/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/compact-clear/)
