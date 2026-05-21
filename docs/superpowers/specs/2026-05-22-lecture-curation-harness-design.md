---
title: 강의자료 큐레이션 하네스 디자인 스펙
slug: lecture-curation-harness-design
date: 2026-05-22
status: draft
authors:
  - 김진관 (닷커넥터)
related:
  - kist-claude-code-workshop (첫 사례 입력)
  - kist-lecture-orchestrator (제작 하네스, 참조 패턴)
---

# 강의자료 큐레이션 하네스 디자인 스펙

## 요약

황민호 수석의 KIST Claude Code 워크숍 자료(zip 묶음 — slides·instructor-notes·handout·labs·22 기능 카탈로그)를 첫 사례로, **강의자료 zip 한 묶음을 tigerjk9.github.io 블로그의 `_lectures/` collection으로 자동 큐레이션하는 5명 에이전트 하네스**를 설계한다. 산출물은 강의 허브 1장과 기능 페이지 N장(KIST의 경우 22장), 슬라이드 PNG·텍스트 추출본, 핸드아웃 PDF로 구성된다. 블로그의 기존 `_posts` 흐름·사이드바·지식그래프와는 격리되며, 향후 강의도 동일 하네스로 동일 형태로 변환된다.

---

## §1. 시스템 흐름

### 입력

강의자료 zip — `260429_황민호_강의자료.Zip` 같은 묶음.

```
<lecture>.zip
├─ slides.html 또는 slides.v2.html         (Reveal.js, 필수)
├─ instructor-notes.md 또는 .v2.md         (슬라이드↔기능 매핑 신뢰도 핵심)
├─ handout.html                            (선택)
├─ labs.md                                 (선택)
├─ _workspace/07_feature_ideas.md          (선택, 강의 카탈로그)
└─ assets/                                 (이미지·폰트)
```

### 진입점

블로그 저장소 루트에서 슬래시 커맨드 실행.

```powershell
/lecture-archive <zip-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright]
```

### 산출

```
tigerjk9.github.io/
├─ _lectures/<slug>/
│   ├─ index.md                            (강의 허브)
│   └─ <feature-slug>.md × N               (기능 페이지)
├─ _data/lectures.yml                      (강의 메타 인덱스, append)
├─ _data/navigation.yml                    ("강의자료" 메뉴, 1회 추가)
├─ _config.yml                             (collections.lectures, 1회 추가)
├─ _includes/lecture-card.html             (1회 신규)
├─ _layouts/lecture.html                   (1회 신규)
├─ _sass/_lectures.scss                    (1회 신규)
└─ assets/lectures/<slug>/
    ├─ slides.html                         (원본 풀스크린 백업)
    ├─ slides/slide-NN.webp × N            (표시용 이미지)
    ├─ slides/slide-NN.png  × N            (원본 PNG, 선택 보존)
    ├─ slides/index.json                   (슬라이드별 텍스트 검색 인덱스)
    ├─ handout.pdf                         (handout.html → PDF)
    ├─ cover.png
    └─ feature-thumb/<feature-slug>.webp × N
```

---

## §2. 5명 에이전트 팀 구성

KIST 자료를 만든 `kist-lecture-orchestrator`의 6명 패턴(researcher·analyst·curriculum·creator·labber·editor)을 큐레이션 목적에 맞게 5명으로 재편한다. **제작이 아니라 재배치**가 목적이라 researcher·creator·labber는 빠지고 입력 파싱·재구성 역할이 들어간다.

| 팀원 | subagent_type | model | 역할 | 주요 출력 |
|------|---------------|-------|------|----------|
| `inventory-mapper` | general-purpose | opus | zip 자산 인벤토리·관계 매트릭스 | `_workspace/<slug>/01_inventory.md` |
| `slide-parser` | executor | opus | Reveal.js HTML → 슬라이드 PNG × N + BeautifulSoup 텍스트 추출 | `_workspace/<slug>/02_slides.json` + `slides/slide-NN.png` |
| `feature-curator` | general-purpose | opus | 강의 카탈로그 × 슬라이드 × 노트 × 실습 매핑 → N개 기능 페이지 마크다운 | `_workspace/<slug>/03_features/*.md` + `_slug_map.yml` |
| `site-builder` | executor | opus | Jekyll collection 활성화·허브·_data·_includes·_layouts·_sass·assets 배포 | `_lectures/<slug>/` + `assets/lectures/<slug>/` + Liquid·SCSS 파일 |
| `reviewer-editor` (리더) | executor | opus | `bundle exec jekyll build` 검증·체크리스트 12개·격리 검증·1회 재호출 권한 | `_workspace/<slug>/04_review.md` |

**리더는 `reviewer-editor`**. 5명 모두 `model: "opus"`. 리더만 1회 재호출 권한을 갖고 나머지 4명은 단일 패스.

### 통신 흐름

```
T1 inventory                       (단독)
    ↓ SendMessage broadcast
T2 slide-parser  ∥  T3 feature-curator(인덱싱 선행)
    ↓ 02_slides.json 완료 → curator에 SendMessage
T3 feature-curator                 (parser·notes·labs·카탈로그 종합)
    ↓ _slug_map.yml 출력 → 사용자 검토 게이트 ★
    ↓ 사용자 승인 후 SendMessage
T4 site-builder                    (Jekyll 산출물 생성)
    ↓ SendMessage
T5 reviewer-editor                 (jekyll build 검증·체크리스트)
    ↓ 이슈 있음 → T4 1회 재호출 (max 1)
    ↓ 이슈 없음 → 완료 보고
```

### KIST 하네스(`kist-lecture-orchestrator`)와의 차이

| KIST 제작 하네스 | 큐레이션 하네스 |
|------------------|----------------|
| 0에서 슬라이드·노트·실습 만들기 | 기존 산출물을 검색·재방문 가능 형태로 재배치 |
| 6명 — researcher·analyst·curriculum·creator·labber·editor | 5명 — inventory·parser·curator·builder·reviewer |
| Discovery 모드 포함 (07_feature_ideas.md 생성) | Discovery 없음. 07_feature_ideas.md를 입력으로 받음 |
| `output/` 5종 파일 (slides·notes·handout·labs·README) | Jekyll collection + assets + _data 갱신 |

---

## §3. 사이트 정보 구조

### 3-1. URL 체계

| 경로 | 종류 | 내용 |
|------|------|------|
| `/lectures/` | 강의 아카이브 인덱스 (1장) | 강의 카드 그리드. 향후 강의 자동 합류 |
| `/lectures/<slug>/` | 강의 허브 (1장) | 강의 메타·트랙·N개 기능 카드 그리드·자산 다운로드 |
| `/lectures/<slug>/<feature-slug>/` | 기능 페이지 (N장) | 정의·핵심 동작·사용법·관련 슬라이드·강사 노트 발췌·실습 발췌·시사점 |
| `/assets/lectures/<slug>/` | 정적 자산 | slides.html, slides/, handout.pdf, cover.png, feature-thumb/ |

permalink는 collection front matter에 `permalink: /lectures/<slug>/<feature-slug>/` 직접 지정. 블로그 자동화의 `inject_permalink()` 패턴 답습.

### 3-2. `_data/lectures.yml` 스키마

```yaml
- slug: kist-claude-code
  title: "Claude Code 실무 활용 — KIST 워크숍"
  subtitle: "황민호 수석 · Forward Deployed Engineer · 2026-04-29"
  audience: "KIST 연구원"
  duration_min: 120
  environment: "Windows PowerShell"
  hub_url: /lectures/kist-claude-code/
  thumbnail: /assets/lectures/kist-claude-code/cover.png
  tracks:
    - id: basic
      label: "Basic (50분 · 12 기능)"
      features: [claudemd, auto-memory, claude-rules, ...]
    - id: advanced
      label: "Advanced (48분 · 10 기능)"
      features: [headless, hooks, skills, subagents, mcp, ...]
  feature_count: 22
  slide_count: 96
  atom_mode: feature_catalog
  assets:
    slides: /assets/lectures/kist-claude-code/slides.html
    handout: /assets/lectures/kist-claude-code/handout.pdf
```

한 강의 = 한 블록. 인덱스·허브·기능 페이지가 모두 이 한 군데를 참조. 향후 강의는 yaml에 블록 1개 추가로 합류.

### 3-3. 기능 페이지 컴포넌트 구조

```
┌─ breadcrumb: 강의자료 ▸ <강의명> ▸ <기능명> (<feature_id>)
├─ feature header (ID·분류·트랙 배지 · 영문명 + 한국어 풀이 · 정의)
├─ 핵심 동작 (3불릿)
├─ 사용법 코드 블록 (PowerShell)
├─ 관련 슬라이드 발췌 [접기·펼치기]
│   └─ slide-NN.webp + 추출 텍스트 × 1~5장
├─ 강사 멘트 (instructor-notes 발췌)
├─ 실습 매핑 (labs 발췌, 해당 시)
├─ 활용 시사점
├─ 출처 링크
└─ 이전·다음 기능 + 허브 복귀
```

각 섹션은 Liquid include로 분리 → 다른 강의에서도 같은 템플릿 재사용.

### 3-4. 격리 모드 적용

| 파일 | 패치 | 격리 보장 |
|------|------|----------|
| `_config.yml` | `collections.lectures: {output: true, permalink: /lectures/:path/}` | _posts 흐름과 분리 |
| `_data/navigation.yml` | `"강의자료" → /lectures/` 1줄 추가 | 자체 진입점 1개 |
| `_includes/sidebar/categories.html` | 변경 없음 | `site.categories`는 _posts만 봄 |
| `_includes/sidebar/tag_cloud.html` | 변경 없음 | `site.tags` 동일 |
| `graph-data.json` | 변경 없음 | 지식그래프 자동 합류 안 함 |
| `_sass/_lectures.scss` | 신규 | 스타일 격리 |
| `_layouts/lecture.html` | 신규 (single 상속) | 강의 전용 레이아웃 |

→ `_posts` 200+개 흐름·통계·지식그래프·사이드바에 영향 0건.

### 3-5. 검색 동작

- 사이트 내장 Lunr는 collection 자동 인덱싱 안 함. **기능 페이지 N장은 메인 검색에서 빠진다** (격리 의도)
- **허브 페이지(`/lectures/<slug>/`)만 메인 검색에 노출**. "Claude Code"·"KIST" 검색 시 블로그 포스트 + 강의 허브 1개가 결과로 — 도배 없음, 발견성 보장
- 허브 안에 자체 검색·필터 UI (키워드·분류·트랙 3축, `_data/lectures.yml` + 기능 메타 client-side JS)

---

## §4. 슬라이드 변환 파이프라인

### 4-1. 듀얼 추출 — Playwright + BeautifulSoup

```
slides.v2.html  (N section, Reveal.js)
       ↓
   ┌────────────────┬─────────────────┐
   ↓                ↓                 ↓
Playwright       BeautifulSoup     Reveal.js API
headless         HTML parser       (in-browser eval)
   ↓                ↓                 ↓
PNG × N          텍스트·코드·       슬라이드 인덱스
1920×1080        data-block         (총수·트랜지션)
   ↓                ↓                 ↓
   └────────────────┴─────────────────┘
                ↓
        02_slides.json (단일 통합 인덱스)
```

**왜 듀얼인가** — Reveal.js는 fragment·중첩 section·동적 시간 표시가 있어 정적 HTML 파싱만으로는 화면 결과와 다를 수 있다. Playwright로 렌더 후 상태에서 한 번 더 검증 + PNG 추출. BeautifulSoup은 코드 블록·`data-*` 속성처럼 정확히 알아야 할 의미 추출 전용.

### 4-2. `02_slides.json` 스키마

```json
[
  {
    "n": 8,
    "track": "basic",
    "block": "CLAUDE.md",
    "data_time": "1",
    "layout": "layout-bullets",
    "title": "CLAUDE.md 개념",
    "text": "첫 기능 CLAUDE.md입니다. 매 세션 시스템 프롬프트 복붙을 0으로 만드는 도구...",
    "code_blocks": [
      { "lang": "powershell", "code": "claude\n/init\nnotepad CLAUDE.md" }
    ],
    "images": [],
    "png": "/assets/lectures/kist-claude-code/slides/slide-08.webp",
    "png_original": "/assets/lectures/kist-claude-code/slides/slide-08.png",
    "feature_id": "F-035",
    "feature_slug": "claudemd",
    "mapping_method": "strict"
  }
]
```

`mapping_method`는 `strict | heading | llm` 중 하나로 향후 신뢰도 추적용.

### 4-3. 슬라이드 ↔ 기능 매핑 (3단계 폴백)

KIST 자료가 round2에서 `data-feature-id`를 화면에서 제거했기 때문에 slides 자체에는 명시적 연결고리가 없다. instructor-notes의 섹션 헤딩이 신뢰 가능한 신호.

```
## CLAUDE.md (S7~S10, 5분)         ← S7~S10이 "CLAUDE.md" 기능
## Auto Memory (S11~S13, 3분)      ← S11~S13이 "Auto Memory" 기능
```

**매핑 단계**

1. **strict** — instructor-notes 헤딩에서 `(S\d+~S\d+, \d+분)` 정규식 추출 → 기능명 ↔ 슬라이드 범위 직접 연결
2. **heading** — strict 실패 시 슬라이드 `h2` ↔ 07_feature_ideas.md의 한국어 풀이 fuzzy matching
3. **llm 폴백** — 1·2 모두 실패한 슬라이드는 Gemini에 슬라이드 텍스트 + N개 기능 카탈로그를 같이 던져 분류 1회. 결과를 `02_slides.json`에 기록하고 `mapping_method: llm`·`[검증 필요]` 마킹

각 단계 통계는 `_workspace/<slug>/04_review.md`에 — "96장 중 strict 78장, heading 14장, llm 4장 → 강사 검증 권장 4장". reviewer가 통계로 신뢰도 평가.

### 4-4. instructor-notes 발췌

```
instructor-notes.v2.md
  ## CLAUDE.md (S7~S10, 5분)
    ### S8. 개념
      - **멘트.** ...
      - **시간.** 1분
      - **강조.** ...
      - **예상 Q.** ...
```

같은 정규식으로 S번호별 멘트·강조·예상 Q를 추출. 기능 페이지에 임베드. 강사 노트 마크다운 원본은 그대로 보존.

### 4-5. 이미지 최적화

- **표시용** — WebP, max-width 1280px, ~80KB/장. N장 × 80KB
- **원본 백업** — PNG 1920×1080 보존 (선택적 풀스크린용)
- **카드 썸네일** — 320×180 WebP, N장
- GitHub Pages 1GB 트래픽 제한 고려해 표시용 default, 원본은 옵트인

### 4-6. 알려진 한계

- 슬라이드 N장 중 일부는 llm 분류 단계까지 가야 함. 강사 검증 권장
- Reveal.js fragment 다중 캡처는 이번 범위 외 (KIST round2에서 fragment 제거됨)
- 망분리 환경 변환은 Playwright Chromium 다운로드 필요. `--skip-playwright`로 강사 사전 추출 폴백

---

## §5. 실행 워크플로우

### 5-1. 슬래시 커맨드

```powershell
/lecture-archive <zip-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright] [--rerun <phase>]
```

| 옵션 | 동작 |
|------|------|
| `<zip-path>` 필수 | 강의자료 zip 절대 경로 |
| `--slug` | 강의 슬러그 강제. 생략 시 zip 파일명에서 추론 |
| `--dry-run` | `_workspace/` 산출물만. 사이트 변경 없음 |
| `--no-push` | 커밋·푸시 생략 |
| `--skip-playwright` | PNG 추출 생략. 사용자가 사전 추출한 `<zip-dir>/slides/` 사용 |
| `--rerun <phase>` | parser·curator·builder 중 한 단계부터 재실행. 이후 단계 자동 |

### 5-2. Phase 0 — 컨텍스트 확인

```
1. <slug> 결정 (옵션·zip 파일명에서)
2. _workspace/<slug>/ 존재 확인
   ├─ 미존재 → 신규 실행 (Phase 1)
   ├─ 존재 + --rerun → 해당 단계부터 재실행
   └─ 존재 + 신규 → _workspace/<slug>_<timestamp>/로 백업 후 신규
```

### 5-3. Phase 1 — 입력 정리

```
zip 압축 해제 → _workspace/<slug>/00_input/
   ├─ slides.v2.html
   ├─ instructor-notes.v2.md
   ├─ handout.html
   ├─ labs.md
   ├─ 07_feature_ideas.md (있을 경우)
   ├─ assets/
   └─ brief.yml  (자동 생성 또는 zip 내장)
```

`brief.yml`은 zip 파일명·README.md·CLAUDE.md를 파싱해 자동 채움. 결정 불가 항목은 `[강사 확인 필요]` 태그. 한글 zip 파일명은 `zipfile` cp437→utf-8 디코드 처리.

### 5-4. Phase 2 — 팀 구성

```python
TeamCreate(
  team_name=f"lecture-archive-{slug}",
  members=[
    {name: "inventory",  agent_type: "general-purpose", model: "opus", prompt: "..."},
    {name: "parser",     agent_type: "executor",        model: "opus", prompt: "scripts/lecture_archive/parse_slides.py 호출"},
    {name: "curator",    agent_type: "general-purpose", model: "opus", prompt: "..."},
    {name: "builder",    agent_type: "executor",        model: "opus", prompt: "scripts/lecture_archive/build_site.py 호출"},
    {name: "reviewer",   agent_type: "executor",        model: "opus", prompt: "팀 리더. bundle exec jekyll build로 빌드 검증."}
  ]
)
```

### 5-5. Phase 3 — 파이프라인 실행

```
T1 inventory
  ↓
T2 parser  ∥  T3 curator(인덱싱 선행)
  ↓
T3 curator
  ↓ _slug_map.yml 출력 → 사용자 검토 게이트 (★ 명시 승인 필요)
  ↓
T4 builder
  ↓
T5 reviewer (이슈 시 T4 1회 재호출)
```

### 5-6. Phase 4 — reviewer 체크리스트 12

```
[ ] 1.  bundle exec jekyll build 성공
[ ] 2.  /lectures/ 인덱스 빌드 OK
[ ] 3.  /lectures/<slug>/ 허브 빌드 OK
[ ] 4.  /lectures/<slug>/<feature-slug>/ N장 모두 빌드 OK
[ ] 5.  기능 페이지 모두 PNG 발췌 1장 이상 임베드 OK
[ ] 6.  슬라이드 ↔ 기능 매핑 통계 (strict %·heading %·llm %·미매핑)
[ ] 7.  미매핑·llm 분류 슬라이드 목록 → 강사 검증 권장 보고
[ ] 8.  격리 검증 — site.categories·site.tags에 강의 항목 0건
[ ] 9.  graph-data.json 변경 0건
[ ] 10. _data/navigation.yml "강의자료" 1줄 추가 확인
[ ] 11. assets/lectures/<slug>/ 용량 합산 50MB 이하 (또는 사용자 동의 시 초과)
[ ] 12. permalink N+2개 모두 unique·격리 패턴
```

### 5-7. Phase 5 — 정리·커밋·푸시

```
1. reviewer 결과 요약 보고 (생성 파일·매핑 통계·검증 권장 N개·알려진 한계)
2. TeamDelete
3. _workspace/<slug>/ 보존 (재실행·후속 수정용)
4. --no-push 아니면:
   git add <명시 파일 목록>  (-A 금지)
   git commit -m "Add: <강의명> 강의자료 아카이브 — N 기능·M 슬라이드"
   git fetch + rebase --autostash + push
```

### 5-8. 후속 작업 패턴

| 시나리오 | 명령 |
|---------|------|
| 슬라이드 텍스트만 재추출 | `/lecture-archive <slug> --rerun parser` |
| N개 기능 페이지 재생성 | `/lecture-archive <slug> --rerun curator` |
| 사이트 빌드만 재실행 | `/lecture-archive <slug> --rerun builder` |
| llm 분류 슬라이드 수동 매핑 | `_workspace/<slug>/02_slides.json` 직접 편집 후 `--rerun curator` |

### 5-9. 디렉토리 구조

```
tigerjk9.github.io/
├─ scripts/lecture_archive/
│   ├─ orchestrate.py            슬래시 진입점 (zip 해제·brief.yml 생성)
│   ├─ parse_slides.py           Playwright + BS4
│   ├─ map_features.py           strict·heading·Gemini 3단계 매핑
│   ├─ build_site.py             Jekyll collection·_data·assets 빌드
│   ├─ extract_notes.py          instructor-notes 발췌
│   └─ requirements.txt          playwright, beautifulsoup4, google-generativeai, weasyprint
├─ .claude/
│   ├─ commands/lecture-archive.md
│   └─ skills/lecture-archive-orchestrator/SKILL.md
├─ _config.yml                   collections.lectures 추가
├─ _data/{navigation.yml, lectures.yml}
├─ _includes/lecture-card.html
├─ _layouts/lecture.html
├─ _sass/_lectures.scss
├─ _lectures/<slug>/{index.md, *.md}
└─ assets/lectures/<slug>/{slides.html, slides/, handout.pdf, cover.png, feature-thumb/}
```

---

## §6. KIST 자료 첫 변환 — 예상 결과

### 6-1. 22 기능 영문 slug 매핑 패턴 (curator 출력 예시)

CLAUDE.md 변경 이력의 v2 22 ID 기준.

**Basic 12개 (F-035 → F-037 묶음)**

| ID | 추정 기능명 | slug |
|----|-----------|------|
| F-035 | CLAUDE.md | `claudemd` |
| F-036 | Auto Memory | `auto-memory` |
| F-037 | `.claude/rules/` | `claude-rules` |
| F-038 | Plan Mode | `plan-mode` |
| F-039 | Slash Commands | `slash-commands` |
| F-040 | Permission Modes | `permission-modes` |
| 외 6개 | 추가 카탈로그 항목 | curator 결정 |

**Advanced 10개 (F-003·006·007·009·010·011·012·013·016·024·028·029)**

| ID | 추정 기능명 | slug |
|----|-----------|------|
| F-006 | Headless mode | `headless` |
| F-007 | Hooks | `hooks` |
| F-009 | Skills | `skills` |
| F-010 | Subagents | `subagents` |
| F-011 | MCP | `mcp` |
| F-016 | UX 보조 | `ux-helper` |
| 외 4개 | 추가 카탈로그 항목 | curator 결정 |

**slug 사전 검토 게이트** — curator가 `_workspace/kist-claude-code/03_features/_slug_map.yml` 출력 후 builder는 멈추고 사용자 명시 승인 대기. URL은 영구적이므로 한 번에 정한다.

### 6-2. 산출 파일·용량 예상

```
_lectures/kist-claude-code/{index.md, *.md × 22}
_data/lectures.yml (1블록 추가)
_data/navigation.yml (1줄 추가)
_config.yml (3줄 추가)
_includes/lecture-card.html (신규)
_layouts/lecture.html (신규)
_sass/_lectures.scss (신규)

assets/lectures/kist-claude-code/
├─ slides.html                       ~92KB
├─ handout.pdf                       ~1MB
├─ cover.png                         ~500KB
├─ slides/
│   ├─ slide-01.webp ~ 96.webp       ~7.5MB
│   └─ slide-01.png ~ 96.png         ~50MB (선택 보존)
└─ feature-thumb/*.webp × 22         ~1MB

총: ~60MB (원본 PNG 포함), ~12MB (WebP만)
```

WebP만 기본 배포, 원본 PNG는 옵트인 결정 권장.

### 6-3. 예상 실행 시간·자원

| 단계 | 시간 | 비용 |
|------|------|------|
| zip 해제·brief.yml | <10s | 무료 |
| inventory | 1~2분 | Claude opus tokens |
| parser (Playwright × 96) | 5~7분 | 무료 (로컬) |
| parser (BS4) | 10s | 무료 |
| curator (strict + heading) | 1~2분 | Claude opus tokens |
| curator (Gemini 폴백) | 30s | Gemini API ~0.001달러 |
| 사용자 slug 검토 게이트 | 가변 | — |
| builder | 1분 | 무료 |
| reviewer (jekyll build) | 30s | Claude opus tokens |
| **합계** | **~10~15분 + 검토 시간** | **opus tokens + Gemini ~0.001달러** |

### 6-4. 강사 검증 권장 4항목

reviewer가 사용자에게 명시 보고.

| 항목 | 권장 행동 |
|------|----------|
| 22 기능 slug 매핑 | `_workspace/<slug>/03_features/_slug_map.yml` 검토 (사전 검토 게이트) |
| llm 분류 슬라이드 (예상 4~6장) | 자동 분류 적절성 빠르게 훑기 |
| 허브 페이지 메타 | `_data/lectures.yml`의 강사명·날짜·청중·환경 자동 채움 |
| 격리 검증 | `bundle exec jekyll serve`로 `/categories/`·`/tags/`에 강의 항목 0건 육안 확인 |

### 6-5. 예상 충돌·블로커 사전 점검

| 위험 | 가능성 | 대비 |
|------|-------|------|
| Playwright Chromium 다운로드 실패 | 중 | `--skip-playwright`로 강사 사전 추출 폴백 |
| Gemini API 키 미설정 | 낮 | `.env`의 `GEMINI_API_KEY` 점검. 기존 자동화 키 재사용 |
| `_workspace/` 디스크 누적 | 중 | `.gitignore`에 `_workspace/`·`assets/lectures/*/slides/*.png` 등록 검토 |
| 07_feature_ideas.md 부재 | 낮 (다른 강의에서 가능) | `atom_mode` 폴백 (§7-1) |
| handout.html → PDF 변환 실패 | 낮 | Playwright print PDF로 통합 |
| 한글 zip 파일명 인코딩 | 중 | `zipfile` cp437→utf-8 디코드 처리 |

### 6-6. 첫 변환 후 5개 시나리오 진입 URL

```
1. 강의 아카이브 인덱스      → /lectures/
2. KIST 강의 허브             → /lectures/kist-claude-code/
3. 기능 페이지 샘플           → /lectures/kist-claude-code/claudemd/
4. 슬라이드 원본 풀스크린     → /assets/lectures/kist-claude-code/slides.html
5. 핸드아웃 PDF              → /assets/lectures/kist-claude-code/handout.pdf
```

5개 모두 정상 동작 시 변환 성공.

---

## §7. 일반화·제외 사항

### 7-1. `brief.yml` 입력 스펙 (다른 강의 적용 시)

```yaml
slug: <영문-슬러그>                       # URL용. 영구
title: "<강의 제목>"
subtitle: "<강사·날짜·기관>"
audience: "<청중>"
duration_min: <분>
environment: "<실습 환경>"
date: <YYYY-MM-DD>

assets:                                  # zip 내 상대 경로
  slides_html: slides.v2.html            # 필수
  instructor_notes: instructor-notes.v2.md  # 권장 (매핑 신뢰도 좌우)
  handout_html: handout.html             # 선택
  labs_md: labs.md                       # 선택
  feature_catalog: 07_feature_ideas.md   # 선택

atom_mode: feature_catalog               # 3택 1
```

### 7-2. `atom_mode` 3가지

강의 구조의 자유도 흡수.

| atom_mode | 적용 강의 예 | 페이지 단위 |
|-----------|------------|------------|
| `feature_catalog` (KIST 답습) | 기능 카탈로그가 명확한 강의 | 카탈로그 항목 1개 = 1 페이지 |
| `section_heading` | 카탈로그 없이 instructor-notes만 있는 강의 | 노트 `##` 헤딩 1개 = 1 페이지 |
| `slide_group` | 노트도 없고 슬라이드만 있는 강의 | `data-block` 묶음 1개 = 1 페이지 |

curator는 atom_mode에 따라 페이지 생성 로직 분기. 다른 단계(parser·builder·reviewer)는 atom_mode 무관 동일.

### 7-3. 이번 디자인 범위 외

| 제외 | 이유 | 추가 시점 |
|------|------|----------|
| 다국어 강의 (영어·일본어) | 첫 사례 한국어 1개 집중 | 다국어 강의 들어올 때 별도 spec |
| Reveal.js fragment 다중 캡처 | KIST round2에서 fragment 제거됨. 0건 | 다른 강의에 fragment 있고 강사 요청 시 |
| 통합 사이트 검색에 강의 포함 | 격리 모드와 충돌 | 정책 변경 시 |
| 강의 동영상 자료 변환 | 별 도메인 | YouTube 강의는 `/video`에 별도 |
| 학습자 댓글·진도 추적 | 동적 기능. Giscus 통합 별도 결정 | 학습자 피드백 필요 시 |
| 한 강의를 다른 청중용 변형 | 제작이지 큐레이션 아님 | `kist-lecture-orchestrator` 패턴으로 별도 |
| PowerPoint·Keynote 슬라이드 입력 | Reveal.js HTML만 지원 | 변환 어댑터 별도 |

---

## §8. 결정 로그 (8개)

| # | 결정 | 채택 | 대안 | 근거 |
|---|------|------|------|------|
| 1 | 큐레이션 대상 | 세 역할 동시 (학습자·강사·블로그 독자) | 단일 역할 | 같은 자산이 세 역할을 만족하면 가치 최대. 사용자 명시 선택 |
| 2 | 호스팅 위치 | tigerjk9.github.io 블로그 내 `/lectures/` | 별도 저장소·오프라인 폴더 | 기존 Jekyll·검색·다크모드 인프라 재활용. 사용자 명시 선택 |
| 3 | 콘텐츠 구조 | 허브 1장 + N개 기능 페이지 | 단일 페이지·_posts 분해 | SEO·깊이 탐색·블로그 흐름 분리. 사용자 명시 선택 |
| 4 | 슬라이드 처리 | 텍스트 추출 + PNG 하이브리드 | iframe·캐러셀 | 모바일 친화·검색·풀스크린 백업 동시. 사용자 명시 선택 |
| 5 | 하네스 일반화 | KIST 첫 사례 + 패턴 일반화 | 1회용·최대 일반화 | atom_mode로 자유도 흡수. 사용자 명시 선택 |
| 6 | 하네스 구조 | Superpowers 멀티 에이전트 5명 | Python 단일·하이브리드 | KIST 패턴 답습. 사용자 명시 선택 |
| 7 | 통합 수준 | 격리 모드 | 부분·완전 통합 | _posts 200+개 흐름·통계·지식그래프 영향 0건. 사용자 명시 선택 |
| 8 | slug 검토 게이트 | curator 후 사용자 승인 → builder | 자동 진행 | URL 영구성. 사용자 명시 선택 |

추가 결정 — URL slug는 영문 (`claudemd`), F-NNN ID는 front matter `feature_id:` 메타 보존. Lunr 검색은 허브 페이지만 노출, 기능 페이지 N장은 빠짐.

---

## §9. 인터페이스 명세 요약

### 슬래시 커맨드

```
/lecture-archive <zip-path>
  [--slug <slug>]
  [--dry-run]
  [--no-push]
  [--skip-playwright]
  [--rerun parser|curator|builder]
```

### 핵심 스키마

- `brief.yml` (§7-1) — 강의 입력 메타
- `_data/lectures.yml` (§3-2) — 강의 인덱스
- `02_slides.json` (§4-2) — 슬라이드 통합 인덱스

### 핵심 파일·디렉토리

- `scripts/lecture_archive/{orchestrate,parse_slides,map_features,build_site,extract_notes}.py`
- `.claude/commands/lecture-archive.md`
- `.claude/skills/lecture-archive-orchestrator/SKILL.md`
- `_lectures/<slug>/{index,*.md}`
- `assets/lectures/<slug>/{slides.html, slides/, handout.pdf, cover.png, feature-thumb/}`

### 체크리스트 12 (§5-6)

reviewer-editor가 빌드·격리·매핑·용량을 단계별로 검증.

---

## §10. 변경 이력

| 날짜 | 변경 | 사유 |
|------|------|------|
| 2026-05-22 | 초안 작성 | 황민호 수석 KIST 자료를 첫 사례로 큐레이션 하네스 디자인. 9개 사용자 결정 게이트(대상·위치·구조·슬라이드·범위·구조·통합·게이트·LLM) 합의 |

---

*이 문서는 Superpowers brainstorming 스킬의 결과물이며, 사용자 검토 승인 후 writing-plans 스킬에서 실행 plan으로 전개한다.*
