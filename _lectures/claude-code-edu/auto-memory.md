---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-036
feature_name: "Auto Memory"
title: "Auto Memory"
track: basic
order: 2
permalink: /lectures/claude-code-edu/auto-memory/
---

## 정의

Auto Memory는 사용자가 정정·선호를 자연어로 말하면 Claude가 자동으로 노트해 두는 머신 로컬 메모리 시스템이다. ChatGPT 메모리와 비슷하지만 클라우드가 아닌 본인 노트북의 마크다운 파일로 저장돼, 무엇이 기억됐는지 직접 보고 편집·삭제할 수 있다.

## 핵심 동작

- 저장 위치는 `~/.claude/projects/<project>/memory/`. project 경로는 git repo로부터 도출돼, 같은 repo의 모든 worktree·하위 디렉터리가 한 메모리 디렉터리를 공유한다
- 매 세션 시작 시 `MEMORY.md`의 첫 200행 또는 25KB가 자동 로드된다. 토픽 파일(`debugging.md`·`api-conventions.md`)은 필요할 때만 Claude가 read한다
- "다음부터 표 끝에는 출처를 붙여 줘" 같은 자연어 정정이 자동 저장된다
- `/memory` 슬래시 커맨드로 토글하거나 폴더를 직접 열 수 있다
- 끄려면 환경 변수 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` 또는 settings의 `autoMemoryEnabled: false`

## 사용법

```powershell
# 토글·폴더 열기
claude
> /memory

# 자연어 정정 (자동 저장됨)
> 그림 캡션 끝에는 마침표 빼는 게 우리 학교 표준이야. 다음부터 그렇게 해 줘

# 끄기
$env:CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
claude
```

settings.json 예시.

```json
{
  "autoMemoryEnabled": true,
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

## 강사 멘트

> Auto Memory는 "왜 자꾸 같은 정정을 해야 하지" 라는 좌절을 풀어 주는 기능이다. 매일 열두 번 정정하던 것이 자동으로 누적되면, 한 달 뒤에는 본인 톤이 거의 자동으로 잡힌다. 핵심 차별점은 — ChatGPT 메모리는 클라우드에서만 보이지만, Claude Code는 `~/.claude/projects/<project>/memory/` 아래 마크다운으로 쌓인다. 본인이 손으로 열어 보고 지울 수 있다. 민감한 정정(예. 미발표 자료의 약어)이 자동 저장되는 게 부담스러우면 환경 변수 한 줄로 끈다. 학생 개인정보·평가 자료를 다루는 교사는 이것을 꺼 두고 시작하는 것이 안전하다.

## 실습

세션 안에서 자연어로 "다음부터 평가 루브릭은 4단계 표로 만들어 줘"라고 말한 뒤, 다른 폴더에서 같은 프롬프트를 보내 규칙이 자동 적용되는지 확인한다. `/memory`로 폴더를 열어 저장된 마크다운을 직접 본다.

## 활용 시사점

교육 현장에서 Auto Memory는 다음 두 가지로 활용된다.

- **반복 정정 누적**. "활동지 시간 표기는 분 단위로", "학생 호칭은 학생 이름 대신 이니셜로" 같은 정정이 자동 누적돼, 한 학기 뒤에는 본인 톤이 거의 자동으로 잡힌다
- **민감 정보 환경에서는 OFF**. 학생 개인정보·미공개 평가 문항을 다루는 폴더는 `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`로 메모리 저장을 끄고 시작한다. 내부 작업과 외부 작업의 디렉터리·메모리 설정을 분리하는 것이 안전하다

---

[← 이전 기능](/lectures/claude-code-edu/claudemd/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/plan-mode/)
