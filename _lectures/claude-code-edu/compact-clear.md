---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-038
feature_name: "/compact 와 /clear"
title: "/compact 와 /clear"
track: basic
order: 8
permalink: /lectures/claude-code-edu/compact-clear/
---

## 정의

`/compact`는 대화 요약본과 도구 호출 결과 일부를 보존하면서 컨텍스트를 압축한다. `/clear`는 컨텍스트를 처음부터 비운다. 긴 분석 세션의 필수기. 자동(컨텍스트 임계 초과 시) + 수동 두 가지로 동작한다.

## 핵심 동작

- `/compact` 후에도 프로젝트 루트 `CLAUDE.md`는 디스크에서 다시 읽혀 재주입된다. 중첩 `CLAUDE.md`는 다음 파일 read 때 lazy reload
- 스킬은 가장 최근 호출만 첫 5,000 토큰 보존(공유 25,000 토큰 예산)
- `PreCompact`/`PostCompact` 훅으로 압축 전후에 백업·로깅·차단 가능. exit 2 또는 `{decision:"block"}`로 압축 자체 차단 가능
- 자동 압축 무한 루프(autocompact thrash)는 자동 감지·중단돼 API 호출 낭비를 막는다

## 사용법

```text
# 수동 요약·압축
/compact

# 완전 초기화
/clear
```

압축 직전 트랜스크립트 백업 훅.

```json
{
  "hooks": {
    "PreCompact": [{
      "matcher": "auto",
      "hooks": [{
        "type": "command",
        "command": "powershell -File .claude/hooks/backup-transcript.ps1"
      }]
    }]
  }
}
```

## 강사 멘트

> 차이를 한 줄로 정리한다. `/clear`는 "다른 일 시작", `/compact`는 "같은 일 이어가기". 임계점을 넘으면 자동으로 compact가 돌기도 한다. 그래서 그 직전에 핵심을 메모로 남겨 두는 것이 안전하다. 압축 직전에 "5문장 요약하고 압축" 한 마디 보내는 게 안전벨트다. 자동 compact는 가끔 핵심을 흐릴 수도 있다. `PreCompact`·`PostCompact` 훅으로 자동 보존을 걸 수도 있지만 Advanced에서 본다. `/compact`는 강력하지만 무손실은 아니다. 핵심 산출물은 직전에 명시적으로 보존 요청을 거는 것이 안전하다.

## 실습

긴 분석 세션 중간에 "지금까지의 분석 흐름을 5문장으로 요약하고 컨텍스트를 압축해 줘"라고 요청한 뒤 `/compact`를 실행한다. 압축 후에도 CLAUDE.md 규칙이 그대로 살아 있는지 확인한다.

## 활용 시사점

교육 현장에서 `/compact`·`/clear`는 다음 두 가지로 활용된다.

- **하루 작업 한 세션 유지**. 오전 활동지 검토 → 오후 평가 루브릭 작성을 한 세션에서 진행할 때, 중간에 `/compact`로 압축하면 핵심만 남기고 토큰을 회수한다. `--continue`로 다음 날 이어 가도 부담이 적다
- **새 작업 진입 시 /clear**. 활동지 작업이 끝난 뒤 학생 평가 자료 작업으로 넘어가면 `/clear`로 한 번 비운다. 이전 맥락이 새 작업에 섞이는 것을 막는다

---

[← 이전 기능](/lectures/claude-code-edu/agents-panel/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/usage/)
