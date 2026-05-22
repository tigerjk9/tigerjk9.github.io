---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-016
feature_name: "UX 보조 5종"
title: "UX 보조 5종"
track: advanced
order: 22
permalink: /lectures/claude-code-edu/ux-helpers/
---

## 정의

v2.1.90~121에 추가된 사용자 경험 보조 커맨드 묶음 5종이다. 진입 장벽을 낮춰 주는 도구 다섯 개 — `/powerup`·`/focus`·`/copy`·`/terminal-setup`·`/less-permission-prompts`. Claude Code를 처음 쓰는 동료에게 권하는 도구다.

## 핵심 동작

- `/powerup`(v2.1.90) — Claude Code 기능을 애니메이션 데모로 가르치는 인터랙티브 레슨
- `/focus`(v2.1.116) — Toggle. 프롬프트와 최종 답변만 보이는 집중 뷰
- `/copy`(v2.1.121) — 직전 응답 클립보드 복사. "Full response"는 정렬된 마크다운 표 그대로
- `/terminal-setup`(v2.1.121) — iTerm2 클립보드, 스크롤 감도 같은 터미널 종속 옵션을 자동 켜기
- `/less-permission-prompts`(v2.1.111) — 트랜스크립트를 스캔해 자주 거치는 read-only 명령들의 우선순위 allowlist를 제안

## 사용법

```text
/powerup
/focus
/copy
/terminal-setup
/less-permission-prompts
```

## 강사 멘트

> 마지막 Advanced 기능, UX 보조다. 진입 장벽을 낮춰 주는 도구 다섯 개를 한 화면에 모았다. Claude Code를 처음 쓰는 동료가 있다면 `/powerup` 한 마디 권한다. `/less-permission-prompts`가 행정 자리 분들에게 결정타다. 매번 묻는 게 답답한 read-only 명령을 한 번에 정리해 준다. 본인 일상에 맞는 한 개만 머리에 둔다. 다섯 개 다 외울 필요 없다. `/focus`로 강의·시연 화면 깔끔하게. `/terminal-setup`은 새 노트북 첫 세팅. 22개 기능 모두 봤다. 본인 일상에 한두 개라도 후보가 떠올랐으면 성공이다.

## 활용 시사점

교육 현장에서 UX 보조 5종은 다음 세 가지로 활용된다.

- **`/powerup` 동료 교사 진입 장벽 해소**. Claude Code 처음 쓰는 동료 교사에게 `/powerup` 한 마디 — 애니메이션 튜토리얼로 자기 페이스에 맞게 학습. "튜토리얼 보면서 따라하면 된다"는 안전감
- **`/less-permission-prompts` 권한 피로 해소**. 매주 누적되는 권한 prompt 피로를 한 번에 정리. 본인이 늘 yes 누른 read-only 명령들을 한 번에 영구 허용으로 정리
- **`/focus` 강의·시연 깔끔하게**. 다른 교사 앞에서 시연할 때 `/focus`로 프롬프트와 답변만 표시. 강의 화면 깔끔. `/copy`는 결과를 마크다운 표 그대로 메신저·이메일에 붙여 넣기

---

[← 이전 기능](/lectures/claude-code-edu/effort/) | [허브로 돌아가기](/lectures/claude-code-edu/)
