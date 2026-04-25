# /lecture-script — 다양한 입력 → 교사 연수용 연수 자료

이 스킬은 유저 레벨 스킬이므로 어디서든 호출 가능하다.
모든 작업의 대상은 아래 블로그 프로젝트이다:

```
BLOG_ROOT = "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
```

## 사용법

```
/lecture-script <입력> [옵션]
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

**3단계 — 마크다운 연수 자료 생성**
답변을 확인한 뒤 아래 명령어를 실행하세요:

```bash
cd "I:/내 드라이브/Github Desktop/tigerjk9.github.io"
python scripts/lecture_script.py $ARGUMENTS --duration <분> --level <초급|중급>
```

스크립트가 완료되면 `_posts/YYYY-MM-DD-slug.md` 경로를 확인하세요.

**4단계 — HWPX 변환 (government 템플릿, Workflow A)**

**템플릿 선택 이유**: 섹션 수(10~24개)가 유동적이라 동적 루프 생성이 필요 → government Workflow A 채택.
컬러 섹션 바가 섹션마다 붙어 읽는 중 즉시 위치 파악 가능. `hwpx_helpers.py`가 XML 생성을 대신해 토큰 절약.

생성된 `.md` 파일을 파싱해 HWPX로 변환합니다.
저장 위치: `_lectures/YYYY-MM-DD-slug.hwpx` (`_lectures/` 폴더가 없으면 생성)

### 마크다운 → HWPX 매핑

| 마크다운 요소 | HWPX 변환 |
|-------------|-----------|
| `title:` (front matter) | `make_cover_page(title)` + `make_cover_banner(title)` |
| `## N. 섹션 제목` | `make_section_bar(N, 섹션 제목)` |
| `**핵심 개념**` 아래 `- ` 불릿 | `make_body_para("•", 내용)` |
| 일반 본문 텍스트 단락 | `make_body_para("▶", 내용)` |
| `**현장 적용**` 아래 `- ` 불릿 | `make_body_para("·", 내용)` |
| `**생각해보기**` 아래 `> ` 블록 | `make_body_para("Q.", 질문)` |

### HWPX 빌드 스크립트

아래 코드를 실제 경로로 채워 `C:/Users/windo/AppData/Local/Temp/build_lecture_hwpx.py`로 저장 후 실행합니다.

```python
import subprocess, sys, re
from pathlib import Path

sys.path.insert(0, "C:/Users/windo/.claude/skills/hwpx/scripts")
from hwpx_helpers import *

BLOG_ROOT = Path("I:/내 드라이브/Github Desktop/tigerjk9.github.io")
SKILL_DIR = Path("C:/Users/windo/.claude/skills/hwpx")
REF_HWPX  = SKILL_DIR / "assets/government-reference.hwpx"

# ── 실제 경로로 교체 ──────────────────────────────
MD_PATH = BLOG_ROOT / "_posts/YYYY-MM-DD-slug.md"   # 3단계에서 생성된 파일
OUTPUT  = BLOG_ROOT / "_lectures/YYYY-MM-DD-slug.hwpx"
# ─────────────────────────────────────────────────

OUTPUT.parent.mkdir(exist_ok=True)

# 1. 마크다운 파싱
text = MD_PATH.read_text(encoding="utf-8")

fm_m = re.search(r'^---\n(.+?)\n---', text, re.DOTALL)
fm   = fm_m.group(1) if fm_m else ""
title_m = re.search(r'title:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
date_m  = re.search(r'date:\s*(\d{4})-(\d{2})-(\d{2})', fm)
title   = title_m.group(1).strip() if title_m else "연수 자료"
date_display = f"{date_m.group(1)}. {int(date_m.group(2))}. {int(date_m.group(3))}." if date_m else ""

sections = []
for block in re.split(r'(?=^## \d+\.)', text, flags=re.MULTILINE):
    m = re.match(r'^## (\d+)\. (.+)', block)
    if not m:
        continue
    num, stitle = m.group(1), m.group(2).strip()

    # 핵심 개념 bullets
    concept_m = re.search(r'\*\*핵심 개념\*\*\n((?:^- .+\n?)+)', block, re.MULTILINE)
    key_concepts = re.findall(r'^- (.+)', concept_m.group(1), re.MULTILINE) if concept_m else []

    # 본문 텍스트 단락 (특수 섹션 제거 후 남은 텍스트)
    clean = block
    clean = re.sub(r'\*\*핵심 개념\*\*\n(?:^- .+\n?)+', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'\*\*현장 적용\*\*\n(?:^- .+\n?)+', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'\*\*생각해보기\*\*[^\n]*\n(?:^> ?.+\n?)+', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^## \d+\. .+\n?', '', clean, flags=re.MULTILINE)
    body_paras = [p.strip() for p in re.split(r'\n{2,}', clean)
                  if p.strip() and not p.strip().startswith('-') and not p.strip().startswith('>')]

    # 현장 적용 bullets
    apply_m = re.search(r'\*\*현장 적용\*\*\n((?:^- .+\n?)+)', block, re.MULTILINE)
    apply_bullets = re.findall(r'^- (.+)', apply_m.group(1), re.MULTILINE) if apply_m else []

    # 생각해보기
    q_m = re.search(r'\*\*생각해보기\*\*[^\n]*\n((?:^> ?.+\n?)+)', block, re.MULTILINE)
    question = "\n".join(
        re.sub(r'^> ?', '', l) for l in q_m.group(1).splitlines()
    ).strip() if q_m else ""

    sections.append((num, stitle, key_concepts, body_paras, apply_bullets, question))

print(f"섹션 {len(sections)}개 파싱 완료")

# 2. secPr 추출
secpr, colpr = extract_secpr_and_colpr(REF_HWPX)

# 3. section0.xml 조립
parts = [
    '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>',
    f'<hs:sec {NS_DECL}>',
    make_first_para(secpr, colpr),
    *make_cover_page(title, subtitle="교원 연수", date=date_display),
    make_cover_banner(title),
    make_empty_line(),
]
for num, stitle, key_concepts, body_paras, apply_bullets, question in sections:
    parts.append(make_section_bar(num, stitle))
    for c in key_concepts:
        parts.append(make_body_para("•", c))
    for p in body_paras:
        parts.append(make_body_para("▶", p))
    for a in apply_bullets:
        parts.append(make_body_para("·", a))
    if question:
        parts.append(make_body_para("Q.", question))
    parts.append(make_empty_line())
parts.append('</hs:sec>')

# 4. 빌드
section_xml = Path("C:/Users/windo/AppData/Local/Temp/lecture_section0.xml")
section_xml.write_text("\n".join(parts), encoding="utf-8")
subprocess.run([
    "python", str(SKILL_DIR / "scripts/build_hwpx.py"),
    "--header",  str(SKILL_DIR / "templates/government/header.xml"),
    "--section", str(section_xml),
    "--title",   title,
    "--output",  str(OUTPUT),
], check=True)
subprocess.run(["python", str(SKILL_DIR / "scripts/fix_namespaces.py"), str(OUTPUT)], check=True)
subprocess.run(["python", str(SKILL_DIR / "scripts/validate.py"), str(OUTPUT)])

print(f"[OK] HWPX saved: {OUTPUT}")
```

> ⚠️ `fix_namespaces.py`는 반드시 실행. 빠뜨리면 한글에서 빈 페이지로 표시됨.

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
5. 강의 시간에 맞는 섹션 수 자동 계산
6. Gemini로 교사 연수용 연수 자료 생성 (수준·관련 포스트 반영)
7. `_posts/YYYY-MM-DD-slug.md` 저장 후 git push
8. 생성된 `.md`를 파싱해 HWPX 변환 → `_lectures/YYYY-MM-DD-slug.hwpx` 저장

## 출력 파일

| 파일 | 위치 | 용도 |
|------|------|------|
| `.md` | `_posts/` | 블로그 포스트 (Jekyll) |
| `.hwpx` | `_lectures/` | 연수 자료 문서 (한컴오피스) |

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
