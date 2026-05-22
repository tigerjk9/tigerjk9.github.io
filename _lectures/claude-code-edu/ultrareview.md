---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-013
feature_name: "/ultrareview 와 /ultraplan"
title: "/ultrareview 와 /ultraplan"
track: advanced
order: 18
permalink: /lectures/claude-code-edu/ultrareview/
---

## 정의

`/ultrareview`와 `/ultraplan`은 클라우드 세션에서 여러 병렬 서브에이전트가 코드 리뷰나 계획 수립을 수행하고 브라우저 기반 검토 화면을 제공하는 명령이다. Reviewer 2 시뮬레이션 — 의도적 다관점 검토로 빈 곳을 덜 남긴다.

## 핵심 동작

- `/ultrareview` 인자 없이 호출 시 현재 변경사항을, `<PR#>` 인자로 GitHub PR 검토 가능
- `/ultraplan`은 plan mode를 클라우드에서 다중 에이전트로 확장 — "이 큰 리팩토링을 어떻게 단계별로 쪼갤까"에 적합
- CLI에서 비대화형으로도 호출 가능 — `claude ultrareview 1234 --json --timeout 30`으로 stdout JSON. exit code 0/1
- 클라우드 의존. 망분리에서는 미작동

## 사용법

```text
/ultrareview
/ultrareview 1234
/ultraplan 인증 모듈을 OAuth2로 마이그레이션
```

CI 합성.

```powershell
# CI에서 비대화형
claude ultrareview 1234 --json --timeout 30 | ConvertFrom-Json
```

## 강사 멘트

> `/ultrareview`는 클라우드에서 자동으로 reviewer 에이전트 N명을 병렬로 돌리고 통합 결과를 준다. 본인이 에이전트를 직접 정의할 필요 없는 자동 모드다. `/ultraplan`은 큰 계획에 어울리고, `/ultrareview`는 코드·문서 변경 검토에 어울린다. `--json --timeout` 옵션을 쓰면 CI에 합성하기도 쉽다. 활동지·평가 자료를 자주 쓰는 사람의 본편 활용처다. `/ultrareview`를 매주 한 번 돌리면 리뷰 코멘트가 줄어든다. 망분리 폴백을 한 번 더 강조 — 본 강의실 환경에서는 시연만 보고 넘어가도 된다.

## 활용 시사점

교육 현장에서 `/ultrareview`·`/ultraplan`은 다음 두 가지로 활용된다.

- **수업 자료 다관점 검토**. 본인이 작성한 활동지 초고를 `/ultraplan 이 활동지의 학습목표·차시 분량·안전 요소를 비판적으로 검토`로 보내면 여러 에이전트가 다른 시각(학습목표·분량·안전)에서 동시 검토 후 통합 보고
- **GitHub PR 자동 리뷰**. 학생 코드 PR을 `/ultrareview <PR#>`로 보내면 다중 시각 리뷰가 자동 생성. 본인은 핵심만 확인. 망분리 환경에서는 시연만 보고 통과

---

[← 이전 기능](/lectures/claude-code-edu/routines/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/loop/)
