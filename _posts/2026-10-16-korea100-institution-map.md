---
title: "법령을 한 장 구조도로 읽는 대한민국 제도 지도, Korea100"
date: 2026-10-16 00:10:08 +0900
categories: [정책, 기술]
tags: [대한민국 제도, 법령 시각화, 행정 리터러시, 오픈소스, 데이터 시각화, Agent Skill, Claude Code, Codex]
header:
  teaser: /assets/korea100-institution-map-home.jpg
permalink: /post/korea100-institution-map/
---
"기업에는 비즈니스 모델이 있듯이, 국가에는 제도 모델이 있다." 공개 웹서비스 Korea100의 소개 문구다. 서비스 화면에는 '대한민국 제도 지도'라는 이름으로 뜬다. Korea100은 대한민국의 주요 제도를 법령·기관·문서·기한·병목으로 나눈 뒤 한 장의 요약과 업무구조도로 다시 그린다. 저장소 README는 이 제도 모델을 일반 국민이 따라 읽을 수 있는 행정 리터러시의 형태로 만드는 것이 목표라고 밝힌다.

<figure>
<img src="/assets/korea100-institution-map-home.jpg" alt="Korea100 대한민국 제도 지도 첫 화면">
<figcaption>Korea100 첫 화면(2026년 10월 16일). 위쪽에 메뉴와 기준일 2026-09-14가 있고, 그 아래로 검색창, 제도·절차 노드 수, 분야별 목록, 제도 대장이 이어진다.</figcaption>
</figure>

## 줄글을 구조도로 바꾸는 방식

법령 원문에는 조문과 기관, 기한이 여기저기 흩어져 있다. Korea100은 이 줄글을 세 가지 구조로 다시 짠다. README가 정리한 대응 관계는 다음과 같다.

| 법령의 줄글 | Korea100의 구조 | 이해할 수 있는 질문 |
| --- | --- | --- |
| 조문·기관·기한이 흩어진 원문 | 한 장 요약. 목적, 권한, 돈·문서 흐름, 병목 | 이 제도는 왜 있고, 내게 무엇이 필요한가? |
| 신청·심사·통지·이의신청의 절차 | 업무구조도. 행위주체 레인, 단계, 근거 조문, 회귀 경로 | 누가 언제 무엇을 결정하며, 막히면 어디로 돌아가는가? |
| 법령만으로 확인할 수 없는 운영 정보 | 검증 대장. 근거와 확인 필요 사유를 공개 | 무엇이 확인됐고, 무엇을 더 확인해야 하는가? |

README는 법령을 요약하는 데서 멈추지 않고, 줄글을 구조도로 바꿔 행정이 실제로 작동하는 경로를 보이게 하는 것이 이 서비스의 목적이라고 설명한다.

## 지금 볼 수 있는 규모와 기능

저장소 README는 제도 509개, 절차 노드 6,883개, 법령 인용 8,746개, 현장 확인 필요 항목 1,924개를 소개한다. 2026년 10월 16일에 연 서비스 첫 화면에는 제도 660, 절차 노드 8,391이 표시돼 README보다 늘었고, 조문 인용 대조 15,407과 조문 검증 완료 575라는 항목도 함께 나온다. 목록이 계속 늘고 있으니 최신 규모는 서비스 화면에서 확인하는 편이 정확하다. 서비스에 표시된 법령 기준일은 2026년 9월 14일이다.

README가 꼽는 주요 기능은 다섯 가지다.

- 제도 찾기: 법령·기관·문서·병목 키워드로 제도를 찾고, 최대 3개를 같은 기준으로 비교한다.
- 제도 한 장 요약: 목적, 이해관계자, 법적 근거, 기관 권한, 돈·문서 흐름, 병목과 개선점을 한 화면에서 읽는다.
- 업무구조도: 국민, 심사기관, 정보시스템 같은 행위주체가 어떤 순서로 일하는지, 신청·반려·이의신청에서 어디로 되돌아가는지를 함께 보여 준다.
- 검증 대장: 법령만으로 확정할 수 없는 정보는 감추거나 추정하지 않고 [확인 필요 사유](https://hosungseo.github.io/korea100/verification/)와 함께 공개한다.
- 법령 지도: 법률 271건을 법률·시행령·시행규칙·행정규칙·자치법규 층으로 펼치고, 조문 사이의 위임선을 클릭해 따라간다. 제도 페이지의 법적 근거에서 [법령 지도](https://hosungseo.github.io/korea100/law/)로 바로 넘어간다.

첫 화면 메뉴에는 제도 대장, 법령 지도, 현장 검증 대장, 요청하기 말고도 메가프로젝트, 5극3특, AI 전후 비교, 종합상황판이 있다. 아래는 제도 대장에서 행정심판을 연 화면이다.

<figure>
<img src="/assets/korea100-institution-map-appeals.jpg" alt="Korea100 행정심판 제도 페이지의 업무구조도">
<figcaption>행정심판 제도 페이지. 절차 노드 17, 행위 레인 6, 게이트 6, 조문 확인 55/55, 병목 구간 4라는 요약 아래로 청구인·피청구인(처분청)·행정심판위원회 등 행위주체별 레인과 G0~G5 단계의 업무구조도가 펼쳐진다. 맨 아래 칸은 '서면·구술 심리' 노드의 기한과 법적 근거(행정심판법 제40조, 같은 법 시행령 제27조)를 보여 준다.</figcaption>
</figure>

## 데이터를 관리하는 네 가지 원칙

README는 정확성을 이 프로젝트의 핵심 가치로 꼽는다. 절차 노드에 붙은 법령·행정규칙·조약 인용은 다음 원칙으로 관리한다.

1. 원문 대조. 국가법령정보센터의 현행 원문으로 조문 번호가 맞는지뿐 아니라 그 조문이 실제 행위·주체·기한의 근거인지까지 확인한다.
2. 다층 검증. 구조·인용 형식·도달 가능성을 기계로 검사하고, 조문 의미 대조, 독립 절차 재구성, 당사자 관점 워크스루를 거친다.
3. 지어내지 않기. 공개 API에서 확인하지 못한 훈령·고시·내부 규정은 조문 번호를 추정하지 않고 `unverified`로 표시한다.
4. 정정 이력 공개. 발견하거나 수정한 오류는 각 제도 데이터의 `warnings`에 날짜와 근거를 남긴다.

## 데이터를 더 쓰고 싶을 때

Korea100은 읽는 웹서비스이면서, 제도 데이터를 다른 도구와 작업 흐름에 잇는 기반이기도 하다. 저장소에는 개발 환경·데이터 계약·검증 스크립트를 다룬 개발 문서(`docs/development.md`)와 해외 비교법 파일럿 두 건, 일본 환경영향평가와 베트남 상업 수입통관 문서가 공개돼 있다.

보고 싶은 제도가 없으면 [제작 요청 페이지](https://hosungseo.github.io/korea100/request/)에서 요청할 수 있다. 입력값은 서버에 저장되지 않고 사용자의 메일 앱 초안으로만 전달된다.

## 읽기 전에 알아둘 점

- 구조도에 보이는 '진행 중' 같은 상태는 실시간 행정 데이터가 아니라 제도 흐름을 설명하려고 붙인 편집 상태다.
- 법령 기준일은 제도마다 `asOfDate`로 표시된다. 법령은 개정되므로 중요한 판단을 하기 전에는 원문을 다시 확인해야 한다.
- Korea100은 법령 기준일 시점으로 작성한 참고자료다. 법률 자문이나 정부기관의 공식 해석(유권해석)을 대신하지 않는다.
- 저장소의 소프트웨어는 MIT 라이선스로 공개돼 있다.

## 업무구조도 렌더러를 떼어 낸 korea100studio

korea100studio는 Korea100의 업무구조도 렌더러를 특정 분야에 묶이지 않게 추출·일반화한 독립 에이전트 스킬(Agent Skill)이다. 행위자 × 단계 × 업무로 이루어진 프로세스라면 무엇이든 세로형 스윔레인(swimlane) 보드로 그리고, 보드의 구성 품질을 감사하고, 단계가 차례로 켜지는 애니메이션으로 내보낸다. `SKILL.md` 진입점과 네이티브 의존성이 없는 작은 ESM CLI(`scripts/board.mjs`)로 이루어져 있어 Claude Code와 Codex 안에서 그대로 동작한다.

같은 엔진에 프로필이 두 개 있다. `default`는 영어 라벨을 쓰는 중립 프로필로 어느 분야에나 쓸 수 있고, README의 예시는 소프트웨어 릴리스 보드다. `gov`는 Korea100식 한국 정부 스타일로 선행·핵심·병목·회귀 배지를 단다. 프로필은 `--profile` 플래그나 보드 파일의 `"profile"` 필드로 고른다.

<figure>
<img src="/assets/korea100-institution-map-studio-gov.jpg" alt="korea100studio gov 프로필 예시 보드, 행정심판 청구·심리·재결">
<figcaption>korea100studio 저장소의 gov 프로필 예시 보드 '행정심판 청구·심리·재결'. 위쪽에 행위자 레인 네 개, 왼쪽에 G0~G5 단계가 놓이고, 카드마다 근거 조문과 선행·핵심·병목 같은 배지가 붙는다.</figcaption>
</figure>

### 설치

README는 두 가지 설치 방법을 안내한다. 에이전트 스킬로 쓰려면 에이전트가 `SKILL.md`를 인식하도록 스킬 디렉터리에 클론한다.

```bash
# Claude Code
git clone https://github.com/hosungseo/korea100studio.git ~/.claude/skills/korea100studio
# Codex
git clone https://github.com/hosungseo/korea100studio.git ~/.agents/skills/korea100studio

cd ~/.claude/skills/korea100studio   # 클론한 위치로
npm install && npm test
```

어느 프로젝트에서든 CLI로 쓰려면 npm으로 설치한다.

```bash
npm install -g korea100studio
korea100studio render board.json --out board.svg

# 설치 없이:
npx korea100studio render board.json --out board.svg
```

### 명령과 입력

| 명령 | 용도 |
| --- | --- |
| `render <board.json> [--out f.svg] [--png] [--profile p]` | 보드를 SVG로 렌더하고, 래스터라이저가 있으면 PNG도 만든다 |
| `audit <board.json> [--json] [--profile p]` | 구성 점수와 지표를 출력한다(`--json`은 기계 판독용) |
| `validate <board.json> [--strict] [--profile p]` | 스키마와 구성 게이트를 검사한다(`--strict`면 위반 시 exit 1) |
| `motion <board.json> [--out f.svg] [--profile p]` | 단계 점등 애니메이션 SVG를 만든다 |
| `check <file.svg>` | SVG 구조 무결성을 점검한다 |

`--version`과 `--help`도 지원한다.

보드 입력은 `schemas/board-v1.schema.json`을 따르며 `lanes`(행위자), `stages`(단계), `nodes`(`{id, lane, stage, label, emphasis, refs}`), `edges`(`{id, source, target, type}`)로 구성된다. 자연어로 적힌 프로세스를 보드로 옮기는 방법은 `references/authoring.md`에, 시작용 골격은 `templates/board.template.json`에 있다. 존재하지 않는 레인이나 단계를 가리키거나, 엣지가 끊기거나, id가 중복되는 것처럼 스키마가 잡지 못하는 참조 오류는 어느 노드가 무엇을 잘못 참조했는지 메시지로 알려 준다.

순수 Node.js(20 이상)로 돌아가고, 의존성은 스키마 검증용 `ajv` 하나다. SVG는 항상 생성되고, PNG는 `rsvg-convert`(librsvg)나 `cairosvg`가 `PATH`에 있을 때만 나온다. 모션 출력은 JS나 외부 자산 없이 SMIL만 쓰는 자체 완결형 애니메이션 SVG다. 라이선스는 MIT다.

### 구성 품질 감사

`audit`는 보드의 배선 지오메트리를 교차, 노드관통, 꺾임, 우회율로 점수화한다. `validate`는 이를 품질 예산 게이트로 검사하며, `--strict`를 붙이면 예산을 넘었을 때 exit 1로 끝난다. 핵심 지표인 노드관통은 연결선이 관계없는 카드 뒤로 지나가 z-order에 가려지는 현상을 말한다. 렌더러는 거터 라우팅으로 행 내부 엣지와 회귀 엣지가 카드 뒤로 숨지 않게 한다.

## 출처

- Korea100(대한민국 제도 지도) 서비스: https://hosungseo.github.io/korea100/
- hosungseo/korea100 저장소 README: https://github.com/hosungseo/korea100
- hosungseo/korea100studio 저장소 README(한국어판): https://github.com/hosungseo/korea100studio
