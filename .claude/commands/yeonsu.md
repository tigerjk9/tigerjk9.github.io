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

**4단계 — HWPX 변환 (government 템플릿, Workflow A)**

생성된 `.md` 파일을 파싱해 HWPX로 변환합니다.
저장 위치: `_lectures/YYYY-MM-DD-slug.hwpx` (`_lectures/` 폴더가 없으면 생성)

### 마크다운 → HWPX 매핑

| 마크다운 요소 | HWPX 변환 |
|-------------|-----------|
| `title:` (front matter) | `make_cover_page(title)` + `make_cover_banner(title)` |
| `## N. 챕터 제목` | `make_section_bar(N, 챕터 제목)` |
| 에피그래프 `> ` (챕터 상단 첫 인용) | `make_body_para('"', 내용)` |
| `**교실 이야기**` 아래 단락 | `make_body_para("◇", 내용)` |
| 일반 본문 텍스트 단락 | `make_body_para("▶", 내용)` |
| `**토의 활동**` 아래 `> ` 블록 | `make_body_para("Q.", 질문)` |
| `**핵심 정리**` 아래 `> ` 블록 | `make_body_para("■", 정리)` |
| `## 참고문헌` 아래 `- ` 항목 | `make_body_para("•", 참고문헌)` |

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
MD_PATH = BLOG_ROOT / "_posts/YYYY-MM-DD-slug.md"
OUTPUT  = BLOG_ROOT / "_lectures/YYYY-MM-DD-slug.hwpx"
# ─────────────────────────────────────────────────

OUTPUT.parent.mkdir(exist_ok=True)

# 1. 마크다운 파싱
text = MD_PATH.read_text(encoding="utf-8")

fm_m = re.search(r'^---\n(.+?)\n---', text, re.DOTALL)
fm   = fm_m.group(1) if fm_m else ""
title_m = re.search(r'title:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
date_m  = re.search(r'date:\s*(\d{4})-(\d{2})-(\d{2})', fm)
title   = title_m.group(1).strip() if title_m else "연수 교재"
date_display = f"{date_m.group(1)}. {int(date_m.group(2))}. {int(date_m.group(3))}." if date_m else ""

chapters = []
for block in re.split(r'(?=^## \d+\.)', text, flags=re.MULTILINE):
    m = re.match(r'^## (\d+)\. (.+)', block)
    if not m:
        continue
    num, stitle = m.group(1), m.group(2).strip()

    # 에피그래프: 챕터 상단의 첫 번째 blockquote (**교실 이야기** 이전)
    before_story = block.split('**교실 이야기**')[0] if '**교실 이야기**' in block else block
    epigraph_m = re.search(r'^> (.+)', before_story, re.MULTILINE)
    epigraph = re.sub(r'\*', '', epigraph_m.group(1)).strip().strip('"') if epigraph_m else ""

    # 교실 이야기 단락
    story_m = re.search(r'\*\*교실 이야기\*\*\n\n((?:.+\n?)+?)(?=\n\n\*\*|\Z)', block, re.MULTILINE)
    story_paras = [p.strip() for p in re.split(r'\n{2,}', story_m.group(1)) if p.strip()] if story_m else []

    # 본문 텍스트 단락 (특수 섹션 제거 후 남은 텍스트)
    clean = block
    clean = re.sub(r'\*\*교실 이야기\*\*\n\n(?:.+\n?)+?(?=\n\n\*\*|\Z)', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'\*\*토의 활동\*\*[^\n]*\n(?:^> ?.+\n?)+', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'\*\*핵심 정리\*\*[^\n]*\n(?:^> ?.+\n?)+', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^> .+\n?', '', clean, flags=re.MULTILINE)
    clean = re.sub(r'^## \d+\. .+\n?', '', clean, flags=re.MULTILINE)
    body_paras = [p.strip() for p in re.split(r'\n{2,}', clean)
                  if p.strip() and not p.strip().startswith('**') and not p.strip().startswith('-')]

    # 토의 활동
    q_m = re.search(r'\*\*토의 활동\*\*[^\n]*\n((?:^> ?.+\n?)+)', block, re.MULTILINE)
    question = "\n".join(
        re.sub(r'^> ?', '', l) for l in q_m.group(1).splitlines()
    ).strip() if q_m else ""

    # 핵심 정리
    summary_m = re.search(r'\*\*핵심 정리\*\*[^\n]*\n((?:^> ?.+\n?)+)', block, re.MULTILINE)
    summary = "\n".join(
        re.sub(r'^> ?', '', l) for l in summary_m.group(1).splitlines()
    ).strip() if summary_m else ""

    chapters.append((num, stitle, epigraph, story_paras, body_paras, question, summary))

# 참고문헌 파싱
ref_m = re.search(r'^## 참고문헌\n((?:.+\n?)+)', text, re.MULTILINE)
references = re.findall(r'^- (.+)', ref_m.group(1), re.MULTILINE) if ref_m else []

print(f"챕터 {len(chapters)}개 파싱 완료")

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
for num, stitle, epigraph, story_paras, body_paras, question, summary in chapters:
    parts.append(make_section_bar(num, stitle))
    if epigraph:
        parts.append(make_body_para('"', epigraph))
    for s in story_paras:
        parts.append(make_body_para("◇", s))
    for p in body_paras:
        parts.append(make_body_para("▶", p))
    if question:
        parts.append(make_body_para("Q.", question))
    if summary:
        parts.append(make_body_para("■", summary))
    parts.append(make_empty_line())

if references:
    parts.append(make_section_bar("ref", "참고문헌"))
    for ref in references:
        parts.append(make_body_para("•", ref))
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
5. 강의 시간에 맞는 챕터 수 자동 계산 (45분/챕터 기준)
6. Gemini로 교원 연수 교재 생성 (수준·관련 포스트 반영)
7. `_posts/YYYY-MM-DD-slug.md` 저장 후 git push
8. 생성된 `.md`를 파싱해 HWPX 변환 → `_lectures/YYYY-MM-DD-slug.hwpx` 저장

## 출력 파일

| 파일 | 위치 | 용도 |
|------|------|------|
| `.md` | `_posts/` | 블로그 포스트 (Jekyll) |
| `.hwpx` | `_lectures/` | 연수 교재 문서 (한컴오피스) |

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
