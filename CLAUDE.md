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

### 마무리 커맨드

`/wrap` — 작업 세션 마무리 전역 슬래시 커맨드 (`~/.claude/commands/wrap.md`).
메모리 저장 → CLAUDE.md 정리 → PRD 정리 → git commit & push 4단계를 순서대로 실행한다.

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
| 본문 복사 + 링크 복사 버튼 | `assets/js/post-copy.js`, `_layouts/single.html` |
| 사이드바 섹션 접기/펼치기 | `assets/js/sidebar-toggle.js` (`initSectionCollapse`), `_includes/sidebar.html` |

**다크/라이트 모드**: `html[data-theme="light"]` CSS 레이어 방식. 컴파일된 dark skin 위에 light 오버라이드 덮기. anti-FOUC 인라인 스크립트를 `_includes/head.html` CSS `<link>` 이전에 삽입. `theme-toggle.js`는 이벤트 위임 방식 — masthead와 모바일 사이드바의 `.theme-toggle` 버튼 모두 처리.

**모바일 사이드바**: `injectMobileSidebarHeader()`가 사이드바 최상단에 `.sidebar-mobile-header`(테마 토글 포함)를 주입. iOS Safari dvh 버그는 `height: 100dvh; max-height: 100dvh`로 수정.

**본문 복사**: `.page__content` DOM 클론 → `.sidebar__right`, `[rel="permalink"]`, `.sr-only` 제거 → `innerText` 복사. 복사 텍스트에 `원문링크: <decoded URL>` 자동 삽입 (`## 출처` 섹션 앞, 없으면 맨 끝). URL은 `decodeURIComponent(window.location.href)`로 한글 디코딩.

**출처 섹션**: 모든 자동화 포스트의 출처는 `## 출처` 헤딩으로 통일 (기존 `<출처>` 태그 폐기). 프롬프트 템플릿 7개 + 기존 포스트 54개 일괄 변환 완료 (2026-04-28).

**링크 복사**: 포스트 URL만 단독 복사. 한글 경로도 디코딩된 상태로 복사. 버튼은 `.post-copy-wrap` flex 컨테이너에 본문 복사 버튼과 나란히 배치 (모바일에서는 세로 스택).

**사이드바 섹션 높이**: 데스크톱 `max-height: calc(50vh - 175px) !important` — 두 섹션 합산 시 페이지네이션 라인 근방에서 끝남. 내부 스크롤(얇은 4px 스크롤바) 유지.

**모바일 최적화** (`assets/css/main.scss` `@media (max-width: 1023px)` 블록):
- 사이트 제목 한 줄 고정: `max-width: calc(100vw - 155px)` + `overflow: hidden` + `text-overflow: ellipsis` + `flex-shrink: 1` (이전 `overflow: visible` 방식 폐기)
- 테이블 가로 스크롤: `.page__content table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch }`
- 코드 블록 가로 스크롤: `.page__content pre, .highlight { overflow-x: auto }`
- 이미지 뷰포트 이탈 방지: `.page__content img { max-width: 100%; height: auto }`

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
설계 의도: 어떤 논문을 넣어도 일정한 품질이 나오는 반복 가능한 구조 → `scripts/paper-prd.md` 참고.

```bash
python scripts/pdf_to_post.py _papers/paper.pdf           # 변환 + git push + PDF 자동 삭제
python scripts/pdf_to_post.py _papers/paper.pdf --dry-run
python scripts/pdf_to_post.py _papers/paper.pdf --no-push
python scripts/pdf_to_post.py _papers/paper.pdf --keep-pdf # 원본 PDF 보존
```

- **환경변수**: `GEMINI_API_KEY` — `.env` 파일에서 자동 로드 (gitignore 등록됨)
- **의존성**: `google-generativeai`, `pdfplumber`, `PyMuPDF`
- **로컬 용량 정책**: `_papers/*.pdf`는 `.gitignore` 등록. 처리 완료 후 원본 PDF 자동 삭제 (로컬 누적 방지). 보존 필요 시 `--keep-pdf`
- **포스트 구조 (고정 6섹션)**: 연구목적 → 방법 → 주요발견 → 결론 및 시사점 → 리뷰어 ADD One → 탐구질문 + APA 출처
  - 섹션 1·2는 간결하게, 섹션 3·4·5가 전체의 70% 이상 차지
  - 섹션 3(주요 발견): 3개 이상 항목. 프레임워크·모델 제안 논문은 구성요소를 각각 별도 항목으로 전개
  - 섹션 5(리뷰어 ADD One): 3항목 — 주목할 지점 / 인접 분야 연결 / 발전 아이디어
- **형식 규칙**: 번호 체계 `(1)(2)...`는 최상위만. 하위 목록은 `-` 불릿(2칸 들여쓰기). 중첩 번호 금지
- **문체**: 단정체(`~함·~됨·~임`). 존칭 어미(`~합니다·~됩니다`) 금지. 따옴표(' ") 금지
- **Figure 자동 추출**: PyMuPDF로 300×200px 이상 이미지 최대 6개 추출 → `assets/` 저장 → 멀티모달 삽입
- **APA 출처**: URL/DOI 미포함. Gemini가 생성하는 링크는 신뢰할 수 없으므로 텍스트 출처만 기재한다

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
  web_to_post.py         # 웹 아티클 → 포스트 패러프레이즈 변환 스크립트
  web_prompt_template.txt # Gemini 프롬프트 (패러프레이즈 전용)
  web_multi_prompt_template.txt # Gemini 프롬프트 (복수 URL 통합)
  web_merge_prompt_template.txt # Gemini 프롬프트 (--into 머지 모드)
  lecture_script.py      # 교원 연수용 강의 스크립트 생성
  image_fetcher.py       # 이미지 검색·삽입 공용 모듈 (OG→DDG→Pexels 순서, 4개 스크립트 공유)
  requirements.txt       # Python 의존성 (pdf + yt + web 통합)
.env                     # GEMINI_API_KEY + PEXELS_API_KEY 저장 (gitignore)
.env.example             # 키 형식 예시 (git 추적됨)
.claude/commands/video.md  # /video 슬래시 커맨드
.claude/commands/paper.md  # /paper 슬래시 커맨드
.claude/commands/paraph.md # /paraph 슬래시 커맨드
```

### 알려진 동작 특성

- Gemini가 `date:` 연도를 임의로 바꾸는 버그 있음 → 스크립트가 생성 후 강제 복원
- 한국어 제목에서 슬러그 직접 추출 불가 → Gemini slug 생성으로 해결
- 기업 네트워크 SSL 인증서 오류 → `ssl._create_unverified_context` + requests 세션 패치로 우회

---

## 웹 아티클 → 블로그 포스트 자동화 (`/paraph`)

`scripts/web_to_post.py`가 일반 웹 페이지 URL을 한국어 Jekyll 포스트로 자동 변환한다.
Claude Code에서는 `/paraph <URL>` 슬래시 커맨드로 호출한다 (`.claude/commands/paraph.md`).
번역이 아닌 **패러프레이즈** — 원본 논지를 이해한 뒤 교육 전문가의 목소리로 재서술한다.
설계 의도·3가지 모드·비공개 레포 우회 절차는 `scripts/paraph-prd.md` 참고.

```bash
python scripts/web_to_post.py <URL>            # 변환 + git push
python scripts/web_to_post.py <URL> --dry-run  # 출력만
python scripts/web_to_post.py <URL> --no-push  # 로컬 저장만
python scripts/web_to_post.py <URL> --slug SLUG  # 슬러그 지정
python scripts/web_to_post.py <URL> --into _posts/YYYY-MM-DD-slug.md  # 머지 모드
```

**머지 모드(`--into`)**: 신규 포스트 생성 대신 기존 포스트에 신규 자료를 녹여 같은 파일을 덮어쓴다. 기존 구조·문체·날짜·크로스오버 섹션을 보존하고, 신규 자료에서 수치·비유·인용·균형 관점·구조적 대안을 채굴해 자연스럽게 통합한다. 프롬프트는 `scripts/web_merge_prompt_template.txt`.

- **환경변수**: `GEMINI_API_KEY` — `.env` 파일에서 자동 로드 (gitignore 등록됨)
- **의존성**: `google-generativeai`, `requests`, `beautifulsoup4`

### 콘텐츠 추출 우선순위

1. `requests` + `BeautifulSoup` — 정적 HTML 파싱
2. `r.jina.ai/{url}` — JS 렌더링 페이지 폴백 (본문 500자 미만 시 자동 전환)

### 포스트 스타일

- **문체**: `~이다`, `~한다` 단정체. 존칭/명사형 어미 금지.
- **패러프레이즈 원칙**: 원문 이해 후 재서술. 번역 금지. 한국 교육 맥락 예시 추가 허용.
- **구조**: 도입부 → 본문(재구성 자유) → 크로스오버 섹션 → 출처

### 패러프레이즈 세부 원칙

- 전문 용어는 쉬운 말로 풀어 설명하되 정확성을 잃지 않는다
- 딱딱한 문장을 교육 전문가의 따뜻하고 친절한 어투로 바꾼다
- 독자의 이해를 돕는 구체적인 예시·비유를 추가한다
- 중요한 수치·데이터·사례는 빠짐없이 포함한다
- 복잡한 구조는 목록·표로 정리한다
- **크로스오버**: 실행마다 20개 분야 풀에서 `random.choice()`로 선택 → 프롬프트에 주입
- **슬러그**: Gemini가 front matter의 `slug:` 필드로 영문 생성 → 스크립트가 파일명으로 사용 후 필드 제거

### 알려진 동작 특성

- JS 렌더링 사이트(React/Next.js 등)는 1차 requests 추출 실패 → Jina Reader 자동 폴백
- Gemini가 `date:` 연도를 임의로 바꾸는 버그 있음 → 스크립트가 생성 후 강제 복원
- 기업 네트워크 SSL 인증서 오류 → `ssl._create_unverified_context` + requests 세션 패치로 우회
- Gemini가 한글 퍼센트 인코딩 URL 끝자락을 깨뜨리는 경우가 있음(예: `설계` → `설곳`) — 출처 섹션은 생성 후 수동 검증

### 비공개 레포 콘텐츠 처리 (Second-Brain 등)

`tigerjk9/Second-Brain` 같은 비공개 GitHub 레포의 `.md`는 blob/raw URL이 404. 로컬 클론(`C:/Users/user/Desktop/GitHub Blog/Second-Brain/`)을 `python -m http.server` 로 임시 서빙한 뒤 localhost URL을 `/paraph`에 전달한다. 처리 후 반드시 (1) 서버 종료 (2) 생성 포스트의 `<출처>` 섹션을 `tigerjk9/Second-Brain — <상대경로>` 표기로 교체. 세부 절차는 메모리 `project_paraph_private_source.md`.

---

## 교원 연수 자료 자동화 (`/yeonsu`)

`scripts/lecture_script.py`가 다양한 입력(YouTube/웹/PDF/파일)을 교원 연수용 자료로 자동 변환한다.
Claude Code에서는 `/yeonsu <입력>` 슬래시 커맨드로 호출한다 (`.claude/commands/yeonsu.md`).
설계 의도·출력 구조·수준별 원칙은 `scripts/lecture-script-prd.md` 참고.

```bash
python scripts/lecture_script.py <입력>                        # 변환 + git push
python scripts/lecture_script.py <입력1> <입력2> ...           # 복수 입력 → 하나의 아티클로 통합
python scripts/lecture_script.py <입력> --dry-run              # 출력만
python scripts/lecture_script.py <입력> --no-push              # 로컬 저장만
python scripts/lecture_script.py <입력> --duration 90          # 강의 시간 지정 (기본 120분)
python scripts/lecture_script.py <입력> --level 초급           # 수준 지정 (기본 중급)
```

입력 형식: YouTube URL, 웹 URL, PDF 경로, 텍스트/docx 파일 경로 모두 지원. **복수 입력** 시 공백으로 구분하면 모두 추출해 하나의 포스트로 통합 생성.

**Naver 블로그 URL**: `blog.naver.com` URL을 자동으로 `m.blog.naver.com`으로 변환해 모바일 UA로 스크래핑 → 로그인 없이 본문 추출 가능.

**이미지 삽입 형식 (필수)**: 포스트에 이미지를 넣을 때는 반드시 `<figure>/<figcaption>` HTML을 사용한다. 마크다운 `![alt](url)` 형식은 Minimal Mistakes 테마 CSS(`figure { display: flex }`) 때문에 캡션이 이미지 옆에 붙으므로 **절대 사용하지 않는다**.

```html
<figure>
<img src="/assets/파일명.png" alt="한국어 설명">
<figcaption>이미지 아래 캡션.</figcaption>
</figure>
```

- **환경변수**: `GEMINI_API_KEY` — `.env` 파일에서 자동 로드
- **의존성**: 기존 `requirements.txt` 공용 (추가 설치 불필요)

### 출력 구조 (탐구 에세이 형식 블로그 포스트)

본문 챕터 (`## N. 챕터 제목`):
- 에피그래프 `> *"..."*` — 저서명·연도를 즉시 댈 수 있을 만큼 확실한 경우만 `— 이름` 출처 표기. 불확실하면 경구만. 한국인 학자 이름 날조 절대 금지.
- 케이스 오프너 — 2~3문장. 교육 현장 구체 상황 + 딜레마 질문으로 끝남. 특정 인물 주인공 금지.
- 탐구 에세이 본문 — 오프너 질문에서 출발해 개념·이론·연구를 사유의 흐름으로 전개. 최소 800자.
- `**토의 활동**` — 전체 문서에서 3~5개만. 모든 챕터에 달지 않음.
- `**핵심 정리**` — 챕터 핵심 메시지 한 문장.

마지막 챕터 (갈무리):
- 앞선 챕터들의 핵심 논점 연결·종합 본문 (최소 400자)
- `**앞으로**` — 교실·학교·자기 자신에게 이어갈 방향. 처방이 아닌 가능성으로 서술.
- `**생각할 질문**` — 열린 질문 3개. 각 질문은 빈 줄로 구분된 별도 blockquote.

### 관련 포스트 자동 보강

`_posts/` 전체에서 키워드 매칭으로 유사 포스트 최대 3개를 자동 탐색해 프롬프트에 포함.
Gemini는 이 포스트들의 관점·사례를 강의 흐름에 자연스럽게 녹여 쓴다.

### 파일 구조

```
scripts/
  lecture_script.py           # 메인 스크립트
  lecture_prompt_template.txt # Gemini 프롬프트
  lecture-script-prd.md       # 설계 PRD
.claude/commands/
  yeonsu.md                   # /yeonsu 슬래시 커맨드
```

---

## 공통: AI 티 금지 표현 (4개 자동화 스크립트 전체 적용)

`/yeonsu`, `/paraph`, `/video`, `/paper` 4개 Gemini 프롬프트 템플릿 말미에 **Humanize KR v1.3.1** 기준 AI 표현 금지 규칙이 포함되어 있다.
프롬프트를 수정할 때 이 섹션을 제거하거나 축소하지 않는다.

**S1 (무조건 교체)**: `~를 통해`, `~을 넘어`, `결론적으로`, `시사하는 바가 크다`, `혁신적`, `'A'에서 'B'로` 변환 공식, 콜론 헤딩(`## 제목: 부제`), 이모지

**S2 (3회 이상 반복 시 교체)**: `또한/따라서/즉` 문두 남발, `~할 수 있다` 반복 종결, `~것이다` 종결 반복, 볼드 남용

> 출처: [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) — Humanize KR v1.3.1

## 공통: 이미지 자동 삽입

`scripts/image_fetcher.py`가 4개 자동화 스크립트(`/paper`, `/video`, `/paraph`, `/yeonsu`) 공용 모듈로 동작한다.

**이미지 소스 우선순위:**
1. **OG 이미지** — `## 출처` 섹션의 URL에서 `og:image` / `twitter:image` 추출 (가장 관련도 높음)
2. **DuckDuckGo 이미지 검색** — `duckduckgo-search` 패키지, API 키 불필요. 400×200px 이상 가로형 필터
3. **Pexels 폴백** — `PEXELS_API_KEY` 필요. 기존 동작과 동일

- **검색 쿼리**: front matter `title:` 앞 3단어 + `tags:` 앞 2개 조합 (DDG·Pexels 공통)
- **저장 위치**: `assets/{slug}-thumb.{ext}` (jpg/png/webp content-type 자동 판별)
- **삽입 위치**: front matter `header.teaser` + 본문 첫 `##` 앞 `<figure>` 블록 (alt= 포스트 title 자동 주입)
- **노출 범위**: 본문 `<figure>`로 표시 + `_includes/seo.html`에서 OG 이미지로 송출. 리스트/프리뷰 노출 없음
- **Windows cp949 주의**: `image_fetcher.py` print 문에 em dash(`-`) 사용 (em dash `—` 금지)
- **기업 SSL 우회**: requests 세션 `verify=False`, DDG는 `DDGS(verify=False)` 사용

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
