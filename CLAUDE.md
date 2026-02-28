# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
bundle install

# Serve the blog locally (live at http://localhost:4000)
bundle exec jekyll serve

# Build the site
bundle exec jekyll build

# Serve the theme test suite (http://localhost:4000/test/)
bundle exec rake preview

# Build JS assets (minified bundle)
bundle exec rake js

# Update version across files
bundle exec rake version
```

## Architecture

This repository is simultaneously the **Minimal Mistakes Jekyll theme source** (v4.27.3) and the **owner's personal blog** at https://tigerjk9.github.io. The theme files (`_layouts`, `_includes`, `_sass`, `assets/`) are used directly rather than loaded from a gem.

The `docs/` and `test/` directories belong to the upstream theme project and are excluded from the blog build (`_config.yml` exclude list).

### Blog Content

- **Posts**: `_posts/YYYY-MM-DD-slug.md` — front matter requires `title`, `date`, `categories` (array), `tags` (array)
- **Images**: stored flat in `assets/` (e.g. `/assets/post-slug-1.jpg`)
- **Navigation**: `_data/navigation.yml` — defines the masthead nav links
- **Site config**: `_config.yml` — locale `ko-KR`, dark skin, Giscus comments (disabled by default), Google Analytics (`G-Y8TNBPZQEZ`)

Post default layout is `single` with author profile, read time, and related posts enabled. Comments are globally disabled in defaults; to enable per-post add `comments: true` to front matter.

### Custom Features

**3D Knowledge Graph** (`/knowledge-graph/`):
- The page is `knowledge-graph.md` with layout `wide`
- Graph data is generated at build time by the Liquid template `graph-data.json` and `knowledge-graph.json` — these files aggregate post tags and create node/edge JSON
- The visualization uses Three.js + D3 + 3d-force-graph loaded from CDN; nodes represent posts and tags, edges represent tag relationships

**Custom Sidebar** (`_includes/sidebar/`):
- `categories.html` — lists all site categories with post counts
- `tag_cloud.html` — tag cloud display
- Sidebar is configured in `_config.yml` under the `sidebar` key

### Theme Customization Layers

When overriding theme files, the lookup order is: project files → gem files. Any file placed in the project's `_includes/`, `_layouts/`, `_sass/`, or `assets/` overrides the gem equivalent.

The `_sass/minimal-mistakes.scss` entry point imports all partials from `_sass/minimal-mistakes/`. Custom style overrides belong in `assets/css/main.scss`.

---

## PDF 논문 → 블로그 포스트 자동화 (`/paper`)

### 개요

`scripts/pdf_to_post.py` 스크립트가 PDF 논문을 한국어 Jekyll 블로그 포스트로 자동 변환한다.
Claude Code에서는 `/paper` 스킬로 호출한다.

```bash
python scripts/pdf_to_post.py _papers/paper.pdf          # 변환 + git push
python scripts/pdf_to_post.py _papers/paper.pdf --dry-run  # 출력만 (저장 안 함)
python scripts/pdf_to_post.py _papers/paper.pdf --no-push  # 로컬 저장만
```

### 환경 요구사항

- **Python**: 3.9.6 (시스템 기본) — `X | Y` 타입 힌트 미지원, `from __future__ import annotations` 필수
- **환경변수**: `GEMINI_API_KEY` (Google AI Studio)
- **의존성** (`scripts/requirements.txt`):
  ```
  google-generativeai>=0.8.0
  pdfplumber>=0.11.0
  PyMuPDF>=1.23.0
  ```

### 주요 기능

1. **기존 태그/카테고리 재사용**: `_posts/*.md` 전체 스캔 → 빈도순 목록 → Gemini 프롬프트에 주입해 기존 어휘 우선 사용
2. **Figure 자동 추출·삽입**: PyMuPDF로 PDF 이미지 추출 (300×200px 이상, 중복 제거, 최대 6개) → `assets/{slug}-fig-N.ext` 저장 → Gemini 멀티모달 API로 포스트 적절한 위치에 삽입
3. **고정 포스트 구조** (Gemini가 임의로 변경 불가):

```
제목: 연구의 핵심 내용을 묻는 한국어 질문 형태
  예) "AI 챗봇은 자기조절학습을 어떻게 지원하는가?"

## 1. 연구의 목적
## 2. 연구의 방법
## 3. 주요 발견
## 4. 결론 및 시사점
## 5. 리뷰어의 ADD(+) One: 생각 더하기
## 6. 추가 탐구 질문
<출처>
```

### 파일 구조

```
scripts/
  pdf_to_post.py       # 메인 변환 스크립트
  prompt_template.txt  # Gemini 시스템 프롬프트 (플레이스홀더 포함)
  requirements.txt     # Python 의존성

_papers/               # PDF 원본 보관 (Jekyll 빌드에서 제외)
assets/                # 추출된 Figure 이미지 저장 (flat, 서브디렉토리 없음)
```

### git push 주의사항

원격에 로컬에 없는 커밋이 있으면 push가 실패한다. 이때:

```bash
git stash
git pull origin main --rebase
git stash pop
git push origin main
```

### 주요 카테고리 (빈도순)

`AI`, `교육`, `학습과학`, `AI디지털기반교육혁신`, `철학`, `인지과학`, `바이브코딩`, `코딩`

### 주요 태그 (빈도순 상위)

`이미지`, `논문리뷰`, `바이브코딩`, `AI`, `생성형AI`, `학습과학`, `교육`, `LLM`, `메타인지`, `AI윤리`, `에듀테크`, `교육공학`, `자기조절학습`, `피드백`, `프롬프트엔지니어링`
