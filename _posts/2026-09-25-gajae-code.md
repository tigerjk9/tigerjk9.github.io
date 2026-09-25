---
title: 이미 쓰는 구독으로 돌리는 코딩 에이전트, gajae-code 정리
date: 2026-09-25 19:19:00 +0900
categories: [AI, 코딩]
tags: [AI, 코딩, 에이전트, LLM, 오픈소스]
description: 별도 API 과금 없이 이미 결제 중인 코딩 플랜으로 돌아가고, 변경 전에 계획하고, 휴대폰으로 답하는 오픈소스 코딩 에이전트 하네스 gajae-code(gjc)의 핵심을 치트시트를 바탕으로 정리했다.
permalink: /post/gajae-code/
---
gajae-code(명령어 `gjc`)는 외부 코딩 에이전트 하네스다. 아무 저장소나 워크트리에 넣고 돌리는 도구로, MIT 라이선스로 공개돼 있다. 표어는 "의도를 인코딩하고, 소프트웨어를 디코딩한다"이며, 세 가지를 내세운다. 이미 결제 중인 코딩 플랜으로 돌아가고, 파일 하나 바뀌기 전에 계획하고, 에이전트의 질문에는 터미널이든 휴대폰이든 어디서든 답한다. 이 글은 저장소에 포함된 치트시트를 바탕으로 gjc의 골자를 정리한 것이다. 베타 단계 프로젝트이므로 중요한 작업에는 출력을 검증한 뒤 쓰는 편이 좋다.

## 무엇을 푸는 도구인가

만든 쪽은 대부분의 코딩 에이전트가 세 군데서 무너진다고 본다. 요금을 두 번 물리고, 이해하기 전에 코드를 고치고, 키보드에서 벗어나는 순간 침묵한다는 것이다. gjc의 해법은 다음과 같다.

| 문제 | 어떻게 되나 | gjc의 해법 |
| :--- | :--- | :--- |
| 별도 API 과금 | 플랜 요금에 더해 토큰당 API 비용까지 낸다 | 이미 결제 중인 코딩 플랜으로 로그인해 그대로 쓴다 |
| 코드부터 고치는 에이전트 | 이해 전에 수정해 재작업이 생긴다 | 인터뷰 → 계획 → 비평 → 그 다음에 변경하는 계획 게이트 워크플로 |
| 터미널 종속 세션 | 자리를 비우면 질문이 와도 멈춘다 | 질문을 텔레그램·Discord·Slack으로 보내 어디서든 답한다 |
| 컨텍스트 폭발 | 전체 파일 읽기와 로그 홍수가 컨텍스트를 태운다 | 구조 요약, artifact 스필, 캐시 인지 라우팅, 컴팩션 |

## 설치와 첫 실행

Linux·macOS·Windows용 프리빌드 바이너리를 제공하며 Bun은 필요 없다. 설치 스크립트를 내려받아 실행한 뒤 `gjc`로 진입한다.

```sh
curl -fsSL <repo>/scripts/install.sh -o gjc-install.sh
sh gjc-install.sh
gjc
```

첫 실행은 플랜을 고르고 바로 시작하는 흐름이다.

```text
/login                     프로바이더·코딩 플랜 선택
/skill:deep-interview      모호한 요구사항을 구체화
/skill:ralplan             계획 수립과 비평
gjc ultragoal create-goals 승인된 계획으로 목표 생성
```

실행 모드는 상황에 맞게 고른다.

```sh
gjc                            # 현재 체크아웃에서 실행
gjc --tmux                     # tmux 기반 리더 세션
gjc --tmux --worktree my-task  # 위험한 작업을 격리 워크트리에서
gjc @shot.png "뭘 바꿔야 할까?"    # 이미지 입력
gjc -p "..."                   # 한 번의 프롬프트로 실행
```

패키지 매니저로 설치하면 `가재씨`라는 한국어 별칭도 함께 붙는다.

## 쓰던 코딩 플랜 그대로

한 번 로그인하면 이미 구독 중인 플랜으로 gjc가 돌아간다. 세션 안에서 `/login`을 실행해 플랜을 고른다.

| 플랜·구독 | OAuth 로그인 |
| :--- | :--- |
| Claude Pro / Max | `anthropic` |
| ChatGPT Plus / Pro (Codex) | `openai-codex` |
| Cursor | `cursor` |
| GitHub Copilot | `github-copilot` |
| OpenCode Zen / Go | `opencode-zen` |
| Kimi / Moonshot | `kimi-code` |
| Z.AI GLM | `zai` |
| MiniMax | `minimax-code` |
| xAI Grok | `xai` |
| Qwen Portal | `qwen-portal` |

키 기반 플랜은 프리셋 명령 하나로 온보딩된다. 프리셋이 API 타입·base URL·환경 변수·라이브 모델 카탈로그를 한 번에 기록하므로, 새 모델이 gjc 업데이트 없이 바로 잡힌다.

```sh
gjc setup provider --preset commandcode-goat
gjc setup provider --preset cline-pass
```

이 밖에 API 키 프로바이더, 로컬 런타임(Ollama·LM Studio·vLLM), 게이트웨이까지 50개가 넘는 프로바이더를 지원한다. 계정 관리는 `gjc accounts list`·`gjc accounts check <p>` 등으로 하고, 모델은 `provider/model:effort` 형식으로 지정한다. effort는 off·minimal·low·medium·high·xhigh·max 중에서 고른다.

## 변경 전에 계획

워크플로 표면은 의도적으로 좁다. 스킬 4개와 역할 에이전트 4개가 전부다.

```text
deep-interview -> ralplan -> ultragoal
              └ 필요할 때 autoresearch가 계획을 뒷받침
```

| 표면 | 역할 |
| :--- | :--- |
| `deep-interview` | 모호한 요청을 구체적인 요구사항으로 바꾼다 |
| `ralplan` | 코드 변경 전에 구현 계획을 세우고 비평한다 |
| `ultragoal` | 실행·수정·검증·증거까지 목표를 추적한다 |
| `autoresearch` | 목표 지향 리서치를 수행하고 구조화된 판정으로 마무리한다 |
| `executor` · `architect` · `planner` · `critic` | 구현과 읽기 전용 리뷰를 위한 번들 역할 에이전트 |

가벼운 분류가 필요하면 `gjc quick-lane classify "..."`로 빠르게 처리한다. 세션은 `gjc -c`(이어가기), `gjc -r [id|path]`(재개), `gjc --fork <id>`(분기), `gjc --export=<f>`(내보내기)로 다룬다.

## 휴대폰으로 답하기

에이전트가 결정을 요청하면 알림이 오고, 자리에 없어도 답할 수 있다. 설정은 실행 중인 세션의 `/settings`에서 하거나 헤드리스로 `gjc notify setup|status|health|test`를 쓴다. `gjc daemon`이 봇 토큰당 하나의 안전한 연결 소유자를 유지해 새 세션이 충돌 없이 붙는다. 텔레그램·Discord·Slack을 지원하며, 범용 `action_needed`/`reply` 프로토콜을 써서 어떤 봇이나 모바일 앱이든 터미널을 긁지 않고 답을 되돌린다.

## 토큰을 덜 쓰기

비용의 양쪽을 모두 줄인다. 캐시는 프로바이더별 `cacheRetention`으로 제어하며, Anthropic은 짧은 캐시가 긴 에이전트 실행에 취약하므로 기본이 장기(1시간) 유지다. 컨텍스트 쪽에서는 파일 읽기가 전체 파일 대신 구조 요약을 돌려주고, 과대한 셸 출력은 컨텍스트를 채우는 대신 회수 가능한 `artifact://` 참조로 대체된다. 컴팩션과 브랜치 요약이 긴 세션을 윈도 안에 유지한다. 사용량은 `gjc stats`로 확인한다.

## 파일 주소 지정과 도구

도구는 read·search·find·edit·write·bash·task로 이루어진다. 파일을 읽을 때 주소 지정 문법이 세밀하다.

| 표기 | 의미 |
| :--- | :--- |
| `file.ts:50-200` | 50~200번째 줄 |
| `file.ts:50+150` | 50번째 줄부터 150줄 |
| `file.ts:5-16,60-73` | 여러 구간을 한 번에 |
| `file.ts:raw` | 요약 없이 원본 |
| `file.ts:conflicts` | 병합 충돌 구간 |
| `a.zip:in/f.ts:1-20` | 압축 파일 내부 |
| `db.sqlite:users:42` | DB 테이블의 특정 행 |
| `db.sqlite?q=SELECT..` | 쿼리 결과 |

키바인딩도 정리돼 있다. 예를 들어 `ctrl+p`(명령), `ctrl+l`(정리), `shift+tab`(모드 전환), `ctrl+r`(재개), `escape`(중단) 등이다.

## 스킬·확장·유지보수

스킬은 Claude Code·Codex의 `SKILL.md` 규약을 따르되 gjc 정식 경로에서만 로드한다. 프로젝트별은 `.gjc/skills`, 사용자 전역은 `~/.gjc/agent/skills`에 둔다. `gjc skills discover`가 정확한 복사 명령을 알려 준다. MCP 서버는 `gjc mcp list`, 플러그인은 `gjc plugin install|list`로 다룬다.

설정은 `~/.gjc/agent/config.yml`(역할·오버라이드·UI), `~/.gjc/agent/models.yml`(프로바이더·프로필), `~/.gjc/config.yml`(재시도)로 나뉜다. 재시도 예산은 아래처럼 잡는다.

```yaml
retry:
  requestMaxRetries: 4
  streamMaxRetries: 100
  maxRetries: 3
  maxDelayMs: 300000
```

`requestMaxRetries`는 스트림 수립 전에, `streamMaxRetries`는 재생 안전한 일시적 스트림 실패에만 적용된다. 유지보수는 `gjc update`(원자적 교체), `gjc gc`(정리), `gjc customize doctor`(도구·스킬·훅·MCP 진단)로 한다. 진단 도구는 자격증명이나 토큰을 절대 출력하지 않는다.

기본 테마는 다크가 red-claw, 밝은 터미널이 blue-crab이며, Claude Code·Codex·OpenCode 외관을 따라가는 마이그레이션 테마도 번들돼 있다.

## 출처

- gajae-code (github.com/Yeachan-Heo/gajae-code, MIT 라이선스). 본문은 저장소의 `docs/cheatsheet` 치트시트와 한국어 README를 바탕으로 정리했다. 공식 사이트: gajae-code.com
