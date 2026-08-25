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

### 슬래시 커맨드 카탈로그

블로그 자동화·유지보수 슬래시 커맨드 전체 목록. 상세는 각 커맨드 파일(`.claude/commands/<name>.md`)과 아래 해당 섹션 참고.

| 커맨드 | 용도 | 상세 |
|--------|------|------|
| `/paper` | PDF 논문 → 고정 6섹션 리뷰 포스트 | 아래 "PDF 논문…" |
| `/edit-paper` | PDF 논문 → 자유구조 리뷰(주인장 목소리, 복수 PDF `--edit`) | `edit-paper.md` |
| `/video` | 유튜브 → 포스트 | 아래 "YouTube…" |
| `/edit-video` | 유튜브 → 프레임 삽입 리뷰(`yt_to_post.py --edit`) | `edit-video.md` |
| `/paraph` | 웹 아티클 → 패러프레이즈 | 아래 "웹 아티클…" |
| `/edit-paraph` | 웹 → 주인장 목소리 리뷰(`web_to_post.py --edit`) | `edit-paraph.md` |
| `/plain-paraph` | 웹 → 교육 앵커링 없는 담백한 포스트(`--plain`) | 아래 "담백한 전달…" |
| `/plain-video` | 유튜브 → 담백한 포스트(`--plain`) | 아래 "담백한 전달…" |
| `/yeonsu` | 다입력 → 교원 연수 자료 | 아래 "교원 연수…" |
| `/edit-yeonsu` | 연수 자료 주인장 목소리 | `edit-yeonsu.md` |
| `/digest` | 주간 다이제스트 | 아래 "주간 다이제스트…" |
| `/cardnews` | 카드뉴스 PNG 세트 | 아래 "카드뉴스…" |
| `/hook` | 후킹 티저 카드 1장 | 아래 "후킹 이미지 카드…" |
| `/naver` | 네이버 블로그 크로스포스팅 | 아래 "네이버…" |
| `/lecture-archive` | 강의자료 zip → `_lectures/` 큐레이션(개발 중) | 아래 "강의자료 큐레이션…" |
| `/column` | 클로드 직접 집필 전문가 칼럼(유튜브 자막 지원, 저장 직후 `py scripts/column_qa.py`로 후처리 2패스 필수) | `column.md` |
| `/tidy-claude-md` | CLAUDE.md 진단·정리(6지표 채점, 교훈 보존) | `tidy-claude-md.md` |
| `/wrap` | 세션 마무리(메모리→CLAUDE.md 정리→PRD→커밋) | 전역 `~/.claude/commands/wrap.md` |

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
- **미니 그래프 뷰** (`assets/js/post-graph.js`, 2026-07-11): 모든 포스트 우측 sticky 사이드바 "On this page" **위**에 현재 글 + 태그 IDF top-8 이웃을 표시 (Quartz 스타일). D3 무의존 vanilla 포스 시뮬레이션(동기 300 iter 후 정적 SVG), `/knowledge-graph.json`을 `requestIdleCallback`으로 유휴 fetch. 엣지 스코어링은 KG 페이지 `buildEdges`와 동일(IDF 합산, 카테고리 fallback 포함), 이웃 간 엣지는 노드당 top-2. 노드 클릭 → 해당 글 이동, 헤더 확장 아이콘 → `/knowledge-graph/`, 헤더 돋보기(`#post-graph-zoom`) → **확대 모달**(`#pg-modal`, JS lazy-build — 같은 로컬 그래프를 대형 캔버스에 재레이아웃, 라벨 18자·13px, Esc/바깥 클릭/✕ 닫기, body 스크롤 락). 현재 글 미매칭·이웃 0이면 위젯 자동 숨김. 모바일(<1024px)에서도 본문 상단 전체폭 카드로 노출(2026-07-24 — JS가 컨테이너 실측 폭으로 렌더하므로 CSS 숨김 해제만으로 동작). sticky 컬럼 뷰포트 초과 방지 위해 그래프 존재 시 `.toc__menu` max-height를 290px 축소(`main.scss`). `single.html`은 `page.toc or page.date`로 aside를 렌더
- **미니 그래프 가독성 원칙 (2026-07-11 재설계)**: ① viewBox는 컨테이너 **실측 폭 1:1 px 매핑**(고정 200 viewBox는 사이드바 300px에서 레터박스+블러 유발) ② 라벨은 halo 필수(`paint-order: stroke` + 배경색 stroke 3px — 엣지 선 위에서 판독) ③ 라벨은 4방향(아래/위/우/좌) 그리디 배치 — 이미 놓인 라벨 + **노드 원을 장애물로 등록**하고 겹침 면적·경계 이탈 비용 최소 위치 선택 (상하 플립만으론 중심 라벨·3중 겹침을 못 풀어 교체) ④ 라벨 10.5px·12자 잘림(모달 13px·18자) ⑤ hover는 `transform-box: fill-box` + scale(1.3) ⑥ 모달 대형 캔버스는 중력을 스케일 반비례(0.01/s)로 완화해야 가운데 뭉침이 풀림. 검증: DOM 스텁 하네스 + **독립 HTML(평탄화 CSS+합성 데이터+fetch 오버라이드) → Edge 헤드리스 스크린샷**으로 시각 확인(스크래치패드 pg-test.html 패턴)

**리서치 허브** (`/research/`):
- 페이지: `research.md` (layout `default` — 사이트 내비·푸터 유지, 저자 사이드바 없음). 자체 완결 `<style>`/`<script>`, `#rh-app` 스코프. 테마 대응(다크 기본 + `html[data-theme="light"] #rh-app` 오버라이드). 스크립트는 `{% raw %}` 래핑(Liquid 안전)
- **디자인 아이덴티티 (2026-08-25 리디자인)**: 소개 히어로의 **오로라 스레드**(앰버→로즈→바이올렛→블루, 다크/라이트 팔레트 분리 CSS 변수 `--rh-a1..a4`)를 리서치 허브까지 통일해 한 제품으로 읽히게 함. 액센트는 시안(`#2ec4cc`, AI슬롭 팔레트)에서 **사이트 블루**(`#58a6ff`/라이트 `#0969da`)+앰버로 교체. 히어로 radial 블롭 제거 → 스탯을 헤어라인 밴드(상단 오로라 세그먼트)로, 이모지 UI 아이콘(🔍✨💬)→인라인 SVG, 정렬 셀렉트 커스텀 화살표, 카드 호버·펼침 시 오로라 상단 스레드+등장 모션(`rh-in`, reduced-motion 대응), Pretendard 동적 서브셋 로드. **JS 무변경**(카드 DOM class·id 후크 유지) — 리스타일 기법·검증 하네스는 메모리 `feedback_selfcontained_page_restyle` 참고
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
- **사이드바 토글 겹침 함정 (2026-07-04)**: `assets/js/sidebar-toggle.js`가 layout `default` 페이지(`/research/`·`/ask/` — `.sidebar` 요소 없음)에서도 플로팅 ☰/✕ 버튼을 body에 추가해 본문 제목을 가렸다. `initSidebarToggle()` 맨 앞에 `if (!document.querySelector('.sidebar')) return;` 조기 반환 추가로 해결. **layout default 커스텀 페이지를 새로 만들 때 이 버튼이 뜨는지 항상 확인**
- 프론트: `research.md` AI 검색 토글(Enter 실행, 유사도순 재정렬) + `ask.md` 챗 UI(`[n]` 인용→출처 링크, 출처 카드, sessionless). 둘 다 `/api/health` 프로브 성공 시에만 AI UI 노출 — **서비스 미배포여도 사이트는 완전 정상**
- **배포 완료 (2026-07-03)**: 프로덕션 `https://dotconnector-ask.vercel.app` (팀 `dot-connectors-projects-282d6187` / 프로젝트 `dotconnector-ask` — 코드의 `ASK_API` 상수와 일치). 재배포(코드 수정 시에만 — 데이터 갱신은 불필요): `cd research-ask && npx vercel link --yes --project dotconnector-ask --scope dot-connectors-projects-282d6187 && npx vercel deploy --prod --yes --scope dot-connectors-projects-282d6187` (`.vercel` 링크는 gitignore라 클론마다 link 먼저). **배포 전 `npx vercel whoami`로 CLI 인증 확인** — 이 머신은 전역 인증돼 있어 토큰 불필요(2026-07-03 확인). 인증 없고 `vercel login`이 한글 컴퓨터 이름 ByteString 오류로 실패하면 `--token <VERCEL_TOKEN>` 우회. 비대화 모드는 `--scope` 명시 필수
- 남용 방지: CORS 허용(블로그+localhost), 인스턴스 로컬 레이트리밋(ask 6/min·400/day), 질문 500자·답변 2000토큰 상한. 트래픽 증가 시 Upstash 교체
- **주인장 전용 모드 (2026-07-03, API 비용 통제)**: Vercel env `ASK_ACCESS_KEY` 설정 시 embed/ask는 `X-Ask-Key` 헤더 필수(401), health가 `authRequired`/`authorized`를 반환. 블로그 UI는 미인증 방문자에게 AI 토글·CTA를 숨기고, `/ask/` 방문 시 잠금 안내+키 입력 폼 표시. **키는 `.env`의 `ASK_ACCESS_KEY`** — 주인장이 기기당 1회 `/ask/`에서 입력하면 localStorage(`dc_ask_key`) 저장, 허브 AI 검색도 같은 키 공유. 허브 키워드 탐색은 전면 공개 유지(클라이언트 연산, 비용 0). 키 제거하면 공개 모드로 복귀. 로컬 하네스는 키 자동 첨부(`--no-key`로 미인증 시뮬레이션). **Vercel env를 Sensitive로 저장하면 `vercel env pull`이 빈 값을 내려 복구 불가** — 실제로 최초 키가 Sensitive라 복구가 안 돼 2026-07-03 새 키로 교체(일반 Encrypted로 저장, `.env`와 동기화)했다. 접근 키는 Sensitive로 만들지 말 것
- **방문자 BYOK 모드 (2026-07-03 추가)**: 잠금 상태여도 방문자가 `/ask/`에서 **본인 Gemini API 키**(Google AI Studio 무료 발급)를 입력하면 이용 가능. 프론트가 Google `models` 엔드포인트로 키를 직접 검증(우리 서버 미경유) 후 localStorage(`dc_gemini_key`) 저장 → embed/ask 요청에 `X-Gemini-Key` 헤더 첨부 → 서버가 접근 키 검사 우회 + 해당 요청의 Gemini 호출을 방문자 키로 수행(비용 방문자 부담). BYOK 요청은 일일 총량(주인장 키 보호)에서 제외, 분당 IP 제한은 유지. 키 무효(400/401/403)는 401 `bad_gemini_key`(프론트가 키 자동 삭제), 할당량 소진(429)은 `gemini_quota`로 구분 응답. **프론트는 health의 `byok` 플래그를 확인한 뒤에만 키 입력 UI를 노출**(구버전 배포와 새 프론트가 섞여도 안전). 허브는 미인증이어도 `byok`면 "AI에게 묻기" CTA를 노출해 입구를 열어 둔다. 키 형식 검증 regex `AIza[0-9A-Za-z_-]{30,80}` (프론트·백엔드 동일)
- 로컬 E2E: `node research-ask/test/local-harness.mjs "질문"` (`--embed`·`--health`·`--byok` 모드 지원, .env 키 자동 로드, 블로그 fetch를 로컬 파일로 몽키패치). `--byok`는 잠금 강제 후 무키 401 / 무효키 401 / 본인키 200 3종 검증

**프롬프트 라이브러리** (`/prompts/`, 2026-07-24):
- 페이지: `prompt-library.md` (layout `default`, `#pl-app` 스코프 — research.md와 동일 패턴). 데이터: `assets/prompt-library.json`
- 빌드: `py scripts/build_prompt_library.py` — prompts.chat(CC0 1.0) 원본 `prompts.csv`에서 스크립트 내 `WHITELIST`(act명+교육 카테고리, 현재 32개·7카테고리)로 선별 → Gemini 한국어 번안(텍스트 해시 증분 캐시 `scripts/.prompt_library_cache.json`, gitignore) → JSON. **항목 추가 = WHITELIST에 (act, 카테고리) 추가 후 재실행·JSON 커밋**
- `clean_prompt`: prompts.chat 변수 문법 정리 — `${이름:기본값}`→기본값 치환, 단독 라인 `${이름}`→제거, 인라인→`[이름]`. 기여자 필드는 이메일·다중어절 제거(GitHub 아이디만 공개 JSON에 유지 — 개인정보)
- UI: 카테고리 필터+검색+**프롬프트 복사**(복사 시 한글 프롬프트 블록 자동 펼침)+영어 원문 토글. 표시 블록은 연속 빈 줄을 squeeze(복사는 원본 유지)
- 격리: front matter에 `categories`/`tags` 없음 → 사이드바·지식그래프·카테고리/태그 페이지 침투 0. 확장 설계는 `scripts/prompt-library-hub-prd.md`

**Custom Sidebar** (`_includes/sidebar/`):
- `categories.html` — 카테고리별 포스트 수
- `tag_cloud.html` — 태그 클라우드
- `recent-posts.html` — 최근 방문 포스트 (localStorage `recentPosts`, MAX 8개, `window.__currentPost` 소비)
- `books-widget.html` — 저서 미니 서재 ("최근 방문" 아래). `site.data.published_books` **전체**(현재 10권)를 표지 그리드로 노출 + "닷커넥터의 서재 →" 링크(`/lectures/`). CSS는 `main.scss`의 `.books-widget__covers` = `display:grid; grid-template-columns:repeat(5,1fr)`(5열×2행 미니 서재, 2026-07-30 기존 `limit:3`·flex 한 줄에서 확장). 좁은 사이드바에서도 2행 높이로 라이브러리 전체 조망. 후보(3권/5×2/4열/auto-fill) Edge 헤드리스 실측 비교로 5×2 채택
- `_config.yml`의 `sidebar` 키에서 설정

### Theme Customization

파일 탐색 순서: 프로젝트 파일 → gem 파일. `_includes/`, `_layouts/`, `_sass/`, `assets/`에 놓으면 gem 파일을 덮어씀.
커스텀 스타일 오버라이드: `assets/css/main.scss`.

> **주의**: `_sass/minimal-mistakes/_sidebar.scss`에 `.sidebar.sticky { max-height: calc(100vh - #{$nav-height} - 2em) }` 하드코딩 → `main.scss` 오버라이드에 `!important` 필수.

**기본 화면 배율 (2026-08-04)**: 크롬 80% 줌으로 보던 밀도를 100%의 기본값으로 삼았다. `main.scss` 최상단(테마 import 앞)에서 `$doc-font-size*` 4개를 덮어씀 — 16 / 18 / 20 / 22px → **16 / 16 / 16 / 17.6px**. 모바일(<768px)은 가독성 하한 때문에 16px 유지, 데스크톱 구간만 축소. 이 변수는 `_reset.scss`의 `html { font-size }`와 `em()` 함수 기본 컨텍스트에만 쓰이는데 `em()`은 실사용처가 없고, 브레이크포인트는 breakpoint gem이 자체 16px 기준으로 em 변환(`@include breakpoint-set("to ems", true)`)하므로 **폰트 스케일을 바꿔도 브레이크포인트는 이동하지 않는다**. 사이드바 폭(`$right-sidebar-width` 300px)은 의도적으로 유지 — 줄이면 미니 그래프·서재 위젯(5열 표지 그리드)이 좁아진다. 커스텀 UI의 하드코딩 px(버튼·토스트·토글 14~18px)도 그대로라 본문만 작아지고 컨트롤 크기는 보존된다. 재조정은 `-x-large`(≥1280px)·`-large` 두 값만 만지면 된다. 검증: 라이브 HTML에 `<base>` + 오버라이드 `<style>`을 주입한 정적 하네스를 Edge 헤드리스로 캡처해 **진짜 80% 줌**(`--window-size=1920,1125 --force-device-scale-factor=0.8`)과 픽셀 비교.

### Custom UI Features

| 기능 | 주요 파일 |
|------|----------|
| 다크/라이트 모드 토글 | `assets/js/theme-toggle.js`, `_includes/masthead.html` |
| 모바일 사이드바 테마 토글 | `assets/js/sidebar-toggle.js` (`injectMobileSidebarHeader`) |
| 본문 복사 버튼 (상단) | `assets/js/post-copy.js`, `_layouts/single.html` |
| 소셜 공유 패널 (카카오톡·X·링크드인·페이스북·스레드·링크복사) | `_includes/post-share.html`, `assets/js/post-share.js`, `assets/css/main.scss`, `_config.yml`(kakao_js_key) |
| 포스트 미니 그래프 뷰 (TOC 위 sticky, Quartz 스타일) | `assets/js/post-graph.js`, `_layouts/single.html`, `assets/css/main.scss` |
| 최근 방문 포스트 사이드바 (localStorage, 8개) | `_includes/sidebar/recent-posts.html`, `assets/css/main.scss` |
| 사이드바 섹션 접기/펼치기 | `assets/js/sidebar-toggle.js` (`initSectionCollapse`), `_includes/sidebar.html` |
| 웰빙 코너 | `assets/js/wellbeing.js`, `wellbeing.md`, `_includes/footer.html`, `assets/css/main.scss` |
| 리서치 허브 (논문 탐색+AI 검색) | `research.md`, `scripts/build_research_db.py`, `scripts/build_embeddings.py`, `assets/research-*.json` |
| 프롬프트 라이브러리 (교육자용 큐레이션) | `prompt-library.md`(`/prompts/`), `scripts/build_prompt_library.py`, `assets/prompt-library.json` |
| 자료실 (강의+도서+교실자료 허브) | `_pages/lectures.md`, `_data/lectures.yml`, `_data/books.yml`, `_data/resources.yml`, `scripts/gen_book_covers.py`, `_sass/_lectures.scss` |
| AI에게 묻기 (RAG 챗봇, 주인장 키 + 방문자 BYOK) | `ask.md`, `research-ask/` (Vercel `dotconnector-ask`) |
| 주간 다이제스트 자동화 | `scripts/weekly_digest.py`, `.github/workflows/weekly-digest.yml`, `/digest` |
| NE 수업 디자이너 (노벨 엔지니어링 수업 설계기) | `tools/ne-designer/index.html` (front matter 없는 정적 단독 HTML) |
| 학습자 친화적 어휘 사전 (497개, 등급 대조) | `tools/vocab/index.html`, `assets/vocab-db.json` |
| 포스트 번호 표시 (홈·단일·검색 공통 넘버링) | `_layouts/single.html`, `_includes/archive-single.html`, `assets/js/lunr/lunr-store.js`·`lunr-en.js`, `assets/css/main.scss` |
| 검색 키보드 단축키 (`/`·`Ctrl/Cmd+K`) | `assets/js/search-shortcut.js`, `_includes/search/search_form.html`, `_includes/scripts.html` |
| 소개 페이지 그래프 히어로 (하프톤 도트 초상 + 지식그래프형 내비) | `_pages/about.md`, `_layouts/about.html` |
| 이미 읽은 글 표시 (localStorage `readPosts`) | `assets/js/read-tracker.js`, `_includes/scripts.html`, `assets/css/main.scss` |

**독자 편의 UI (2026-07-25)** — 기조(다크 에디토리얼·블루 액센트·미니멀) 유지하며 추가:
- **포스트 넘버링**: 홈 리스트(`archive-single.html` seq)·단일 글(`single.html` 헤더, `page.collection == 'posts'` 게이트 후 `site.posts`에서 위치 탐색)·검색 결과 모두 **`전체수 − index0`** 동일 공식(최신글=총편수, 3자리 zero-pad). 검색은 `lunr-store.js`가 **`site.posts` 순회**로 seq·date를 스토어에 담아야 정확(컬렉션 docs 순서 아님) → `lunr-en.js`가 홈과 동일 카드(`.recent-posts` 상속, `.search-results` 래퍼)로 렌더
- **리스트 발췌 제거 (2026-08-03)**: 리스트 카드에서 발췌(`post.excerpt`)를 뺐다 — 이미지로 시작하는 글은 캡션/빈칸, 텍스트 글은 도입문이 나와 카드마다 제각각이라 어수선했다. 이제 제목 중심으로 통일(홈 카드는 번호·카테고리·날짜·제목·해시태그). 적용 범위: ① 홈 = `archive-single.html` **seq 분기**에서 excerpt `<p>` 제거 ② 카테고리/태그 = else 분기 excerpt를 `{% unless include.hide_excerpt %}`로 감싸고 `posts-category.html`·`posts-tag.html`·`posts-taxonomy.html` 세 곳에서 `hide_excerpt=true` 전달. **관련 글(`page__related`, grid)·컬렉션(`documents-collection`)·`posts.html` 아카이브는 플래그 미전달이라 발췌 유지**. 향후 자동화·테마 업스트림 병합이 되살리지 않도록 주의
- **페이지네이션**: `paginator-v1.html` 노출 창 ±2→±3, 임계값 5로 인접 페이지 사이 가짜 `…` 제거. `.pagination--numbered` 클래스로 숫자형만 스코프(단일 글 `.pagination--pager`와 분리), 중앙정렬 개별 라운드 칩
- **검색 단축키**: `/`·`Ctrl/Cmd+K`로 오버레이 열기(`.search__toggle` click 재사용). 자동 포커스·Esc 닫기는 테마 `main.min.js`가 이미 처리, 입력 중이면 무시. 오버레이에 `.search-hint` kbd 힌트
- **읽은 글 표시**: 방문 글을 `readPosts` localStorage에 기록(기존 `recentPosts`는 8개 한정이라 **별도 키**). 리스트·검색에서 `.is-read` + 넘버 옅게 채움 + `.entry-read` "읽음" 배지. 검색 결과는 `MutationObserver`로 비동기 렌더 대응
- **본문 이미지 지연 로딩**: `single.html`에서 `{{ content | replace: '<img ', '<img loading="lazy" decoding="async" ' }}` **빌드타임 주입**. end-of-body JS로는 이미 로드가 시작돼 늦으므로 Liquid 필터로 처리(508편 수정·재빌드 불필요)
- **프로필**(`_includes/author-profile.html`): 이메일은 mailto 링크 대신 주소(`faithfuljk@naver.com`) 표시 + 클릭 복사(onclick, no-JS mailto 폴백). 소셜 링크(Website·Facebook·GitHub·Instagram = `author.links`)에 `target="_blank"` → 새 탭
- **모바일 사이드바 토글**: `@media max-width:1023px` 안에 좌하단 FAB(2026-07-24) 뒤로 남아 있던 `.sidebar-toggle { top:70px }` 스테일 오버라이드 제거 → FAB가 상단으로 튀어 포스트 번호와 겹치던 문제 해소

**소개 페이지 (2026-08-22 재설계)**: `/about/`은 layout `about`(`_layouts/about.html` — layout `default` 기반, `#about-app` 스코프 CSS/JS 전체 보유) + `_pages/about.md`(콘텐츠). 히어로는 하프톤 도트 초상(기존 `assets/dot-connector-portrait.png`를 클라이언트 캔버스로 렌더, 원형 액자 없음) + 성과 위성 노드 그래프(노드 = 섹션 앵커 내비, innerWidth ≥1260 JS 그래프 모드 — 헤드 블록 실측 충돌 회피 포함·미만은 스택 폴백). 숫자 밴드는 Liquid 동적(`site.posts | size`·`site.data.published_books | size`·연차 `minus: 2006`). **본문 마크다운은 전부 사전 렌더링 HTML로 커밋됨** — kramdown 중첩 `markdown="1"` 의존 제거 목적이므로 활동 기록 추가는 해당 시대 `details` 안 `<li>`로 하고 summary 건수·`ab-sub` 총계(현재 219건)를 함께 갱신한다. Pretendard는 jsDelivr dynamic-subset CSS를 About 한정 로드. **연결선(그래프 모드)**: 하프톤 렌더 시 방향별 실루엣 반경을 실측(`SILH`)해 선이 흉상 가장자리에서 출발 — 사진 교체 시 자동 추종. **출발점 흔들림 수정 (2026-08-25)**: 초기 구현은 ① 실루엣을 *그려진 도트*에서 재고 ② 5° 버킷을 *최근접*으로 조회했다. 도트는 디더링·페이드·테마(`v=light?1-L:L`)로 빠지고, 목 옆 오목한 구간 때문에 반경 프로파일에 절벽(20°→25°에서 46→117px)이 생겨 **각도가 3°만 달라져도 출발점이 70.6px 튀고 8개 중 4개가 얼굴 안쪽(28~80px)에서 출발**했다(실측). 노드는 상시 미세 진동+마우스 패럴랙스로 각도가 계속 바뀌므로 로드·조작마다 다른 지점으로 보였다. → ① 실루엣을 **원본 사진의 피사체 마스크**(배경색 거리 판정)에서 2° 180버킷으로 재고 ② 빈 방향 최근접 채움 → ±28° 러닝맥스로 오목부 메움 → ±20° 이동평균 2패스 (`buildSilhouette`) ③ 조회는 이웃 버킷 **선형 보간** + 링 반경 대비 밴드 `[0.86R, 1.05R]` 클램프(`silRadius`). 결과 3° 민감도 70.6→**7.0px**, 반경 103~126px로 항상 링 가장자리, 다크/라이트 동일. 추가로 히어로·헤드 블록에 `ResizeObserver`를 걸어 스크롤바 등장·지연 폰트로 폭이 바뀌면 재배치한다. 검증은 라이브 HTML의 히어로 스크립트만 패치본으로 갈아끼운 로컬 하네스 + Edge 헤드리스(초상 이미지는 canvas taint 회피용 동일 출처 로컬 사본, `python -m http.server`) — DOM 프로브로 출발점 좌표를 3회 덤프해 0.1px 동일 확인. 색은 오로라 그라디언트(앰버→로즈→바이올렛→시안블루, 다크/라이트 팔레트 분리) + 드로우-인(진입 시 순차) + 흐르는 빛 입자(선당 1, 호버 시 그 선 증폭) + 곡률 미세 진동, 숫자 밴드는 스크롤 진입 카운트업. 모바일 스택은 CSS 세로 줄기+가지(같은 오로라 팔레트, `.ab-nodes::before/::after`). 헤드라인 "점과 점을 잇는 사람"(점 아닌 연결이 핵심 — 사용자 확정), 웹 도구 노드는 "40+"(바이브코딩 컬렉션 37+블로그 6−중복 1=실측 42, 증가 감안 표기). **`overflow-x:hidden` 함정**: 한 축 hidden이면 다른 축이 auto로 계산돼 요소가 스크롤 컨테이너가 되어 내부 스크롤바가 생김(이중 스크롤바 실측) → `overflow-x:clip` 사용. 설계 상세는 `docs/superpowers/specs/2026-08-22-about-redesign-design.md`. **바디 폴리시 (2026-08-25)**: 히어로는 유지하고 본문만 다듬음 — 시대별 "전체 기록 N건 보기"를 폼컨트롤형 회색 바에서 `fit-content` 알약 버튼+펼침 패널로, 현직 박스(`.ab-now`)의 좌측 색상 보더 클리셰를 오로라 상단 스레드+2단 컬럼(`columns:2` ≥760px)으로, 타임라인 스파인(`.ab-tl::before`)을 히어로 연결선과 같은 오로라 그라디언트로(다크/라이트 분리), 라이트 모드 히어로에 옅은 오로라 radial 틴트 3겹. 리서치 허브와 같은 오로라 아이덴티티로 수렴시키는 작업.

**`tools/` 정적 단독 페이지**: front matter 없는 `tools/<슬러그>/index.html`은 Jekyll이 정적 파일로 그대로 복사한다(exclude 목록에 없음). 테마 CSS·`sidebar-toggle.js`가 로드되지 않아 라이트모드 앵커 색·플로팅 ☰ 버튼 함정이 원천 차단된다 — layout default 커스텀 페이지에 필요한 `#앱ID` 스코핑도 불필요. 첫 사례가 NE 수업 디자이너(`/tools/ne-designer/`), 두 번째가 어휘 사전(`/tools/vocab/`). 검증은 스크래치패드 복사 후 Edge 헤드리스 `#demo` 해시 렌더 캡처(메모리 `project_tools_static_pages`). 데이터 fetch가 절대경로(`/assets/...`)면 로컬 file:// 에서 안 잡히므로 `window.fetch`를 목데이터로 덮어쓴 사본을 만들어 캡처한다.

> **`[hidden]` 무력화 함정 (2026-08-04 실측)**: 저자 CSS에서 `display`를 지정한 요소는 UA 스타일시트의 `[hidden]{display:none}`을 **이겨서** JS의 `el.hidden = true`가 통하지 않는다. 어휘 사전 `.more{display:block}`이 그래서 결과가 0건일 때도 "더 보기" 단추를 계속 보여줬다(누르면 라벨이 `더 보기 (0개 남음)`으로 바뀜). `display`를 주는 셀렉터마다 `&[hidden]{display:none}`을 짝으로 붙인다. `display` 미지정 요소(`.clr`·`.kbd`)는 무영향.

**다크/라이트 모드**: `html[data-theme="light"]` CSS 레이어 방식. 컴파일된 dark skin 위에 light 오버라이드 덮기. anti-FOUC 인라인 스크립트를 `_includes/head.html` CSS `<link>` 이전에 삽입. `theme-toggle.js`는 이벤트 위임 방식 — masthead와 모바일 사이드바의 `.theme-toggle` 버튼 모두 처리.

**모바일 사이드바**: `injectMobileSidebarHeader()`가 사이드바 최상단에 `.sidebar-mobile-header`(테마 토글 포함)를 주입. iOS Safari dvh 버그는 `height: 100dvh; max-height: 100dvh`로 수정.

**본문 복사**: `.page__content` DOM 클론 → `.sidebar__right`, `[rel="permalink"]`, `.sr-only` 제거 → `innerText` 복사. 복사 텍스트에 `원문링크: <decoded URL>` 자동 삽입 (`## 출처` 섹션 앞, 없으면 맨 끝). URL은 `decodeURIComponent(window.location.href)`로 한글 디코딩.

**출처 섹션**: 모든 자동화 포스트의 출처는 `## 출처` 헤딩으로 통일한다(기존 `<출처>` 태그 폐기 · 2026-04-28 프롬프트 7개·기존 포스트 54편 전량 변환).

**링크 복사**: 포스트 URL만 단독 복사. raw `window.location.href` 사용 (NFC 인코딩 형태). iOS Safari는 한글을 NFD로 클립보드에 저장해 카카오톡·메모앱 등 NFC 기대 환경에서 깨지므로 디코딩된 한글 URL은 모바일에서 위험. 본문 복사 안의 "원문링크:" 표시는 사람이 읽는 텍스트라 디코딩 유지. **링크복사 버튼은 상단이 아니라 하단 소셜 공유 패널에 있음**(아래 참고). 상단 `.post-copy-wrap`엔 본문 복사만 남김.

**소셜 공유 패널** (`_includes/post-share.html` · `assets/js/post-share.js` · `main.scss`의 `.post-share`/`.share-btn`, 2026-07-11): 포스트 하단(`single.html`에서 `page.date` 있는 글, footer meta 뒤·pagination 앞)에 카카오톡·X·링크드인·페이스북·스레드·링크복사 버튼. 테마 기본 `social-share.html`(X·FB·LinkedIn·Bluesky)은 중복이라 제거. `window.__currentPost`(title/url/description/image, `seo.html` OG 이미지 재사용)를 JS가 소비. X·링크드인·페이스북·스레드는 표준 인텐트 URL 팝업(키 불필요).
- **CSS float 함정**: `.post-share`는 테마 `.page__meta`/`.page__share`처럼 `float:inline-start; width:100%; clear:both` 필수(`_sass/minimal-mistakes/_page.scss:55-63`). 없으면 float된 `.page__content` 옆에 끼어 "오른쪽에 붙은" 것처럼 렌더됨.
- **카카오톡 = 도메인 2곳 + 키 일치 (에러 4019, 비직관)**: `Kakao.Share.sendDefault`는 ① 제품 링크 관리→웹 도메인(링크 이동) ② 플랫폼 키→JavaScript 키→**JavaScript SDK 도메인**(SDK 인증, 4019 담당) **두 곳** 등록 필요. `_config.yml`의 `kakao_js_key`는 **SDK 도메인이 등록된 바로 그 키**여야 함(JS 키 여러 개면 엉뚱한 키 등록으로 4019 지속 — 실제 `9751bcbf…`→`9e4827c8…` 교체로 해결). 도메인은 scheme+host만(경로/슬래시 자동 제거). JS 키는 도메인 제한 공개 클라이언트 키라 커밋 안전(REST API/Admin 키는 금지). SDK는 `kakao_js_key` 설정 시에만 로드, 미설정 시 카카오 버튼은 OS 공유시트→링크복사 폴백.

**사이드바 섹션 높이**: 데스크톱 `max-height: calc(60vh - 120px) !important` — 최근 방문 8개가 잘리지 않도록 확대 (2026-07-11, 이전 `calc(50vh - 175px)`). 내부 스크롤(얇은 4px 스크롤바) 유지.

**웰빙 코너**: `assets/js/wellbeing.js`가 IIFE `(function(W){...})(window.WB = window.WB || {})`로 실행됨. 내부 `$` 헬퍼는 `id => document.getElementById(id)` (jQuery 아님). `W.init()`에서 각 모듈 호출을 개별 `try/catch`로 래핑해 한 모듈 오류가 나머지에 영향 없음.
- **`/wellbeing/` 페이지**: `wellbeing.md` — meta refresh + JS로 `https://comma-for-wellbeing.vercel.app/` 즉시 리디렉트. 상단 네비게이션 "쉼표" 메뉴도 동일 외부 URL 직접 연결
- **푸터**: `_includes/footer.html` — 로고+저작권만. `max-width:400px; margin:0 auto; text-align:center` 인라인 style 컨테이너로 중앙 정렬. CSS 클래스 방식은 인라인 style에 특이성이 져서 HTML 인라인으로 직접 지정
- **네비게이션** (`_data/navigation.yml`): 쉼표(comma-for-wellbeing.vercel.app), 기록 대화(dotconnector-log.vercel.app), 말씀의 길(malsseum-ui.vercel.app) 외부 링크 포함

**모바일 최적화** (`assets/css/main.scss` `@media (max-width: 1023px)` 블록):
- 사이트 제목 한 줄 고정: `max-width: calc(100vw - 200px)` + `overflow: hidden` + `text-overflow: ellipsis` + `flex-shrink: 1`. **예약폭 함정(2026-07-24)**: 155px 가정은 실측 버튼 영역(테마토글44+검색44+햄버거52+패딩·여백≈180px)보다 작아 masthead row가 뷰포트를 넘고 맨 끝 햄버거가 화면 밖으로 밀렸음 — 우측에 버튼을 추가하면 이 예약폭도 함께 늘려야 한다. 모바일 토글은 36/40으로 축소
- hits 배지: 상단 메뉴가 아니라 **푸터**(로고·저작권 아래)에 배치 — 메뉴에 넣으면 이미지 로드 폭 변동으로 greedy-nav 배치가 무너짐(실측 사고 2회)
- 플로팅 사이드바 토글(파란 ☰): 모바일에선 **좌하단 원형 FAB**(44px) — 상단(top 80px)은 제목·헤딩과 겹쳐 지저분
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
.claude/commands/*.md    # 슬래시 커맨드 (전체 목록은 상단 "슬래시 커맨드 카탈로그" 표 참고)
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
- **yt-dlp web client 차단**: "The page needs to be reloaded" 오류로 메타데이터·자막 추출이 간헐적으로 실패 → `extractor_args: {"youtube": {"player_client": ["android", "web"]}}`로 android client 우선 폴백 (2026-07-11 추가, `fetch_video_metadata`·`fetch_auto_captions_via_ytdlp` 양쪽 적용)
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

## 카드뉴스 자동화 (`/cardnews`)

`scripts/cardnews.py`가 유튜브·웹 아티클·논문(PDF)을 1080×1350 카드뉴스 PNG 세트로 변환한다.
Claude Code에서는 `/cardnews <입력>` 슬래시 커맨드로 호출 (`.claude/commands/cardnews.md` — QA 체크리스트 포함).

```bash
py -X utf8 scripts/cardnews.py <URL|PDF> --cards 10   # 기본(아웃트로 포함 총 10장). 출력: 바탕화면 cardnews/<날짜>-<슬러그>/
py -X utf8 scripts/cardnews.py <입력> --dry-run        # 카피 JSON만
py -X utf8 scripts/cardnews.py --rerender <출력폴더>    # cards.json 수정 후 재렌더(Gemini 재호출 없음)
py -X utf8 scripts/cardnews.py <입력> --keep-images --out <기존폴더>  # 이미지 재사용, 카피만 재생성
py -X utf8 scripts/cardnews.py --style diagram --topic "..."          # 밝은 개념 다이어그램(journey)
```

- **디자인 (2026-07-27 다크 시네마틱으로 전면 리뉴얼)**: 짙은 차콜 그라디언트 배경 + 좌상단 흰 스크립트 로고(`prep_logo(ink=…)`가 `assets/logo.jpg`를 밝기 기반 알파로 배경 제거 + 하단 슬로건 띠를 연속 런 20% 기준 블록 삭제 → 투명 `logo.png`를 **흰 잉크**로 칠함. 행 잉크 총량 기준은 굵은 획을 띠로 오탐하니 금지) + 우상단 노란 닷네트워크 SVG 마크, 헤드라인 2단(흰 주제 라벨 + `#f5e14e` 핵심 주장, 마침표 없음), 노란 세로 바 본문 2~3줄(**단정체 — 구버전 존칭체에서 뒤집힘**), 라운드 16:9 이미지(top 655·926×509), 큰 페이지 번호 + `출처: OOO`. **마지막 장은 고정 브랜드 아웃트로**(`cardnews_outro.html` — 닷커넥터·@Dot_Connector·linktr.ee 필 버튼·소셜 3종 simple-icons 경로. 문구는 `cardnews.py`의 `BRAND` dict)
- **헤드라인 폰트 = Black Han Sans (실측으로 특정)**: 레퍼런스 카드의 글리프높이:잉크폭(95:740)이 Pretendard Black(91:617)과 안 맞고 BHS(78:604)와 일치 → OFL 폰트를 `.fonts/`에 자동 다운로드(`ensure_headline_font`, `.fonts/`는 gitignore라 클론마다 없음). 크기는 CSS 고정이 아니라 **템플릿 내 JS가 60~122px에서 자동 축소** — 본문 블록 하단이 y=626을 넘지 않을 때까지 2px씩 줄인다(레퍼런스도 글자 수에 따라 122/94/76px로 달라짐). 좌표·색은 레퍼런스 PNG를 픽셀 측정해 맞췄고(로고·마크·푸터 ±2px), 레이아웃 회귀 검증도 같은 픽셀 대조로 한다
- **카피**: `cardnews_prompt_template.txt` → gemini-2.5-flash JSON 모드. `headline_top`(주제 라벨) + `headline_highlight`(**그 자체로 완결된 단언** — 구버전의 '이어읽기 한 문장' 구조 폐기) + `body`(2~3줄 배열) + `image_hint`/`image_query`. 따옴표는 스크립트가 강제 제거
- **카피 톤 (2026-07-27 2차 조정)**: "퇴근길 스마트폰 독자에게 쉽게, 그러나 얕지 않게" — 전문 용어는 그 자리에서 괄호로 풀고 카드마다 수치·고유명·메커니즘 중 하나는 남긴다. **친절함은 존댓말이 아니라 쉬운 설명에서 나온다**(단정체 유지). 훈계조·상투어 금지. **프롬프트만으로는 안 지켜진다** — "쉽게 쓰라"고만 하면 Gemini가 존칭체로 뒤집고 금지어(중요하다)·명사형 헤드라인·훈계조를 그대로 낸다(실측). 그래서 `validate_cards`(정규식 3종 + 헤드라인 `~다` 종결 검사) → `repair_cards`(위반 카드만 되돌려 재작성, 최대 2회) 루프를 코드에 넣었고, 남은 위반은 로그에 경고로 뜬다. 본문 줄바꿈은 `wrap_body`가 어절 단위 DP로 재배치(32자 초과 시 CSS가 접으면서 "늘었다." 같은 한 어절 고아 줄이 생김)
- **이미지 (원자료 캡처 → 생성 → 검색 3단)**: ① YouTube 실프레임(암전 프레임 회피 문턱 mean 9·std 7 — 22로 잡으면 검은 배경 강의가 6장 중 5장 탈락. 푸터에 실측 `화면 MM:SS`) / 기사 본문 이미지·og:image(썸네일 URL을 `_upsize`로 원본 승급 — 위키 220px→1280px, 안 하면 0장) / 논문은 **"Figure N" 캡션 위 영역을 페이지째 렌더**(`get_images()` 래스터 추출은 벡터 도해를 놓치고 부록 프롬프트 스크린샷을 1순위로 끌어옴 — 실측 후 교체, `p.N` 표기) ② `gemini-2.5-flash-image` 생성(16:9는 `generationConfig.imageConfig`, 다크 시네마틱 톤) ③ DDG 검색 ④ 인용 패널. 카드↔이미지는 **멀티모달이 후보 이미지를 직접 보고 배정**(실패 시 순서대로)
- **표시 방식 3종**: 흰 바탕 도표(`_is_paper` — 가장자리 흰색 75% 판정)는 종이 패널 `contain`, 세로로 긴 사진은 어두운 박스 `fit`, 나머지는 `cover`. `cards.json`의 `images[]`가 `{path, fit, note}`라 `--rerender`가 그대로 복원한다
- **추출 재사용**: web_to_post `fetch_content` / yt_to_post 자막 체인 import. 본문 200자 미만이면 생성 중단(환각 방지). arXiv `abs` URL은 `pdf`로 자동 치환, 출처의 arXiv ID는 **추출된 값만** 사용(첫 8000자 검색 — 세로 스탬프라 앞 120줄만 보면 놓침)
- **후처리 QA**: cards.json 사실성 대조·이미지 육안 확인 필수 (`.claude/commands/cardnews.md` 체크리스트). **논문 출처(source_label)는 저자·연도·제목을 원문에서 verbatim 확인 — 요약·의역해 짧은 제목 지어내기 금지, arXiv/DOI는 추출값만**(hook-image 스킬과 동일 환각방지 원칙, 2026-08-01)
- **밝은 다이어그램 스타일 (`--style diagram`, 2026-08-02)**: 다크 시네마틱과 별개 경로. 밝은 크래프트지 배경 + 손그림 개념 다이어그램 1장. **다이어그램은 이미지 생성이 아니라 SVG로 그려 한글이 안 깨진다**(이미지 모델 한글 파손 회피 — hook/cardnews가 텍스트를 오버레이하는 것과 같은 이유). 기존 `_shot`(Edge 캡처)·`_font_css` 재사용, 과금은 스펙 카피 1회뿐. 입력은 `--topic "주제"` 직접 또는 URL/PDF 추출 **둘 다**.
  - **아키타입 5종** (`--archetype {auto,journey,comparison,cycle,steps,quadrant}`, 기본 `auto`=LLM이 내용에 맞게 선택): **journey**(기대 직선+핀 vs 현실 Catmull-Rom 위빙 경로+노드) · **comparison**(좌우 2패널+헤더밴드+VS 배지) · **cycle**(원둘레 노드+시계방향 호 화살표) · **steps**(번호 원+라벨+설명 세로 흐름+연결선) · **quadrant**(십자축+화살표+4사분면+축 low/high/명 라벨).
  - LLM은 고른 아키타입 스펙만 내고(`cardnews_diagram_prompt_template.txt`, 단정체·환각금지 상속), 파이썬 디스패처 `render_diagram_svg`가 `render_{journey,comparison,cycle,steps,quadrant}_svg`로 라우팅(미지값 journey 폴백)해 렌더(`cardnews_diagram_template.html`). 공통 헬퍼 `_diag_open/_diag_close/_title/_arrowhead/_wrap_kr/_put_lines`. 라벨은 명사·짧게(길면 폰트 자동 축소·충돌 회피). 아웃트로 없이 하단 `@Dot_Connector` 푸터. `cards.json`에 `style:diagram`+archetype 저장 → `--rerender`가 스펙만으로 무과금 재렌더(스펙 필드 수정 후). 색: 크림 `#f3f0e9`·네이비 `#2b2d3a`·오렌지 `#e8631f`.
  - **cinematic(기본값)은 완전 무영향**(라이브 URL dry-run 비회귀 검증). 신규 파일 2개(template·prompt) + `cardnews.py` 함수군. 5종 전부 Edge 캡처 PNG 육안 검증 완료.
  - **전역 스킬화 (2026-08-02)**: `~/.claude/skills/cardnews/SKILL.md`로 어느 cwd에서든 사용(엔진은 블로그 repo 절대경로 호출, 리소스는 `__file__` 기준 해석이라 cwd 무관 — `_load_dotenv`도 `REPO_ROOT/.env`). 엔진·브랜드 자산(logo·.env·.fonts)이 블로그 repo에 묶여 그 저장소가 있어야 동작. 전역 스킬은 스타일 선택→아키타입→생성 워크플로 포함. 프로젝트 커맨드(`.claude/commands/cardnews.md`)는 in-repo 상대경로로 병존.

## 후킹 이미지 카드 (`/hook`, 2026-07-31)

`scripts/hookcard.py`가 포스트·영상·기사·논문을 **소셜용 티저 1장**(1080×1350)으로 만든다. 카드뉴스가 "여러 장으로 설명"이면 이쪽은 "한 장으로 클릭 유도"다. 출력은 `바탕화면/hookcard/<슬러그>/hook-01.png` + `card.json`.

- **cardnews.py를 import해 재사용**: 캔버스·`prep_logo`·`_font_css`(Black Han Sans)·이미지 3단 수급·`gemini_copy`·`_shot`(Edge 헤드리스)·`COPY_RULES`. **cardnews의 이 함수들을 고치면 `/hook`도 영향받는다.** 신규 파일은 `hookcard.py`·`hookcard_template.html`·`hookcard_prompt_template.txt` 3개뿐
- **레이아웃 (레퍼런스 PNG 실측 고정)**: 강조색 **`#F0B24B`**(카드뉴스 `#f5e14e`보다 따뜻한 금색) · 좌우 패딩 96 · 사진 `(32,140)`–`(1048,1222)` · 아이브로우(금색 대시 66×6 + 라벨 30px) · 헤드라인 2행(1행 흰색·2행 금색, BHS 최대 160px, 행 피치 147) · **하단 y1229~1281에 좌 로고(h52)·우 출처(우단 x984, 24px 2줄)**. 카드뉴스와 달리 로고가 **좌하단**이고 상단 닷네트워크 마크·페이지 번호·본문 블록이 없다. 회귀 검증은 카드뉴스와 동일하게 픽셀 대조(구현 후 실측: 로고 좌단·출처 우단·푸터 밴드 ±2px 일치)
- **헤드라인 `white-space: nowrap` 필수**: 자동 축소 루프가 `scrollWidth`로 폭 초과를 감지하는데, 줄바꿈이 허용되면 div가 넘치지 않아 축소가 발동하지 않고 헤드라인이 3~4행으로 깨진다(실측 사고). 폭 조절은 오직 font-size로 한다
- **카피**: `line1`+`line2`를 이어 읽어 한 문장, 끊는 지점에 긴장. **각 행 8자 내외**(길면 축소돼 힘이 빠짐). 카드뉴스의 "`~다` 종결" 규칙은 **적용하지 않는다** — 후킹은 의문형이 가장 강해서다(레퍼런스가 `공부일까, / 연기일까?`)
- **헤드라인 3단계 사고 강제 (2026-07-31 개선)**: 초기 프롬프트는 유형 예시만 줘서 `참여의 비용, 누가 내는가?`·`AI 도구, 왜 겉돌았나?`처럼 **주제를 되풀이하는 밋밋한 제목**이 절반쯤 나왔다. JSON 스키마에 사고 과정을 넣어 강제한다 — `sharp_facts`(자료에서 통념 반박·놀라운 수치·이름 붙일 수 있는 구체물·대가와 역설 3개 추출) → `drafts`(서로 다른 유형 4개) → `verdict`(고른 이유). 선별은 **세 시험**: ① 구체성(같은 주제의 다른 글에 올려도 말이 되면 실패) ② 정보(질문만 남기면 실패) ③ 구체명사(추상어만이면 실패). 적용 후 같은 글에서 `교사의 희망, 집단적 실천인가?` → `내 아이는 / 이제 없다`(논문의 '우리 아이·내 아이 구분을 넘어' 발견)로 바뀜
- **`validate_copy` 검사 항목**: 존칭체·훈계조·AI티·행 길이·콜론 + **추상어 위주**(비용·가치·의미·변화 등만 있고 수치·영문·구체물 없음) + **공허한 되묻기**(`~은 어떠한가?`류에 수치도 없음) + **단정체 어미+물음표 비문**(`모른다?`) + **출처 말줄임표**. 정규식으로 잡히는 것만 자동 재작성되고, 구체성 시험은 모델 판단 영역이라 프롬프트가 담당한다
- **도표는 히어로로 쓰지 않는다**: `_photo_like`가 `_is_paper`와 저채도·고휘도 판정으로 논문 figure·흰 바탕 도표를 탈락시킨다. 처음엔 카드뉴스처럼 `contain` 종이 패널을 넣었다가 다크 디자인과 충돌하고 도표 속 글자가 헤드라인과 경쟁하는 것을 실측 확인 → PDF 입력은 캡처를 건너뛰고 바로 생성으로 간다
- **생성 이미지는 1:1 + "피사체를 상단에"가 정답 (2026-07-31 실측)**: 카드뉴스 기본값 16:9를 그대로 쓰면 세로 박스(0.939)에서 cover가 **높이 기준**으로 맞아 세로 여백이 0이 된다 → `object-position`으로는 1px도 못 올리고 피사체가 헤드라인과 겹친다. `gemini_image(..., aspect=)` 인자를 추가(기본 16:9 유지, 카드뉴스 무영향)해 후킹은 `1:1`로 뽑고, 프롬프트에 **"주 피사체를 상단 절반에, 하단 3분의 1은 비워라"**를 명시한다. 사후 크롭보다 이쪽이 화질 손실이 없어 1차 해법이다
- **사후 재배치는 해상도 여유가 있을 때만**: `_recompose`가 피사체 밴드를 찾아 박스 비율로 다시 자르되, `MAX_UPSCALE`(1.35) 기준 하한(`BOX_H/1.35`=801px)보다 원본이 작으면 **자르지 않는다**. 원본 높이 대비 비율로 한도를 잡았다가 675px 이미지를 393×418로 깎아 2.6배 확대가 된 사고가 있었다(8%p 개선에 화질을 버림). 피사체 탐지는 **밝기 합이 아니라 상위 4% 밝은 픽셀 수**로 센다 — 합계를 쓰면 어둡지만 폭이 넓은 바닥 반사 띠가 작고 강한 실제 광원을 이겨 피크가 화면 맨 아래로 잡힌다(실측). 거기서 **연결된 구간만** 넓힌다
- **레터박스 제거는 12% 상한**: gemini가 비율을 맞추며 넣는 순검정 띠는 얇다. 상한이 없으면 다크 시네마틱 이미지의 의도된 어두운 여백(위 프롬프트로 요청한 하단 3분의 1)까지 깎아 1024→783로 해상도만 잃는다(실측)
- **단정체 어미 + 물음표 = 비문**: `모른다?`·`실천이다?`가 반복 생성됐다. 의문형은 권장하지만 어미까지 의문형(`~인가?`/`~일까?`/`~하는가?`)이어야 한다. `validate_copy`에 정규식으로 넣어 자동 재작성시킨다
- **스크림 필수**: 레퍼런스 원본은 사진이 이미 어두웠지만 밝은 사진이 들어오면 흰 헤드라인이 날아간다 → 사진 위에 하단 그라디언트(30%부터 99%까지)를 항상 덮는다
- **긴 출처는 상단 우측으로 (2026-08-03)**: 논문 제목이 길면 푸터 우측 출처 블록이 위로 자라 헤드라인을 침범한다. `hookcard_template.html` 스크립트가 **4단계로 물러난다** — ① 푸터 유지(2행 이내, 레퍼런스 실측 배치) ② `.source.top` 으로 상단 띠(0~140px) 이동, 폭은 헤드라인과 같은 **888px**(760px로 잡으면 제목 끝 한 단어가 3행으로 떨어져 고아 줄이 생김) ③ 24→20px 축소 ④ **마지막 줄만** 말줄임(저자·연도 줄은 불변). 이를 위해 `hookcard.py`가 출처를 `<br>` 한 덩어리가 아니라 `.s-line` 요소로 넘긴다. 템플릿 `<div class="source">`에 **`id="source"` 필수**(누락 시 스크립트가 조용히 no-op). 프롬프트도 "제목은 원문 그대로 전부 쓰고 스스로 줄이지 말 것"으로 바꿨다 — 미리 자른 제목으론 독자가 검색해도 원문을 못 찾는다. `validate_copy`의 "출처 말줄임표" 검사는 유지(Gemini의 어중간한 절단을 막는 별개 규칙)
- **자체 집필 글은 출처 = 블로그 주소 (2026-08-04)**: `## 출처`가 없는 자기 글은 모델이 저자·제목만 쓰고 **주소를 빼먹어, 카드를 봐도 원문을 찾아갈 수 없었다**(실측). `extract_post`가 `## 출처` 부재 시 front matter `permalink` + `_config.yml`의 `url`·`author.name`(하드코딩 아님, `blog_identity()`)으로 "자체 집필 글 + 글 주소" 힌트를 만들고, 프롬프트 `[source]`에 "`출처: 닷커넥터 <저자>` + 줄바꿈 + 주어진 주소 그대로, **2줄 초과 금지**(제목은 헤드라인과 중복)" 규칙을 넣었다. **`## 출처`가 있는 글(논문·기사 리뷰)은 기존대로 원 자료를 인용** — 우선순위가 바뀌지 않는다. 3줄이 되면 폴백이 출처를 상단 띠로 올려 좌하단 로고 옆 레퍼런스 배치가 깨지므로 2줄 상한이 핵심
- **카드를 포스트 히어로로 넣기 (2026-08-04, 9편 적용)**: 카드는 소셜용이지만 해당 글 맨 위 표지로도 쓴다. `assets/<permalink슬러그>-card.jpg`(PNG→JPEG q90, 장당 ~130KB)로 두고 `<figure style="max-width:560px;margin-inline:auto">`로 감싼다 — 1080×1350 세로라 본문 폭을 다 채우면 과하다. 원본보다 작은 사본(SNS 경유 등)을 받으면 확대 손실을 피해 그 폭을 그대로 쓴다. **선두에 자동 삽입된 teaser `<figure>`가 있으면 카드로 교체**한다(같은 자리·같은 역할이라 두면 큰 이미지가 두 장 쌓인다). 이미지 파일은 남겨 `header.teaser`(OG·리스트)로 계속 쓰이므로 미리보기는 그대로다. **`header.teaser`를 세로 카드로 바꾸지 말 것** — 카카오·OG가 가로로 잘라 헤드라인이 날아간다
- **이미지가 본문 첫 블록이면 description 이 빈다 (CRITICAL)**: Jekyll 자동 발췌가 `<figure>` 블록이 되고 `_includes/seo.html`이 `strip_html` 하면 `meta description`·`og:description`이 **빈 문자열**이 된다(공유 카드에 설명 증발). front matter에 `description:`을 직접 넣어 막는다. 문구는 본문 첫 문단에서 **추출**한다(생성 금지). 참고로 `/paper` 산출 글은 카드 삽입 전에도 이미 발췌가 `## 1. 연구의 목적` 헤딩이라 `"1. 연구의 목적"`이 description 이었다 — 카드를 넣는 김에 함께 고친다
- **후처리 QA**: 헤드라인이 원문에 없는 주장을 만들지 않았는지(놀라움은 자료 안 사실에서), 출처 저자·연도 환각, **자체 글이면 블로그 주소 포함 여부**, 생성 이미지에 글자 혼입 여부 육안 확인. 수정은 `card.json` 고쳐 `--rerender`(무과금)
- **`image_hint`가 글자를 부른다 (실측 2회)**: 힌트에 "essay page", "handwritten cheat sheet"처럼 **글이 적힌 사물**을 요구하면 `STYLE_SUFFIX`의 `No text, no letters` 지시를 덮고 화면 가득 가짜 글자가 나온다. 글이 필요한 주제는 힌트에서 필기 요구를 빼거나 "handwriting completely out of focus and unreadable"로 초점을 흐린다

## 네이버 블로그 크로스포스팅 (`/naver`)

`scripts/naver_crosspost.py`가 `_posts/` 포스트를 네이버 블로그(blog.naver.com/dot_connector)에 자동 발행한다.
네이버 글쓰기 API는 2020년 종료 → **Playwright(전용 프로필) + 스마트에디터 ONE 브라우저 자동화**.
Claude Code에서는 `/naver` 슬래시 커맨드로 호출한다 (`.claude/commands/naver.md` — 옵션·QA·운영 규칙 상세).

```bash
py -u scripts/naver_crosspost.py --limit 5     # 미게시 5편 발행 (기본, 하루 1회 권장)
py -u scripts/naver_crosspost.py --dry-run     # 대상·분류 미리보기
py -u scripts/naver_crosspost.py --login       # 로그인 쿠키 갱신 (풀렸을 때)
```

- **범위**: `2026-05-14-measuring-ai-ability...md` 이후 ~ 최신 (BASELINE_FILENAME 상수), 주간다이제스트 제외. 게시 이력 `scripts/naver_crosspost_state.json`(커밋 대상)
- **게시 이력 자동 동기화 (2026-08-03, 중복 발행 20편 사고 후 추가)**: 이력 파일이 곧 중복 방지 장치인데 그 장치가 로컬에만 있으면 무력하다. 실제로 이력이 커밋되지 않은 채 스케줄 실행이 돌아 원격에만 기록된 20편을 미게시로 판단해 두 번 올렸다. → `sync_state_before_run()`이 **대상 산정 전에** `origin/main`의 이력을 합치고(같은 글이 양쪽에 있으면 `posted_at` 늦은 쪽, 다르면 경고), `push_state()`가 실행 종료 시(중단·예외 포함) 이력 파일만 커밋·rebase·push 한다. `--no-git-sync`로 끔. 네트워크·인증 실패는 경고만 하고 발행은 계속
- **발행 전 네이버 존재 확인 = 중복 발행 최종 차단 (2026-08-20, 재발 사고 후 추가)**: 이력은 1차 방지책이지만 발행 후 이력이 원격에 못 올라가면(로컬 커밋이 다른 git 조작에 유실 등) 다음 실행이 같은 글을 재발행한다. 실제로 2026-08-20 16:00 스케줄 배치 7편이 이력에 안 남아(고아) 밤 수동 실행이 그대로 재발행했고, 스캔 결과 8.10·8.11/8.13 등 총 29제목이 중복이었다. → **Defense 1**: 각 글 발행 직전 공개 목록 API로 같은 제목 존재를 조회(`naver_existing_logno`/`_load_naver_title_index`, 로그인 불필요·1회 캐시)해 있으면 **발행 생략+이력 보정**. 이력이 무엇을 놓치든 중복 발행이 구조적으로 불가(소스 오브 트루스=네이버 자체). `--post` 단건 강제 발행은 예외. 실행 로그에 `[guard] 네이버 기존 글 N편 색인` / 건너뛸 때 `[SKIP] 네이버에 이미 존재…`가 뜬다. **네이버 조회 실패 시 색인이 비어 guard가 자동으로 꺼지고 기존 이력 기반 동작으로 복귀**(더 나빠지지 않음). → **Defense 2**: `push_state`가 rebase 충돌 시 그냥 포기(수동 push 안내)하던 것을, **이력 파일 단독 충돌이면 union(합집합) 자동 병합 후 `--continue`**(`_resolve_ledger_rebase`)하도록. 이력이 로컬에만 남아 유실되는 씨앗을 제거. 검증: Defense1 라이브 5/5, Defense2 임시레포 red-green 통과. **고아 정리**: 이미 생긴 중복은 `naver_delete_posts.py`로 제거하되 **이력에 기록된 쪽을 남기고 고아(이력 미기재)만 삭제**한다(둘 다 고아·둘 다 이력이면 사람 판단)
- **중복 정리 도구 `scripts/naver_delete_posts.py`**: `--file <targets.json>`·`--logno`·`--dry-run`·`--limit`. 삭제는 되돌릴 수 없어 매 건 ① 열린 글의 logNo 대조 ② `⋮` 메뉴(`a._open_overflowmenu`, class에 `_param(<logNo>)`) 안의 **숨은 삭제 링크**(class에 `_param(<logNo>|false|false)`) 선택 ③ 삭제 후 소멸 검증 — 세 겹 대조. 글 하단의 **보이는** 삭제 링크는 class가 `_param(<글 순번>|...)`라 어느 글인지 알 수 없어 쓰지 않는다
- **삭제된 글 URL은 최신 글로 리다이렉트된다 (실측, 위험)**: 지운 logNo로 접근하면 404가 아니라 **가장 최근 글이 열린다**. logNo 대조 없이 화면의 삭제 링크를 누르면 멀쩡한 최신 글이 지워진다. 위 ①이 이걸 막는다
- **`url: "unknown"`은 "다른 주소로 발행됨"이 아니라 "발행 결과 미확인"**: 실제로 발행이 성사되지 않은 기록일 수 있다. 2026-08-03 이 값을 중복 근거로 읽어 **유일본을 삭제**했다(재발행 복구). 중복 판정에서 남길 쪽 URL이 `unknown`인 행은 제외한다(`warn_unknown_pair`)
- **카테고리 자동 분류**: 인공지능교육 인사이트(26)/뇌기반 학습 과학(84)/생각하는 교실, 깊이있는 학습(87). Gemini 일괄 분류가 `scripts/naver_category_overrides.json`에 캐시(수동 교정 우선). categoryNo는 `postwrite?categoryNo=N` URL로 사전 선택
- **마루부리 15 구현 (실측)**: 붙여넣기 HTML의 인라인 `font-size:15px` → 에디터 `se-fs15` 자동 매핑(소제목 h2는 19 유지). 서체는 Ctrl+A 후 고정 툴바 버튼(`button.se-font-family-toolbar-button[data-group='propertyToolbar']`) → 드롭다운 `se-toolbar-option-text-button` 마루부리 클릭 — **서체만 바꾸면 크기는 요소별 보존됨**
- **발행 팝업 셀렉터 (실측)**: 상단 `button[class*='publish_btn']`(has-text('발행')는 숨은 예약발행 버튼을 잡으므로 금지) → 카테고리 라벨 `selectbox_button__` → 태그 input `placeholder*='태그'` → 최종 `button[class*='confirm_btn']`. 발행 후 URL은 `logNo=` 형식도 매칭
- **로그인 쿠키 함정**: NID_AUT/NID_SES는 세션 쿠키라 persistent 프로필로도 브라우저 종료 시 소실 → 로그인 감지 즉시 `scripts/.naver_profile/cookies.json`으로 백업하고 매 실행 시 `add_cookies` 재주입. 프로필·쿠키·스크린샷 디렉토리는 gitignore (쿠키 커밋 절대 금지)
- **세션 만료 안전장치 (2026-07-23, 첫 자동 실행이 서버측 세션 만료로 0건 실패한 뒤 추가)**: 실행 시작 시 `verify_login`이 `postwrite` 진입 리다이렉트 여부로 서버 기준 세션을 검증 — 만료면 `[EXPIRED]` 로그 + **종료코드 2**(`Get-ScheduledTaskInfo`의 LastTaskResult로 원격 확인 가능) 후 `--login` 재실행 필요.
- **로그인 2대 버그 수정 (2026-07-26)**: ① **'로그인 상태 유지' 체크박스 id가 `#keep`→`#loginStay`(name `nvlong`)로 변경**됐는데 구 셀렉터 실패를 `except: pass`로 삼켜, 매 로그인이 상태유지 없이 성립 → **하루 만에 세션 사망이 반복**된 근본 원인. `KEEP_SELECTORS` 후보 순회 + 실패 시 경고로 수정 ② **로그인 완료 판정이 `NID_AUT` 쿠키 '이름 존재'** 기준이라, 만료 백업 쿠키가 복원된 `--login`에서 사용자가 입력하기도 전에 성공 처리 후 창을 닫았다(= "로그인하고 바로 중단"). 시작 시점 **값과 달라지고 + 서버 `verify_login` 통과**해야 성공으로 본다. 추가로 수동 실행은 만료 감지 시 `ensure_session()`이 **그 자리에서 로그인 창을 띄우고 이어서 발행**(스케줄러 태스크는 `--no-auto-login` 인자 추가로 기존 즉시 종료 유지), `--check-session`으로 세션만 점검 가능(만료 시각 출력). 만료 쿠키는 복원 시 필터링. 수정 후 실측: 로그인 시 `NID_AUT`가 세션 쿠키 → **약 30일 만료 영속 쿠키**(2026-07-26 로그인 → 08-25 만료)로 발급되고 자동 복구 후 발행까지 이어짐
- **세션 30일은 상한이며 연장 불가 (2026-07-26 실측 3종)**: ① 만료는 발급 시점 기준 **고정** — 인증 요청을 보내도 밀리지 않음(sliding 아님) ② 유효 세션으로 `nidlogin.login`·네이버 메인 재방문해도 **재발급 안 됨** ③ 백업 파일의 `expires`만 늘리는 건 무의미(수명 판정은 서버). 따라서 30일에 한 번 사람이 로그인해야 한다 → **D-7부터 실행 로그에 만료 임박 경고**(`warn_if_expiring`)를 띄우고, `--force-login`(유효해도 폼을 띄워 30일 리셋)으로 미리 갱신. 스케줄 실행은 `--no-auto-login`이라 만료되면 조용히 멈추므로 이 경고가 유일한 사전 신호
- **배치 중단 방지 (2026-07-26)**: 발행 직후 네이버의 지연 리다이렉트(`PostList.naver`)가 다음 글 `postwrite` goto와 겹쳐 `interrupted by another navigation`으로 4번째 글에서 배치 전체가 죽었다 → `goto_editor()`가 진행 중 네비게이션 완료를 기다린 뒤 최대 3회 재시도(`write_post`·`update_post` 공용). 배치 루프도 단일 실패 시 `break` 대신 다음 글로 진행하고 **연속 2회** 실패에만 중단(실패 글은 미게시로 남아 다음 실행에 재시도) 주의: `nidlogin.login` 직접 방문은 **로그인 상태여도 폼에 머물러** 판별 신호로 못 씀(실측, 이 오판으로 유효 세션을 만료 처리한 사고 있었음). 로그아웃 상태에선 쿠키 백업을 덮어쓰지 않으며(마지막 정상 백업 보존), `--login`은 '로그인 상태 유지'를 자동 체크한다(가시성 실패 시 JS 폴백). 로그인은 반드시 `--login`이 띄우는 전용 프로필 창에서 — 일반 브라우저 로그인은 자동화에 반영 안 됨
- **한글 입력**: 제목은 `keyboard.insert_text`(IME 우회), 본문은 clipboard API(text/html) + Ctrl+V. 표·볼드·소제목·링크가 네이티브 컴포넌트로 변환됨
- **가독성 여백 (필수)**: 네이버 에디터는 문단 여백이 없어 변환 HTML 그대로면 벽글이 됨(첫 발행에서 실측) → `md_to_html`이 블록 요소 사이에 빈 문단 `<p><br></p>`을 자동 삽입(소제목 앞 여백, 소제목 뒤는 밀착). 기존 글 재포맷은 `--update <logNo> --post <파일>`(본문만 교체, 제목·카테고리·태그 유지)
- **브라우저 경고 배너 제거 (2026-07-26)**: 네이버 화면 위에 뜨던 "지원되지 않는 명령줄 플래그" 배너는 Edge 경고. `chrome://version` 명령줄 실측으로 원인 2개 확인 — 직접 넘기던 `--disable-blink-features=AutomationControlled`(제거해도 `add_init_script`의 webdriver 은닉으로 `undefined` 유지)와 Playwright 기본 `--no-sandbox`(`chromium_sandbox=True`로 해제). 둘 다 없애 위험 플래그 0개. 샌드박스 불가 환경 대비 msedge/기본 × 샌드박스 on/off 4단 폴백
- **발행 속도 상향 (2026-08-25, 이전 2026-07-26)**: 실행당 10편→**15편**, 글 간 45~90초→**25~50초**, 하루 상한 20편→**30편**(스케줄 태스크도 `--limit 15`). 15편이면 실행당 약 9분. 네이버는 하루 총량보다 **짧은 시간에 몰아쓰기**를 스팸 신호로 보므로 이번 상향은 백로그 소진을 우선한 선택이고 **검색 노출 관찰이 전제**다 — 이상 징후 시 `--limit 10 --daily-cap 20 --min-wait 45 --max-wait 90`(더 보수적이면 `--min-wait 180 --max-wait 360`)으로 롤백. `--daily-cap`(기본 30, 최근 24시간 `posted_at` 집계)이 수동+스케줄 중복 과발행을 차단(`--post` 단건은 예외). 상한에 걸린 실행은 남은 자리만 발행한다(2026-08-25 실측: 최근 24시간 19편 상태에서 `--limit 10` 실행이 1편만 처리)
- **운영 (자동)**: Windows 작업 스케줄러 `NaverCrosspost`가 매일 10:00·16:00에 15편씩 자동 발행 (2026-07-23부터, 2026-08-25 상향, 로그 `scripts/naver_task.log`). **태스크가 어느 시점에 소실돼 2026-08-22 재등록**(원인 미상 — `schtasks` 조회 0건이었음. `cmd /c py -u scripts\naver_crosspost.py --limit 15 --no-auto-login >> scripts\naver_task.log 2>&1`, WorkingDirectory=repo, StartWhenAvailable, 실행 상한 2h, 로그온 시에만 실행). 수동 실행 전 `Get-ScheduledTaskInfo -TaskName NaverCrosspost`로 존재를 확인하는 습관 유지. PC 꺼져 있으면 다음 부팅 시 실행. 로그인 풀리면 로그에 "로그인 쿠키가 없습니다"가 찍히고 건너뛰므로 `--login` 재실행. 첫 며칠 네이버 검색 노출 확인, 누락 시 하루 5편 감속. 게시일은 실행일(원 작성일은 글 말미 표기). 자동화는 네이버 약관 회색지대 — 본인 계정 유지. 백필 완료 후에도 새 포스트가 자동으로 대상에 포함되어 계속 크로스포스팅됨

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

## 공통: 프롬프트 문체·안티슬롭 규칙

> 자동화 스크립트(`/yeonsu`·`/paraph`·`/video`·`/paper` 등)의 Gemini 프롬프트 템플릿에 공통 적용되는 문체 규칙 묶음.

### 표 활용 규칙 (윤문화 방지)

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

### 날카로움+따뜻함 원칙 (11개 프롬프트 템플릿 전체 적용)

모든 Gemini 프롬프트 템플릿의 `비판적 낙관주의...제시한다.` 줄 바로 다음에 **[날카로움 + 따뜻함 원칙]** 블록이 삽입되어 있다 (2026-05-05 전체 적용).

이 블록은 문체 절대 규칙과 쌍으로 작동한다. 프롬프트 수정 시 이 블록을 제거하거나 위치를 옮기지 않는다.

핵심 지침:
- "중요하다" 대신 → 왜 중요한지, 무엇이 달라지는지를 수치·사례로 보여준다
- "~일 수 있다" 대신 → "~다" 또는 "~조건에서만 ~다"로 조건을 명시한다
- 한 섹션에 최소 한 문장은 독자가 멈추게 만드는 뾰족한 단언을 넣는다
- 금지: 입장 없이 요약만 하는 섹션 / "앞으로 더 연구가 필요하다" 식 마무리 / 내용 없는 감탄 문장

### AI 티 금지 표현 (4개 자동화 스크립트 전체 적용)

`/yeonsu`, `/paraph`, `/video`, `/paper` 4개 Gemini 프롬프트 템플릿 말미에 **Humanize KR v2.0.0** 기준 AI 표현 금지 규칙이 포함되어 있다.
프롬프트를 수정할 때 이 섹션을 제거하거나 축소하지 않는다.

**S1 (무조건 교체)**: `~를 통해`, `~을 넘어`, `결론적으로`, `시사하는 바가 크다`, `혁신적`, `'A'에서 'B'로` 변환 공식, 콜론 헤딩(`## 제목: 부제`), 이모지

**S2 (3회 이상 반복 시 교체)**: `또한/따라서/즉` 문두 남발, `~할 수 있다` 반복 종결, `~것이다` 종결 반복, 볼드 남용

> 출처: [epoko77-ai/im-not-ai](https://github.com/epoko77-ai/im-not-ai) — Humanize KR v2.0.0

### PLC 상투 마무리·콜론 헤딩 템플릿 레벨 차단 (2026-05-30)

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

## 공통: 의문문 제목 물음표 자동 통일 (2026-08-02)

`image_fetcher.normalize_question_title(content)` 공용 함수가 permalink 삽입 **직후** 4개 자동화 스크립트(`/paper`·`/video`·`/paraph`·`/yeonsu` 및 `/edit-*`·`/plain-*` 파생 전부)에서 호출되어, front matter `title:`이 의문문인데 물음표가 없으면 자동으로 `?`를 붙인다.

**왜**: Gemini가 의문형 제목(`~는가`·`~인가`·`~할까` 등)을 생성하며 물음표를 자주 빠뜨려 블로그 제목이 `?` 있는 것/없는 것으로 뒤섞였다. 전수 정리(2026-08-02, 기존 38편) 후 신규 글은 생성 시점에 통일한다.

**보수적 규칙 (오탐 방지)**:
- 제목에 이미 `?`가 있으면(중간·끝 어디든) 손대지 않음
- 강한 의문 종결어미(`는가·은가·운가·인가·던가·한가·까·까요·나요·냐·느냐`)로 **끝나는** 경우에만 삽입. 판정 정규식 `_STRONG_Q_ENDINGS`
- 닫는 따옴표 뒤 인용 의문구(`… '어떻게 인간다워지는가'`)는 종결이 아니라 자연히 제외됨
- 부제 분리(2026-08-03 콜론 확장): `A — 부제`(em/en 대시)는 앞 절이 의문이면 대시 앞에 `?`, `A: 부제`(콜론)는 앞 절이 의문이면 콜론을 떼고 `A? 부제`로(`?:` 회피). 판정 순서는 `끝 의문(끝에 ?)` → `대시` → `콜론` — 그래서 `AI 피로: … 아는가`처럼 콜론이 라벨 접두어이고 의문이 끝에 오면 끝에 `?`가 붙고 콜론은 그대로 유지됨. 라벨 접두어(`스티븐 울프럼:`)는 강한 종결어미 게이트로 자동 제외
- **자동 처리 안 함**(생성 후 QA 유지): `『책제목』` 내부 의문, `認可`·`閑暇` 같은 동형 명사, `…하나` 종결. 이런 애매 케이스는 7단계 후처리 QA에서 사람이 판단

## 공통: 제목 대시(—) 부제 자동 쉼표 치환 (2026-08-18)

`image_fetcher.normalize_title_dash(content)` 공용 함수가 `normalize_question_title` **바로 다음**(permalink·물음표 정규화 직후)에 4개 자동화 스크립트(`/paper`·`/video`·`/paraph`·`/yeonsu` 및 `/edit-*`·`/plain-*` 파생 전부)에서 호출되어, front matter `title:`의 em/en 대시 부제 구분자(` — `/` – `)를 **쉼표**로 치환한다.

**왜**: Gemini·집필이 `본문 결론 — 대상 설명` 꼴 부제 제목을 반복 생성해 제목에서 대시가 AI 티로 몰렸다(2026-08-18 최근 16편에서 집중 확인 → 전수 쉼표 치환). 블로그 전체에서 제목의 대시 부제는 쉼표로 통일한다.

**보수적 규칙 (오탐 방지)**:
- **공백으로 감싼** 대시(` — `/` – `)만 대상. 하이픈(`GPT-4`)·복합어·붙여쓴 대시(`설계도—현장`)·숫자 범위는 건드리지 않음
- 대시 앞 글자가 문장부호(`? ! .`)면 쉼표 대신 **공백**으로 치환(`?,` 표기 회피) — 그래서 `무엇인가? — 부제` → `무엇인가? 부제`
- `title:` 라인만 손댐(본문·다른 front matter의 대시는 불변). 호출 순서는 반드시 물음표 정규화 **뒤** — 의문형 `A — 부제`가 먼저 `A? — 부제`로 바뀐 뒤 대시가 공백으로 정리되도록
- 단위 테스트 9종(`plain`·`q-dash`·`book`·`hyphen`·`nospace-dash`·pipeline 2종·`body-untouched`) 전부 통과

**클로드 집필(`/column`·수동)에도 동일 정책**: 위 함수는 자동화 스크립트(Gemini 출력) 전용이라 `/column` 등 클로드가 직접 쓰는 글은 거치지 않는다. 제목을 지을 때 **대시로 부제를 붙이지 말 것**(`본문 — 부제` 금지) — 한 문장으로 쓰거나 정보 보존이 필요하면 쉼표로 잇는다. 이미 있는 대시 제목은 쉼표 치환.

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

**도서 원고 섹션 (2026-07-07, 8권 갱신 2026-07-21)** — `/lectures/` 허브는 "워크숍 강의"(`_data/lectures.yml`) + "도서 원고"(`_data/books.yml`) 2섹션 구성.
- 도서 1~7권은 `tigerjk9/Book-Publisher`(비공개 레포) 완성 원고 — 전부 라이브 Vercel 웹 도서로 새 탭 연결(웹 도서가 단일 진실 소스, 원고 개정 시 Vercel만 재배포하면 블로그는 무수정. 1권은 teacher-claude-guide.vercel.app — 최초 편입 때 배포 없는 줄 알고 블로그 내 전문 렌더링했다가 사용자가 URL 확인해 줘 제거).
- **8권(2026-07-21)은 한빛미디어 신간(요즘 교사를 위한 웹앱 만들기 with 바이브 코딩 · 서명 확정 2026-08-24 · 이상선·김진관·김상섭·이대형·윤신영 공저)으로 유일하게 블로그 내부 큐레이션 정리본(`_lectures/vibecode-for-teacher/`)에 연결** — 조판원고 전체 대신 목차·파트별 요약·실습 표·컴패니언 GitHub(lifeofpi-ux/vibecode-for-teacher)만.
- 통일 표지 재생성: `py scripts/gen_book_covers.py [볼륨…]` (인자 없으면 전체, `7 8`처럼 특정 권만 재생성 — 기존 01~06 무변경 유지용. 8권은 per-book `eyebrow`/`footer` 오버라이드로 닷커넥터 대신 한빛미디어 브랜딩. `.fonts/` Pretendard 필요, 출력 `assets/lectures/books/book-0N-cover.jpg`, 권별 액센트 컬러).
- 상태 배지: 최신(앰버)·이전 판(슬레이트) — **최신은 단일**이라 신간 추가 시 직전 최신 권의 `status: 최신` 제거 + 표지 재생성(8권 추가로 7권 최신 배지 해제).
- **잠금 카드**(`locked: true`+`locked_payload`)는 대상 URL을 **AES-256-GCM + PBKDF2-HMAC-SHA256(20만회)**로 암호화한 값이다(2026-07-30 기존 반복키 XOR에서 교체 — XOR은 known-plaintext로 비번 없이 URL 복원이 가능했음). payload(base64) 레이아웃 `[ver=2][salt:16][iv:12][ct+tag]`, 카드마다 salt/iv가 랜덤이라 동일 URL도 암호문이 다르고 카드 간 상관관계가 없다. 복호화 JS는 `_pages/lectures.md` — 비번 입력은 window.prompt가 아니라 **커스텀 모달**(`.lec-pw-*`, 스타일 `_sass/_lectures.scss`, 2026-07-30 모바일 비율 문제로 교체. 오류 인라인+shake, ≤600px 상단 배치, 팝업 차단 시 같은 탭 폴백, 잠금 카드 제목 표시 `.lec-pw-name`+등장 애니메이션은 같은 날 PC 폴리시). 재암호화 레시피·표준 절차는 메모리 `project_locked_cards`. 잠금 자료 전부 **하나의 공통 비번**을 공유하며 비번 값은 코드/문서에 남기지 않음(메모리에만). 내부 잠금 페이지(`_lectures/<slug>/`)는 front matter에 `sitemap: false` + `noindex: true`, 허브 카드 썸네일은 슬러그 없는 중립 경로(`/assets/lectures/covers/<hash>.jpg`)를 써서 URL 노출을 줄였다. **단 정적 사이트라 근본은 obscurity** — 콘텐츠 페이지·외부 Vercel 앱 자체엔 인증이 없어 URL이 알려지면 비번 없이 열린다(진짜 비공개는 서버측 게이트 필요).
- 4권 웹 도서와 `vibe-coding-git-github` 슬라이드 강의는 동일 주제의 별개 자산(도서 vs 강의)으로 의도적 공존.
- 카드에는 저자 크레딧 필수(도서 `author` 필드 + "저자" 라벨, 타사 원본 자료는 `author` 원작 + `curator` 2단 — AIEP 튜토리얼 선례), 섹션 도입 산문은 넣지 않는다(헤딩+카드 그리드만). 외부 링크형 강의 카드(학생용 생성형 AI 안내서·AIEP·AX 핸드북) 표지는 사이트 히어로 스크린샷 — 이 머신은 playwright·gstack browse가 없거나 고장이라 **Edge 헤드리스**(`--user-data-dir` 임시 프로필 필수)로 캡처한다.

### 자료실 탭과 대용량 자료 (2026-08-19)

상단 탭 이름은 **자료실**이다(구 "강의자료" — 저서 10권·워크숍 강의·도서 원고에 교실 자료까지 들어와 범위가 안 맞았다). 라벨은 `_data/navigation.yml`·`_pages/lectures.md` front matter·`_layouts/lecture.html` breadcrumb 세 곳에 있으니 함께 고친다. 허브 섹션은 서재 → 워크숍 강의 → **교실 자료**(`_data/resources.yml`) → 도서 원고 순이며, 교실 자료 카드는 `.lecture-card--media` 마크업을 그대로 쓰되 크레딧 라벨만 원작/큐레이션 대신 **자료/아카이빙**이다.

**대용량 자료는 저장소에 넣지 않는다 (CRITICAL)**. 발행 사이트가 이미 약 865MB인데 GitHub Pages 한도가 1GB다. 수십 MB 이상 다운로드 자료는 **GitHub 릴리스 자산**으로 올리고 페이지에서 링크만 건다(릴리스는 이 한도에 미포함, 파일당 2GB). 첫 사례가 `eval-assessment-2026` 태그 — 대전교육과학연구원 서·논술형 평가도구 29개 218MB, 안내 페이지 `_lectures/eval-assessment-tool/`.

- **릴리스는 한글 파일명을 지운다**: `2026학년도 2학기 수학과 … 목록(3~6학년).hwp` → `2026.2.3.6.hwp`로 뭉개지고 서로 충돌한다. 업로드 전 영문 슬러그로 재명명한다(`2026-s2-math-g3-6-tools.pdf` 꼴). 매핑 스크립트는 누락·중복·미매핑을 assert로 막고 업로드 후 `gh api …/releases/tags/<tag>`의 자산 목록과 본문 링크를 대조한다.
- 릴리스는 교차 출처라 `<a download="한글이름">`이 **무시된다**. 방문자는 영문 파일명으로 받으므로 페이지 표에 한글 제목·쪽수·용량을 함께 적는다.
- 이 머신엔 Ruby가 없어 `jekyll build` 사전 검증이 불가하다. 푸시 후 `gh run watch`로 배포를 확인하고 라이브 URL을 Edge 헤드리스로 캡처해 검증한다.

**진입점**:
```powershell
/lecture-archive <zip-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright] [--rerun parser|curator|builder]
```

**의존성**: playwright(Chromium ~150MB)·beautifulsoup4·google-generativeai·weasyprint·Pillow·PyYAML·pytest. 기존 `.env`의 `GEMINI_API_KEY` 재사용.

**알려진 동작 특성**:
- **`_pages` include 필수**: `_config.yml`에 `include: [_pages]` 누락 시 `/lectures/` 404. Jekyll은 `_` 접두사 디렉토리를 기본 무시한다.
- **PDF iframe 자동 로드 금지**: 강의 페이지에 `<iframe src="….pdf">`를 항상 로드하면 모바일 브라우저가 렌더 대신 **페이지 진입 즉시 다운로드**를 트리거한다(문해력 교안에서 실측). 다운로드형 자료는 `.gyoan-btn` 내려받기 버튼(`download` 속성) + 클릭 시 lazy iframe 미리보기(≤1023px 미리보기 숨김) 패턴을 쓴다 — `_lectures/literacy-reading-muscle/index.md` 참고.
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
8. **논문리뷰 태그 확인 (`/edit-paper` 한정)** — Gemini가 front matter `tags:`에 `논문리뷰`를 종종 누락한다. 리서치 허브(/research/) 편입의 1차 신호이므로 없으면 추가한다 (출처 블록 arXiv/DOI가 있으면 자동 보완되지만, DOI 없는 논문은 태그가 없으면 허브에서 누락). 확인 후 `build_research_db.py` → `build_embeddings.py` 재실행·커밋.

**운영 노트**

- 한글·따옴표가 든 커밋 메시지는 PowerShell here-string이 git 인자 파싱을 깨뜨린다(메시지 단어가 pathspec로 오인). `git commit -F <임시 메시지 파일>` 로 처리한다.
- `/edit-*` 호출 시 사용자가 URL 뒤에 편집 지시·맥락을 길게 덧붙이면, 그대로 명령행에 이으면 `web_to_post.py`의 `urls`(`nargs="+"`)가 한국어 단어를 전부 URL로 오인한다. URL은 positional 하나로, 지시문은 `--notes '<전문>'` 로 전달한다(프롬프트의 `{OWNER_NOTES}` 자리에 주입, 단일 URL `--edit` 경로에서 동작 확인됨).
- 추출 실패 시(예: `yozm.wishket.com` 은 CloudFront가 requests·Jina 모두 403 차단 → 제목이 `The request could not be satisfied`·`403`·슬러그 `content-access-forbidden`류) Gemini가 "콘텐츠 접근 불가" 환각 메타 포스트를 생성·푸시한다. 즉시 `git rm` + 미추적 소스 이미지 로컬 삭제 + 사용자에게 차단 사실을 정직하게 보고한다. 대안: 사용자가 PDF·스크린샷·본문을 제공하면 본문을 임시 `.md`(첫 줄 `# <원문 제목>`)로 저장 후 `python scripts/web_to_post.py "<임시.md 절대경로>" --edit` 로 처리한다(`fetch_content` 가 로컬 파일 경로를 직접 지원하며 첫 줄을 title로 사용). 처리 후 출처를 원문 URL로 교정하고 임시 파일을 정리한다.