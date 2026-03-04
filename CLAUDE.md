# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
bundle install                  # 의존성 설치
bundle exec jekyll serve        # 로컬 서버 (http://localhost:4000)
bundle exec jekyll build        # 사이트 빌드
bundle exec rake preview        # 테마 테스트 (http://localhost:4000/test/)
bundle exec rake js             # JS 번들 빌드
bundle exec rake version        # 버전 일괄 업데이트
```

## Architecture

이 저장소는 **Minimal Mistakes Jekyll 테마 소스**(v4.27.3)이자 **개인 블로그** https://tigerjk9.github.io 이다.
테마 파일(`_layouts`, `_includes`, `_sass`, `assets/`)은 gem 대신 프로젝트 내에서 직접 사용된다.

`docs/`, `test/`는 업스트림 테마 전용 — `_config.yml` exclude 목록에 포함되어 블로그 빌드에서 제외된다.

### Blog Content

- **포스트**: `_posts/YYYY-MM-DD-slug.md` — front matter: `title`, `date`, `categories`(배열), `tags`(배열) 필수
- **이미지**: `assets/`에 flat 저장 (서브디렉토리 없음), 예: `/assets/post-slug-1.jpg`
- **내비게이션**: `_data/navigation.yml` — 상단 메뉴 정의
- **사이트 설정**: `_config.yml` — locale `ko-KR`, dark skin, Giscus 댓글(기본 비활성), Google Analytics `G-Y8TNBPZQEZ`
- **timezone**: `_config.yml`에 `timezone: Asia/Seoul` 반드시 설정. 미설정 시 KST 당일 포스트가 UTC 기준 future로 판단되어 GitHub Pages에서 숨겨짐.

포스트 기본 레이아웃은 `single` (author profile, read time, related posts 활성화). 댓글은 기본 비활성; 활성화하려면 front matter에 `comments: true` 추가.

### Custom Features

**3D Knowledge Graph** (`/knowledge-graph/`):
- 페이지: `knowledge-graph.md` (layout `wide`)
- 그래프 데이터: Liquid 템플릿 `graph-data.json`, `knowledge-graph.json`이 빌드 시 포스트 태그를 집계해 노드/엣지 JSON 생성
- 시각화: Three.js + D3 + 3d-force-graph (CDN). 노드 = 포스트·태그, 엣지 = 태그 관계

**Custom Sidebar** (`_includes/sidebar/`):
- `categories.html` — 카테고리별 포스트 수
- `tag_cloud.html` — 태그 클라우드
- `_config.yml`의 `sidebar` 키에서 설정

### Theme Customization

파일 탐색 순서: 프로젝트 파일 → gem 파일. `_includes/`, `_layouts/`, `_sass/`, `assets/`에 놓으면 gem 파일을 덮어씀.
커스텀 스타일 오버라이드: `assets/css/main.scss`.

---

## PDF 논문 → 블로그 포스트 자동화 (`/paper`)

### 개요

`scripts/pdf_to_post.py`가 PDF 논문을 한국어 Jekyll 포스트로 자동 변환한다.
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
2. **Figure 자동 추출·삽입**: PyMuPDF로 PDF 이미지 추출 (300×200px 이상, 중복 제거, 최대 6개) → `assets/{slug}-fig-N.ext` 저장 → Gemini 멀티모달 API로 포스트 내 관련 섹션 근처에 삽입
3. **timezone 자동 점검**: `_config.yml`의 `timezone: Asia/Seoul`이 없으면 자동 수정 후 커밋에 포함
4. **포스트 날짜**: 스크립트 실행 시점의 실제 시각이 자동 삽입 (`YYYY-MM-DD HH:MM:SS +0900`). 같은 날 여러 논문을 처리해도 시간이 달라 중복되지 않음.

### 포스트 구조 (고정)

Gemini가 임의로 변경 불가. `prompt_template.txt`가 이 구조를 강제함.

```
title: "연구의 핵심 내용을 묻는 한국어 질문 형태"
  예) "AI 챗봇은 자기조절학습을 어떻게 지원하는가?"

date: YYYY-MM-DD HH:MM:SS +0900   ← 스크립트 실행 시각 자동삽입
categories: [카테고리1]            ← 최대 2개, 기존 카테고리 우선
tags: [태그1, ..., 태그8]          ← 5~8개, 기존 태그 우선

## 1. 연구의 목적
## 2. 연구의 방법
## 3. 주요 발견
## 4. 결론 및 시사점
## 5. 리뷰어의 ADD(+) One: 생각 더하기
## 6. 추가 탐구 질문
<출처>
```

**섹션 내부 형식 규칙**:
- `### 소제목` 하위헤딩 사용 금지
- `(1) (2) (3)...` 번호 형식으로 포인트 나열
- 섹션 5 ADD: 4관점 고정 — (1)인상적 지점, (2)더 넓은 연결, (3)한계·다른 맥락, (4)독창적 제안
- 섹션 6 탐구질문: `(1) 질문?` 번호 형식 (글머리 기호 금지)
- 출처: APA 7판, DOI는 마크다운 링크로 표시

### Figure 처리 원칙

- **포함**: 논문의 실제 연구 Figure (그래프, 플롯, 다이어그램 등)
- **제외**: 장식용 클립아트, 의미 불명 이미지, 검은 화면, 아이콘류
- **위치**: 관련 섹션(주로 섹션 2·3) 근처, 내용과 직접 연관된 포인트 바로 뒤

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

충돌 발생 시 충돌 파일을 수동으로 Edit 해결 후 `git add` → `git rebase --continue`.

### 주요 카테고리 (빈도순)

`AI`, `교육`, `학습과학`, `AI디지털기반교육혁신`, `철학`, `인지과학`, `바이브코딩`, `코딩`

### 주요 태그 (빈도순 상위)

`이미지`, `논문리뷰`, `바이브코딩`, `AI`, `생성형AI`, `학습과학`, `교육`, `LLM`, `메타인지`, `AI윤리`, `에듀테크`, `교육공학`, `자기조절학습`, `피드백`, `프롬프트엔지니어링`
