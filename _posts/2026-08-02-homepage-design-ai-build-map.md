---
title: "홈페이지를 짓고 검증하는 오픈소스 GitHub 지도"
date: 2026-08-02 14:53:00 +0900
categories: [바이브코딩, AI]
tags: [바이브코딩, 오픈소스, 디자인시스템, 웹개발, AI]
permalink: /post/homepage-design-ai-build-map/
header:
  teaser: /assets/homepage-design-ai-build-map-thumb.png
---

홈페이지 하나를 만드는 일은 예쁜 화면을 그리는 것으로 끝나지 않는다. 레퍼런스를 참고하고, 색과 글꼴을 설계하고, 코드로 구현하고, 성능과 접근성을 검증하는 네 단계가 한 흐름으로 이어져야 한다. 문제는 각 단계에 쓸 오픈소스가 흩어져 있고, AI 웹 빌더까지 쏟아지면서 무엇을 어디에 끼울지 판단하기 어렵다는 점이다.

닷커넥터가 2026년 7월 말 GitHub 공개 정보를 스냅샷으로 정리한 지도는 이 도구들을 참고, 설계, 구현, 검증이라는 한 축에 배치한 큐레이션이다. 40여 개 레포를 나열하는 대신 필요한 레이어만 골라 조합하도록 짜여 있다. 이 글은 그 지도를 읽고 쓰는 법을 정리한다.

<figure>
<img src="/assets/homepage-design-ai-build-map-thumb.png" alt="홈페이지를 짓고 검증하는 오픈소스 GitHub 지도">
</figure>

## 어디서 시작할까

모든 도구를 한 번에 도입할 필요는 없다. 지금 풀어야 할 문제가 무엇인지부터 정하고 거기에 맞는 레이어만 붙이면 된다. 지도는 네 가지 필요를 진입점으로 제시한다.

- AI에게 디자인 언어를 전달하고 싶다. DESIGN.md 포맷과 레퍼런스 컬렉션부터 본다. 디자인 결정을 텍스트로 버전 관리한다.
- 스크린샷이나 기존 화면을 출발점으로 삼고 싶다. AI 웹 빌드와 시각 편집 도구를 쓰되 허가된 화면과 오리지널 자산만 넣는다.
- 색·글꼴·간격을 토큰으로 운영하고 싶다. DTCG, Style Dictionary, Tokens Studio로 디자인과 코드의 값 체계를 잇는다.
- 홈페이지 품질을 반복 검증하고 싶다. 컴포넌트 문서화, 시각 회귀, 접근성, 성능 검사를 릴리스 체인에 붙인다.

여기서 clone 계열 도구는 전제 하나를 반드시 깔고 봐야 한다. 소유했거나 명시적으로 허가받은 사이트의 마이그레이션·학습·내부 프로토타이핑에만 쓴다는 것이다. 공개 CSS를 볼 수 있다는 사실이 남의 로고·카피·상표·로그인 흐름을 재현할 권리를 주지는 않는다.

## 목적별 네 가지 스택

한 레포가 모든 문제를 풀지는 않는다. 지도는 도구를 하나의 흐름으로 엮은 네 가지 출발 조합을 제안한다.

| 스택 | 언제 쓰나 | 도구 체인 |
|------|-----------|-----------|
| 새 브랜드 홈페이지 | 카피·자산·토큰을 처음부터 소유하고 빠른 구현과 장기 유지보수를 모두 원할 때 | design.md → Tailwind → shadcn/ui → Motion → Playwright + axe |
| 토큰 우선 디자인 시스템 | 여러 페이지를 운영하고 디자이너·개발자가 같은 토큰 계약을 공유해야 할 때 | DTCG → Tokens Studio → Style Dictionary → Storybook |
| 소유·허가된 기존 사이트 현대화 | 소스가 오래됐거나 CMS를 이전하며 구조 관찰과 컴포넌트 스펙을 분리할 때 | Firecrawl → open-lovable 또는 JCodesMore → Design spec → Visual QA |
| 시각 반복 편집 | 화면에서 조정해 코드로 잇거나 마케팅 팀이 페이지를 독립 운영할 때 | Onlook / Webstudio / Instatic → Radix → Lighthouse |

## 카테고리별로 골라 본 핵심 레포

40여 개 레포 중 홈페이지 작업에 바로 닿는 것들만 카테고리별로 추렸다. 각 레포에 붙은 별 수는 관찰 시점의 약값이므로 그대로 못박지 않는다.

### 디자인 언어와 레퍼런스

- google-labs-code/design.md — 색·타이포그래피·컴포넌트·레이아웃 규칙을 사람과 AI가 함께 읽는 계약으로 적는 포맷 명세. 흩어진 규칙을 하나의 실행 가능한 디자인 계약으로 통합할 때.
- VoltAgent/awesome-design-md — 유명 디자인 시스템을 DESIGN.md 형태로 모은 대형 레퍼런스. 내 브랜드용 문서를 짜기 전 목차와 표현 방식을 연구할 때.

### AI 웹 빌드

- abi/screenshot-to-code (MIT) — 스크린샷·목업·Figma를 HTML/Tailwind/React/Vue 초안으로 바꾸는 이 분야 대표 프로젝트. 내 오리지널 목업을 작동하는 프런트엔드 초안으로 옮길 때. 픽셀 퍼펙트는 보장하지 않는다.
- firecrawl/open-lovable (MIT) — 웹 컨텍스트와 대화형 AI로 React 앱을 만들어 샌드박스에서 미리 보는 예시 앱. API 키와 샌드박스 비용이 들 수 있다.
- JCodesMore/ai-website-cloner-template (MIT) — 허가된 사이트를 분석해 토큰·스펙·섹션 구현·visual QA로 잇는 Next.js 템플릿. README가 피싱·사칭을 명시적으로 금지한다. 로그인·OTP·결제·상표 자산은 제외한다.

### 시각 편집과 빌더

- onlook-dev/onlook — React/Next 프로젝트를 화면에서 편집하고 코드와 동기화하는, 디자이너를 위한 Cursor를 표방하는 도구. 디자이너와 개발자가 랜딩 페이지를 함께 조정하고 변경을 코드로 남길 때.
- webstudio-is/webstudio — Webflow 대안을 표방하는 오픈소스 비주얼 빌더. 거의 모든 CSS 속성과 헤드리스 CMS 연결, 호스팅 선택권이 강점이다.

### 컴포넌트와 CSS

- tailwindlabs/tailwindcss (MIT) — 유틸리티 퍼스트 CSS. grid·spacing·반응형을 빠르게 짜면서 토큰 제약을 코드에 반영한다.
- shadcn-ui/ui (MIT) — 컴포넌트를 블랙박스로 설치하는 대신 접근성 기반 UI 코드를 프로젝트로 가져와 직접 소유·수정한다. 복사한 코드도 유지보수 대상이다.
- radix-ui/primitives (MIT) — 스타일이 거의 없는 접근성 중심 프리미티브. 메뉴·팝오버·탭·다이얼로그의 행동을 브랜드 디자인과 분리해 구현한다.

### 토큰과 디자인 시스템

- style-dictionary/style-dictionary (Apache-2.0) — JSON 토큰을 CSS와 앱 플랫폼 산출물로 일관되게 변환하는 빌드 시스템. 홈페이지와 앱, 여러 테마에서 같은 토큰 원천을 유지할 때.
- tokens-studio/figma-plugin (MIT) — Figma에서 토큰을 관리하고 코드 측 토큰과 잇는다. DTCG 스펙(design-tokens/community-group)을 데이터 계약의 기준으로 삼으면 도구가 바뀌어도 토큰을 오래 쓸 수 있다.

### 모션

- motiondivision/motion (MIT) — 구 Framer Motion 계열 애니메이션 라이브러리. 히어로·진입·마이크로 인터랙션을 duration/easing 토큰으로 다룬다. 강한 스토리텔링 랜딩이라면 greensock/GSAP도 후보지만 상용 라이선스 조건을 직접 확인해야 한다.

### 문서화와 QA

- storybookjs/storybook (MIT) — 컴포넌트를 격리해 개발·문서화·테스트하는 표준. 작은 카드·버튼도 페이지 밖에서 상태별로 검증한다.
- microsoft/playwright — 여러 브라우저에서 E2E·시각 회귀 테스트를 만든다. 메뉴·CTA·폼과 viewport별 레이아웃의 회귀를 자동 점검한다.
- GoogleChrome/lighthouse — 성능·접근성·권장 사례·SEO를 수치로 감사한다. 예쁘게 보이는 것과 빠르고 발견 가능한 것은 다르다는 점을 배포 전에 확인시킨다. 접근성은 dequelabs/axe-core로 CI에 자동 검사를 붙인다.

### 리서치와 컨텍스트

- mendableai/firecrawl — 웹페이지를 Markdown·JSON·스크린샷 등 LLM 친화적 형태로 가져오는 크롤링 인프라. UI를 만드는 도구가 아니라 승인된 정보 구조를 디자인·콘텐츠 작업의 입력으로 넣는 컨텍스트 레이어다.

## 기능 매트릭스

같은 홈페이지 제작이라도 풀려는 문제에 따라 출발 레포가 달라진다.

| 문제 | 먼저 볼 레포 | 산출물 | 주의점 |
|------|-------------|--------|--------|
| 브랜드·홈페이지 규칙을 AI에 전달 | google-labs-code/design.md, VoltAgent/awesome-design-md | 색·타입·spacing·컴포넌트·금지 규칙을 담은 DESIGN.md | 타사 상표·카피가 아닌 내 디자인 언어를 문서화 |
| 기존 사이트 현대화 | JCodesMore/ai-website-cloner-template, firecrawl/open-lovable | 섹션 스펙, 오리지널 자산 목록, Next/React 코드 | 소유·허가 범위만. 인증·결제·계정 화면 제외 |
| 스크린샷에서 프로토타입 제작 | abi/screenshot-to-code | HTML/Tailwind/React/Vue 초안 | 스크린샷·이미지의 저작권·초상권부터 확인 |
| 디자인 토큰을 디자인·개발에서 동기화 | DTCG, Tokens Studio, Style Dictionary | JSON 토큰 → CSS/Android/iOS 산출물 | semantic token과 primitive token을 분리 |
| 기본 UI를 빠르게 구현 | Tailwind, shadcn/ui, Radix | 반응형 섹션, 접근성 프리미티브, 소유 가능한 UI 코드 | 컴포넌트를 섞기보다 하나의 토큰 규칙으로 정리 |
| 마케팅 팀과 시각적으로 반복 편집 | Onlook, Webstudio, Instatic | 시각 편집 페이지 또는 정적 출력 | 호스팅·CMS·권한·보안 모델을 먼저 검토 |
| 시각·접근성·성능 품질 자동 검증 | Storybook, Playwright, axe-core, Lighthouse | 컴포넌트 카탈로그, E2E, a11y, 성능 리포트 | 자동 검사는 보조 수단. 키보드·모바일 점검 병행 |

## 도입 전에 붙일 가드레일

유명 레포를 링크하는 것과 실제 서비스에 도입하는 것은 다른 일이다. 특히 AI 생성과 사이트 재구성 도구는 아래 기준을 템플릿, 에이전트 규칙, 코드 리뷰에 함께 넣어야 안전하다.

- 권리와 목적을 먼저 명시한다. 내 사이트 이전, 허가된 클라이언트 작업, 오리지널 UI 학습처럼 허용 목적을 문서로 남기고 타사 사칭·피싱·브랜드 위장은 금지한다.
- 인증·금융·개인정보 화면은 분리한다. 로그인·비밀번호·OTP·결제·계좌 화면은 분석·재현·자동화 대상에서 빼고, 테스트는 가짜 데이터와 별도 환경에서만 한다.
- 디자인 토큰과 브랜드 자산을 구분한다. spacing scale, contrast, responsive grid는 재사용 가능하지만 로고·고유 일러스트·브랜드 카피·사진은 별도 권리 검토가 필요하다.
- 라이선스·유지보수·비용을 확인한다. MIT, Apache-2.0, MPL, 상용 이중 라이선스, API 키·샌드박스 비용은 서로 다르다. 배포 전에 각 레포의 최신 LICENSE, SECURITY, release 상태를 다시 본다.
- 한국어 UI는 따로 검증한다. 영문 데모의 글자 수·행 높이·버튼 폭을 그대로 옮기지 말고 Pretendard, Noto Sans KR 같은 폰트와 한글 줄바꿈, 숫자·영문 혼용을 실제 콘텐츠로 확인한다.
- 생성 결과는 검토 후 병합한다. AI가 만든 코드에는 중복, 취약한 의존성, 의미 없는 ARIA, 무거운 에셋이 섞일 수 있다. 타입 검사, lint, visual diff, 성능·a11y 검사를 배포 게이트로 둔다.

## 마무리

이 지도의 쓸모는 레포 개수가 아니라 배치에 있다. 도구를 참고, 설계, 구현, 검증 순서로 세워 두면 지금 내게 빠진 레이어가 어디인지 한눈에 보인다. 별 수와 트렌딩은 빠르게 변하므로 링크를 공유하거나 도입하기 전에는 각 레포의 최신 README, LICENSE, 릴리스를 한 번 더 확인하는 편이 안전하다. 도구가 홈페이지를 완성해 주지는 않는다. 권리와 목적을 분명히 하고 자동 생성물에 사람의 검토를 게이트로 걸어 둘 때 이 지도가 제 몫을 한다.

## 출처

닷커넥터 자체 리서치 (2026 홈페이지 디자인·AI 빌드 GitHub 지도, 2026-07-29 스냅샷). 본문에 언급한 저장소는 google-labs-code/design.md, VoltAgent/awesome-design-md, abi/screenshot-to-code, firecrawl/open-lovable, JCodesMore/ai-website-cloner-template, onlook-dev/onlook, webstudio-is/webstudio, tailwindlabs/tailwindcss, shadcn-ui/ui, radix-ui/primitives, style-dictionary/style-dictionary, tokens-studio/figma-plugin, design-tokens/community-group, motiondivision/motion, greensock/GSAP, storybookjs/storybook, microsoft/playwright, GoogleChrome/lighthouse, dequelabs/axe-core, mendableai/firecrawl 등이며, 별 수와 활동 신호는 관찰 시점의 약값이다.
