---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-009
feature_name: "/usage"
title: "/usage"
track: basic
order: 9
permalink: /lectures/claude-code-edu/usage/
---

## 정의

`/usage`는 일·주·달 토큰 사용량, 세션 수, 연속 사용일을 보여 주는 통계 탭이다. v2.1.118에서 기존 `/cost`·`/stats`가 통합되어 기본 단축 별칭이 됐다. AI 비용이 두려운 사용자에게 매주 본인 사용량을 그래프로 보여 주는 영수증 역할을 한다.

## 핵심 동작

- "stats" 탭. 일별 사용량, 누적 세션, streak
- "extra usage" 탭. Team·Enterprise·API 사용자가 한도 초과 후 메터드 오버에이지 사용 여부
- Remote Control 클라이언트에서도 호출 가능

## 사용법

```text
/usage
/extra-usage
```

## 강사 멘트

> `/usage`는 영수증이다. 회사 단체 라이선스 환경이면 매주 한 번씩 보고 본인 페이스를 잡는 용도다. `/usage` 한 번 띄우고 AI한테 분석시키기. 본인 비용 패턴을 한 주에 한 번씩만 보면 다음 주가 반으로 줄어든다. "AI가 비싸면 어쩌지" 우려가 큰 사람에게 매주 본인 토큰 사용량을 그래프로 보여 주면 "회의록 8개 합치고 4달러"라는 구체 감각이 생긴다. 부서 단위로 청구되는 단체 라이선스 환경에서는 `/usage`가 곧 "내가 얼마나 썼나" 영수증이다.

## 활용 시사점

교육 현장에서 `/usage`는 다음 두 가지로 활용된다.

- **본인 사용 패턴 파악**. 매주 한 번 `/usage`를 띄워 어떤 작업이 토큰을 많이 쓰는지 확인한다. 활동지 일괄 변환 vs 학생 글쓰기 평가 vs 회의록 요약을 비교하면 다음 주 전략이 달라진다
- **학교·학년 단위 라이선스 가시화**. 학년부·학교 단위 단체 라이선스 환경에서는 본인 세션 단위 통계가 공동 비용 책임감을 만든다. "내가 쓰면 누가 부담하는지" 가시화

---

[← 이전 기능](/lectures/claude-code-edu/compact-clear/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/continue-resume/)
