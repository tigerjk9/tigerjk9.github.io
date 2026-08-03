#!/usr/bin/env python3
"""GitHub Pages 포스트 -> 네이버 블로그 크로스포스팅 자동화.

네이버 블로그 글쓰기 API는 2020년 종료되어, Playwright로 로그인된 브라우저를
조종해 스마트에디터 ONE에 직접 글을 쓴다.

사용법:
  py scripts/naver_crosspost.py --login          # 브라우저에서 수동 로그인(쿠키 갱신)
  py scripts/naver_crosspost.py --check-session  # 세션 유효성만 확인 (유효 0 / 만료 2)
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
- 세션이 만료돼 있으면 발행 실행이 그 자리에서 로그인 창을 띄워 복구한 뒤 이어서
  발행한다(--no-auto-login으로 끔. 스케줄러는 이 플래그로 즉시 종료).
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

# '로그인 상태 유지' 체크박스. 네이버가 id를 바꿔도 버티도록 후보를 순회한다
# (2026-07-26 실측: #keep -> #loginStay, name=nvlong).
KEEP_SELECTORS = ("#loginStay", "input[name='nvlong']", ".input_stay", "#keep")
LOGIN_WAIT_SEC = 300
# 네이버 세션은 약 30일 고정 만료(사용해도 연장 안 됨) — 남은 기간이 이 값 이하면 경고
EXPIRY_WARN_DAYS = 7

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


# ---------------------------------------------------------------- 게시 이력 동기화
#
# 2026-08-03 사고: 게시 이력이 커밋되지 않은 채 스케줄 실행이 돌아, 원격에만 기록된
# 20편을 미게시로 판단해 네이버에 중복 발행했다. 이력 파일이 곧 중복 방지 장치이므로
# 실행 전에 원격과 합치고, 실행 후에 결과를 되돌려 놓아야 장치가 성립한다.
# 네트워크·인증 문제로 동기화가 실패해도 발행 자체는 계속한다(경고만).

def _git(*args, timeout: int = 60):
    import subprocess
    return subprocess.run(["git", *args], cwd=str(ROOT), capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)


def _git_ok() -> bool:
    try:
        return _git("rev-parse", "--git-dir").returncode == 0
    except Exception:
        return False


def merge_state(base: dict, other: dict) -> "tuple[dict, int, int]":
    """두 이력을 합친다. 같은 글이 양쪽에 있으면 posted_at 이 늦은 쪽을 남긴다.

    반환: (합친 이력, other 에만 있던 건수, 서로 다르게 기록된 건수)
    """
    merged = dict(base.get("posted", {}))
    added = conflicts = 0
    for k, v in other.get("posted", {}).items():
        if k not in merged:
            merged[k] = v
            added += 1
        elif merged[k] != v:
            conflicts += 1
            if str(v.get("posted_at", "")) > str(merged[k].get("posted_at", "")):
                merged[k] = v
    return {"posted": merged}, added, conflicts


def sync_state_before_run(state: dict) -> dict:
    """원격 이력을 끌어와 로컬에 합친다. 원격에만 있는 발행분을 미게시로 오인하지 않도록."""
    if not _git_ok():
        print("[WARN] git 저장소가 아닙니다 - 이력 동기화를 건너뜁니다")
        return state
    try:
        r = _git("fetch", "origin", "--quiet", timeout=120)
        if r.returncode != 0:
            print(f"[WARN] git fetch 실패 - 이력 동기화 건너뜀: {r.stderr.strip()[:200]}")
            return state
        rel = STATE_FILE.relative_to(ROOT).as_posix()
        show = _git("show", f"origin/main:{rel}")
        if show.returncode != 0:
            print("[WARN] 원격 이력을 읽지 못했습니다 - 동기화 건너뜀")
            return state
        remote = json.loads(show.stdout)
    except Exception as e:
        print(f"[WARN] 이력 동기화 실패 - 로컬 이력으로 진행: {e}")
        return state

    merged, added, conflicts = merge_state(state, remote)
    if added or conflicts:
        save_json(STATE_FILE, merged)
        print(f"[SYNC] 원격 이력 반영: 신규 {added}건, 시각 갱신 {conflicts}건 "
              f"(총 {len(merged['posted'])}편)")
        if conflicts:
            print("       같은 글이 양쪽에 다르게 기록돼 있습니다 - 중복 발행 가능성을 확인하세요")
    return merged


def push_state(note: str) -> None:
    """이력 파일만 커밋·푸시한다. 다른 작업 중인 변경은 건드리지 않는다."""
    if not _git_ok():
        return
    rel = STATE_FILE.relative_to(ROOT).as_posix()
    try:
        if not _git("status", "--porcelain", "--", rel).stdout.strip():
            return
        if _git("add", "--", rel).returncode != 0:
            print("[WARN] 이력 stage 실패")
            return
        msg = f"chore: 네이버 크로스포스팅 게시 이력 갱신 ({note})"
        if _git("commit", "-m", msg, "--", rel).returncode != 0:
            print("[WARN] 이력 커밋 실패")
            return
        # 다른 커밋이 원격에 먼저 올라와 있어도 이력 커밋만 얹어 올린다.
        # --autostash 는 작업 중인 다른 파일을 잠시 치워 rebase 가 멈추지 않게 한다.
        _git("fetch", "origin", "--quiet", timeout=120)
        rb = _git("rebase", "origin/main", "--autostash", timeout=180)
        if rb.returncode != 0:
            _git("rebase", "--abort")
            print("[WARN] rebase 충돌 - 이력은 로컬에 커밋됨. 수동으로 push 하세요")
            return
        pu = _git("push", "origin", "HEAD:main", timeout=180)
        if pu.returncode != 0:
            print(f"[WARN] 이력 push 실패 (로컬 커밋은 남음): {pu.stderr.strip()[:200]}")
            return
        print(f"[SYNC] 게시 이력 push 완료 ({note})")
    except Exception as e:
        print(f"[WARN] 이력 push 실패: {e}")


def recent_post_count(state: dict, hours: int = 24) -> int:
    """최근 N시간 발행 수. 수동 실행과 스케줄 실행이 겹쳐 과발행되는 것을 막는다."""
    cutoff = time.time() - hours * 3600
    n = 0
    for v in state.get("posted", {}).values():
        stamp = v.get("posted_at")
        if not stamp:
            continue
        try:
            t = time.mktime(time.strptime(stamp, "%Y-%m-%d %H:%M:%S"))
        except Exception:
            continue
        if t >= cutoff:
            n += 1
    return n


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
        cookies = json.loads(COOKIE_FILE.read_text(encoding="utf-8"))
        # 만료 시각이 지난 쿠키는 복원해도 즉시 폐기된다. 걸러서 넣어야
        # ctx.cookies() 결과가 '지금 실제로 유효한 것'만 담긴다.
        now = time.time()
        fresh = [c for c in cookies
                 if not isinstance(c.get("expires"), (int, float))
                 or c["expires"] <= 0 or c["expires"] > now]
        ctx.add_cookies(fresh)
    except Exception as e:
        print(f"  [warn] 쿠키 복원 실패: {e}")


def launch(playwright, headless=False):
    """브라우저 실행. '지원되지 않는 명령줄 플래그' 경고 배너를 띄우지 않는다.

    2026-07-26 실측(chrome://version 명령줄 확인): 경고 대상 플래그가 둘이었다.
    ① 직접 넘기던 --disable-blink-features=AutomationControlled — 제거해도
       아래 add_init_script만으로 navigator.webdriver가 undefined로 유지된다.
    ② Playwright 기본값 --no-sandbox — chromium_sandbox=True로 끈다.
    둘 다 없애면 위험 플래그가 0개가 되어 배너가 뜨지 않는다. 샌드박스가 막힌
    환경도 있으니 msedge/기본, 샌드박스 on/off 순으로 폴백한다.
    """
    PROFILE_DIR.mkdir(exist_ok=True)
    last = None
    for extra in ({"channel": "msedge", "chromium_sandbox": True},
                  {"channel": "msedge", "chromium_sandbox": False},
                  {"chromium_sandbox": True},
                  {"chromium_sandbox": False}):
        try:
            ctx = playwright.chromium.launch_persistent_context(
                str(PROFILE_DIR), headless=headless, args=[],
                viewport={"width": 1400, "height": 900}, locale="ko-KR", **extra)
            break
        except Exception as e:
            last = e
    else:
        raise last
    ctx.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    try:
        ctx.grant_permissions(["clipboard-read", "clipboard-write"],
                              origin="https://blog.naver.com")
    except Exception:
        pass
    restore_cookies(ctx)
    return ctx


def _nid_aut(ctx) -> str:
    for c in ctx.cookies("https://naver.com"):
        if c["name"] == "NID_AUT":
            return c.get("value") or ""
    return ""


def is_logged_in(ctx) -> bool:
    """쿠키 존재 여부만 본다 — 서버측 유효성은 verify_login이 판정한다."""
    return bool(_nid_aut(ctx))


def _browser_gone(exc) -> bool:
    msg = str(exc).lower()
    return any(s in msg for s in ("closed", "crashed", "disconnected", "target page"))


def session_days_left(ctx):
    """NID_AUT 만료까지 남은 일수. 세션 쿠키·부재면 None."""
    for c in ctx.cookies("https://naver.com"):
        if c["name"] == "NID_AUT":
            exp = c.get("expires", -1)
            if isinstance(exp, (int, float)) and exp > 0:
                return (exp - time.time()) / 86400
            return None
    return None


def report_session(ctx):
    """NID_AUT 수명을 알려 준다. 세션 쿠키면 '로그인 상태 유지' 미적용 신호.

    네이버 '로그인 상태 유지'는 발급 시점 기준 약 30일 고정이다(2026-07-26 실측).
    사용해도 만료가 밀리지 않고(sliding 아님), 로그인 URL 재방문으로도 재발급되지
    않는다. 즉 30일에 한 번은 사람이 자격증명으로 다시 로그인해야 한다.
    """
    for c in ctx.cookies("https://naver.com"):
        if c["name"] != "NID_AUT":
            continue
        exp = c.get("expires", -1)
        if isinstance(exp, (int, float)) and exp > 0:
            days = (exp - time.time()) / 86400
            print("  세션 만료 예정: "
                  + time.strftime("%Y-%m-%d %H:%M", time.localtime(exp))
                  + f" (D-{days:.0f}, 로그인 상태 유지 적용됨)")
        else:
            print("  [note] NID_AUT가 세션 쿠키로 발급됨 — 브라우저를 닫으면 폐기되므로 "
                  "백업 파일에 의존한다. 서버 세션도 하루 안에 만료될 수 있음.")
        return
    print("  [note] NID_AUT 없음 (로그아웃 상태)")


def warn_if_expiring(ctx):
    """만료 임박 경고. 스케줄 실행은 --no-auto-login이라 만료되면 조용히 멈추므로,
    그 전에 로그에 눈에 띄게 남겨 사용자가 미리 갱신하게 한다."""
    days = session_days_left(ctx)
    if days is None or days > EXPIRY_WARN_DAYS:
        return
    print("!" * 62)
    print(f"[세션 만료 임박] 남은 기간 D-{days:.0f}. 만료되면 자동 발행이 멈춥니다.")
    print("  지금 갱신: py scripts/naver_crosspost.py --force-login")
    print("!" * 62)


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


def apply_keep_login(page) -> bool:
    """'로그인 상태 유지'를 체크한다. 미체크면 세션 쿠키라 하루 안에 만료된다.

    2026-07-26 실측: 체크박스 id가 #keep -> #loginStay(name=nvlong)로 바뀌었다.
    구 셀렉터만 보던 코드는 매 로그인마다 조용히 실패했고(예외를 통째로 삼킴),
    그 결과 모든 로그인이 '상태 유지 없음'으로 성립해 다음 날 [EXPIRED]가 반복됐다.
    셀렉터가 또 바뀔 수 있으므로 후보를 순회하고, 실패는 크게 경고한다.
    """
    for sel in KEEP_SELECTORS:
        try:
            # 이미 체크돼 있으면 건드리지 않아 수동 체크를 되돌리지 않는다
            if page.eval_on_selector(
                    sel, "el => { if (!el.checked) el.click(); return !!el.checked; }"):
                return True
        except Exception:
            continue  # 폼 미로딩 / 셀렉터 부재 — 다음 후보, 다음 루프 재시도
    return False


def do_login(ctx, page=None, check_existing=True) -> bool:
    """브라우저에서 사람이 로그인할 때까지 기다린 뒤 쿠키를 백업한다.

    만료된 백업 쿠키가 복원돼 있어도 '이미 로그인됨'으로 오판하지 않도록,
    시작 시점의 NID_AUT 값과 달라졌을 때만 로그인 성립으로 본다.
    (구버전은 쿠키 이름 존재만 확인해, 만료 쿠키가 남아 있으면 사용자가
     입력하기도 전에 성공 처리하고 창을 닫아 버렸다.)

    check_existing=False면 이미 세션 검증을 마친 호출자(ensure_session)를 위해
    중복 검증을 생략한다.
    """
    page = page or (ctx.pages[0] if ctx.pages else ctx.new_page())

    # 세션이 아직 살아 있으면 재로그인 없이 백업만 갱신한다.
    # (없으면 유효 세션에서 --login 실행 시 5분을 헛기다린다)
    if check_existing and is_logged_in(ctx) and verify_login(page):
        save_cookies(ctx)
        print("이미 유효한 세션입니다. 쿠키 백업만 갱신했습니다.")
        report_session(ctx)
        return True

    before = _nid_aut(ctx)
    try:
        page.goto("https://nid.naver.com/nidlogin.login?url=https://blog.naver.com/" + BLOG_ID,
                  wait_until="domcontentloaded", timeout=60000)
    except Exception as e:
        print(f"  [warn] 로그인 페이지 이동 실패: {e}")

    print("-" * 62)
    print("브라우저 창에서 네이버 로그인을 완료해 주세요.")
    print("  · '로그인 상태 유지'는 자동으로 체크됩니다 (세션 수명 연장의 핵심)")
    print("  · 2단계 인증·새 기기 등록 화면이 뜨면 끝까지 진행해 주세요")
    print("  · 창을 직접 닫지 마세요. 로그인이 감지되면 자동으로 진행됩니다")
    wait_label = (f"{LOGIN_WAIT_SEC // 60}분" if LOGIN_WAIT_SEC >= 60
                  else f"{LOGIN_WAIT_SEC}초")
    print(f"최대 {wait_label} 대기...")
    print("-" * 62)

    keep_ok = False
    deadline = time.time() + LOGIN_WAIT_SEC
    while time.time() < deadline:
        try:
            if not keep_ok and apply_keep_login(page):
                keep_ok = True
                print("  '로그인 상태 유지'를 자동 체크했습니다.")
            now = _nid_aut(ctx)
            if now and now != before:
                break
        except Exception as e:
            if _browser_gone(e):
                print("  [FAIL] 브라우저 창이 닫혔습니다. 다시 실행해 주세요.")
                return False
        time.sleep(2)
    else:
        print(f"  [FAIL] {wait_label} 안에 로그인이 감지되지 않았습니다.")
        return False

    print("  로그인 감지됨. 리다이렉트·세션 확정 대기...")
    try:
        page.wait_for_timeout(4000)
    except Exception:
        pass
    if not keep_ok:
        print("  [warn] '로그인 상태 유지' 자동 체크 실패 — 세션이 하루 안에 만료될 수 "
              "있습니다. 다음 로그인 때 브라우저에서 직접 체크해 주세요.")
    if not verify_login(page):
        print("  [FAIL] 로그인은 됐으나 서버 세션 검증에 실패했습니다.")
        print("        (2단계 인증·기기 등록이 남아 있을 수 있음. 완료 후 재시도)")
        return False
    save_cookies(ctx)
    print("  로그인 확인 완료. 쿠키를 백업했습니다.")
    report_session(ctx)
    return True


def ensure_session(ctx, page, allow_login: bool) -> bool:
    """발행 전 세션 보장. 쿠키 존재 + 서버 유효성까지 확인하고,
    만료면 (허용된 경우) 로그인 창을 띄워 그 자리에서 복구한다.
    """
    if is_logged_in(ctx):
        if verify_login(page):
            warn_if_expiring(ctx)
            return True
        print("[EXPIRED] 네이버 세션 만료 — 쿠키는 있으나 서버가 거부했습니다.")
    else:
        print("[EXPIRED] 로그인 쿠키가 없습니다.")

    if not allow_login:
        print("조치: py scripts/naver_crosspost.py --login  (로그인 상태 유지 자동 체크됨)")
        return False

    print("자동 복구: 로그인 창을 엽니다 (끄려면 --no-auto-login).")
    return do_login(ctx, page, check_existing=False)  # 위에서 이미 검증함


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


def _norm_label(s: str) -> str:
    """네이버 UI 라벨 비교용 정규화.

    발행 팝업의 카테고리 라벨은 공백을 non-breaking space(\\xa0)로 내려준다.
    그대로 비교하면 '생각하는 교실, 깊이있는 학습'이 항상 불일치로 잡혀
    매 발행마다 [warn] + 불필요한 드롭다운 조작을 유발했다(2026-07-22~26 로그).
    """
    return re.sub(r"\s+", " ", s or "").strip()


def goto_editor(page, url: str, attempts: int = 3):
    """에디터 진입. 직전 발행의 지연 리다이렉트와 겹치면 goto가 죽는다.

    발행 직후 네이버는 PostList.naver로 늦게 리다이렉트하는데, 그게 다음 글의
    goto와 겹치면 'interrupted by another navigation'으로 예외가 난다
    (2026-07-26 실측: 4번째 글에서 배치 전체가 중단됨). 진행 중인 네비게이션이
    끝나길 기다린 뒤 시도하고, 충돌하면 잠시 쉬었다 재시도한다.
    """
    last = None
    for i in range(attempts):
        try:
            page.wait_for_load_state("domcontentloaded", timeout=15000)
        except Exception:
            pass
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            return
        except Exception as e:
            last = e
            if "interrupted by another navigation" not in str(e):
                raise
            print(f"  [warn] 네비게이션 충돌 — 재시도 {i + 1}/{attempts}")
            time.sleep(4)
    raise last


def write_post(page, post: dict, cat_key: str, html: str, tags: list[str],
               publish: bool, debug: bool) -> str | None:
    cat = CATEGORIES[cat_key]
    goto_editor(page, f"https://blog.naver.com/{BLOG_ID}/postwrite?categoryNo={cat['no']}")
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
        sel_label = _norm_label(
            page.locator("button[class*='selectbox_button']").first.inner_text())
        if _norm_label(cat["name"]) not in sel_label:
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
    goto_editor(page, f"https://blog.naver.com/{BLOG_ID}/postwrite?logNo={logno}")
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
    ap.add_argument("--login", action="store_true", help="수동 로그인 (세션이 유효하면 건너뜀)")
    ap.add_argument("--force-login", action="store_true",
                    help="세션이 유효해도 다시 로그인해 만료일을 30일 뒤로 초기화")
    ap.add_argument("--check-session", action="store_true",
                    help="세션 유효성만 확인하고 종료 (유효 0 / 만료 2)")
    ap.add_argument("--no-auto-login", action="store_true",
                    help="세션 만료 시 로그인 창을 띄우지 않고 종료 (스케줄러용)")
    ap.add_argument("--dry-run", action="store_true", help="대상 목록/분류 미리보기")
    ap.add_argument("--classify-gemini", action="store_true",
                    help="전체 대상 포스트를 Gemini로 일괄 분류해 overrides 파일에 저장")
    ap.add_argument("--limit", type=int, default=10, help="이번 실행 최대 발행 수 (기본 10)")
    ap.add_argument("--daily-cap", type=int, default=20,
                    help="최근 24시간 발행 상한 (0=해제, 기본 20). 과발행 사고 방지")
    ap.add_argument("--post", help="특정 포스트 파일만 발행 (이미 게시된 글도 재발행)")
    ap.add_argument("--update", metavar="LOGNO",
                    help="기존 네이버 글의 본문을 교체 (--post와 함께 사용, 제목·카테고리 유지)")
    ap.add_argument("--category", choices=list(CATEGORIES), help="분류 수동 지정")
    ap.add_argument("--no-images", action="store_true", help="이미지 제외")
    ap.add_argument("--no-publish", action="store_true", help="발행 직전까지만 진행")
    ap.add_argument("--no-tags", action="store_true", help="태그 입력 생략")
    ap.add_argument("--debug", action="store_true", help="단계별 스크린샷 저장")
    # 글 간 대기. 2026-07-22부터 45~90초로 운영해 문제가 없었으므로 유지한다
    # (10편이면 실행당 약 11분). 발행이 몰리는 게 걱정되면 값을 올려 쓸 것.
    ap.add_argument("--no-git-sync", action="store_true",
                    help="게시 이력 원격 동기화·자동 커밋 끄기 (오프라인 실행용)")
    ap.add_argument("--min-wait", type=int, default=45)
    ap.add_argument("--max-wait", type=int, default=90)
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

    print(f"\n=== 실행 {time.strftime('%Y-%m-%d %H:%M:%S')} ===")

    state = load_json(STATE_FILE, {"posted": {}})
    # 대상 산정 전에 원격 이력을 합친다. 이 순서가 아니면 원격에만 기록된 발행분이
    # 미게시로 잡혀 그대로 중복 발행된다(2026-08-03 실제 사고, 20편).
    if not args.no_git_sync:
        state = sync_state_before_run(state)
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
            page = ctx.pages[0] if ctx.pages else ctx.new_page()

            if args.login or args.force_login:
                # --force-login은 '이미 유효한 세션' 지름길을 건너뛰고 폼을 띄운다
                if not do_login(ctx, page, check_existing=not args.force_login):
                    raise SystemExit(2)
                print("이어서 발행하려면: py scripts/naver_crosspost.py --limit 10")
                return

            if args.check_session:
                # 리포트는 검증 '전'에 — verify_login이 로그인 페이지로 리다이렉트되면
                # 네이버가 NID_AUT를 지워 버려 사후 조회는 항상 '없음'으로 보인다.
                report_session(ctx)
                warn_if_expiring(ctx)
                ok = is_logged_in(ctx) and verify_login(page)
                print("세션 유효 — 발행 가능" if ok
                      else "[EXPIRED] 세션 무효 — py scripts/naver_crosspost.py --login")
                raise SystemExit(0 if ok else 2)

            # 만료면 그 자리에서 로그인 창을 띄워 복구하고 이어서 발행한다.
            # 스케줄러(비대화 실행)는 --no-auto-login으로 기존 즉시 종료 동작 유지.
            if not ensure_session(ctx, page, allow_login=not args.no_auto_login):
                raise SystemExit(2)

            if args.update:
                if not args.post or not pending:
                    print("--update는 --post <파일>과 함께 사용합니다.")
                    return
                post = pending[0]
                html = md_to_html(post, include_images=not args.no_images)
                url = update_post(page, args.update, html, args.debug)
                print(f"[OK] 본문 교체 완료: {url or '(URL 미확인)'}")
                save_cookies(ctx)
                return

            if not pending:
                print("발행할 포스트가 없습니다.")
                return

            limit = args.limit
            if args.daily_cap > 0 and not args.post:
                done = recent_post_count(state)
                room = args.daily_cap - done
                if room <= 0:
                    print(f"최근 24시간 발행 {done}편 — 일일 상한 {args.daily_cap}편 도달. "
                          "이번 실행을 건너뜁니다.")
                    return
                if room < limit:
                    print(f"최근 24시간 발행 {done}편 — 상한까지 남은 {room}편만 발행합니다.")
                    limit = room

            batch = pending[:limit]
            span = len(batch) * (args.min_wait + args.max_wait) // 120
            print(f"이번 실행 발행 예정: {len(batch)}편 (전체 잔여 {len(pending)}편, "
                  f"예상 소요 약 {span}분)")

            # 한 편의 일시적 실패(네비게이션 충돌 등)로 남은 글까지 버리지 않는다.
            # 연속 2회 실패면 구조적 문제(세션·UI 변경)로 보고 중단한다.
            fails = 0
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
                    fails += 1
                    if fails >= 2:
                        print("  연속 2회 실패 — 이번 실행을 중단합니다.")
                        break
                    print("  이 글은 미게시로 남깁니다. 다음 글로 넘어갑니다...")
                    time.sleep(15)
                    continue
                fails = 0
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
            # 중단·예외로 끝나도 여기까지 발행한 만큼은 원격에 남겨야 다음 실행이
            # 같은 글을 다시 올리지 않는다.
            if not args.no_git_sync and not args.no_publish:
                done = len(state.get("posted", {}))
                push_state(f"{done}편 누적")


if __name__ == "__main__":
    main()
