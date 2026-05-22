---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-040
feature_name: "Routines (클라우드 영구 스케줄)"
title: "Routines (클라우드 영구 스케줄)"
track: advanced
order: 17
permalink: /lectures/claude-code-edu/routines/
---

## 정의

Routines는 Anthropic 클라우드 인프라에서 노트북이 꺼져도 도는 영구 스케줄 작업이다. 한 routine에 (1) cron 스케줄, (2) 전용 HTTPS POST 엔드포인트, (3) GitHub event 세 트리거를 조합할 수 있다. 베타 헤더 `experimental-cc-routine-2026-04-01` 사용.

## 핵심 동작

- 생성. claude.ai/code/routines 웹, Desktop 앱 Routines 사이드바, CLI `/schedule`. 모두 같은 클라우드 계정에 기록
- 환경. 네트워크 액세스 레벨, 환경 변수, 셋업 스크립트(캐싱), 커넥터(MCP)를 작업별로 설정
- 저장소. 클론 후 `claude/`-prefix 브랜치로만 푸시(unrestricted 토글로 일반 브랜치도 허용)
- API 트리거. 토큰 발급 1회만 표시 — 한 routine당 전용 토큰. POST `/fire`에 `{"text": "..."}` 자유 텍스트
- GitHub 트리거. `pull_request.opened/closed/...`, `release.*` + author·title·body·branch·label·draft·merged 필터
- 일회성 cron은 daily cap에서 제외

## 사용법

```text
/schedule daily PR review at 9am
/schedule weekdays 8am, 어제 학교 공문 5개 요약하고 학년부 메신저에 게시
/schedule in 1 week, feature flag cleanup PR 만들기
/schedule list
/schedule update
/schedule run
```

외부 알림에서 호출.

```bash
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_xxx/fire \
  -H "Authorization: Bearer sk-ant-oat01-yyy" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod."}'
```

## 강사 멘트

> Routines는 v2의 가장 큰 신기능 중 하나다. 본인 노트북이 꺼져 있어도 클라우드에서 도는 진짜 무인 작업이다. AI 비서 주니어가 출근 전에 보고서 초안을 만들어 두는 시나리오. 행정 업무가 많은 사람에게 결정타가 된다. 모범 프롬프트 #5 — 자연어로 cron을 등록한다는 게 묘한 감각이다. AI가 그 말을 받아 클라우드에 영구 작업으로 등록한다. 주의 — Routines는 베타다. 베타 헤더 `experimental-cc-routine-2026-04-01` 사용. 베타에서 빠질 때 인터페이스가 바뀔 수 있다. 트리거 세 종류 — 시간(cron)·이벤트(API)·GitHub. 셋을 엮으면 꽤 복잡한 자동화도 된다. 본인 일상에서 "출근 전에 누가 해 두면 좋겠다" 싶은 작업 한 개 잡아서 routine으로 만들어 본다. 망분리 환경이면 routine 등록은 건너뛰고 시연만 보고 통과한다. `/loop`로 폴백할 수 있다.

## 실습

작은 routine 한 개를 등록한다 (망분리 환경이면 시연만 보고 통과).

```text
/schedule weekdays 8am, 어제 학교 공지 5개 요약하고 학년부 위키 '주간동향'에 추가
```

`/schedule list`로 등록 확인.

## 활용 시사점

교육 현장에서 Routines는 다음 세 가지로 활용된다.

- **AI 비서 주니어 실현**. 매일 아침 8시에 어제 학교 공지 5개를 자동 요약해 학년부 위키에 게시. 출근하면 결과가 도착해 있다. ChatGPT는 매번 사람이 켜야 하지만 routines는 노트북이 꺼져도 클라우드에서 돈다 — 진정한 무인 실행
- **GitHub PR 자동 검토**. 학생이 PR 올리면 자동으로 routine이 1차 검토 → 본인은 2차 검토만. 매주 5명 학생 코드 검토 시간 4시간 → 1시간
- **베타 헤더·망분리 폴백**. 베타라 인터페이스 변경 가능성. 망분리 환경에선 `/loop`로 노트북 폴링 대체

---

[← 이전 기능](/lectures/claude-code-edu/plugins/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/ultrareview/)
