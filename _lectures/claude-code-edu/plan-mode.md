---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-024
feature_name: "Plan Mode"
title: "Plan Mode"
track: basic
order: 3
permalink: /lectures/claude-code-edu/plan-mode/
---

## 정의

Plan Mode는 Claude가 파일과 셸을 읽기만 하고 절대 수정하지 않으면서, 변경 계획을 먼저 작성해 사용자 승인을 받는 워크플로우다. "AI가 멋대로 고쳐 버리면 어쩌지" 라는 가장 큰 우려에 직접 답하는 안전망 모드다.

## 핵심 동작

- 진입 방법 세 가지. `Shift+Tab` 두 번(default → acceptEdits → plan 사이클), 단발 프롬프트 앞에 `/plan`, 또는 시작 시 `claude --permission-mode plan`
- 계획 완료 시 4가지 옵션 제공. 자동 모드로 진행 / acceptEdits로 진행 / 수동 검토로 진행 / 계속 계획
- 계획 텍스트는 `Ctrl+G`로 외부 에디터에서 직접 편집 가능
- 계획 수락 시 세션 이름이 계획 내용 기반으로 자동 명명됨
- Plan 모드에서도 Bash 도구의 읽기 명령(`git status` 등)은 실행. 변경 명령은 보류

## 사용법

```powershell
# 시작 시 강제
claude --permission-mode plan

# 세션 안에서 진입
claude
# Shift+Tab Shift+Tab 두 번
```

세션 안에서 단발 사용.

```text
> /plan 이 보고서 12페이지를 8페이지로 줄여줘. 어디를 어떻게 줄일지 먼저 계획만 보여줘
```

승인 후 진행.

```text
> 진행해
```

## 강사 멘트

> 세 번째 기능 Plan Mode다. "AI가 멋대로 고쳐 버리면 어쩌지" 라는 가장 큰 우려에 직접 답하는 기능이다. Claude Code를 처음 쓰는 분에게는 "두려움 없이 시작할 수 있는 첫 모드"로 권한다. 처음 한 주는 전부 Plan Mode로 쓰고, 익숙해지면 default로 넘어간다. 진입 방법 세 가지 중 일상에서는 키보드 `Shift+Tab` 두 번이 제일 편하다. 프롬프트 핵심은 "먼저 계획만 보여 줘. 실행은 아직 하지 마." 이 한 줄이 들어가면 어떤 모드에서도 계획부터 받는다. 안전벨트 두 겹이다. 가장 흔한 오해는 "Plan 모드면 아무것도 안 도는 거 아닌가" — 아니다. 읽기는 된다. 폴더 구조 분석·파일 검색은 그대로 돌아간다.

## 실습

자기 폴더에서 `claude --permission-mode plan`으로 시작하거나 `Shift+Tab` 두 번으로 진입한 뒤, "이 폴더의 모든 활동지를 통합해 weekly-plan.md로 만들어줘"라고 요청한다. 화면에 변경 계획만 출력되고 실제 파일은 만들어지지 않는 것을 확인한 뒤 `진행해`로 승인한다.

확인 포인트는 두 가지. (1) Plan 모드 안에서 "진행할까요?" 물음만 나오는지 (2) 승인 전까지는 폴더에 새 파일이 생기지 않는지.

## 활용 시사점

교육 현장에서 Plan Mode는 다음 두 가지로 활용된다.

- **수업 자료 일괄 수정 전 검토**. 활동지 12개를 한 번에 새 양식으로 옮길 때, Plan 모드로 "무엇을 어떻게 바꿀지" 계획부터 받은 뒤 일부 샘플만 먼저 변환·확인 후 전체 적용한다. 실수로 30분 작업이 1초에 망가지는 사고를 막는다
- **첫 한 주 적응 기간 안전망**. Claude Code에 익숙하지 않은 교사가 첫 한 주 동안 Plan 모드만 쓰면 파일 손실 가능성이 0이다. "잘못 눌러도 되돌릴 게 없다"는 안도감이 학습 곡선을 단축한다

---

[← 이전 기능](/lectures/claude-code-edu/auto-memory/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/permission-modes/)
