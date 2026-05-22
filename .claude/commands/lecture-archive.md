---
description: "강의자료(zip·pdf·html·디렉토리) → _lectures/ collection 자동 큐레이션"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
---

# /lecture-archive

강의자료(zip·pdf·html·디렉토리 등 형식 자유)를 tigerjk9.github.io 블로그의 `_lectures/` collection으로 자동 큐레이션한다.

## 지원 입력 형식

| 형식 | 예시 | atom_mode 결정 |
|------|------|---------------|
| zip 묶음 | `강의자료.zip` | 내부 자산에 따라 자동 |
| PDF | `강의슬라이드.pdf` | `section_heading` |
| HTML (Reveal.js 등) | `slides.html` | `slide_group` |
| 디렉토리 | `C:\강의\` | 내부 자산에 따라 자동 |

## 사용

```
/lecture-archive <input-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright] [--rerun parser|curator|builder]
```

| 옵션 | 설명 |
|------|------|
| `<input-path>` | 강의자료 경로 (zip·pdf·html·디렉토리, 필수) |
| `--slug` | 강의 슬러그 강제. 생략 시 파일명에서 자동 추론 |
| `--dry-run` | `_workspace/` 산출물만 생성. 사이트 파일·git 변경 없음 |
| `--no-push` | 커밋·푸시 생략 |
| `--skip-playwright` | PNG 추출 생략. 사전 추출된 `_workspace/<slug>/slides/` 사용 |
| `--rerun <phase>` | `parser`·`curator`·`builder` 중 해당 단계부터 재실행 |

## 실행

`$ARGUMENTS`가 비어 있으면 입력 경로를 먼저 사용자에게 물어본 후 아래를 실행한다.

### Step 1: orchestrate.py (zip 해제·brief.yml)

```powershell
python -m scripts.lecture_archive.orchestrate $ARGUMENTS
```

`_workspace/<slug>/brief.yml`이 생성되면 Step 2로 진행.

### Step 2: 5명 에이전트 팀 실행

`.claude/skills/lecture-archive-orchestrator/SKILL.md`의 워크플로우에 따라 5명 팀을 구성하고 파이프라인을 실행한다.

팀 구성:

| 팀원 | 역할 |
|------|------|
| inventory | zip 자산 인벤토리 + 관계 매트릭스 |
| parser | Reveal.js 슬라이드 추출 (BeautifulSoup + Playwright) |
| curator | 기능 카탈로그 × 슬라이드 × 노트 매핑 → N개 기능 페이지 마크다운 |
| builder | Jekyll collection 배포 (pages + assets + lectures.yml) |
| reviewer (리더) | jekyll build 검증·체크리스트 12·격리 검증 |

## 사용자 입력 지점

**slug 검토 게이트 (필수)** — curator가 `_workspace/<slug>/03_features/_slug_map.yml`을 출력한 뒤 멈춘다. 사용자가 slug를 검토하고 `"슬러그 승인"` 입력 → builder 시작.

URL은 영구적이므로 한 번에 확정한다.

## 산출물

```
_lectures/<slug>/
  index.md                     강의 허브 페이지
  <feature-slug>.md × N        기능 개별 페이지
assets/lectures/<slug>/
  slides.html                  원본 풀스크린
  slides/slide-NN.webp × N     표시용 이미지
  handout.html                 핸드아웃
  cover.jpg                    Pillow 생성 커버 (인물 사진 금지)
_data/lectures.yml             강의 항목 append
_workspace/<slug>/             변환 작업 디렉토리 (보존)
```

## 격리 보장

`_lectures/`는 `_posts` 흐름과 분리. 사이드바·지식그래프·검색에 강의 항목 미노출.

## 알려진 한계

- Playwright Chromium 첫 다운로드 ~150MB
- Subagent에는 `bundle`·`ruby` PATH 없음 → `bundle exec jekyll build`는 사용자가 직접 실행
- 한 강의 변환 예상 시간: 10~15분 + slug 검토 시간
