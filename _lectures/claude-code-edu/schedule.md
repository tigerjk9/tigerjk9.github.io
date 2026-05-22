---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-012
feature_name: "/schedule"
title: "/schedule"
track: advanced
order: 20
permalink: /lectures/claude-code-edu/schedule/
---

## 정의

`/schedule`은 Anthropic 클라우드 인프라에서 돌아가는 영구 스케줄 작업(Routines)을 자연어로 만들고 관리하는 슬래시 커맨드다. 노트북이 꺼져도 동작한다. 자연어로 cron을 등록하는 가장 편한 진입점이다.

## 핵심 동작

- `/schedule daily PR review at 9am` — 반복 작업 생성. 최소 1시간 간격
- `/schedule tomorrow at 9am, summarize yesterday's merged PRs` — 일회성 future-time 작업
- `/schedule list` — 모든 routines 나열
- `/schedule update` — 기존 작업 변경(cron 식 직접 입력도 가능)
- `/schedule run` — 즉시 실행
- 트리거는 schedule + API + GitHub event를 한 routine에 조합 가능(API/GitHub 트리거는 web UI에서 추가)
- 베타 헤더 `experimental-cc-routine-2026-04-01`

## 사용법

```text
/schedule weekdays at 8am, 어제 학교 공지 5개 요약하고 학년부 위키에 게시
/schedule in 2 weeks, 다음 평가 계획 초안 만들기
/schedule list
/schedule update
/schedule run
```

`/loop`와 분 단위는 `/loop`, 시간·일 단위는 `/schedule`로 구분.

API 트리거 (web에서 토큰 발급 후).

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_01...../fire \
  -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod."}'
```

## 강사 멘트

> Routines와 통합된 명령이다. 자연어로 cron을 등록하는 가장 편한 진입점이다. `/schedule list`로 본인 routine 목록을 한 화면에서 본다. update는 자연어를 다시 한 번 던지면 된다. `/loop`와 `/schedule` 구분 — 분 단위는 `/loop`, 시간·일 단위는 `/schedule`. "AI 비서 주니어"가 진짜 생긴다. `/schedule weekdays at 8am, 어제 부처 공문 5개 요약해 메일 초안 만들고 임시저장`으로 매일 아침 출근 전 보고 자료 초안이 메일함에 도착한다. ChatGPT는 같은 업무를 매일 사람이 직접 켜야 하지만 routines는 노트북이 꺼져도 클라우드에서 돈다 — 진정한 무인 실행.

## 활용 시사점

교육 현장에서 `/schedule`은 다음 두 가지로 활용된다.

- **매주 정기 보고서 자동 초안**. `/schedule 매주 금요일 오후 5시에 이번 주 학년부 활동 5개를 요약해서 README에 추가`로 매주 자동 초안. 본인은 검토·송부만
- **자연어 cron의 학습 부담 0**. cron 식(`0 8 * * 1-5`)을 외울 필요 없다. "매주 월요일 오전 8시" 한 마디면 끝. 학습 곡선 0으로 자동화 진입

---

[← 이전 기능](/lectures/claude-code-edu/loop/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/effort/)
