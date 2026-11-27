---
title: "몸이 없는 AI도 의미를 이해할 수 있을까?"
date: 2026-11-27 21:04:00 +0900
categories: [AI, 인지과학]
tags: [몸이아는것AI가아는것, 기호접지문제, 중국어방, 대규모언어모델, 이해, 개념표상, 체화된인지]
series: "몸이 아는 것, AI가 아는 것"
header:
  teaser: /assets/body-and-ai-05.jpg
permalink: /post/body-and-ai-05-symbol-grounding/
description: "글자만 읽고 배운 AI는 '사과'의 의미를 아는 걸까? 중국어 방, 기호 접지 문제, 문어 테스트 같은 고전적 반론과 이에 대한 재반론, 그리고 LLM과 사람의 개념을 직접 비교한 최신 연구를 정리한다."
---

<div class="notice--info" style="font-size:.85em" markdown="1">
**몸이 아는 것, AI가 아는 것 시리즈** · [1 자동화와 체화](/post/body-and-ai-01-automatic-vs-embodied/) · [2 손글씨와 타이핑](/post/body-and-ai-02-handwriting-vs-typing/) · [3 도구와 오프로딩](/post/body-and-ai-03-tools-and-offloading/) · [4 추상 개념](/post/body-and-ai-04-abstract-concepts/) · **5 기호 접지** · [6 AI 내부 들여다보기](/post/body-and-ai-06-inside-the-model/) · [7 AI와 정의](/post/body-and-ai-07-teaching-justice/)
</div>

대규모 언어모델(LLM)은 사과를 한 번도 본 적도, 먹어 본 적도 없다. 그런데도 사과에 대해 사람보다 그럴듯한 글을 쓴다. 이것은 사과의 의미를 이해한 것일까, 아니면 의미 없이 기호를 능숙하게 다루는 것일까? 4편에서 본 것처럼 사람의 개념이 몸과 언어라는 두 길로 만들어진다면, 언어의 길만 가진 AI는 어디까지 갈 수 있을까?

<figure>
  <img src="/assets/body-and-ai-05.jpg" alt="몸이 아는 것, AI가 아는 것 시리즈 5편 표지">
  <figcaption>시리즈 5편. 기호 접지 문제와 AI의 이해</figcaption>
</figure>

## 고전적 반론 1. 중국어 방

*Searle, J. R. (1980). Minds, brains, and programs. Behavioral and Brain Sciences, 3(3), 417-424.*

중국어를 전혀 모르는 사람이 방 안에 있다. 문틈으로 중국어 질문이 들어오면, 그는 두꺼운 규칙서를 보고 정해진 기호를 골라 내보낸다. 밖에서 보면 방은 중국어를 완벽하게 이해하는 것처럼 보인다. 하지만 방 안의 사람은 단 한 글자도 이해하지 못한다.

Searle의 주장은 이렇다. 겉으로 드러나는 행동이 완벽해도, 기호를 형식적 규칙에 따라 다루는 것만으로는 이해가 생기지 않는다.

## 고전적 반론 2. 기호 접지 문제

*Harnad, S. (1990). The symbol grounding problem. Physica D, 42(1-3), 335-346.*

Harnad는 이 문제를 더 날카롭게 만들었다. 중국어를 모르는 사람에게 중국어 사전 한 권만 주고 중국어를 배우라고 하면 어떻게 될까? 한 단어를 찾으면 다른 중국어 단어들로 설명되어 있고, 그 단어를 찾으면 또 다른 중국어 단어가 나온다. 기호에서 기호로 끝없이 돌 뿐, 어디에서도 실제 세계에 닿지 않는다.

기호가 의미를 가지려면 어딘가에서는 감각과 경험에 '접지'되어야 한다는 것이 기호 접지 문제다.

## 고전적 반론 3. 문어 테스트

*Bender, E. M., & Koller, A. (2020). Climbing towards NLU: On meaning, form, and understanding in the age of data. ACL 2020, 5185-5198.*

두 사람이 각자 무인도에 갇혀 해저 케이블로 전보를 주고받는다. 아주 영리한 문어가 케이블을 엿들으며 대화의 패턴을 익히고, 어느 날 케이블을 끊고 한 사람인 척 답장을 보낸다. 일상 대화는 그럴듯하게 이어진다.

그런데 한 사람이 코코넛과 밧줄로 투석기를 만드는 법을 보내자, 문어는 코코넛과 밧줄이 무엇인지 모르니 "멋진 생각이야!" 같은 말만 돌려준다. 그리고 곰에게 쫓기는 긴급 상황이 오자 문어는 쓸모 있는 도움을 줄 수 없다.

Bender와 Koller는 언어의 **형식**만으로 학습한 시스템은 원리적으로 **의미**를 배울 수 없다고 주장한다. 언어는 실제 세계에 대해 소통하기 위한 것인데, 형식만으로는 말과 세계를 잇는 관계를 배울 신호가 없다는 것이다.

## 재반론. 의미는 관계 속에도 있다

*Piantadosi, S. T., & Hill, F. (2022). Meaning without reference in large language models. arXiv:2208.02957.*

반대쪽의 대표적인 주장이다. 의미가 반드시 바깥 대상을 가리키는 것(지시)에서만 오는 것은 아니라는 것이다. 인지과학에는 개념의 의미가 다른 개념들과의 관계, 곧 **개념적 역할**에서 나온다는 이론이 있다. '홀수'는 '짝수', '나누기', '2'와의 관계망 속에서 의미를 가진다.

저자들은 LLM이 이런 개념적 역할을 어느 정도 포착하고 있을 가능성이 크다고 본다. 그리고 의미가 있는지는 모델의 구조나 학습 데이터만 보고 판단할 수 없고, 모델 내부 상태들이 서로 어떻게 관련되는지를 직접 들여다봐야 알 수 있다고 주장한다. 이 주장은 6편의 해석 가능성 연구로 이어진다.

## 중간 입장. 선험적으로 판단하지 말고 실험하라

*Pavlick, E. (2023). Symbols and grounding in large language models. Philosophical Transactions of the Royal Society A, 381(2251), 20220041.*

Pavlick은 양쪽 비판 모두 선험적으로 받아들일 수 없고 경험적으로 검증해야 한다고 말한다. 모델이 어떤 과제를 잘하거나 못하는 겉모습보다, 그 밑에 깔린 역량이 무엇인지를 밝히는 것이 우선이라는 것이다.

*Mitchell, M., & Krakauer, D. C. (2023). The debate over understanding in AI's large language models. PNAS, 120(13), e2215907120.*

이 논쟁이 얼마나 팽팽한지 보여 주는 숫자가 있다. 이 논문이 소개한 자연어처리 연구자 대상 설문에서, 텍스트만으로 학습한 모델이 언어를 어떤 의미에서 이해할 수 있다는 진술에 480명 중 51%가 동의하고 49%가 반대했다. 저자들은 인간과 다른 방식의 이해가 있을 수 있으며, 그 강점과 한계를 밝히는 확장된 지능 과학이 필요하다고 제안한다.

## 실험 1. AI는 몸과 관련된 개념에서 사람과 멀어진다

*Xu, Q., Peng, Y., Nastase, S. A., Chodorow, M., Wu, M., & Li, P. (2025). Nature Human Behaviour, 9(9), 1871-1886.*

이 논쟁을 실제 데이터로 시험한 연구다. 연구진은 약 4,442개 단어에 대해 사람들이 여러 차원으로 평정한 자료(글래스고 규준과 랭커스터 규준)와 최신 LLM의 평정을 비교했다. 차원은 세 영역으로 나뉜다.

- **비감각운동 영역** 예: '꽃'이 얼마나 감정을 불러일으키는가
- **감각 영역** 예: '꽃'을 냄새로 얼마나 경험하는가
- **운동 영역** 예: '꽃'을 손이나 팔로 얼마나 경험하는가

결과는 선명했다. 사람과 모델의 표상이 닮은 정도는 비감각운동 영역에서 감각 영역으로 갈수록 낮아졌고, 운동 영역에서 가장 낮았다. 그리고 이미지까지 함께 학습한 모델은 시각과 관련된 차원에서 사람과 더 닮아 있었다.

**쉽게 말하면** 언어만으로도 개념의 상당 부분, 특히 감정이나 추상적 속성은 사람과 비슷하게 복원된다. 하지만 몸으로 겪어야 하는 부분, 특히 움직임과 관련된 부분은 잘 복원되지 않는다. 그리고 감각을 하나 더해 주면 그 감각에 해당하는 부분이 좋아진다. 몸이 의미의 전부는 아니지만 의미의 일부라는 것을 보여 주는 결과다.

## 실험 2. AI의 감정 개념은 너무 칸이 잘 나뉘어 있다

*Bhattacharyya, S., et al. (2025). Too categorical to be human: Emotion concepts in LLMs and humans. arXiv:2508.05880.*

4편에서 개념을 잉크에 비유했다. 진한 중심과 흐린 가장자리가 있고, 가장자리는 사람마다 다르게 번진다. 이 연구는 AI의 잉크가 어떻게 번지는지를 본 셈이다.

연구진은 15가지 감정 범주에 걸친 감정 상황 시나리오를 만들고, 사람과 LLM에게 각 상황을 얼마나 즐거운지, 얼마나 노력이 드는지 같은 평가 차원으로 판단하게 했다. 그 결과 LLM은 사람보다 감정 개념을 **더 범주적이고, 균질하고, 확정적으로** 표상했다. 한 감정 안의 다양성은 더 작았고, 서로 다른 감정 사이의 거리는 더 멀었다. 과제 형식을 바꾸거나 다양한 인구집단의 페르소나를 입혀도 이 구조는 유지되었고, 서로 다른 계열의 모델들끼리는 사람 집단끼리보다 훨씬 더 비슷했다.

**쉽게 말하면** AI의 잉크는 중심은 진하지만 거의 번지지 않는다. 모두가 공유하는 핵심은 잘 잡지만, 사람마다 다르게 번지는 가장자리, 곧 감정 경험의 주관성은 잘 담지 못한다.

## 정리

| 입장 | 핵심 주장 | 대표 연구 |
|---|---|---|
| 이해할 수 없다 | 형식만으로는 의미에 닿을 수 없다 | Searle, Harnad, Bender & Koller |
| 이해할 수 있다 | 의미는 개념 사이의 관계에서도 나온다 | Piantadosi & Hill |
| 실험으로 가리자 | 선험적 논증보다 내부 역량을 측정해야 한다 | Pavlick, Mitchell & Krakauer |
| 데이터가 보여 준 것 | 추상적 속성은 닮고, 몸의 속성과 주관적 번짐은 다르다 | Xu 등, Bhattacharyya 등 |

AI가 개념의 진한 중심까지는 이해하고 수행한다는 직관, 그러나 가장자리는 다르다는 직관 모두 데이터와 어긋나지 않는다. 다만 지금까지의 실험은 AI가 무엇을 '표상하는가'를 본 것이지, 무엇을 '느끼는가'를 본 것은 아니다.

## 더 생각해 볼 질문

1. 시각 장애가 있는 사람도 '빨강'의 의미를 안다. 그렇다면 몸의 경험은 의미에 꼭 필요한 것일까, 아니면 여러 경로 중 하나일까?
2. AI에게 카메라와 로봇 팔을 달아 주면 기호 접지 문제는 풀리는 걸까?
3. 개념의 가장자리가 사람마다 다르게 번지는 것은 결점일까, 인간 개념의 본질일까?

다음 편에서는 Piantadosi와 Hill의 제안대로 AI의 내부를 직접 들여다본 연구들을 살펴본다.

## 참고 자료

- Searle, J. R. (1980). Minds, brains, and programs. *Behavioral and Brain Sciences, 3*(3), 417-424. [doi.org/10.1017/S0140525X00005756](https://doi.org/10.1017/S0140525X00005756)
- Harnad, S. (1990). The symbol grounding problem. *Physica D: Nonlinear Phenomena, 42*(1-3), 335-346. [doi.org/10.1016/0167-2789(90)90087-6](https://doi.org/10.1016/0167-2789(90)90087-6)
- Bender, E. M., & Koller, A. (2020). Climbing towards NLU: On meaning, form, and understanding in the age of data. *Proceedings of ACL 2020*, 5185-5198. [doi.org/10.18653/v1/2020.acl-main.463](https://doi.org/10.18653/v1/2020.acl-main.463)
- Piantadosi, S. T., & Hill, F. (2022). Meaning without reference in large language models. *arXiv:2208.02957*. [arxiv.org/abs/2208.02957](https://arxiv.org/abs/2208.02957)
- Pavlick, E. (2023). Symbols and grounding in large language models. *Philosophical Transactions of the Royal Society A, 381*(2251), 20220041. [doi.org/10.1098/rsta.2022.0041](https://doi.org/10.1098/rsta.2022.0041)
- Mitchell, M., & Krakauer, D. C. (2023). The debate over understanding in AI's large language models. *PNAS, 120*(13), e2215907120. [doi.org/10.1073/pnas.2215907120](https://doi.org/10.1073/pnas.2215907120)
- Xu, Q., Peng, Y., Nastase, S. A., Chodorow, M., Wu, M., & Li, P. (2025). Large language models without grounding recover non-sensorimotor but not sensorimotor features of human concepts. *Nature Human Behaviour, 9*(9), 1871-1886. [doi.org/10.1038/s41562-025-02203-8](https://doi.org/10.1038/s41562-025-02203-8)
- Bhattacharyya, S., et al. (2025). Too categorical to be human: Emotion concepts in LLMs and humans. *arXiv:2508.05880*. [arxiv.org/abs/2508.05880](https://arxiv.org/abs/2508.05880)
