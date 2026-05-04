# /edit-yeonsu — 다양한 입력 → 교원 연수 자료 (블로그 주인장 목소리 강화 버전)

이 스킬은 유저 레벨 스킬이므로 어디서든 호출 가능하다.
모든 작업의 대상은 아래 블로그 프로젝트이다:

```
BLOG_ROOT = "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
```

## 사용법

```
/edit-yeonsu <입력> [입력2 ...] [옵션]
```

입력 가능한 형식:
- YouTube URL: `https://youtube.com/watch?v=...`
- 웹 URL: `https://example.com/article`
- PDF 파일 경로: `_papers/paper.pdf` 또는 절대 경로
- 텍스트·마크다운·docx 파일 경로
- **복수 입력 지원**: 여러 URL/파일을 공백으로 구분하면 하나의 아티클로 통합 생성

## 설명
기존 `/yeonsu`와 달리 **블로그 주인장 목소리 강화** 프롬프트를 사용합니다.

**스타일 특징**:
- 챕터 구조 유연화 — 에피그래프·케이스오프너는 자연스러울 때만 사용
- 케이스오프너가 있어도 딜레마 질문으로 끝낼 필요 없음
- 핵심정리는 2~3문장도 허용
- 필자의 직접 판단과 절제된 비관론이 최소 2곳 드러남
- 도입부가 질문에 국한되지 않음 — 선언·탄식·일화·역설 등 다양한 첫 문장
- 크로스오버 섹션이 억지 연결이면 본문에 통합하거나 생략
- 본문 내 [IMAGE: query] 마커로 다중 이미지 자동 삽입 (Pexels/DDG 검색)
- 핵심 판단 강조 시 `~됨·~임` 명사형 단문 허용

---

## 실행 순서

**1단계 — 입력 확인**
`$ARGUMENTS`가 비어 있으면 입력값(URL 또는 파일 경로)을 먼저 물어보세요.

**2단계 — 즉시 실행**
입력값이 확인되면 바로 아래 명령어를 실행하세요. 시간·수준은 묻지 않고 기본값(120분/중급)으로 실행합니다.
옵션이 `$ARGUMENTS`에 포함된 경우 그대로 전달하세요.

```bash
cd "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
python scripts/lecture_script.py $ARGUMENTS --edit
```

스크립트가 완료되면 `_posts/YYYY-MM-DD-slug.md` 경로를 확인하세요.

---

## 동작 순서 전체

1. `.env`에서 GEMINI_API_KEY 자동 로드
2. 입력 타입 자동 감지 (YouTube / 웹 URL / PDF / 파일)
3. 입력 타입에 맞게 콘텐츠 추출 (복수 입력 시 순서대로 추출 후 통합)
4. `_posts/` 전체에서 키워드 매칭으로 관련 포스트 최대 3개 자동 탐색 → 프롬프트에 포함
5. 강의 시간에 맞는 챕터 수 자동 계산 (45분/챕터 기준)
6. Gemini로 블로그 주인장 목소리 교원 탐구 에세이 생성 (`edit_lecture_prompt_template.txt` 사용)
7. [IMAGE: query] 마커를 Pexels/DDG 이미지로 교체 (다중 이미지)
8. `_posts/YYYY-MM-DD-slug.md` 저장 후 git push

## 이미지 삽입 규칙

포스트에 이미지를 삽입할 때는 반드시 `<figure>/<figcaption>` HTML 형식을 사용한다.
마크다운 `![alt](url)` 형식은 Minimal Mistakes 테마의 `figure { display: flex }` CSS 때문에 캡션이 이미지 옆(인라인)에 붙으므로 **절대 사용하지 않는다**.

```html
<figure>
<img src="/assets/이미지파일명.png" alt="한국어 이미지 설명">
<figcaption>이미지 아래에 표시될 한국어 캡션 문장.</figcaption>
</figure>
```

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
