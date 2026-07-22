<div align="center">

# 닷커넥터의 지식과 경험의 발자국

**교육 · AI · 학습과학을 가로지르는 개인 기술 블로그**

논문 한 편, 유튜브 영상 하나, 웹 아티클 한 편을 넣으면 — 한국어 블로그 포스트로 나온다.
그 위에 논문리뷰를 근거로 대화하는 RAG 챗봇과 의미 기반 리서치 허브를 얹었다.

<br>

[![Live](https://img.shields.io/badge/blog-tigerjk9.github.io-2ec4cc?style=for-the-badge&logo=jekyll&logoColor=white)](https://tigerjk9.github.io) [![Posts](https://img.shields.io/badge/posts-500-4c9aff?style=for-the-badge)](https://tigerjk9.github.io) [![Research](https://img.shields.io/badge/papers-162-8e75b2?style=for-the-badge)](https://tigerjk9.github.io/research/) [![Last commit](https://img.shields.io/github/last-commit/tigerjk9/tigerjk9.github.io?style=for-the-badge&color=555)](https://github.com/tigerjk9/tigerjk9.github.io/commits/main) [![License](https://img.shields.io/badge/license-MIT-lightgrey?style=for-the-badge)](LICENSE)

<br>

[**블로그**](https://tigerjk9.github.io) · [**리서치 허브**](https://tigerjk9.github.io/research/) · [**AI에게 묻기**](https://tigerjk9.github.io/ask/) · [**지식 그래프**](https://tigerjk9.github.io/knowledge-graph/)

<br>

![Jekyll](https://img.shields.io/badge/Jekyll-CC0000?style=flat-square&logo=jekyll&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Google Gemini](https://img.shields.io/badge/Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white) ![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white) ![GitHub Pages](https://img.shields.io/badge/GitHub_Pages-222?style=flat-square&logo=githubpages&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white) ![D3.js](https://img.shields.io/badge/D3.js-F9A03C?style=flat-square&logo=d3dotjs&logoColor=white)

</div>

---

## 이 저장소는 무엇인가

[Minimal Mistakes](https://github.com/mmistakes/minimal-mistakes) Jekyll 테마(v4.27.3)를 gem이 아니라 **프로젝트 안에 직접 포함**해 자유롭게 개조한 개인 블로그이자, 그 위에 쌓아 올린 **콘텐츠 자동화 파이프라인**의 소스다. GitHub Pages로 호스팅하고, AI 챗봇 백엔드만 Vercel 서버리스로 분리했다.

콘텐츠 생성은 Claude Code 슬래시 커맨드로 호출하는 Python 스크립트가 담당하고, Gemini가 초안을 쓰며, 사람이 후처리 QA를 거쳐 커밋한다.

---

## ✨ 시그니처 기능

| | 기능 | 한 줄 소개 |
|---|------|-----------|
| 🔎 | **[리서치 허브](https://tigerjk9.github.io/research/)** | AI·교육 논문리뷰 162편을 태그·연도·키워드로 걸러 발견·시사점까지 카드에서 바로 읽는다. 의미 기반 AI 검색 포함 |
| 💬 | **[AI에게 묻기](https://tigerjk9.github.io/ask/)** | 논문리뷰 코퍼스를 근거로 답하는 RAG 챗봇. 방문자가 본인 Gemini 키를 넣으면 누구나 대화 가능(BYOK) |
| 🕸️ | **[지식 그래프](https://tigerjk9.github.io/knowledge-graph/)** | 태그 IDF 가중 엣지 + Louvain 군집을 클라이언트에서 계산하는 D3 포스 그래프 |
| 🤖 | **자동화 파이프라인** | 논문·영상·웹·연수자료를 한국어 포스트로 바꾸는 스크립트 6종 + 주간 다이제스트 cron + 네이버 블로그 자동 크로스포스팅 |

---

## 🤖 자동화 파이프라인

Claude Code에서 슬래시 커맨드로 호출하면 각 스크립트가 콘텐츠를 추출하고 Gemini로 한국어 포스트를 생성한 뒤 `_posts/`에 저장하고 커밋·푸시한다.

| 커맨드 | 입력 | 출력 | 모델 |
|--------|------|------|------|
| `/paraph` | 웹 URL (단일·복수·머지) | 패러프레이즈 포스트 | gemini-2.5-flash |
| `/video` | YouTube URL (단일·복수) | 영상 요약 포스트 | gemini-2.0-flash |
| `/paper` | PDF 논문 | 고정 6섹션 논문리뷰 | gemini-2.5-flash |
| `/yeonsu` | URL·PDF·파일 (복수 통합) | 교원 연수 탐구 에세이 | gemini-2.5-flash |
| `/edit-*` | 위와 동일 | 주인장 목소리 강화 버전 | 〃 |
| `/plain-*` | 웹·YouTube | 교육 앵커링 없는 담백한 전달 | 〃 |
| `/digest` | 지난 7일 포스트 | 주간 다이제스트 (cron 자동) | gemini-2.5-flash |
| `/naver` | `_posts/` 마크다운 | 네이버 블로그 크로스포스팅 (스케줄러 일 2회 자동) | Playwright (분류만 gemini) |

### 공통 출력 품질 규칙

모든 Gemini 프롬프트 템플릿 상단에 `[문체 절대 규칙]` 블록으로 강제된다.

| 규칙 | 내용 |
|------|------|
| **단정체 강제** | `~이다`·`~한다` (paper는 `~함`·`~됨` 명사형). 존칭 어미 전면 금지 |
| **콜론 헤딩 금지** | `title:` 및 `##` 섹션 제목에 `제목: 부제` 형식 금지 |
| **Humanize KR v2.0.0** | `~를 통해`·`~을 넘어`·`혁신적`·이모지 등 AI 티 표현 즉시 교체 |
| **날카로움 + 따뜻함** | 입장 없는 요약·"더 연구가 필요하다"식 마무리 금지, 섹션마다 뾰족한 단언 1개 |

<details>
<summary><b>/paraph — 웹 아티클 → 포스트 (3모드)</b></summary>

<br>

웹 페이지를 한국어로 **패러프레이즈**(번역 아님)해 포스트를 만든다. 단일 URL, 복수 URL 통합, 기존 포스트에 신규 자료를 녹이는 머지(`--into`) 세 모드.

```bash
python scripts/web_to_post.py <URL>                                   # 단일 → 신규 포스트
python scripts/web_to_post.py <URL1> <URL2>                           # 복수 통합 → 포스트 1개
python scripts/web_to_post.py <URL> --into _posts/YYYY-MM-DD-slug.md  # 기존 포스트에 통합
python scripts/web_to_post.py <URL> --dry-run   # 출력만
python scripts/web_to_post.py <URL> --no-push   # 로컬 저장만
python scripts/web_to_post.py <URL> --slug SLUG # 슬러그 지정
```

- 본문 추출은 requests + BeautifulSoup, 500자 미만이면 Jina Reader(`r.jina.ai`) 폴백 (JS 렌더링·접근 제한 대응)
- Naver 블로그는 `m.blog.naver.com` 자동 변환
- **머지 모드**: 기존 `date`·구조·문체·크로스오버 분야를 보존한 채 신규 자료에서 수치·비유·인용·사례·균형 관점을 채굴해 흡수. 새 글이 아니라 정밀 수술
- 마지막에 뜻밖의 분야(신경과학·행동경제학·언어학 등)와 잇는 크로스오버 섹션

</details>

<details>
<summary><b>/video — YouTube → 포스트</b></summary>

<br>

자막을 분석해 영상 흐름을 따라가는 포스트를 만든다. 단일·복수(하나로 종합) 모드.

```bash
python scripts/yt_to_post.py <URL>              # 변환 + push
python scripts/yt_to_post.py <URL1> <URL2>      # 복수 통합
python scripts/yt_to_post.py <URL> --dry-run
python scripts/yt_to_post.py <URL> --no-push
python scripts/yt_to_post.py <URL> --lang en    # 영어 자막 우선
```

- 자막 3단계 폴백: `youtube-transcript-api` → `yt-dlp` VTT → 영상 description
- `--edit` 단일 모드는 OpenCV로 영상 프레임 4장을 추출해 본문에 배치
- Gemini가 영문 slug를 생성하고, 스크립트가 `date` 연도 변조 버그를 강제 복원

</details>

<details>
<summary><b>/paper — PDF 논문 → 논문리뷰</b></summary>

<br>

`_papers/`에 PDF를 넣고 한 줄로 고정 6섹션 논문리뷰를 만든다.

```bash
python scripts/pdf_to_post.py _papers/paper.pdf            # 변환 + push
python scripts/pdf_to_post.py _papers/paper.pdf --dry-run
python scripts/pdf_to_post.py _papers/paper.pdf --keep-pdf # 원본 보존 (기본은 처리 후 삭제)
```

- 구조: 연구 목적 → 방법 → 주요 발견 → 결론 및 시사점 → 리뷰어 ADD One → 탐구 질문 + APA 출처
- PyMuPDF로 그림 최대 6개 추출 → Gemini가 본문에 배치
- **arXiv ID / DOI**: PDF 첫 2페이지에서 실제 값을 추출해 ground truth로 주입 (환각 방지). 추출 실패 시 ID 생략
- 이 출력이 **리서치 허브·AI 챗봇의 데이터 원천**이라, 후처리 QA 끝에 임베딩 재생성 단계가 붙는다

</details>

<details>
<summary><b>/yeonsu — 다양한 입력 → 교원 연수 탐구 에세이</b></summary>

<br>

YouTube·웹·PDF·텍스트/docx를 받아 현직 교사용 탐구 에세이를 만든다. 복수 입력을 하나로 통합.

```bash
python scripts/lecture_script.py <입력>
python scripts/lecture_script.py <입력1> <입력2> ...   # 복수 통합
python scripts/lecture_script.py <입력> --duration 90  # 강의 시간 (기본 120분)
python scripts/lecture_script.py <입력> --level 초급    # 수준 (기본 중급)
```

- 입력 타입 자동 감지, `_posts/`에서 관련 포스트 3개를 찾아 프롬프트에 포함
- 챕터: 에피그래프 → 케이스 오프너 → 탐구 에세이 본문 → 토의 활동 → 핵심 정리
- 이미지는 반드시 `<figure>/<figcaption>` HTML (마크다운 `![]()`는 캡션이 옆에 붙어 금지)

</details>

<details>
<summary><b>/edit-* · /plain-* — 목소리 변주 모드</b></summary>

<br>

**`/edit-*`** — 필자의 직접 판단과 절제된 비관론을 최소 2곳 살린 강화 버전. 도입부가 질문에 국한되지 않고, 억지 크로스오버는 본문에 통합하거나 생략.

| 커맨드 | 기반 |
|--------|------|
| `/edit-paraph` | `web_to_post.py --edit` |
| `/edit-video` | `yt_to_post.py --edit` |
| `/edit-paper` | `pdf_to_post.py --edit` |
| `/edit-yeonsu` | `lecture_script.py --edit` |

**`/plain-*`** — 교육 렌즈를 제거하고 주제를 원문이 정하게 하는 담백한 전달 모드. 원문 정보를 정확·빠짐없이 옮기고 개인 의견은 절제.

```bash
python scripts/web_to_post.py <URL> --plain
python scripts/yt_to_post.py <URL> --plain --model gemini-2.5-flash
```

</details>

<details>
<summary><b>/digest — 주간 다이제스트 (완전 자동)</b></summary>

<br>

지난 7일 포스트를 주제별로 재구성한 다이제스트를 만든다. GitHub Actions cron이 **매주 일요일 20:00 KST**에 생성·커밋·푸시한다 (`.github/workflows/weekly-digest.yml`).

```bash
py scripts/weekly_digest.py             # 수동 실행 + push
py scripts/weekly_digest.py --dry-run   # 출력만
py scripts/weekly_digest.py --days 14   # 기간 변경
```

- Gemini의 링크 도메인 환각을 permalink 화이트리스트로 자동 차단
- 3편 미만이면 생성 안 함, 다이제스트 자기 참조 방지

</details>

<details>
<summary><b>/naver — 네이버 블로그 크로스포스팅 (완전 자동)</b></summary>

<br>

`_posts/`의 포스트를 [네이버 블로그](https://blog.naver.com/dot_connector)에 자동 발행한다. 네이버 글쓰기 API가 2020년에 종료되어, **Playwright가 로그인된 브라우저로 스마트에디터 ONE을 직접 조작**한다. Windows 작업 스케줄러가 매일 10:00·16:00에 5편씩 자동 실행.

```bash
py -u scripts/naver_crosspost.py --limit 5     # 미게시 5편 발행
py -u scripts/naver_crosspost.py --dry-run     # 대상·분류 미리보기
py -u scripts/naver_crosspost.py --login       # 최초 1회 수동 로그인 (쿠키 백업)
py -u scripts/naver_crosspost.py --update <logNo> --post <파일>  # 기존 글 본문 교체
```

- **카테고리 자동 분류**: Gemini가 전체 포스트를 3개 카테고리(인공지능교육 인사이트·뇌기반 학습 과학·생각하는 교실, 깊이있는 학습)로 일괄 의미 분류해 캐시. 수동 교정 우선
- **마루부리 15 서체**: 붙여넣기 HTML의 인라인 `font-size:15px`가 에디터 크기로 매핑되고(소제목 19 유지), 전체 선택 후 서체 드롭다운으로 마루부리 적용
- **가독성 여백**: 네이버 에디터는 문단 여백이 없어 블록 요소 사이에 빈 문단을 자동 삽입
- 표·볼드·소제목·이미지가 에디터 네이티브 컴포넌트로 변환, 글 끝에 원 작성일 + 원문 링크 자동 삽입
- 발행 이력 상태 파일로 중복 방지, 발행 URL은 모바일 API 제목 대조로 자동 기록

</details>

---

## 🧩 커스텀 기능 상세

### 🔎 리서치 허브 — `/research/`

AI·교육 논문리뷰 **162편**을 태그·연도·키워드로 탐색하는 전용 페이지. 그라디언트 히어로 + 통계 행(논문리뷰·원문 링크·태그·연도 범위) + 카드 인라인 확장 UI.

- **데이터**: `scripts/build_research_db.py`가 논문리뷰 포스트를 2계층(고정 6섹션 / 자유 구조)으로 파싱해 `assets/research-db.json` 정적 생성
- **카드 확장**: 연구 목적·주요 발견·시사점·탐구 질문을 원문 이동 없이 읽고 arXiv/DOI 원문으로 바로 이동
- **AI 시맨틱 검색**: 질문하듯 검색하면 gemini-embedding(int8 양자화) 코사인 유사도로 재정렬
- **격리**: 사이드바·지식 그래프·검색·카테고리 카운트에 침투 0건

### 💬 AI에게 묻기 — `/ask/`

논문리뷰 코퍼스를 근거로 답하는 RAG 챗봇. 답변의 모든 주장에 근거 논문이 `[n]` 인용으로 붙고, 근거가 없으면 없다고 답한다.

- **백엔드**: `research-ask/` — 의존성 제로 Vercel 서버리스. 블로그 정적 파일(DB + 임베딩 인덱스)을 콜드스타트에 로드·6h 캐시 → **콘텐츠가 늘어도 재배포 불필요**
- **방문자 BYOK**: 본인 Gemini API 키(Google AI Studio 무료 발급)를 넣으면 누구나 대화 가능. 키는 브라우저에만 저장되고 Google에 직접 검증(서버 미경유), 호출 비용은 방문자 키 부담
- **주인장 모드**: 접근 키(`ASK_ACCESS_KEY`)로 입장하면 서버 Gemini 키로 동작 (일일 사용량 보호 포함)
- **유사도 게이트**: 무관 질의(top1 0.5~0.6)를 절대 컷 + top1 게이트로 걸러 생성 호출 없이 차단

### 🕸️ 지식 그래프 — `/knowledge-graph/`

포스트를 노드로 하는 D3 v7 2D 포스 그래프. 엣지·군집을 전부 클라이언트에서 계산한다.

- **엣지**: 태그 IDF 가중 + 노드당 top-K(8) 가지치기 (흔한 허브 태그 디스카운트)
- **군집**: 연결 구조 Louvain 군집 탐지(직접 구현), 자동 라벨은 군집 내 태그빈도 × IDF 상위
- Liquid 템플릿이 노드만 출력해 페이로드 5MB → 236KB로 경량화

### 🎨 그 외 UI

<details>
<summary>다크/라이트 토글 · 본문 복사 · 읽기 진행줄 · 모바일 TOC · 조회수 배지 …</summary>

<br>

| 기능 | 구현 |
|------|------|
| 다크/라이트 모드 토글 | `theme-toggle.js` — `html[data-theme="light"]` 레이어, FOUC 방지 인라인 스크립트 |
| 본문 복사 / 링크 복사 | `post-copy.js` — 본문에 `원문링크:` 자동 삽입, 한글 URL 디코딩 |
| 접이식 사이드바 섹션 | `sidebar-toggle.js` (`initSectionCollapse`) — localStorage 상태 유지 |
| 읽기 진행 표시줄 | `reading-progress.js` |
| 모바일 TOC 드로어 | `mobile-toc.js` |
| 맨 위로 버튼 | `back-to-top.js` |
| 조회수 카운터 | `myhits.vercel.app` 배지 |
| 웰빙 코너 | `wellbeing.js` (모듈별 try/catch 격리) |
| NE 수업 디자이너 | `tools/ne-designer/` — 책·인물·곤란을 입력하면 노벨 엔지니어링 7단계 수업 계획과 Gems 캐릭터 프롬프트(안전 가드레일 포함)를 만들어 주는 정적 단독 페이지 |

`tools/<슬러그>/index.html`은 front matter 없이 정적 파일로 그대로 배포되어, 테마 CSS·사이드바 스크립트의 간섭 없이 자체 완결 도구를 올릴 수 있다.

상단 네비게이션은 `_data/navigation.yml`에서 외부 서비스([쉼표](https://comma-for-wellbeing.vercel.app/) · [기록 대화](https://dotconnector-log.vercel.app/) · [말씀의 길](https://malsseum-ui.vercel.app/))로 직접 연결된다.

> ⚠️ 커스텀 페이지 스타일은 반드시 컨테이너 ID로 스코프한다 — 테마의 `html[data-theme="light"] a` 규칙이 버튼형 앵커를 덮어 파란 배경+파란 글자가 되는 함정이 있다.

</details>

---

## 📚 강의자료 아카이브 — `/lectures/`

블로그 본문(`_posts`)과 완전히 분리된 별도 Jekyll collection. 강의 한 건당 허브 1장 + 기능 페이지 N개 + 원본 슬라이드·핸드아웃·OG 커버 한 묶음으로 큐레이션한다.

```
/lectures/                            아카이브 인덱스
/lectures/<slug>/                     강의 허브 (개요·다운로드·기능 트랙)
/lectures/<slug>/<feature>/           기능 페이지
/assets/lectures/<slug>/slides.html   Reveal.js 풀스크린
/assets/lectures/<slug>/handout.html  A4 핸드아웃
/assets/lectures/<slug>/cover.jpg     OG 커버 (1200×630)
```

- **격리 모드**: `_posts` 사이드바·지식 그래프·검색·카테고리 카운트에 침투 0건
- **첫 사례**: `claude-code-edu` — Claude Code 실무 활용 교육자 워크숍. K-12 교사·연구자 듀얼 트랙으로 22개 기능 슬라이드 + 7면 핸드아웃
- **외부 링크형 카드**: 별도 배포된 자료(공교육 AX 핸드북·학생용 생성형 AI 안내서·AIEP 계정 관리 튜토리얼)는 허브 카드에서 바로 외부 사이트로 연결. 표지는 사이트 히어로 스크린샷
- **도서 원고 섹션**: Book-Publisher 완성 원고 7권을 링크 카드로 편입(`_data/books.yml`). 카드를 누르면 라이브 Vercel 웹 도서가 새 탭으로 열리고, 원고 개정 시 웹 도서만 재배포하면 된다. 통일 표지는 `scripts/gen_book_covers.py`로 생성, 카드에 저자 크레딧 표시

---

## ⚙️ 시작하기

```bash
# 1) Ruby 의존성 (Jekyll)
bundle install

# 2) Python 의존성 (자동화 스크립트 공통)
pip install -r scripts/requirements.txt

# 3) API 키 (.env는 gitignore)
cp .env.example .env
```

`.env` 형식 — 모든 자동화 스크립트가 여기서 자동 로드:

```dotenv
GEMINI_API_KEY=AIza...
PEXELS_API_KEY=...   # 이미지 자동 삽입 (없으면 DuckDuckGo 폴백)
```

로컬 개발:

```bash
bundle exec jekyll serve   # http://localhost:4000
bundle exec jekyll build   # 사이트 빌드
bundle exec rake preview   # 테마 테스트
```

---

## 🗂️ 프로젝트 구조

```
_posts/            블로그 포스트 (YYYY-MM-DD-slug.md)
_papers/           논문 PDF 원본 (/paper 입력, gitignore)
_lectures/         강의자료 collection (격리)
assets/            이미지 (flat) + research-*.json (허브·챗봇 데이터)
research-ask/       AI 챗봇 백엔드 (Vercel 서버리스, 의존성 제로)
scripts/
  web_to_post.py            /paraph, /plain-paraph, /edit-paraph
  yt_to_post.py             /video, /plain-video, /edit-video
  pdf_to_post.py            /paper, /edit-paper
  lecture_script.py         /yeonsu, /edit-yeonsu
  weekly_digest.py          /digest (+ GitHub Actions cron)
  build_research_db.py      논문리뷰 → research-db.json
  build_embeddings.py       임베딩 인덱스 (허브 검색 + RAG)
  image_fetcher.py          이미지 공용 모듈 (OG→Pexels→DDG)
  *_prompt_template.txt     각 스킬별 Gemini 프롬프트
.claude/commands/  슬래시 커맨드 정의
.github/workflows/ CI + 주간 다이제스트 cron
_config.yml        사이트 설정 (timezone: Asia/Seoul 필수)
_data/navigation.yml  상단 메뉴
```

---

## 🔧 주요 설정값

| 항목 | 값 |
|------|----|
| 테마 | Minimal Mistakes v4.27.3 (dark skin) |
| locale / timezone | ko-KR / Asia/Seoul |
| 검색 | Lunr.js |
| 댓글 | Giscus (기본 비활성) |
| 분석 | Google Analytics `G-Y8TNBPZQEZ` |
| 호스팅 | GitHub Pages (블로그) + Vercel (AI 챗봇 백엔드) |

---

<div align="center">

이 블로그는 [**Minimal Mistakes**](https://github.com/mmistakes/minimal-mistakes) (Michael Rose, MIT License)를 기반으로 한다.

**[김진관 · 닷커넥터](https://tigerjk9.github.io)** 가 만들고 기록한다.

</div>
