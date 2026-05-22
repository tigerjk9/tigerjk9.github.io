---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-035
feature_name: "CLAUDE.md + @import"
title: "CLAUDE.md + @import"
track: basic
order: 1
permalink: /lectures/claude-code-edu/claudemd/
---

## 정의

`CLAUDE.md`는 Claude Code가 매 세션 시작 시 자동으로 읽어 들이는 영구 컨텍스트 파일이다. 매번 같은 시스템 프롬프트를 복붙하는 대신, 프로젝트 루트의 마크다운 파일 한 개로 톤·언어·작업 규칙을 영구 고정한다. 4계층(managed → user → project → local)으로 cascade되며, `@path/to/file` 문법으로 다른 마크다운을 import해 공용 규칙을 한 곳에서 관리한다.

## 핵심 동작

- 프로젝트 루트의 `./CLAUDE.md` 또는 `./.claude/CLAUDE.md`가 매 세션 자동 로드된다
- 사용자 전역은 `~/.claude/CLAUDE.md`, 머신 정책은 `/etc/claude-code/CLAUDE.md`(Linux/WSL) 또는 `C:\Program Files\ClaudeCode\CLAUDE.md`(Windows)에 둔다
- `@../공용규칙/표준.md` 형식으로 외부 파일 import 가능, 최대 5단계 재귀
- 디렉터리 트리를 위로 걸어 올라가며 모든 `CLAUDE.md`를 자동 발견·연결한다
- 200행 이내 권장. 길어지면 `.claude/rules/<topic>.md`로 분리한다

## 사용법

```powershell
# 1. /init으로 초안 자동 생성
claude
> /init

# 2. 직접 작성
notepad CLAUDE.md

# 3. 로드된 파일 목록 확인 및 편집
> /memory
```

CLAUDE.md 예시.

```markdown
# 우리 학교 AI 수업 자료 — Claude 가이드

## 프로젝트 개요
- 목적. 학생 활동지·평가 루브릭 자동 생성
- 데이터. ./data/ (학생 개인정보 포함 파일은 절대 수정 금지)

## 답변 규칙
- 모든 답변은 한국어로 한다
- 학습목표는 Bloom 분류 동사로 시작한다
- 평가 루브릭은 4단계 표로 정리한다

## 외부 규칙 import
@~/.claude/my-personal-style.md
@./docs/lesson-template.md
```

## 강사 멘트

> 첫 기능 CLAUDE.md다. 어떤 기능보다 먼저 손에 익혀야 하는 1순위. 매 세션마다 시스템 프롬프트 복붙하는 일을 0으로 만드는 도구다. 4계층은 외울 필요 없다. 일상은 project 계층 — 폴더 루트의 CLAUDE.md 한 개로 시작한다. 익숙해지면 `~/.claude/CLAUDE.md`(user)에 본인 톤·언어를 적어 둔다. `@import` 한 줄이 핵심이다. 본인이 만든 공용 규칙 마크다운 한 개를 만들어 두면 모든 프로젝트 CLAUDE.md가 그것을 끌어 쓴다. 학교·학년 표준을 한곳에서 관리하는 핵심 트릭이다.

## 실습

`C:\work\edu-lab\demo01` 아래에 CLAUDE.md 5~10줄을 작성하고, 작성 전후 동일 프롬프트를 두 번 보내 답변 차이를 비교한다. 비교 대상은 답변 언어·표 형식·출처 표기 세 가지.

```powershell
PS C:\work\edu-lab\demo01> @"
# 프로젝트 규칙

- 모든 답변은 한국어로 한다
- 실험 결과는 항상 마크다운 표 형식으로 정리한다
- 단위는 SI 단위로 통일한다
- 인용·수치는 출처(파일명)를 함께 표기한다
- 콜론 대신 마침표를 쓴다
"@ | Out-File -Encoding UTF8 CLAUDE.md
```

핵심 검증 포인트는 답변이 표 형식·한국어·출처 표기로 바뀌는지 두 눈으로 확인하는 것이다.

## 활용 시사점

교육 현장에서 CLAUDE.md는 다음 세 가지로 활용된다.

- **학년·교과별 톤 통일**. 1학년용 활동지와 6학년용 활동지의 어휘 수준이 다르다. 학년별 폴더에 CLAUDE.md 한 개씩 두면 매 세션 톤이 자동 통일된다
- **학교 공용 규칙 import**. `@~/공용규칙/학교양식.md`로 학교 표준 양식 파일 한 개를 모든 프로젝트가 끌어 쓰면 교사 5명이 같은 표준으로 작업할 수 있다
- **개인정보 보호 룰 박기**. `./data/` 폴더의 학생 개인정보 파일은 절대 수정·외부 송신 금지 규칙을 CLAUDE.md에 박아 두면 실수로 외부에 노출될 위험이 줄어든다

---

[허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/auto-memory/)
