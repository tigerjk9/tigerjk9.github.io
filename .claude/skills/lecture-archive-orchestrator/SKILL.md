---
name: lecture-archive-orchestrator
description: "강의자료 zip을 tigerjk9.github.io _lectures/ collection으로 자동 큐레이션하는 5명 에이전트 팀. 트리거: '강의자료 큐레이션', 'lecture archive', '강의자료 변환', '기능 페이지 생성'. 후속 작업: '--rerun parser|curator|builder'."
argument-hint: "<zip-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright] [--rerun parser|curator|builder]"
---

# Lecture Archive Orchestrator

강의자료 zip 한 묶음(slides·instructor-notes·handout·labs·기능 카탈로그)을 tigerjk9.github.io 블로그의 `_lectures/` Jekyll collection으로 자동 큐레이션하는 5명 에이전트 팀.

## Input

```
$ARGUMENTS = "<zip-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright] [--rerun parser|curator|builder]"
```

`$ARGUMENTS`가 비어 있으면 zip 경로를 먼저 사용자에게 물어본다.

---

## Phase 0 — 컨텍스트 확인

`$ARGUMENTS`에서 `zip_path`와 옵션을 파싱한다.

```python
# 예시 파싱
zip_path = args[0]             # 필수
slug     = --slug 값 or None   # 생략 시 orchestrate.py가 zip 파일명에서 추론
dry_run  = --dry-run 포함 여부
no_push  = --no-push 포함 여부
skip_pw  = --skip-playwright 포함 여부
rerun    = --rerun 값 or None  # "parser" | "curator" | "builder"
```

`--rerun`이 없으면 Phase 1부터 전체 실행. `--rerun parser`이면 parse_slides 단계부터 재실행.

---

## Phase 1 — orchestrate.py 실행 (zip 해제·brief.yml 생성)

```powershell
python -m scripts.lecture_archive.orchestrate <zip_path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright]
```

성공 시 `_workspace/<slug>/brief.yml`이 생성된다. 실패하면 에러를 사용자에게 보고하고 중단.

`brief.yml` 내용 확인:
- `slug` — 강의 식별자 (URL 영구 고정, 변경 불가)
- `atom_mode` — `feature_catalog | section_heading | slide_group`
- `assets` — 탐색된 자산 경로 목록

---

## Phase 2 — 팀 구성

```python
TeamCreate(
  team_name=f"lecture-archive-{slug}",
  members=[
    {"name": "inventory",  "subagent_type": "general-purpose", "model": "opus"},
    {"name": "parser",     "subagent_type": "executor",        "model": "opus"},
    {"name": "curator",    "subagent_type": "general-purpose", "model": "opus"},
    {"name": "builder",    "subagent_type": "executor",        "model": "opus"},
    {"name": "reviewer",   "subagent_type": "executor",        "model": "opus"},
  ]
)
```

팀 리더는 `reviewer`. 나머지 4명은 단일 패스 (재호출 권한 없음). reviewer만 builder를 1회 재호출할 수 있다.

---

## Phase 3 — 파이프라인 실행

### T1: inventory (단독)

**프롬프트 핵심:**
```
_workspace/<slug>/00_input/ 디렉토리 전체를 탐색하고
_workspace/<slug>/01_inventory.md를 작성하라.

포함 내용:
- 자산 파일 목록 (경로·크기·종류)
- slides.html 슬라이드 총 수 (Reveal.js <section> 태그 수)
- instructor-notes 섹션 헤딩 목록 (## 로 시작하는 줄)
- 기능 카탈로그(07_feature_ideas.md) 있으면 기능 수·F-NNN 목록
- brief.yml의 atom_mode 확인 및 검증

완료 후 SendMessage(to="curator", body="inventory done: {inventory_summary}")
```

### T2: parser (T1 완료 후)

**프롬프트 핵심:**
```
brief.yml의 slides_html 경로에서 슬라이드를 추출하라.

1. BeautifulSoup으로 <section> 파싱 → 텍스트·코드블록·data-* 속성 추출
2. --skip-playwright가 아니면:
   python -m scripts.lecture_archive.parse_slides <slides_html> --output _workspace/<slug>/02_slides.json
3. _workspace/<slug>/02_slides.json 확인

완료 후 SendMessage(to="curator", body="parser done: N slides extracted")
```

`--skip-playwright`이면 기존 `_workspace/<slug>/slides/` PNG를 그대로 사용.

### T3: curator (T1·T2 완료 후)

**프롬프트 핵심:**
```
다음 입력을 종합해 기능별 마크다운 페이지를 생성하라:
- 01_inventory.md
- 02_slides.json
- instructor-notes.v2.md (있으면)
- labs.md (있으면)
- 07_feature_ideas.md (있으면)
- brief.yml의 atom_mode

atom_mode == "feature_catalog":
  각 F-NNN 기능에 대해 _workspace/<slug>/03_features/<feature-slug>.md 생성
  슬라이드-기능 매핑: strict → heading → Gemini 3단계 폴백 적용

atom_mode == "section_heading":
  instructor-notes의 ## 헤딩 1개 = 1 페이지

각 기능 페이지 구조:
---
layout: lecture
lecture_slug: <slug>
feature_id: F-NNN
title: "<기능명>"
track: basic|advanced
permalink: /lectures/<slug>/<feature-slug>/
---

## 정의
...

## 핵심 동작
...

## 사용법
```powershell
...
```

## 관련 슬라이드
(슬라이드 PNG 임베드 + 추출 텍스트)

## 강사 멘트
(instructor-notes 발췌)

## 실습
(labs 발췌, 해당 시)

## 시사점
...

---
마지막으로 _workspace/<slug>/03_features/_slug_map.yml 생성:
features:
  - feature_id: F-035
    feature_slug: claudemd
    title: "CLAUDE.md"
    track: basic
    mapping_method: strict|heading|llm
  ...

★ _slug_map.yml 완성 후 반드시 멈추고 사용자 승인 대기.
SendMessage(to="reviewer", body="slug_gate: 사용자 slug 검토 게이트 대기 중")
사용자에게: "_workspace/<slug>/03_features/_slug_map.yml를 검토하고 '슬러그 승인'을 입력하세요."
```

### 슬러그 게이트 (사용자 명시 승인 필요)

curator가 `_slug_map.yml`을 출력한 뒤 **멈추고** 사용자 입력을 기다린다.

승인 키워드: `"슬러그 승인"`, `"slug 승인"`, `"approve slugs"`

URL은 영구적이므로 한 번에 확정한다. 사용자가 yml을 직접 편집하고 승인해도 된다.

### T4: builder (slug 게이트 승인 후)

**프롬프트 핵심:**
```
_workspace/<slug>/03_features/ 의 마크다운들을 Jekyll collection으로 배포하라.

python -m scripts.lecture_archive.build_site <slug> [--dry-run] [--no-push]

추가로:
- _data/lectures.yml에 강의 항목 append (중복 체크)
- assets/lectures/<slug>/ 에 slides.html·handout.html·cover.jpg 복사
- cover.jpg 없으면 Pillow로 1200×630 생성 (Malgun Gothic 필수, 인물 사진 금지)
- de-institutionalization: 기관명(KIST 등) → 청중명(교육자) 치환
  치환 시 긴 표현 먼저 처리

완료 후 SendMessage(to="reviewer", body="builder done")
```

### T5: reviewer (팀 리더, T4 완료 후)

**프롬프트 핵심:**
```
체크리스트 12개를 검증하라:

[ ] 1. bundle exec jekyll build 성공
[ ] 2. /lectures/ 인덱스 빌드 OK
[ ] 3. /lectures/<slug>/ 허브 빌드 OK
[ ] 4. /lectures/<slug>/<feature-slug>/ N장 모두 빌드 OK
[ ] 5. 기능 페이지 모두 슬라이드 PNG 1장 이상 임베드 OK
[ ] 6. 슬라이드 ↔ 기능 매핑 통계 (strict %·heading %·llm %·미매핑)
[ ] 7. llm 분류·미매핑 슬라이드 목록 → 강사 검증 권장 보고
[ ] 8. 격리 검증 — site.categories·site.tags에 강의 항목 0건
[ ] 9. graph-data.json 변경 0건
[ ] 10. _data/navigation.yml "강의자료" 1줄 확인
[ ] 11. assets/lectures/<slug>/ 용량 합산 50MB 이하
[ ] 12. permalink N+2개 모두 unique·격리 패턴

이슈 발견 시 builder에게 SendMessage로 재호출 (최대 1회).
이슈 없으면 04_review.md 작성 후 완료 보고.
```

---

## Phase 4 — 정리·커밋·푸시

```
1. 04_review.md 요약 사용자에게 보고
2. TeamDelete
3. _workspace/<slug>/ 보존 (재실행·후속 수정용)
4. --no-push 아니면:
   git add _lectures/<slug>/ assets/lectures/<slug>/ _data/lectures.yml
   git commit -m "Add: <강의명> 강의자료 아카이브 — N 기능·M 슬라이드"
   git fetch origin && git rebase origin/main --autostash && git push origin main
```

---

## 후속 작업 패턴

| 시나리오 | 명령 |
|---------|------|
| 슬라이드 텍스트만 재추출 | `/lecture-archive <slug> --rerun parser` |
| 기능 페이지 재생성 | `/lecture-archive <slug> --rerun curator` |
| 사이트 빌드만 재실행 | `/lecture-archive <slug> --rerun builder` |
| llm 분류 슬라이드 수동 수정 | `_workspace/<slug>/02_slides.json` 직접 편집 후 `--rerun curator` |

---

## 알려진 제약

- Playwright Chromium 첫 다운로드 ~150MB. 망분리 환경은 `--skip-playwright`
- Subagent 환경에 `bundle`·`ruby` PATH 없음. `bundle exec jekyll build`는 사용자 측에서 직접 실행
- 한 강의 변환 예상 시간: 10~15분 + slug 검토 시간
- cover.jpg에 실제 인물 사진 절대 사용 금지 (초상권). Pillow 생성 이미지로 대체
