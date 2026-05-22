---
layout: lecture
lecture_slug: claude-code-edu
feature_id: F-010
feature_name: "/effort"
title: "/effort"
track: advanced
order: 21
permalink: /lectures/claude-code-edu/effort/
---

## 정의

`/effort`는 모델의 추론 깊이를 5단계(`low`/`medium`/`high`/`xhigh`/`max`)로 조절하는 명령이다. v2.1.111에서 `xhigh`(Opus 4.7 전용)와 인터랙티브 화살표 슬라이더가 추가됐고, `auto`도 도입됐다. 단순 작업은 빠르게, 복잡 추론은 깊게 — 비용 대비 깊이를 투명하게 조절한다.

## 핵심 동작

- 인자 없이 호출하면 화살표·Enter로 슬라이더 조작
- 단계 순서. `low → medium → high → xhigh → max`. 사용 가능 단계는 모델별로 다르다(Opus 4.7만 `xhigh` 가능)
- 스킬 프론트매터 `effort: high`로 스킬별 오버라이드 가능 — 그 스킬 활성 동안만 적용 후 원복
- Pro/Max 구독자가 Opus 4.6/Sonnet 4.6 쓸 때 기본값이 v2.1.111부터 `medium → high`로 상향됐다

## 사용법

```text
/effort                    # 슬라이더
/effort xhigh              # 직접 지정
/effort auto               # 자동 조절
```

```powershell
# 시작 시 강제
claude --effort high
```

스킬 오버라이드.

```yaml
---
name: 깊은검토
description: 활동지 깊은 검토
effort: high
---
```

## 강사 멘트

> `/effort`는 추론 강도 다이얼이다. 단순 작업에 max를 쓰면 비용·시간 낭비, 복잡 추론에 low를 쓰면 답이 얕다. xhigh는 Opus 4.7에서만 가능, max는 그보다 더 깊은 추론. 같은 질문이라도 effort에 따라 답의 깊이가 달라진다. xhigh는 시간 1.5~2배·비용 1.5~3배지만, 깊은 검토에는 결정적인 차이가 난다. 본인 작업을 한 번 분류해 본다. 보통 low가 50%, medium 35%, high 이상이 15% 정도다. Auto가 무난하다. 본인이 일일이 다이얼 돌릴 필요 없고, 정말 깊은 작업에서만 xhigh로 올린다. ChatGPT의 "GPT-4 vs GPT-4o" 같은 모델 스위치는 정확도-속도 거래만 표면화하지만 `/effort`는 같은 모델 안에서 추론 시간을 명시적으로 조절 — 비용 대비 깊이가 투명하다.

## 활용 시사점

교육 현장에서 `/effort`는 다음 두 가지로 활용된다.

- **작업 성격별 깊이 조절**. 활동지 캡션 정리는 `low`로 빠르게, 학생 글쓰기 평가 루브릭 작성은 `xhigh`로 깊게. 같은 도구가 작업 성격에 맞게 변속
- **`auto` 기본 권장**. 본인이 일일이 다이얼 돌릴 필요 없다. Auto가 분류기로 자동 결정. 정말 깊은 작업(예. 평가 신뢰도 비판 반박)에서만 명시적으로 `xhigh`로 올린다

---

[← 이전 기능](/lectures/claude-code-edu/schedule/) | [허브로 돌아가기](/lectures/claude-code-edu/) | [다음 기능 →](/lectures/claude-code-edu/ux-helpers/)
