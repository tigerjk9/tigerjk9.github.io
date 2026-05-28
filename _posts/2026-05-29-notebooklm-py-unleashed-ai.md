---
title: "구글 NotebookLM, 비공식 API로 야생화된 학습 조교의 등장"
date: 2026-05-29 00:30:06 +0900
categories: [AI, 교육]
tags: [LLM, 생성형AI, 에듀테크, 교육혁신, AI협업, AI리터러시, 학습과학, 교사전문성]
header:
  teaser: /assets/notebooklm-py-unleashed-ai-src1-thumb.jpg
permalink: /post/notebooklm-py-unleashed-ai/
---

새 도구는 매일 쏟아진다. 교실로 옮겨도 될 도구와 그저 호기심 정도로 만져볼 도구의 구분이 교사의 일이 됐다. 최근 구글의 **NotebookLM**을 파이썬·AI 에이전트에서 직접 제어하는 비공식 라이브러리 **`notebooklm-py`**가 공개됐다. 정식 SDK 없이 비공개 내부 API를 파고든 결과물이다. 편리함의 새 카드라기보다, 기술을 어떻게 마주할지 다시 묻게 만드는 카드에 가깝다.

## 첫 만남 — 연구 조수의 탈을 쓴 야생마

**NotebookLM**은 구글이 제공하는 연구 도구이다. PDF, 웹 페이지, 동영상 같은 다양한 자료를 입력하면, 이를 바탕으로 채팅, 오디오 개요, 영상 요약, 슬라이드, 인포그래픽 등을 자동으로 만들어낸다. 문제는 그동안 웹 UI로만 접근 가능했다는 점이다. 대량의 자료를 일괄 처리하거나 다른 AI 도구와 연계하기에는 명백한 한계가 있었다. 이때 **`notebooklm-py`**가 등장한다. 이 라이브러리는 **NotebookLM**의 비공개 API를 파고들어, 파이썬 코드나 명령줄 환경에서 거의 모든 기능을 제어하도록 돕는다.


<figure>
<img src="/assets/notebooklm-py-unleashed-ai-src1-thumb.jpg" alt="구글 NotebookLM, 비공식 API로 야생화된 학습 조교의 등장">
</figure>


이는 비공식 프로젝트이므로, 안정성을 맹신해서는 곤란하다. **`notebooklm-py`** 개발팀도 README에 "Google과 제휴 관계가 없으며, 내부 API가 예고 없이 바뀌면 동작이 중단될 수 있다"고 명확히 안내한다. 즉, 이 도구는 완벽하게 다듬어진 경주마가 아니라, 길들여지지 않은 야생마에 가깝다. 그만큼 강력한 잠재력을 지니지만, 언제든 예측 불가능한 변수를 던질 수 있다는 경고이다. 현장 교육자들은 이 도구를 프로토타입이나 개인 연구 자동화에 활용하는 것이 현명한 접근 방식임을 인지해야 한다. 공식적인 학교 시스템이나 핵심 의존성으로 도입하는 행위는 재앙을 부를 수 있다.

## 자동화, 그 너머의 지능형 조교

**`notebooklm-py`**의 가장 흥미로운 지점은 단순히 API를 래핑하는 데 그치지 않는다는 점이다. 이 라이브러리는 AI 에이전트와의 통합을 핵심 사용 시나리오로 제시한다. 저장소에는 **NotebookLM** 사용법을 정리한 `SKILL.md` 파일이 포함된다. 이 스킬 파일을 설치하면, **Claude Code**나 **OpenAI Codex** 같은 LLM 기반 에이전트가 **NotebookLM**의 기능을 자연어 명령으로 실행한다.

| 사용 방식 | 주요 사용자 | 강점 | 약점 및 고려사항 |
|---|---|---|---|
| CLI | 셸 스크립트 사용자, 빠른 자동화 | 직관적, 스크립트화 용이, CI/CD 통합 | 복잡한 로직 구현 어려움, 학습 곡선 존재 |
| Python API | 개발자, 애플리케이션 임베딩 | 유연성, 비동기 처리, 복잡한 워크플로우 | 코딩 지식 필수, 초기 설정 난이도 있음 |
| AI 에이전트 | 비기술 사용자, 자연어 제어 | 자연어 인터페이스, 워크플로우 자동화 | 에이전트의 해석 능력 의존, 오작동 가능성, 프롬프트 엔지니어링 필요 |

이것은 무엇을 의미하는가? "이 PDF 5개를 **NotebookLM** 노트북에 올리고, 오디오 개요를 만든 다음 MP3로 저장해 줘" 같은 명령을 AI 에이전트에게 내리는 것만으로 일련의 작업을 자동화하는 일이 가능하다는 뜻이다. 교사가 참고 자료를 모아 자동으로 요약본을 만들고, 퀴즈나 플래시카드를 생성하는 시간을 획기적으로 줄이는 데 직접적인 도움이 된다. 본질적으로 이는 반복적인 정보 처리 작업에서 교사를 해방시켜, 교육 본연의 역할에 집중하게 만드는 강력한 도구이다. 그러나 에이전트의 지시 해석 능력에 따라 결과가 달라지므로, 프롬프트 엔지니어링 역량이 결과물의 질을 결정한다.

## 보이지 않던 기능들의 출현 — '숨겨진 보물'과 '불확실성의 영역' 사이

**`notebooklm-py`**의 또 다른 주목할 만한 특성은 **NotebookLM** 웹 UI에서는 제공하지 않는 기능들을 API나 CLI로 노출한다는 점이다. 모든 산출물을 한 번에 내려받는 일괄 다운로드, 퀴즈와 플래시카드를 JSON, Markdown, HTML 같은 구조화된 형태로 내보내는 export 기능이 대표적이다. 편집 가능한 PPTX 형태의 슬라이드 덱 다운로드, 슬라이드 단위로 자연어 프롬프트를 사용하여 수정하는 기능도 포함된다.


<figure>
<img src="/assets/notebooklm-py-unleashed-ai-img2-thumb.jpg" alt="구글 NotebookLM, 비공식 API로 야생화된 학습 조교의 등장">
</figure>


이러한 '웹 UI 너머'의 기능들은 교육 콘텐츠 생산의 패러다임을 바꾼다. 교사는 더 이상 하나씩 수작업으로 자료를 처리할 필요가 없다. 특정 주제에 대한 수십 개의 PDF를 한 번에 처리하고, 각 자료에서 핵심 개념을 추출해 다양한 형태의 학습 자료로 변환하는 것이 가능해진다. 이는 교육 자료 제작의 생산성을 극대화하는 동시에, 개인화된 학습 자료를 대량으로 생산하는 기반이 된다. 단, 이러한 확장 기능은 더욱 깊이 있는 비공개 API 사용을 의미한다. 구글이 언제든 내부 구조를 변경하면, 이 기능들은 가장 먼저 작동을 멈출 수 있다. 기능의 강력함만큼 그 지속가능성에 대한 의구심도 커진다.

## 기술 활용의 스펙트럼 — CLI, API, 에이전트

**`notebooklm-py`**는 같은 기능 집합을 세 가지 인터페이스로 제공한다. 사용자는 자신의 기술 숙련도와 활용 맥락에 따라 가장 적합한 방식을 선택한다.

*   **CLI (명령줄 인터페이스)**: 셸 스크립트와 빠른 작업, CI/CD 자동화에 적합하다. `notebooklm login`, `notebooklm create "My Research"`, `notebooklm source add "./paper.pdf"`와 같은 직관적인 명령으로 작업을 수행한다.
*   **Python API**: 애플리케이션 임베드, 비동기 워크플로우, 사용자 정의 파이프라인에 유용하다. `async with await NotebookLMClient.from_storage() as client:`와 같이 파이썬 코드 내에서 직접 기능을 호출하며 복잡한 로직을 구현한다.
*   **Agent 통합**: **Claude Code**나 **OpenClaw** 같은 LLM 기반 에이전트가 자연어 명령으로 **NotebookLM**을 다루도록 만든다. `notebooklm skill install` 명령으로 에이전트가 사용할 스킬을 설치한다.

```python
import asyncio
from notebooklm import NotebookLMClient

async def main():
    async with await NotebookLMClient.from_storage() as client:
        # 노트북 생성 및 소스 추가
        nb = await client.notebooks.create("초등 수학 연구")
        await client.sources.add_url(nb.id, "https://example.com/math-curriculum", wait=True)

        # 소스 기반 질의응답
        result = await client.chat.ask(nb.id, "이 교육과정의 핵심 목표는 무엇인가?")
        print(result.answer)

        # 오디오 개요 생성 및 다운로드 (예시)
        status = await client.artifacts.generate_audio(nb.id, instructions="교사들에게 친숙하게 설명해 줘")
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_audio(nb.id, "math_podcast.mp3")

asyncio.run(main())
```
위 Python 코드는 교사가 특정 수학 교육과정에 대한 URL을 입력하고, 그 내용을 바탕으로 질문하며, 심지어 오디오 개요까지 만드는 과정을 자동화하는 예시이다. 이처럼 도구의 힘은 사용자의 숙련도에 정비례한다. 파이썬을 다룰 줄 아는 교사라면 훨씬 더 강력한 워크플로우를 설계할 수 있다는 의미이다.

## 지속가능성의 딜레마와 윤리적 책임

**`notebooklm-py`**는 MIT 라이선스로 배포되어 자유롭게 사용 가능하지만, **NotebookLM** 자체의 이용 약관은 구글이 별도로 관리한다. 즉, 비공식 API를 통한 자동화된 호출이 구글의 사용 정책이나 속도 제한(rate limit)을 위반할 위험이 상존한다. 인증 방식 또한 **Playwright**를 통해 브라우저 로그인 쿠키를 저장하는 방식을 사용한다. 이는 기술적인 우회일 뿐, 안정적인 공식 API의 그것과는 본질적으로 다르다.


<figure>
<img src="/assets/notebooklm-py-unleashed-ai-img3-thumb.jpg" alt="구글 NotebookLM, 비공식 API로 야생화된 학습 조교의 등장">
</figure>


혁신의 그림자에는 늘 책임의 무게가 따른다. **`notebooklm-py`** 같은 도구는 분명 교육자의 업무 효율성을 비약적으로 높일 잠재력을 가진다. 그러나 이 잠재력을 실제 가치로 전환하려면 몇 가지 구조적인 분석이 선행되어야 한다. 첫째, 비공식 API에 대한 의존성은 기술 부채로 작용한다. 언제든 서비스가 중단될 위험을 감수해야 한다. 둘째, AI 에이전트가 생성한 콘텐츠의 출처와 정확성, 그리고 표절 문제에 대한 책임은 여전히 사용자에게 있다. 셋째, 민감한 학습자 데이터를 이런 비공식 경로로 처리하는 것은 윤리적, 법적 문제를 야기할 수 있다. 단순히 '편리하다'는 이유만으로 기술을 무비판적으로 수용해서는 곤란하다.

## 우리가 '어떻게' 나아갈 것인가

**`notebooklm-py`**는 교육 현장의 '전략적 탐구자'에게 매력적인 도구이다. 매력만큼 신중한 접근이 필요하다. 새로운 기술 도입은 기능 카탈로그를 외우는 일이 아니라, 어디서 멈출지를 함께 정하는 일이다.

가벼운 시도부터 시작한다. 학년 메신저에 "이 라이브러리로 다음 주 과학 단원 PDF 5개를 한 번에 오디오 개요로 뽑아봤다"는 한 줄을 던지는 것, 동학년 점심 자리에서 "퀴즈 JSON으로 뽑아 우리 반에 돌렸더니 오답 패턴이 이렇게 모이더라"는 관찰을 나누는 것. 이런 작은 공유가 쌓일 때 비로소 비공식 API의 위험 감수 범위와 실제 효용의 경계가 우리 학교의 언어로 자리 잡는다. 거꾸로 말하면, 한 명의 얼리 어답터만이 어두운 화면 앞에서 분주한 학년실은 곧 그 도구를 잃는다. 다음 학기에 그 교사가 자리를 옮기면 노하우도 함께 떠나기 때문이다. 비공식 도구의 진짜 리스크는 API가 막히는 날이 아니라, 그것을 다루는 사람이 한 명뿐인 날이다.

## 출처
- <https://discuss.pytorch.kr/t/notebooklm-py-google-notebooklm-python-ai-api/10268>
