# tigerjk9.github.io

[![Jekyll](https://img.shields.io/badge/jekyll-%3E%3D%203.7-blue.svg)](https://jekyllrb.com/)
[![GitHub Pages](https://img.shields.io/badge/hosted-GitHub%20Pages-brightgreen.svg)](https://tigerjk9.github.io)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)

교육, AI, 학습과학을 중심으로 다양한 분야를 넘나드는 개인 블로그.
[https://tigerjk9.github.io](https://tigerjk9.github.io)

Minimal Mistakes Jekyll 테마(v4.27.3) 기반. 테마 파일을 gem 대신 프로젝트 내 직접 포함.

---

## 자동화 파이프라인

### `/paraph` — 웹 아티클 → 블로그 포스트

웹 페이지 URL을 주면 내용을 한국어로 패러프레이즈해 Jekyll 포스트를 자동 생성한다.
**3가지 모드**를 지원한다 — 단일 URL 변환, 복수 URL 통합, 그리고 기존 포스트에 신규 자료를 녹이는 머지 모드(`--into`).

```bash
python scripts/web_to_post.py <URL>                              # 단일 출처 → 신규 포스트
python scripts/web_to_post.py <URL1> <URL2>                      # 복수 출처 통합 → 신규 포스트 1개
python scripts/web_to_post.py <URL> --into _posts/YYYY-MM-DD-slug.md  # 기존 포스트에 통합·덮어쓰기
python scripts/web_to_post.py <URL> --dry-run                    # 파일 저장 없이 출력만
python scripts/web_to_post.py <URL> --no-push                    # 로컬 저장만
python scripts/web_to_post.py <URL> --slug my-slug               # 슬러그 직접 지정
```

Claude Code에서는 `/paraph <URL> [URL2 ...] [--into PATH]` 스킬로 호출한다.

**동작 순서**

1. `.env`에서 `GEMINI_API_KEY` 자동 로드
2. 각 URL에서 제목·본문 추출 (requests + BeautifulSoup)
3. 본문 500자 미만이면 Jina Reader(`r.jina.ai`) 폴백 — JS 렌더링 사이트·접근 제한 도메인 대응
4. 기존 포스트에서 카테고리·태그 수집
5. 모드별 프롬프트 선택:
   - 단일: `web_prompt_template.txt` + 랜덤 크로스오버 분야
   - 복수: `web_multi_prompt_template.txt` + 랜덤 크로스오버 분야
   - 머지: `web_merge_prompt_template.txt` (기존 크로스오버 분야 보존)
6. Gemini(`gemini-2.5-flash`)로 한국어 포스트 생성
7. `_posts/`에 저장(신규) 또는 기존 파일 덮어쓰기(머지) → git commit + push

**포스트 스타일** (`/paraph` 전용)

- **패러프레이즈**: 원문 이해 후 재서술. 번역 금지. 처음부터 새로 쓴다.
- **복수 URL 통합**: 각 출처의 핵심 논점을 목차식 나열 없이 하나의 흐름으로 재구성
- **교육 전문가 컨셉**: 전문 용어를 쉽게 풀고, 한국 교육 맥락 예시 추가
- **크로스오버**: 뜻밖의 분야와 연결하는 마지막 섹션 (신경과학·행동경제학·언어학·복잡계 이론 등 풀)
- **문체**: `~이다`, `~한다` 단정체

**머지 모드(`--into`) 핵심 원칙**

기존 포스트의 정체성을 보존한 채 신규 자료를 흡수한다. 새 글을 만드는 것이 아니라 정밀 수술이다.

- 기존 `date`·구조·문체·크로스오버 분야 절대 보존 (SEO 슬러그·발행 시각 유지)
- 신규 자료에서 채굴 우선순위: **수치·통계 → 비유·은유 → 인용·출처 → 사례·실험 → 균형 관점·비판 → 구조적 대안**
- 새 섹션 신설은 (a) 비판적 균형, (b) 분류 체계 확장, (c) 기존 어디에도 못 들어가는 독자적 관점일 때만 정당
- 커밋 메시지는 `Update:` 접두어 (신규 모드는 `Add:`)

---

### `/video` — YouTube → 블로그 포스트

YouTube URL을 주면 자막을 분석해 Jekyll 포스트를 자동 생성한다.
**3가지 모드**: 단일 URL 변환, 복수 URL 통합(하나의 포스트로 종합), 영어 자막 우선.

```bash
python scripts/yt_to_post.py <YouTube_URL>                      # 변환 + git push
python scripts/yt_to_post.py <URL1> <URL2>                      # 복수 영상 통합 → 포스트 1개
python scripts/yt_to_post.py <YouTube_URL> --dry-run            # 파일 저장 없이 출력만
python scripts/yt_to_post.py <YouTube_URL> --no-push            # 로컬 저장만
python scripts/yt_to_post.py <YouTube_URL> --lang en            # 영어 자막 우선
```

Claude Code에서는 `/video <URL> [URL2 ...]` 스킬로 호출한다.

**동작 순서**

1. `.env`에서 `GEMINI_API_KEY` 자동 로드
2. `yt-dlp`로 각 영상 메타데이터(제목·채널·업로드 날짜) 수집
3. 자막 3단계 폴백: `youtube-transcript-api` → `yt-dlp` VTT → 영상 description
4. 모드별 프롬프트 선택:
   - 단일: `yt_prompt_template.txt` + 랜덤 크로스오버 분야
   - 복수: `yt_multi_prompt_template.txt` + 랜덤 크로스오버 분야
5. Gemini(`gemini-2.0-flash`)로 한국어 포스트 생성 (영문 slug 포함)
6. `_posts/YYYY-MM-DD-{slug}.md` 저장 → git commit + push

**포스트 스타일** (`/video` 전용)

- **문체**: `~이다`, `~한다` 단정체. 존칭·명사형 어미(`~입니다`, `~함`, `~됨`) 금지
- **분량**: 자막 내용을 빠짐없이 다룬다. 생략 없음
- **구조**: 도입부 → 본문(자유 섹션) → 크로스오버 섹션 → 출처
- **복수 URL 통합**: 각 영상을 순서대로 나열하지 않고 공통 주제·대비 관점·보완 논점을 하나의 흐름으로 재구성
- **크로스오버**: 실행마다 20개 분야 풀(신경과학·행동경제학·언어학·음악이론·스포츠과학 등)에서 `random.choice()`로 선택 → 본문 끝에 3~5문장으로 짧게 수록

---

### `/yeonsu` — 다양한 입력 → 교원 연수 탐구 에세이

YouTube URL, 웹 페이지, PDF 논문, 텍스트 파일을 주면 내용을 분석해 현직 교사를 위한 탐구 에세이 형식의 블로그 포스트를 자동 생성한다.

```bash
python scripts/lecture_script.py <입력>                          # 변환 + git push
python scripts/lecture_script.py <입력1> <입력2> ...             # 복수 입력 → 하나의 아티클로 통합
python scripts/lecture_script.py <URL or 파일> --dry-run         # 파일 저장 없이 출력만
python scripts/lecture_script.py <URL or 파일> --no-push         # 로컬 저장만
python scripts/lecture_script.py <URL or 파일> --duration 90     # 강의 시간 지정 (기본 120분)
python scripts/lecture_script.py <URL or 파일> --level 초급      # 수준 지정 (기본 중급)
```

Claude Code에서는 `/yeonsu <입력>` 스킬로 호출한다. 입력값이 확인되면 시간·수준을 묻지 않고 기본값(120분/중급)으로 즉시 실행한다.
**복수 입력**: 여러 URL/파일을 공백으로 구분하면 모두 추출해 하나의 포스트로 통합 생성한다.

**입력 형식**

| 입력 타입 | 감지 조건 | 추출 방법 |
|-----------|-----------|-----------|
| YouTube URL | `youtube.com` 또는 `youtu.be` 포함 | youtube-transcript-api → yt-dlp VTT → description |
| 웹 URL (일반) | `http(s)://`로 시작 | requests + BeautifulSoup → Jina Reader 폴백 |
| 웹 URL (Naver 블로그) | `blog.naver.com` 포함 | `m.blog.naver.com`으로 자동 변환 후 모바일 UA 추출 |
| PDF | `.pdf` 확장자 | pdfplumber → PyMuPDF |
| 기타 파일 | 위 외 모든 경로 | python-docx → 텍스트 읽기 |

**동작 순서**

1. `.env`에서 `GEMINI_API_KEY` 자동 로드
2. 입력 타입 자동 감지 → 콘텐츠 추출
3. `_posts/` 전체에서 키워드 매칭으로 관련 포스트 최대 3개 탐색 → 프롬프트에 포함
4. 강의 시간에 맞는 챕터 수 자동 계산 (챕터당 평균 45분)
5. Gemini(`gemini-2.5-flash`)로 탐구 에세이 생성
6. `_posts/YYYY-MM-DD-{slug}.md` 저장 → git commit + push

**출력 파일**

| 파일 | 위치 | 용도 |
|------|------|------|
| `.md` | `_posts/` | 블로그 포스트 (Jekyll) |

**포스트 구조**

본문 챕터 (`## N. 챕터 제목`):
- **에피그래프** `> *"..."*` — 확인 가능한 인용만 `— 이름` 출처 표기. 불확실하면 경구만. 한국인 학자 이름 날조 금지.
- **케이스 오프너** — 2~3문장. 교육 현장 구체 상황 + 딜레마 질문으로 끝남. 특정 인물 주인공 금지.
- **탐구 에세이 본문** — 오프너 질문에서 출발해 개념·이론·연구를 사유의 흐름으로 전개. 최소 800자.
- **토의 활동** — 전체 문서에서 3~5개만.
- **핵심 정리** — 챕터 핵심 메시지 한 문장.

마지막 챕터 (갈무리):
- 앞선 챕터들의 핵심 논점 연결·종합 본문 (최소 400자)
- **앞으로** — 교실·학교·자기 자신에게 이어갈 방향. 처방이 아닌 가능성으로 서술.
- **생각할 질문** — 열린 질문 3개. 각 질문은 빈 줄로 구분.

**수준별 작성 방식**

- **초급**: 핵심 개념 2~3개에 집중. 비유·실생활 예시 중심. 전문 용어 필수 풀이.
- **중급**: 전체 개념 다룸. 심화 적용·비판적 시각. 연구 결과·데이터 직접 인용.

**이미지 삽입 형식**: 포스트에 이미지를 넣을 때는 반드시 `<figure>/<figcaption>` HTML 형식을 사용한다. 마크다운 `![alt](url)` 형식은 캡션이 이미지 옆에 붙으므로 절대 사용하지 않는다.

```html
<figure>
<img src="/assets/파일명.png" alt="한국어 설명">
<figcaption>이미지 아래 캡션.</figcaption>
</figure>
```

---

### `/paper` — PDF 논문 → 블로그 포스트

`_papers/`에 PDF를 넣고 명령어 한 줄로 한국어 포스트를 자동 생성한다.  
Claude Code에서는 `/paper <PDF경로>` 스킬로 호출한다.

```bash
python scripts/pdf_to_post.py _papers/paper.pdf           # 변환 + git push
python scripts/pdf_to_post.py _papers/paper.pdf --dry-run
python scripts/pdf_to_post.py _papers/paper.pdf --no-push
```

**동작 순서**

1. `.env`에서 `GEMINI_API_KEY` 자동 로드
2. PyMuPDF로 300×200px 이상 이미지 최대 6개 추출 → `assets/` 저장
3. pdfplumber로 텍스트 추출 (최대 100,000자)
4. Gemini(`gemini-2.5-flash`)로 한국어 포스트 생성 (멀티모달)
5. `_posts/YYYY-MM-DD-{slug}.md` 저장 → git commit + push

**포스트 스타일** (`/paper` 전용)

- **구조 고정**: 연구 목적 → 연구 방법 → 주요 발견 → 결론 → ADD One → 탐구 질문 + APA 출처
- **APA 출처**: URL/DOI 미포함 — LLM이 생성하는 링크는 신뢰할 수 없으므로 텍스트만 기재
- **Figure**: 논문 이미지가 본문 적절한 위치에 자동 삽입됨

---

## 환경 설정

```bash
# Ruby 의존성 (Jekyll)
bundle install

# Python 의존성 (/paper, /video 스크립트 공통)
pip install -r scripts/requirements.txt

# API 키 설정 (.env는 gitignore 등록됨)
cp .env.example .env
# .env 파일에 GEMINI_API_KEY=AIza... 입력
```

**`.env` 형식** — `/paraph`, `/paper`, `/video`, `/yeonsu` 네 스크립트 모두 이 파일에서 자동 로드

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
_papers/         # 논문 PDF 원본 (/paper 스크립트 입력)
assets/          # 이미지 (flat, 서브디렉토리 없음)
scripts/
  web_to_post.py                # /paraph — 웹 아티클 → 포스트 변환 (단일/복수/머지 3모드)
  web_prompt_template.txt       # /paraph 단일 URL용 Gemini 프롬프트
  web_multi_prompt_template.txt # /paraph 복수 URL 통합용 Gemini 프롬프트
  web_merge_prompt_template.txt # /paraph --into 머지 모드용 Gemini 프롬프트
  yt_to_post.py                 # /video — YouTube → 포스트 변환 (단일/복수 2모드)
  yt_prompt_template.txt        # /video 단일 URL용 Gemini 프롬프트
  yt_multi_prompt_template.txt  # /video 복수 URL 통합용 Gemini 프롬프트
  pdf_to_post.py                # /paper — PDF → 포스트 변환
  prompt_template.txt           # /paper Gemini 프롬프트 (URL 미포함 규칙 명시)
  lecture_script.py             # /yeonsu — 다양한 입력 → 탐구 에세이 변환
  lecture_prompt_template.txt   # /yeonsu Gemini 프롬프트 (탐구 에세이·케이스 오프너 구조 포함)
  lecture-script-prd.md         # /yeonsu 설계 PRD
  requirements.txt              # Python 의존성 (네 스크립트 공통)
.claude/
  commands/
    paraph.md          # /paraph 슬래시 커맨드 정의
    video.md           # /video 슬래시 커맨드 정의
    paper.md           # /paper 슬래시 커맨드 정의
    yeonsu.md          # /yeonsu 슬래시 커맨드 정의
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
- 연속 빈 줄 3개 이상 → 1개로 압축 (번호 항목 사이 빈 줄 1개는 유지)

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
