---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-011
feature_name: "/loop"
title: "/loop"
track: advanced
order: 19
permalink: /lectures/claude-code-edu/loop/
---

## 정의

`/loop`는 한 프롬프트(또는 다른 슬래시 커맨드)를 인터벌마다 반복 실행하는 번들 스킬이다. Routines가 클라우드 영구라면, `/loop`는 본인 노트북에서 도는 짧은 반복이다. 인터벌 단위는 `s/m/h/d`, 최소 1분, 7일 후 자동 만료.

## 핵심 동작

- **Fixed mode**. `/loop 5m <prompt>`처럼 인터벌 명시
- **Dynamic mode**. `/loop <prompt>` 인터벌 생략 시 Claude가 매 반복마다 1분~1시간 사이 다음 대기를 직접 정하고 그 이유를 출력. Monitor 도구로 백그라운드 스트리밍 폴링이 더 효율적이면 자동 전환
- **Maintenance mode**. `/loop` (둘 다 생략)은 기본 메인테넌스 프롬프트(미완료 작업 마무리·PR 코멘트 응답·CI 실패 처리·간단한 클린업)를 반복
- `loop.md`(`.claude/loop.md` 또는 `~/.claude/loop.md`)로 메인테넌스 프롬프트를 본인 것으로 교체 가능
- `Esc`로 다음 발화 전에 중단. 한 세션 최대 50개 스케줄

## 사용법

```text
/loop 5m check if the deployment finished and tell me what happened
/loop check whether CI passed and address any review comments
/loop 20m /review-pr 1234
/loop                       # loop.md 또는 내장 메인테넌스
```

학교 일상 예시.

```text
/loop 30m 새 학교 공지 메일이 도착했는지 확인하고 도착했으면 한 줄 요약
/loop 10m 학생 제출 폴더에 새 과제가 들어왔는지 확인
```

## 강사 멘트

> `/loop`는 한 프롬프트를 일정 간격으로 반복한다. Routines가 클라우드 영구라면, `/loop`는 본인 노트북에서 도는 짧은 반복이다. 3모드 — fixed는 정해진 인터벌, dynamic은 Claude가 적절한 인터벌을 스스로 정하고, maintenance는 주기 유지 점검. 한 세션에 50개 한도. 7일 뒤 자동 만료. 무한 루프 방지장치다. 본인 노트북이 켜져 있을 때 돌리는 짧은 반복에 잘 맞는다. `/loop`와 Routines 차이 — `/loop`는 본인 노트북, Routines는 클라우드 영구. 둘 다 알아 두면 자리에 맞게 쓸 수 있다.

## 활용 시사점

교육 현장에서 `/loop`는 다음 두 가지로 활용된다.

- **본인 노트북 켜진 동안 폴링**. 학생 제출 폴더·새 공지 메일·자동화 잡 결과를 30분마다 자연어로 확인. 회의 들어가도 결과가 도착한 순간 후처리 시작
- **Routines 망분리 폴백**. Routines가 막힌 환경에서는 `/loop`가 같은 역할. 본인 노트북이 켜진 시간 동안만 도는 짧은 반복으로 대체

---

[← 이전 기능](/lectures/claude-code-edu/ultrareview/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/schedule/)
