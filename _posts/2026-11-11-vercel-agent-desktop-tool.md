---
title: "Vercel agent-desktop, AI 에이전트 여러 개가 PC 앱을 동시에 조작하는 도구"
date: 2026-11-11 15:05:44 +0900
categories: [AI, 코딩]
tags: [AI에이전트, agent-desktop, 자동화, ClaudeCode, Vercel]
description: "Next.js를 개발하는 Vercel이 공개한 agent-desktop은 Claude Code나 Codex 같은 AI 에이전트가 맥, 윈도우, 리눅스의 앱을 직접 조작하게 해 준다. 에이전트 여러 개가 동시에 일해도 사용자의 마우스와 화면을 빼앗지 않는다."
header:
  teaser: /assets/vercel-agent-desktop-tool-src1-thumb.jpg
permalink: /post/vercel-agent-desktop-tool/
---

AI 에이전트 세 개가 한 컴퓨터에서 동시에 메모를 쓰고, 미리 알림을 넣고, 계산기를 두드린다. Next.js를 개발하는 Vercel이 공개한 무료 도구 agent-desktop은 Claude Code나 Codex 같은 AI 에이전트가 맥, 윈도우, 리눅스의 앱을 직접 조작하게 해 준다.

<figure>
<img src="/assets/vercel-agent-desktop-tool-src1-thumb.jpg" alt="영상 클로드에 붙여 쓰는 미친 도구 agent-desktop의 썸네일">
<figcaption>영상 썸네일. (출처: 잔재미코딩(DaveLee))</figcaption>
</figure>

## computer use와의 차이

Claude Code에도 computer use 기능이 있다. 다만 한 번에 세션 하나만 쓸 수 있고, 일하는 동안 다른 앱을 숨겨서 사용자가 PC를 함께 쓰기 어렵다. agent-desktop은 에이전트 여러 개가 동시에 일한다. 진짜 마우스를 움직이지 않고 버튼과 입력칸을 곧바로 다루므로 옆에서 사용자가 다른 일을 해도 방해받지 않는다.

| 비교 항목 | Claude Code computer use | agent-desktop |
|---|---|---|
| 동시 실행 | 한 번에 세션 하나 | 에이전트 여러 개 동시 실행 |
| 작업 중 사용자 PC 사용 | 다른 앱을 숨겨 쓰기 어려움 | 방해받지 않음 |
| 붙여 쓸 수 있는 에이전트 | Claude Code | Claude Code, Codex 등 |

공식 저장소 설명에 따르면 agent-desktop은 스크린숏이나 픽셀 대조를 쓰지 않는다. 에이전트가 앱의 접근성 트리를 JSON으로 읽고, 조작할 수 있는 요소마다 붙은 참조(ref)를 지정해 동작시킨 뒤 화면을 다시 읽어 결과를 확인한다. 운영체제별로 macOS는 AX API, 윈도우는 UI Automation, 리눅스는 AT-SPI를 쓴다. 참조 기반 동작은 기본적으로 포인터를 움직이거나 포커스를 가져가지 않는다. 라이선스는 Apache-2.0이다.

## 설치와 실행

1. Claude Code에 agent-desktop의 GitHub 주소(`https://github.com/vercel-labs/agent-desktop`)를 주고 프로그램과 스킬을 같이 설치해 달라고 한다.
2. 맥에서는 처음 한 번 손쉬운 사용 권한을 허용한다.
3. 평소 말로 시킨다. 예: "agent-desktop으로 계산기 열어서 7 곱하기 6 해 줘"

직접 설치하려면 공식 저장소가 안내하는 명령을 쓴다.

```bash
npm install -g agent-desktop
agent-desktop permissions --guide
npx skills add https://github.com/vercel-labs/agent-desktop --skill agent-desktop
```

첫 줄이 CLI 설치, 둘째 줄이 권한 안내, 셋째 줄이 에이전트용 스킬 설치다. 맥과 리눅스에서는 `brew install agent-desktop`도 된다.

## 맥북에서 써 본 결과

잔재미코딩 운영자가 맥북에서 다른 앱으로 작업하며 위 계산 명령을 시켰더니, Claude가 뒤에 깔린 계산기의 버튼을 하나씩 눌러 답을 읽어 왔다. 그동안 계산기 창은 한 번도 앞으로 나오지 않았고 마우스 커서도 빼앗기지 않았다.

최소화해 둔 다른 앱 창에도 글을 써 넣었다. 에이전트 두 개를 동시에 돌렸을 때는 하나가 계산기를 누르는 사이 다른 하나가 글을 쓰며 서로 방해 없이 둘 다 해냈다.

## 출처

- 잔재미코딩(DaveLee). (2026-11-01). [클로드에 붙여 쓰는 미친 도구 | agent-desktop](https://www.youtube.com/shorts/luEhiMTWlW8). YouTube.
- Vercel Labs. [agent-desktop](https://github.com/vercel-labs/agent-desktop). GitHub.
