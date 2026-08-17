---
title: "AI 디자인 슬롭 방지 기술 Hallmark"
date: 2026-08-18 01:29:29 +0900
categories: [AI, 기술]
tags: [AI, 디자인, 생성형AI, 프롬프트엔지니어링, 웹앱, 자동화, UX, LLM]
header:
  teaser: /assets/hallmark-anti-ai-slop-design-thumb.jpg
permalink: /post/hallmark-anti-ai-slop-design/
---
인공지능(AI)이 만들어내는 디자인은 편리하지만, 때로는 획일적인 'AI 슬롭(slop)'이라는 비판을 받는다. **Hallmark**는 이러한 문제를 해결하고자 탄생한 AI 디자인 기술이다. 이 기술은 AI가 생성한 흔적을 지우고, 독창적이며 인간적인 감각을 지닌 디자인 결과물을 만든다.

<figure>
<img src="/assets/hallmark-anti-ai-slop-design-thumb.jpg" alt="AI 디자인 슬롭 방지 기술 Hallmark">
</figure>

## AI 슬롭을 거부하는 디자인 접근법

**Hallmark**는 **Claude Code**, **Cursor**, **Codex** 등 코드 생성 AI를 위한 디자인 기술이다. 이 기술의 핵심 목표는 AI가 흔히 만들어내는 틀에 박힌 디자인을 피하고, 마치 인간 디자이너가 직접 작업한 듯한 고유한 결과물을 제공하는 데 있다. **Together AI**가 개발한 Hallmark는 디자인 요청(brief)마다 새로운 접근 방식을 취한다.

Hallmark는 다음 과정을 거쳐 AI 슬롭을 방지한다.

*   요청 내용에 맞는 **매크로 구조**를 선택한다.
*   **21가지 테마** 중 하나를 적용한다.
*   **57가지 슬롭 테스트 게이트**를 거치며, 최종 결과물 도출 전 자체 검토 과정을 진행한다.
*   모든 대규모 언어 모델(LLM)이 훈련된 기본 분포를 의도적으로 거부한다.

이러한 과정을 통해 Hallmark로 생성된 두 개의 페이지는 서로 다른 웹사이트처럼 느껴진다. 단순히 색상만 바꾼 템플릿 복사본과는 확연히 다르다.

## 네 가지 핵심 기능: 디자인 작업의 새로운 지평

Hallmark는 네 가지 핵심 기능(Verb)을 제공하며, 각 기능은 디자인 과정의 특정 요구를 충족시킨다.

다음 표는 Hallmark의 네 가지 핵심 기능과 그 역할을 설명한다.

| 기능명            | 역할                                                                                              |
| :---------------- | :------------------------------------------------------------------------------------------------ |
| **(기본)**        | 새로운 UI를 구축한다. 매크로 구조를 선택하고 규칙 세트를 적용하며, 결과물을 반환하기 전에 슬롭 테스트를 실행한다. |
| `hallmark audit <target>`   | 기존 코드를 **안티-패턴**에 따라 평가한다. 수정 없이 문제 목록(punch list)만 제공한다.               |
| `hallmark redesign <target>` | 기존 구조를 버리고, 내용(copy), 정보 아키텍처(IA), 브랜드를 유지한 채 다른 **지문(fingerprint)**으로 다시 구축한다. |
| `hallmark study <screenshot 또는 URL>` | 사용자가 선호하는 디자인에서 **핵심 DNA**를 추출한다. 매크로 구조, 타이포그래피 조합, 색상 기준점을 파악한다. 픽셀 복제나 유료 템플릿 사용은 거부한다. 선택적으로 다른 AI 도구에 전달할 수 있는 휴대 가능한 `design.md` 파일을 생성한다. |

이러한 기능들은 사용자가 AI를 활용해 디자인을 시작하거나, 기존 디자인을 개선하거나, 특정 디자인 미학을 분석하여 새로운 영감을 얻을 수 있도록 돕는다.

## 맞춤형 디자인과 유연한 구조

Hallmark는 다양한 디자인 요청에 맞춰 매번 독특한 형태를 만들어낸다. 예를 들어, 빵 앱, 콘텐츠 추출 API, 레코드 레이블, AI 도구, 차 메뉴, 양봉장, 인쇄 박람회, 타이포그래피 스튜디오 등 각기 다른 목적의 페이지들이 서로 다른 테마와 구조, 제작 방식을 적용받아 완성된다. 모든 페이지는 자체 포함된 HTML + CSS로 구성되며, CSS 주석에 매크로 구조가 명시된다.

특히, 일반적인 테마로는 표현하기 어려운 독창적인 의도를 담은 요청에는 **'Custom(커스텀)' 모드**가 적용된다. 이 모드는 정해진 카탈로그 테마를 사용하지 않고, 맞춤형 색상 팔레트, 글꼴, 레이아웃을 완전히 처음부터 디자인한다. 역시 동일한 57가지 슬롭 테스트 게이트를 거치지만, 아래에 깔린 템플릿은 없다. **Cascadia Nightjar** 열차 티켓 페이지나 **Mend Assembly** 수리 카페 브로드시트 페이지처럼 맞춤형으로 제작된 디자인 사례들은 Hallmark가 단순한 템플릿 엔진이 아님을 보여준다.

## 설치

Hallmark는 다음과 같이 설치한다.

```
npx skills add nutlope/hallmark
```

이 명령어를 다시 실행하면 언제든지 최신 버전으로 업데이트된다. 또는 `SKILL.md` 파일과 `references/` 디렉터리를 각 AI 도구의 지정된 경로에 직접 복사하여 설치할 수 있다.

*   **Claude Code**: `~/.claude/skills/hallmark/`
*   **Cursor**: `.cursor/rules/hallmark.mdc` (SKILL.md 본문, frontmatter 제외)
*   **Codex**: `~/.codex/skills/hallmark/` (개인용) 또는 `.codex/skills/hallmark/` (프로젝트 범위)

Hallmark의 규칙 세트는 `SKILL.md`와 `references/`에 저장되어 있다. 자세한 사용 예시는 `docs/recipes.md`와 `docs/study-examples.md`에서 확인한다.

## 출처
- Nutlope(Together AI), hallmark (GitHub). https://github.com/Nutlope/hallmark
