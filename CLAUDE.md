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

**Knowledge Graph** (`/knowledge-graph/`):
- 페이지: `knowledge-graph.md` (layout `wide`). D3 v7 2D force 그래프 (Three.js/3d-force-graph 아님)
- 데이터: Liquid 템플릿 `knowledge-graph.json`이 **노드(포스트)만** 출력 (노드 id = `date+slug`로 고유화, url은 링크 전용). 구버전의 O(N²) 엣지 이중루프와 `graph-data.json`(dead code)은 제거됨 → 페이로드 5MB→236KB
- 엣지·군집은 전부 클라이언트 계산: 엣지 = 태그 IDF 가중 + 노드당 top-K(8) 가지치기(흔한 허브 태그 디스카운트) / 색·분류 = 연결 구조 Louvain 군집 탐지(클라 직접 구현, 자동 라벨 = 군집내 태그빈도×IDF 상위). forceLink 레이아웃 + degree 비례 노드 반경 + 동적 centroid 라벨 칩
- 검증 하네스 `.omc/kg-eval/`(gitignore, Ruby 부재 환경에서 Python 산출 재현 + gstack browse 헤드리스). 설계·품질 루브릭은 메모리 `project_knowledge_graph` 참고

**리서치 허브** (`/research/`):
- 페이지: `research.md` (layout `default` — 사이트 내비·푸터 유지, 저자 사이드바 없음). 자체 완결 `<style>`/`<script>`, `#rh-app` 스코프. 테마 대응(다크 기본 + `html[data-theme="light"] #rh-app` 오버라이드). 스크립트는 `{% raw %}` 래핑(Liquid 안전)
- 데이터: `scripts/build_research_db.py`가 **2계층**으로 파싱 → `assets/research-db.json` (2026-07 기준 147편). ① structured — '리뷰어의 ADD' 헤딩 보유 고정 6섹션(/paper 출력, 100편) ② article — 자유구조(/edit-paper 등, 47편)는 실제 H2(부족하면 H3) 헤딩 그대로 섹션화. **대상 판정 3신호**: ADD 헤딩 ∪ `논문리뷰` 태그 ∪ **출처 블록의 arXiv/DOI**(edit-paper 출력 일부가 태그 없이 생성되는 것 포착 — 단 본문 폴백은 오탐이라 블록 발견만 인정). **sections는 `[{key,label,body}]` 배열 스키마** (research.md·build_embeddings.py·research-ask ask.js 모두 이 스키마 소비 — 바꾸면 셋 다 함께 수정+서비스 재배포)
- 파서 설계: 섹션 원자화 금지·텍스트 블롭 보존(h2/h3·번호 off-by-one·존칭/단정체 편차 흡수). structured 매핑은 번호 아닌 **헤딩 키워드**(목적/방법/발견/결론/ADD/탐구, '목적 및 방법' 결합 헤딩은 목적 우선). article은 출처류 헤딩 제외 최대 10섹션, 요약은 첫 헤딩 앞 도입부. 출처 6종 포맷(`## 출처`·`_**출처:**_`·`**출처**:`·`### 📚 APA`) 유연 추출 후 arXiv/DOI 정규식. 요약은 본문에서 추출(생성·환각 금지)
- UI: 태그 칩 AND 필터 + 연도 + 키워드 검색(제목·요약·발견·시사점) + 정렬. 카드 인라인 확장(마크다운 라이트 렌더 — 볼드·불릿·`####` 소제목·인용·**표**·링크). 원문 링크(arXiv/DOI) + 블로그 링크
- **재생성 필수 (2단계)**: 논문리뷰 포스트를 새로 올리거나 수정하면 `py scripts/build_research_db.py` → `py scripts/build_embeddings.py` 순서로 재실행 → `assets/research-db.json`·`research-emb-posts.json`·`research-rag-index.json` 커밋. `/paper` 후처리 QA 마지막에 이 단계를 추가한다(안 하면 허브·AI 검색·챗봇이 신규 글을 누락). 임베딩은 텍스트 해시 기반 증분이라 신규 포스트 분량만 API 호출
- 격리: `research.md`는 front matter에 `categories`/`tags` 없음 → 사이드바·카테고리/태그 페이지·지식그래프에 침투 0건. 검증은 `bundle exec jekyll build && ls _site/categories | wc -l` 카운트가 추가 전후 동일해야 함

**AI 시맨틱 검색 + RAG 챗봇** (`/research/` AI 모드 · `/ask/`):
- 백엔드: `research-ask/` — 의존성 제로 Vercel 서버리스(Gemini REST 직접 호출). `api/health`(프로브)·`api/embed`(쿼리 임베딩)·`api/ask`(RAG 답변). 블로그 정적 파일(`research-db.json`+`research-rag-index.json`)을 콜드스타트에 fetch·6h 캐시 → **콘텐츠가 늘어도 서비스 재배포 불필요**. `_config.yml` exclude 등록(Jekyll 빌드 제외)
- 임베딩: `scripts/build_embeddings.py` — gemini-embedding-001 768차원, 포스트당 overview+6섹션 청크(현재 ~700청크), int8 양자화(per-vector scale, base64). `research-emb-posts.json`(허브 클라 코사인용 ~108KB) + `research-rag-index.json`(RAG용 ~765KB)
- **유사도 게이트 (중요)**: gemini-embedding은 무관 질의도 top1 0.5~0.6이 나옴(실측: 김치찌개 0.52, 주식 0.60, 관련 질의 0.79). 절대 컷 하나로는 판별 불가 → `ask.js` MIN_SIM 0.6 + TOP_GATE 0.63, `research.md` AI_TOP_GATE 0.62 + top1 대비 상대 컷 0.08. 무관 질문은 생성 호출 없이 차단
- **thinking 토큰 함정**: gemini-2.5-flash는 thinking이 기본 켜져 있어 maxOutputTokens를 소진해 답변이 잘림 → `generationConfig.thinkingConfig.thinkingBudget: 0` 필수 (`lib/store.js`)
- **라이트모드 가독성 함정 (CRITICAL)**: `main.scss`의 `html[data-theme="light"] a { color: #0078c8 }`(특이성 0,1,1)가 커스텀 페이지 버튼형 앵커의 흰 텍스트(단일 클래스 0,1,0)를 덮어 **파란 배경+파란 글자**가 됨 (2026-07-03 챗봇에서 실측). research.md·ask.md는 전 셀렉터에 `#rh-app`/`#ask-app` ID 프리픽스(1,1,0)로 방어 완료. **새 커스텀 페이지를 만들 땐 반드시 컨테이너 ID 프리픽스로 스타일을 스코프**할 것. 챗봇 인용 `[n]`은 단락당 1회만 붙도록 프롬프트에 명시(문장마다 붙으면 가독성 붕괴)
- 프론트: `research.md` AI 검색 토글(Enter 실행, 유사도순 재정렬) + `ask.md` 챗 UI(`[n]` 인용→출처 링크, 출처 카드, sessionless). 둘 다 `/api/health` 프로브 성공 시에만 AI UI 노출 — **서비스 미배포여도 사이트는 완전 정상**
- **배포 완료 (2026-07-03)**: 프로덕션 `https://dotconnector-ask.vercel.app` (팀 `dot-connectors-projects-282d6187` / 프로젝트 `dotconnector-ask` — 코드의 `ASK_API` 상수와 일치). **이 머신은 컴퓨터 이름이 한글이라 `vercel login`이 ByteString 오류로 실패** → `.env`의 `VERCEL_TOKEN`으로 우회. 재배포(코드 수정 시에만 — 데이터 갱신은 불필요): `cd research-ask && npx vercel deploy --prod --yes --scope dot-connectors-projects-282d6187 --token <VERCEL_TOKEN>`. 비대화 모드는 `--scope` 명시 필수
- 남용 방지: CORS 허용(블로그+localhost), 인스턴스 로컬 레이트리밋(ask 6/min·400/day), 질문 500자·답변 2000토큰 상한. 트래픽 증가 시 Upstash 교체
- **주인장 전용 모드 (2026-07-03, API 비용 통제)**: Vercel env `ASK_ACCESS_KEY` 설정 시 embed/ask는 `X-Ask-Key` 헤더 필수(401), health가 `authRequired`/`authorized`를 반환. 블로그 UI는 미인증 방문자에게 AI 토글·CTA를 숨기고, `/ask/` 방문 시 잠금 안내+키 입력 폼 표시. **키는 `.env`의 `ASK_ACCESS_KEY`** — 주인장이 기기당 1회 `/ask/`에서 입력하면 localStorage(`dc_ask_key`) 저장, 허브 AI 검색도 같은 키 공유. 허브 키워드 탐색은 전면 공개 유지(클라이언트 연산, 비용 0). 키 제거하면 공개 모드로 복귀. 로컬 하네스는 키 자동 첨부(`--no-key`로 미인증 시뮬레이션)
- 로컬 E2E: `node research-ask/test/local-harness.mjs "질문"` (`--embed`·`--health` 모드 지원, .env 키 자동 로드, 블로그 fetch를 로컬 파일로 몽키패치)

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
| 웰빙 코너 | `assets/js/wellbeing.js`, `wellbeing.md`, `_includes/footer.html`, `assets/css/main.scss` |

**다크/라이트 모드**: `html[data-theme="light"]` CSS 레이어 방식. 컴파일된 dark skin 위에 light 오버라이드 덮기. anti-FOUC 인라인 스크립트를 `_includes/head.html` CSS `<link>` 이전에 삽입. `theme-toggle.js`는 이벤트 위임 방식 — masthead와 모바일 사이드바의 `.theme-toggle` 버튼 모두 처리.

**모바일 사이드바**: `injectMobileSidebarHeader()`가 사이드바 최상단에 `.sidebar-mobile-header`(테마 토글 포함)를 주입. iOS Safari dvh 버그는 `height: 100dvh; max-height: 100dvh`로 수정.

**본문 복사**: `.page__content` DOM 클론 → `.sidebar__right`, `[rel="permalink"]`, `.sr-only` 제거 → `innerText` 복사. 복사 텍스트에 `원문링크: <decoded URL>` 자동 삽입 (`## 출처` 섹션 앞, 없으면 맨 끝). URL은 `decodeURIComponent(window.location.href)`로 한글 디코딩.

**출처 섹션**: 모든 자동화 포스트의 출처는 `## 출처` 헤딩으로 통일 (기존 `<출처>` 태그 폐기). 프롬프트 템플릿 7개 + 기존 포스트 54개 일괄 변환 완료 (2026-04-28).

**링크 복사**: 포스트 URL만 단독 복사. raw `window.location.href` 사용 (NFC 인코딩 형태). iOS Safari는 한글을 NFD로 클립보드에 저장해 카카오톡·메모앱 등 NFC 기대 환경에서 깨지므로 디코딩된 한글 URL은 모바일에서 위험. 본문 복사 안의 "원문링크:" 표시는 사람이 읽는 텍스트라 디코딩 유지. 버튼은 `.post-copy-wrap` flex 컨테이너에 본문 복사 버튼과 나란히 배치 (모바일에서는 세로 스택).

**사이드바 섹션 높이**: 데스크톱 `max-height: calc(50vh - 175px) !important` — 두 섹션 합산 시 페이지네이션 라인 근방에서 끝남. 내부 스크롤(얇은 4px 스크롤바) 유지.

**웰빙 코너**: `assets/js/wellbeing.js`가 IIFE `(function(W){...})(window.WB = window.WB || {})`로 실행됨. 내부 `$` 헬퍼는 `id => document.getElementById(id)` (jQuery 아님). `W.init()`에서 각 모듈 호출을 개별 `try/catch`로 래핑해 한 모듈 오류가 나머지에 영향 없음.
- **`/wellbeing/` 페이지**: `wellbeing.md` — meta refresh + JS로 `https://comma-for-wellbeing.vercel.app/` 즉시 리디렉트. 상단 네비게이션 "쉼표" 메뉴도 동일 외부 URL 직접 연결
- **푸터**: `_includes/footer.html` — 로고+저작권만. `max-width:400px; margin:0 auto; text-align:center` 인라인 style 컨테이너로 중앙 정렬. CSS 클래스 방식은 인라인 style에 특이성이 져서 HTML 인라인으로 직접 지정
- **네비게이션** (`_data/navigation.yml`): 쉼표(comma-for-wellbeing.vercel.app), 기록 대화(dotconnector-log.vercel.app), 말씀의 길(malsseum-ui.vercel.app) 외부 링크 포함

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
- **Figure 자동 추출**: PyMuPDF로 300×200px 이상 이미지 최대 6개 추출 → `assets/` 저장 → Gemini가 본문에 배치. `fetch_and_inject_image`는 `inject_body=False`로 호출해 본문 중복 삽입 방지 (teaser만 주입)
- **Figure 참조 환각 후처리 (필수)**: Gemini가 실제 추출본 수(최대 6개)를 초과하는 `fig-7`·`fig-8` 등을 본문 `<figure>`에 참조하는 환각이 잦다(추출본 일부는 미사용으로 남음). 스크립트가 그대로 commit·push하므로 배포 시 404. `/paper` 실행 직후 **항상** 본문 `<img src=...-fig-N>` 목록과 `assets/<slug>-fig-*` 실제 파일을 대조 → 미존재 참조는 미사용 추출본으로 교체하되 **이미지를 직접 Read로 확인해 캡션을 실제 내용에 맞게 정직하게 재작성**(환각 캡션 금지) → 그림 번호 `1..N` 순차 정렬 → 별도 커밋. 콜론 헤딩 `## 5. 리뷰어의 ADD(+) One: 생각 더하기`는 46개 기존 포스트 공유 고정 템플릿이라 S1 예외로 유지. (2026-05-17 세션 정착)
- **arXiv ID / DOI 자동 추출**: `extract_paper_metadata()`가 PDF 첫 2페이지에서 `arXiv:XXXX.XXXXX` 및 `10.XXXX/...` 패턴을 추출 → `{PAPER_METADATA}` 블록으로 프롬프트에 주입 → Gemini는 이 값만 그대로 사용 (추측 금지). 추출 실패 시 생성 금지 지시 주입
- **APA 출처**: arXiv 논문이면 추출된 ID로 `*arXiv preprint arXiv:XXXX.XXXXX*` 형식 포함. DOI도 추출 성공 시 `https://doi.org/...` 추가. 추출 실패 시 ID 완전 생략
- **arXiv ID/DOI 환각 후처리 (필수)**: `extract_paper_metadata()` 로그에 `arXiv ID/DOI 미확인 — 출처 ID 생성 금지 지시 적용` 메시지가 떠도 Gemini가 종종 `*arXiv preprint arXiv:2605.10122*` 같은 환각 ID를 출처 라인에 끼워 넣는다. `/paper` 실행 직후 **스크립트 로그 + 본문 `## 출처` 섹션 동시 확인**으로 검증 → 로그가 추출 실패였는데 출처에 ID 들어가 있으면 즉시 제거(논문 제목·저자만 유지). arXiv ID는 한 번 인용되면 잘못된 인용이 영구화돼 학술적 신뢰 손실. (2026-05-25 세션 정착)

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

### `--edit` 모드 — 영상 프레임 추출 (단일 URL 전용)

`/edit-video` 스킬이 `yt_to_post.py <URL> --edit`으로 실행될 때 추가 동작:

1. yt-dlp로 360p 이하 최저화질 비디오 임시 다운로드
2. OpenCV(`cv2`)로 인트로(10%)·아웃트로(10%) 제외 구간에서 4개 프레임 균등 추출
3. `{video_id}-frame{N}.jpg`로 임시 저장 → slug 확정 후 `{slug}-frame{N}.jpg`로 재명명
4. 프레임 이미지를 Gemini 멀티모달 API에 전달 → `{FRAME_INFO}` 플레이스홀더에 타임스탬프 주입
5. Gemini가 `[FRAME:N]` 마커를 본문에 삽입 → `replace_frame_markers()`가 `<figure>` 블록으로 교체
6. 남은 `[IMAGE:]` 마커는 Pexels/DDG로 처리 (프레임이 있으면 거의 없음)

**관련 함수**: `yt_to_post.py`: `extract_video_frames()`, `call_gemini_api_multimodal()`  
**관련 함수**: `image_fetcher.py`: `replace_frame_markers()`  
**프롬프트**: `edit_yt_prompt_template.txt` (`{FRAME_INFO}` 플레이스홀더, `[FRAME:N]` 지침 포함)  
**새 의존성**: `opencv-python-headless>=4.8.0`, `Pillow>=10.0.0` (`requirements.txt` 추가됨)  
**멀티 URL**: `--edit` 복수 URL 모드는 프레임 추출 없이 기존 썸네일 방식 유지

### 알려진 동작 특성

- Gemini가 `date:` 연도를 임의로 바꾸는 버그 있음 → 스크립트가 생성 후 강제 복원
- 한국어 제목에서 슬러그 직접 추출 불가 → Gemini slug 생성으로 해결
- 기업 네트워크 SSL 인증서 오류 → `ssl._create_unverified_context` + requests 세션 패치로 우회
- **`--edit` 프레임 추출 실패 시 `[FRAME:N]` 마커 자동 제거**: 403 등으로 영상 다운로드 실패 → `frame_results` 비어 있음 → dry-run 이전에 regex로 마커 일괄 제거 (2026-05-05 추가)
- **`--edit` 프레임 없을 때 다중 이미지 자동 삽입**: `{FRAME_INFO}` 비어있으면 "[이미지 지침 — 프레임 없음]" 텍스트를 프롬프트에 주입 → Gemini가 `[IMAGE:]` 마커 2~3개 생성 → Pexels/DDG 이미지로 자동 교체. `[IMAGE:]` 마커도 없으면 썸네일 `<figure>` 블록 자동 삽입 폴백 (2026-05-06 추가)

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
- **Naver 블로그 URL**: `blog.naver.com` → `m.blog.naver.com` 자동 변환 후 Jina로 추출 (iframe 구조 우회)
- Gemini가 `date:` 연도를 임의로 바꾸는 버그 있음 → 스크립트가 생성 후 강제 복원
- 기업 네트워크 SSL 인증서 오류 → `ssl._create_unverified_context` + requests 세션 패치로 우회
- Gemini가 한글 퍼센트 인코딩 URL 끝자락을 깨뜨리는 경우가 있음(예: `설계` → `설곳`) — 출처 섹션은 생성 후 수동 검증

### 비공개 레포 콘텐츠 처리 (Second-Brain 등)

`tigerjk9/Second-Brain` 같은 비공개 GitHub 레포의 `.md`는 blob/raw URL이 404. 로컬 클론(`C:/Users/user/Desktop/GitHub Blog/Second-Brain/`)을 `python -m http.server` 로 임시 서빙한 뒤 localhost URL을 `/paraph`에 전달한다. 처리 후 반드시 (1) 서버 종료 (2) 생성 포스트의 `<출처>` 섹션을 `tigerjk9/Second-Brain — <상대경로>` 표기로 교체. 세부 절차는 메모리 `project_paraph_private_source.md`.

---

## 담백한 전달 — 교육 앵커링 없는 블로거 (`/plain-paraph`·`/plain-video`)

기존 `/paraph`·`/video`·`/edit-*`는 모두 페르소나가 "기술과 교육의 접점을 탐구하는 전략적 탐구자", 독자가 "한국의 교사·교육 관계자"로 고정돼 어떤 주제를 넣어도 교육 렌즈로 수렴한다. blog 콘텐츠 다양성을 위해 **교육 앵커링을 제거한 "담백한 설명자" 모드**를 별도로 추가했다 (2026-06-15). 설계 PRD: `scripts/plain-prd.md`.

```bash
python scripts/web_to_post.py <URL> [URL2 ...] --plain              # /plain-paraph (web)
python scripts/yt_to_post.py <URL> [URL2 ...] --plain --model gemini-2.5-flash  # /plain-video (youtube)
```

- **신규 스크립트 없음** — 기존 `web_to_post.py`·`yt_to_post.py`에 `--plain` 플래그만 추가. 로더가 `plain → edit → default` 3-way로 템플릿을 고른다. 이미지·프레임 분기는 전부 `args.edit` 게이트라 plain(edit=False)은 default 자동주입 경로로 흐른다.
- **신규 템플릿 4종**: `plain_web_prompt_template.txt`·`plain_web_multi_prompt_template.txt`·`plain_yt_prompt_template.txt`·`plain_yt_multi_prompt_template.txt`. 각 default 템플릿 기반, 페르소나·독자·서술방식만 교체.
- **페르소나 (담백한 설명자)**: 주제는 원문이 정함(교육 렌즈 금지). 원문 정보를 정확·빠짐없이 전달, 개인 의견은 절제. 원문에 없는 사실·수치·인용 날조 금지. `edit_*`의 "날카로움+따뜻함"을 "명료함 원칙"으로 대체.
- **유지**: 단정체 문체 규칙·AI 슬롭 금지·콜론 헤딩 금지·표 활용·이미지 자동삽입·크로스오버(단 **선택적** — 억지면 생략). 카테고리도 교육에 억지로 끼워넣지 않고 원문 주제로 고른다.
- **`--plain`은 `--dry-run`·`--no-push`·`--slug`·`--date`·`--notes`(웹 단일) 상속.** 멀티 URL 모드(2개 이상)는 notes 미지원(단일 경로만 `{OWNER_NOTES}` 주입).
- **후처리**: 다른 자동화와 동일하게 7단계 QA 대상. plain 고유 추가 점검 — 억지 교육 연결 혼입 여부(있으면 원문 주제로 교정).
- **차단 소스 우회**: 403·게이트 페이지(axios·anthropic resources 등)는 본문 추출 실패로 환각 메타 포스트(쿠키 정책 등)를 양산한다. 즉시 삭제하고, 원문 PDF가 있으면 `py -3.12 -m markitdown <pdf> -o <임시.md>` → 첫 줄에 `# <제목>` prepend → `python scripts/web_to_post.py <임시.md> --plain` (fetch_content가 로컬 파일 경로 직접 지원) → 출처를 원문으로 교정 → 임시 파일 삭제. (2026-06-15 anthropic 사례에서 검증)

---

## 공통: Gemini 중복출력 가드 (`_strip_duplicate_post`, 2026-06-15)

Gemini가 간헐적으로 **본문을 통째로 두 번 출력**하거나 `(Self-correction during drafting)` 같은 **메타 코멘트를 누출**하는 실패 모드가 있다(같은 영상 2회 실행 중 1회 발생 확인). 스크립트가 그대로 commit·push하면 깨진 글(중복 본문 + 두 번째 front matter)이 라이브로 나간다.

`web_to_post.py`·`yt_to_post.py`의 `_sanitize_content` 맨 앞에서 `_strip_duplicate_post`를 호출해 차단한다: 두 번째 `--- / title:` front matter 블록 이후를 절단하고, 말미 self-correction 메타 블록을 제거한다. **web/yt 공용이라 기존 `/video`·`/edit-video`·`/paraph`·`/edit-paraph`·`/plain-*` 모두 보호된다.** 정상 단일 글은 무영향(Red-Green 검증). 단 가드는 두 번째 front matter 또는 **영어** `(Self-correction)` 블록만 잡는다. **한국어 자기검토 누출**(`생성 완료 후 검토 사항`·`준수하여 작성`)은 놓치므로(2026-06-15 envy 포스트에서 `## 출처` 뒤에 10항목 체크리스트가 통째 붙어 수동 절단함), 생성 후 출처 섹션 뒤에 메타 체크리스트가 붙지 않았는지 항상 확인해 절단한다.

---

## 주간 다이제스트 자동화 (`/digest`)

`scripts/weekly_digest.py`가 지난 7일 포스트를 모아 주간 다이제스트 포스트를 생성한다.
**자동 실행**: `.github/workflows/weekly-digest.yml`이 매주 일요일 20:00 KST에 생성·커밋·푸시한다
(`GEMINI_API_KEY`는 repo Actions secret 등록됨, 수동 트리거는 Actions 탭 workflow_dispatch).
수동 실행은 `/digest` 슬래시 커맨드 (`.claude/commands/digest.md`).

```bash
py scripts/weekly_digest.py             # 생성 + git push
py scripts/weekly_digest.py --dry-run   # 출력만
py scripts/weekly_digest.py --no-push   # 로컬 저장만
py scripts/weekly_digest.py --days 14   # 기간 변경
```

- **구조**: 도입 2~3문장 → 주제별 `###` 섹션(카테고리 그대로가 아닌 실제 묶임 재구성) → 글마다 `- **[제목](퍼머링크)** — 한 줄 코멘트`(요약 아닌 "왜 읽을 가치") → 마무리 한 단락. 프롬프트 `scripts/digest_prompt_template.txt`
- **자기 참조 방지**: `주간다이제스트` 태그 포스트는 수집 제외. 3편 미만이면 생성 안 함
- **링크 환각 자동 차단**: Gemini가 제공된 상대경로에 존재하지 않는 도메인(`https://dotconnector.co`)을 전 링크에 붙인 사례 실측(2026-07-03 첫 실행) → `normalize_links()`가 도메인을 벗겨 상대경로로 정규화하고 대상 포스트 permalink 화이트리스트와 대조해 불일치 시 경고 출력
- **출력**: `_posts/YYYY-MM-DD-weekly-digest.md`, 카테고리 `[다이제스트]`, 퍼머링크 `/post/weekly-digest-YYYY-MM-DD/`. Gemini 출력은 `TITLE:` 첫 줄 + 본문 형식 — front matter는 스크립트가 직접 조립(환각 여지 축소)
- **후처리 QA**: 링크가 대상 포스트 permalink와 일치하는지(지어낼 수 있음), S1 금지 표현(`~을 넘어` 등 혼입 확인됨), 포스트 누락, 존칭 어미 — `.claude/commands/digest.md`의 체크리스트 참고

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

### 알려진 동작 특성

- **날짜 시각 자동 사용**: `date_with_time`을 `datetime.now().strftime("%H:%M:%S")`로 생성. 과거에는 `09:00:00` 고정이라 자정 직후 실행 시 Jekyll `future: false` 정책에 걸려 포스트가 숨겨졌음 → 현재 시각으로 수정 완료 (2026-05-02)
- **YouTube 자막 없는 영상**: youtube-transcript-api → yt-dlp VTT → **Gemini 멀티모달(영상 직접 분석)** → description 순으로 폴백. Gemini 멀티모달이 description 대비 3배 이상 풍부한 내용을 추출함 (2026-05-02 추가)
- Gemini가 `date:` 연도를 임의로 바꾸는 버그 있음 → `fix_date()`가 생성 후 강제 복원
- 한국어 제목에서 슬러그 직접 추출 불가 → Gemini slug 생성으로 해결
- 기업 네트워크 SSL 인증서 오류 → `ssl._create_unverified_context` + requests 세션 패치로 우회

---

## 공통: 표 활용 규칙 (윤문화 방지)

`/yeonsu`, `/paraph`, `/video`, `/paper` 4개 스킬의 7개 프롬프트 템플릿 말미(AI 티 금지 표현 직전)에 **표 활용 규칙** 섹션이 포함되어 있다.

**왜**: Gemini가 비교·분류·매트릭스·수치 같은 본질적으로 표인 내용을 "첫째, ~. 둘째, ~. 셋째, ~." 식의 윤문으로 풀어쓰는 경향을 차단한다. 원본 자료에 명백한 표가 있어도 서술로 풀어버리는 경우가 많다.

**즉시 표화 신호**: 비교·대조, N가지 분류, 항목별 속성 매트릭스, 수치 비교, 시간 흐름, 원칙+설명+효과 N열 구조.

**서술 유지**: 도입·전환·종합 단락, 사례·일화·인용, 추론·논증의 사고 흐름, 한 줄 결론.

스킬별 추가 지침:
- `/yeonsu`·`/paraph`(단일): 원본 표 보존 + 서술이라도 신호 있으면 표화
- `/paper`: 가설 vs 결과, 실험군 vs 대조군 등 연구 설계 적극 표화
- `/video`(단일): 발화자가 항목 나열하면 표로 재구성
- `/video`(복수)·`/paraph`(복수): 영상 vs 영상, 출처 vs 출처 매트릭스 필수
- `/paraph --into`: 기존 포스트 표 보존 + 신규 자료 표 신호 통합

## 공통: 날카로움+따뜻함 원칙 (11개 프롬프트 템플릿 전체 적용)

모든 Gemini 프롬프트 템플릿의 `비판적 낙관주의...제시한다.` 줄 바로 다음에 **[날카로움 + 따뜻함 원칙]** 블록이 삽입되어 있다 (2026-05-05 전체 적용).

이 블록은 문체 절대 규칙과 쌍으로 작동한다. 프롬프트 수정 시 이 블록을 제거하거나 위치를 옮기지 않는다.

핵심 지침:
- "중요하다" 대신 → 왜 중요한지, 무엇이 달라지는지를 수치·사례로 보여준다
- "~일 수 있다" 대신 → "~다" 또는 "~조건에서만 ~다"로 조건을 명시한다
- 한 섹션에 최소 한 문장은 독자가 멈추게 만드는 뾰족한 단언을 넣는다
- 금지: 입장 없이 요약만 하는 섹션 / "앞으로 더 연구가 필요하다" 식 마무리 / 내용 없는 감탄 문장

## 공통: AI 티 금지 표현 (4개 자동화 스크립트 전체 적용)

`/yeonsu`, `/paraph`, `/video`, `/paper` 4개 Gemini 프롬프트 템플릿 말미에 **Humanize KR v2.0.0** 기준 AI 표현 금지 규칙이 포함되어 있다.
프롬프트를 수정할 때 이 섹션을 제거하거나 축소하지 않는다.

**S1 (무조건 교체)**: `~를 통해`, `~을 넘어`, `결론적으로`, `시사하는 바가 크다`, `혁신적`, `'A'에서 'B'로` 변환 공식, 콜론 헤딩(`## 제목: 부제`), 이모지

**S2 (3회 이상 반복 시 교체)**: `또한/따라서/즉` 문두 남발, `~할 수 있다` 반복 종결, `~것이다` 종결 반복, 볼드 남용

> 출처: [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) — Humanize KR v2.0.0

## 공통: PLC 상투 마무리·콜론 헤딩 템플릿 레벨 차단 (2026-05-30)

`/edit-*` 자동화가 글마다 "전문적 학습 공동체(PLC)를 통한 집단 학습과 성찰 문화가 정착되어야" / "이 변화가 정착되려면 교사들이 함께 실험하고 성찰하는 구조가 먼저다" 같은 **동일 마무리를 반복**하던 근본 원인은, 프롬프트 "필자 관점/비판적 낙관" 항목이 PLC 마무리를 **직접 지시**하고 있었기 때문이다. `edit_paper_prompt_template.txt`·`edit_web_prompt_template.txt`·`edit_web_multi_prompt_template.txt` 3종에서 해당 지시문을 "상투구 절대 금지 + 매번 다른 구체적 협력 행위(동학년 점심 대화·학년 메신저 한 줄·의심 사례 함께 보기·관찰 일지)로 변주"로 교체했고, 콜론 헤딩 금지 규칙에 `###`(H3)를 포함시켰다.

- **전체 적용 완료 (2026-06-04)**: 7개 `edit_*` 프롬프트 템플릿(`edit_paper`·`edit_paper_multi`·`edit_web`·`edit_web_multi`·`edit_yt`·`edit_yt_multi`·`edit_lecture`) 모두 동일한 "상투구 절대 금지 + 매번 다른 구체적 협력 행위로 변주" 지시로 일관화됨. `/edit-video` 병렬 5건에서 영상 3건이 PLC 마무리 문장을 글자 그대로 반복한 것이 직접 원인이었다. 근본 차단 완료. 단 템플릿 수정 후에도 Gemini가 재발시킬 수 있으니 후처리 점검은 유지.
- **후처리는 계속 필요**: 템플릿을 고쳐도 Gemini가 콜론 헤딩·arXiv ID 환각을 종종 생성한다. arXiv ID는 스크립트 로그가 "추출 실패"여도 그럴듯한 틀린 번호를 끼워 넣으므로 `## 출처`의 ID는 **항상 WebSearch 교차검증**(실제 ID면 교정, 미확인이면 제거). 상세 절차는 메모리 `feedback_edit_paper_workflow`.

## 공통: 이미지 자동 삽입

`scripts/image_fetcher.py`가 4개 자동화 스크립트(`/paper`, `/video`, `/paraph`, `/yeonsu`) 공용 모듈로 동작한다.

**이미지 소스 우선순위:**
1. **OG 이미지** — `## 출처` 섹션의 URL에서 `og:image` / `twitter:image` 추출 (가장 관련도 높음)
2. **Pexels** — `PEXELS_API_KEY` 필요. 사용자가 API키를 직접 등록한 고품질 큐레이션 이미지
3. **DuckDuckGo 최후 폴백** — `duckduckgo-search` 패키지, API 키 불필요. 400×200px 이상 가로형 필터

- **검색 쿼리**: front matter `title:` 앞 3단어 + `tags:` 앞 2개 조합 (DDG·Pexels 공통)
- **저장 위치**: `assets/{slug}-thumb.{ext}` (jpg/png/webp content-type 자동 판별)
- **삽입 위치**: front matter `header.teaser` + 본문 첫 `##` 앞 `<figure>` 블록 (alt= 포스트 title 자동 주입). `/paper` 스킬에서 PDF figure가 추출된 경우 Gemini가 본문에 직접 배치하므로 `inject_body=False`로 teaser만 삽입
- **노출 범위**: 본문 `<figure>`로 표시 + `_includes/seo.html`에서 OG 이미지로 송출. 리스트/프리뷰 노출 없음
- **Windows cp949 주의**: `image_fetcher.py` print 문에 em dash(`-`) 사용 (em dash `—` 금지)
- **기업 SSL 우회**: requests 세션 `verify=False`, DDG는 `DDGS(verify=False)` 사용

## 공통: 영문 permalink 자동 삽입

`image_fetcher.inject_permalink(content, slug)` 공용 함수가 4개 자동화 스크립트(`/paper`, `/video`, `/paraph`, `/yeonsu`) 저장 직전 호출되어 front matter에 `permalink: /post/<slug>/`를 자동 삽입한다.

**왜**: Jekyll 기본 slugify가 한글 카테고리(`AI디지털기반교육혁신`)를 `aidigital기반교육혁신` 같은 한영 혼재 슬러그로 변환해 URL이 추하게 깨짐. 영문 slug 기반 permalink를 직접 지정해 깔끔한 URL 보장.

**규칙**:
- 이미 front matter에 `permalink:`가 있으면 변경하지 않음
- 카테고리 분류는 그대로 보존 (사이드바·카테고리 페이지에서 정상 동작)
- 기존 포스트 URL은 영향 없음 (수동으로 `permalink:`를 추가한 경우만 변경됨)

## 공통: git push 주의사항

원격에 로컬에 없는 커밋이 있으면 push가 실패한다. `--autostash` 옵션이 unstaged 변경사항을 자동으로 처리한다:

```bash
git fetch origin && git rebase origin/main --autostash && git push origin main
```

> `git stash → git pull --rebase → git stash pop` 방식은 stash 스택 누적으로 "cannot rebase: unstaged changes" 오류를 반복 유발하므로 사용하지 않는다. `pdf_to_post.py`·`lecture_script.py` 내부 push 로직도 동일 패턴 적용됨.

## 공통: 주요 카테고리·태그

**카테고리** (빈도순): `AI`, `교육`, `학습과학`, `AI디지털기반교육혁신`, `철학`, `인지과학`, `바이브코딩`, `코딩`

**태그** (빈도순 상위): `이미지`, `논문리뷰`, `바이브코딩`, `AI`, `생성형AI`, `학습과학`, `교육`, `LLM`, `메타인지`, `AI윤리`, `에듀테크`, `교육공학`, `자기조절학습`, `피드백`, `프롬프트엔지니어링`

---

## 강의자료 큐레이션 하네스 (`/lecture-archive`) — 개발 중

황민호 수석 KIST Claude Code 워크숍 자료(`260429_황민호_강의자료.Zip`)를 첫 사례로 강의자료 zip 한 묶음(slides·instructor-notes·handout·labs·N 기능 카탈로그) → `_lectures/` Jekyll collection 자동 큐레이션. 5명 Superpowers 멀티 에이전트 팀(inventory·parser·curator·builder·reviewer).

**현재 상태 (2026-05-24 기준 Phase A+B 완료, Phase D 첫 변환·큐레이션 완료, Phase C 자동화 진입점 미완)**

| Phase | 산출 | 상태 |
|-------|------|------|
| 디자인 | `docs/superpowers/specs/2026-05-22-lecture-curation-harness-design.md` (605줄) | ✅ |
| Plan | `docs/superpowers/plans/2026-05-22-lecture-curation-harness-plan.md` (1957줄, 19 task) | ✅ |
| A 인프라 | `_config.yml` collections.lectures·`_layouts/lecture.html`·`_sass/_lectures.scss`·`_data/lectures.yml`+`navigation.yml`·`_includes/lecture-card.html`+`lecture-nav.html`·`_pages/lectures.md` | ✅ |
| B 스크립트 | `scripts/lecture_archive/{utils,parse_slides,extract_notes,map_features,build_site,orchestrate}.py` + tests/ (18 tests pass) | ✅ |
| D 첫 변환·큐레이션 (수동) | `claude-code-edu`: 허브 + 22 feature 페이지 + 슬라이드·핸드아웃·OG 커버. 김진관/닷커넥터 큐레이션 메타 + K-12 교사 듀얼 트랙 (15장 슬라이드 + 6곳 핸드아웃) + 허브 카드 큐레이션 배지·크레딧 + Reveal 캔버스 1280x820 + 핸드아웃 터미널 카드 재설계 | ✅ |
| C 자동화 진입점 | `.claude/skills/lecture-archive-orchestrator/SKILL.md` + `.claude/commands/lecture-archive.md` (두 번째 강의부터 적용 예정) | ⏳ |

**큐레이션 작업 패턴 (claude-code-edu에서 정착)**

- **격리 모드 유지**: `_lectures/`는 `_posts` 사이드바·지식그래프·검색에 침투 0건. 강의자료 추가 시 `bundle exec jekyll build && ls _site/categories/ | wc -l` 카운트 변경 전후 동일해야 함
- **외부 기관명 de-institutionalization**: 슬러그·타이틀에서 KIST 등 제3자 기관명 회피 (`claude-code-edu`). 청중명(교육자)로 치환
- **OG 커버**: `scripts/gen_lecture_cover.py`로 Pretendard 4 weight (Black/Bold/SemiBold/Medium) 사용, 슬레이트 네이비 + 블루/앰버 액센트 + macOS 도트 터미널 카드. 폰트는 `.fonts/` (gitignore)에 다운로드 — 스크립트 헤더 docstring에 다운로드 안내
- **큐레이션 메타 일관화**: 원작자/큐레이터 2-칸 메타를 슬라이드 표지·강사 소개·마무리·푸터 + 핸드아웃 표지·푸터에 동시 표기. `_data/lectures.yml`의 `curator`+`curation_note` 필드로 허브 카드에도 자동 배지 노출 (`curator` 없으면 원작자 1줄 분기)
- **K-12 교사 듀얼 트랙**: 페르소나 카드·prompt 예제·결과 화면 3 레이어를 **동시** 환원해야 톤 바뀜. 시나리오 한 줄만 추가하면 본문이 학술 톤이라 어색. "교사 자리 / 연구자 자리" 듀얼 페르소나로 통일
- **Reveal 캔버스**: 한국어+카드 밀도 슬라이드는 기본 960×700이 좁아 잘림 → `width: 1280, height: 820, margin: 0.04`가 안전 기본값. `.card-grid-4`에 카드 5장 넣으면 inline `style="grid-template-columns: repeat(3, 1fr);"`로 3-col 강제
- **핸드아웃 터미널 카드**: 절대 위치 `.fcmd-tag`는 점선·코드 첫줄과 겹침 → 터미널 타이틀바(`bg-strong`) + 코드블록(`bg-soft`) 2단 flow + macOS 도트 정체성

**격리 모드** — `_lectures/` collection은 `_posts` 흐름과 분리. 사이드바·지식그래프·검색에 침투 0건. `_posts` 400+개·`knowledge-graph.json`·`_includes/sidebar/*.html` 영향 없음.

**진입점**:
```powershell
/lecture-archive <zip-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright] [--rerun parser|curator|builder]
```

**의존성**: playwright(Chromium ~150MB)·beautifulsoup4·google-generativeai·weasyprint·Pillow·PyYAML·pytest. 기존 `.env`의 `GEMINI_API_KEY` 재사용.

**알려진 동작 특성**:
- **`_pages` include 필수**: `_config.yml`에 `include: [_pages]` 누락 시 `/lectures/` 404. Jekyll은 `_` 접두사 디렉토리를 기본 무시한다.
- **외부 기관명 de-institutionalization**: 제3자 강의자료를 블로그에 올릴 때 기관명(KIST 등)은 청중명(교육자)으로 치환. HTML 치환 패턴: `sed`보다 Python `str.replace()` 순서 주의 (긴 표현 먼저).
- **커버 이미지**: 강의 현장 사진은 초상권 위반 가능. Pillow로 1200×630 텍스트+터미널 모크업 생성(`Malgun Gothic` 폰트 필수). `assets/lectures/<slug>/cover.jpg` 위치.
- **Python 3.9 호환**: 모든 스크립트가 `from __future__ import annotations` + `typing.Union/Optional/List/Dict` 사용. PEP 604 `bytes | str`은 사용자 환경에서 작동 안 함.
- **Subagent 환경 Ruby 부재**: Claude Code Agent dispatch subagent에는 `bundle`·`ruby`·`jekyll` PATH 없음. Jekyll 변경 검증은 사용자 측 직접 빌드로.
- **격리 회귀 검증**: 강의자료 추가 시 `bundle exec jekyll build && ls _site/categories/ | wc -l && ls _site/tags/ | wc -l` 카운트가 변경 전후 동일해야 함.
- **slug 사용자 게이트**: curator가 `_workspace/<slug>/03_features/_slug_map.yml` 출력 후 builder는 사용자 명시 승인 ("slug 승인") 대기. URL은 영구적이므로 한 번에 정함.
- **KIST zip 통합 검증 통과**: orchestrate.py가 zip 5종 자산(slides.v2.html·instructor-notes.v2.md·handout.v2.html·labs.md·07_feature_ideas.md) 자동 발견, Playwright Chromium으로 98장 PNG 캡처 성공, `atom_mode: feature_catalog` 자동 결정.

---

## 공통: 자동화 포스트 후처리 QA 체크리스트 (`/edit-paper`·`/edit-video`·`/edit-paraph`·`/edit-yeonsu`)

Gemini 생성 직후 스크립트가 그대로 commit·push하므로, 생성된 `_posts/*.md`는 **항상 아래 7단계를 수동 점검·교정한 뒤 별도 커밋**한다. (2026-05-17 세션에서 정착)

1. **front matter 직후 잔류 코드펜스** — Gemini가 출력을 ` ```markdown ` 로 감쌀 때 닫는 펜스가 front matter 닫는 `---` 다음 줄에 ` ``` ` 단독으로 남는 경우. 그대로 두면 본문 전체가 코드블록으로 렌더링됨. 스크립트 펜스 제거 regex는 맨앞/맨끝만 잡으므로 상단 10줄을 직접 확인해 제거한다.
2. **출처 정확성** — 임시 파일 경로·애그리게이터 URL이면 원문으로 교정. `news.hada.io`(GeekNews)는 애그리게이터 → 토픽 페이지 `.topictitle` 앵커 `href`에서 원문 URL을 추출해 `- 원문: …` / `- 경유: GeekNews …` 2줄로 표기. 저자명이 확인 안 되면 추정 기입 금지(환각 방지).
3. **미번역 영단어·영문장** — 한국어로 교체. 단 툴·플러그인·API 식별자(`useEffect`·`Superpowers`·`MCP`·`CLAUDE.md` 등)는 영문 유지가 정답이며, 한글 음역됐으면 영문으로 복구한다.
4. **콜론 헤딩(S1)** — `## 제목: 부제`는 무조건 콤마(`제목, 부제`)·접속(`제목과 부제`)·장식 접두어 제거(`비판적 낙관: X`→`X`)로 교정. Gemini가 프롬프트의 S1 규칙을 자주 무시한다. 대상은 본문 `##` 헤딩이며 front matter `title:`의 콜론은 제외.
5. **오타** — Gemini 특유의 한 글자 누락·중복(`영향을 미 주는가`→`미치는가`, `두 순 개의`→`두 개의`)을 확인.
6. **출처는 최종 섹션** — 크로스오버 단락·마무리 질문이 `## 출처` 뒤에 배치되는 경우가 있다. 본문을 출처 앞으로 이동해 출처를 맨 끝에 둔다.
7. **figure 앞뒤 빈 줄** — `[IMAGE:]` 마커가 단락 중간에 빈 줄 없이 삽입되면(`텍스트.\n<figure>…`) kramdown 블록 파싱이 깨진다. `<figure>` 앞뒤에 빈 줄을 보강하고 잘린 단락을 정리한다.

**운영 노트**

- 한글·따옴표가 든 커밋 메시지는 PowerShell here-string이 git 인자 파싱을 깨뜨린다(메시지 단어가 pathspec로 오인). `git commit -F <임시 메시지 파일>` 로 처리한다.
- `/edit-*` 호출 시 사용자가 URL 뒤에 편집 지시·맥락을 길게 덧붙이면, 그대로 명령행에 이으면 `web_to_post.py`의 `urls`(`nargs="+"`)가 한국어 단어를 전부 URL로 오인한다. URL은 positional 하나로, 지시문은 `--notes '<전문>'` 로 전달한다(프롬프트의 `{OWNER_NOTES}` 자리에 주입, 단일 URL `--edit` 경로에서 동작 확인됨).
- 추출 실패 시(예: `yozm.wishket.com` 은 CloudFront가 requests·Jina 모두 403 차단 → 제목이 `The request could not be satisfied`·`403`·슬러그 `content-access-forbidden`류) Gemini가 "콘텐츠 접근 불가" 환각 메타 포스트를 생성·푸시한다. 즉시 `git rm` + 미추적 소스 이미지 로컬 삭제 + 사용자에게 차단 사실을 정직하게 보고한다. 대안: 사용자가 PDF·스크린샷·본문을 제공하면 본문을 임시 `.md`(첫 줄 `# <원문 제목>`)로 저장 후 `python scripts/web_to_post.py "<임시.md 절대경로>" --edit` 로 처리한다(`fetch_content` 가 로컬 파일 경로를 직접 지원하며 첫 줄을 title로 사용). 처리 후 출처를 원문 URL로 교정하고 임시 파일을 정리한다.