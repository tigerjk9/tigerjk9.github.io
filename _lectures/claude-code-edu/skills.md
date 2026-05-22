---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-007
feature_name: "Skills"
title: "Skills"
track: basic
order: 5
permalink: /lectures/claude-code-edu/skills/
---

## 정의

Skills는 재사용 가능한 절차·체크리스트·플레이북을 `SKILL.md`(YAML 프론트매터 + 마크다운 본문) 한 파일로 정의하고, `/<skill-name>` 한 줄 호출로 실행하는 확장이다. 매 세션 시스템 프롬프트를 복붙하는 대신 한 번 정의 후 영구 재사용한다. 본문은 호출될 때만 컨텍스트에 들어가 평상시 토큰 부담이 거의 없다.

## 핵심 동작

- 위치는 사용자 전역 `~/.claude/skills/<name>/SKILL.md`, 프로젝트 `.claude/skills/<name>/SKILL.md`, 또는 플러그인
- 본문은 호출 시에만 로드. `description`만 평상시 색인에 머문다 — 스킬 100개를 만들어도 평상시 토큰 부담은 거의 없다
- 프론트매터 필드로 호출 통제. `disable-model-invocation`·`user-invocable`·`paths`(특정 파일에서만 자동 활성)·`shell: powershell`·`allowed-tools`
- 인자 치환. `$ARGUMENTS`·`$0`·`$N`·`$name`(named args)
- `` !`<command>` `` 인라인 또는 ` ```! ` 블록으로 셸을 미리 실행해 결과를 본문에 박을 수 있다

## 사용법

```powershell
# 사용자 스킬 디렉터리 생성
mkdir ~/.claude/skills/활동지요약

# SKILL.md 작성
notepad ~/.claude/skills/활동지요약/SKILL.md
```

SKILL.md 예시.

```yaml
---
name: 활동지요약
description: 활동지 마크다운 한 편을 받아 학습목표·활동 단계·평가 기준 3섹션 요약 출력. 사용 시점 — 수업 자료 검토, 학년 공유 회의 준비
argument-hint: "[md-path]"
allowed-tools: Read Grep
paths:
  - "**/*.md"
  - "activities/**/*.md"
shell: powershell
---

$0 활동지를 읽고 다음 형식으로 답변하라.

## 학습목표 (Bloom 동사 기반)
## 활동 단계 5줄 요약
## 평가 기준 4단계 표
## 우리 학년에 줄 시사점 2개

현재 디렉터리. !`Get-Location | Select-Object -ExpandProperty Path`
```

호출.

```text
/활동지요약 activities/2026-Q2/물의여행.md
```

## 강사 멘트

> Skills의 가치는 두 가지다. 재사용과 토큰 효율. 평상시에는 description만 색인되고 본문은 호출 시에만 로드돼서, 스킬 100개를 만들어도 평상시 토큰 부담이 거의 없다. 활용 패턴은 자주 하는 작업을 스킬 몇 개로 만들어 두면, 한 줄 호출만으로 끝나 작업 흐름이 짧아진다. 모범 프롬프트 #1을 그대로 쓴다. Claude가 자기 자신을 정의하는 묘한 메타 작업이다. SKILL.md를 손으로 짜지 말고, AI에게 시켜서 만든 다음 본인이 검토한다. 프론트매터의 핵심은 `name`(호출 이름), `description`(평상시 색인), `allowed-tools`(권한), `paths`(자동 매칭).

## 실습

`~/.claude/skills/요약/SKILL.md` 5줄짜리 단순 스킬을 만들어 `/요약` 한 줄 호출이 동작하는지 확인한다. 한국어 스킬 이름도 그대로 작동한다.

```powershell
mkdir ~/.claude/skills/요약
@"
---
name: 요약
description: 입력 텍스트를 3문장 한국어 요약
---

다음 내용을 3문장으로 요약하라.
"@ | Out-File -Encoding UTF8 ~/.claude/skills/요약/SKILL.md
```

세션에서 `/요약` 호출 시 한 줄이 진짜 도는 감각을 손에 익히는 것이 핵심이다.

## 활용 시사점

교육 현장에서 Skills는 다음 세 가지로 활용된다.

- **반복 작업 한 줄 호출화**. 활동지 요약·평가 루브릭 생성·학습목표 추출 같은 매주 반복하는 작업을 각각 스킬로 만들면, 한 줄 명령으로 끝난다. 매주 1시간 절약
- **학년·교과 공유 자산**. 학년부 공용 폴더에 SKILL.md를 두면 학년 교사 5명이 동일한 양식·톤으로 자료를 만들 수 있다
- **`paths` 자동 매칭**. `paths: ["**/*.pdf"]` 한 줄을 박아 두면 Claude가 PDF를 보는 순간 자동으로 그 스킬을 활성화한다. 사용자가 호출을 잊어도 동작

---

[← 이전 기능](/lectures/claude-code-edu/permission-modes/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/subagents/)
