---
title: "스킬 154만 개에서 맞는 것을 찾아 설치해 주는 find-skills"
date: 2026-11-11 15:06:08 +0900
categories: [AI, 코딩]
tags: [ClaudeCode, AI에이전트, find-skills, 생산성, 자동화]
description: "Claude에게 이거 하는 스킬 있어라고만 물으면 스킬 154만 개 중에서 맞는 것을 찾아 설치까지 해 주는 스킬 find-skills를 정리한다. 스킬 마켓 전체 설치 수 1위이고 Vercel의 스킬 저장소에 들어 있다."
header:
  teaser: /assets/find-skills-claude-agent-src1-thumb.jpg
permalink: /post/find-skills-claude-agent/
---

Claude에게 "이거 하는 스킬 있어?"라고만 물으면 스킬 154만 개 중에서 맞는 것을 찾아 설치까지 해 준다. find-skills라는 스킬이 하는 일이다.

<figure>
<img src="/assets/find-skills-claude-agent-src1-thumb.jpg" alt="영상 클로드 스킬 154만 개, 말만 하면 알아서 찾아 깔아 줍니다의 썸네일">
<figcaption>영상 썸네일. (출처: 빌더 조쉬 Builder Josh)</figcaption>
</figure>

## find-skills 개요

find-skills는 스킬 마켓 skills.sh에서 전체 설치 수 1위인 스킬이다. 영상 시점에 411만 번 설치됐다. Vercel이 만든 스킬 저장소 `vercel-labs/skills`에 들어 있고, 이 저장소의 GitHub 별은 영상 시점에 3만 7천 개다. 저장소 라이선스는 MIT다.

## 찾고 설치하는 과정

1. "PPT 만드는 스킬 찾아 줘"처럼 필요한 일을 말한다.
2. find-skills가 설치 순위부터 확인하고 후보를 골라 설치 명령어까지 보여 준다.
3. "설치해 줘"라고 하면 지금 프로젝트에 바로 설치된다.

skills.sh의 스킬 페이지에 따르면 find-skills는 먼저 skills.sh 순위표에서 검증된 인기 스킬을 확인하고, `npx skills find [검색어]`로 검색한 뒤, 고른 스킬을 `npx skills add <패키지>`로 설치한다. 후보를 가릴 때는 설치 수, 만든 곳의 신뢰도, GitHub 별을 본다.

find-skills 자체는 스킬 페이지에 적힌 아래 명령으로 설치한다.

```bash
npx skills add https://github.com/vercel-labs/skills --skill find-skills
```

## 쓸 수 있는 에이전트

Claude Code뿐 아니라 Codex, Cursor 등 80개 가까운 에이전트에서 똑같이 쓴다. 스킬을 찾느라 검색할 필요 없이 필요한 것을 말하면 된다.

## 출처

- 빌더 조쉬 Builder Josh. (2026-10-31). [클로드 스킬 154만 개, 말만 하면 알아서 찾아 깔아 줍니다 (무료)](https://www.youtube.com/shorts/6lPgzuKb90g). YouTube.
- Vercel Labs. [find-skills](https://skills.sh/vercel-labs/skills/find-skills). skills.sh.
- Vercel Labs. [skills](https://github.com/vercel-labs/skills). GitHub.
