# -*- coding: utf-8 -*-
"""
weekly_digest.py — 지난 한 주 포스트를 모아 주간 다이제스트 포스트를 생성한다.

주당 20~30편이 올라오는 발행 페이스에서 독자가 따라올 수 있는 진입점을 만든다.
Claude Code에서는 /digest 슬래시 커맨드로 호출한다.

실행:
  py scripts/weekly_digest.py                # 생성 + git push
  py scripts/weekly_digest.py --dry-run      # 출력만
  py scripts/weekly_digest.py --no-push      # 로컬 저장만
  py scripts/weekly_digest.py --days 14      # 대상 기간 변경 (기본 7일)

환경변수: GEMINI_API_KEY (.env 자동 로드)
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "_posts"
TEMPLATE = REPO_ROOT / "scripts" / "digest_prompt_template.txt"
MODEL = "gemini-2.5-flash"
EXCERPT_CHARS = 500
DIGEST_TAG = "주간다이제스트"


def _load_dotenv() -> None:
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_post(path: Path):
    """포스트에서 title/categories/tags/permalink/발췌를 추출."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        return None
    fm, body = m.group(1), text[m.end():]

    def scalar(key):
        mm = re.search(r"^%s:\s*(.+?)\s*$" % key, fm, re.MULTILINE)
        if not mm:
            return ""
        return mm.group(1).strip().strip('"').strip("'")

    def array(key):
        mm = re.search(r"^%s:\s*\[(.*?)\]" % key, fm, re.MULTILINE | re.DOTALL)
        if not mm:
            return []
        return [x.strip().strip('"').strip("'") for x in mm.group(1).split(",") if x.strip()]

    tags = array("tags")
    if DIGEST_TAG in tags:  # 다이제스트가 다이제스트를 소화하지 않도록
        return None

    permalink = scalar("permalink")
    if not permalink:
        slug = path.stem[11:]
        permalink = "/post/%s/" % slug

    # 본문 발췌: HTML/figure/헤딩/링크 마커 정리 후 앞부분
    body = re.sub(r"<figure\b.*?</figure>", "", body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r"<[^>]+>", "", body)
    body = re.sub(r"^#{1,4}\s.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"[*>`_]", "", body)
    body = re.sub(r"\s+", " ", body).strip()

    return {
        "file": path.name,
        "date": path.name[:10],
        "title": scalar("title"),
        "categories": array("categories"),
        "tags": tags,
        "permalink": permalink,
        "excerpt": body[:EXCERPT_CHARS],
    }


def collect_posts(days: int, end_date: datetime):
    start = (end_date - timedelta(days=days)).strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")
    posts = []
    for p in sorted(POSTS_DIR.glob("*.md")):
        d = p.name[:10]
        if start < d <= end:
            info = parse_post(p)
            if info and info["title"]:
                posts.append(info)
    return posts


def build_posts_block(posts) -> str:
    lines = []
    for i, p in enumerate(posts, 1):
        lines.append(
            "%d. 제목: %s\n   날짜: %s | 카테고리: %s | 태그: %s\n   퍼머링크: %s\n   발췌: %s"
            % (i, p["title"], p["date"], ", ".join(p["categories"]),
               ", ".join(p["tags"][:6]), p["permalink"], p["excerpt"]))
    return "\n\n".join(lines)


def call_gemini(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY 미설정 (.env 확인)")
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name=MODEL)
    res = model.generate_content(prompt)
    return res.text


def sanitize(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:markdown)?\s*\n", "", text)
    text = re.sub(r"\n```\s*$", "", text)
    text = re.sub(r"^\*\s+", "- ", text, flags=re.MULTILINE)  # 불릿 컨벤션 통일
    return text.strip()


def normalize_links(body: str, valid_permalinks: set) -> str:
    """링크 후처리: Gemini가 붙인 환각 도메인 제거 + permalink 화이트리스트 검증.

    실측: 제공한 상대경로에 존재하지 않는 도메인(https://dotconnector.co)을
    전 링크에 붙인 사례 확인 (2026-07-03). 도메인을 벗겨 상대경로로 정규화하고,
    대상 포스트 permalink와 일치하지 않는 링크는 경고를 출력한다.
    """
    warnings = []

    def fix(m):
        text, url = m.group(1), m.group(2)
        u = re.sub(r"^https?://[^/]+", "", url)  # 도메인 제거
        if not u.startswith("/post/"):
            return m.group(0)  # 외부 링크 등은 손대지 않음
        if u not in valid_permalinks:
            warnings.append("%s → %s" % (text[:30], u))
        return "[%s](%s)" % (text, u)

    body = re.sub(r"\[([^\]]+)\]\((\S+?)\)", fix, body)
    for w in warnings:
        print("[WARN] 대상 포스트에 없는 링크: %s" % w)
    return body


def split_title(text: str):
    m = re.match(r"TITLE:\s*(.+?)\s*\n", text)
    if not m:
        return None, text
    return m.group(1).strip().strip('"'), text[m.end():].strip()


def git_push(paths, message):
    def run(args):
        return subprocess.run(["git"] + args, cwd=str(REPO_ROOT),
                              capture_output=True, text=True)
    run(["add"] + paths)
    r = run(["commit", "-m", message])
    if r.returncode != 0:
        print("[WARN] git commit 실패:\n%s" % r.stderr.strip())
        return
    print("[OK] git commit 완료")
    run(["fetch", "origin"])
    run(["rebase", "origin/main", "--autostash"])
    r = run(["push", "origin", "main"])
    if r.returncode != 0:
        print("[WARN] git push 실패. 수동으로 push 하라.\n  → git push origin main")
    else:
        print("[OK] git push 완료")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7, help="대상 기간 (기본 7일)")
    ap.add_argument("--date", help="기준일 YYYY-MM-DD (기본 오늘)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    end_date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.now()
    posts = collect_posts(args.days, end_date)
    if len(posts) < 3:
        print("[SKIP] 지난 %d일 포스트가 %d편뿐이라 다이제스트를 만들지 않는다 (최소 3편)."
              % (args.days, len(posts)))
        return
    print("대상 포스트 %d편 (%d일)" % (len(posts), args.days))
    for p in posts:
        print("  - %s %s" % (p["date"], p["title"][:44]))

    prompt = TEMPLATE.read_text(encoding="utf-8").replace(
        "{POSTS_DATA}", build_posts_block(posts))
    print("[..] Gemini 생성 중 (%s)" % MODEL)
    out = sanitize(call_gemini(prompt))
    title, body = split_title(out)
    body = normalize_links(body, {p["permalink"] for p in posts})
    if not title:
        title = "주간 다이제스트, %s" % end_date.strftime("%Y년 %m월 %d일 무렵")
        print("[WARN] TITLE 라인 미검출 — 기본 제목 사용")

    date_str = end_date.strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M:%S")
    slug = "weekly-digest-%s" % date_str
    front = "\n".join([
        "---",
        'title: "%s"' % title.replace('"', "'"),
        "date: %s %s +0900" % (date_str, now_time),
        "categories: [다이제스트]",
        "tags: [%s, 블로그]" % DIGEST_TAG,
        "permalink: /post/%s/" % slug,
        "---",
        "", ""])
    content = front + body + "\n"

    out_path = POSTS_DIR / ("%s-weekly-digest.md" % date_str)
    if args.dry_run:
        print("\n" + "=" * 60)
        print(content[:3000])
        print("=" * 60)
        print("[dry-run] 저장 안 함: %s" % out_path.name)
        return

    out_path.write_text(content, encoding="utf-8")
    print("[OK] 저장: %s" % out_path.relative_to(REPO_ROOT))
    if args.no_push:
        print("[SKIP] push 생략 (--no-push)")
        return
    git_push([str(out_path.relative_to(REPO_ROOT))],
             "add: %s 주간 다이제스트" % date_str)


if __name__ == "__main__":
    main()
