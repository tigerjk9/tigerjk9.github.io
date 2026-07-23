#!/usr/bin/env python3
"""GitHub Pages 포스트 -> 네이버 블로그 크로스포스팅 자동화.

네이버 블로그 글쓰기 API는 2020년 종료되어, Playwright로 로그인된 브라우저를
조종해 스마트에디터 ONE에 직접 글을 쓴다.

사용법:
  py scripts/naver_crosspost.py --login          # 최초 1회: 브라우저에서 수동 로그인
  py scripts/naver_crosspost.py --dry-run        # 대상 포스트 + 분류 미리보기
  py scripts/naver_crosspost.py --limit 5        # 미게시 포스트 5편 발행
  py scripts/naver_crosspost.py --post _posts/2026-06-01-foo.md  # 특정 파일만
  py scripts/naver_crosspost.py --no-images      # 이미지 제외(텍스트만)
  py scripts/naver_crosspost.py --no-publish     # 발행 직전까지만 (수동 확인용)

규칙:
- 대상 범위: BASELINE_FILENAME 이후(파일명 사전순) ~ 최신. 주간 다이제스트 제외.
- 카테고리 3곳 자동 분류: 뇌기반 학습 과학(84) > 인공지능교육 인사이트(26)
  > 생각하는 교실, 깊이있는 학습(87). 수동 교정은 naver_category_overrides.json.
- 본문은 마루부리 서체 적용(크기는 에디터 기본 15 유지), 글 끝에 원문 링크 삽입.
- 게시 이력은 naver_crosspost_state.json 에 기록되어 중복 발행 방지.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = ROOT / "_posts"
STATE_FILE = ROOT / "scripts" / "naver_crosspost_state.json"
OVERRIDES_FILE = ROOT / "scripts" / "naver_category_overrides.json"
PROFILE_DIR = ROOT / "scripts" / ".naver_profile"
SHOT_DIR = ROOT / "scripts" / ".naver_shots"

BLOG_ID = "dot_connector"
SITE_URL = "https://tigerjk9.github.io"
BASELINE_FILENAME = "2026-05-14-measuring-ai-ability-to-complete-long-software.md"

# categoryNo는 m.blog.naver.com/api/blogs/dot_connector/category-list 실측 (2026-07-22)
CATEGORIES = {
    "ai": {"no": 26, "name": "인공지능교육 인사이트"},
    "brain": {"no": 84, "name": "뇌기반 학습 과학"},
    "class": {"no": 87, "name": "생각하는 교실, 깊이있는 학습"},
}

BRAIN_SIGNALS = {
    "학습과학", "인지과학", "뇌과학", "신경과학", "메타인지", "자기조절학습",
    "수면", "기억", "뇌", "인지부하", "작업기억", "신경가소성", "소뇌",
}
AI_SIGNALS = {
    "ai", "생성형ai", "llm", "에듀테크", "교육공학", "바이브코딩", "코딩",
    "ai디지털기반교육혁신", "프롬프트엔지니어링", "ai윤리", "머신러닝", "딥러닝",
    "클로드", "claude", "gemini", "챗gpt", "chatgpt", "에이전트", "ai교육",
    "논문리뷰", "개발자", "소프트웨어",
}

FONT_NAME = "마루부리"
FONT_SIZE = "15"

EXCLUDE_TAG = "주간다이제스트"


# ---------------------------------------------------------------- front matter

def parse_post(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        raise ValueError(f"front matter 없음: {path.name}")
    fm_text, body = m.group(1), text[m.end():]

    def _field(name):
        fm = re.search(rf"^{name}:\s*(.+?)\s*$", fm_text, re.MULTILINE)
        return fm.group(1).strip() if fm else ""

    def _list_field(name):
        raw = _field(name)
        if raw.startswith("["):
            return [x.strip().strip("'\"") for x in raw.strip("[]").split(",") if x.strip()]
        # 블록 리스트 (- item)
        items = []
        block = re.search(rf"^{name}:\s*\n((?:\s+-\s+.*\n?)+)", fm_text, re.MULTILINE)
        if block:
            items = [ln.strip().lstrip("-").strip().strip("'\"")
                     for ln in block.group(1).splitlines() if ln.strip().startswith("-")]
        return items

    title = _field("title").strip("'\"")
    permalink = _field("permalink")
    if not permalink:
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", path.stem)
        permalink = f"/post/{slug}/"
    date = path.name[:10]
    return {
        "path": path,
        "file": path.name,
        "title": title,
        "date": date,
        "categories": _list_field("categories"),
        "tags": _list_field("tags"),
        "url": SITE_URL + permalink,
        "body": body,
    }


# ---------------------------------------------------------------- 분류

def classify(post: dict, overrides: dict) -> str:
    if post["file"] in overrides:
        return overrides[post["file"]]
    signals = {s.lower().replace(" ", "") for s in post["categories"] + post["tags"]}
    title_lower = post["title"].lower()
    if signals & BRAIN_SIGNALS:
        return "brain"
    if any(k in title_lower for k in ("뇌", "학습과학", "메타인지", "인지", "수면", "기억")):
        return "brain"
    if signals & AI_SIGNALS:
        return "ai"
    if any(k in title_lower for k in ("ai", "인공지능", "claude", "클로드", "코딩", "llm", "프롬프트")):
        return "ai"
    return "class"


def _load_dotenv():
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


GEMINI_CLASSIFY_PROMPT = """당신은 블로그 글 분류기다. 각 글을 아래 세 카테고리 중 하나로 분류한다.

[brain] 뇌기반 학습 과학 - 뇌과학, 인지과학, 학습과학 연구, 기억, 수면, 인지부하,
  메타인지 등 '사람이 어떻게 배우고 생각하는가'가 글의 중심 주제일 때.
  AI가 소재로 등장해도 핵심 논지가 인지·학습 메커니즘이면 여기로 분류한다.
[ai] 인공지능교육 인사이트 - AI 도구, LLM, 코딩, 에듀테크, AI 정책, AI 활용법과
  그 교육적 시사점이 중심일 때. AI 기술 자체를 다루는 글도 여기.
[class] 생각하는 교실, 깊이있는 학습 - 수업 설계, 평가, 교육과정, 백워드 설계,
  교육철학, 리더십, 학교 문화 등 교육학적 실천이 중심이거나, AI와 인지과학
  어느 쪽도 아닌 일반 주제(심리, 사회, 스포츠, 인문학 등)일 때.

출력 형식: 글마다 한 줄씩 "번호|키" 만 출력한다. 키는 brain, ai, class 중 하나.
설명이나 다른 텍스트는 출력하지 않는다.

분류할 글 목록:
{ITEMS}
"""


def classify_gemini(posts: list[dict]) -> dict:
    """전체 포스트를 Gemini로 일괄 의미 분류 -> {filename: key}."""
    _load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY 미설정 (.env 확인)")
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")

    result = {}
    chunk_size = 50
    for start in range(0, len(posts), chunk_size):
        chunk = posts[start:start + chunk_size]
        items = []
        for i, p in enumerate(chunk):
            excerpt = re.sub(r"<[^>]+>|[#*>\[\]`]|\{%.*?%\}", " ", p["body"])
            excerpt = re.sub(r"\s+", " ", excerpt).strip()[:250]
            items.append(
                f"{i}| 제목: {p['title']} | 카테고리: {','.join(p['categories'])}"
                f" | 태그: {','.join(p['tags'])} | 도입부: {excerpt}"
            )
        prompt = GEMINI_CLASSIFY_PROMPT.replace("{ITEMS}", "\n".join(items))
        res = model.generate_content(prompt)
        text = res.text or ""
        parsed = {}
        for line in text.splitlines():
            m = re.match(r"\s*(\d+)\s*\|\s*(brain|ai|class)\s*$", line.strip())
            if m:
                parsed[int(m.group(1))] = m.group(2)
        for i, p in enumerate(chunk):
            key = parsed.get(i)
            if key is None:
                key = classify(p, {})
                print(f"  [warn] Gemini 응답 누락, 규칙 폴백: {p['file']} -> {key}")
            result[p["file"]] = key
        print(f"  {min(start + chunk_size, len(posts))}/{len(posts)} 분류 완료")
        time.sleep(2)
    return result


# ---------------------------------------------------------------- 변환

def md_to_html(post: dict, include_images: bool) -> str:
    import markdown

    body = post["body"]
    body = re.sub(r"\{%.*?%\}", "", body, flags=re.DOTALL)  # liquid 태그 제거
    html = markdown.markdown(body, extensions=["extra", "sane_lists"])

    # 상대 경로 이미지 -> 절대 URL
    html = html.replace('src="/assets/', f'src="{SITE_URL}/assets/')
    html = html.replace("src='/assets/", f"src='{SITE_URL}/assets/")
    # 상대 경로 내부 링크 -> 절대 URL
    html = re.sub(r'href="/(?!/)', f'href="{SITE_URL}/', html)

    if not include_images:
        html = re.sub(r"<figure\b.*?</figure>", "", html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r"<img\b[^>]*>", "", html, flags=re.IGNORECASE)

    footer = (
        f'<p>원 글 작성일: {post["date"]}<br>'
        f'원문(개인 블로그): <a href="{post["url"]}">{post["url"]}</a></p>'
    )
    html = html + footer

    # 본문 텍스트를 에디터 크기 15로 매핑 (인라인 font-size가 se-fs15로 변환됨,
    # 소제목 h2/h3는 건드리지 않아 19 등 큰 크기 유지 - 2026-07-22 실측)
    html = re.sub(r"<(p|li|td|th)(\s[^>]*)?>",
                  lambda m: f'<{m.group(1)}{m.group(2) or ""} style="font-size:15px">',
                  html)

    # 가독성: 블록 요소 사이에 빈 줄 삽입. 네이버 에디터는 문단 여백이 없어
    # 그대로 붙여넣으면 벽글이 된다. 소제목(h2/h3) 앞에도 빈 줄이 생기고,
    # 소제목 '뒤'는 본문과 밀착되도록 닫는 태그 목록에서 헤딩을 제외한다.
    gap = '<p style="font-size:15px"><br></p>'
    block_close = r"</(?:p|ul|ol|table|blockquote|figure|pre)>"
    block_open = r"<(?:p|ul|ol|table|blockquote|figure|pre|h[1-6])\b"
    html = re.sub(rf"({block_close})\s*({block_open})", rf"\1{gap}\2", html)
    return html


def html_to_text(html: str) -> str:
    text = re.sub(r"<br\s*/?>", "\n", html)
    text = re.sub(r"</(p|h[1-6]|li|tr|figure|blockquote)>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


# ---------------------------------------------------------------- 상태

def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def collect_pending(state: dict, only_file: str | None = None) -> list[dict]:
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        if only_file:
            if path.name != Path(only_file).name:
                continue
        elif path.name <= BASELINE_FILENAME:
            continue
        if path.name in state["posted"]:
            if not only_file:
                continue
        try:
            post = parse_post(path)
        except ValueError as e:
            print(f"  [skip] {e}")
            continue
        if EXCLUDE_TAG in post["tags"] or "weekly-digest" in path.name:
            continue
        posts.append(post)
    return posts


# ---------------------------------------------------------------- 브라우저

COOKIE_FILE = PROFILE_DIR / "cookies.json"


def save_cookies(ctx):
    """NID_AUT 등 세션 쿠키는 브라우저 종료 시 폐기되므로 파일로 백업한다.

    로그아웃 상태(NID_AUT 부재)면 기존 백업을 덮어쓰지 않는다 —
    실패한 실행이 마지막 정상 백업을 파괴하는 것을 방지.
    """
    try:
        cookies = ctx.cookies()
        if not any(c["name"] == "NID_AUT" for c in cookies):
            print("  [warn] NID_AUT 없음 — 쿠키 백업 건너뜀 (기존 백업 보존)")
            return
        COOKIE_FILE.write_text(
            json.dumps(cookies, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print(f"  [warn] 쿠키 백업 실패: {e}")


def restore_cookies(ctx):
    if not COOKIE_FILE.exists():
        return
    try:
        ctx.add_cookies(json.loads(COOKIE_FILE.read_text(encoding="utf-8")))
    except Exception as e:
        print(f"  [warn] 쿠키 복원 실패: {e}")


def launch(playwright, headless=False):
    PROFILE_DIR.mkdir(exist_ok=True)
    args = ["--disable-blink-features=AutomationControlled"]
    try:
        ctx = playwright.chromium.launch_persistent_context(
            str(PROFILE_DIR), channel="msedge", headless=headless, args=args,
            viewport={"width": 1400, "height": 900}, locale="ko-KR",
        )
    except Exception:
        ctx = playwright.chromium.launch_persistent_context(
            str(PROFILE_DIR), headless=headless, args=args,
            viewport={"width": 1400, "height": 900}, locale="ko-KR",
        )
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        ctx.grant_permissions(["clipboard-read", "clipboard-write"],
                              origin="https://blog.naver.com")
    except Exception:
        pass
    restore_cookies(ctx)
    return ctx


def is_logged_in(ctx) -> bool:
    return any(c["name"] == "NID_AUT" for c in ctx.cookies("https://naver.com"))


def verify_login(page) -> bool:
    """서버 기준 세션 유효성 확인. 쿠키가 있어도 서버가 만료시켰으면 무효.

    만료 세션으로 postwrite에 진입하면 nidlogin.login으로 리다이렉트되고,
    유효하면 에디터 URL에 머무른다 (2026-07-23 양방향 실측).
    nidlogin.login 직접 방문은 로그인 상태와 무관하게 폼에 머물러 판별 불가.
    """
    try:
        page.goto(f"https://blog.naver.com/{BLOG_ID}/postwrite",
                  wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(3000)
        return "nidlogin" not in page.url
    except Exception as e:
        print(f"  [warn] 세션 검증 실패: {e}")
        return False


def do_login(ctx):
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://nid.naver.com/nidlogin.login?url=https://blog.naver.com/" + BLOG_ID)
    try:
        page.check("#keep", timeout=5000)  # 로그인 상태 유지 — 세션 수명 연장의 핵심
        print("'로그인 상태 유지'를 자동 체크했습니다.")
    except Exception:
        try:
            # 스타일 스위치가 input을 가려 가시성 검사에 걸리면 JS로 직접 토글
            page.eval_on_selector("#keep", "el => { if (!el.checked) el.click() }")
            print("'로그인 상태 유지'를 자동 체크했습니다 (JS).")
        except Exception:
            print("'로그인 상태 유지' 자동 체크 실패 — 브라우저에서 직접 체크해 주세요.")
    print("브라우저에서 네이버 로그인을 완료해 주세요 (로그인 상태 유지 체크 권장).")
    print("로그인이 감지되면 자동으로 종료됩니다. 최대 5분 대기...")
    for _ in range(150):
        time.sleep(2)
        if is_logged_in(ctx):
            save_cookies(ctx)
            print("로그인 확인 완료. 쿠키가 저장되었습니다.")
            time.sleep(2)
            return True
    print("로그인이 감지되지 않았습니다. 다시 시도해 주세요.")
    return False


# ---------------------------------------------------------------- 에디터 조작

def shot(page, name):
    try:
        SHOT_DIR.mkdir(exist_ok=True)
        page.screenshot(path=str(SHOT_DIR / f"{name}.png"))
    except Exception:
        pass


def dismiss_popups(page):
    """작성 중인 글 이어쓰기 팝업, 도움말 패널 등 정리."""
    for sel, label in [
        (".se-popup-button-cancel", None),          # 이어쓰기 팝업 -> 취소(새 글)
        (".se-help-panel-close-button", None),
        ("button.se-popup-close-button", None),
    ]:
        try:
            btn = page.locator(sel).first
            if btn.is_visible(timeout=1500):
                btn.click()
                time.sleep(0.5)
        except Exception:
            pass


def paste_html(page, html: str, plain: str) -> bool:
    """클립보드에 HTML을 싣고 Ctrl+V. 실패 시 합성 paste 이벤트 폴백."""
    try:
        page.evaluate(
            """async ({html, plain}) => {
                const item = new ClipboardItem({
                    'text/html': new Blob([html], {type: 'text/html'}),
                    'text/plain': new Blob([plain], {type: 'text/plain'}),
                });
                await navigator.clipboard.write([item]);
            }""",
            {"html": html, "plain": plain},
        )
        page.keyboard.press("Control+v")
        return True
    except Exception as e:
        print(f"  clipboard write 실패({e}); 합성 paste 이벤트로 폴백")
    try:
        page.evaluate(
            """({html, plain}) => {
                const dt = new DataTransfer();
                dt.setData('text/html', html);
                dt.setData('text/plain', plain);
                const ev = new ClipboardEvent('paste',
                    {clipboardData: dt, bubbles: true, cancelable: true});
                document.activeElement.dispatchEvent(ev);
            }""",
            {"html": html, "plain": plain},
        )
        return True
    except Exception as e:
        print(f"  합성 paste도 실패: {e}")
        return False


def apply_font(page):
    """본문 전체 선택 후 서체를 마루부리로 변경. 크기는 요소별로 보존된다.

    셀렉터는 2026-07-22 실측: 고정 툴바 서체 버튼은
    button.se-font-family-toolbar-button[data-group='propertyToolbar'],
    드롭다운 항목은 button.se-toolbar-option-text-button (innerText '마루부리').
    """
    try:
        page.keyboard.press("Control+a")
        time.sleep(0.5)
        btn = page.locator(
            "button.se-font-family-toolbar-button[data-group='propertyToolbar']")
        label = (btn.inner_text() or "").strip()
        if FONT_NAME not in label:
            btn.click()
            time.sleep(0.8)
            page.locator(
                f"button.se-toolbar-option-text-button:has-text('{FONT_NAME}')"
            ).first.click()
            time.sleep(0.8)
            label = (btn.inner_text() or "").strip()
        page.keyboard.press("End")  # 선택 해제
        if FONT_NAME in label:
            return True
        print(f"  [warn] 서체 적용 확인 실패 (라벨: {label!r})")
        return False
    except Exception as e:
        print(f"  [warn] 서체 적용 실패: {e}. 에디터 기본 서체 설정에 의존합니다.")
        return False


def write_post(page, post: dict, cat_key: str, html: str, tags: list[str],
               publish: bool, debug: bool) -> str | None:
    cat = CATEGORIES[cat_key]
    page.goto(f"https://blog.naver.com/{BLOG_ID}/postwrite?categoryNo={cat['no']}",
              wait_until="domcontentloaded")
    page.wait_for_selector(".se-content, .se-component", timeout=30000)
    time.sleep(2)
    dismiss_popups(page)
    if debug:
        shot(page, f"{post['path'].stem}-01-editor")

    # 제목
    title_area = page.locator(".se-section-documentTitle .se-text-paragraph, "
                              ".se-documentTitle .se-text-paragraph").first
    title_area.click()
    time.sleep(0.3)
    page.keyboard.insert_text(post["title"])
    time.sleep(0.3)

    # 본문으로 이동 후 붙여넣기
    body_area = page.locator(".se-component.se-text .se-text-paragraph").last
    body_area.click()
    time.sleep(0.3)
    if not paste_html(page, html, html_to_text(html)):
        raise RuntimeError("본문 붙여넣기 실패")
    time.sleep(3)

    # 외부 이미지 업로드 대기 (있다면)
    for _ in range(20):
        loading = page.locator("[class*='se-image'][class*='loading'], .se-uploading").count()
        if loading == 0:
            break
        time.sleep(1)

    apply_font(page)
    if debug:
        shot(page, f"{post['path'].stem}-02-pasted")

    if not publish:
        print("  --no-publish: 발행 직전 상태로 중단(브라우저에서 직접 확인 후 발행하세요).")
        return None

    # 발행 팝업 열기 (셀렉터 2026-07-22 실측: publish_btn__/selectbox_button__/confirm_btn__)
    page.locator("button[class*='publish_btn']").first.click()
    time.sleep(1.5)
    if debug:
        shot(page, f"{post['path'].stem}-03-publish-popup")

    # 카테고리 확인 - URL categoryNo로 이미 선택돼 있어야 정상
    try:
        sel_label = page.locator("button[class*='selectbox_button']").first.inner_text()
        if cat["name"] not in sel_label:
            print(f"  [warn] 팝업 카테고리 불일치({sel_label!r}), 직접 선택 시도")
            page.locator("button[class*='selectbox_button']").first.click()
            time.sleep(0.7)
            page.locator(f"label:has-text('{cat['name']}'), "
                         f"span:has-text('{cat['name']}')").last.click()
            time.sleep(0.5)
    except Exception as e:
        print(f"  [warn] 카테고리 확인/선택 실패: {e}")

    # 태그 입력 (최대 5개)
    try:
        tag_input = page.locator("input[placeholder*='태그']").first
        if tag_input.is_visible(timeout=2000):
            for t in tags[:5]:
                tag_input.click()
                page.keyboard.insert_text(t.replace(" ", ""))
                page.keyboard.press("Enter")
                time.sleep(0.3)
    except Exception:
        pass

    # 최종 발행
    page.locator("button[class*='confirm_btn']").first.click()

    # 발행 완료 -> 글 URL로 이동 대기. 발행 후 블로그 홈으로 이동하는 경우가 많아
    # (URL에 logNo 없음, 2026-07-22 실측) 짧게 기다린 뒤 API 폴백으로 넘어간다.
    for _ in range(10):
        time.sleep(1)
        url = page.url
        m = (re.search(rf"blog\.naver\.com/{BLOG_ID}/(\d+)", url)
             or re.search(r"logNo=(\d+)", url))
        if m:
            return f"https://blog.naver.com/{BLOG_ID}/{m.group(1)}"
    # 폴백: 모바일 API에서 제목 대조로 logNo 찾기
    time.sleep(3)
    logno = fetch_logno_by_title(post["title"])
    if logno:
        return f"https://blog.naver.com/{BLOG_ID}/{logno}"
    print("  [warn] 발행 후 URL을 확인하지 못했습니다. 블로그에서 직접 확인 필요.")
    if debug:
        shot(page, f"{post['path'].stem}-04-after-publish")
    return None


def _norm_title(s: str) -> str:
    import unicodedata
    s = "".join(ch for ch in (s or "") if not 0xD800 <= ord(ch) <= 0xDFFF)
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"[\s'\"‘’“”]+", "", s)


def fetch_logno_by_title(title: str) -> str | None:
    """발행 직후 브라우저가 블로그 홈으로 이동해 URL에 logNo가 없는 경우의 폴백.

    모바일 공개 API에서 최신 글 목록을 받아 제목 앞부분을 대조한다.
    """
    import ssl
    import urllib.request
    try:
        req = urllib.request.Request(
            f"https://m.blog.naver.com/api/blogs/{BLOG_ID}/post-list"
            "?categoryNo=0&itemCount=10&pageNo=1",
            headers={
                "User-Agent": ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                               "AppleWebKit/605.1.15"),
                "Referer": f"https://m.blog.naver.com/{BLOG_ID}",
            })
        raw = urllib.request.urlopen(
            req, context=ssl._create_unverified_context(), timeout=15).read()
        data = json.loads(raw.decode("utf-8", errors="replace"))
        want = _norm_title(title)[:20]
        for it in data.get("result", {}).get("items", []):
            t = it.get("titleWithInspectMessage") or it.get("title") or ""
            if _norm_title(t)[:20] == want:
                return str(it.get("logNo"))
    except Exception as e:
        print(f"  [warn] logNo 조회 실패: {e}")
    return None


def update_post(page, logno: str, html: str, debug: bool) -> str | None:
    """기존 발행 글의 본문만 교체 (제목·카테고리·태그는 유지).

    편집 URL postwrite?logNo=N 로 진입, 본문 Ctrl+A -> Delete -> 재붙여넣기.
    Ctrl+A는 본문 컴포넌트에만 적용되어 제목은 건드리지 않는다(2026-07-22 실측).
    """
    page.goto(f"https://blog.naver.com/{BLOG_ID}/postwrite?logNo={logno}",
              wait_until="domcontentloaded")
    page.wait_for_selector(".se-content, .se-component", timeout=30000)
    time.sleep(3)
    dismiss_popups(page)

    body_area = page.locator(".se-component.se-text .se-text-paragraph").first
    body_area.click()
    time.sleep(0.3)
    # 기존 본문이 로드됐는지 확인 (빈 에디터면 잘못된 logNo)
    text_len = page.evaluate(
        "() => (document.querySelector('.se-content')?.innerText || '').length")
    if text_len < 100:
        raise RuntimeError(f"편집 대상 본문이 비어 있음 (logNo={logno} 확인 필요)")

    page.keyboard.press("Control+a")
    time.sleep(0.5)
    page.keyboard.press("Delete")
    time.sleep(1)
    if not paste_html(page, html, html_to_text(html)):
        raise RuntimeError("본문 붙여넣기 실패")
    time.sleep(3)
    for _ in range(20):
        if page.locator("[class*='se-image'][class*='loading'], .se-uploading").count() == 0:
            break
        time.sleep(1)
    apply_font(page)
    if debug:
        shot(page, f"update-{logno}-pasted")

    page.locator("button[class*='publish_btn']").first.click()
    time.sleep(1.5)
    if debug:
        shot(page, f"update-{logno}-popup")
    page.locator("button[class*='confirm_btn']").first.click()

    for _ in range(30):
        time.sleep(1)
        m = (re.search(rf"blog\.naver\.com/{BLOG_ID}/(\d+)", page.url)
             or re.search(r"logNo=(\d+)", page.url))
        if m:
            return f"https://blog.naver.com/{BLOG_ID}/{m.group(1)}"
    print("  [warn] 수정 발행 후 URL 전환 미확인. 블로그에서 직접 확인 필요.")
    return None


# ---------------------------------------------------------------- 메인

def main():
    ap = argparse.ArgumentParser(description="GitHub 블로그 -> 네이버 블로그 크로스포스팅")
    ap.add_argument("--login", action="store_true", help="최초 1회 수동 로그인")
    ap.add_argument("--dry-run", action="store_true", help="대상 목록/분류 미리보기")
    ap.add_argument("--classify-gemini", action="store_true",
                    help="전체 대상 포스트를 Gemini로 일괄 분류해 overrides 파일에 저장")
    ap.add_argument("--limit", type=int, default=5, help="이번 실행 최대 발행 수 (기본 5)")
    ap.add_argument("--post", help="특정 포스트 파일만 발행 (이미 게시된 글도 재발행)")
    ap.add_argument("--update", metavar="LOGNO",
                    help="기존 네이버 글의 본문을 교체 (--post와 함께 사용, 제목·카테고리 유지)")
    ap.add_argument("--category", choices=list(CATEGORIES), help="분류 수동 지정")
    ap.add_argument("--no-images", action="store_true", help="이미지 제외")
    ap.add_argument("--no-publish", action="store_true", help="발행 직전까지만 진행")
    ap.add_argument("--no-tags", action="store_true", help="태그 입력 생략")
    ap.add_argument("--debug", action="store_true", help="단계별 스크린샷 저장")
    ap.add_argument("--min-wait", type=int, default=45)
    ap.add_argument("--max-wait", type=int, default=90)
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

    print(f"\n=== 실행 {time.strftime('%Y-%m-%d %H:%M:%S')} ===")

    state = load_json(STATE_FILE, {"posted": {}})
    overrides = load_json(OVERRIDES_FILE, {})
    pending = collect_pending(state, args.post)

    if args.classify_gemini:
        print(f"Gemini 일괄 분류 시작: {len(pending)}편")
        mapping = classify_gemini(pending)
        merged = {**mapping, **overrides}  # 수동 교정이 있으면 그것을 우선
        save_json(OVERRIDES_FILE, merged)
        counts = {}
        for v in merged.values():
            counts[v] = counts.get(v, 0) + 1
        print(f"저장: {OVERRIDES_FILE.name}")
        for k, v in counts.items():
            print(f"  {CATEGORIES[k]['name']}: {v}편")
        return

    if args.dry_run:
        counts = {}
        print(f"대상 {len(pending)}편 (기준: {BASELINE_FILENAME} 이후, 게시 이력 제외)\n")
        for p in pending:
            key = args.category or classify(p, overrides)
            counts[key] = counts.get(key, 0) + 1
            print(f"  [{CATEGORIES[key]['name']}] {p['file']}")
            print(f"      {p['title']}")
        print("\n분류 요약:")
        for k, v in counts.items():
            print(f"  {CATEGORIES[k]['name']}: {v}편")
        return

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        ctx = launch(pw)
        try:
            if args.login:
                do_login(ctx)
                return
            if not is_logged_in(ctx):
                print("로그인 쿠키가 없습니다. 먼저 실행: py scripts/naver_crosspost.py --login")
                raise SystemExit(2)

            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            if not verify_login(page):
                print("[EXPIRED] 네이버 세션 만료 — 쿠키는 있으나 서버가 거부했습니다.")
                print("조치: py scripts/naver_crosspost.py --login  (로그인 상태 유지 자동 체크됨)")
                raise SystemExit(2)

            if args.update:
                if not args.post or not pending:
                    print("--update는 --post <파일>과 함께 사용합니다.")
                    return
                post = pending[0]
                html = md_to_html(post, include_images=not args.no_images)
                page = ctx.pages[0] if ctx.pages else ctx.new_page()
                url = update_post(page, args.update, html, args.debug)
                print(f"[OK] 본문 교체 완료: {url or '(URL 미확인)'}")
                save_cookies(ctx)
                return

            if not pending:
                print("발행할 포스트가 없습니다.")
                return

            batch = pending[: args.limit]
            print(f"이번 실행 발행 예정: {len(batch)}편 (전체 잔여 {len(pending)}편)")
            page = ctx.pages[0] if ctx.pages else ctx.new_page()

            for i, post in enumerate(batch):
                cat_key = args.category or classify(post, overrides)
                cat_name = CATEGORIES[cat_key]["name"]
                print(f"\n[{i+1}/{len(batch)}] {post['file']} -> {cat_name}")
                html = md_to_html(post, include_images=not args.no_images)
                try:
                    url = write_post(page, post, cat_key, html,
                                     [] if args.no_tags else post["tags"],
                                     publish=not args.no_publish, debug=args.debug)
                except Exception as e:
                    shot(page, f"{post['path'].stem}-error")
                    print(f"  [FAIL] {e}")
                    print(f"  스크린샷: {SHOT_DIR}")
                    break
                if args.no_publish:
                    print("검수 모드: 브라우저 창을 직접 닫으면 종료됩니다.")
                    try:
                        while ctx.pages:
                            time.sleep(2)
                    except Exception:
                        pass
                    break
                state["posted"][post["file"]] = {
                    "url": url or "unknown", "category": cat_name,
                    "posted_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                }
                save_json(STATE_FILE, state)
                print(f"  [OK] {url or '(URL 미확인)'}")
                if i < len(batch) - 1:
                    wait = random.randint(args.min_wait, args.max_wait)
                    print(f"  다음 글까지 {wait}초 대기...")
                    time.sleep(wait)
            save_cookies(ctx)  # 세션 쿠키 갱신분 백업
        finally:
            try:
                ctx.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
