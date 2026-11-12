---
title: "스킬 154만 개에서 맞는 것을 찾아 설치해 주는 find-skills"
date: 2026-11-11 15:06:08 +0900
categories: [AI, 코딩]
tags: [ClaudeCode, AI에이전트, find-skills, 생산성, 자동화]
description: "Claude에게 이거 하는 스킬 있어라고만 물으면 스킬 154만 개 중에서 맞는 것을 찾아 설치까지 해 준다. find-skills라는 스킬이 하는 일이다."
header:
  teaser: /assets/find-skills-claude-agent-src1-thumb.jpg
permalink: /post/find-skills-claude-agent/
---

Claude에게 "이거 하는 스킬 있어?"라고만 물으면 스킬 154만 개 중에서 맞는 것을 찾아 설치까지 해 준다. find-skills라는 스킬이 하는 일이다. 스킬을 찾아 주는 스킬이라 처음 들으면 말장난 같지만, 공개된 스킬이 이만큼 많아지면 무엇을 고를지가 가장 큰 일이 된다.

<figure>
<img src="/assets/find-skills-claude-agent-src1-thumb.jpg" alt="영상 클로드 스킬 154만 개, 말만 하면 알아서 찾아 깔아 줍니다의 썸네일">
<figcaption>영상 썸네일. (출처: 빌더 조쉬 Builder Josh)</figcaption>
</figure>

## 스킬이 무엇인가

스킬은 AI 에이전트에게 특정 작업을 하는 방법을 적어 준 재사용 가능한 지시서다. 코드 리뷰를 하는 순서, 특정 라이브러리를 쓰는 요령, PPT 파일을 만드는 절차 같은 것을 `SKILL.md`라는 문서 하나에 정리해 두면, 에이전트가 그 일을 부탁받았을 때 문서를 읽고 그대로 따른다. 사람으로 치면 업무 매뉴얼을 책상에 꽂아 두는 일과 비슷하다.

이런 스킬을 모아 둔 공개 마켓이 skills.sh다. 영상 제작자가 정리한 안내 페이지에 따르면 2026년 10월 30일 기준 skills.sh에 등록된 스킬은 1,543,559개다. 같은 일을 하는 스킬이 여럿 있고, 공식 출처에서 만든 것과 잘 모르는 작성자가 올린 것이 같은 목록에 섞여 있다. 사람이 직접 고르려면 검색하고, 설치 수를 비교하고, 저장소를 열어 보는 일을 매번 해야 한다.

## find-skills가 하는 일

find-skills는 이 고르는 일을 에이전트에게 맡긴다. 사용자가 "PPT 만드는 스킬 찾아 줘"라고 하면 설치 순위부터 확인하고, 후보를 골라 설치 명령어까지 보여 주며, "설치해 줘"라고 하면 지금 프로젝트에 바로 설치한다.

| 항목 | 내용 |
| --- | --- |
| 만든 곳 | Vercel의 스킬 저장소 `vercel-labs/skills` (MIT 라이선스) |
| 순위 | skills.sh 전체 설치 수 1위. 영상 시점 411만 번, 2026년 11월 skills.sh 페이지 표기 430만 번 |
| 저장소 GitHub 별 | 영상 시점 3만 7천 개, 2026년 11월 skills.sh 페이지 표기 3만 8,900개 |
| 비용 | 무료 |
| 필요한 환경 | Node.js 22.20 이상 |
| 쓸 수 있는 에이전트 | Claude Code, Codex, Cursor, OpenCode와 그 밖의 75개, 모두 79개 |

스킬 문서(`SKILL.md`)에 적힌 작업 순서는 다음과 같다.

1. 사용자가 필요한 것의 분야(예: 디자인, 테스트, 배포)와 구체적인 작업을 파악한다.
2. skills.sh 순위표부터 확인해 이미 널리 쓰이는 스킬이 있는지 본다.
3. 순위표에 없으면 `npx skills find [검색어]`로 검색한다.
4. 검색 결과만 보고 추천하지 않고 품질을 확인한다.
5. 스킬 이름, 하는 일, 설치 수, 출처, 설치 명령, skills.sh 링크를 함께 보여 준다.
6. 사용자가 원하면 `npx skills add <owner/repo@skill> -g -y`로 설치한다.

4단계의 품질 기준이 이 스킬의 핵심이다. 설치 수는 1천 회 이상을 우선하고 100회 미만은 조심한다. 출처는 `vercel-labs`, `anthropics`, `microsoft` 같은 공식 출처를 모르는 작성자보다 믿는다. 스킬이 든 저장소의 GitHub 별이 100개 미만이면 의심하고 본다. 스킬은 에이전트가 그대로 따르는 지시서라서, 엉터리 스킬을 깔면 에이전트가 엉터리로 일한다. 아무 스킬이나 검색 1위라는 이유로 깔지 않게 막는 장치가 여기에 들어 있다. 맞는 스킬을 못 찾으면 그 사실을 알리고, 에이전트가 직접 작업을 돕거나 사용자가 `npx skills init`으로 자기 스킬을 만들 수 있다고 안내한다.

## 설치하기

`npx`는 Node.js에 딸린 명령으로, 프로그램을 미리 깔지 않고 바로 내려받아 실행한다. 그래서 Node.js가 먼저 깔려 있어야 하고, 버전이 22.20 이상이어야 한다. 터미널에서 `node -v`를 입력하면 버전을 확인할 수 있다.

skills.sh 페이지에 적힌 기본 설치 명령은 다음과 같다. 이 명령은 지금 터미널이 열린 폴더(프로젝트)에만 설치한다.

```bash
npx skills add https://github.com/vercel-labs/skills --skill find-skills
```

어느 폴더에서 Claude Code를 열어도 쓰고 싶다면 영상 안내 페이지가 권하는 명령을 쓴다.

```bash
npx skills add vercel-labs/skills --skill find-skills -g -a claude-code -y
```

| 옵션 | 뜻 |
| --- | --- |
| `-g` | 전역 설치. 모든 프로젝트에서 쓴다 |
| `-a claude-code` | 설치할 에이전트 지정. Codex면 `-a codex`, Cursor면 `-a cursor` |
| `-y` | 확인 질문을 건너뛴다 |

전역과 프로젝트 설치는 쓰임이 다르다. 혼자 쓰는 스킬은 `-g`로 한 번 깔아 두면 편하다. 안내 페이지는 반대로 팀 단위로 맞출 때는 `-g` 없이 프로젝트 폴더에 설치하라고 권한다. 그 저장소를 여는 사람이 모두 같은 스킬을 쓰게 되기 때문이다.

## 스킬이 안 보일 때

안내 페이지가 정리한 점검 순서는 다음과 같다.

- `-g` 없이 설치했다면 설치한 그 폴더에서 Claude Code를 열어야 보인다. 다른 폴더에서도 쓰려면 `-g`로 다시 설치한다.
- 설치 후 Claude Code를 껐다 켠다. 새 스킬은 시작할 때 읽는다.
- Claude Code에서 `/`를 눌러 목록에 find-skills가 있는지 확인한다.
- 이 설치 방법은 Claude 앱의 채팅창이 아니라 터미널에서 쓰는 Claude Code용이다.
- Node.js 버전이 22.20 이상인지 `node -v`로 확인한다.

## 이렇게 물어보면 된다

사용법은 말로 묻는 것이 전부다. 안내 페이지는 분야별 질문 예시 40개를 실었고, 괄호 안에 2026년 10월 30일 skills.sh 검색에서 실제로 나온 대표 스킬과 설치 수를 적었다. 문서 작업에 가까운 예시 몇 개를 옮기면 다음과 같다.

| 질문 | 검색에서 나온 대표 스킬 |
| --- | --- |
| PPT 만드는 스킬 찾아 줘 | anthropics/skills의 pptx (24.5만) |
| 워드(docx) 보고서 만들고 고치는 스킬 있어? | anthropics/skills의 docx (21.0만) |
| 엑셀 파일 분석하고 수식 넣는 스킬 찾아 줘 | anthropics/skills의 xlsx (19.0만) |
| PDF 합치고 표 뽑아내는 스킬 있어? | anthropics/skills의 pdf (21.9만) |
| 노션 API 쓰는 스킬 찾아 줘 | intellectronica/agent-skills의 notion-api (9.7만) |
| 새 스킬을 직접 만드는 스킬 찾아 줘 | anthropics/skills의 skill-creator |

회의록 정리, 웹 접근성 점검, 반복 업무 자동화처럼 대표 스킬이 적혀 있지 않은 질문도 그대로 던지면 된다. 고르는 기준을 같이 말하면 결과가 더 정확해진다. "설치 수 1만 이상, 공식 출처만 골라 줘", "후보 3개 비교표로 보여 줘", "전역(-g)으로 설치해 줘"처럼 조건을 붙이는 식이다. 새 작업을 시작하기 전에 "이 작업에 쓸 만한 스킬 먼저 찾아 줘"라고 한 번 물어 두면, 남들이 이미 다듬어 둔 방법으로 출발할 수 있다.

## 설치한 뒤 관리하기

find-skills가 쓰는 도구는 Vercel의 skills CLI(터미널 명령 프로그램)다. 이 CLI로 설치한 스킬을 관리할 수도 있다.

| 명령 | 하는 일 |
| --- | --- |
| `npx skills list` | 설치된 스킬 목록 |
| `npx skills check` | 업데이트가 있는지 확인 |
| `npx skills update` | 설치된 스킬 업데이트 |
| `npx skills remove` | 스킬 제거 |
| `npx skills use <source>@<skill>` | 설치하지 않고 한 번만 써 보기 |

Claude Code 안에서 "설치된 스킬 업데이트 확인해 줘"라고 해도 된다. 저장소 설명에 따르면 이 CLI는 익명 사용 데이터를 수집하며, 환경 변수 `DISABLE_TELEMETRY=1`이나 `DO_NOT_TRACK=1`을 설정하면 끌 수 있다.

skills.sh는 스킬마다 보안 점검 결과도 보여 준다. find-skills 페이지에는 Gen Agent Trust Hub와 Socket 점검이 통과(Pass), Snyk 점검이 경고(Warn)로 표시돼 있다. 다른 스킬을 깔 때도 설치 수와 출처에 더해 이 표시를 한 번 보고 넘어가면 좋다.

## 출처

- 빌더 조쉬 Builder Josh. (2026-10-31). [클로드 스킬 154만 개, 말만 하면 알아서 찾아 깔아 줍니다 (무료)](https://www.youtube.com/shorts/6lPgzuKb90g). YouTube.
- 빌더 조쉬 Builder Josh. [파인드 스킬즈(find-skills) 설치 + 바로 쓰는 질문 예시 40개](https://tuemarz.notion.site/find-skills-40-409137c926d581e49251cd2f1770447b). Notion.
- Vercel Labs. [find-skills](https://skills.sh/vercel-labs/skills/find-skills). skills.sh.
- Vercel Labs. [skills](https://github.com/vercel-labs/skills). GitHub.
- Vercel Labs. [find-skills SKILL.md](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md). GitHub.
