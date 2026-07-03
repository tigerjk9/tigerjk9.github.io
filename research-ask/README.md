# research-ask — 리서치 허브 AI API

tigerjk9.github.io 리서치 허브의 시맨틱 검색(`/api/embed`)과 RAG 질의응답(`/api/ask`)을 담당하는 Vercel 서버리스 API.

## 아키텍처

```
블로그(GitHub Pages, 데이터 원본)          이 서비스(Vercel, 무상태 컴퓨트)
  assets/research-db.json        ←fetch←   콜드스타트 시 로드, 6h 캐시
  assets/research-rag-index.json ←fetch←   (재배포 없이 콘텐츠 자동 갱신)
  /research/  /ask/              →호출→    /api/embed  /api/ask  /api/health
```

- 논문리뷰가 늘어나면 블로그 쪽에서 `build_research_db.py` + `build_embeddings.py`만 재실행·커밋하면 된다. 이 서비스는 재배포 불필요.
- 의존성 제로 — Gemini REST를 직접 호출한다.

## 배포 (최초 1회)

```bash
cd research-ask
npx vercel login          # 브라우저 로그인
npx vercel link           # 새 프로젝트로 연결 — 이름: dotconnector-ask 권장
npx vercel env add GEMINI_API_KEY production   # .env의 키 값 입력
npx vercel --prod
```

프로젝트 이름을 `dotconnector-ask`로 하면 블로그 페이지(`research.md`, `ask.md`)의
`ASK_API` 상수(`https://dotconnector-ask.vercel.app`)를 수정할 필요가 없다.
다른 이름을 쓰면 두 파일 상단의 `ASK_API` 값을 배포 URL로 바꾼다.

## 환경변수

| 변수 | 필수 | 설명 |
|------|------|------|
| `GEMINI_API_KEY` | O | Google AI Studio 키 |
| `BLOG_ORIGIN` | X | 데이터 원본 (기본 `https://tigerjk9.github.io`) |
| `GEN_MODEL` | X | 생성 모델 (기본 `gemini-2.5-flash`) |
| `ALLOWED_ORIGINS` | X | 추가 CORS 오리진 (쉼표 구분) |

## 엔드포인트

- `GET /api/health` → `{ok, posts, chunks, hasKey}` — 블로그가 AI 기능 노출 여부 판단에 사용
- `POST /api/embed` `{q}` → `{vec: float[768]}` — 쿼리 임베딩 (문서 코사인은 클라이언트)
- `POST /api/ask` `{q, history?}` → `{answer, sources[]}` — 논문리뷰 근거 RAG 답변

## 남용 방지

- CORS 허용: `tigerjk9.github.io` + localhost
- 인스턴스 로컬 레이트리밋: embed 10/min·1200/day, ask 6/min·400/day
- 질문 500자 제한, 답변 토큰 상한 1600
- 주의: 레이트리밋은 인스턴스 메모리 기반이라 완화용이다. 트래픽이 커지면 Upstash Redis로 교체할 것.

## 로컬 테스트

블로그 리포 루트에서 (Gemini 키가 .env에 있어야 함):

```bash
node research-ask/test/local-harness.mjs "AI 피드백이 학습에 효과가 있나?"
```
