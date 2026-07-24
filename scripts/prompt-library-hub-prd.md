# 교육자용 큐레이션 프롬프트 라이브러리 허브 — PRD (설계안)

> 상태: **설계(구현 전)**. 2026-07-24 작성. prompts.chat 반영 Phase 3.
> 이 문서는 기획만 담는다. 구현은 별도 승인 후 진행한다.

## 1. 목적·배경

prompts.chat(옛 awesome-chatgpt-prompts, GitHub 16만+ 스타)은 2,000+ 프롬프트를
**CC0 1.0 퍼블릭 도메인**으로 공개한다 — 출처 표기 의무 없이 번안·재배포 가능.
그러나 원본은 (1) 대부분 영어이고 (2) 범용(코드·마케팅·이미지)이라, 한국 교사·교육
관계자가 곧바로 쓰기 어렵다.

**허브의 가치 = 큐레이션.** 2,000개를 그대로 옮기는 것이 아니라, 교육 실무에 실제로
쓰이는 것만 골라 **한국어로 번안하고 교육 맥락 예시를 붙인** 소수 정예 라이브러리를
만든다. 블로그의 기존 자산(research 허브·lectures 허브)과 같은 "격리형 큐레이션 허브"
패턴을 재사용한다.

## 2. 핵심 원칙

- **덤프 금지, 큐레이션 우선.** 초기 40~80개 목표. 교육 실무 카테고리로 재분류:
  수업 설계 / 평가·문항 / 학생 피드백 / 학부모·동료 소통 / 행정·공문 / 자료 조사·요약 /
  이미지·시각자료 프롬프트.
- **번역이 아닌 번안.** 원문 의도를 살리되 한국 학교 맥락 예시로 재서술(/paraph 철학과 동일).
  원문 프롬프트 링크를 함께 제공해 대조 가능하게.
- **격리 모드 필수.** 페이지 front matter에 `categories`/`tags` 없음 → 사이드바·지식그래프·
  카테고리/태그 페이지·검색에 침투 0건 (research.md 선례). 검증은 빌드 전후
  `_site/categories`·`_site/tags` 카운트 동일.
- **저작권.** CC0라 표기 의무는 없으나, 신뢰를 위해 "출처: prompts.chat (CC0 1.0)"를
  허브 상단과 카드에 명시. 우리 번안분은 블로그 기존 라이선스 정책을 따른다.

## 3. 데이터 파이프라인

`scripts/build_prompt_library.py` (신규):

1. **수집**: prompts.chat CC0 원본(`github.com/f/prompts.chat`의 `prompts.csv`/`PROMPTS.md`)
   fetch. 저장소 클론 없이 raw URL 요청(기업 SSL 우회 `verify=False` 기존 패턴).
2. **선별**: 교육 실무 관련 프롬프트를 키워드 + 수동 화이트리스트로 필터(초기엔 사람이 고른
   ID 목록 기반 — 자동 분류는 오탐 많음).
3. **번안**: 선별분을 Gemini로 한국어 번안 + 교육 예시 1줄 첨부(기존 `.env` GEMINI_API_KEY
   재사용). 번안 결과는 **텍스트 해시 기반 증분 캐시**(research 임베딩 패턴)로 재실행 시
   신규분만 API 호출.
4. **출력**: `assets/prompt-library.json` — 스키마
   `[{id, category, title_ko, prompt_ko, prompt_en, tags[], source_url}]`.
   스키마는 페이지 JS와 단일 계약(바꾸면 양쪽 함께 수정).

## 4. 페이지·UI 설계

- **파일**: `_pages/prompt-library.md`, `permalink: /prompts/`, layout `default`
  (사이트 내비·푸터 유지, 저자 사이드바 없음 — research.md와 동일).
- **스코핑(CRITICAL)**: 모든 CSS 셀렉터에 컨테이너 ID `#pl-app` 프리픽스.
  `main.scss`의 `html[data-theme="light"] a{color:#0078c8}`(특이성 0,1,1)가 버튼형 앵커
  흰 글자를 덮는 함정 방어(research.md·ask.md 선례). 스크립트는 `{% raw %}` 래핑.
- **테마 대응**: 다크 기본 + `html[data-theme="light"] #pl-app` 오버라이드.
- **레이아웃 default 함정**: `sidebar-toggle.js`의 플로팅 ☰/✕ 버튼이 뜨는지 확인
  (`.sidebar` 부재 시 조기 반환 로직 이미 있음, 회귀만 확인). 또는 **`tools/` 정적 단독
  HTML 패턴**(front matter 없는 `tools/prompt-library/index.html`)으로 만들면 테마 CSS·
  토글 JS가 로드되지 않아 함정이 원천 차단됨 — 대안으로 검토.
- **UI 요소**(research 허브 UX 재사용):
  - 교육 카테고리 탭 + 태그 칩 AND 필터 + 키워드 검색(제목·본문)
  - 카드: 제목_ko / 한 줄 설명 / **[복사] 버튼**(prompt_ko 클립보드) / 원문 토글(prompt_en) /
    prompts.chat 원문 링크
  - 인라인 확장, 마크다운 라이트 렌더

## 5. 격리 회귀 검증

```bash
bundle exec jekyll build && ls _site/categories | wc -l && ls _site/tags | wc -l
```
추가 전후 카운트 동일해야 함. `_config.yml`에 데이터 JSON은 빌드 산출물이라 exclude 불필요
(assets/ 정적 서빙).

## 6. 구현 단계 (승인 후)

1. **A. 데이터**: 화이트리스트 초안(40~80개 ID) 선정 → `build_prompt_library.py` →
   `assets/prompt-library.json`. **화이트리스트 선정은 주인장 편집 판단 필요(게이트)**.
2. **B. 페이지**: `_pages/prompt-library.md` + `#pl-app` 스코프 스타일/스크립트.
3. **C. 내비**: `_data/navigation.yml`에 "프롬프트" 추가 여부 결정.
4. **D. 검증**: 격리 회귀 + 라이트/다크 + 모바일(스크래치패드 Edge 헤드리스 캡처 패턴).

## 7. 열린 결정사항 (주인장 승인 필요)

- 초기 큐레이션 규모(40 / 60 / 80개)와 카테고리 최종안.
- Jekyll 인사이트 페이지 vs `tools/` 정적 단독 HTML 중 택1.
- 번안 자동(Gemini) vs 반자동(초안 후 수동 교정) 수준.
- 내비게이션 노출 여부, permalink(`/prompts/` 제안).
- prompts.chat 외 CC0/오픈 프롬프트 소스 추가 편입 여부.
