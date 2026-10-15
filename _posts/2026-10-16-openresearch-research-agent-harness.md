---
title: "OpenResearch, 코딩 에이전트를 연구 에이전트로 바꾸는 alphaXiv의 로컬 우선 하네스"
date: 2026-10-16 00:10:09 +0900
categories: [AI, 기술]
tags: [AI, 에이전트, 연구자동화, 오픈소스, LLM, 소프트웨어개발, 생산성, 로컬우선]
header:
  teaser: /assets/openresearch-research-agent-harness-screenshot.jpg
permalink: /post/openresearch-research-agent-harness/
---
OpenResearch는 연구 에이전트를 위한 로컬 우선 하네스이자 워크스페이스다. alphaXiv가 공개한 오픈소스 프로젝트로, GitHub 저장소 설명은 "Turn your coding agents into research agents", 곧 코딩 에이전트를 연구 에이전트로 바꾼다는 것이다. Claude Code나 Codex 같은 코딩 에이전트에 논문 검색, 실험을 돌릴 컴퓨팅 환경, 실험 기록을 연결해 문헌 검토와 가설 수립, 실험 실행, 연구 산출물 작성을 맡기는 방식이다. README는 코파일럿을 찾는 사람이든 자율 연구(autoresearch) 도구를 찾는 사람이든 작업 속도를 높여 준다고 소개한다.

저장소는 MIT 라이선스이고 Rust로 작성됐다. 예전 주소 alphaXiv/openresearch-cli에서 지금의 alphaXiv/OpenResearch로 이름을 바꿨으며, 2026년 10월 16일 기준 GitHub 별은 7,200개를 넘었다.

<figure>
<img src="/assets/openresearch-research-agent-harness-screenshot.jpg" alt="OpenResearch 데스크톱 앱에서 연구 에이전트와 나눈 대화와 실험 로그가 함께 보이는 화면">
<figcaption>OpenResearch 데스크톱 앱 화면. 가운데에 연구 에이전트와 나눈 대화가, 오른쪽에 실험 로그가 보인다. 왼쪽 프로젝트 목록의 nanochat은 데모 프로젝트다.</figcaption>
</figure>

## 작동 방식

README가 설명하는 작동 방식은 코딩 에이전트, 문헌 연동, 컴퓨팅, 실험 기록의 네 갈래로 나뉜다.

| 항목 | 내용 |
|---|---|
| 코딩 에이전트 | Claude Code, Codex, OpenCode, Cursor, Google Antigravity를 기본 지원한다. OpenCode를 쓰면 LM Studio, oMLX, Ollama 또는 사용자 지정 엔드포인트를 거쳐 로컬 모델도 쓸 수 있다. |
| 문헌 연동 | alphaXiv, bioRxiv, PubMed와 연동된다. 에이전트는 관련 논문을 찾아 근거 있는 가설을 세우고, 자신이 돌리는 실험을 기존 연구와 연결한다. |
| 컴퓨팅 | 실험을 로컬에서 돌리거나 SSH, Slurm, Kubernetes, Modal, Tinker, Ray, Hugging Face Jobs, OpenResearch 관리형 컴퓨팅 가운데서 고른다. |
| 실험 기록 | 모든 실험을 로컬 SQL 데이터베이스에 기록하고 로그, 코드, 산출물을 사용자 컴퓨터에 보관한다. 에이전트는 이 기록을 보고 과거 결과에서 배워 다음에 무엇을 시도할지 정한다. 데스크톱 앱에서는 에이전트가 한 일과 각 결과의 근거를 살펴볼 수 있다. |

## 연구 데이터는 사용자 컴퓨터에

README는 연구를 직접 보관하고 소유하라고 강조한다. 모든 작업을 로컬에서 실행할 수 있고, 개발진은 사용자의 코드나 에이전트 실행 기록(agent traces)을 수집하지 않는다고 밝힌다. 프로젝트, 대화, 실험, 로그, 산출물은 사용자 컴퓨터에 남고 사용자가 관리한다.

다만 공식 릴리스 빌드는 기본 설정에서 두 종류의 데이터를 백그라운드로 보낸다. 하나는 개략적인 제품 사용 분석 이벤트이고, 다른 하나는 에이전트가 작성하는 상세 피드백이다. 둘 다 임의로 만든 설치 ID에 연결되며, 사용자가 꺼야 전송이 멈춘다. README에 따르면 이 데이터에는 코드, 프롬프트, 파일 내용이나 경로, 저장소 이름, 토큰, 이메일, 프로젝트·실험 식별자가 들어가지 않는다.

에이전트 피드백은 버그 신고, 기능 요청, OpenResearch에 대한 전반적인 불만을 담아 보내는 보고서다. 에이전트는 연구나 코드에 관한 민감한 정보를 빼고 보고서를 쓰도록 지시받는다.

사용 분석과 에이전트 피드백은 데스크톱 앱의 Settings에서, 또는 터미널에서 `orx telemetry off`를 실행해 둘 다 끌 수 있다.

## 설치와 요구 사항

개발진은 데스크톱 앱을 권장한다. 플랫폼별 설치 파일과 요구 사항은 다음과 같다.

| 플랫폼 | 설치 파일 | 요구 사항 |
|---|---|---|
| macOS | OpenResearch.dmg | macOS 11 이상 |
| Windows (베타) | OpenResearch-Setup.exe | Git for Windows |
| Linux | AppImage (x86_64, ARM64) | glibc 2.35 이상 |

Windows 안내 문서에 따르면 Git for Windows는 git 때문에만 필요한 것이 아니다. orx가 실험을 실행할 때 쓰는 `bash`와 coreutils를 여기서만 얻을 수 있어서 반드시 설치해야 한다.

독립 실행형 CLI는 macOS와 Linux에서 다음 명령으로 설치한다.

```sh
curl -LsSf https://openresearch.sh/install.sh | sh
orx up
```

`orx up`을 실행하면 `http://127.0.0.1:4791`에서 로컬 대시보드가 열린다. 기기 관리 정책이 걸린 Mac에서는 `install.sh`로 설치한 CLI가 아직 서명되지 않아 차단될 수 있다. 이때는 서명과 공증을 거친 데스크톱 앱을 쓰면 된다. 앱의 Settings → Updates → Install the `orx` command 메뉴에서 터미널용 `orx` 명령을 설치할 수도 있다.

openresearch.sh에서 계정을 만들면 이메일로 소식을 받고 OpenResearch 관리형 컴퓨팅을 쓸 수 있다.

## 출처

- alphaXiv, OpenResearch GitHub 저장소 README. https://github.com/alphaXiv/OpenResearch
- OpenResearch 문서. https://openresearch.sh/docs
- OpenResearch Windows 안내(docs/windows.md). https://github.com/alphaXiv/OpenResearch/blob/main/docs/windows.md
