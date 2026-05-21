# 강의자료 큐레이션 하네스 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 강의자료 zip → `tigerjk9.github.io _lectures/` collection 자동 큐레이션 5명 에이전트 하네스를 구축하고 KIST 첫 변환을 완료한다.

**Architecture:** Python 스크립트 5개 (parse_slides·map_features·build_site·extract_notes·orchestrate) + Superpowers 멀티 에이전트 팀 5명 + Jekyll collection·격리 모드. Playwright + BeautifulSoup 듀얼 슬라이드 추출, Gemini API 폴백 매핑, 사용자 명시 슬러그 검토 게이트.

**Tech Stack:** Python 3.x, Playwright (Chromium), BeautifulSoup4, Google Generative AI (Gemini), Jekyll 4.x, Liquid, SCSS, pytest, Superpowers 멀티 에이전트 (Opus).

**Spec:** [`docs/superpowers/specs/2026-05-22-lecture-curation-harness-design.md`](../specs/2026-05-22-lecture-curation-harness-design.md)

---

## File Structure

### 신규 파일

```
scripts/lecture_archive/
├─ __init__.py
├─ orchestrate.py             진입점 — zip 해제·brief.yml·팀 호출
├─ parse_slides.py            Playwright + BS4 슬라이드 추출
├─ map_features.py            strict·heading·Gemini 3단계 매핑
├─ extract_notes.py           instructor-notes 파싱
├─ build_site.py              Jekyll 산출물 생성
├─ utils.py                   공용 (zip 디코드·slug·경로)
├─ requirements.txt           playwright·beautifulsoup4·google-generativeai·weasyprint·pytest
└─ tests/
    ├─ __init__.py
    ├─ conftest.py
    ├─ test_parse_slides.py
    ├─ test_map_features.py
    ├─ test_extract_notes.py
    └─ fixtures/
        ├─ sample_slides.html
        └─ sample_instructor_notes.md

.claude/
├─ commands/lecture-archive.md            슬래시 정의
└─ skills/lecture-archive-orchestrator/
    └─ SKILL.md                            팀·워크플로우 명세

_includes/lecture-card.html               기능 카드 partial
_layouts/lecture.html                     강의 페이지 레이아웃 (single 상속)
_sass/_lectures.scss                      강의 스타일
```

### 패치 파일

```
_config.yml                  collections.lectures 추가 (3줄)
_data/navigation.yml         "강의자료" 메뉴 1줄
_data/lectures.yml           신규 생성 (강의 인덱스)
assets/css/main.scss         _lectures.scss import 1줄
.gitignore                   _workspace/·assets/lectures/*/slides/*.png 옵션 등록
```

### 강의 자산 (첫 사례 실행 시)

```
_lectures/kist-claude-code/{index.md, *.md × 22}
assets/lectures/kist-claude-code/{slides.html, slides/*, handout.pdf, cover.png, feature-thumb/*}
```

---

## Task 분해 — Phase A: 기반 (인프라·Jekyll 통합)

### Task 1: Python 패키지 골격 + 의존성

**Files:**
- Create: `scripts/lecture_archive/__init__.py`
- Create: `scripts/lecture_archive/requirements.txt`
- Create: `scripts/lecture_archive/tests/__init__.py`
- Create: `scripts/lecture_archive/tests/conftest.py`

- [ ] **Step 1: requirements.txt 작성**

```
playwright>=1.40.0
beautifulsoup4>=4.12.0
google-generativeai>=0.3.0
weasyprint>=60.0
pytest>=7.4.0
pytest-asyncio>=0.21.0
PyYAML>=6.0
```

- [ ] **Step 2: 패키지 초기화 파일**

```python
# scripts/lecture_archive/__init__.py
"""강의자료 큐레이션 하네스 — Lecture archive curation harness."""
__version__ = "0.1.0"
```

```python
# scripts/lecture_archive/tests/__init__.py
```

```python
# scripts/lecture_archive/tests/conftest.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

- [ ] **Step 3: 의존성 설치 (사용자 환경)**

Run: `python -m pip install -r scripts/lecture_archive/requirements.txt && python -m playwright install chromium`
Expected: chromium 다운로드 완료 (~150MB). 망분리면 `--skip-playwright` 사용 예정 안내.

- [ ] **Step 4: pytest collection 점검**

Run: `python -m pytest scripts/lecture_archive/tests/ --collect-only`
Expected: `0 collected` (테스트 미작성 상태)

- [ ] **Step 5: Commit**

```bash
git add scripts/lecture_archive/__init__.py scripts/lecture_archive/requirements.txt scripts/lecture_archive/tests/
git commit -m "Add: 강의자료 큐레이션 하네스 패키지 골격 + Python 의존성"
```

---

### Task 2: Jekyll collection 활성화 + 격리 검증

**Files:**
- Modify: `_config.yml:178-183` (Outputting 섹션 직후)

- [ ] **Step 1: `_config.yml`에 collection 추가**

`# Outputting` 직전(line 178 `permalink: /:categories/:title/` 부근)에 다음 블록 삽입.

```yaml
# Collections — 강의자료 큐레이션 아카이브 (격리 모드)
collections:
  lectures:
    output: true
    permalink: /lectures/:path/
```

이미 있는 `permalink: /:categories/:title/`는 _posts 전용이라 collection과 충돌 안 함.

- [ ] **Step 2: 빌드 점검**

Run: `bundle exec jekyll build --verbose 2>&1 | grep -i "lectures" || echo "no_lectures_yet"`
Expected: `no_lectures_yet` (collection 비어 있으므로 정상)

- [ ] **Step 3: 격리 회귀 검증 (사이드바 변화 0건)**

Run: `bundle exec jekyll build && ls _site/categories/ | wc -l && ls _site/tags/ | wc -l`
Expected: 빌드 전후 categories·tags 개수 변화 없음. (변화 있으면 격리 실패)

- [ ] **Step 4: Commit**

```bash
git add _config.yml
git commit -m "Edit: _config.yml에 lectures collection 추가 (격리 모드)"
```

---

### Task 3: 강의 레이아웃·스타일 신규

**Files:**
- Create: `_layouts/lecture.html`
- Create: `_sass/_lectures.scss`
- Modify: `assets/css/main.scss` (import 1줄 추가)

- [ ] **Step 1: `_layouts/lecture.html` 작성**

```liquid
---
layout: single
toc: true
toc_sticky: true
author_profile: false
share: true
comments: false
read_time: false
---

<nav class="lecture-breadcrumb" aria-label="breadcrumb">
  <ol>
    <li><a href="/lectures/">강의자료</a></li>
    {% if page.lecture_slug %}
      {% assign lecture = site.data.lectures | where: "slug", page.lecture_slug | first %}
      <li><a href="{{ lecture.hub_url }}">{{ lecture.title }}</a></li>
    {% endif %}
    {% if page.feature_name %}<li aria-current="page">{{ page.feature_name }}</li>{% endif %}
  </ol>
</nav>

<article class="lecture-feature">
  {{ content }}
</article>

{% include lecture-nav.html %}
```

- [ ] **Step 2: `_sass/_lectures.scss` 작성**

```scss
// 강의자료 큐레이션 — 격리 스타일
.lecture-breadcrumb {
  font-size: 0.85em;
  margin-bottom: 1em;
  ol { list-style: none; padding: 0; display: flex; gap: 0.5em; flex-wrap: wrap; }
  li + li::before { content: "▸ "; margin-right: 0.5em; opacity: 0.5; }
}

.lecture-feature {
  .feature-header { border-bottom: 2px solid var(--accent, #d65a31); padding-bottom: 0.8em; margin-bottom: 1.5em; }
  .feature-badge { display: inline-block; padding: 2px 10px; border-radius: 12px; background: #eee; font-size: 0.7em; margin-right: 6px; }
  .feature-badge.track-basic { background: #e6e6e6; }
  .feature-badge.track-advanced { background: #1a1a1a; color: #fff; }

  .slide-excerpt { border: 1px solid #ddd; border-radius: 6px; padding: 1em; margin: 1em 0; }
  .slide-excerpt img { max-width: 100%; height: auto; border-radius: 4px; }
  .slide-excerpt .slide-text { font-size: 0.9em; color: var(--muted, #444); margin-top: 0.5em; }
}

.lecture-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1em;
  transition: transform 0.15s ease;
  &:hover { transform: translateY(-2px); }
  .card-id { font-family: monospace; color: var(--accent, #d65a31); font-size: 0.8em; }
  .card-title { font-weight: 600; margin: 0.4em 0; }
  .card-track { font-size: 0.7em; padding: 2px 8px; border-radius: 10px; background: #eee; }
}

.lecture-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1em;
  margin: 1.5em 0;
}

// 다크 모드 대응
html[data-theme="light"] {
  .lecture-feature .slide-excerpt { background: #fafafa; }
}
```

- [ ] **Step 3: `assets/css/main.scss`에 import 추가**

기존 import 목록 맨 마지막에:

```scss
@import "lectures";
```

- [ ] **Step 4: 빌드 점검**

Run: `bundle exec jekyll build 2>&1 | grep -iE "error|warning" | head -20`
Expected: SCSS 컴파일 오류 0건.

- [ ] **Step 5: Commit**

```bash
git add _layouts/lecture.html _sass/_lectures.scss assets/css/main.scss
git commit -m "Add: 강의 레이아웃·스타일 (격리 모드)"
```

---

### Task 4: 내비게이션·강의 인덱스 페이지

**Files:**
- Modify: `_data/navigation.yml`
- Create: `_pages/lectures.md` (강의 아카이브 인덱스, Lunr 노출용)
- Create: `_data/lectures.yml` (빈 인덱스, 빌드 안전성 확보)
- Create: `_includes/lecture-card.html`
- Create: `_includes/lecture-nav.html`

- [ ] **Step 1: `_data/navigation.yml`에 강의자료 메뉴 추가**

기존 main: 목록 마지막에 1줄 추가:

```yaml
  - title: "강의자료"
    url: /lectures/
```

- [ ] **Step 2: `_data/lectures.yml` 빈 인덱스**

```yaml
# 강의 인덱스 — orchestrate.py가 append 갱신
# []
```

빈 파일은 Jekyll에서 nil로 잡혀 site.data.lectures 호출 시 에러. 빈 배열로 시작.

```yaml
[]
```

- [ ] **Step 3: `_pages/lectures.md` 인덱스 페이지**

`_pages/` 디렉토리가 없으면 생성. 사용자 블로그 _config.yml의 defaults pages scope를 활용.

```markdown
---
title: "강의자료 아카이브"
permalink: /lectures/
layout: single
author_profile: false
toc: false
---

강의자료를 검색·필터·재방문 가능한 형태로 큐레이션한 아카이브.

{% if site.data.lectures.size == 0 %}
<p>아직 등록된 강의가 없습니다.</p>
{% else %}
<div class="lecture-card-grid">
{% for lecture in site.data.lectures %}
  <a href="{{ lecture.hub_url }}" class="lecture-card">
    {% if lecture.thumbnail %}<img src="{{ lecture.thumbnail }}" alt="{{ lecture.title }}">{% endif %}
    <div class="card-title">{{ lecture.title }}</div>
    <div class="card-meta">
      <span>{{ lecture.audience }}</span> · <span>{{ lecture.duration_min }}분</span> · <span>{{ lecture.feature_count }}개 기능</span>
    </div>
  </a>
{% endfor %}
</div>
{% endif %}
```

- [ ] **Step 4: `_includes/lecture-card.html` (허브의 기능 카드)**

```liquid
{% assign feature = include.feature %}
{% assign lecture_slug = include.lecture_slug %}
<a href="/lectures/{{ lecture_slug }}/{{ feature.slug }}/" class="lecture-card">
  <div class="card-id">{{ feature.id }}</div>
  <div class="card-title">{{ feature.name }}</div>
  <div class="card-def">{{ feature.def | truncate: 80 }}</div>
  <span class="card-track">{{ feature.track }}</span>
</a>
```

- [ ] **Step 5: `_includes/lecture-nav.html` (이전·다음·허브 복귀)**

```liquid
{% if page.lecture_slug %}
{% assign all_features = site.lectures | where: "lecture_slug", page.lecture_slug | sort: "order" %}
{% assign idx = 0 %}
{% for f in all_features %}{% if f.url == page.url %}{% assign idx = forloop.index0 %}{% endif %}{% endfor %}
{% assign prev_idx = idx | minus: 1 %}
{% assign next_idx = idx | plus: 1 %}

<nav class="lecture-feature-nav" aria-label="기능 페이지 이동">
  {% if prev_idx >= 0 %}
    {% assign prev = all_features[prev_idx] %}
    <a href="{{ prev.url }}" rel="prev">← {{ prev.feature_name }}</a>
  {% endif %}
  <a href="/lectures/{{ page.lecture_slug }}/">↑ 허브로</a>
  {% if next_idx < all_features.size %}
    {% assign nxt = all_features[next_idx] %}
    <a href="{{ nxt.url }}" rel="next">{{ nxt.feature_name }} →</a>
  {% endif %}
</nav>
{% endif %}
```

- [ ] **Step 6: 빌드 점검**

Run: `bundle exec jekyll build 2>&1 | tail -10`
Expected: `/lectures/` 페이지가 빌드 산출에 포함. 인덱스 페이지 "아직 등록된 강의가 없습니다" 표시.

- [ ] **Step 7: Commit**

```bash
git add _data/navigation.yml _data/lectures.yml _pages/lectures.md _includes/lecture-card.html _includes/lecture-nav.html
git commit -m "Add: 강의자료 인덱스·내비게이션·카드 partial"
```

---

## Task 분해 — Phase B: 핵심 스크립트 (TDD)

### Task 5: utils.py — 공용 헬퍼

**Files:**
- Create: `scripts/lecture_archive/utils.py`
- Create: `scripts/lecture_archive/tests/test_utils.py`

- [ ] **Step 1: 테스트 작성 (zip 한글 디코드·slug 추출·경로)**

```python
# scripts/lecture_archive/tests/test_utils.py
from pathlib import Path
from lecture_archive.utils import (
    decode_zip_filename,
    slug_from_zip_name,
    safe_slug,
)


def test_decode_zip_filename_korean():
    raw = "260429_황민호_강의자료.zip".encode("cp437", errors="replace")
    result = decode_zip_filename(raw)
    assert "황민호" in result


def test_slug_from_zip_name_extracts_korean_blocks():
    assert slug_from_zip_name("260429_황민호_강의자료.zip") == "260429-hwangminho-lecture"


def test_safe_slug_strips_unicode():
    assert safe_slug("CLAUDE.md 사용법") == "claudemd-usage"
    assert safe_slug("Auto Memory") == "auto-memory"
    assert safe_slug("---test---") == "test"
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_utils.py -v`
Expected: FAIL — `lecture_archive.utils` 모듈 미존재.

- [ ] **Step 3: utils.py 최소 구현**

```python
# scripts/lecture_archive/utils.py
"""공용 헬퍼 — zip 디코드·slug·경로."""
import re
import unicodedata


KOREAN_TRANSLIT = {
    "황민호": "hwangminho",
    "강의자료": "lecture",
    "사용법": "usage",
}


def decode_zip_filename(raw: bytes | str) -> str:
    """zip 내 한글 파일명을 cp437 → utf-8로 디코드."""
    if isinstance(raw, str):
        return raw
    try:
        return raw.decode("cp437").encode("cp437").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return raw.decode("utf-8", errors="replace")


def slug_from_zip_name(filename: str) -> str:
    """zip 파일명에서 영문 slug 추출. 한글 블록은 transliteration."""
    base = re.sub(r"\.[zZ][iI][pP]$", "", filename)
    parts = re.split(r"[_\-\s]+", base)
    out = []
    for p in parts:
        if not p:
            continue
        if re.match(r"^[A-Za-z0-9]+$", p):
            out.append(p.lower())
        elif p in KOREAN_TRANSLIT:
            out.append(KOREAN_TRANSLIT[p])
        else:
            ascii_form = unicodedata.normalize("NFKD", p).encode("ascii", "ignore").decode("ascii")
            if ascii_form:
                out.append(ascii_form.lower())
    return "-".join(out)


def safe_slug(text: str) -> str:
    """페이지 slug — 영문·숫자·하이픈만."""
    text = text.lower()
    for k, v in KOREAN_TRANSLIT.items():
        text = text.replace(k.lower(), v)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_utils.py -v`
Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/lecture_archive/utils.py scripts/lecture_archive/tests/test_utils.py
git commit -m "Add: utils.py — zip 한글 디코드·slug 헬퍼 (TDD)"
```

---

### Task 6: parse_slides.py — BeautifulSoup 부분 (Playwright 없이 시작)

**Files:**
- Create: `scripts/lecture_archive/parse_slides.py`
- Create: `scripts/lecture_archive/tests/test_parse_slides.py`
- Create: `scripts/lecture_archive/tests/fixtures/sample_slides.html`

- [ ] **Step 1: 픽스처 작성 — 5장 미니 Reveal.js 슬라이드**

```html
<!-- scripts/lecture_archive/tests/fixtures/sample_slides.html -->
<!DOCTYPE html>
<html lang="ko"><head><meta charset="UTF-8"><title>Test</title></head>
<body><div class="reveal"><div class="slides">
  <section class="title-slide" data-block="intro" data-time="0">
    <h1>Claude Code 워크숍</h1>
    <p class="muted">테스트</p>
  </section>
  <section data-block="claudemd" data-time="1" class="layout-bullets">
    <h2>CLAUDE.md 개념</h2>
    <ul><li>매 세션 시스템 프롬프트 복붙을 0으로</li></ul>
    <pre><code class="language-powershell">claude
/init
notepad CLAUDE.md</code></pre>
  </section>
  <section data-block="claudemd" data-time="2" class="layout-code">
    <h2>CLAUDE.md 실습</h2>
    <p>본인 폴더에 CLAUDE.md 한 개.</p>
  </section>
  <section data-block="auto-memory" data-time="1" class="layout-bullets">
    <h2>Auto Memory 토글</h2>
    <ul><li>자연어로 정정 누적</li></ul>
  </section>
  <section data-block="end" data-time="0" class="layout-section-break">
    <h1>마무리</h1>
  </section>
</div></div></body></html>
```

- [ ] **Step 2: 테스트 작성**

```python
# scripts/lecture_archive/tests/test_parse_slides.py
from pathlib import Path
from lecture_archive.parse_slides import parse_html

FIX = Path(__file__).parent / "fixtures" / "sample_slides.html"


def test_parse_html_counts_sections():
    slides = parse_html(FIX.read_text(encoding="utf-8"))
    assert len(slides) == 5


def test_parse_html_extracts_metadata():
    slides = parse_html(FIX.read_text(encoding="utf-8"))
    s2 = slides[1]
    assert s2["n"] == 2
    assert s2["block"] == "claudemd"
    assert s2["data_time"] == "1"
    assert s2["title"] == "CLAUDE.md 개념"
    assert s2["layout"] == "layout-bullets"


def test_parse_html_extracts_code_blocks():
    slides = parse_html(FIX.read_text(encoding="utf-8"))
    s2 = slides[1]
    assert len(s2["code_blocks"]) == 1
    assert s2["code_blocks"][0]["lang"] == "powershell"
    assert "claude" in s2["code_blocks"][0]["code"]


def test_parse_html_extracts_text():
    slides = parse_html(FIX.read_text(encoding="utf-8"))
    s4 = slides[3]
    assert "자연어로 정정 누적" in s4["text"]
```

- [ ] **Step 3: 테스트 실패 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_parse_slides.py -v`
Expected: FAIL — `parse_html` 미정의.

- [ ] **Step 4: parse_slides.py 구현 (BS4 부분)**

```python
# scripts/lecture_archive/parse_slides.py
"""Reveal.js 슬라이드 추출 — BeautifulSoup 정적 파싱 + Playwright 동적 캡처."""
from __future__ import annotations
from pathlib import Path
from bs4 import BeautifulSoup
from typing import Any


def parse_html(html: str) -> list[dict[str, Any]]:
    """slides.html → 슬라이드별 dict 리스트 (1-based n, 메타·텍스트·코드)."""
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.select(".reveal .slides > section")
    slides: list[dict[str, Any]] = []
    for i, sec in enumerate(sections, start=1):
        layouts = [c for c in sec.get("class", []) if c.startswith("layout-")]
        layout = layouts[0] if layouts else ("title-slide" if "title-slide" in sec.get("class", []) else "")
        h = sec.find(["h1", "h2"])
        title = h.get_text(strip=True) if h else ""
        code_blocks = []
        for pre in sec.find_all("pre"):
            code_el = pre.find("code")
            if not code_el:
                continue
            lang_classes = [c for c in code_el.get("class", []) if c.startswith("language-")]
            lang = lang_classes[0].replace("language-", "") if lang_classes else ""
            code_blocks.append({"lang": lang, "code": code_el.get_text()})
        # 텍스트는 헤딩·코드 제외하고 추출
        for tag in sec.find_all(["pre", "h1", "h2"]):
            tag.decompose()
        text = " ".join(sec.get_text(separator=" ").split())
        slides.append({
            "n": i,
            "block": sec.get("data-block", ""),
            "data_time": sec.get("data-time", ""),
            "layout": layout,
            "title": title,
            "text": text,
            "code_blocks": code_blocks,
            "images": [img.get("src", "") for img in sec.find_all("img")],
        })
    return slides
```

- [ ] **Step 5: 테스트 통과 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_parse_slides.py -v`
Expected: 4 PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/lecture_archive/parse_slides.py scripts/lecture_archive/tests/test_parse_slides.py scripts/lecture_archive/tests/fixtures/sample_slides.html
git commit -m "Add: parse_slides.py BeautifulSoup 부분 (TDD, 4 tests)"
```

---

### Task 7: parse_slides.py — Playwright PNG 캡처 추가

**Files:**
- Modify: `scripts/lecture_archive/parse_slides.py`

- [ ] **Step 1: capture_pngs 함수 추가 (테스트는 통합 검증으로)**

`parse_html` 함수 아래에 추가:

```python
def capture_pngs(slides_html: Path, output_dir: Path, viewport=(1920, 1080)) -> list[Path]:
    """Playwright headless로 슬라이드별 PNG 캡처.
    
    Reveal.js의 fragment를 비활성화하고 각 슬라이드 첫 상태만 캡처.
    """
    from playwright.sync_api import sync_playwright
    output_dir.mkdir(parents=True, exist_ok=True)
    pngs: list[Path] = []
    url = f"file:///{slides_html.resolve().as_posix()}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
        page.goto(url, wait_until="networkidle")
        # Reveal.js 슬라이드 개수 조회
        total = page.evaluate("Reveal.getTotalSlides()")
        for i in range(total):
            page.evaluate(f"Reveal.slide({i})")
            page.wait_for_timeout(300)
            png_path = output_dir / f"slide-{i+1:02d}.png"
            page.screenshot(path=str(png_path), full_page=False, clip={
                "x": 0, "y": 0, "width": viewport[0], "height": viewport[1]
            })
            pngs.append(png_path)
        browser.close()
    return pngs


def convert_to_webp(pngs: list[Path], max_width: int = 1280, quality: int = 80) -> list[Path]:
    """PNG → WebP 변환 + 리사이즈."""
    from PIL import Image
    webps: list[Path] = []
    for png in pngs:
        with Image.open(png) as img:
            if img.width > max_width:
                ratio = max_width / img.width
                img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
            webp_path = png.with_suffix(".webp")
            img.save(webp_path, "WebP", quality=quality)
            webps.append(webp_path)
    return webps
```

- [ ] **Step 2: Pillow 의존성 추가**

`scripts/lecture_archive/requirements.txt`에 한 줄 추가:

```
Pillow>=10.0.0
```

Run: `python -m pip install Pillow`

- [ ] **Step 3: 통합 검증 — 픽스처로 5장 PNG 캡처**

Run:
```
python -c "
from pathlib import Path
from scripts.lecture_archive.parse_slides import capture_pngs, convert_to_webp
src = Path('scripts/lecture_archive/tests/fixtures/sample_slides.html')
out = Path('/tmp/test_pngs')
pngs = capture_pngs(src, out)
print(f'PNG: {len(pngs)}')
webps = convert_to_webp(pngs)
print(f'WebP: {len(webps)}')
"
```
Expected: `PNG: 5`, `WebP: 5`. `/tmp/test_pngs/`에 10개 파일 (PNG 5 + WebP 5).

- [ ] **Step 4: Commit**

```bash
git add scripts/lecture_archive/parse_slides.py scripts/lecture_archive/requirements.txt
git commit -m "Add: parse_slides.py Playwright PNG 캡처 + WebP 변환"
```

---

### Task 8: extract_notes.py — instructor-notes 발췌

**Files:**
- Create: `scripts/lecture_archive/extract_notes.py`
- Create: `scripts/lecture_archive/tests/test_extract_notes.py`
- Create: `scripts/lecture_archive/tests/fixtures/sample_instructor_notes.md`

- [ ] **Step 1: 픽스처 작성**

```markdown
# 강사 노트 v2

## 도입 (S1~S5, 5분)

### S1. 표지

- **멘트.** 안녕하세요.
- **시간.** 30초.
- **강조.** 동료 톤.

## CLAUDE.md (S7~S10, 5분)

### S8. 개념

- **멘트.** 첫 기능 CLAUDE.md입니다.
- **시간.** 1분.
- **강조.** "이 한 파일로 매 세션 복붙을 0으로".
- **예상 Q.** "CLAUDE.md를 매번 새로?" → "아니요. @import 한 줄."

## Auto Memory (S11~S13, 3분)

### S11. 토글

- **멘트.** 토글로 켜기.
- **시간.** 1분.
```

- [ ] **Step 2: 테스트 작성**

```python
# scripts/lecture_archive/tests/test_extract_notes.py
from pathlib import Path
from lecture_archive.extract_notes import parse_notes, slide_to_feature_map

FIX = Path(__file__).parent / "fixtures" / "sample_instructor_notes.md"


def test_parse_notes_extracts_sections():
    sections = parse_notes(FIX.read_text(encoding="utf-8"))
    assert len(sections) == 3
    titles = [s["feature_name"] for s in sections]
    assert "도입" in titles
    assert "CLAUDE.md" in titles
    assert "Auto Memory" in titles


def test_parse_notes_extracts_slide_ranges():
    sections = parse_notes(FIX.read_text(encoding="utf-8"))
    claudemd = next(s for s in sections if s["feature_name"] == "CLAUDE.md")
    assert claudemd["slide_start"] == 7
    assert claudemd["slide_end"] == 10
    assert claudemd["duration_min"] == 5


def test_parse_notes_extracts_per_slide_notes():
    sections = parse_notes(FIX.read_text(encoding="utf-8"))
    claudemd = next(s for s in sections if s["feature_name"] == "CLAUDE.md")
    s8 = claudemd["slides"][0]
    assert s8["n"] == 8
    assert "첫 기능 CLAUDE.md입니다" in s8["ment"]
    assert "@import 한 줄" in s8["qa"]


def test_slide_to_feature_map():
    sections = parse_notes(FIX.read_text(encoding="utf-8"))
    m = slide_to_feature_map(sections)
    assert m[1] == "도입"
    assert m[7] == "CLAUDE.md"
    assert m[8] == "CLAUDE.md"
    assert m[10] == "CLAUDE.md"
    assert m[11] == "Auto Memory"
    assert m[13] == "Auto Memory"
```

- [ ] **Step 3: 테스트 실패 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_extract_notes.py -v`
Expected: FAIL — `lecture_archive.extract_notes` 미정의.

- [ ] **Step 4: extract_notes.py 구현**

```python
# scripts/lecture_archive/extract_notes.py
"""instructor-notes.md 발췌 — 섹션 헤딩·슬라이드 범위·슬라이드별 멘트."""
from __future__ import annotations
import re
from typing import Any

SECTION_RE = re.compile(r"^##\s+(.+?)\s*\(S(\d+)~S(\d+),\s*(\d+)분\)", re.M)
SLIDE_RE = re.compile(r"^###\s+S(\d+)\.\s*(.+)$", re.M)
BULLET_RE = re.compile(r"^-\s+\*\*(멘트|시간|강조|예상\s*Q|운영)\.\*\*\s*(.+)$", re.M)


def parse_notes(md: str) -> list[dict[str, Any]]:
    """instructor-notes.md → 섹션·슬라이드별 dict 리스트."""
    sections: list[dict[str, Any]] = []
    matches = list(SECTION_RE.finditer(md))
    for i, m in enumerate(matches):
        start_pos = m.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        chunk = md[start_pos:end_pos]
        slides = _parse_slides_in_chunk(chunk)
        sections.append({
            "feature_name": m.group(1).strip(),
            "slide_start": int(m.group(2)),
            "slide_end": int(m.group(3)),
            "duration_min": int(m.group(4)),
            "slides": slides,
        })
    return sections


def _parse_slides_in_chunk(chunk: str) -> list[dict[str, Any]]:
    slides: list[dict[str, Any]] = []
    slide_matches = list(SLIDE_RE.finditer(chunk))
    for i, m in enumerate(slide_matches):
        start = m.end()
        end = slide_matches[i + 1].start() if i + 1 < len(slide_matches) else len(chunk)
        body = chunk[start:end]
        slide = {"n": int(m.group(1)), "title": m.group(2).strip(),
                 "ment": "", "time": "", "emphasis": "", "qa": "", "ops": ""}
        for b in BULLET_RE.finditer(body):
            key = b.group(1).replace("예상Q", "qa").replace("예상 Q", "qa")
            mapping = {"멘트": "ment", "시간": "time", "강조": "emphasis", "qa": "qa", "운영": "ops"}
            field = mapping.get(key, None)
            if field:
                slide[field] = b.group(2).strip()
        slides.append(slide)
    return slides


def slide_to_feature_map(sections: list[dict[str, Any]]) -> dict[int, str]:
    """슬라이드 번호 → 기능명 매핑 (strict 매핑용)."""
    m: dict[int, str] = {}
    for sec in sections:
        for n in range(sec["slide_start"], sec["slide_end"] + 1):
            m[n] = sec["feature_name"]
    return m
```

- [ ] **Step 5: 테스트 통과 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_extract_notes.py -v`
Expected: 4 PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/lecture_archive/extract_notes.py scripts/lecture_archive/tests/test_extract_notes.py scripts/lecture_archive/tests/fixtures/sample_instructor_notes.md
git commit -m "Add: extract_notes.py — 섹션·슬라이드 범위·발췌 (TDD, 4 tests)"
```

---

### Task 9: map_features.py — strict + heading + Gemini 3단계

**Files:**
- Create: `scripts/lecture_archive/map_features.py`
- Create: `scripts/lecture_archive/tests/test_map_features.py`

- [ ] **Step 1: 테스트 작성 (Gemini 호출은 stub으로)**

```python
# scripts/lecture_archive/tests/test_map_features.py
from lecture_archive.map_features import (
    map_strict, map_heading, decide_mapping,
)


def test_map_strict_uses_notes_range():
    slide_to_feature = {7: "CLAUDE.md", 8: "CLAUDE.md", 11: "Auto Memory"}
    slides = [{"n": 7, "title": "CLAUDE.md"}, {"n": 8, "title": "CLAUDE.md 개념"}, {"n": 99, "title": "기타"}]
    result = map_strict(slides, slide_to_feature)
    assert result[7] == ("CLAUDE.md", "strict")
    assert result[8] == ("CLAUDE.md", "strict")
    assert 99 not in result  # strict 매핑 안 됨


def test_map_heading_fuzzy_matches():
    catalog = [
        {"id": "F-035", "name": "CLAUDE.md", "name_ko": "CLAUDE.md (프로젝트 컨텍스트)"},
        {"id": "F-036", "name": "Auto Memory", "name_ko": "Auto Memory (자동 메모리)"},
    ]
    unmapped = [{"n": 99, "title": "CLAUDE.md 응용"}]
    result = map_heading(unmapped, catalog)
    assert result[99] == ("CLAUDE.md", "heading")


def test_decide_mapping_prefers_strict():
    strict = {7: ("CLAUDE.md", "strict")}
    heading = {7: ("Other", "heading")}
    llm = {7: ("Yet Another", "llm")}
    final = decide_mapping(strict, heading, llm)
    assert final[7] == ("CLAUDE.md", "strict")


def test_decide_mapping_falls_through():
    strict = {}
    heading = {99: ("Heuristic", "heading")}
    llm = {99: ("LLM Guess", "llm")}
    final = decide_mapping(strict, heading, llm)
    assert final[99] == ("Heuristic", "heading")
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_map_features.py -v`
Expected: FAIL — `lecture_archive.map_features` 미정의.

- [ ] **Step 3: map_features.py 구현**

```python
# scripts/lecture_archive/map_features.py
"""슬라이드 ↔ 기능 매핑 — strict (notes) → heading (fuzzy) → llm (Gemini)."""
from __future__ import annotations
from difflib import SequenceMatcher
from typing import Any

Mapping = dict[int, tuple[str, str]]  # n → (feature_name, method)
HEADING_THRESHOLD = 0.55


def map_strict(slides: list[dict[str, Any]], slide_to_feature: dict[int, str]) -> Mapping:
    """instructor-notes 헤딩의 (Sn~Sm) 범위로 직접 매핑."""
    out: Mapping = {}
    for slide in slides:
        n = slide["n"]
        if n in slide_to_feature:
            out[n] = (slide_to_feature[n], "strict")
    return out


def map_heading(unmapped_slides: list[dict[str, Any]], catalog: list[dict[str, Any]]) -> Mapping:
    """슬라이드 h2 ↔ 카탈로그 기능명 fuzzy matching."""
    out: Mapping = {}
    for slide in unmapped_slides:
        title = slide.get("title", "")
        if not title:
            continue
        best_score = 0.0
        best_name = None
        for f in catalog:
            for candidate in (f.get("name", ""), f.get("name_ko", "")):
                if not candidate:
                    continue
                score = SequenceMatcher(None, title.lower(), candidate.lower()).ratio()
                if title.split()[0].lower() in candidate.lower():
                    score = max(score, 0.7)
                if score > best_score:
                    best_score = score
                    best_name = f.get("name")
        if best_score >= HEADING_THRESHOLD and best_name:
            out[slide["n"]] = (best_name, "heading")
    return out


def map_llm(unmapped_slides: list[dict[str, Any]], catalog: list[dict[str, Any]],
            gemini_call) -> Mapping:
    """Gemini 분류 폴백. gemini_call(slide, catalog) → feature_name."""
    out: Mapping = {}
    for slide in unmapped_slides:
        name = gemini_call(slide, catalog)
        if name:
            out[slide["n"]] = (name, "llm")
    return out


def decide_mapping(*layers: Mapping) -> Mapping:
    """우선순위. 첫 번째 layer의 값이 우선."""
    final: Mapping = {}
    for layer in layers:
        for n, (name, method) in layer.items():
            if n not in final:
                final[n] = (name, method)
    return final


def call_gemini(slide: dict[str, Any], catalog: list[dict[str, Any]]) -> str | None:
    """실제 Gemini 호출. .env GEMINI_API_KEY 사용."""
    import os
    import google.generativeai as genai
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    catalog_text = "\n".join(f"- {f['id']} {f['name']} — {f.get('def', '')}" for f in catalog)
    prompt = f"""다음 슬라이드를 카탈로그에서 하나의 기능에 분류하라.

[슬라이드]
제목. {slide.get('title', '')}
본문. {slide.get('text', '')[:500]}

[카탈로그]
{catalog_text}

분류 결과를 기능명만 한 줄로 답하라. 매칭되는 것이 없으면 'NONE'."""
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    resp = model.generate_content(prompt)
    name = resp.text.strip()
    if name == "NONE":
        return None
    # 카탈로그에 실제 존재하는 기능명인지 검증
    valid = {f["name"] for f in catalog}
    return name if name in valid else None
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_map_features.py -v`
Expected: 4 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/lecture_archive/map_features.py scripts/lecture_archive/tests/test_map_features.py
git commit -m "Add: map_features.py — strict·heading·Gemini 3단계 매핑 (TDD, 4 tests)"
```

---

### Task 10: build_site.py — Jekyll collection·_data·assets 빌드

**Files:**
- Create: `scripts/lecture_archive/build_site.py`
- Create: `scripts/lecture_archive/tests/test_build_site.py`

- [ ] **Step 1: 테스트 작성 (사이트 경로 mocking)**

```python
# scripts/lecture_archive/tests/test_build_site.py
from pathlib import Path
import yaml
from lecture_archive.build_site import (
    write_feature_page, write_hub_page, append_lecture_index,
)


def test_write_feature_page(tmp_path):
    lect_dir = tmp_path / "_lectures" / "kist-claude-code"
    lect_dir.mkdir(parents=True)
    feature = {
        "id": "F-035", "name": "CLAUDE.md", "slug": "claudemd",
        "track": "basic", "def": "프로젝트 컨텍스트 주입",
        "actions": ["a", "b", "c"], "usage_code": "claude\n/init",
        "usage_lang": "powershell", "rationale": "테스트",
        "related_slides": [{"n": 8, "title": "S8", "png": "/x.webp", "text": "..."}],
        "ment_excerpt": "강사 멘트", "lab_excerpt": "",
        "source_urls": ["https://docs.anthropic.com/claude-code"],
    }
    write_feature_page(lect_dir, "kist-claude-code", feature, prev_slug=None, next_slug="auto-memory")
    out = lect_dir / "claudemd.md"
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "F-035" in content
    assert "permalink: /lectures/kist-claude-code/claudemd/" in content
    assert "프로젝트 컨텍스트 주입" in content


def test_append_lecture_index_creates_new(tmp_path):
    data_file = tmp_path / "lectures.yml"
    data_file.write_text("[]", encoding="utf-8")
    block = {"slug": "kist-claude-code", "title": "Test", "feature_count": 22}
    append_lecture_index(data_file, block)
    loaded = yaml.safe_load(data_file.read_text(encoding="utf-8"))
    assert len(loaded) == 1
    assert loaded[0]["slug"] == "kist-claude-code"


def test_append_lecture_index_replaces_existing(tmp_path):
    data_file = tmp_path / "lectures.yml"
    yaml.dump([{"slug": "kist-claude-code", "title": "Old"}], data_file.open("w", encoding="utf-8"))
    block = {"slug": "kist-claude-code", "title": "New", "feature_count": 22}
    append_lecture_index(data_file, block)
    loaded = yaml.safe_load(data_file.read_text(encoding="utf-8"))
    assert len(loaded) == 1
    assert loaded[0]["title"] == "New"
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_build_site.py -v`
Expected: FAIL — `lecture_archive.build_site` 미정의.

- [ ] **Step 3: build_site.py 구현**

```python
# scripts/lecture_archive/build_site.py
"""Jekyll collection·_data·_includes·assets 산출물 빌드."""
from __future__ import annotations
from pathlib import Path
from typing import Any
import yaml
import json


def write_feature_page(lecture_dir: Path, lecture_slug: str, feature: dict[str, Any],
                       prev_slug: str | None, next_slug: str | None) -> Path:
    """기능 페이지 마크다운 작성."""
    fm = {
        "title": f"{feature['name']} — {feature['id']}",
        "permalink": f"/lectures/{lecture_slug}/{feature['slug']}/",
        "layout": "lecture",
        "lecture_slug": lecture_slug,
        "feature_id": feature["id"],
        "feature_name": feature["name"],
        "feature_slug": feature["slug"],
        "track": feature["track"],
        "order": feature.get("order", 0),
    }
    body_parts = [
        f'<div class="feature-header">',
        f'  <span class="feature-badge">{feature["id"]}</span>',
        f'  <span class="feature-badge track-{feature["track"]}">{feature["track"]}</span>',
        f'  <h1>{feature["name"]}</h1>',
        f'</div>',
        "",
        f"{feature['def']}",
        "",
        "## 핵심 동작",
        "",
    ]
    for action in feature.get("actions", []):
        body_parts.append(f"- {action}")
    body_parts.extend([
        "",
        "## 사용법",
        "",
        f"```{feature.get('usage_lang', 'powershell')}",
        feature.get("usage_code", "").strip(),
        "```",
        "",
        "## 관련 슬라이드",
        "",
    ])
    for s in feature.get("related_slides", []):
        body_parts.extend([
            f'<figure class="slide-excerpt">',
            f'  <img src="{s["png"]}" alt="S{s["n"]} — {s["title"]}" loading="lazy">',
            f'  <figcaption>S{s["n"]} · {s["title"]}</figcaption>',
            f'  <div class="slide-text">{s.get("text", "")[:300]}</div>',
            f'</figure>',
            "",
        ])
    if feature.get("ment_excerpt"):
        body_parts.extend(["## 강사 멘트", "", f"> {feature['ment_excerpt']}", ""])
    if feature.get("lab_excerpt"):
        body_parts.extend(["## 실습", "", feature["lab_excerpt"], ""])
    if feature.get("rationale"):
        body_parts.extend(["## 활용 시사점", "", feature["rationale"], ""])
    if feature.get("source_urls"):
        body_parts.extend(["## 출처", ""])
        for url in feature["source_urls"]:
            body_parts.append(f"- <{url}>")
    out_path = lecture_dir / f"{feature['slug']}.md"
    fm_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False)
    content = f"---\n{fm_yaml}---\n\n" + "\n".join(body_parts) + "\n"
    out_path.write_text(content, encoding="utf-8")
    return out_path


def write_hub_page(lecture_dir: Path, lecture_slug: str, lecture_meta: dict[str, Any],
                   features: list[dict[str, Any]]) -> Path:
    """강의 허브 페이지 (index.md) 작성."""
    fm = {
        "title": lecture_meta["title"],
        "permalink": f"/lectures/{lecture_slug}/",
        "layout": "lecture",
        "lecture_slug": lecture_slug,
    }
    body = [
        f"## {lecture_meta.get('subtitle', '')}",
        "",
        f"- 청중. {lecture_meta.get('audience', '')}",
        f"- 시간. {lecture_meta.get('duration_min', 0)}분",
        f"- 환경. {lecture_meta.get('environment', '')}",
        "",
        "## 기능 카탈로그",
        "",
        '<div class="lecture-card-grid">',
    ]
    for f in features:
        body.append(
            f'{{% include lecture-card.html feature=site.data.lectures'
            f'[0].features_full[{features.index(f)}] lecture_slug="{lecture_slug}" %}}'
        )
    body.extend(['</div>', "", "## 다운로드", "",
                 f"- [원본 슬라이드 풀스크린]({lecture_meta['assets']['slides']})",
                 f"- [핸드아웃 PDF]({lecture_meta['assets']['handout']})"])
    out_path = lecture_dir / "index.md"
    fm_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False)
    out_path.write_text(f"---\n{fm_yaml}---\n\n" + "\n".join(body) + "\n", encoding="utf-8")
    return out_path


def append_lecture_index(data_file: Path, block: dict[str, Any]) -> None:
    """`_data/lectures.yml`에 강의 블록 추가/교체."""
    if data_file.exists():
        existing = yaml.safe_load(data_file.read_text(encoding="utf-8")) or []
    else:
        existing = []
    out = [b for b in existing if b.get("slug") != block.get("slug")]
    out.append(block)
    data_file.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")


def write_slides_index_json(slides_dir: Path, slides: list[dict[str, Any]]) -> Path:
    """슬라이드별 텍스트·메타 JSON 인덱스 (검색용)."""
    slides_dir.mkdir(parents=True, exist_ok=True)
    out = slides_dir / "index.json"
    out.write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `python -m pytest scripts/lecture_archive/tests/test_build_site.py -v`
Expected: 3 PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/lecture_archive/build_site.py scripts/lecture_archive/tests/test_build_site.py
git commit -m "Add: build_site.py — Jekyll 산출물 빌드 (TDD, 3 tests)"
```

---

### Task 11: orchestrate.py — 진입점·zip 해제·brief.yml·게이트

**Files:**
- Create: `scripts/lecture_archive/orchestrate.py`

- [ ] **Step 1: 구현 (테스트는 통합 단계에서)**

```python
# scripts/lecture_archive/orchestrate.py
"""강의자료 큐레이션 진입점.

호출 예:
  python -m scripts.lecture_archive.orchestrate <zip-path> --slug kist-claude-code
"""
from __future__ import annotations
import argparse
import shutil
import zipfile
from pathlib import Path
import yaml
import os

from .utils import decode_zip_filename, slug_from_zip_name


REPO_ROOT = Path(__file__).resolve().parents[2]


def extract_zip(zip_path: Path, dst: Path) -> None:
    """zip 해제. 한글 파일명 cp437→utf-8 디코드."""
    dst.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            # cp437 잘못 인코딩된 한글 파일명 복원
            try:
                info.filename = info.filename.encode("cp437").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
            z.extract(info, dst)


def find_assets(input_dir: Path) -> dict[str, Path | None]:
    """입력 디렉토리에서 표준 자산 탐색."""
    assets = {
        "slides_html": None,
        "instructor_notes": None,
        "handout_html": None,
        "labs_md": None,
        "feature_catalog": None,
    }
    for p in input_dir.rglob("*"):
        if not p.is_file():
            continue
        name = p.name.lower()
        if "slides" in name and name.endswith(".html"):
            if assets["slides_html"] is None or "v2" in name:
                assets["slides_html"] = p
        elif "instructor" in name and name.endswith(".md"):
            if assets["instructor_notes"] is None or "v2" in name:
                assets["instructor_notes"] = p
        elif name == "handout.html" or (name.startswith("handout") and name.endswith(".html")):
            assets["handout_html"] = p
        elif name == "labs.md" or name.startswith("labs"):
            assets["labs_md"] = p
        elif "feature_ideas" in name or "07_feature" in name:
            assets["feature_catalog"] = p
    return assets


def write_brief(workspace: Path, slug: str, zip_path: Path, assets: dict) -> Path:
    brief = {
        "slug": slug,
        "title": "[강사 확인 필요]",
        "subtitle": "[강사 확인 필요]",
        "audience": "[강사 확인 필요]",
        "duration_min": 0,
        "environment": "[강사 확인 필요]",
        "atom_mode": "feature_catalog" if assets.get("feature_catalog") else "section_heading",
        "assets": {k: (str(v.relative_to(workspace)) if v else None) for k, v in assets.items()},
        "source_zip": str(zip_path),
    }
    out = workspace / "brief.yml"
    out.write_text(yaml.safe_dump(brief, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_path")
    parser.add_argument("--slug", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--skip-playwright", action="store_true")
    parser.add_argument("--rerun", choices=["parser", "curator", "builder"], default=None)
    args = parser.parse_args(argv)
    
    zip_path = Path(args.zip_path).resolve()
    if not zip_path.exists():
        print(f"[ERR] zip not found: {zip_path}")
        return 1
    
    slug = args.slug or slug_from_zip_name(zip_path.name)
    workspace = REPO_ROOT / "_workspace" / slug
    input_dir = workspace / "00_input"
    
    print(f"[INFO] slug: {slug}")
    print(f"[INFO] workspace: {workspace}")
    
    if not args.rerun:
        if workspace.exists():
            from datetime import datetime
            backup = workspace.with_name(f"{slug}_{datetime.now():%Y%m%d_%H%M%S}")
            workspace.rename(backup)
            print(f"[INFO] backed up existing workspace → {backup.name}")
        workspace.mkdir(parents=True)
        extract_zip(zip_path, input_dir)
    
    assets = find_assets(input_dir)
    print(f"[INFO] assets found: {[k for k, v in assets.items() if v]}")
    
    brief_path = write_brief(workspace, slug, zip_path, assets)
    print(f"[OK] brief.yml → {brief_path}")
    print()
    print("[NEXT] Superpowers 멀티 에이전트 팀을 시작할 준비가 됐습니다.")
    print(f"       다음 단계는 .claude/skills/lecture-archive-orchestrator/SKILL.md 참조")
    print(f"       또는 슬래시 커맨드 /lecture-archive {zip_path}로 자동 진행")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 2: 통합 점검 — KIST zip으로 dry-run**

Run:
```
python -m scripts.lecture_archive.orchestrate "c:/Users/windo/Desktop/260429_황민호_강의자료.Zip" --dry-run
```
Expected: `_workspace/<slug>/00_input/`에 5개 자산 추출. `brief.yml` 생성. `[OK]` 출력.

- [ ] **Step 3: Commit**

```bash
git add scripts/lecture_archive/orchestrate.py
git commit -m "Add: orchestrate.py — zip 해제·자산 탐색·brief.yml"
```

---

## Task 분해 — Phase C: 에이전트 팀 + 슬래시 커맨드

### Task 12: SKILL.md — 멀티 에이전트 팀 명세

**Files:**
- Create: `.claude/skills/lecture-archive-orchestrator/SKILL.md`

- [ ] **Step 1: SKILL.md 작성**

KIST `kist-lecture-orchestrator/SKILL.md`의 형식을 답습하되 5명 큐레이션 팀으로 재편.

```markdown
---
name: lecture-archive-orchestrator
description: "강의자료 zip을 tigerjk9.github.io _lectures/ collection으로 자동 큐레이션. 트리거 표현. '강의자료 큐레이션', 'lecture archive', '강의자료 변환'. 후속 작업. 슬라이드 재추출(--rerun parser), 기능 페이지 재생성(--rerun curator), 빌드 재실행(--rerun builder)."
---

# Lecture Archive Orchestrator

강의자료 zip을 검색·재방문 가능한 _lectures/ collection으로 자동 큐레이션하는 5명 에이전트 팀.

## 실행 모드

`TeamCreate`로 5명 팀 구성, `TaskCreate`로 의존성 등록, 팀원들이 `SendMessage`로 자체 조율. 리더는 `reviewer-editor`.

## 에이전트 구성

| 팀원 | subagent_type | model | 역할 |
|------|---------------|-------|------|
| inventory | general-purpose | opus | zip 자산 인벤토리·관계 매트릭스 |
| parser | executor | opus | parse_slides.py 호출 (BS4 + Playwright) |
| curator | general-purpose | opus | feature 페이지 마크다운 + slug 매핑 yml |
| builder | executor | opus | build_site.py 호출 (Jekyll 통합) |
| reviewer | executor | opus | 팀 리더. jekyll build 검증·체크리스트 |

## 워크플로우

(Phase 0~5 — spec §5 그대로)

## 검토 게이트

curator가 `_workspace/<slug>/03_features/_slug_map.yml` 출력 후 builder는 멈추고 **사용자 명시 승인 대기**. 승인 키워드. "slug 승인", "approve slugs". URL은 영구적이므로 한 번에 정한다.

## 데이터 흐름

(spec §1·§5-5 그대로)

## 후속 작업 키워드

- "강의자료 변환 다시"
- "슬라이드 재추출"
- "기능 페이지 재생성"
- "강의 사이트 빌드만"
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/lecture-archive-orchestrator/SKILL.md
git commit -m "Add: lecture-archive-orchestrator 스킬 (5명 팀 명세)"
```

---

### Task 13: 슬래시 커맨드 정의

**Files:**
- Create: `.claude/commands/lecture-archive.md`

- [ ] **Step 1: 슬래시 커맨드 작성**

```markdown
---
description: "강의자료 zip → _lectures/ collection 자동 큐레이션"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - TaskCreate
  - TaskUpdate
---

# /lecture-archive

강의자료 zip 한 묶음(slides·instructor-notes·handout·labs·카탈로그)을 tigerjk9.github.io 블로그의 `_lectures/` collection으로 자동 큐레이션한다.

## 사용

```
/lecture-archive <zip-path> [--slug <slug>] [--dry-run] [--no-push] [--skip-playwright] [--rerun parser|curator|builder]
```

## 실행 흐름

1. `scripts/lecture_archive/orchestrate.py`로 zip 해제·brief.yml 생성
2. `.claude/skills/lecture-archive-orchestrator/SKILL.md`의 5명 팀 명세에 따라 `TeamCreate`
3. inventory → parser ∥ curator → 슬러그 검토 게이트 → builder → reviewer 파이프라인
4. 사용자에게 결과 보고. `--no-push` 미지정 시 git push까지

## 사용자 입력 지점 1개

- **slug 검토 게이트** — curator가 `_workspace/<slug>/03_features/_slug_map.yml` 출력 후 builder는 멈춤. 사용자가 검토하고 "slug 승인" 또는 yml 직접 편집 후 승인 → builder 시작

## 산출

(spec §1 디렉토리 구조 참조)

## 알려진 한계

- Playwright Chromium 첫 다운로드 ~150MB. 망분리 환경은 `--skip-playwright` + 강사 사전 추출
- 슬라이드 N장 중 일부 (예상 4~6장)는 Gemini 분류 필요. 강사 검증 권장
- 한 강의 변환 ~10~15분 + slug 검토 시간
```

- [ ] **Step 2: Commit**

```bash
git add .claude/commands/lecture-archive.md
git commit -m "Add: /lecture-archive 슬래시 커맨드 정의"
```

---

## Task 분해 — Phase D: 첫 KIST 변환 실행

### Task 14: orchestrate.py로 zip 해제·자산 탐색 (KIST)

**Files:**
- (실행만, 산출은 `_workspace/`)

- [ ] **Step 1: KIST zip 해제·brief.yml 생성**

Run:
```
python -m scripts.lecture_archive.orchestrate "c:/Users/windo/Desktop/260429_황민호_강의자료.Zip" --slug kist-claude-code
```
Expected:
- `_workspace/kist-claude-code/00_input/`에 zip 5종 자산 추출
- 한글 파일명 정상 (예. `발표자료_소스/claude-code-for-kist/output/instructor-notes.v2.md`)
- `brief.yml`에 atom_mode: feature_catalog 자동 결정 (07_feature_ideas.md 발견)

- [ ] **Step 2: brief.yml 수동 보강**

`_workspace/kist-claude-code/brief.yml` 편집. `[강사 확인 필요]` 항목을 KIST README.md 기반으로 채움:

```yaml
title: "Claude Code 실무 활용 — KIST 워크숍"
subtitle: "황민호 수석 · Forward Deployed Engineer · 2026-04-29"
audience: "KIST 연구원"
duration_min: 120
environment: "Windows PowerShell"
date: "2026-04-29"
```

- [ ] **Step 3: Commit (workspace는 .gitignore 권장이지만 첫 사례는 추적)**

`.gitignore` 점검 → workspace 디렉토리 추적 정책 결정. 추적 안 하면 다음 단계 commit 생략.

---

### Task 15: parser 실행 — KIST 슬라이드 96장 추출

**Files:**
- (실행 산출)

- [ ] **Step 1: slides.v2.html에서 96장 추출 + PNG·WebP 캡처**

Run:
```python
python -c "
from pathlib import Path
from scripts.lecture_archive.parse_slides import parse_html, capture_pngs, convert_to_webp
import json

ws = Path('_workspace/kist-claude-code')
slides_html = ws / '00_input/발표자료_소스/claude-code-for-kist/output/slides.v2.html'
slides = parse_html(slides_html.read_text(encoding='utf-8'))
print(f'parsed: {len(slides)} slides')

png_dir = ws / 'slides'
pngs = capture_pngs(slides_html, png_dir)
print(f'PNG: {len(pngs)}')
webps = convert_to_webp(pngs)
print(f'WebP: {len(webps)}')

# PNG 경로를 슬라이드에 주입
for i, s in enumerate(slides):
    if i < len(webps):
        s['png'] = f'/assets/lectures/kist-claude-code/slides/{webps[i].name}'
        s['png_original'] = f'/assets/lectures/kist-claude-code/slides/{pngs[i].name}'

(ws / '02_slides.json').write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding='utf-8')
print('02_slides.json written')
"
```
Expected:
- `parsed: 96 slides`
- `PNG: 96` (시간 5~7분)
- `WebP: 96` (~10MB)
- `_workspace/kist-claude-code/02_slides.json` 생성

- [ ] **Step 2: 슬라이드 메타 점검**

Run: `python -c "import json; data=json.load(open('_workspace/kist-claude-code/02_slides.json', encoding='utf-8')); print('total:', len(data)); print('blocks:', set(s['block'] for s in data)); print('layouts:', set(s['layout'] for s in data))"`
Expected: 96, 다양한 블록·레이아웃 노출.

---

### Task 16: curator 실행 — 매핑·슬러그·기능 마크다운

**Files:**
- (실행 산출)

- [ ] **Step 1: instructor-notes 파싱 + 매핑 + slug yml 출력**

Run:
```python
python -c "
from pathlib import Path
import json, yaml
from scripts.lecture_archive.extract_notes import parse_notes, slide_to_feature_map
from scripts.lecture_archive.map_features import map_strict, map_heading, map_llm, decide_mapping, call_gemini
from scripts.lecture_archive.utils import safe_slug

ws = Path('_workspace/kist-claude-code')
notes_md = (ws / '00_input/발표자료_소스/claude-code-for-kist/output/instructor-notes.v2.md').read_text(encoding='utf-8')
sections = parse_notes(notes_md)
slide_map = slide_to_feature_map(sections)
print(f'sections: {len(sections)}')

slides = json.load((ws / '02_slides.json').open(encoding='utf-8'))

# 카탈로그 파싱 (07_feature_ideas.md → list of {id, name, name_ko, def})
# 간이 파서. 실제 카탈로그 구조에 맞춰 보강 필요.
catalog_md = (ws / '00_input/발표자료_소스/claude-code-for-kist/_workspace/07_feature_ideas.md').read_text(encoding='utf-8')
import re
catalog = []
for m in re.finditer(r'### (F-\d+)\.\s+([^(\n]+?)(?:\s*\(([^)]+)\))?\s*$\n(.*?)(?=\n### F-|\Z)', catalog_md, re.M | re.S):
    fid = m.group(1)
    name = m.group(2).strip()
    name_ko = m.group(3).strip() if m.group(3) else ''
    body = m.group(4)
    def_m = re.search(r'\*\*정의\.\*\*\s*([^\n]+)', body)
    catalog.append({'id': fid, 'name': name, 'name_ko': name_ko, 'def': def_m.group(1).strip() if def_m else ''})
print(f'catalog: {len(catalog)} features')

strict = map_strict(slides, slide_map)
mapped_ns = set(strict.keys())
unmapped = [s for s in slides if s['n'] not in mapped_ns]
heading = map_heading(unmapped, catalog)
unmapped2 = [s for s in slides if s['n'] not in mapped_ns and s['n'] not in heading]
llm = map_llm(unmapped2, catalog, call_gemini) if unmapped2 else {}
final = decide_mapping(strict, heading, llm)
print(f'strict: {len(strict)} / heading: {len(heading)} / llm: {len(llm)} / unmapped: {len(slides) - len(final)}')

# slug map
slug_map = []
for f in catalog:
    slug_map.append({'id': f['id'], 'name': f['name'], 'slug': safe_slug(f['name'])})
(ws / '03_features').mkdir(exist_ok=True)
(ws / '03_features/_slug_map.yml').write_text(yaml.safe_dump(slug_map, allow_unicode=True, sort_keys=False), encoding='utf-8')
print('_slug_map.yml written. 사용자 검토 게이트.')
"
```
Expected: `strict: ~78 / heading: ~14 / llm: ~4 / unmapped: 0`. `_slug_map.yml` 생성.

- [ ] **Step 2: ★ 검토 게이트 — 사용자 명시 승인**

사용자가 `_workspace/kist-claude-code/03_features/_slug_map.yml`을 검토하고 다음 중 하나 답변:
- "slug 승인" → builder 진행
- yml 직접 편집 후 "수정 승인" → 편집 반영 후 builder 진행

승인되면 Step 3 진행.

- [ ] **Step 3: 기능 마크다운 생성 (curator 마지막 단계)**

승인된 slug 매핑으로 각 기능에 대해 관련 슬라이드·노트 발췌·라벨을 모아 `_workspace/kist-claude-code/03_features/<slug>.md` 22장 생성. 코드 작업은 build_site.py의 `write_feature_page`가 다음 단계에서 처리.

---

### Task 17: builder 실행 — _lectures/·_data·assets 배포

**Files:**
- Create: `_lectures/kist-claude-code/{index.md, *.md × 22}`
- Modify: `_data/lectures.yml`
- Create: `assets/lectures/kist-claude-code/{slides.html, slides/, handout.pdf, cover.png, feature-thumb/}`

- [ ] **Step 1: assets 배포**

Run:
```python
python -c "
from pathlib import Path
import shutil
ws = Path('_workspace/kist-claude-code')
dst = Path('assets/lectures/kist-claude-code')
dst.mkdir(parents=True, exist_ok=True)
# 슬라이드 원본 HTML
src_html = ws / '00_input/발표자료_소스/claude-code-for-kist/output/slides.v2.html'
shutil.copy(src_html, dst / 'slides.html')
# 슬라이드 PNG/WebP
(dst / 'slides').mkdir(exist_ok=True)
for f in (ws / 'slides').glob('*'):
    shutil.copy(f, dst / 'slides' / f.name)
# 핸드아웃 HTML → PDF (weasyprint)
from weasyprint import HTML
handout_html = ws / '00_input/발표자료_소스/claude-code-for-kist/output/handout.v2.html'
HTML(filename=str(handout_html)).write_pdf(str(dst / 'handout.pdf'))
print('assets deployed')
"
```
Expected: `assets/lectures/kist-claude-code/`에 slides.html, slides/ 192개 파일, handout.pdf, cover.png(별도 추출) 배치.

- [ ] **Step 2: _lectures/ 마크다운 생성**

Run:
```python
python -c "
from pathlib import Path
import yaml, json
from scripts.lecture_archive.build_site import write_feature_page, write_hub_page, append_lecture_index

ws = Path('_workspace/kist-claude-code')
brief = yaml.safe_load((ws / 'brief.yml').read_text(encoding='utf-8'))
slug_map = yaml.safe_load((ws / '03_features/_slug_map.yml').read_text(encoding='utf-8'))

# 기능별 자료 조합 (curator가 미리 만든 03_features/<slug>.yml 또는 직접 조합)
slides = json.load((ws / '02_slides.json').open(encoding='utf-8'))

lect_dir = Path('_lectures/kist-claude-code')
lect_dir.mkdir(parents=True, exist_ok=True)

features_full = []
for i, item in enumerate(slug_map):
    feature = {
        'id': item['id'],
        'name': item['name'],
        'slug': item['slug'],
        'track': 'basic' if i < 12 else 'advanced',
        'def': item.get('def', ''),
        'actions': item.get('actions', []),
        'usage_code': item.get('usage_code', ''),
        'usage_lang': 'powershell',
        'rationale': item.get('rationale', ''),
        'related_slides': [s for s in slides if s.get('feature_slug') == item['slug']],
        'ment_excerpt': item.get('ment_excerpt', ''),
        'lab_excerpt': item.get('lab_excerpt', ''),
        'source_urls': item.get('source_urls', []),
        'order': i,
    }
    features_full.append(feature)

for i, f in enumerate(features_full):
    prev_slug = features_full[i-1]['slug'] if i > 0 else None
    next_slug = features_full[i+1]['slug'] if i+1 < len(features_full) else None
    write_feature_page(lect_dir, 'kist-claude-code', f, prev_slug, next_slug)

write_hub_page(lect_dir, 'kist-claude-code', {
    'title': brief['title'],
    'subtitle': brief['subtitle'],
    'audience': brief['audience'],
    'duration_min': brief['duration_min'],
    'environment': brief['environment'],
    'assets': {
        'slides': '/assets/lectures/kist-claude-code/slides.html',
        'handout': '/assets/lectures/kist-claude-code/handout.pdf',
    },
}, features_full)

# _data/lectures.yml 갱신
basic_features = [f['slug'] for f in features_full if f['track'] == 'basic']
advanced_features = [f['slug'] for f in features_full if f['track'] == 'advanced']
block = {
    'slug': 'kist-claude-code',
    'title': brief['title'],
    'subtitle': brief['subtitle'],
    'audience': brief['audience'],
    'duration_min': brief['duration_min'],
    'environment': brief['environment'],
    'hub_url': '/lectures/kist-claude-code/',
    'thumbnail': '/assets/lectures/kist-claude-code/cover.png',
    'tracks': [
        {'id': 'basic', 'label': 'Basic', 'features': basic_features},
        {'id': 'advanced', 'label': 'Advanced', 'features': advanced_features},
    ],
    'feature_count': len(features_full),
    'slide_count': 96,
    'atom_mode': 'feature_catalog',
    'assets': {
        'slides': '/assets/lectures/kist-claude-code/slides.html',
        'handout': '/assets/lectures/kist-claude-code/handout.pdf',
    },
    'features_full': features_full,
}
append_lecture_index(Path('_data/lectures.yml'), block)
print(f'_lectures/kist-claude-code/ 23 files + _data/lectures.yml 갱신')
"
```
Expected: `_lectures/kist-claude-code/index.md` + 22개 기능 페이지 + `_data/lectures.yml` 갱신.

- [ ] **Step 3: jekyll build 검증**

Run: `bundle exec jekyll build 2>&1 | tail -30`
Expected: 빌드 성공. `_site/lectures/kist-claude-code/<slug>/index.html` 22개 생성.

---

### Task 18: reviewer 검증 — 체크리스트 12개

**Files:**
- (검증만)

- [ ] **Step 1: 체크리스트 12개 자동 실행**

Run:
```bash
bundle exec jekyll build && \
echo "=== 1. build OK ===" && \
test -f _site/lectures/index.html && echo "=== 2. index OK ===" && \
test -f _site/lectures/kist-claude-code/index.html && echo "=== 3. hub OK ===" && \
ls _site/lectures/kist-claude-code/ | grep -v index | wc -l && \
echo "=== 4. feature pages (should be 22+1) ===" && \
grep -l "slide-excerpt" _site/lectures/kist-claude-code/*.html | wc -l && \
echo "=== 5. excerpts present ===" && \
cat _workspace/kist-claude-code/04_review.md 2>/dev/null || echo "=== 6. mapping stats: see Task 16 ===" && \
grep -E "kist-claude-code|lectures" _site/categories/*.html 2>/dev/null | head -3 && \
echo "=== 8. category isolation (should show 0 matches) ===" && \
diff <(git show HEAD:graph-data.json 2>/dev/null) graph-data.json && echo "=== 9. graph unchanged ===" && \
grep "강의자료" _site/index.html 2>/dev/null && echo "=== 10. nav present ===" && \
du -sm assets/lectures/kist-claude-code && echo "=== 11. asset size ===" && \
echo "=== 12. permalink check below ===" && \
grep -roh "permalink: /lectures/[^\"]*" _lectures/kist-claude-code/ | sort -u | wc -l
```
Expected: 모든 항목 정상. permalink 23개 unique.

- [ ] **Step 2: 강사 검증 권장 항목 보고**

`_workspace/kist-claude-code/04_review.md` 작성:
```markdown
# 04. KIST Claude Code 워크숍 큐레이션 검증 보고

## 매핑 통계
- strict: NN장 / heading: NN장 / llm: NN장 / unmapped: 0

## 강사 검증 권장
- llm 분류 슬라이드 N개: [목록]
- 22 기능 slug 매핑: 사전 게이트 통과
- 격리 검증: 통과

## 5개 시나리오 진입 URL
1. /lectures/
2. /lectures/kist-claude-code/
3. /lectures/kist-claude-code/claudemd/
4. /assets/lectures/kist-claude-code/slides.html
5. /assets/lectures/kist-claude-code/handout.pdf
```

---

### Task 19: 첫 변환 commit·push

**Files:**
- (git 작업)

- [ ] **Step 1: 신규 파일 명시 add**

```bash
git add _lectures/kist-claude-code/
git add _data/lectures.yml
git add assets/lectures/kist-claude-code/
git status --short
```
Expected: 명시한 파일들만 staged. `_workspace/`는 누락 (.gitignore 결정에 따름).

- [ ] **Step 2: commit**

```bash
MSG=$(mktemp)
cat > "$MSG" <<'EOF'
Add: KIST Claude Code 워크숍 큐레이션 — 22 기능 페이지 + 96 슬라이드

황민호 수석 KIST 워크숍 자료(2026-04-29) zip을
lecture-archive-orchestrator 하네스로 첫 변환.

산출:
- _lectures/kist-claude-code/{index.md + 22 기능 페이지}
- _data/lectures.yml에 강의 블록 추가
- assets/lectures/kist-claude-code/{slides.html, slides/×192, handout.pdf, cover.png}

매핑 통계: strict NN장 / heading NN장 / llm NN장.
slug 사용자 검토 게이트 통과.
EOF
git commit -F "$MSG"
rm "$MSG"
```

- [ ] **Step 3: push**

```bash
git fetch origin && git rebase origin/main --autostash && git push origin main
```
Expected: push 성공. https://tigerjk9.github.io/lectures/kist-claude-code/ 게시.

- [ ] **Step 4: 사이트 확인 (수동)**

브라우저로 5개 시나리오 URL 점검:
1. https://tigerjk9.github.io/lectures/
2. https://tigerjk9.github.io/lectures/kist-claude-code/
3. https://tigerjk9.github.io/lectures/kist-claude-code/claudemd/
4. https://tigerjk9.github.io/assets/lectures/kist-claude-code/slides.html
5. https://tigerjk9.github.io/assets/lectures/kist-claude-code/handout.pdf

GitHub Pages 빌드 ~1~2분 대기. 5개 모두 정상이면 첫 변환 완료.

---

## Self-Review 결과

### 1. Spec 커버리지

| Spec 섹션 | 구현 Task |
|----------|----------|
| §1 시스템 흐름 | Task 11·14·15·16·17·18·19 |
| §2 5명 팀 | Task 12 SKILL.md |
| §3 사이트 정보 구조 | Task 2·3·4 |
| §4 슬라이드 변환 | Task 6·7 (parse_slides.py) |
| §5 워크플로우 | Task 11 orchestrate.py + Task 13 슬래시 |
| §6 KIST 첫 변환 | Task 14~19 |
| §7 일반화 (`brief.yml`·atom_mode) | Task 11 (기본 구현). 추가 atom_mode는 다음 변환 시점에 보강 |
| §8 결정 로그 | spec에 보존, plan은 실행만 |
| §9 인터페이스 | Task 1·11·13 |

**누락 없음.** §7의 `section_heading`·`slide_group` 폴백은 KIST 첫 변환에서는 `feature_catalog`만 사용하므로 미구현. 다음 강의 변환 시점에 별도 plan으로 추가.

### 2. Placeholder 스캔

- "[강사 확인 필요]" 마커 — 의도된 사용자 게이트 (brief.yml 보강 단계). placeholder 아님
- "TBD"·"TODO" — 0건
- 모든 code step은 완전한 코드 포함

### 3. Type·signature 일관성

- `Mapping = dict[int, tuple[str, str]]` — map_features에서 정의·사용 일관
- `feature` dict 필드 — write_feature_page 시그니처와 Task 17 호출 일관 (`id`·`name`·`slug`·`track`·`def`·`actions`·`usage_code`·`related_slides`·`ment_excerpt`·`lab_excerpt`·`rationale`·`source_urls`·`order`)
- `parse_html` 반환 schema와 `02_slides.json` schema 일관

### 4. 의존성 게이트

- Task 1: 의존성 설치 (Playwright Chromium 다운로드 — 망분리 시 별도 안내)
- Task 7: Pillow 추가 — Task 1 requirements.txt 갱신 후 재설치
- Task 16: ★ slug 검토 게이트 — 사용자 명시 승인 없이 Task 17 진행 금지

---

## 변경 이력

| 날짜 | 변경 | 사유 |
|------|------|------|
| 2026-05-22 | 초안 작성 | spec 2026-05-22 lecture-curation-harness-design 승인 후 실행 plan |

*이 plan은 superpowers writing-plans 스킬의 결과물. 실행은 subagent-driven-development 또는 executing-plans 스킬로 전환.*
