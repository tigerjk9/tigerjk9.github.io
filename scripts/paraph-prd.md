# /paraph 스킬 PRD

## 목적

웹 아티클 URL을 한국어 블로그 포스트로 자동 패러프레이즈하는 반복 가능한 파이프라인.
번역이 아니라 **재서술** — 원본 논지를 이해한 뒤 교육 전문가의 목소리로 처음부터 새로 쓴다.
`/paper`(PDF), `/video`(YouTube)와 같은 계열의 자동화 스킬.

---

## 3가지 모드

| 모드 | 호출 | 프롬프트 템플릿 | 출력 |
|------|------|----------------|------|
| 단일 URL | `python scripts/web_to_post.py <URL>` | `web_prompt_template.txt` | 신규 `_posts/YYYY-MM-DD-slug.md` |
| 복수 URL 통합 | `python scripts/web_to_post.py <URL1> <URL2> [...]` | `web_multi_prompt_template.txt` | 신규 통합 포스트 1개 |
| 머지 (`--into`) | `python scripts/web_to_post.py <URL> --into _posts/....md` | `web_merge_prompt_template.txt` | 기존 파일 덮어쓰기 |

---

## 파이프라인 흐름

```
URL 입력 (1개 이상)
  → 기존 _posts 스캔: 카테고리·태그 빈도 수집
  → requests + BeautifulSoup: 1차 추출
  → 본문 500자 미만이면 Jina Reader(r.jina.ai) 폴백 (JS 렌더링 대응)
  → 크로스오버 분야 random.choice() (20개 풀, 머지 모드는 제외)
  → 적절한 프롬프트 템플릿 + 기존 카테고리/태그 주입
  → Gemini API: 한국어 포스트 생성
  → _posts/YYYY-MM-DD-slug.md 저장 (또는 --into 파일 덮어쓰기)
  → date 연도 강제 복원 (Gemini 임의 변경 버그 가드)
  → git add → commit → push
```

---

## 포스트 구조

고정된 섹션 수는 없다. `/paper`가 6섹션 고정인 것과 달리, 원문 구조를 존중한다.

- **도입부**: 문제의식·후킹 (3~5문장)
- **본문**: 원문 흐름을 살리되 재구성 자유 — 섹션 제목은 Gemini가 생성
- **크로스오버 섹션**: "~의 시선으로 보면" — 20개 분야 풀에서 랜덤 선택
- **출처**: 원본 URL (URL은 그대로 유지, DOI 없음)

### 크로스오버 분야 풀 (20개)

신경과학, 행동경제학, 생태학·먹이그물 이론, 언어학·인지언어학, 음악이론·즉흥연주,
요리과학·발효학, 스포츠과학·운동학습, 도시계획·공간행동학, 연극학·서사이론,
진화생물학·공진화, 철학·인식론, 인류학·문화진화론, 물리학·복잡계 이론, 면역학·항상성,
경제사·제도경제학, 게임이론·협력의 진화, 수면과학·기억 공고화, 동물행동학·각인 이론,
기상학·카오스 이론, 정보이론·엔트로피.

---

## 머지 모드 (`--into`) 설계

기존 포스트에 신규 자료를 녹여 **같은 파일을 덮어쓴다**. 신규 포스트 생성이 아니다.
SEO 슬러그와 발행 시각을 보존하는 것이 핵심.

### 보존 원칙
- front matter `date` 절대 변경 금지
- 기존 섹션 제목·순서 보존
- 기존 크로스오버 분야명 변경 금지 (random 재선택 안 함)
- 기존 문체·카테고리·태그 유지

### 채굴 우선순위 — 신규 자료에서 다음을 발굴해 통합
1. 충격적 수치·통계
2. 저자의 인상적 비유·은유
3. 잘 알려지지 않은 인용·출처(개념 제안자 이름 등)
4. 구체적 사례·실험 결과
5. 기존에 없는 균형 관점·비판 → 별도 섹션 신설 정당
6. 구조적·정책적 대안

### 새 섹션 신설 기준 (셋 중 하나 충족 시)
- 자료의 한계·비판적 관점이 있어 균형감 필요
- 기존 분류 체계를 확장하는 새 층위 (예: 3분류 → 4분류 추가)
- 기존 섹션 어디에도 자연스럽게 들어가지 못하는 독자적 관점

### 커밋 메시지 컨벤션
- 신규 모드: `Add: ...`
- 머지 모드: `Update: ...`

---

## 패러프레이즈 원칙

- 전문 용어는 쉬운 말로 풀되 정확성 유지
- 딱딱한 문장을 교육 전문가의 따뜻한 어투로 재서술
- 구체적 예시·비유 추가, 한국 교육 맥락 삽입 허용
- 중요한 수치·데이터·사례는 빠짐없이 포함
- 복잡한 구조는 목록·표로 정리
- 번역 금지 — 반드시 재서술

---

## 문체·형식 규칙

- **문체**: `~이다`, `~한다` 단정체. 존칭(`~합니다`)·명사형(`~것`) 어미 금지
- **따옴표**: 불필요한 `'` `"` 자제, 강조는 볼드로
- **볼드**: 핵심 개념·고유명사·수치만
- **크로스오버 섹션 제목**: "{분야}의 시선으로 보면" 고정 패턴
- **슬러그**: Gemini가 front matter `slug:` 필드로 영문 생성 → 스크립트가 파일명으로 사용 후 필드 제거

---

## 콘텐츠 추출 우선순위

1. `requests` + `BeautifulSoup` — 정적 HTML 파싱, `article`·`main` 우선
2. `r.jina.ai/{url}` — JS 렌더링 페이지 폴백 (본문 500자 미만 시 자동 전환)
3. Naver 블로그처럼 WebFetch가 막히는 도메인도 Jina Reader 경유로 추출 가능

---

## 비공개 레포 콘텐츠 우회 (Second-Brain 등)

`tigerjk9/Second-Brain` 같은 private 레포의 `.md`는 `raw.githubusercontent.com`·`github.com/blob/` 모두 404.

### 절차

```bash
# 1) 로컬 클론 디렉터리에서 임시 HTTP 서버 기동
cd "C:/Users/user/Desktop/GitHub Blog/Second-Brain"
python -m http.server 8765 > /dev/null 2>&1 &

# 2) localhost URL을 /paraph에 전달
cd "C:/Users/user/Desktop/GitHub Blog/tigerjk9.github.io"
python scripts/web_to_post.py "http://localhost:8765/notes/debates/<파일>.md"

# 3) 서버 종료 (PowerShell)
Get-NetTCPConnection -LocalPort 8765 -State Listen |
  ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }
```

### 후처리 (필수)
- 생성 포스트의 `<출처>`가 `http://localhost:8765/...`로 찍힘 → `tigerjk9/Second-Brain — <상대경로>` 표기로 교체
- Gemini가 한글 퍼센트 인코딩 URL 끝자락을 깨뜨릴 수 있음 (예: `설계` → `설곳`) — 출처 섹션 수동 검증
- 후처리 커밋은 별도: `Fix: paraph 포스트 출처를 localhost → <원본> 경로로 교체`

---

## 파일 구조

```
scripts/
  web_to_post.py              # 메인 스크립트 (단일·복수·머지 모두 처리)
  web_prompt_template.txt     # 단일 URL 프롬프트
  web_multi_prompt_template.txt # 복수 URL 통합 프롬프트
  web_merge_prompt_template.txt # --into 머지 프롬프트
  requirements.txt            # requests, beautifulsoup4, google-generativeai
.env                          # GEMINI_API_KEY (gitignore)
.claude/commands/paraph.md    # /paraph 슬래시 커맨드 정의
```

---

## CLI 옵션

```bash
python scripts/web_to_post.py <URL> [URL2 ...]       # 변환 + git push
python scripts/web_to_post.py <URL> --dry-run        # 출력만, 저장 안 함
python scripts/web_to_post.py <URL> --no-push        # 로컬 저장만
python scripts/web_to_post.py <URL> --slug SLUG      # 파일명 슬러그 지정
python scripts/web_to_post.py <URL> --date YYYY-MM-DD
python scripts/web_to_post.py <URL> --model gemini-2.5-flash
python scripts/web_to_post.py <URL> --into _posts/YYYY-MM-DD-slug.md  # 머지
```

---

## 품질 기준

- 원문 논지가 왜곡 없이 재서술되는가 (번역체 아님)
- 단정체 문체가 전편에 유지되는가
- 크로스오버 섹션이 원문과 자연스럽게 연결되는가 (억지 연결 금지)
- 머지 모드에서 기존 `date`·슬러그·기존 섹션 제목이 그대로인가
- 출처 섹션 URL이 올바르게 기재되었는가 (localhost·깨진 인코딩 없음)

---

## 알려진 제약

- Gemini가 `date:` 연도를 임의로 바꾸는 버그 → 스크립트가 생성 후 강제 복원
- Gemini가 한글 퍼센트 인코딩 URL 마지막 바이트를 깨뜨리는 경우 있음 (드물지만 반복 관찰)
- 비공개 GitHub 레포는 URL 기반 접근 불가 → localhost http.server 우회 필요
- 기업 네트워크 SSL 인증서 오류 → `ssl._create_unverified_context` + requests 세션 패치로 우회
- Windows cp949 인코딩 환경에서 subprocess 출력 깨짐 (기능에는 영향 없음)
- 한국어 제목에서 슬러그 직접 추출 불가 → Gemini slug 생성으로 해결
