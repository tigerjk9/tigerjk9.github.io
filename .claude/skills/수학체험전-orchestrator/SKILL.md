---
name: 수학체험전-orchestrator
description: >
  초등학교 5학년 수학체험전 부스 운영계획서를 처음부터 끝까지 완성하는 오케스트레이터.
  사전 조사 → 부스 설계 → 계획서 집필 → 심사 시뮬레이션 → 합격 판정 파이프라인 자동 실행.
  "수학체험전", "수학 부스", "운영계획서", "수학 탐구 부스", "체험전 계획", "수학 활동 계획",
  "부스 선발", "체험전 심사", "수학체험전 다시", "계획서 수정", "부스 재설계" 키워드 시 반드시 사용.
---

# 수학체험전 부스 운영계획서 오케스트레이터

초등 5학년 수학체험전 부스 운영 선발을 목표로,
사전 조사부터 심사 합격 계획서까지 4명의 전문 에이전트가 파이프라인으로 협업한다.

## 실행 모드: 서브 에이전트 (파이프라인)

각 Phase는 독립 서브 에이전트로 실행되며, 파일 기반으로 중간 산출물을 전달한다.
User gate(사용자 확인 지점)가 Phase 2와 Phase 3 사이에 존재한다.

---

## Phase 0: 컨텍스트 확인

오케스트레이터 시작 시 기존 산출물 여부를 확인한다.

```
_workspace/ 디렉토리 존재 여부 확인:
- 없음 → 초기 실행 (Phase 1부터 시작)
- 있음 + 사용자가 수정 요청 → 부분 재실행 (해당 Phase부터 재시작)
- 있음 + 사용자가 새 주제 요청 → _workspace_prev/ 로 이동 후 신규 실행
```

**부분 재실행 판별**:
- "계획서만 수정해줘" → Phase 3(집필)부터
- "부스 설계 다시" → Phase 2(설계)부터
- "검토만 다시 해줘" → Phase 4(심사)만
- "처음부터" → Phase 1부터

---

## Phase 1: 대회 정보 수집 (User Interview)

서브 에이전트 실행 전, 사용자에게 다음 정보를 확인한다.

### 필수 확인 항목

| 항목 | 질문 | 기본값(미제공 시) |
|------|------|----------------|
| 대회명 | 참가할 대회의 정식 명칭은? | "교육청 수학체험전" 가정 |
| 주최 수준 | 교내/교육청/지역/전국? | 교육청 수준 가정 |
| 심사 양식 | 계획서 양식 파일이 있는가? | 표준 6섹션 구성 적용 |
| 주제 선호 | 관심 있는 수학 주제가 있는가? (없으면 추천 요청) | 연구 결과로 추천 |
| 예산 규모 | 사용 가능한 예산은? | 8만원 이내 설계 |
| 제출 기한 | 계획서 제출 기한은? | 기한 압박 없음 가정 |
| 팀 인원 | 운영 학생 수는? | 4~6명 가정 |
| 부스 시간 | 부스 운영 시간은? (예: 각 팀 10분, 2시간 운영 등) | 총 2시간 운영 가정 |

최소 "대회명"과 "주제 선호 여부"만 확인해도 조사를 시작할 수 있다.
나머지는 기본값으로 진행하고 보고서에 "[가정]" 표시.

---

## Phase 2: 사전 조사 (math-fair-researcher)

**실행 모드**: 서브 에이전트
**에이전트**: `math-fair-researcher` (model: opus)

```
Agent(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
  [math-fair-researcher 에이전트로서 작업]
  에이전트 정의 파일: .claude/agents/math-fair-researcher.md 를 읽고 역할과 원칙을 이해한다.
  
  입력 정보:
  - 대회명: {대회명}
  - 주최 수준: {수준}
  - 학년: 초등 5학년
  - 사용자 선호 주제: {선호_주제 또는 "없음(추천 요청)"}
  
  작업:
  1. 대회 특성 분석 (웹 검색 활용)
  2. 초등 5학년 수학 교육과정 매핑
  3. 우수 사례 3개 발굴
  4. 추천 주제 5선 도출 (선호 주제가 있으면 해당 주제 포함)
  
  출력: _workspace/01_research.md 저장
  """
)
```

**완료 기준**: `_workspace/01_research.md` 생성 확인

---

## [User Gate 1] 주제 선택

`_workspace/01_research.md`의 추천 주제 5선을 사용자에게 제시한다.

```
📊 사전 조사 완료!

추천 주제 5선:
1. [주제명] — [한 줄 설명]
2. [주제명] — [한 줄 설명]
3. [주제명] — [한 줄 설명]
4. [주제명] — [한 줄 설명]
5. [주제명] — [한 줄 설명]

어떤 주제로 진행할까요?
번호로 선택하거나, 직접 주제를 알려주세요.
```

사용자가 선택하면 Phase 3 진행. 선택 거부 또는 새 주제 제안 시 math-fair-researcher에게 추가 조사 요청.

---

## Phase 3: 부스 설계 (math-fair-booth-designer)

**실행 모드**: 서브 에이전트
**에이전트**: `math-fair-booth-designer` (model: opus)

```
Agent(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
  [math-fair-booth-designer 에이전트로서 작업]
  에이전트 정의 파일: .claude/agents/math-fair-booth-designer.md 를 읽고 역할과 원칙을 이해한다.
  
  입력 파일: _workspace/01_research.md 읽기
  사용자 선택 주제: {선택된_주제}
  예산: {예산}원 이내
  팀 인원: {인원}명
  부스 운영 시간: {운영시간}
  
  작업:
  1. 부스명 설계
  2. STEP별 활동 상세 설계 (3~4 STEP, 총 10~15분)
  3. 준비물·예산 산출
  4. 안전관리 매트릭스 작성
  5. 공간 배치도 및 역할 분담
  6. 디지털 증폭 방안 (3조건 통과 시만)
  
  출력: _workspace/02_booth-design.md 저장
  """
)
```

**완료 기준**: `_workspace/02_booth-design.md` 생성 확인

---

## [User Gate 2] 부스 설계 확인 (선택적)

부스 설계 결과를 간략히 요약하여 사용자에게 보고한다.

```
🎪 부스 설계 완료!

부스명: [이름]
핵심 활동: [한 줄 요약]
STEP 수: N개 / 총 체험 시간: N분
예산: 약 N원

계획서 작성을 시작할까요? (Y / 수정 요청 있으면 알려주세요)
```

별도 수정 요청이 없으면 즉시 Phase 4로 진행.

---

## Phase 4: 계획서 집필 (math-fair-proposal-writer)

**실행 모드**: 서브 에이전트
**에이전트**: `math-fair-proposal-writer` (model: opus)

```
Agent(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
  [math-fair-proposal-writer 에이전트로서 작업]
  에이전트 정의 파일: .claude/agents/math-fair-proposal-writer.md 를 읽고 역할과 원칙을 이해한다.
  
  입력 파일:
  - _workspace/01_research.md 읽기 (교육과정 연계, 심사 기준)
  - _workspace/02_booth-design.md 읽기 (설계 전체)
  
  대회 공식 양식: {양식_경로 또는 "없음"}
  
  작업:
  1. 30초 법칙을 염두에 두고 개요 섹션 작성
  2. 이론적 배경 (수학 개념 + 수학사 + 오개념 교정)
  3. 활동 계획 (STEP 표 + 준비물 표 + 공간 배치)
  4. 운영 계획 (역할 분담 + 안전관리)
  5. 기대 효과 (수치·구체적 변화 명시)
  6. 참고 자료
  
  문체 규칙: 단정체("~이다/한다"), 수치 명시, 표 우선
  
  출력: _workspace/03_proposal-draft.md 저장
  """
)
```

**완료 기준**: `_workspace/03_proposal-draft.md` 생성 확인

---

## Phase 5: 심사 시뮬레이션 (math-fair-judge-reviewer)

**실행 모드**: 서브 에이전트
**에이전트**: `math-fair-judge-reviewer` (model: opus)

```
Agent(
  subagent_type: "general-purpose",
  model: "opus",
  prompt: """
  [math-fair-judge-reviewer 에이전트로서 작업]
  에이전트 정의 파일: .claude/agents/math-fair-judge-reviewer.md 를 읽고 역할과 원칙을 이해한다.
  
  입력 파일: _workspace/03_proposal-draft.md 읽기
  
  작업:
  1. 7축 채점 (가중 합산)
  2. 30초 법칙 시뮬레이션
  3. "왜 이 수학인가" 테스트
  4. 오개념·리스크 탐지
  5. PASS/REVISE/REWRITE 판정
  6. 수정 요청 목록 (REVISE 시) 또는 재설계 근거 (REWRITE 시)
  
  출력: _workspace/04_review.md 저장
  """
)
```

**완료 기준**: `_workspace/04_review.md` 생성 확인

---

## Phase 6: 판정 처리

`_workspace/04_review.md`의 판정을 읽어 분기한다.

### PASS 판정 시

```
✅ 심사 통과! 계획서가 선발 가능한 수준입니다.

최종 계획서 위치: _workspace/03_proposal-draft.md

다음 단계:
- HWPX 파일 변환이 필요하면: /hwpx-skill 실행 요청
- 추가 수정이 있으면: 수정 내용 알려주세요 (계획서 재작성)
- 계획서를 블로그 포스트로 정리하려면: /paraph 활용 가능
```

### REVISE 판정 시

수정 목록을 사용자에게 요약 보고 후, `math-fair-proposal-writer`를 재실행한다.
이때 프롬프트에 수정 요청 목록을 포함한다.
수정 후 `math-fair-judge-reviewer`를 재실행하여 재검토한다.
**재검토 루프 최대 3회** — 3회 후에도 PASS 미달 시 사용자에게 보고.

### REWRITE 판정 시

사용자에게 재설계 근거를 보고하고 다음을 확인한다:

```
❌ 부스 개념 재설계가 필요합니다.

주요 이유: [judge-reviewer의 재설계 근거 요약]

선택지:
A. 현재 주제로 부스 설계를 전면 재설계 (Phase 3으로 돌아감)
B. 다른 주제로 변경 (Phase 2 추천 주제 중 선택)
C. 계획서만 수정 재시도 (REVISE 처리로 전환)

어떻게 하시겠어요?
```

---

## 데이터 흐름

```
Phase 1 (User Interview)
    ↓ [대회 정보]
Phase 2 (Researcher) → _workspace/01_research.md
    ↓ [User Gate 1: 주제 선택]
Phase 3 (Booth Designer) → _workspace/02_booth-design.md
    ↓ [User Gate 2: 설계 확인 - 선택적]
Phase 4 (Proposal Writer) → _workspace/03_proposal-draft.md
    ↓
Phase 5 (Judge Reviewer) → _workspace/04_review.md
    ↓
Phase 6 (판정 처리)
  PASS → 최종 출력
  REVISE → Phase 4 재실행 (최대 3회)
  REWRITE → Phase 2 또는 3 재실행
```

---

## 에러 핸들링

| 상황 | 처리 방법 |
|------|---------|
| _workspace 파일 생성 실패 | 에이전트에게 재실행 요청, 2회 실패 시 사용자 보고 |
| 웹 검색 결과 없음 | 교육과정 문서 기반으로 대체, "[검색 실패]" 표시 |
| 사용자 응답 없음 | 기본값으로 진행하고 "[기본값 적용]" 표시 |
| REVISE 루프 3회 초과 | 사용자에게 보고, 수동 수정 안내 |
| 양식 파일 읽기 실패 | 표준 6섹션 구성으로 대체 |

---

## 테스트 시나리오

### 시나리오 1 (정상 흐름)
```
입력: "수학체험전 계획서 만들어줘. 교육청 수준이고 주제는 없어."
기대: Phase 1 → 2 → User Gate → 3 → User Gate → 4 → 5 → PASS
산출: _workspace/03_proposal-draft.md (완성 계획서)
```

### 시나리오 2 (REVISE 루프)
```
입력: "비와 비율 주제로 수학체험전 계획서"
기대: ... → Phase 5 REVISE → Phase 4 재실행 → Phase 5 PASS
산출: 수정된 계획서
```

### 시나리오 3 (부분 재실행)
```
입력: "계획서 2섹션 이론적 배경만 다시 써줘"
기대: Phase 0 컨텍스트 확인 → Phase 4만 부분 재실행
산출: 수정된 _workspace/03_proposal-draft.md
```
