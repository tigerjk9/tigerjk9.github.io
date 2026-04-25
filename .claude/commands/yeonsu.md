# /yeonsu — 다양한 입력 → 교원 연수 자료

이 스킬은 유저 레벨 스킬이므로 어디서든 호출 가능하다.
모든 작업의 대상은 아래 블로그 프로젝트이다:

```
BLOG_ROOT = "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
```

## 사용법

```
/yeonsu <입력> [옵션]
```

입력 가능한 형식:
- YouTube URL: `https://youtube.com/watch?v=...`
- 웹 URL: `https://example.com/article`
- PDF 파일 경로: `_papers/paper.pdf` 또는 절대 경로
- 텍스트·마크다운·docx 파일 경로

---

## 실행 순서

**1단계 — 입력 확인**
`$ARGUMENTS`가 비어 있으면 입력값(URL 또는 파일 경로)을 먼저 물어보세요.

**2단계 — 연수 조건 확인 (반드시)**
입력값이 확인됐으면, 스크립트 실행 전에 아래 두 가지를 한 번에 물어보세요:

> "강의 시간과 수준을 알려주세요.
> - 시간: 몇 분? (기본 120분)
> - 수준: 초급 / 중급?"

**3단계 — 마크다운 연수 교재 생성**
답변을 확인한 뒤 아래 명령어를 실행하세요:

```bash
cd "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
python scripts/lecture_script.py $ARGUMENTS --duration <분> --level <초급|중급>
```

스크립트가 완료되면 `_posts/YYYY-MM-DD-slug.md` 경로를 확인하세요.

---

## 동작 순서 전체

1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 입력 타입 자동 감지 (YouTube / 웹 URL / PDF / 파일)
3. 입력 타입에 맞게 콘텐츠 추출
   - YouTube: youtube-transcript-api → yt-dlp VTT → description 순으로 시도
   - 웹 URL: requests + BeautifulSoup → Jina Reader 폴백
   - PDF: pdfplumber → PyMuPDF 순으로 시도
   - 파일: docx 또는 텍스트로 읽기
4. `_posts/` 전체에서 키워드 매칭으로 관련 포스트 최대 3개 자동 탐색 → 프롬프트에 포함
5. 강의 시간에 맞는 챕터 수 자동 계산 (45분/챕터 기준)
6. Gemini로 교원 연수 교재 생성 (수준·관련 포스트 반영)
7. `_posts/YYYY-MM-DD-slug.md` 저장 후 git push

## 출력 파일

| 파일 | 위치 | 용도 |
|------|------|------|
| `.md` | `_posts/` | 블로그 포스트 (Jekyll) |

## 옵션

| 옵션 | 설명 |
|------|------|
| `--duration N` | 강의 시간(분) (기본값: 120) |
| `--level 초급\|중급` | 강의 수준 (기본값: 중급) |
| `--dry-run` | 파일 저장 없이 출력만 (테스트용) |
| `--no-push` | git push 없이 로컬 저장만 |
| `--slug SLUG` | 파일명 슬러그 직접 지정 |
| `--date YYYY-MM-DD` | 포스트 날짜 지정 |
| `--model MODEL` | Gemini 모델 ID (기본값: gemini-2.5-flash) |
