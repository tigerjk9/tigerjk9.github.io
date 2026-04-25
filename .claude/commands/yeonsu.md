# /yeonsu — 다양한 입력 → 교원 연수 자료

이 스킬은 유저 레벨 스킬이므로 어디서든 호출 가능하다.
모든 작업의 대상은 아래 블로그 프로젝트이다:

```
BLOG_ROOT = "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
```

## 사용법

```
/yeonsu <입력> [입력2 ...] [옵션]
```

입력 가능한 형식:
- YouTube URL: `https://youtube.com/watch?v=...`
- 웹 URL: `https://example.com/article`
- PDF 파일 경로: `_papers/paper.pdf` 또는 절대 경로
- 텍스트·마크다운·docx 파일 경로
- **복수 입력 지원**: 여러 URL/파일을 공백으로 구분하면 하나의 아티클로 통합 생성

---

## 실행 순서

**1단계 — 입력 확인**
`$ARGUMENTS`가 비어 있으면 입력값(URL 또는 파일 경로)을 먼저 물어보세요.

**2단계 — 즉시 실행**
입력값이 확인되면 바로 아래 명령어를 실행하세요. 시간·수준은 묻지 않고 기본값(120분/중급)으로 실행합니다.
옵션이 `$ARGUMENTS`에 포함된 경우 그대로 전달하세요.

```bash
cd "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
python scripts/lecture_script.py $ARGUMENTS
```

스크립트가 완료되면 `_posts/YYYY-MM-DD-slug.md` 경로를 확인하세요.

---

## 동작 순서 전체

1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 입력 타입 자동 감지 (YouTube / 웹 URL / PDF / 파일)
3. 입력 타입에 맞게 콘텐츠 추출 (복수 입력 시 순서대로 추출 후 통합)
   - YouTube: youtube-transcript-api → yt-dlp VTT → description 순으로 시도
   - 웹 URL: requests + BeautifulSoup → Jina Reader 폴백
   - PDF: pdfplumber → PyMuPDF 순으로 시도
   - 파일: docx 또는 텍스트로 읽기
4. `_posts/` 전체에서 키워드 매칭으로 관련 포스트 최대 3개 자동 탐색 → 프롬프트에 포함
5. 강의 시간에 맞는 챕터 수 자동 계산 (45분/챕터 기준)
6. Gemini로 교원 연수 교재 생성 (수준·관련 포스트 반영)
7. `_posts/YYYY-MM-DD-slug.md` 저장 후 git push

## 이미지 삽입 규칙

포스트에 이미지를 삽입할 때는 반드시 `<figure>/<figcaption>` HTML 형식을 사용한다.
마크다운 `![alt](url)` 형식은 Minimal Mistakes 테마의 `figure { display: flex }` CSS 때문에 캡션이 이미지 옆(인라인)에 붙으므로 **절대 사용하지 않는다**.

```html
<figure>
<img src="/assets/이미지파일명.png" alt="한국어 이미지 설명">
<figcaption>이미지 아래에 표시될 한국어 캡션 문장.</figcaption>
</figure>
```

- 이미지 파일: `assets/` 디렉토리에 저장, `/assets/파일명.png`로 참조
- Naver 블로그 이미지 URL: `mblogthumb-phinf.pstatic.net/...?type=w800` 형태 사용
- `main.scss`의 `.page__content figure`에 `flex-direction: column; align-items: center` 적용 → 캡션이 항상 이미지 아래 가운데 정렬
- `figure img`에 `width: auto !important` 적용 → 원본 사이즈 유지 (화질 보존)

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
