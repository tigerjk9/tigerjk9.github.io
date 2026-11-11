---
title: "먼저 말을 거는 AI 에이전트, Claude Duet과 Muse와 dots 비교"
date: 2026-11-11 13:35:18 +0900
categories: [AI]
tags: [AI에이전트, ClaudeDuet, Anthropic, Meta, OpenAI, 생성형AI, 생산성]
permalink: /post/proactive-ai-agents-claude-duet-muse-dots/
description: "챗봇은 사람이 물어야 답한다. 2026년 가을에 나온 Meta Muse, OpenAI dots, Anthropic Claude Duet은 연결해 둔 메일과 일정을 스스로 살피다가 챙길 일이 생기면 먼저 알린다. 세 제품의 대상과 승인 구조, 쓰기 전에 정할 기준을 정리한다."
---

챗봇은 사람이 물어야 답한다. 2026년 가을에 나온 세 제품은 이 순서를 뒤집었다. Meta의 Muse(9월 8일), OpenAI의 dots(9월 29일), Anthropic의 Claude Duet(10월 21일)은 사용자가 연결해 둔 메일과 일정, 업무 앱을 스스로 살피다가 챙길 일이 생기면 먼저 알린다. 창을 닫아도 일은 계속된다.

세 제품의 뼈대는 같다. 에이전트마다 브라우저가 달린 클라우드 컴퓨터를 한 대씩 받고, 거기서 사용자가 허락한 앱에 접속해 일한다. 그래서 내 노트북이나 휴대전화가 꺼져 있어도 작업이 이어진다. 메일 발송이나 결제처럼 되돌리기 어려운 행동 앞에서는 멈추고 사람의 승인을 기다린다. 차이는 누구를 겨냥하는지, 어디서 만나는지, 승인 규칙을 누가 정하는지에 있다.

## Claude Duet, 일하는 사람의 아침 브리핑

Anthropic은 Duet을 챙길 일이 감당할 수 없을 만큼 많은 전문직과 소상공인을 위한 제품이라고 소개한다. 매일 아침 연결된 앱에서 중요한 일을 추려 짧은 브리핑을 보내고, 몇 시간마다 계정을 확인해 사람이 봐야 할 일이 있을 때만 메시지를 보낸다. 대화는 글이나 음성으로 하고, 주고받은 내용은 하나의 스레드에 계속 쌓인다.

기반 모델은 Claude Opus 5.5다. Claude 계정에 이미 있는 메모리와 스킬, 연결 앱을 그대로 가져오므로 따로 설정할 것이 적다. 공식 글이 이름을 든 앱은 Gmail, Slack, QuickBooks, Stripe, Gusto, LinkedIn, Docusign, HubSpot, Canva, Shopify이고, Claude 마켓플레이스의 커넥터와 플러그인 6,000여 개를 쓸 수 있다고 한다. 예시로 든 일은 놓친 메시지를 찾아 답장 초안 쓰기, 미수금 독촉, 급여 준비, 회의 일정 잡기, 매출 예측과 대시보드 만들기다.

승인 구조는 세 단계로 읽힌다. 메시지 발송, 결제, 문서 서명, 삭제는 무엇을 할지 먼저 보여 준 뒤 승인을 받는다. 증권 거래와 계좌 간 송금은 승인을 해도 하지 않는다. 비밀번호와 로그인 토큰은 Duet이 직접 보지 못하게 설계했고, 별도 분류기가 메시지마다 민감 정보가 새지 않는지 검사한다.

지금은 연구 미리보기 단계다. 미국의 Pro, Max, Ultra 구독자가 대기 명단에 등록해 순서대로 받는다. claude.ai와 iOS, Android 전용 앱으로 쓰며 기존 Claude 앱과는 별개다. 추가 요금은 없지만 요금제 사용 한도를 함께 쓰고, Duet이 뒤에서 계정을 확인하는 작업도 한도에서 차감된다. Anthropic이 직접 밝힌 약점도 있다. 스레드를 잘못 읽거나 급한 정도를 잘못 판단할 수 있고, 티켓 예매 같은 개인 용무는 업무보다 서툴며, 작업 중인 브라우저 화면을 아직 보여 주지 못한다.

## Meta Muse, 일상과 장기 목표

Muse는 범위가 생활 쪽이다. Meta는 메일 보내기와 여행 예약, 양식 작성, 가격 흥정을 예로 들고, 장기 목표를 실행 계획으로 바꿔 준다고 설명한다. 인스타그램에 저장한 요리 영상을 장보기 목록으로 바꾸거나, 초대장을 보내기 전에 친구들의 식이 제한을 기억해 내는 식이다.

만나는 곳은 Muse 앱(iOS, Android), muse.ai, 그리고 WhatsApp이다. 사람에게 메시지를 보내듯 말을 걸면 된다. 미국에서 먼저 출시됐고, Meta 뉴스룸에는 10월 27일자로 싱가포르 출시 공지가 올라와 있다. 기본 기능은 무료이고 더 많이 쓰려는 사람을 위한 구독 요금제가 따로 있다.

실행 환경은 Muse Secure VM이라는 전용 클라우드 컴퓨터다. 연결할 앱과 권한 수준은 사용자가 정한다. 메일이라면 읽기만 허용할 수도 있고 대신 보내기까지 맡길 수도 있다. 메일 발송과 구매 같은 민감한 행동은 승인을 받는다. 여기에 Sentinel이라는 별도 에이전트가 같은 컴퓨터에서 Muse와 분리된 채 돌아가며, Muse가 인터넷으로 내보내는 행동을 먼저 검사하고 필요하면 사용자에게 허락을 구한다. 결제는 Stripe의 Link로 하고 일회용 카드 번호를 써서 실제 카드 정보를 가린다. Muse가 한 일과 하려는 일은 감사 기록으로 남는다. Meta는 대화와 VM 안의 데이터를 광고 시스템과 공유하지 않으며, 모델 학습에 쓰이는 것도 사용자가 거부할 수 있다고 밝혔다.

## OpenAI dots, 개인에서 팀과 회사로

dots는 OpenAI가 DevDay 2026에서 공개했다. 채팅 창을 닫아도 프로젝트를 지켜보고 소프트웨어를 다루다가, 끝낸 일을 승인받으러 돌아오는 상시 에이전트다. 기반 모델은 GPT-6 Astra이고, OpenAI 플러그인 생태계로 4,000개가 넘는 앱에 연결된다. ChatGPT 데스크톱 앱이나 웹에서 만들고, 그 뒤로는 ChatGPT 모바일 앱과 Slack, Microsoft Teams에서 부를 수 있다.

눈여겨볼 장치는 능동 조사(proactive research)다. 사용자가 일을 시키지 않는 동안 dot은 연결된 앱을 살펴 챙길 만한 일을 표시하는데, 이때 쓰는 도구는 읽기 전용이다. 메시지를 보내거나 내용을 고치거나 사용자의 컴퓨터를 조작하지 못한다. 실제 행동의 허용 범위는 사용자 지정 규칙(Custom Rules)으로 정한다. 어떤 행동은 알아서 하게 두고, 어떤 행동은 승인을 요구하고, 어떤 행동은 금지할 수 있다. 자동 검토 시스템이 중대한 행동을 사용자 지시와 규칙에 비추어 그대로 진행할지 승인을 받을지 가른다. 비밀번호 변경 같은 민감한 조작은 사람 몫으로 남는다. 작업 중인 클라우드 컴퓨터 화면은 사용자가 언제든 볼 수 있다.

다른 두 제품과 갈리는 지점은 조직이다. 첫 번째 dot은 Pro와 Business Premium 요금제에 포함되고, Enterprise, Edu, Healthcare 고객은 관리자가 켜면 베타를 쓸 수 있다. 조달이나 청구서 처리처럼 회사 안의 역할과 자격 증명을 따로 받는 전문 dot은 일부 기업과 시범 운영 중이다. 추가 dot의 가격과 집중 작업 허용량은 보도 시점에 공개되지 않았다.

## 한눈에 비교

| 항목 | Claude Duet | Meta Muse | OpenAI dots |
|------|-------------|-----------|-------------|
| 주 대상 | 전문직, 소상공인 | 일반 개인 | 개인부터 팀, 회사 |
| 만나는 곳 | 전용 앱(iOS, Android), claude.ai | Muse 앱, muse.ai, WhatsApp | ChatGPT, Slack, Teams |
| 주로 하는 일 | 아침 브리핑, 업무 준비와 처리 | 일상 용무, 장기 목표 계획과 실행 | 업무 맥락을 이어 가는 상시 작업 |
| 승인 구조 | 발송, 결제, 서명, 삭제 전 승인. 증권 거래와 송금은 금지 | 민감 행동 전 승인. Sentinel이 외부 행동 검사 | 사용자 지정 규칙과 자동 검토. 능동 조사는 읽기 전용 |
| 출시 상태 | 10월 21일 연구 미리보기. 미국 Pro, Max, Ultra 대기 명단 | 9월 8일 미국 출시. 기본 무료, 구독제 별도 | 9월 29일 공개. Pro, Business Premium에 1개 포함 |

Duet은 대기 명단이 미국 구독자부터 열렸고, Muse는 미국에서 시작했다. dots의 제공 국가는 발표 보도에 나오지 않는다. 한국에서 바로 쓸 수 있다고 볼 근거는 아직 없다.

## 쓰기 전에 정할 세 가지

### 무엇을 맡길까

세 제품 모두 잘하는 일은 반복되고, 결과를 사람이 금방 확인할 수 있는 일이다. 놓친 메일 찾기, 일정 충돌 알림, 답장 초안, 청구서 누락 확인이 그렇다. 반대로 맥락을 한 번 잘못 읽으면 관계나 돈이 걸리는 일은 초안까지만 맡기는 편이 안전하다. Anthropic이 스스로 적은 약점이 스레드 오독과 긴급도 오판이라는 점을 기억해 둘 만하다. 교사라면 학부모 메시지 가운데 답이 필요한 것을 추려 초안을 받아 보는 일은 맡길 수 있어도, 학생 평가나 상담 내용이 담긴 답장을 그대로 보내게 둘 일은 아니다. 비용도 따져야 한다. Duet은 뒤에서 계정을 확인하는 작업까지 요금제 한도를 쓴다.

### 어디까지 연결할까

연결한 앱이 곧 에이전트가 읽는 범위다. 처음에는 메일과 일정처럼 브리핑에 꼭 필요한 계정만 연결하고, 읽기 권한에서 시작해 쓰기 권한을 하나씩 여는 순서가 맞다. Muse는 메일을 읽기 전용으로 둘 수 있고, dots의 능동 조사는 처음부터 읽기 전용이며, Duet은 연결한 앱을 언제든 끊을 수 있다. 결제 수단과 회계, 급여 계정은 가장 나중에 연결한다. 직장 계정이라면 개인이 판단할 일이 아니다. dots도 Enterprise와 Edu 요금제에서는 관리자가 켜야 쓸 수 있다. 학생 정보가 든 학교 계정을 개인 판단으로 연결해서는 안 된다.

### 언제 승인할까

기본값은 제품이 정해 두었지만 그 선이 내 일에 맞는지는 따로 봐야 한다. 밖으로 나가는 것(메일, 메시지, 게시), 돈이 움직이는 것, 지우는 것, 서명하는 것은 매번 승인으로 둔다. 일정 초안 만들기나 문서 정리처럼 되돌릴 수 있는 일은 풀어 줘도 된다. 승인 요청이 지나치게 잦으면 내용을 읽지 않고 누르게 되고, 그때부터 승인 단계는 형식만 남는다. 그래서 승인 항목은 적게, 대신 하나하나는 내용을 확인할 수 있게 두어야 한다. Muse의 감사 기록이나 dots의 활동 보기처럼 에이전트가 한 일을 나중에 훑을 수 있는 화면도 주기적으로 열어 본다.

Anthropic은 Duet이 스레드를 잘못 읽을 수 있다고 적었고, OpenAI는 중대한 작업을 사람이 검토하라고 권한다. Duet은 아직 연구 미리보기다. 에이전트가 먼저 움직이게 하더라도 어디서 멈출지는 쓰는 사람이 미리 정해 두어야 한다.

## 출처

- Anthropic. (2026-10-21). Claude Duet 연구 미리보기 소개 글. https://claude.com/resources/articles/claude-duet
- Meta Newsroom. (2026-09-08). Introducing Muse: The World's First Personal AI Agent Built for Everyone. https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- Franzen, C. (2026-09-29). OpenAI launches Dots, always-on AI agent coworkers. VentureBeat. https://venturebeat.com/ai/openai-launches-dots-always-on-ai-agent-coworkers-and-chatgpt-space-where-they-can-collaborate-with-human-teams
- 9to5Google. (2026-09-29). OpenAI dots 발표 보도. https://9to5google.com/2026/09/29/openai-dots-agent/
- Clover, J. (2026-10-21). Anthropic Launches Claude Duet, a Proactive AI Agent. MacRumors. https://www.macrumors.com/2026/10/21/anthropic-claude-duet/
- SiliconANGLE. (2026-10-22). Anthropic introduces Claude Duet, a proactive AI agent for professionals. https://siliconangle.com/2026/10/22/anthropic-introduces-claude-duet-a-proactive-ai-agent-for-professionals/
- 경유: 근쌤의 AI 브리프(2026-10-23)
