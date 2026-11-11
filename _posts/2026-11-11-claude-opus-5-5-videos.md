---
title: "Claude Opus 5.5로 만든 영상 418편과 프롬프트 703개 모음"
date: 2026-11-11 14:07:15 +0900
categories: [AI]
tags: [Claude, 프롬프트, 모션그래픽, 생성형AI, 바이브코딩]
header:
  teaser: /assets/claude-opus-5-5-videos-thumb.jpg
permalink: /post/claude-opus-5-5-videos/
description: "Claude Opus 5.5에게 애니메이션을 코드로 써 달라고 해서 만든 영상과 그 프롬프트를 모은 깃허브 저장소가 있다. 프롬프트 703개가 올라와 있고, 그중 418편은 Skillry에서 원본과 리메이크를 나란히 볼 수 있다."
---

Claude Opus 5.5에게 애니메이션을 코드로 써 달라고 해서 만든 영상과 그 프롬프트를 모은 깃허브 저장소가 있다. `yihui-dev/awesome-opus5-5-videos`에는 프롬프트 703개가 올라와 있고, 그중 418편은 Skillry에서 원본과 리메이크를 나란히 볼 수 있다. 영상 편집 프로그램으로 만든 것이 아니라 HTML, Canvas, SVG, Three.js 같은 코드가 화면을 그린다.

<figure>
<img src="/assets/claude-opus-5-5-videos-thumb.jpg" alt="Skillry의 Opus 5.5 영상 모음 페이지 대표 이미지">
<figcaption>Skillry의 Opus 5.5 영상 모음 페이지 대표 이미지. (출처: skillry.dev)</figcaption>
</figure>

## 두 곳에 나뉘어 있는 자료

| 곳 | 들어 있는 것 | 쓰임 |
|---|---|---|
| 깃허브 저장소 | `prompts/` 폴더의 프롬프트 703개, 목록 파일 `data/videos.json`, README에 고른 리메이크 100편 | 프롬프트를 복사해 내 에이전트에서 실행 |
| Skillry 페이지 | 영상 418편, 원본과 실시간 리메이크 나란히 보기 | 결과를 눈으로 비교하며 고르기 |

저장소의 항목마다 만든 사람의 원 게시물 링크가 붙어 있다. 프롬프트가 공개되지 않은 영상은 프롬프트 대신 원 게시물을 싣는다. README 기준 마지막 갱신은 2026년 10월 12일이고, 그날 프롬프트 285개와 영상 10편이 추가됐다.

## 영상의 갈래

Skillry 페이지는 418편을 네 갈래로 나눈다.

| 갈래 | 편수 |
|---|---|
| 모션 그래픽 | 229 |
| 설명 영상 | 68 |
| 3D 장면 | 56 |
| 게임·인터랙티브 | 65 |

README에 실린 100편도 같은 갈래로 묶여 있다. 모션 그래픽 58편, 설명 영상 16편, 3D 장면 14편, 게임·인터랙티브 12편이다.

## 쓰는 법

README가 안내하는 순서는 짧다. 마음에 드는 영상을 고르고, 그 프롬프트를 복사해, 자기 에이전트에 넣어 본다. 프롬프트 복사는 무료다. 같은 프롬프트라도 결과는 실행마다 달라질 수 있으므로 Skillry의 나란히 보기로 원본과 리메이크의 차이를 먼저 확인해 두면 기대치를 잡기 쉽다.

## 출처

- yihui-dev, awesome-opus5-5-videos, GitHub. <https://github.com/yihui-dev/awesome-opus5-5-videos>
- Skillry, Opus 5.5 Videos: Awesome Prompts & Live Remakes. <https://skillry.dev/ai-videos/opus-5-5>
