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

> **주의**: `_sass/minimal-mistakes/_sidebar.scss`에 `.sidebar.sticky { max-height: calc(100vh - #{$nav-height} - 2em) }` 하드코딩 → `main.scss` 오버라이드에 `!important` 필수.

### Custom UI Features

| 기능 | 주요 파일 |
|------|----------|
| 다크/라이트 모드 토글 | `assets/js/theme-toggle.js`, `_includes/masthead.html` |
| 모바일 사이드바 테마 토글 | `assets/js/sidebar-toggle.js` (`injectMobileSidebarHeader`) |
| 본문 복사 버튼 (모든 포스트) | `assets/js/post-copy.js`, `_layouts/single.html` |
| 사이드바 섹션 접기/펼치기 | `assets/js/sidebar-toggle.js` (`initSectionCollapse`), `_includes/sidebar.html` |

**다크/라이트 모드**: `html[data-theme="light"]` CSS 레이어 방식. 컴파일된 dark skin 위에 light 오버라이드 덮기. anti-FOUC 인라인 스크립트를 `_includes/head.html` CSS `<link>` 이전에 삽입. `theme-toggle.js`는 이벤트 위임 방식 — masthead와 모바일 사이드바의 `.theme-toggle` 버튼 모두 처리.

**모바일 사이드바**: `injectMobileSidebarHeader()`가 사이드바 최상단에 `.sidebar-mobile-header`(테마 토글 포함)를 주입. iOS Safari dvh 버그는 `height: 100dvh; max-height: 100dvh`로 수정.

**본문 복사**: `.page__content` DOM 클론 → `.sidebar__right`, `[rel="permalink"]`, `.sr-only` 제거 → `innerText` 복사.

**사이드바 섹션 높이**: 데스크톱 `max-height: calc(50vh - 175px) !important` — 두 섹션 합산 시 페이지네이션 라인 근방에서 끝남. 내부 스크롤(얇은 4px 스크롤바) 유지.

### JS 번들 주의사항 (CRITICAL)

**브라우저는 `assets/js/main.min.js` 번들을 로드한다.** 소스 플러그인 파일(`assets/js/plugins/jquery.greedy-navigation.js` 등) 직접 편집은 브라우저에 반영되지 않는다.

JS 수정 방법:
- **재빌드 방식** (권장): 소스 파일 편집 후 `bundle exec rake js` 실행
- **직접 패치** (빠른 수정): Python으로 `main.min.js` 문자열 치환 (`open/read/replace/write`)

**Greedy-nav 커스텀 버튼**: nav에 커스텀 버튼(`.theme-toggle` 등)을 추가하면 `availableSpace` 계산에서 해당 버튼 폭을 빼야 한다. 미적용 시 메뉴 항목이 잘려서 표시됨. `main.min.js`에 `$themeToggle.outerWidth(!0)` 차감 패치 적용됨.

---

## PDF 논문 → 블로그 포스트 자동화 (`/paper`)

`scripts/pdf_to_post.py`가 PDF 논문을 한국어 Jekyll 포스트로 자동 변환한다.
Claude Code에서는 `/paper <PDF경로>` 슬래시 커맨드로 호출한다 (`.claude/commands/paper.md`).

```bash
python scripts/pdf_to_post.py _papers/paper.pdf          # 변환 + git push
python scripts/pdf_to_post.py _papers/paper.pdf --dry-run
python scripts/pdf_to_post.py _papers/paper.pdf --no-push
```

- **환경변수**: `GEMINI_API_KEY` — `.env` 파일에서 자동 로드 (gitignore 등록됨)
- **의존성**: `google-generativeai`, `pdfplumber`, `PyMuPDF`
- **포스트 구조 (고정)**: 6개 섹션 (연구목적 → 방법 → 발견 → 결론 → ADD One → 탐구질문) + APA 출처
- **Figure 자동 추출**: PyMuPDF로 300×200px 이상 이미지 최대 6개 추출 → `assets/` 저장 → 멀티모달 삽입
- **APA 출처**: URL/DOI 미포함. Gemini가 생성하는 링크는 신뢰할 수 없으므로 텍스트 출처만 기재한다 (`scripts/prompt_template.txt` 규칙)

---

## YouTube 영상 → 블로그 포스트 자동화 (`/video`)

`scripts/yt_to_post.py`가 YouTube URL을 한국어 Jekyll 포스트로 자동 변환한다.
Claude Code에서는 `/video <URL>` 스킬로 호출한다.

```bash
python scripts/yt_to_post.py <URL>            # 변환 + git push
python scripts/yt_to_post.py <URL> --dry-run  # 출력만
python scripts/yt_to_post.py <URL> --no-push  # 로컬 저장만
python scripts/yt_to_post.py <URL> --lang en  # 영어 자막 우선
```

- **환경변수**: `GEMINI_API_KEY` — `.env` 파일에서 자동 로드 (gitignore 등록됨)
- **의존성**: `google-generativeai`, `yt-dlp`, `youtube-transcript-api`

### 자막 추출 우선순위

1. `youtube-transcript-api` — 수동/자동자막 (ko → en)
2. `yt-dlp` VTT 자동자막 (SSL 우회 포함)
3. 영상 description으로 대체

### 포스트 스타일

- **문체**: `~이다`, `~한다` 단정체. 존칭/명사형 어미 금지.
- **분량**: 자막 내용을 빠짐없이 다룸 (생략 없음)
- **구조**: 도입부 → 본문(영상 흐름 따라 자유 섹션) → 크로스오버 섹션 → 출처
- **크로스오버**: 실행마다 20개 분야 풀에서 `random.choice()`로 선택 → 프롬프트에 주입
  - 풀 예시: 신경과학, 행동경제학, 언어학, 음악이론, 요리과학, 스포츠과학, 도시계획, 연극학, 진화생물학, 철학, 인류학, 물리학, 면역학, 정보이론 등
- **슬러그**: Gemini가 front matter의 `slug:` 필드로 영문 생성 → 스크립트가 파일명으로 사용 후 필드 제거

### 파일 구조

```
scripts/
  yt_to_post.py          # YouTube → 포스트 변환 스크립트
  yt_prompt_template.txt # Gemini 프롬프트 ({CROSSOVER_DOMAIN} 플레이스홀더 포함)
  pdf_to_post.py         # PDF → 포스트 변환 스크립트
  prompt_template.txt    # Gemini 프롬프트 (APA 출처 URL 제외 규칙 포함)
  requirements.txt       # Python 의존성 (pdf + yt 통합)
.env                     # GEMINI_API_KEY 저장 (gitignore, 두 스크립트 공통)
.env.example             # 키 형식 예시 (git 추적됨)
.claude/commands/video.md  # /video 슬래시 커맨드
.claude/commands/paper.md  # /paper 슬래시 커맨드
```

### 알려진 동작 특성

- Gemini가 `date:` 연도를 임의로 바꾸는 버그 있음 → 스크립트가 생성 후 강제 복원
- 한국어 제목에서 슬러그 직접 추출 불가 → Gemini slug 생성으로 해결
- 기업 네트워크 SSL 인증서 오류 → `ssl._create_unverified_context` + requests 세션 패치로 우회

---

## 공통: git push 주의사항

원격에 로컬에 없는 커밋이 있으면 push가 실패한다:

```bash
git stash
git pull origin main --rebase
git stash pop
git push origin main
```

## 공통: 주요 카테고리·태그

**카테고리** (빈도순): `AI`, `교육`, `학습과학`, `AI디지털기반교육혁신`, `철학`, `인지과학`, `바이브코딩`, `코딩`

**태그** (빈도순 상위): `이미지`, `논문리뷰`, `바이브코딩`, `AI`, `생성형AI`, `학습과학`, `교육`, `LLM`, `메타인지`, `AI윤리`, `에듀테크`, `교육공학`, `자기조절학습`, `피드백`, `프롬프트엔지니어링`
