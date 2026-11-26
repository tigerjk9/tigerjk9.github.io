---
title: "AI 시대, 왜 역량보다 지식이 먼저인가? 21편의 연구로 본 근거와 쟁점"
date: 2026-11-26 11:00:00 +0900
categories: [학습과학, 교육]
tags: [논문리뷰, 지식교육, 역량중심교육, 생성형AI, 학습과학, 인지부하이론, 메타인지, 교육과정, 문헌리뷰]
description: "생성형 AI가 답을 대신 주는 시대에도 지식교육이 역량교육의 토대여야 하는 이유를 무작위 실험, 메타분석, 국제기구 보고서, 교육과정 이론 21편으로 정리하고, 연구들이 공유하는 결론과 서로 갈리는 지점을 짚는다."
permalink: /post/knowledge-before-competency-ai-era/
---

생성형 AI가 답을 대신 주는 시대에도 지식교육이 역량교육보다 먼저여야 하는 이유를, AI 시대의 실험 연구와 인지과학, 교실·정책 연구, 교육과정 이론 21편으로 정리했다.

> "어디서 찾을 수 있는지 아는 것"과 "실제로 아는 것"은 다르다.
> Oakley 외, *The Memory Paradox* (2025)

## 들어가며

"검색하면 다 나오는데 왜 외워야 하나?", "이제는 AI가 답을 주니 지식보다 역량이 중요하다."
2015·2022 개정 교육과정을 거치며 우리 교육은 '역량'을 중심에 두었고, 생성형 AI의 등장은 이런 흐름에 더욱 힘을 실어 주는 듯 보인다.

그런데 최근 쏟아지는 실증 연구들은 정반대 방향을 가리킨다. AI가 똑똑해질수록, 그 AI를 판단하고 감독할 인간의 내부 지식이 더 중요해진다는 것이다.

이 글의 출발점은 Barbara Oakley, Terrence Sejnowski 등이 쓴 [*The Memory Paradox: Why Our Brains Need Knowledge in an Age of AI*](https://link.springer.com/chapter/10.1007/978-3-032-11814-1_22)다. 이 장(chapter)은 2026년 Springer의 *The Artificial Intelligence Revolution*에 실렸고, 프리프린트는 [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5250447)과 [arXiv](https://arxiv.org/abs/2506.11015)에서 무료로 볼 수 있다. 핵심 주장은 다음과 같다.

- 지식과 기술(skill)은 분리된 것이 아니라 동전의 양면이다.
- 사실·개념은 서술기억(해마)에서 출발해, 반복 인출과 연습을 거쳐 절차기억(기저핵)으로 옮겨 가며 '직관'이 된다.
- 외부 도구(계산기, 검색, AI)에 너무 일찍, 너무 많이 맡기면 이 과정이 끊기고 '얕은 스키마'만 남는다.
- 탄탄한 내부 스키마를 가진 사람만이 AI 출력을 평가하고, 고치고, 이끌 수 있다.

이 장 자체의 리뷰는 [AI가 다 알려 주는 시대에 왜 여전히 머릿속 지식이 필요한가?](/post/oakley-2026-memory-paradox/)에 따로 정리해 두었다. 아래에서는 이 주장을 뒷받침하거나 보완하는 대표 연구 21편을 네 갈래로 나누어 정리하고, 마지막에 이 연구들의 공통 인사이트와 서로 다른 지점을 총평으로 묶었다.

---

## 한눈에 보기

| # | 연구 · 출처 · 설계 | 핵심 결과 |
|---|---|---|
| 1 | **Bastani 외 (2025)**<br>PNAS<br>현장 무작위 실험, 고교생 약 1,000명<br>[논문](https://doi.org/10.1073/pnas.2422633122) · [무료 PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12232635) | AI로 연습하면 점수가 오르지만, AI를 빼면 시험 점수 17% 하락 |
| 2 | **OECD (2026)**<br>Digital Education Outlook 2026<br>국제기구 증거 종합<br>[보고서](https://www.oecd.org/en/publications/oecd-digital-education-outlook-2026_062a7394-en.html) | 과제를 AI로 잘 해내는 것이 곧 학습은 아니다 |
| 3 | **Shen & Tamkin (2026)**<br>arXiv (Anthropic)<br>무작위 실험, 개발자<br>[논문](https://arxiv.org/abs/2601.20245) · [해설](https://www.anthropic.com/research/AI-assistance-coding-skills) | AI로 배운 집단의 숙달 점수 17% 낮음, 특히 디버깅 |
| 4 | **Lehmann 외 (2025)**<br>arXiv / SSRN<br>사전등록 실험 2개 + 현장 연구<br>[논문](https://arxiv.org/abs/2409.09047) | LLM은 사전지식 많은 학생은 돕고 적은 학생은 해친다 |
| 5 | **Fan 외 (2025)**<br>British Journal of Educational Technology<br>무작위 실험, 4개 집단<br>[논문](https://doi.org/10.1111/bjet.13544) | 에세이 점수는 올랐지만 지식 습득·전이 차이 없음 |
| 6 | **Dell'Acqua 외 (2026)**<br>Organization Science<br>현장 실험, BCG 컨설턴트 758명<br>[논문](https://doi.org/10.1287/orsc.2025.21838) | AI 능력 밖 과제에서 AI 사용자의 정답률 19% 낮음 |
| 7 | **Lee 외 (2025)**<br>CHI 2025 (Microsoft Research)<br>지식노동자 319명 설문<br>[논문](https://doi.org/10.1145/3706598.3713778) | AI를 믿을수록 비판적 사고 감소, 자기 확신이 클수록 증가 |
| 8 | **Budzyń 외 (2025)**<br>Lancet Gastroenterology & Hepatology<br>다기관 관찰 연구<br>[논문](https://doi.org/10.1016/S2468-1253(25)00133-5) | AI에 익숙해진 의사가 AI 없이 할 때 선종 발견율 28.4%에서 22.4%로 |
| 9 | **미네소타대 CEHD (2026)**<br>전문가 합의 보고서<br>전문가 합의 연구<br>[보고서](https://www.cehd.umn.edu/AI-expert-consensus-report-2026) | 무분별한 AI 사용은 기억 형성과 고차적 사고를 위협 |
| 10 | **Kirschner, Sweller & Clark (2006)**<br>Educational Psychologist<br>이론·증거 종합<br>[논문](https://doi.org/10.1207/s15326985ep4102_1) | 최소 안내 수업은 강한 안내 수업보다 덜 효과적 |
| 11 | **Tricot & Sweller (2014)**<br>Educational Psychology Review<br>이론 리뷰<br>[논문](https://doi.org/10.1007/s10648-013-9243-1) | 지적 능력의 핵심은 영역 특수적 지식 |
| 12 | **Sala & Gobet (2019), Gobet & Sala (2023)**<br>Collabra / Perspectives on Psychological Science<br>2차 메타분석<br>[2019](https://doi.org/10.1525/collabra.203) · [2023](https://doi.org/10.1177/17456916221091830) | 일반 인지 훈련의 원전이 효과는 작거나 없음 |
| 13 | **Tetzlaff 외 (2025)**<br>Learning and Instruction<br>메타분석, 60개 실험<br>[논문(OA)](https://doi.org/10.1016/j.learninstruc.2025.102142) | 초보자는 안내 많은 수업, 숙련자는 안내 적은 수업이 유리 |
| 14 | **Willingham (2007) / Recht & Leslie (1988)**<br>American Educator / J. of Educational Psychology<br>리뷰 / 실험<br>[Willingham](https://www.aft.org/sites/default/files/media/2014/Crit_Thinking.pdf) · [Recht & Leslie](https://doi.org/10.1037/0022-0663.80.1.16) | 비판적 사고와 독해는 배경지식에 달려 있다 |
| 15 | **Grissmer 외 (2023)**<br>EdWorkingPaper<br>입학 추첨(자연 실험)<br>[논문](https://edworkingpapers.com/ai23-755) | 지식 중심 학교 입학 시 읽기 성취 16 백분위 상승 |
| 16 | **Smith 외 (2021)**<br>Reading Psychology<br>비판적 문헌 리뷰<br>[논문](https://doi.org/10.1080/02702711.2021.1888348) | 배경지식은 약한 독해력을 일부 보완 |
| 17 | **Stockard 외 (2018)**<br>Review of Educational Research<br>메타분석, 328편<br>[논문](https://doi.org/10.3102/0034654317751919) | 직접교수법 효과는 50년간 일관되게 긍정적 |
| 18 | **OECD PISA 2015 분석 / McKinsey (2017)**<br>OECD / McKinsey<br>국제 비교 상관 분석<br>[OECD](https://www.oecd.org/content/dam/oecd/en/publications/reports/2018/11/the-science-of-teaching-science_b00c65f8/f5bd9e57-en.pdf) · [McKinsey](https://www.mckinsey.com/industries/education/our-insights/how-to-improve-student-educational-outcomes-new-insights-from-data-analytics) | 교사 주도 수업이 대부분 + 탐구 수업 일부가 최적 |
| 19 | **Young & Muller (2013)**<br>Review of Education<br>교육과정 이론<br>[논문](https://doi.org/10.1002/rev3.3017) | 역량 담론은 지식의 역할을 약화시킨다, '힘 있는 지식' |
| 20 | **OECD Learning Compass 2030**<br>OECD 개념 노트<br>정책 프레임워크<br>[PDF](https://www.oecd.org/content/dam/oecd/en/about/projects/edu/education-2040/concept-notes/OECD_Learning_Compass_2030_concept_note.pdf) | 역량과 지식은 경쟁 관계가 아니다 |
| 21 | **「역량기반 교육과정의 딜레마」 (2020)**<br>교육과정연구 38(4)<br>국내 교육과정 논쟁 검토<br>[KCI](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002667686) | 2015 개정 이후 역량 대 지식 논쟁을 정리 |

---

## A. AI 시대의 직접 증거

생성형 AI가 실제로 학습에 어떤 영향을 미치는지 측정한 연구들이다. 이 글의 주장에서 가장 무게가 실리는 부분이다.

### 1. Bastani 외 (2025), "Generative AI without guardrails can harm learning", *PNAS*

| 항목 | 내용 |
|---|---|
| 대상 | 튀르키예 고등학교 수학 수업, 학생 약 1,000명 |
| 설계 | 세 집단 무작위 배정: ① 일반 ChatGPT형(GPT Base) ② 정답 대신 교사가 만든 힌트를 주는 튜터형(GPT Tutor) ③ AI 없음 |
| 연습 단계 | AI 없는 집단보다 GPT Base는 48%, GPT Tutor는 127% 높은 점수 |
| 시험 단계(AI 없음) | GPT Base 집단은 AI를 쓰지 않은 집단보다 17% 낮은 점수. GPT Tutor 집단은 통제 집단과 유의미한 차이 없음 |
| 해석 | 학생들이 AI를 '목발(crutch)'처럼 써서 스스로 풀 능력을 기르지 못했다 |

**왜 중요한가:** "AI를 쓰면 점수가 오른다"는 관찰과 "AI를 쓰면 실력이 는다"는 주장이 전혀 다르다는 것을 가장 깔끔하게 보여 준다. 동시에 AI를 어떻게 설계하느냐에 따라 부작용을 막을 수 있다는 점도 보여 주기 때문에, 이 연구는 'AI 반대'가 아니라 '지식 형성을 보호하는 AI'를 지지하는 근거로 쓰는 것이 정확하다. 다만 튜터형도 시험 점수를 *올리지는* 못했다는 점은 기억해 둘 만하다.

### 2. OECD (2026), *Digital Education Outlook 2026*

OECD가 생성형 AI와 학습에 관한 연구를 종합한 보고서다. 핵심 메시지는 제목처럼 간결하다. "GenAI로 과제를 성공적으로 해냈다고 해서 학습이 저절로 일어나지는 않는다."

- 일반 목적 챗봇에 인지 작업을 맡기면 '메타인지적 게으름'과 학습 이탈 위험이 생긴다.
- 여러 연구에서 AI를 쓴 학생이 더 좋은 결과물을 냈지만, AI를 빼고 본 시험에서는 그 이점이 사라지거나 오히려 뒤집혔다.
- 반대로 교육적 목적을 갖고 설계된 AI 도구는 지속적인 학습 효과를 보였다.
- 2024년 TALIS 기준, 중학교 교사의 37%가 업무에 AI를 사용했다.

**왜 중요한가:** 한국 교육정책이 크게 참고하는 OECD가 "수행과 학습은 다르다"는 결론을 공식화했다는 점에서, 정책 문서나 학교 기획안에 인용하기 가장 좋은 자료다.

### 3. Shen & Tamkin (2026), "How AI Impacts Skill Formation", arXiv (Anthropic)

| 항목 | 내용 |
|---|---|
| 대상 | 새로운 비동기 Python 라이브러리를 처음 배우는 개발자 |
| 설계 | AI 보조 사용 집단과 직접 코딩 집단 무작위 배정, 과제 후 개념 퀴즈 |
| 결과 | AI 집단 평균 50%, 직접 코딩 집단 67% (Cohen's d = 0.738, p = 0.01) |
| 속도 | AI 집단이 약 2분 빨랐지만 통계적으로 유의하지 않음 |
| 가장 큰 격차 | 디버깅, 즉 코드가 왜 틀렸는지 알아내는 능력 |
| 추가 발견 | AI 사용 패턴 6가지 중 3가지(추가 질문, 개념 설명 요청 등 인지적으로 참여하는 방식)는 AI를 써도 학습을 유지 |

**왜 중요한가:** AI를 만드는 회사가 직접 "AI가 높여 준 생산성은 역량으로 가는 지름길이 아니다"라고 보고했다는 점이 상징적이다. 특히 AI를 감독하는 데 꼭 필요한 '오류를 알아보는 능력'이 가장 크게 손상되었다는 결과는, AI 시대에 지식이 왜 더 필요한지를 정확히 보여 준다. 아직 동료심사 전 프리프린트다.

### 4. Lehmann, Cornelius & Sting (2025), "AI Meets the Classroom: When Do Large Language Models Harm Learning?"

- 사전등록한 실험 2개에서는 LLM이 전체 학습 성과에 평균적으로는 영향을 주지 않았다.
- 그러나 사용 방식에 따라 결과가 갈렸다.
  - **대체형 사용**(연습 문제를 LLM에게 맡김): 진도는 빨라지지만 각 주제를 얕게 이해
  - **보완형 사용**(LLM을 튜터처럼 활용해 설명을 요청): 주제 이해도 향상
- 대학 프로그래밍 수업 현장 연구에서는 대체형 사용만 관찰되었고, 장기적으로 학습 성과가 유의미하게 떨어졌다.
- 가장 중요한 결과: LLM은 사전지식이 많은 학생의 학습은 도왔지만, 사전지식이 적은 학생의 학습은 해쳤다.

**왜 중요한가:** "지식이 먼저"라는 주장을 가장 직접적으로 뒷받침한다. 저자들은 직장에서는 AI가 격차를 줄이는 것과 달리, 교육에서는 AI가 불평등을 키우는 것으로 보인다고 지적한다. 프리프린트다.

### 5. Fan 외 (2025), "Beware of metacognitive laziness", *British Journal of Educational Technology*

| 집단 | ChatGPT / 인간 전문가 / 체크리스트 도구 / 통제 |
|---|---|
| 에세이 점수 향상 | ChatGPT 집단이 다른 모든 집단보다 유의미하게 높음 |
| 내재적 동기 | 집단 간 차이 없음 |
| 지식 습득 | 집단 간 차이 없음 |
| 지식 전이 | 집단 간 차이 없음 |

**왜 중요한가:** 결과물은 좋아졌지만 머릿속에 남은 것은 같았다. 연구진은 학습자가 AI 피드백을 그대로 따르면서 스스로 점검하고 조절하는 과정을 건너뛰는 현상을 '메타인지적 게으름'이라고 이름 붙였고, 이 용어는 이후 OECD 보고서에도 그대로 인용되었다.

### 6. Dell'Acqua 외 (2026), "Navigating the Jagged Technological Frontier", *Organization Science*

- BCG 컨설턴트 758명 대상 현장 실험
- AI가 잘하는 과제(18개)에서는 AI 사용자가 과제를 12.2% 더 많이, 25.1% 더 빨리, 더 높은 품질로 완료
- AI 능력 밖에 있도록 고른 복잡한 경영 과제에서는 AI 사용자가 정답을 낼 확률이 19% 낮음
- AI의 능력 경계는 '울퉁불퉁(jagged)'해서, 겉보기에 비슷한 난이도의 과제라도 AI가 잘하는 것과 못하는 것이 섞여 있음

**왜 중요한가:** AI가 언제 틀리는지 알아보려면 그 분야의 지식이 필요하다. 하버드경영대학원(HBS)의 후속 연구인 ["GenAI Wall Effect"](https://www.hbs.edu/ris/Publication%20Files/26-011_04dcb593-c32b-4e4e-80fc-b51030cf8a12.pdf)(HBS, 2025)도 해당 분야와 거리가 먼 사람은 AI를 써도 전문가 수준에 도달하지 못한다고 보고한다. "AI가 있으니 누구나 전문가가 될 수 있다"는 주장에 대한 반례다.

### 7. Lee 외 (2025), "The Impact of Generative AI on Critical Thinking", *CHI 2025*

- Microsoft Research 등이 지식노동자 319명에게서 AI 사용 사례 936건을 수집
- **AI에 대한 신뢰가 높을수록 비판적 사고를 덜 했고**, 자기 능력에 대한 확신이 높을수록 비판적 사고를 더 했다.
- 사람들이 비판적 사고를 하는 방식도 달라졌다. 목표 설정, 프롬프트 수정, 그리고 AI 출력을 외부 자료와 자신의 전문 지식에 비추어 검증하는 활동이 중심이 된다.

**왜 중요한가:** AI 시대의 비판적 사고는 결국 '검증'이고, 검증의 기준은 내 안의 지식이다. 자기 확신의 근거가 되는 것이 바로 탄탄한 영역 지식이라는 점에서, 지식교육이 비판적 사고의 전제라는 논리를 받쳐 준다. 다만 자기보고식 설문이라는 한계가 있다.

### 8. Budzyń 외 (2025), 대장내시경 의사의 '탈숙련(deskilling)', *Lancet Gastroenterology & Hepatology*

- AI 보조 대장내시경을 도입한 뒤, 의사들이 AI 없이 시행한 일반 내시경의 선종 발견율(ADR)을 도입 전과 비교
- 환자 1,443명 기준, ADR이 28.4%에서 22.4%로 6.0%p 하락
- 다변량 분석에서도 AI 노출은 독립적으로 ADR 감소와 연관 (오즈비 0.69)

**왜 중요한가:** 이미 숙련된 전문가도 AI에 익숙해지면 혼자 하는 실력이 떨어질 수 있다는 사례다. 숙련자도 그렇다면, 아직 기초를 쌓는 학생에게는 위험이 더 클 것이라고 추론할 수 있다. 2026년 [ESMO 스코핑 리뷰](https://www.sciencedirect.com/science/article/pii/S2949820126000123)도 의료 분야의 탈숙련 증거는 아직 적지만 분야를 가리지 않고 일관된다고 정리했다. 무작위 실험이 아닌 관찰 연구라는 점은 밝혀 두어야 한다.

### 9. 미네소타대 CEHD (2026), 생성형 AI와 학습에 관한 전문가 합의 보고서

- 학습·교육 전문가들이 AI가 영향을 줄 수 있는 학습 과정 65가지를 정의하고, 그중 42가지에 대해 합의에 도달
- **위협이 가장 큰 영역:** 고차적 사고와 자기조절 과정. 특히 어린 학습자일수록 위험이 큼
- **도움이 되는 영역:** 피드백을 통한 학습, 자기 테스트, 예시를 통한 학습, 튜터링, 비계(scaffolding), 의도적 연습
- 보고서 표현: 일반 목적 AI를 무분별하게 쓰면 새로운 내용을 기억에 새기는 과정과, 그것을 깊이 이해하고 새로운 상황에 적용하는 고차적 사고를 모두 위협할 수 있다

**왜 중요한가:** 2026년 10월에 나온 가장 최신 종합 자료다. AI가 도움이 되는 영역이 모두 이미 배운 지식을 다지는 과정이라는 점이 이 글의 주장과 정확히 맞물린다. AI는 지식을 굳히는 데는 쓸모가 있지만, 지식을 처음 얻는 과정을 대신해서는 안 된다는 것이다.

---

## B. 인지과학의 근거, 왜 지식이 역량보다 먼저인가

AI 이전부터 축적된 연구들로, "왜 지식 없이 역량을 기를 수 없는가"에 대한 메커니즘을 설명한다.

### 10. Kirschner, Sweller & Clark (2006), "Why Minimal Guidance During Instruction Does Not Work", *Educational Psychologist*

발견학습, 문제기반학습, 탐구학습 등 '최소 안내' 교수법에 대한 가장 유명한 비판이다.

- **근거:** 인간의 작업기억은 용량이 매우 작다. 초보자는 새로운 정보를 처리할 장기기억 속 스키마가 없기 때문에, 스스로 탐색하게 하면 작업기억이 탐색 자체에 다 쓰이고 정작 배울 내용은 장기기억에 남지 않는다.
- **결론:** 최소 안내 수업은 학습 과정을 강하게 안내하는 수업보다 효과도 효율도 낮다. 풀이 예제(worked example)를 공부하는 것이 혼자 문제를 푸는 것보다 초보자에게 더 효과적이라는 연구들이 이를 뒷받침한다.

**연결점:** Oakley 외가 비판하는 "guide on the side" 교수법의 이론적 반론이 바로 이 논문이다.

### 11. Tricot & Sweller (2014), "Domain-Specific Knowledge and Why Teaching Generic Skills Does Not Work", *Educational Psychology Review*

- 지금까지 '일반 능력'으로 설명해 온 많은 현상이 사실은 장기기억 속 영역 특수적 지식으로 더 잘 설명된다고 주장한다.
- 진화교육심리학(Geary)의 구분을 활용한다. 모국어 말하기, 얼굴 인식 같은 생물학적 1차 지식은 저절로 습득되지만, 읽기·수학·과학 같은 생물학적 2차 지식은 명시적 교수가 필요하다.
- 문제해결, 비판적 사고 같은 일반 전략은 대부분 1차 지식이라 이미 갖고 있으며, 따로 가르쳐도 효과가 작다. 학교가 가르쳐야 할 것은 2차 지식, 즉 교과 지식이다.

**연결점:** "역량을 직접 가르치자"는 주장에 대한 가장 정면의 반박이다.

### 12. Sala & Gobet (2019), Gobet & Sala (2023), 원전이(far transfer)는 존재하는가

| 훈련 유형 | 근전이(비슷한 과제) | 원전이(다른 능력) |
|---|---|---|
| 작업기억 훈련 | 효과 있음 | 작거나 없음 |
| 음악, 체스, 비디오게임, 운동 게임 | - | 작거나 없음 |
| 위약 효과 통제 시 | - | 사실상 0 |

- 2019년 연구는 여러 메타분석을 다시 종합한 2차 메타분석이다.
- 2023년 논문에서 저자들은 "훈련으로 인한 원전이의 부재는 인간 인지의 불변적 특성"이라고까지 결론 내리며, 전문성은 영역 특수적이라는 기존 연구(Chase & Simon의 체스 연구 등)와도 일관된다고 설명한다.

**연결점:** '문제해결력', '창의성', '비판적 사고' 같은 일반 역량을 특정 활동으로 훈련하면 다른 영역으로 옮겨 갈 것이라는 기대에 실증적으로 의문을 제기한다.

### 13. Tetzlaff, Simonsmeier, Peters & Brod (2025), 전문성 역전 효과 메타분석, *Learning and Instruction*

| 항목 | 내용 |
|---|---|
| 규모 | 실험 연구 60편, 효과크기 176개, 참가자 5,924명 |
| 사전지식 적은 학습자 | 안내가 많은 수업에서 더 잘 배움 (d = 0.505) |
| 사전지식 많은 학습자 | 안내가 적은 수업에서 더 잘 배움 (d = -0.428) |
| 단서 | 어린 학생, 인문학·언어 학습 분야에서는 증거가 덜 분명함 |

**연결점:** 탐구학습, 프로젝트 학습, 자기주도 학습이 효과를 내려면 먼저 지식이 쌓여 있어야 한다는 것을 보여 준다. 즉 "역량 중심 수업"이 나쁘다는 것이 아니라 순서의 문제라는 점을 정교하게 뒷받침한다. 오픈 액세스라 누구나 전문을 볼 수 있다.

### 14. Willingham (2007)과 Recht & Leslie (1988), 비판적 사고와 독해는 지식에 달려 있다

- **Willingham, "Critical Thinking: Why Is It So Hard to Teach?"** (*American Educator*): 비판적 사고는 내용과 분리된 기술이 아니며, 어떤 분야에 대해 비판적으로 생각하려면 그 분야의 지식이 있어야 한다고 설명한다. 교사용 잡지에 실린 글이라 현장에서 읽기 쉽다.
- **Recht & Leslie, 야구 연구** (*Journal of Educational Psychology*): 중학생을 독해력(상/하)과 야구 지식(상/하)으로 나누어 야구 경기 글을 읽게 했더니, 독해력보다 야구 지식이 이해도와 회상에 더 큰 영향을 주었다. 독해력이 낮아도 야구를 잘 아는 학생이 독해력이 높지만 야구를 모르는 학생보다 더 잘 이해했다.

**연결점:** '문해력'이나 '비판적 사고' 같은 역량이 사실은 배경지식 위에서 작동한다는 고전적 근거다.

---

## C. 교실과 정책의 근거

### 15. Grissmer 외 (2023), Core Knowledge 차터스쿨 입학 추첨 연구

- 유치원 입학 추첨에서 당첨되어 지식 중심 교육과정(Core Knowledge Sequence) 학교에 다닌 학생과, 떨어진 학생을 비교한 자연 실험
- 3~6학년 읽기 성취가 16 백분위(0.47 표준편차) 상승
- **저소득층 학생에게서 효과가 훨씬 컸음**
- 연구진은 이 효과가 모든 소득 계층을 포함한 교육 개입 연구 중 가장 큰 편에 속한다고 평가

**왜 중요한가:** 읽기 '전략'을 가르치는 것보다 과학·역사·예술 등 폭넓은 지식을 체계적으로 쌓는 것이 장기적으로 읽기 능력을 더 키운다는 근거다. 형평성 측면에서도 강력하다. 다만 아직 동료심사를 거친 학술지 논문이 아닌 워킹페이퍼다.

### 16. Smith, Snow, Serry & Hammond (2021), "The Role of Background Knowledge in Reading Comprehension: A Critical Review", *Reading Psychology*

- 배경지식의 효과는 글의 성격, 필요한 이해의 깊이, 독자의 오개념 여부에 따라 달라짐
- 배경지식이 적은 독자는 응집성이 높은 글에서 더 도움을 받음
- **독해력이 약한 독자도 배경지식이 많으면 약한 독해 기술을 어느 정도 보완할 수 있었음**

**연결점:** Grissmer 연구의 메커니즘을 설명해 주는 리뷰다. 호주 퀸즐랜드 교육부의 읽기 지도 문헌 검토에서도 독해에 영향을 주는 요인 중 배경지식이 가장 중요하다고 인용된다.

### 17. Stockard 외 (2018), 직접교수법(Direct Instruction) 50년 메타분석, *Review of Educational Research*

| 항목 | 내용 |
|---|---|
| 범위 | 1966~2016년 연구 328편, 연구 설계 413개, 효과 약 4,000개 |
| 결과 | 읽기, 수학, 언어, 철자 등 모든 영역에서 효과가 긍정적이고 통계적으로 유의 (정의적 영역 메타회귀만 예외) |
| 지속성 | 유지 기간에도 효과가 거의 줄지 않음 |
| 노출량 | 프로그램에 더 오래 노출될수록 효과가 큼 |

**연결점:** 명시적이고 구조화된 교수가 장기적으로 효과적이라는 대규모 증거다. 여기서 말하는 'Direct Instruction'은 Engelmann이 개발한 특정 교육과정이라는 점은 구분해 두는 것이 좋다.

### 18. OECD PISA 2015 분석 / McKinsey (2017)

- OECD 분석: 사회경제적 배경을 통제한 뒤 탐구 기반 수업에 더 많이 노출될수록 과학 성취가 낮은 국가가 56개국이었고, 탐구 수업에 자주 노출된 학생이 더 높은 점수를 받은 나라는 없었다. 반대로 교사 주도 수업은 대부분의 국가에서 높은 성취와 연관되었다.
- McKinsey 분석: 최적 지점은 "대부분 또는 거의 모든 수업은 교사 주도, 일부 수업은 탐구 기반"이었다. 학생이 교사 주도 수업으로 충분한 내용을 익힌 뒤에야 탐구학습의 이점을 온전히 누릴 수 있다는 것이 결론이다.

**주의할 점:** 모두 상관 분석이며, 교사 주도 수업과 높은 성취의 연관이 나타나지 않은 예외 국가 세 곳에 한국이 포함되어 있다(인도네시아, 페루와 함께). 안내가 함께 이루어지는 탐구는 긍정적이라는 [후속 연구](https://www.tandfonline.com/doi/full/10.1080/09500693.2020.1716093)도 있으므로, 한국 맥락에서는 "탐구는 나쁘다"보다 "안내 없는 탐구는 위험하다"로 쓰는 것이 정확하다.

---

## D. 교육과정 이론과 역량 대 지식 논쟁

### 19. Young & Muller (2013), "On the Powers of Powerful Knowledge", *Review of Education*

영국 교육사회학자 Michael Young의 '힘 있는 지식(powerful knowledge)' 논의다.

| 구분 | Future 1 | Future 2 | Future 3 |
|---|---|---|---|
| 교육과정 | 전통적 지식 전달 | 역량·일반 기능 중심 | 지식 주도 교육과정 |
| 지식관 | 고정된 지식 | 지식의 경계가 사라짐, '과도하게 사회화된' 지식관 | 오류 가능하고 변화하지만 전문가 공동체의 인식 규칙을 따르는 지식 |
| 교수법 | 주입식 | 학습자 중심, 교사는 촉진자 | 교과 지식에 대한 체계적 접근 |

- 역량 담론은 지식의 선정과 조직이라는 교육과정 설계의 핵심을 피해 가며, 교육에서 지식의 역할을 크게 약화시킨다고 비판한다.
- 교과 지식이 '힘 있는' 이유는 객관적이고 검증 가능하며, 학생을 일상 경험 너머로 데려가 사회적 논쟁에 참여할 수 있게 해 주기 때문이다.
- 그래서 이런 지식에 접근하는 것은 모든 학생의 권리이며, 특히 가정에서 이런 지식을 얻기 어려운 학생에게 학교가 반드시 제공해야 한다.

**연결점:** 인지과학과는 다른 경로, 즉 인식론과 사회정의의 관점에서 같은 결론에 도달한다.

### 20. OECD Learning Compass 2030 개념 노트

역량 중심 교육과정의 국제적 근거로 자주 인용되는 OECD 문서 자체가 지식을 토대로 명시한다.

> "역량과 지식은 경쟁하거나 서로 배타적인 개념이 아니다. 학생은 이해의 기본 토대로서 핵심 지식을 배워야 한다."

같은 시리즈의 [Knowledge for 2030 개념 노트](https://www.oecd.org/content/dam/oecd/en/about/projects/edu/education-2040/concept-notes/Knowledge_for_2030_concept_note.pdf)는 "교과 지식은 여전히 이해의 필수 토대이며, 교과 지식을 습득할 기회는 형평성의 근본"이라고 적고 있다.

**연결점:** 역량 중심 교육을 주장하는 쪽의 근거 문서를 그대로 활용해 "역량 중심 교육과정도 지식을 전제한다"고 말할 수 있는 자료다.

### 21. 「역량기반 교육과정의 딜레마」 (2020), 『교육과정연구』 38(4), 한국교육과정학회

- 2015 개정 교육과정 시행 이후 계속된 논쟁을 세 입장으로 정리한다. ① 역량기반 교육과정을 유지·개선하자 ② 역량기반 교육과정으로 약화된 지식교육을 강화하자 ③ OECD 주도의 글로벌 교육과정 거버넌스에서 벗어나자
- 원래 직업교육에서 쓰이던 역량기반 교육과정이 학교 교육에 들어오면서 딜레마에 빠졌다는 점에 주목한다.
- OECD 교육 2030, Young의 힘 있는 지식론, Biesta의 주체화 담론을 중심으로 대안을 검토한다.
- KCI 피인용 72회로, 국내 논의의 기준점이 되는 논문이다.

**연결점:** 해외 연구를 한국 교육과정 논의로 연결해 주는 다리 역할을 한다.

---

## 총평, 공통 인사이트와 서로 다른 지점

### 공통 인사이트 다섯 가지

**1. 수행(performance)과 학습(learning)은 다르다.**
Bastani, Fan, Shen & Tamkin, Lehmann, OECD가 모두 같은 패턴을 보고한다. AI를 켠 상태의 점수는 오르지만, AI를 끈 상태의 실력은 그대로이거나 오히려 떨어진다. 학습과학에서 오래전부터 강조해 온 '수행과 학습의 구분'이 AI 시대에 가장 극적인 형태로 드러난 셈이다. 교육 현장에서는 결과물의 품질만으로 학습을 판단하면 안 된다는 뜻이다.

**2. 지식은 AI를 감독하는 능력이다.**
Dell'Acqua의 '울퉁불퉁한 경계', Lee의 '자기 확신과 비판적 사고', Shen & Tamkin의 '디버깅 능력 손상', Budzyń의 '탈숙련'은 모두 같은 지점을 가리킨다. AI가 언제 틀리는지 알아보는 능력은 그 분야의 지식에서 나온다. AI가 강력해질수록 AI를 평가할 수 있는 인간의 내부 지식이 오히려 더 중요해진다. Oakley 외가 말한 '기억의 역설'이 바로 이것이다.

**3. 지식은 지식을 부른다 (마태 효과).**
Lehmann(사전지식 많은 학생만 AI 덕을 봄), Tetzlaff(사전지식에 따라 효과적인 수업 방식이 달라짐), Grissmer(저소득층에서 효과가 더 큼), Smith(배경지식이 약한 독해력을 보완)는 모두 사전지식이 이후 학습의 질을 결정한다는 점을 보여 준다. 지식교육을 소홀히 하면 AI가 격차를 줄이는 것이 아니라 키울 수 있다. 지식교육은 형평성의 문제이기도 하다.

**4. 일반 역량은 지식 없이 전이되지 않는다.**
Tricot & Sweller, Sala & Gobet, Willingham, Recht & Leslie는 문제해결력, 비판적 사고, 독해력 같은 '역량'이 내용과 분리된 채 훈련되고 다른 영역으로 옮겨 가기 어렵다는 것을 보여 준다. 역량은 지식 위에서 작동한다.

**5. 결과를 바꾸는 것은 설계다.**
힌트형 튜터(Bastani), 인지적으로 참여하는 사용 패턴(Shen & Tamkin), 보완형 사용(Lehmann), 교육적 목적의 AI(OECD), 지식을 다지는 데 쓰는 AI(미네소타대)는 모두 긍정적이었다. 문제는 AI 자체가 아니라 지식 형성 과정을 건너뛰게 하는 방식이다. 이 연구들의 결론은 "AI를 금지하라"가 아니라 "지식을 먼저 쌓고, AI는 그 과정을 지키는 방향으로 설계하라"다.

### 서로 다른 지점과 긴장

**1. 직장과 교실의 차이.**
Dell'Acqua 연구와 그 이전 직장 연구들은 AI가 능력 범위 안의 과제에서 초보자에게 더 큰 도움을 준다고 보고한다. 반면 Lehmann 연구는 교실에서 AI가 사전지식이 적은 학생을 더 해친다고 보고한다. 겉보기에는 모순이지만, 목표가 다르기 때문이다. 직장의 목표는 '지금 결과물을 내는 것'이고, 교실의 목표는 '나중에 혼자 할 수 있게 되는 것'다. 생산성에 좋은 것이 학습에도 좋다고 단정할 수 없다.

**2. "지식이 많을수록 더 배운다"는 단순한 명제는 성립하지 않는다.**
Simonsmeier 외(2022)의 [대규모 메타분석](https://doi.org/10.1080/00461520.2021.1939700)(효과크기 8,776개)은 사전지식이 이후 성취와는 강하게 연관되지만, 사전지식과 지식 증가량의 상관은 평균적으로 0에 가깝다는 '사전지식의 역설'을 보고했다. 흥미롭게도 같은 연구자(Simonsmeier)가 참여한 Tetzlaff 외(2025)는, 사전지식의 진짜 역할은 어떤 수업 방식이 효과적인지를 결정하는 것임을 보여 준다. 따라서 "지식이 많으면 무조건 더 배운다"보다 "지식은 이해, 판단, 그리고 자기주도 학습이 가능해지는 조건이다"라고 말하는 것이 정확하다.

**3. 같은 결론, 다른 이유.**
인지과학 진영(Sweller, Kirschner)은 작업기억과 장기기억의 구조에서, 교육과정사회학 진영(Young)은 인식론과 사회정의에서, 신경과학 진영(Oakley, Sejnowski)은 서술기억에서 절차기억으로의 전환에서 출발한다. 근거의 성격이 다르기 때문에 함께 인용하면 설득력이 커지지만, 한 진영의 논리로 다른 진영의 주장을 대신 증명할 수는 없다.

**4. 역량 자체를 반대하는가, 순서를 문제 삼는가.**
Young과 Kirschner 등은 역량 담론과 최소 안내 교수법을 강하게 비판한다. 반면 OECD Learning Compass는 역량이 지식을 포함하는 개념이라고 말한다. 실증 연구들(Tetzlaff, McKinsey)이 지지하는 것은 역량 폐기가 아니라 "지식이 먼저, 그 위에 탐구와 역량"이라는 순서다. "역량은 목표, 지식은 토대"라는 틀이 가장 많은 연구와 양립한다.

**5. 증거의 강도가 다르다.**

| 증거 수준 | 해당 연구 |
|---|---|
| 무작위 실험 (동료심사 완료) | Bastani(PNAS), Fan(BJET), Dell'Acqua(Org Sci) |
| 무작위 실험 (프리프린트) | Shen & Tamkin, Lehmann |
| 메타분석 | Stockard, Sala & Gobet, Tetzlaff, Simonsmeier |
| 자연 실험 (워킹페이퍼) | Grissmer |
| 관찰·상관 연구 | Budzyń, PISA/McKinsey, Lee(설문) |
| 이론·리뷰·합의 | Kirschner, Tricot & Sweller, Willingham, Smith, Young & Muller, OECD, 미네소타대 |

Oakley 외가 인용한 MIT의 ["Your Brain on ChatGPT"](https://arxiv.org/abs/2506.08872)(Kosmyna 외, 2025)는 화제가 되었지만 소규모 프리프린트라 보조 근거로만 쓰는 것이 안전하다. 플린 효과 반전을 교육 방식 변화와 연결하는 Oakley 외의 주장 역시 흥미롭지만 인과관계가 확립된 것은 아니다.

**6. 연령과 교과에 따라 다를 수 있다.**
Tetzlaff 메타분석은 어린 학생과 인문학·언어 분야에서 전문성 역전 효과의 증거가 덜 분명하다고 밝혔고, 미네소타대 보고서는 어린 학습자일수록 AI로 인한 위험이 크다고 보았다. PISA 분석에서 한국이 예외였다는 점도 맥락을 고려해야 할 이유다.

---

## 맺으며, 교실에서 무엇을 할 것인가

연구들을 종합하면 다음과 같은 실천 방향이 나온다.

1. AI 없는 평가 구간을 확보한다. AI를 켠 상태의 결과물이 아니라, AI를 끈 상태에서 학생이 무엇을 할 수 있는지를 봐야 학습을 알 수 있다.
2. 핵심 지식은 명시적으로 가르치고 인출 연습으로 굳힌다. 사실, 개념, 어휘, 공식은 '검색하면 되는 것'이 아니라 고차적 사고가 작동하는 재료다.
3. AI는 답을 주는 도구가 아니라 생각을 요구하는 도구로 설계한다. 힌트형 튜터, 자기 테스트, 피드백처럼 이미 배운 지식을 다지는 용도에서 AI는 효과적이다.
4. 사전지식 수준에 따라 안내의 양을 조절한다. 초보자에게는 명시적 안내를, 지식이 쌓인 학습자에게는 탐구와 프로젝트를 제공한다.

AI가 모든 것을 대신 기억해 주는 시대일수록, 무엇이 맞고 틀린지 판단할 수 있는 지식은 학생의 머릿속에 있어야 한다. 역량은 그 지식 위에서만 자랄 수 있다.

---

## 출처

**출발점**
- Oakley, B., Johnston, M., Chen, K.-Z., Jung, E., & Sejnowski, T. (2026). The Memory Paradox: Why Our Brains Need Knowledge in an Age of AI. In *The Artificial Intelligence Revolution* (pp. 573–628). Springer. [링크](https://link.springer.com/chapter/10.1007/978-3-032-11814-1_22) · [SSRN 프리프린트](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5250447) · [arXiv](https://arxiv.org/abs/2506.11015)

**A. AI 시대의 직접 증거**
- Bastani, H., Bastani, O., Sungu, A., Ge, H., Kabakcı, Ö., & Mariman, R. (2025). Generative AI without guardrails can harm learning: Evidence from high school mathematics. *PNAS*, 122(26), e2422633122. [https://doi.org/10.1073/pnas.2422633122](https://doi.org/10.1073/pnas.2422633122)
- OECD (2026). *OECD Digital Education Outlook 2026*. [https://doi.org/10.1787/062a7394-en](https://doi.org/10.1787/062a7394-en)
- Shen, J. H., & Tamkin, A. (2026). How AI Impacts Skill Formation. arXiv:2601.20245. [https://arxiv.org/abs/2601.20245](https://arxiv.org/abs/2601.20245)
- Lehmann, M., Cornelius, P. B., & Sting, F. J. (2025). AI Meets the Classroom: When Do Large Language Models Harm Learning? arXiv:2409.09047. [https://arxiv.org/abs/2409.09047](https://arxiv.org/abs/2409.09047)
- Fan, Y., Tang, L., Le, H., Shen, K., Tan, S., Zhao, Y., Shen, Y., Li, X., & Gašević, D. (2025). Beware of metacognitive laziness. *British Journal of Educational Technology*. [https://doi.org/10.1111/bjet.13544](https://doi.org/10.1111/bjet.13544)
- Dell'Acqua, F., et al. (2026). Navigating the Jagged Technological Frontier. *Organization Science*. [https://doi.org/10.1287/orsc.2025.21838](https://doi.org/10.1287/orsc.2025.21838)
- Lee, H.-P., et al. (2025). The Impact of Generative AI on Critical Thinking. *CHI '25*. [https://doi.org/10.1145/3706598.3713778](https://doi.org/10.1145/3706598.3713778)
- Budzyń, K., et al. (2025). Endoscopist deskilling risk after exposure to artificial intelligence in colonoscopy. *Lancet Gastroenterology & Hepatology*. [https://doi.org/10.1016/S2468-1253(25)00133-5](https://doi.org/10.1016/S2468-1253(25)00133-5)
- University of Minnesota CEHD (2026). Expert consensus report: Ways generative AI can support and threaten learning in K-20 U.S. education. [링크](https://www.cehd.umn.edu/AI-expert-consensus-report-2026)

**B. 인지과학**
- Kirschner, P. A., Sweller, J., & Clark, R. E. (2006). Why minimal guidance during instruction does not work. *Educational Psychologist*, 41(2), 75–86. [https://doi.org/10.1207/s15326985ep4102_1](https://doi.org/10.1207/s15326985ep4102_1)
- Tricot, A., & Sweller, J. (2014). Domain-specific knowledge and why teaching generic skills does not work. *Educational Psychology Review*, 26, 265–283. [https://doi.org/10.1007/s10648-013-9243-1](https://doi.org/10.1007/s10648-013-9243-1)
- Sala, G., & Gobet, F. (2019). Near and far transfer in cognitive training: A second-order meta-analysis. *Collabra: Psychology*, 5(1), 18. [https://doi.org/10.1525/collabra.203](https://doi.org/10.1525/collabra.203)
- Gobet, F., & Sala, G. (2023). Cognitive training: A field in search of a phenomenon. *Perspectives on Psychological Science*. [https://doi.org/10.1177/17456916221091830](https://doi.org/10.1177/17456916221091830)
- Tetzlaff, L., Simonsmeier, B., Peters, T., & Brod, G. (2025). A cornerstone of adaptivity: A meta-analysis of the expertise reversal effect. *Learning and Instruction*, 98, 102142. [https://doi.org/10.1016/j.learninstruc.2025.102142](https://doi.org/10.1016/j.learninstruc.2025.102142)
- Simonsmeier, B. A., Flaig, M., Deiglmayr, A., Schalk, L., & Schneider, M. (2022). Domain-specific prior knowledge and learning: A meta-analysis. *Educational Psychologist*, 57(1). [https://doi.org/10.1080/00461520.2021.1939700](https://doi.org/10.1080/00461520.2021.1939700)
- Willingham, D. T. (2007). Critical thinking: Why is it so hard to teach? *American Educator*, Summer 2007. [PDF](https://www.aft.org/sites/default/files/media/2014/Crit_Thinking.pdf)
- Recht, D. R., & Leslie, L. (1988). Effect of prior knowledge on good and poor readers' memory of text. *Journal of Educational Psychology*, 80(1), 16–20. [https://doi.org/10.1037/0022-0663.80.1.16](https://doi.org/10.1037/0022-0663.80.1.16)

**C. 교실과 정책**
- Grissmer, D., et al. (2023). A Kindergarten Lottery Evaluation of Core Knowledge Charter Schools. EdWorkingPaper 23-755. [https://edworkingpapers.com/ai23-755](https://edworkingpapers.com/ai23-755)
- Smith, R., Snow, P., Serry, T., & Hammond, L. (2021). The role of background knowledge in reading comprehension: A critical review. *Reading Psychology*, 42(3). [https://doi.org/10.1080/02702711.2021.1888348](https://doi.org/10.1080/02702711.2021.1888348)
- Stockard, J., Wood, T. W., Coughlin, C., & Rasplica Khoury, C. (2018). The effectiveness of Direct Instruction curricula: A meta-analysis of a half century of research. *Review of Educational Research*, 88(4). [https://doi.org/10.3102/0034654317751919](https://doi.org/10.3102/0034654317751919)
- OECD (2018). *The Science of Teaching Science: An Exploration of Science Teaching Practices in PISA 2015*. [PDF](https://www.oecd.org/content/dam/oecd/en/publications/reports/2018/11/the-science-of-teaching-science_b00c65f8/f5bd9e57-en.pdf)
- McKinsey & Company (2017). How to improve student educational outcomes: New insights from data analytics. [링크](https://www.mckinsey.com/industries/education/our-insights/how-to-improve-student-educational-outcomes-new-insights-from-data-analytics)

**D. 교육과정 이론**
- Young, M., & Muller, J. (2013). On the powers of powerful knowledge. *Review of Education*, 1(3). [https://doi.org/10.1002/rev3.3017](https://doi.org/10.1002/rev3.3017)
- OECD (2019). *OECD Learning Compass 2030: Concept Note*. [PDF](https://www.oecd.org/content/dam/oecd/en/about/projects/edu/education-2040/concept-notes/OECD_Learning_Compass_2030_concept_note.pdf)
- 「역량기반 교육과정의 딜레마」 (2020). 『교육과정연구』, 38(4), 5–31. 한국교육과정학회. [KCI](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002667686)
