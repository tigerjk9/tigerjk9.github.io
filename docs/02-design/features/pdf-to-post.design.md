# [Design] pdf-to-post

> Plan 참조: `docs/01-plan/features/pdf-to-post.plan.md`

---

## 1. 파일 구조 (최종)

```
tigerjk9.github.io/
├── _papers/                        # PDF 보관 전용 (Jekyll 빌드 제외)
│   └── .gitkeep
├── scripts/
│   ├── pdf_to_post.py              # 메인 변환 스크립트
│   ├── requirements.txt            # 의존성
│   └── prompt_template.txt         # Claude 시스템 프롬프트
└── _posts/
    └── YYYY-MM-DD-{slug}.md        # 자동 생성 포스트
```

---

## 2. CLI 인터페이스 설계

```
사용법:
  python scripts/pdf_to_post.py <PDF_경로> [옵션]

인자:
  PDF_경로              _papers/ 폴더 안의 PDF 파일 경로 (필수)

옵션:
  --date YYYY-MM-DD     포스트 날짜 (기본값: 오늘)
  --slug SLUG           파일명 슬러그 (기본값: PDF 파일명에서 자동 생성)
  --no-push             로컬 저장만 하고 git push 하지 않음
  --dry-run             _posts/ 에 저장하지 않고 터미널에 출력만
  --model MODEL         Claude 모델 ID (기본값: claude-sonnet-4-6)

예시:
  python scripts/pdf_to_post.py _papers/selwyn-2025.pdf
  python scripts/pdf_to_post.py _papers/selwyn-2025.pdf --date 2025-11-26 --slug When-the-prompting-stops
  python scripts/pdf_to_post.py _papers/selwyn-2025.pdf --no-push
  python scripts/pdf_to_post.py _papers/selwyn-2025.pdf --dry-run
```

---

## 3. 모듈 설계 (`scripts/pdf_to_post.py`)

### 3.1 함수 목록

```python
# ─── 진입점 ───────────────────────────────────────────────
def main() -> None
    """CLI 파싱 → 파이프라인 순서 호출"""

# ─── PDF 처리 ─────────────────────────────────────────────
def extract_text_from_pdf(pdf_path: str) -> str
    """pdfplumber로 전체 텍스트 추출. 실패 시 RuntimeError."""

def truncate_text(text: str, max_chars: int = 80000) -> str
    """Claude 컨텍스트 한도 초과 방지용 앞부분 잘라내기"""

# ─── Claude API ───────────────────────────────────────────
def load_prompt_template(template_path: str) -> str
    """scripts/prompt_template.txt 읽기"""

def call_claude_api(paper_text: str, system_prompt: str, model: str) -> str
    """Anthropic SDK 호출 → 마크다운 문자열 반환"""

# ─── 포스트 생성 ──────────────────────────────────────────
def build_filename(date_str: str, slug: str) -> str
    """'YYYY-MM-DD-{slug}.md' 형식 반환"""

def slugify(text: str) -> str
    """PDF 파일명 → URL-safe 슬러그 (소문자, 하이픈)"""

def save_post(content: str, output_path: str) -> None
    """_posts/ 에 파일 저장"""

# ─── Git ──────────────────────────────────────────────────
def git_commit_and_push(filepath: str, commit_msg: str) -> None
    """git add → commit → push origin main"""
```

### 3.2 main() 실행 흐름

```
parse_args()
  │
  ├─ check ANTHROPIC_API_KEY 환경변수
  │    └─ 없으면 에러 출력 후 sys.exit(1)
  │
  ├─ extract_text_from_pdf(pdf_path)
  │    └─ 실패 → 에러 출력 후 sys.exit(1)
  │
  ├─ truncate_text(text)
  │
  ├─ load_prompt_template()
  │
  ├─ call_claude_api(text, prompt, model)
  │    └─ 실패 → 에러 출력 후 sys.exit(1)
  │
  ├─ build_filename(date, slug)
  │
  ├─ [--dry-run] → 터미널 출력 후 종료
  │
  ├─ save_post(content, _posts/filename)
  │
  └─ [--no-push 아닐 때] → git_commit_and_push()
```

---

## 4. Claude API 호출 설계

### 4.1 API 파라미터

```python
client.messages.create(
    model   = model,          # 기본값: "claude-sonnet-4-6"
    max_tokens = 8192,
    system  = system_prompt,  # prompt_template.txt 내용
    messages = [
        {
            "role": "user",
            "content": f"다음은 분석할 연구 논문 전문입니다:\n\n{paper_text}"
        }
    ]
)
```

### 4.2 `scripts/prompt_template.txt` 전체 내용

```
당신은 AI 교육 연구 논문을 한국어로 리뷰하는 교육공학 전문가입니다.
주어진 논문 전문을 읽고, 아래 규칙에 따라 Jekyll 블로그 포스트용 마크다운을 작성하세요.

[출력 규칙]
1. 응답은 오직 마크다운 텍스트만 출력합니다. 다른 설명이나 앞뒤 인사말을 절대 추가하지 마세요.
2. 첫 줄은 반드시 아래 YAML front matter로 시작합니다 (--- 포함):

---
title: "{논문 핵심 내용을 담은 한국어 제목 (원제 직역 금지, 의역 필수)}"
date: {오늘날짜 YYYY-MM-DD} 09:00:00 +0900
categories: [{주제1}, {주제2}]
tags: [{태그1}, {태그2}, {태그3}]
---

3. front matter 바로 다음은 아래 형식을 정확히 따릅니다:

# {front matter의 title과 동일한 제목}

> "{논문 전체를 관통하는 핵심 인사이트를 단 한 문장으로 요약}"

{논문의 핵심 주장과 의의를 2~3문장으로 요약. **볼드 강조** 적극 활용.}

---

##  1. 연구의 목적 및 방법

### 연구의 목적
{연구 목적 서술. 단순 번역이 아닌 "왜 이 연구가 중요한가"를 중심으로.}

### 연구 방법
{연구 방법을 * 불릿 리스트로 정리. 대상, 기간, 방법론, 분석 관점 포함.}

---

##  2. 주요 발견: '{이 섹션의 핵심 주제}'

### (1) {소제목}
{내용. **볼드 강조** 활용. 중요 개념은 굵게.}

### (2) {소제목}
{내용.}

(발견이 3개 이상이면 (3)도 추가)

---

##  3. 결론 및 시사점: '{이 섹션의 핵심 주제}'

### (1) {소제목}
{내용.}

### (2) {소제목}
{내용.}

### (3) {소제목 - 있으면 추가}
{내용.}

---

##  4. 리뷰어의 ADD(+) One: 교육 정책 및 연수 제언

이 섹션은 논문에 없는 내용입니다. 당신이 교육공학 전문가로서 추가하는 실용적 제언입니다.

### (1) {제언 소제목}
{논문의 발견을 교육 현장에 적용하기 위한 구체적인 제언.}

### (2) {제언 소제목}
{연수 프로그램, 정책, 플랫폼 등 실천 가능한 제안.}

---

##  5. 추가 탐구 질문

이 논문을 읽은 후 더 깊이 탐구할 만한 후속 연구 질문 3개를 작성합니다.

* **{키워드}:** {질문 내용}
* **{키워드}:** {질문 내용}
* **{키워드}:** {질문 내용}

---

_**출처:** {APA 7판 형식으로 논문의 저자, 연도, 제목, 저널명, 권(호), 페이지, DOI 기재}_

[출력 규칙 상세]
- categories: AI 교육 관련이면 [AI, 교육] / 일반 기술이면 [AI, 기술] 등 2개
- tags: 논문의 핵심 개념어 3~5개, 한국어 (예: [자기조절학습, AI챗봇, 교육설계])
- **볼드** 강조: 섹션마다 핵심 개념이나 중요 수치를 볼드로 표시
- 표(table): 논문에 비교 데이터가 있으면 마크다운 표로 정리
- 이미지 태그 삽입 금지: 이미지 경로는 직접 알 수 없으므로 이미지 삽입 코드를 절대 작성하지 마세요
```

---

## 5. `scripts/requirements.txt`

```
anthropic>=0.40.0
pdfplumber>=0.11.0
```

---

## 6. 에러 처리 전략

| 상황 | 처리 방법 | 종료 코드 |
|------|-----------|-----------|
| `ANTHROPIC_API_KEY` 미설정 | `[ERROR] ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.\nexport ANTHROPIC_API_KEY=sk-...` 출력 | `sys.exit(1)` |
| PDF 파일 없음 | `[ERROR] 파일을 찾을 수 없습니다: {path}` | `sys.exit(1)` |
| PDF 텍스트 추출 실패 | `[ERROR] PDF 텍스트 추출 실패 (스캔 PDF는 지원하지 않습니다)` | `sys.exit(1)` |
| Claude API 오류 | `[ERROR] Claude API 호출 실패: {error}` | `sys.exit(1)` |
| git push 실패 | `[WARN] git push 실패. 수동으로 push 하세요.\n→ git push origin main` | 경고만, 종료 안 함 |
| 슬러그 충돌 | 파일명에 `-{HHMMSS}` 타임스탬프 자동 추가 | 계속 실행 |

---

## 7. 슬러그 자동 생성 규칙

**입력:** `_papers/selwyn-2025-when-prompting-stops.pdf`

**변환 규칙:**
1. 확장자 제거: `selwyn-2025-when-prompting-stops`
2. 소문자 변환
3. 공백/특수문자 → `-` 치환
4. 연속 `-` 제거
5. 앞뒤 `-` 제거

**최종 슬러그:** `selwyn-2025-when-prompting-stops`
**파일명:** `2025-11-26-selwyn-2025-when-prompting-stops.md`

---

## 8. `_config.yml` 수정 사항

```yaml
# 기존 exclude 목록에 추가
exclude:
  - _papers        # ← 추가
  - scripts        # ← 추가
  - "*.sublime-project"
  # ... (기존 항목 유지)
```

---

## 9. git 자동화 설계

```python
def git_commit_and_push(filepath: str, commit_msg: str) -> None:
    commands = [
        ["git", "add", filepath],
        ["git", "commit", "-m", commit_msg],
        ["git", "push", "origin", "main"],
    ]
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            # push 실패는 경고만 출력, 나머지는 예외
            if "push" in cmd:
                print(f"[WARN] git push 실패. 수동으로 push 하세요.")
                print(f"→ git push origin main")
            else:
                raise RuntimeError(f"git 명령 실패: {' '.join(cmd)}\n{result.stderr}")
```

**커밋 메시지 형식:**
```
Add: {포스트 제목의 앞 50자}

Auto-generated by pdf_to_post.py
Source: {PDF 파일명}
```

---

## 10. 구현 순서 (Do 단계 참고용)

1. `_papers/` 폴더 + `.gitkeep` 생성
2. `_config.yml` exclude에 `_papers`, `scripts` 추가
3. `scripts/requirements.txt` 작성
4. `scripts/prompt_template.txt` 작성
5. `scripts/pdf_to_post.py` 구현
   - argparse CLI
   - extract_text_from_pdf()
   - truncate_text()
   - load_prompt_template()
   - call_claude_api()
   - slugify() + build_filename()
   - save_post()
   - git_commit_and_push()
   - main() 통합
6. 실제 PDF로 `--dry-run` 테스트
7. `--no-push`로 파일 생성 확인
8. 최종 실사용 테스트 (push까지)
