---
title: "AI 코딩 도구를 모션 디자인 작업실로 만드는 GitHub 프로젝트 15개"
date: 2026-11-11 15:00:00 +0900
categories: [바이브코딩]
tags: [바이브코딩, 생성형AI, 디자인, 영상제작, 오픈소스]
description: "코드로 영상을 만든다는 것은 화면의 모든 상태를 시간의 함수로 적어 두는 일이다. Claude Code 같은 AI 코딩 도구에 이 작업 방식을 얹어 주는 GitHub 프로젝트 15개를 목적별로 묶고, 필요한 것과 라이선스, 먼저 설치할 것을 정리한다."
permalink: /post/motion-design-github-projects-for-ai-coding/
---

코드로 영상을 만든다는 것은 편집기 타임라인에 키프레임을 찍는 대신 화면의 모든 상태를 시간의 함수로 적어 두는 일이다. 헤드리스 브라우저가 그 화면을 한 프레임씩 찍고 ffmpeg가 이어 붙여 MP4로 만든다. 결과물이 코드이므로 AI 코딩 도구가 직접 쓰고 고칠 수 있고, "두 번째 장면을 느리게 해줘" 같은 요청이 곧 코드 수정이 된다.

아래는 Claude Code 같은 도구에 이 작업 방식을 얹어 주는 GitHub 프로젝트 15개를 목적별로 묶은 것이다. 설명과 라이선스는 2026년 11월 11일 각 저장소의 README와 라이선스 파일 기준이다.

## 제품 출시와 소개 영상

| 이름 | 하는 일 | 필요한 것 | 라이선스 |
|------|---------|-----------|----------|
| [product-launch-motion](https://github.com/AbubakrChan/product-launch-motion) | 웹사이트 주소를 주면 음악, 효과음, 모션 블러가 들어간 60fps 출시 영상을 만든다 | Node 20 이상, Playwright, FFmpeg, Python 3와 numpy | MIT(예시 영상 제외) |
| [motion-graphics-skills](https://github.com/charlie947/motion-graphics-skills) | 출시 영상, 움직이는 차트, 설명 영상, 릴스 변환 등 스킬 15개 묶음 | MP4 내보내기에 HyperFrames 또는 ffmpeg와 Chrome | MIT |
| [claude-motion-design](https://github.com/howseen-ai/claude-motion-design) | HTML을 프레임 단위로 찍어 음악 박자에 맞춘 영상을 만든다 | Python(playwright, numpy 등), Chromium, ffmpeg | MIT |

세 저장소 모두 React 없이 HTML 한 장을 시간 함수로 움직이고 Playwright와 ffmpeg로 렌더한다. product-launch-motion은 v2에서 GSAP와 HyperFrames를 걷어내고 이 방식으로 다시 짰으며, README는 Claude Opus 5.5와 함께 쓰라고 권한다. motion-graphics-skills는 `brand-intake`를 먼저 실행해 브랜드 색과 모션 규칙 파일을 만들고 나머지 스킬이 그 파일을 읽는 구조다. 발표 자료용이라는 소개가 돌지만 README에 프레젠테이션 이야기는 없고 출시 영상과 차트, 릴스가 중심이다. claude-motion-design은 음악에서 드롭 지점을 찾아 핵심 장면에 맞추고 효과음을 피크 위치에 놓는 절차까지 담았다. 코드로 만든 영상이 어느 수준까지 나오는지는 [Claude Opus 5.5로 만든 영상 418편과 프롬프트 703개 모음](/post/claude-opus-5-5-videos/)에서 볼 수 있다.

## 이미 찍은 영상 편집

| 이름 | 하는 일 | 필요한 것 | 라이선스 |
|------|---------|-----------|----------|
| [herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) (옛 hyperframes-student-kit) | 직접 찍은 영상에서 무음과 말실수 구간을 잘라내고 자막, B-roll, 모션 그래픽을 붙인다 | Node 22 이상, Git, FFmpeg, Chrome. 전사용 ElevenLabs 키는 선택 | MIT(예시 브랜드 자산 제외) |
| [motion-graphics](https://github.com/Barty-Bart/motion-graphics) | 대본 타이밍에 맞춘 모션 B-roll, 인물과 제품의 배경 분리, 제품 설명 영상 3종, 효과음 | 스킬마다 다르다. Node 18 이상 또는 Python 3.10 이상, ffmpeg | MIT |

hyperframes-student-kit은 이름이 herk-edit-kit으로 바뀌었다. 옛 주소로 들어가도 새 저장소로 넘어간다. 스킬 15개와 모션 그래픽 카드 초안 406개가 들어 있고 HyperFrames와 GSAP 위에서 돈다. 전사는 ElevenLabs Scribe가 기본이지만 Whisper로 바꾸거나 이미 가진 대본을 넣어도 된다. motion-graphics는 스킬 여섯 개를 골라 설치하는 방식이다. 배경 분리 스킬은 내 컴퓨터에서 실행되고 처음에 사양에 맞는 모델(156~898MB)을 내려받는다. GPU 없이도 돌아가지만 README 기준 프레임당 5초쯤 걸린다.

## 짧은 애니메이션

| 이름 | 하는 일 | 필요한 것 | 라이선스 |
|------|---------|-----------|----------|
| [animate](https://github.com/cth9191/animate) | canvas 한 장에 그리는 짧은 설명 애니메이션. 기본 화풍 7종 | Node 18 이상, Playwright Chromium, ffmpeg. 내레이션은 faster-whisper | MIT |
| [claude-motion](https://github.com/whaleyxbt/claude-motion) | Remotion 위에 모션 규칙, 프레임 자기 검토, Python 효과음 엔진을 얹은 툴킷 | Node 20 이상, Python 3, ffmpeg | MIT(Remotion 라이선스는 별도) |
| [claude-remotion-skill](https://github.com/haidrrrry/claude-remotion-skill) | Remotion 영상에 모션 규칙 10개와 렌더 후 프레임 점검을 적용한다 | Remotion 프로젝트, ffmpeg | MIT |

animate는 종이 오리기, 리소 인쇄, 수학 설명, 픽셀, 아이소메트릭 같은 화풍을 고르게 하고, 이야기 구성과 화풍, 스토리보드를 차례로 승인받은 뒤에 애니메이션을 만든다. 참고 이미지를 주면 새 화풍을 맞춰 저장해 두는 기능도 있다. claude-motion과 claude-remotion-skill은 같은 문제를 겨눈다. AI는 영상을 볼 수 없으니 렌더한 프레임을 뽑아 직접 확인하고 고치게 한다. claude-motion은 여기에 샘플 음원 없이 Python으로 효과음을 합성하는 엔진과, 시뮬레이션을 웹 페이지로 짜서 60fps 영상으로 찍는 경로를 더했다.

## 웹사이트 애니메이션

| 이름 | 하는 일 | 필요한 것 | 라이선스 |
|------|---------|-----------|----------|
| [Motion](https://github.com/motiondivision/motion) | React, JavaScript, Vue용 애니메이션 라이브러리. 옛 Framer Motion이다 | `npm install motion` | MIT |
| [motion-dev-animations-skill](https://github.com/199-biotechnologies/motion-dev-animations-skill) | Motion으로 진입 효과, 스크롤, 호버, 드래그 코드를 만들게 하는 스킬 | React, Next.js, Svelte, Astro 등 Motion을 쓰는 프로젝트 | MIT |

Motion은 스킬이 아니라 라이브러리다. 다만 README가 `npx motion-ai` 한 줄로 공식 `/motion` 스킬과 문서 검색용 MCP 서버를 설치하는 방법을 안내하므로, 서드파티 스킬보다 이쪽을 먼저 써 볼 만하다. motion-dev-animations-skill은 2026년 3월 이후 갱신이 없고 배지에 Motion v11이 적혀 있어 최신 API와 어긋날 수 있다. 어떤 효과를 넣을지 이름부터 정하고 싶다면 [홈페이지 효과를 주문하는 이름과 한 줄 프롬프트 25개](/post/web-effect-names-and-one-line-prompts/)가 도움이 된다.

## 영상 제작 핵심 도구와 공식 프로젝트

| 이름 | 하는 일 | 필요한 것 | 라이선스 |
|------|---------|-----------|----------|
| [Hyperframes](https://github.com/heygen-com/hyperframes) | HTML, CSS, 미디어를 MP4로 렌더하는 프레임워크. 에이전트용 스킬 포함 | Node.js 22 이상, FFmpeg | Apache 2.0 |
| [Remotion](https://github.com/remotion-dev/remotion) | React 컴포넌트로 영상을 만드는 프레임워크 | Node.js | Remotion License |
| [Remotion Skills](https://github.com/remotion-dev/skills) | Remotion 프로젝트 생성, 마크업, 렌더, 자막, 지도 등 공식 스킬 13개 | Remotion 프로젝트 | 저장소에 라이선스 파일 없음 |
| [GSAP Skills](https://github.com/greensock/gsap-skills) | GSAP 코어, 타임라인, ScrollTrigger, 플러그인, React 사용법 스킬 8개 | GSAP을 쓰는 웹 프로젝트 | MIT |
| [LottieFiles Motion Design Skill](https://github.com/LottieFiles/motion-design-skill) | 타이밍, 이징, 연출 순서 같은 모션 원칙. 특정 라이브러리에 묶이지 않는다 | 없음 | MIT |

앞의 묶음 가운데 claude-motion과 claude-remotion-skill은 Remotion 위에서, herk-edit-kit은 HyperFrames와 GSAP 위에서 돈다. Hyperframes와 Remotion은 둘 다 헤드리스 Chrome과 FFmpeg로 렌더한다. 차이는 작성 방식이다. Remotion은 React 컴포넌트로, Hyperframes는 데이터 속성을 붙인 HTML로 영상을 적는다.

## 무엇부터 설치할까

15개를 다 설치할 필요는 없다. 목적에 맞는 한두 개로 시작한다.

1. 제품 소개 영상은 Remotion이나 Hyperframes부터 본다. React에 익숙하면 Remotion과 Remotion Skills, 그렇지 않으면 HTML만 쓰는 Hyperframes가 맞다. 라이선스가 갈린다. Remotion은 개인, 직원 3명 이하의 영리 조직, 비영리 조직, 도입을 평가하는 단계에서는 상업적 용도까지 무료이고, 그 밖의 조직은 Company License를 사야 한다. 5.0에서 조건이 조금 바뀐다는 예고도 붙어 있다. Hyperframes는 Apache 2.0이고 README에 렌더당 요금이나 상업적 사용 기준이 없다고 적혀 있다.
2. 웹 애니메이션은 Motion이나 GSAP부터 본다. React 화면의 요소 전환이면 Motion, 타임라인과 스크롤 연동이 많거나 프레임워크를 가리지 않아야 하면 GSAP Skills가 낫다. GSAP은 예전 유료 플러그인까지 전부 무료로 바뀌었다고 README가 밝힌다.
3. 움직임이 어색한데 이유를 모르겠다면 LottieFiles 스킬을 먼저 넣는다. 문서로만 이뤄져 실행 환경이 필요 없고 어떤 라이브러리와도 같이 쓸 수 있다.
4. 직접 찍은 영상을 다듬으려면 herk-edit-kit이나 motion-graphics를 본다. 앞의 것은 저장소 전체를 내려받아 그 안에서 작업하고, 뒤의 것은 필요한 스킬만 골라 넣는다.

## 설치 전에 확인할 것

스킬은 AI가 읽고 그대로 따르는 지시문이고, 대부분 셸이나 Python 스크립트가 딸려 있다. `npx skills add`를 실행하기 전에 저장소의 SKILL.md와 스크립트 폴더를 열어 무엇을 설치하고 어떤 명령을 실행하는지 읽어 본다. 첫 실행 때 Playwright와 Chromium, 수백 MB짜리 모델을 내려받는 스킬도 있다.

라이선스는 코드와 자산을 따로 본다. product-launch-motion의 예시 영상과 herk-edit-kit의 예시 브랜드 자산은 MIT 범위 밖이라고 각 저장소가 밝혀 두었다. 배경 음악과 효과음은 내려받는 곳의 조건을 따른다. Remotion 위에서 도는 스킬은 스킬 자체가 MIT여도 Remotion License가 별도로 적용된다. 학교나 회사 이름으로 영상을 낼 계획이라면 이 대목을 먼저 확인한다.

## 출처

- product-launch-motion: https://github.com/AbubakrChan/product-launch-motion
- motion-graphics-skills: https://github.com/charlie947/motion-graphics-skills
- claude-motion-design: https://github.com/howseen-ai/claude-motion-design
- herk-edit-kit(옛 hyperframes-student-kit): https://github.com/nateherkai/herk-edit-kit
- motion-graphics: https://github.com/Barty-Bart/motion-graphics
- animate: https://github.com/cth9191/animate
- claude-motion: https://github.com/whaleyxbt/claude-motion
- claude-remotion-skill: https://github.com/haidrrrry/claude-remotion-skill
- Motion: https://github.com/motiondivision/motion
- motion-dev-animations-skill: https://github.com/199-biotechnologies/motion-dev-animations-skill
- Hyperframes: https://github.com/heygen-com/hyperframes
- Remotion: https://github.com/remotion-dev/remotion
- Remotion Skills: https://github.com/remotion-dev/skills
- GSAP Skills: https://github.com/greensock/gsap-skills
- LottieFiles Motion Design Skill: https://github.com/LottieFiles/motion-design-skill
