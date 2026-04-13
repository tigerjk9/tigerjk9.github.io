# tigerjk9.github.io

[![Jekyll](https://img.shields.io/badge/jekyll-%3E%3D%203.7-blue.svg)](https://jekyllrb.com/)
[![GitHub Pages](https://img.shields.io/badge/hosted-GitHub%20Pages-brightgreen.svg)](https://tigerjk9.github.io)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

교육, AI, 학습과학을 중심으로 다양한 분야를 넘나드는 개인 블로그.
[https://tigerjk9.github.io](https://tigerjk9.github.io)

Minimal Mistakes Jekyll 테마(v4.27.3) 기반. 테마 파일을 gem 대신 프로젝트 내 직접 포함.

---

## 자동화 파이프라인

### `/video` — YouTube → 블로그 포스트

YouTube URL 하나를 주면 자막을 분석해 Jekyll 포스트를 자동 생성한다.

```bash
python scripts/yt_to_post.py <YouTube_URL>            # 변환 + git push
python scripts/yt_to_post.py <YouTube_URL> --dry-run  # 파일 저장 없이 출력만
python scripts/yt_to_post.py <YouTube_URL> --no-push  # 로컬 저장만
python scripts/yt_to_post.py <YouTube_URL> --lang en  # 영어 자막 우선
```

Claude Code에서는 `/video <URL>` 스킬로 호출한다.

**동작 순서**

1. `.env`에서 `GEMINI_API_KEY` 자동 로드
2. `yt-dlp`로 메타데이터(제목·채널·업로드 날짜) 수집
3. 자막 3단계 폴백: `youtube-transcript-api` → `yt-dlp` VTT → 영상 description
4. 20개 분야 풀에서 랜덤 크로스오버 분야 선택
5. Gemini(`gemini-2.0-flash`)로 한국어 포스트 생성 (영문 slug 포함)
6. `_posts/YYYY-MM-DD-{slug}.md` 저장 → git commit + push

**포스트 스타일** (`/video` 전용)

- **문체**: `~이다`, `~한다` 단정체. 존칭·명사형 어미(`~입니다`, `~함`, `~됨`) 금지
- **분량**: 자막 내용을 빠짐없이 다룬다. 생략 없음
- **구조**: 도입부 → 본문(자유 섹션) → 크로스오버 섹션 → 출처
- **크로스오버**: 실행마다 20개 분야 풀(신경과학·행동경제학·언어학·음악이론·스포츠과학 등)에서 `random.choice()`로 선택 → 본문 끝에 3~5문장으로 짧게 수록

---

### `/paper` — PDF 논문 → 블로그 포스트

PDF 논문을 한국어 Jekyll 포스트로 자동 변환한다.

```bash
python scripts/pdf_to_post.py _papers/paper.pdf           # 변환 + git push
python scripts/pdf_to_post.py _papers/paper.pdf --dry-run
python scripts/pdf_to_post.py _papers/paper.pdf --no-push
```

**포스트 스타일** (`/paper` 전용)

- **구조 고정**: 연구 목적 → 연구 방법 → 주요 발견 → 결론 → ADD One → 탐구 질문 + APA 출처
- **Figure 자동 추출**: PyMuPDF로 300×200px 이상 이미지 최대 6개 추출 → `assets/` 저장 → 멀티모달 삽입

---

## 환경 설정

```bash
# 의존성 설치
bundle install
pip install -r scripts/requirements.txt

# API 키 설정 (.env는 gitignore 등록됨)
cp .env.example .env
# .env 파일에 GEMINI_API_KEY=AIza... 입력
```

**`.env` 형식**

```
GEMINI_API_KEY=AIza...
```

---

## 로컬 개발

```bash
bundle exec jekyll serve        # http://localhost:4000
bundle exec jekyll build        # 사이트 빌드
bundle exec rake preview        # 테마 테스트 http://localhost:4000/test/
```

---

## 프로젝트 구조

```
_posts/          # 블로그 포스트 (YYYY-MM-DD-slug.md)
_papers/         # 논문 PDF 원본
assets/          # 이미지 (flat, 서브디렉토리 없음)
scripts/
  yt_to_post.py          # YouTube → 포스트 변환
  pdf_to_post.py         # PDF → 포스트 변환
  yt_prompt_template.txt # Gemini 프롬프트 템플릿 (video)
  prompt_template.txt    # Gemini 프롬프트 템플릿 (paper)
  requirements.txt       # Python 의존성
_config.yml      # 사이트 설정 (timezone: Asia/Seoul 필수)
_data/
  navigation.yml # 상단 메뉴
.env             # API 키 (gitignore, 커밋 금지)
.env.example     # 키 형식 예시
docs/            # 테마 원본 문서 (블로그 빌드에서 제외)
```

---

## 커스텀 UI 기능

### 다크 / 라이트 모드 토글

마스트헤드 우측 버튼으로 전환. `localStorage`에 선택값을 저장해 새로고침 후에도 유지된다.  
FOUC 방지 인라인 스크립트를 CSS `<link>` 앞에 삽입해 깜빡임 없이 테마가 적용된다.

- 구현: `assets/js/theme-toggle.js`, `_includes/masthead.html`, `_includes/head.html`
- CSS: `html[data-theme="light"]` 레이어로 컴파일된 dark skin 위에 덮어씀

### 본문 복사 버튼

포스트 상단에 **본문 복사** 버튼 표시. 클릭 시 포스트 본문 전체를 클립보드에 복사한다.  
TOC("On this page")와 각 헤딩의 Permalink 텍스트는 자동으로 제외된다.

- 구현: `assets/js/post-copy.js`, `_layouts/single.html`
- DOM 클론 방식 — 페이지 표시에 영향 없음

### 접이식 사이드바 섹션

Categories / Tag Cloud 섹션 헤더를 클릭해 접기/펼치기 가능.  
상태는 `localStorage`에 저장되어 재방문 시 유지된다.

- 구현: `assets/js/sidebar-toggle.js` (`initSectionCollapse`), `_includes/sidebar.html`
- 각 섹션 콘텐츠 높이: `calc(50vh - 175px)` — 두 섹션 합산 시 페이지네이션 라인 근방에서 끝남

---

## 주요 설정값

| 항목 | 값 |
|------|----|
| 테마 | Minimal Mistakes v4.27.3 (dark skin) |
| locale | ko-KR |
| timezone | Asia/Seoul |
| 댓글 | Giscus (기본 비활성) |
| 분석 | Google Analytics `G-Y8TNBPZQEZ` |
| 검색 | Lunr.js |

---

## 베이스 테마

이 블로그는 [Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) (Michael Rose, MIT License)를 기반으로 한다.
