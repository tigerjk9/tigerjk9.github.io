---
title: "Taste Skill v2, 방향 설정부터 브라우저 검사까지 맡는 코딩 에이전트용 디자인 스킬"
date: 2026-10-16 01:22:24 +0900
categories: [AI, 디자인]
tags: [AI에이전트, 코딩에이전트, 웹디자인, 프론트엔드, 에이전트스킬, 오픈소스, 생성형AI, UIUX]
header:
  teaser: /assets/taste-skill-v2-design-agent-skill-poster.jpg
permalink: /post/taste-skill-v2-design-agent-skill/
---

코딩 에이전트에게 웹 디자인 감각을 붙여 주는 오픈소스 스킬 모음 Taste Skill이 v2를 냈다. 깃허브 저장소 Leonxlnx/taste-skill(MIT 라이선스)은 2026년 10월 16일 기준 별 9만 7천여 개를 받았다. CHANGELOG에 따르면 2026년 10월 13일 나온 2.0.0의 기본 스킬은 이전 파일을 고친 것이 아니라 새로 만든 스킬이다. README는 이 스킬이 에이전트에게 아트 디렉션과 실제 사진, 그리고 자기 결과물을 실제 브라우저에서 검사하는 방법을 준다고 설명한다. 이 블로그는 2026년 7월 [Taste Skill을 처음 소개했고](/post/taste-skill-anti-slop-ai-design/), 이 글은 그 뒤 나온 정식 v2에서 달라진 점을 정리한다.

<figure>
<img src="/assets/taste-skill-v2-design-agent-skill-poster.jpg" alt="Taste Skill v2 출시 포스터. Your agent, with taste 문구와 설치 명령 npx skills add Leonxlnx/taste-skill, tasteskill.dev 주소가 적혀 있다">
<figcaption>v2.0.0 릴리스에 첨부된 포스터. 설치 명령과 홈페이지 주소가 함께 적혀 있다.</figcaption>
</figure>

## v2 소개글의 여섯 항목과 저장소 문서

v2 소개글(SNS)은 바뀐 점을 여섯 줄로 요약했다. 저장소의 README, CHANGELOG, 릴리스 노트에 적힌 내용과 하나씩 맞춰 보면 다음과 같다.

| v2 소개글 | 저장소 문서에 적힌 내용 |
|---|---|
| 247개 웹사이트 분석 기반 디자인 제안 | 기본 스킬은 엄선한 사이트 247곳(One Page Love, Awwwards의 Sites of the Day)을 연구해 만들었다 |
| 20가지 디자인 방향과 다양한 레이아웃 | 연구로 정리한 디자인 방향 20가지에, 히어로 구성 48가지와 섹션 구성 172가지를 라이브러리로 갖췄다 |
| 실제 사진·영상 소재 자동 탐색 | `scripts/assets.mjs`가 열린 컬렉션에서 사진·지도·영상을 찾아 내려받고 출처를 기록한다 |
| 타이포그래피·색상·애니메이션 구성 | 무료 글꼴로 짠 타입 시스템 44가지, 팔레트 56가지, 모션 11가지가 라이브러리에 들어 있다 |
| PC·태블릿·모바일 화면 검사 | `scripts/inspect.mjs`가 실제 브라우저에서 1440·768·390px 너비로 페이지를 열어 측정한다 |
| 글자 잘림·화면 넘침 등 문제 탐지 | 가려지거나 잘린 글자, 가로로 넘치는 화면을 실패 항목으로 잡는다 |

PC·태블릿·모바일은 소개글의 표현이고, 문서에는 세 가지 픽셀 너비만 적혀 있다.

## 여섯 단계로 돌아가는 기본 스킬

README에 따르면 기본 스킬(`taste-skill`, 설치명 `design-taste-frontend`)은 페이지 하나를 만들 때 여섯 단계를 거친다. CHANGELOG의 설명을 더해 정리하면 이렇다.

1. 인벤토리. 디자인을 시작하기 전에 이 고객만 가진 것을 적는다. 이름과 그 뜻, 거리, 숫자, 단 하나의 제약 같은 것이다.
2. 방향 뽑기. `scripts/draw.mjs`가 20가지 방향 가운데 3개를 뽑아 내밀면, 에이전트는 인벤토리의 무언가를 담아낼 수 있는 하나를 고른다. 나머지는 스크립트가 라이브러리에서 뽑아 준다. 라이브러리에는 히어로 구성 48, 섹션 구성 172, 타입 시스템 44, 팔레트 56, 사진 420, 모션 11가지와 연구한 참고 사이트 181곳이 있다. 뽑힌 청사진마다 그것이 스킬 자체 규칙과 어긋나는 지점도 함께 출력한다.
3. 아이디어와 움직이는 요소 하나. 고객 자신의 자료를 고른 방향의 장치와 잇는 한 문장을 만들고, 가장 가까운 경쟁자와 비교해 확인한다. 방문자가 페이지에서 직접 해 볼 수 있는 것도 하나 넣는다.
4. 빌드. 내용을 끝까지 채워 페이지를 만든다. 자체 사진이 없으면 주제와 관련된 실제 사진을 열린 컬렉션에서 가져오고, 정직하게 쓸 사진이 존재하지 않는 대상만 코드로 그린다.
5. 관문 검사. `scripts/lint.mjs`가 소스를 훑고, `scripts/inspect.mjs`가 실제 브라우저에서 세 너비로 페이지를 열어 측정한다. 슬롭이 발견되면 실패다.
6. 스스로 보기. 에이전트가 자기 스크린샷을 Awwwards 가중치를 따른 기준으로 비평하고 가장 큰 문제 세 가지를 고친다. 이 과정을 최대 세 차례 반복한다.

한 번 빌드하는 데 30~45분쯤 걸리고 토큰은 수십만 개를 쓴다. CHANGELOG는 그 대부분이 프로젝트에 사진이 없을 때 사진을 찾거나 그리는 데 든다고 설명한다.

## 브라우저 검사기가 실패로 판정하는 것

v2 소개글이 화면 검사와 문제 탐지로 요약한 부분이다. CHANGELOG에 실린 실패 항목은 다음과 같다.

- 작은 머리말 라벨(eyebrow label), 코드 밖에서 쓴 고정폭 글꼴, 01/02/03 식 번호 매기기
- 가는 선(hairline)과 테두리만 친 상자, 그라데이션, 가만히 있을 때도 깔린 그림자
- 크림과 테라코타 조합 또는 보라색 팔레트
- 두 줄을 넘는 헤드라인, 13px보다 작은 글자
- 첫 화면에 시선이 머물 초점이 없는 경우, 거의 비어 있는 화면
- 가려지거나 잘린 글자, 가로 방향으로 넘치는 화면

사진과 움직임도 검사한다. CHANGELOG에 따르면 첫 v2로 만든 페이지 10개에는 실제 사진이 하나도 없었고 움직임도 거의 없었다. 강제하지 않으면 에이전트가 사진과 모션을 건너뛴다는 사실이 테스트에서 드러나 검사기에 두 항목을 넣었다. `few-pictures`는 실제 사진(사진, 기록 이미지, 영상, 래스터 아트워크, 소프트웨어라면 잘라 낸 화면 조각)이 4개보다 적으면 실패로 처리하고, SVG 그림은 세지 않는다. 실제 사진이 2개 미만이거나 영상이 없으면 `no-real-pictures`와 `no-footage` 경고가 뜬다. `still-page`는 페이지를 불러오고 스크롤하는 동안 실제로 움직이는 요소를 세어 8개 미만이면 실패, 16개 미만이면 경고를 낸다.

모션 지침도 함께 바뀌었다. 눈에 띄는 대표 동작 하나, 섹션마다 짜인 등장 연출, 모든 조작 요소의 반응, 움직이는 그림 하나를 요구한다. 움직임을 한 순간에만 쓰라던 예전 제한은 없어졌고, 모든 블록에 똑같은 페이드업을 거는 것은 여전히 금지다.

## 실제 사진을 찾아 쓰는 방식

CHANGELOG는 사진이 없는 에이전트가 예전에는 모든 것을 SVG로 그렸다고 적는다. v2의 `scripts/assets.mjs`는 API 키 없이 Openverse, Wikimedia Commons, 시카고 미술관(Art Institute of Chicago), 메트로폴리탄 미술관을 검색한다. 찾은 이미지마다 직접 링크, 원본 페이지, 크기, 만든 사람, 라이선스, 한 줄 출처 표기를 출력한다. 기본값으로는 상업적 이용이 가능한 라이선스(CC0, 퍼블릭 도메인, CC BY, CC BY-SA)만 남기고, 출력한 이미지가 실제로 열리는지도 확인한다. `--get`으로 받은 사진은 프로젝트의 `assets/`에 저장되고 출처는 `assets/credits.json`에 기록된다. `--video`를 붙이면 Wikimedia Commons, Internet Archive, NASA에서 열린 라이선스 영상을 찾아 소리 없는 반복 클립으로 쓸 수 있다.

이미지를 고르는 순서도 정해져 있다. 프로젝트 자체 이미지가 먼저이고, 그다음이 생성 이미지, 열린 컬렉션에서 찾은 주제 세계의 실제 사진(그 거리의 옛 엽서와 옛 지도, 재료, 그 업종을 그린 판화, 같은 종류의 박물관 소장품), 코드로 그린 그림, 스크립트가 뽑아 준 분위기 사진, 글자와 색만 쓰는 방식 순이다. 찾아온 사진을 고객의 제품, 매장, 요리, 사람, 팀인 것처럼 내세우지 않으며, 모든 사진은 페이지에 출처를 밝히고 보고서에도 목록으로 남긴다.

<figure>
<img src="/assets/taste-skill-v2-design-agent-skill-example-roast.jpg" alt="커피 가게 페이지의 로스팅 섹션. Raw, First crack, Dropped, Cooled 네 단계를 사진 네 장으로 보여 준다">
<figcaption>README에 실린 v2 예시. 커피 가게 페이지가 로스팅의 네 단계를 사진 네 장으로 보여 준다.</figcaption>
</figure>

<figure>
<img src="/assets/taste-skill-v2-design-agent-skill-example-night.jpg" alt="테크노 파티 페이지. 기계가 들어찬 산업 시설의 기록 사진을 청록색과 검은색으로 물들이고 그 위에 공연 날짜 칸을 배치했다">
<figcaption>같은 README의 테크노 파티 페이지. 산업 시설 기록 사진 위에 공연 날짜 칸을 끼워 넣었다.</figcaption>
</figure>

README는 이 예시들이 브리프 하나씩으로 만든 페이지이며, 사진은 열린 아카이브에서 찾아 스킬이 출처를 단 실제 사진이라고 밝힌다.

## 테스트 결과와 개발자가 밝힌 한계

CHANGELOG에는 테스트 기록도 있다. 브리프 여섯 개로 블라인드 비교를 다섯 차례 했다. 새 에이전트가 같은 브리프로 스킬 없이, v2로, 그리고 세 브리프에서는 다른 디자인 스킬로 페이지를 만들었고, 별도 에이전트가 익명 스크린샷을 Awwwards 가중치로 채점했다. 마지막 라운드(브리프 3개)의 점수는 v2 7.7, 스킬 없음 7.8, 다른 스킬 7.2였고, v2는 세 브리프 중 두 곳에서 1위였다. 평균 점수만 보면 스킬 없이 만든 페이지가 0.1점 높았다. 검사기로 재면 v2 페이지는 각각 실패 0건, 스킬 없이 만든 페이지는 8~13건이었다.

개발자는 한계도 적어 두었다. 라운드마다 브리프 하나에 심사자가 한 명뿐이라 0.5점 안팎의 오차가 있고, 심사자는 모델이며, 마지막 라운드의 브리프는 직전 라운드에서도 쓴 것이었다.

릴리스 노트는 다른 비교도 실었다. 테스트 브리프 4개를 스킬 없이 만들었을 때는 작은 라벨 37개와 가는 구분선 249개가 나왔고, 스킬을 쓰면 하나도 나오지 않았다. 사진은 스킬 없이 0장, 스킬을 쓰면 48장이었다.

## 다이얼 없는 v2와 이전 판

v2 이전의 두 판은 파일 맨 위에 1~10 범위의 다이얼 세 개를 둔다. `DESIGN_VARIANCE`(가운데 정렬의 단정한 배치부터 비대칭까지), `MOTION_INTENSITY`(호버만부터 스크롤 연동까지), `VISUAL_DENSITY`(여유로운 배치부터 빽빽한 배치까지)다. v2에는 다이얼이 없다. README의 설명대로 방향은 뽑기에서, 한계는 검사기에서 정해진다. 형태도 단일 `SKILL.md`가 아니라 지침, 참고 파일 9개, 라이브러리, 의존성 없는 스크립트 4개로 이뤄진 폴더다.

예전 판도 그대로 쓸 수 있다. 7월 글에서 다룬 브리프 추론, 다크 모드 프로토콜, 최종 점검표 같은 규칙은 v2 직전까지 기본값이던 v2 (experimental)의 내용이다. 이 판은 지금 `taste-skill-v2-experimental`(설치명 `design-taste-frontend-v2-experimental`)로 남아 있고, 최초 판은 `taste-skill-v1`(설치명 `design-taste-frontend-v1`)이다. README는 두 판을 정확한 동작에 의존하는 프로젝트를 위해 보존한다고 밝힌다.

## 설치와 요구 사항

README의 설치 명령은 다음과 같고, 저장소의 스킬을 모두 설치한다.

```bash
npx skills add https://github.com/Leonxlnx/taste-skill
```

v2 소개글과 출시 포스터에 적힌 `npx skills add Leonxlnx/taste-skill`은 같은 저장소를 `owner/repo` 약칭으로 쓴 것이다. `npx skills` CLI의 README(vercel-labs/skills)에도 깃허브 약칭(owner/repo)으로 설치하는 방법이 나온다. 기본 스킬 하나만 설치하려면 설치명을 넘긴다.

```bash
npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"
```

Claude Code에서는 `/plugin marketplace add Leonxlnx/taste-skill`을 실행한 뒤 `/plugin install taste-skill@taste-skill`로 플러그인을 설치한다. 모든 스킬이 `taste-skill:` 이름공간에 들어가 다른 스킬과 이름이 겹치지 않는다. Codex에서는 `codex plugin marketplace add Leonxlnx/taste-skill`과 `codex plugin add taste-skill@taste-skill`을 실행하고 새 세션을 열어야 스킬이 올라온다. Codex 플러그인 설치는 2.0.0에서 추가됐다.

이미 설치했다면 설치 명령을 다시 실행하면 된다. 설치명이 바뀌지 않았으므로 기본 스킬은 v2로 교체되고, 예전 판은 각자의 이름으로 남는다.

기본 스킬을 쓰려면 Node 22 이상과 Chrome, Edge, Chromium 가운데 하나가 설치돼 있어야 한다. 검사기는 DevTools 프로토콜로 브라우저를 조작하며 따로 설치하는 것이 없다. `draw.mjs`, `lint.mjs`, `assets.mjs`는 Node 18 이상에서 돌고, API 키는 필요 없으며, 인터넷 연결은 사진을 찾을 때만 쓴다. 작업 파일은 프로젝트의 `.taste-skill/`에, 방향 뽑기 기록은 `~/.taste-skill/history.json`에 쌓인다.

## 기본 스킬 밖의 구성

기본 스킬 외에 특정 작업용 스킬 8개와 이미지 생성 스킬 3개가 함께 들어 있다. 하나만 쓰려면 설치명을 `--skill`에 넘긴다.

| 스킬 | 설치명 | 하는 일 |
|---|---|---|
| redesign-skill | `redesign-existing-projects` | 기존 프로젝트의 UI를 먼저 감사한 뒤 레이아웃, 간격, 위계, 스타일을 고친다 |
| image-to-code-skill | `image-to-code` | 사이트 참고 이미지를 생성해 분석하고, 그에 맞춰 프론트엔드를 만든다 |
| gpt-tasteskill | `gpt-taste` | GPT와 Codex용으로 더 엄격하게 만든 변형. 레이아웃 변화 폭이 크고 모션 방향이 강하다 |
| soft-skill, minimalist-skill, brutalist-skill | `high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui` | 시각 방향이 정해졌을 때 쓰는 스타일 스킬. 차례로 부드러운 대비와 여백·스프링 모션의 차분한 UI, 절제된 팔레트와 또렷한 구조의 편집 디자인풍 제품 UI, 스위스 타이포그래피와 강한 대비·실험적 레이아웃의 기계적인 시각 언어다 |
| stitch-skill | `stitch-design-taste` | Google Stitch용 규칙. 원하면 `DESIGN.md`로 내보낼 수 있다 |
| output-skill | `full-output-enforcement` | 모델이 작업을 반쯤 끝낸 채 내놓을 때, 자리표시 주석 없이 전체를 출력하게 한다 |
| imagegen-frontend-web, imagegen-frontend-mobile, brandkit | 스킬 이름과 같음 | 코드 없이 디자인 이미지만 만든다. 차례로 웹사이트 시안(히어로, 랜딩 페이지, 여러 섹션), iOS·Android·크로스플랫폼 모바일 화면과 흐름, 로고 방향·팔레트·글꼴·적용 예시를 담은 브랜드 키트 보드다 |

이미지 생성 스킬은 ChatGPT Images, Codex 이미지 모드처럼 이미지를 만드는 에이전트에서 쓰고, 나온 화면을 코딩 에이전트에 넘기는 방식이다. README의 선택 안내는 간단하다. 새 공개 페이지는 taste-skill, 이미 있는 페이지 개선은 redesign-skill, 시각 방향이 정해졌으면 soft-skill·minimalist-skill·brutalist-skill 가운데 하나를 쓴다. 이미지를 먼저 만들고 코드로 옮기려면 이미지 생성 스킬을 쓰거나 전 과정을 한 번에 처리하는 image-to-code-skill을 쓰고, 에이전트가 출력을 자꾸 짧게 자르면 output-skill을 더한다.

기본 스킬은 공개용 페이지를 위한 것이어서 대시보드나 앱 화면에는 맞지 않는다. 제품 UI에는 minimalist-skill이나 soft-skill을 권한다. 규칙이 특정 프레임워크가 아니라 디자인에 관한 것이라 React, Vue, Svelte, 일반 HTML에 모두 쓸 수 있다.

README 맨 위에는 TasteCode도 소개돼 있다. Taste Skill을 디자인 에이전트가 들어간 데스크톱 앱으로 만든 것으로 무료 오픈소스이고, 앱의 디자인 에이전트가 브리프 작성, 빌드, UI 시각 검토를 맡는다. README는 이것을 Taste Skill의 결과를 가장 쉽게 얻는 방법으로 안내한다.

## 출처

- Leonxlnx, taste-skill (GitHub 저장소, MIT 라이선스): [https://github.com/Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)
- taste-skill CHANGELOG, 2.0.0 (2026-10-13): [https://github.com/Leonxlnx/taste-skill/blob/main/CHANGELOG.md](https://github.com/Leonxlnx/taste-skill/blob/main/CHANGELOG.md)
- tasteskill v2 릴리스 노트 (v2.0.0): [https://github.com/Leonxlnx/taste-skill/releases/tag/v2.0.0](https://github.com/Leonxlnx/taste-skill/releases/tag/v2.0.0)
- Taste Skill 홈페이지: [https://tasteskill.dev](https://tasteskill.dev)
- Taste Skill v2 소개글 (SNS)
