---
title: "가재코드 Autoresearch: 웹 리서치와 데이터 실험 병행"
date: 2026-10-16 00:10:32 +0900
categories: [소프트웨어개발, AI]
tags: [가재코드, Autoresearch, AI에이전트, 웹리서치, 데이터실험, PythonREPL, 오픈소스, 개발도구]
header:
  teaser: /assets/gajae-code-autoresearch-thumb.jpg
permalink: /post/gajae-code-autoresearch/
---
**Gajae-Code** 프로젝트의 **Autoresearch**는 단순한 웹 검색을 넘어, 웹 리서치와 데이터 실험을 통합해 최종 결론까지 도출하는 자율적인 연구 미션이다. 이 기능은 복잡한 질문에 대한 **방어 가능한 판정**을 제공하며, 개발 워크플로 내에서 의사 결정을 위한 핵심 증거를 확보한다. 단순한 코드 구현이 아닌, 정보 탐색과 검증에 초점을 맞춘다.

<figure>
<img src="/assets/gajae-code-autoresearch-thumb.jpg" alt="가재코드 Autoresearch: 웹 리서치와 데이터 실험 병행">
</figure>

## 가재코드의 리서치 미션: Autoresearch

`autoresearch`는 **Gajae-Code** (MIT 라이선스, 타입스크립트 기반 오픈소스 프로젝트)의 핵심 기능 중 하나다. 이 스킬은 목표 지향적인 연구 임무를 수행하며, 웹 탐색과 데이터 기반 실험을 교차하여 실행한다. 최종적으로는 구조화된 **최선의 판정**을 내놓는다.

판정은 `status`, `evidence[]`, `caveats[]`, `evaluator` 등으로 구성된다. 연구 미션의 결과물은 **탐색 결과**, **증거**, **실행 기록**, **판정**이며, 제품 코드를 생성하지는 않는다.

`autoresearch`는 `deep-interview`로 요청을 구체화하고 `ralplan`으로 계획을 세우며 `ultragoal`로 목표를 추적하는 과정에서, **선택적인 리서치 미션**으로 계획을 뒷받침해야 할 때 활성화한다. 이 스킬은 사용자가 `/skill:autoresearch "<research goal>"` 형태로 명시적으로 요청하거나, **방어 가능한 결론**이 필요한 연구 목표를 제시할 때 사용한다. 예를 들어 "이 데이터셋에 X가 유효한가?", "어떤 접근 방식이 가장 좋은 벤치마크 결과를 보이는가?", "두 릴리스 사이에 무엇이 달라졌는가?"와 같은 질문에 답을 찾는다.

반면, 단순한 정보 조회나 코드 구현이 목적인 경우에는 `ralplan`, `deep-interview` 같은 다른 스킬을 사용한다. 하나의 검색 요청으로 바로 답을 얻을 수 있는 상황에서는 `autoresearch`가 필요하지 않다.

## Autoresearch 미션 진행 방식

`autoresearch`는 두 가지 방식으로 미션을 시작한다. 첫째는 **Spec Intake** 방식이다. 미리 정의된 `deep-interview` 사양 파일을 `--spec` 플래그로 전달하면 추가 질문 없이 바로 미션을 시작한다. 이때 사양 파일에는 미션 모드(`autoresearch-mode: web`, `mixed`, `data`)가 명시되어야 한다. 이 선언이 없거나 유효하지 않으면 미션 시작은 실패한다. 둘째는 **Cold Intake** 방식으로, `gjc autoresearch "<goal>"`처럼 목표만 제시하는 방식이다. 이 경우, 연구를 시작하기 전에 목표, 제약 조건, 산출물 등을 명확히 하는 과정이 선행된다.

모든 미션은 `web`, `mixed`, `data` 중 하나의 **명시적 모드**를 갖는다. 데이터 파일이 작업 공간에 존재하더라도 모드를 명시하지 않으면 미션은 거부된다. 예를 들어 `web` 모드에서는 데이터 컨텍스트를 연결하지 않는다.

미션은 GJC의 **골 모드**와 연동하여 자율적으로 진행한다. 에이전트는 `goal` 도구를 호출하여 `autoresearch` 미션의 목표를 추적하며, 미션 아티팩트가 생성되면 `goal({"op":"create", ...})` 명령으로 목표를 설정한다. 이 목표는 **구조화된 판정**이 나올 때까지 에이전트의 자율적인 연속 루프를 유도한다.

미션은 크게 두 단계로 진행한다. **첫 번째 단계**는 **하네스 구축**이다. 기존 벤치마크 명령이나 연구 전용 하네스 아티팩트를 사용하여, 성공 시 0을 반환하고 비-0은 실패를 나타내는 실행 환경을 구성한다. 이때, 제품 코드의 수정은 허용하지 않는다. **두 번째 단계**는 **반복 실험**이다. `baseline`, `keep`, `discard` 원칙에 따라 실험을 반복하며 모든 실행 기록을 유지한다. 주 지표가 개선되면 `keep`, 퇴보하거나 유지되면 `discard`, 실패하면 `crash`로 기록한다.

웹 리서치와 데이터 실험은 분리된 트랙이 아니며, 미션 내에서 자유롭게 혼합된다. 예를 들어 웹에서 찾은 정보가 다음 실험을 유도하고, 실험 결과가 새로운 웹 검색으로 이어질 수 있다. 모든 증거는 동일한 미션 원장과 최종 판정에 반영된다.

## 미션 결과와 마무리

`autoresearch` 미션은 단일의 **미션 수준 구조화 판정**으로 종료한다. 이 판정에는 `status` (구조화된 데이터), `evidence[]`, `caveats[]`, 그리고 판정을 발행한 `evaluator`의 신원이 포함된다. 기본적으로는 미션 에이전트가 자체적으로 판정을 발행하지만, 선택적으로 **비평가(Critic)** 패스를 거쳐 별도의 `evaluator` 신원(`critic_receipt`)을 기록할 수 있다.

**비평가**는 미션의 목표, 산출물, 제약 조건에 대해 판정을 검토하는 읽기 전용 역할이다. 비평가는 코드나 파일을 수정하거나 실험을 실행하지 않으며, 단지 제공된 증거가 판정을 뒷받침하는지, 주의사항이 정직하게 명시되었는지 등을 확인한다. **불확실한 판정**(`status.disposition: "inconclusive"`)도 유효하며, 이 경우 미션은 후속 조치를 위해 열린 상태로 유지된다.

미션을 종료하는 방법은 두 가지다. 첫째, 다른 스킬(`ralplan`, `deep-interview`, `ultragoal`)로 **핸드오프**한다. 이때 미션의 비-종료 목표는 드롭되고 새로운 워크플로로 전환된다. 둘째, `gjc autoresearch clear` 명령으로 미션 아티팩트와 작업 세트를 **최종 정리**한다. `status.disposition: "conclusive"` 판정이 내려진 미션만 골 모드 완료 후 자동으로 정리되며, `inconclusive` 판정은 수동으로 정리해야 한다.

모든 미션 상태와 기록은 `.gjc/_session-{sessionid}/autoresearch/` 경로 아래에 지속적으로 저장된다. 여기에는 미션 아티팩트, JSONL 원장, 세션 범위의 실행 기록 등이 포함된다. 이 파일들을 직접 수정하는 것은 허용되지 않으며, `gjc autoresearch` 명령을 통해서만 접근해야 한다.

## 연구 계획과 증거 관리: Research Plan Ledger

`autoresearch` 미션의 효율적인 진행을 위해 **연구 계획 항목**(`ResearchPlanItem`)과 **증거 원장**(`ResearchEvidenceEntry`, `ResearchLedgerVerdict`) 스키마를 정의한다. 이는 단순한 체크리스트 이상의 강력한 계획 계약을 제공한다.

아래 표는 연구 계획 및 증거 관리의 주요 스키마와 그 역할을 나타낸다.

| 스키마 이름 | 주요 필드 | 설명 |
|:---|:---|:---|
| `ResearchPlanItem` | `claim`, `confidence`, `unknowns`, `evidenceNeeded`, `counterexampleQueries`, `sourceConflictPolicy`, `dropCondition`, `verifierChecks` | 연구할 클레임, 불확실성, 필요한 증거, 반례, 소스 충돌 처리 방안 등을 정의하는 계획 항목이다. |
| `ResearchEvidenceEntry` | `claim`, `source`, `confidence`, `verdict` (`support`, `contradict`, `uncertain`), `notes` | 특정 클레임에 대한 증거의 출처, 확신도, 증거의 판정(지지, 반박, 불확실)을 기록하는 항목이다. |
| `ResearchLedgerVerdict` | `claim`, `finalVerdict` (`accepted`, `rejected`, `uncertain`), `survivingSources`, `rejectReason`, `unresolvedUnknowns` | 여러 증거를 종합하여 클레임에 대한 최종 판정, 채택된 증거, 거부 사유 등을 종합적으로 나타내는 원장 판정이다. |

`ResearchPlanItem`은 연구 시작 전 계획을 명확히 하고, `ResearchEvidenceEntry`는 실제 연구 과정에서 수집된 정보를 기록한다. 마지막으로 `ResearchLedgerVerdict`는 이 모든 정보를 기반으로 최종적인 클레임의 유효성을 판단한다. 이러한 체계는 연구의 투명성과 재현성을 높인다.

이러한 구조는 플래너가 연구 항목을 명확히 하고, 워커가 독립적인 증거를 수집하며, 검증자가 모순된 정보나 불확실성을 체계적으로 처리하여 최종 답변의 신뢰성을 높이도록 돕는다. 예를 들어, "모델 X가 생산 환경에서 지연 시간을 30% 줄인다"는 클레임에 대해 생산과 유사한 벤치마크 증거와 함께, 장기 워크로드에서 회귀가 발생했다는 **반례 증거**가 있다면 해당 클레임은 거부된다.

## 파이썬 REPL: Autoresearch의 실행 엔진

`autoresearch`가 데이터 실험을 수행할 때 핵심적인 도구가 바로 **Persistent Python REPL**이다. 이는 `eval` 도구를 통해 제공되며, `packages/coding-agent` 내의 파이썬 실행 스택을 활용한다. 이 시스템은 Jupyter나 추가 `pip` 의존성 없이 순수 **Python 3.8+ 인터프리터**만으로 작동한다. `runner.py`가 IPython의 MIME-번들 디스패치를 재구현하여 다양한 리치 디스플레이 출력을 지원한다.

각 파이썬 커널은 `python -u <runner.py>` 명령어로 실행되는 단일 서브프로세스다. 이 커널은 세션 동안 지속적으로 재사용되며, 변수, 임포트, 로드된 데이터가 호출 간에 유지된다. 이를 통해 복잡한 데이터 분석이나 실험 환경을 일관되게 유지한다. `gjc autoresearch clear` 명령은 `autoresearch`의 상태만 정리하며, 파이썬 커널은 `python` 도구의 `clear` 액션을 통해서만 리셋된다.

파이썬 REPL은 `%pip`, `%cd`, `%timeit` 등 **IPython 스타일 매직 명령어**를 지원한다. 이 명령어들은 내부적으로 일반 파이썬 호출로 변환되어 실행된다. `%%bash`나 `!cmd` 같은 셸 명령어도 활용하여 환경과의 상호작용을 가능하게 한다.

실행 환경은 `PATH`, `HOME` 같은 기본 변수와 `LC_`, `XDG_`, `GJC_` 접두사를 가진 변수만 허용하는 화이트리스트 방식으로 필터링한다. OpenAI, Anthropic, Gemini 등의 API 키는 보안을 위해 자동으로 제거한다. 런타임은 활성 가상 환경(venv), `~/.gjc/python-env` 관리형 venv, 또는 시스템 `PATH`의 `python`/`python3` 순으로 선택된다.

`eval` 도구의 파이썬 백엔드는 기본 30초, 최대 600초의 타임아웃을 지원한다. 실행 중 문제가 발생하면 `SIGINT` 시그널로 `KeyboardInterrupt`를 발생시켜 실행을 취소한다. 만약 5초 내에 응답이 없으면 커널을 종료하고 새로운 커널을 시작한다. **대화형 표준 입력(`input()`)은 지원하지 않는다.** 출력은 `stdout`, `stderr`뿐만 아니라 `Matplotlib` 그래프를 PNG 이미지로 변환하여 보여주는 등 다양한 **리치 디스플레이**를 포함한다.

## 출처
- C:/Users/windo/AppData/Local/Temp/claude/C--Users-windo-Desktop-03-------Github-Desktop-tigerjk9-github-io/4be0d2c9-c078-45ed-9c1c-6560eafe202d/scratchpad/b2/in/gajae-autoresearch.md
