# lecture-archive-prd

강의자료 zip → tigerjk9.github.io `_lectures/` collection 자동 큐레이션 5명 멀티 에이전트 하네스의 Product Requirements Document.

이 문서는 PRD 요약만 담는다. 정식 디자인 스펙은 `docs/superpowers/specs/2026-05-22-lecture-curation-harness-design.md`, 실행 plan은 `docs/superpowers/plans/2026-05-22-lecture-curation-harness-plan.md`를 참조한다.

## 목적

강의자료 zip(slides·instructor-notes·handout·labs·N 기능 카탈로그)이 강의 종료 후 청중에게 슬라이드 PDF 1개로만 남아 검색·재방문이 불가능한 문제를 해결한다. 같은 자산이 세 역할을 동시에 만족하도록 큐레이션한다 — (1) 강의를 들은 청중의 사후 재방문 (2) 강사의 다른 강의 재활용 (3) 블로그 독자의 일반 공개.

## 진입점

```powershell
/lecture-archive <zip-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright] [--rerun parser|curator|builder]
```

| 옵션 | 동작 |
|------|------|
| `<zip-path>` 필수 | 강의자료 zip 절대 경로 |
| `--slug` | 강의 슬러그 강제. 생략 시 zip 파일명에서 추론 |
| `--dry-run` | `_workspace/` 산출물만. 사이트 변경 없음 |
| `--no-push` | 커밋·푸시 생략 |
| `--skip-playwright` | PNG 추출 생략. 사용자가 사전 추출한 `<zip-dir>/slides/` 사용 (망분리 환경) |
| `--rerun <phase>` | parser·curator·builder 중 한 단계부터 재실행 |

## 입력 자산 (zip 안에서 자동 탐색)

`scripts/lecture_archive/orchestrate.py`의 `find_assets()`가 v2 우선 선택으로 자동 발견.

| 자산 | 필수 | 매핑 신뢰도 |
|------|------|------------|
| `slides.html` 또는 `slides.v2.html` (Reveal.js) | 필수 | — |
| `instructor-notes.md` 또는 `.v2.md` | 권장 | strict 매핑의 핵심 신호 |
| `handout.html` | 선택 | PDF로 변환 |
| `labs.md` | 선택 | 기능 페이지에 실습 발췌 |
| `07_feature_ideas.md` (강의 카탈로그) | 선택 | `atom_mode: feature_catalog` 결정 |

## atom_mode 3종

강의 구조 자유도를 흡수하는 단일 결정 변수. `brief.yml`에서 결정.

| atom_mode | 적용 강의 예 | 페이지 단위 |
|-----------|------------|------------|
| `feature_catalog` | 카탈로그가 명확한 강의 (KIST 답습) | 카탈로그 항목 1개 = 1 페이지 |
| `section_heading` | 카탈로그 없이 instructor-notes만 있는 강의 | 노트 `##` 헤딩 1개 = 1 페이지 |
| `slide_group` | 노트도 없고 슬라이드만 있는 강의 | `data-block` 묶음 1개 = 1 페이지 |

## 5명 에이전트 팀

`TeamCreate`로 5명 팀 구성 (`.claude/skills/lecture-archive-orchestrator/SKILL.md`에서 호출).

| 팀원 | 역할 | 입력 | 출력 |
|------|------|------|------|
| `inventory-mapper` | zip 자산 인벤토리·관계 매트릭스 | zip 경로 | `_workspace/<slug>/01_inventory.md` |
| `slide-parser` | Playwright + BS4 슬라이드 추출 | slides.v2.html | `02_slides.json` + `slides/slide-NN.png` |
| `feature-curator` | 카탈로그 × 슬라이드 × 노트 × 실습 매핑 | 02_slides.json + 노트 + labs + 카탈로그 | `03_features/*.md` + `_slug_map.yml` |
| `site-builder` | Jekyll 산출물 생성 | 03_features/ | `_lectures/<slug>/` + assets + `_data/lectures.yml` |
| `reviewer-editor` (리더) | jekyll build 검증·체크리스트 12 | 산출물 전체 | `04_review.md` |

리더 `reviewer-editor`만 1회 builder 재호출 권한.

## 슬라이드 ↔ 기능 매핑 (3단계 폴백)

1. **strict** — instructor-notes 헤딩 `## CLAUDE.md (S7~S10, 5분)`의 슬라이드 범위로 직접 매핑
2. **heading** — strict 실패 시 슬라이드 `h2` ↔ 카탈로그 기능명 fuzzy matching (SequenceMatcher + 첫 토큰 부스트, threshold 0.55)
3. **llm** — 1·2 실패 슬라이드는 Gemini API에 슬라이드 텍스트 + 카탈로그를 던져 분류 1회. `mapping_method: llm` + `[검증 필요]` 마킹

각 단계 통계는 `04_review.md`에 — "96장 중 strict 78장, heading 14장, llm 4장 → 강사 검증 권장 4장".

## 사이트 격리 모드

`_lectures/` collection은 `_posts` 흐름과 명확히 분리.

- `_includes/sidebar/categories.html` (`site.categories`)·`tag_cloud.html` (`site.tags`)에 강의 항목 등장 0건
- `graph-data.json` (`site.posts` 기반 지식그래프)에 강의 노드 자동 합류 안 함
- Lunr 검색은 허브 페이지(`/lectures/<slug>/`)만 노출. 기능 페이지 N장은 빠짐
- 메인 네비 `강의자료` 1줄만 진입점

## URL 체계

```
/lectures/                                  강의 아카이브 인덱스
/lectures/<slug>/                           강의 허브
/lectures/<slug>/<feature-slug>/            기능 페이지 (영문 slug, F-NNN은 front matter 메타)
/assets/lectures/<slug>/slides.html         원본 풀스크린
/assets/lectures/<slug>/slides/slide-NN.webp  표시용 (max 1280px, ~80KB/장)
/assets/lectures/<slug>/slides/slide-NN.png   원본 1920×1080 (선택 보존)
/assets/lectures/<slug>/handout.pdf
/assets/lectures/<slug>/feature-thumb/<slug>.webp
```

permalink는 collection front matter에 `permalink: /lectures/<slug>/<feature-slug>/` 직접 지정.

## 사용자 게이트 1개

curator가 `_workspace/<slug>/03_features/_slug_map.yml` 출력 후 builder는 멈추고 **사용자 명시 승인 대기**. 승인 키워드: "slug 승인", "approve slugs". URL은 영구적이므로 한 번에 정한다.

## 파일 구조

```
scripts/lecture_archive/
├─ __init__.py
├─ orchestrate.py            진입점 — zip 해제·brief.yml
├─ parse_slides.py           Playwright + BS4
├─ map_features.py           strict·heading·Gemini 3단계
├─ extract_notes.py          instructor-notes 파싱
├─ build_site.py             Jekyll collection 빌드
├─ utils.py                  zip 디코드·slug 헬퍼
├─ requirements.txt          playwright·beautifulsoup4·google-generativeai·weasyprint·Pillow·PyYAML·pytest
└─ tests/{conftest.py, fixtures/, test_*.py}   18 tests pass

.claude/
├─ commands/lecture-archive.md             슬래시 (Phase C)
└─ skills/lecture-archive-orchestrator/    팀 명세 (Phase C)
    └─ SKILL.md

_includes/{lecture-card.html, lecture-nav.html}
_layouts/lecture.html
_sass/_lectures.scss
_data/{lectures.yml, navigation.yml}
_pages/lectures.md
_lectures/<slug>/                          (Phase D 산출, 첫 사례는 kist-claude-code)
assets/lectures/<slug>/                    (Phase D 산출)
```

## 알려진 동작 특성

- **Python 3.9 호환** — 모든 스크립트가 `from __future__ import annotations` + `typing.Union/Optional/List/Dict` 사용. PEP 604 `bytes | str` 신문법 사용 시 사용자 환경에서 작동 안 함
- **Subagent Ruby 부재** — Claude Code Agent dispatch subagent는 `bundle`·`ruby` PATH 없음. Jekyll 변경은 사용자 측 직접 빌드로 격리·회귀 검증 필요
- **Playwright Chromium ~150MB** — 첫 설치 시 다운로드. 망분리 환경은 `--skip-playwright` + 강사 사전 추출 폴백
- **격리 회귀 검증 명령** — `bundle exec jekyll build && ls _site/categories/ | wc -l && ls _site/tags/ | wc -l` 카운트 변경 전후 동일
- **한글 zip 파일명** — `zipfile` 모듈의 cp437→utf-8 디코드 처리 (`orchestrate.py extract_zip`)
- **중첩 zip 자동 해제** — KIST zip은 내부에 `발표자료.zip`·`발표자료_소스.zip`·`클로드코드스킬.zip` 중첩. `extract_zip()`이 `rglob` 후 nested zip 재귀 해제
- **`_workspace/` gitignore** — 변환 작업 디렉토리는 추적하지 않음. `.gitignore`에 `_workspace/` 등록됨

## 현재 진행 상태 (2026-05-22)

- **Phase A 인프라** (Task 1~4): ✅ Jekyll collection·layout·partial·navigation·index
- **Phase B 핵심 스크립트** (Task 5~11): ✅ 5개 스크립트 + orchestrate.py, 18 tests pass, KIST zip 통합 검증 통과
- **Phase C 에이전트 팀** (Task 12~13): ⏳ SKILL.md + 슬래시 커맨드
- **Phase D 첫 변환** (Task 14~19): ⏳ KIST 자료 → 22 페이지 + assets 배포·**slug 승인 게이트**·체크리스트·push

다음 세션 첫 명령 권장 — `bundle exec jekyll build` 격리 회귀 검증 → Task 12부터 진행.
