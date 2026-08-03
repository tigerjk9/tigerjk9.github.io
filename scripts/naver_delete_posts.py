#!/usr/bin/env python3
"""네이버 블로그 글 삭제 — 중복 발행 정리용.

  py -u scripts/naver_delete_posts.py --file targets.json --dry-run
  py -u scripts/naver_delete_posts.py --file targets.json --limit 1
  py -u scripts/naver_delete_posts.py --logno 224366411240

targets.json 은 [{"post": "...md", "url": "https://blog.naver.com/dot_connector/224..."}, ...]

삭제는 되돌릴 수 없다. 그래서 매 건마다
  ① 페이지에 실제로 열린 글의 logNo 가 대상과 같은지 확인하고
  ② 사이드바 공지 위젯의 삭제 링크(_noticePost.remove)와 절대 섞이지 않게
     글 본문의 _deletePost 만 클릭하며
  ③ 삭제 후 해당 URL 을 다시 열어 사라졌는지 검증한다.
어느 단계든 어긋나면 그 건을 건너뛴다.

브라우저 세션·쿠키·로그인은 naver_crosspost.py 의 것을 그대로 쓴다.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import naver_crosspost as nc  # noqa: E402

# 글 본문 하단의 삭제 링크. 사이드바 공지 위젯의 것은 _noticePost.remove 라 걸리지 않는다.
DELETE_SEL = "a._deletePost"


def logno_of(url_or_no: str) -> str:
    m = re.search(r"(\d{6,})", url_or_no or "")
    return m.group(1) if m else ""


def warn_unknown_pair(keep_url: str, post: str) -> bool:
    """중복 정리에서 '남길 쪽'의 URL 이 unknown 이면 삭제하면 안 된다.

    게시 이력의 url:"unknown" 은 '다른 주소로 발행됨'이 아니라 **발행 결과를 확인하지 못함**
    이다. 실제로 발행이 성사되지 않은 경우가 있어, 지우려는 쪽이 유일본일 수 있다.
    2026-08-03 codex 글에서 이 오판으로 유일본을 삭제했다(이후 재발행 복구).
    """
    if logno_of(keep_url):
        return False
    print(f"    !! 남길 쪽 URL 이 unknown — 중복이 아닐 수 있어 건너뜁니다: {post}")
    print("       네이버에서 같은 제목 글이 2건인지 직접 확인한 뒤 --logno 로 지정하세요")
    return True


def page_logno(mf) -> str:
    """지금 열린 글의 logNo 를 페이지 안에서 직접 읽는다 (URL 신뢰하지 않음)."""
    try:
        return mf.evaluate("""() => {
          const a = document.querySelector('a._postStat, a._showTagEditBox');
          const cls = a ? a.className : '';
          let m = cls.match(/article\\/(\\d+)\\//) || cls.match(/_param\\(EDIT\\|(\\d+)\\|/);
          if (m) return m[1];
          m = (document.location.href || '').match(/logNo=(\\d+)/);
          return m ? m[1] : '';
        }""") or ""
    except Exception:
        return ""


def is_gone(page, logno: str) -> bool:
    """삭제 검증 — 글 페이지를 다시 열어 본문이 사라졌는지 본다."""
    try:
        page.goto(f"https://blog.naver.com/{nc.BLOG_ID}/{logno}",
                  wait_until="domcontentloaded", timeout=45000)
        page.wait_for_timeout(2500)
        for f in page.frames:
            try:
                txt = f.evaluate("() => document.body ? document.body.innerText : ''") or ""
            except Exception:
                continue
            if re.search(r"삭제되었거나 존재하지 않는|없는 페이지|삭제된 게시(글|물)", txt):
                return True
        mf = next((f for f in page.frames if f.name == "mainFrame"), None)
        # 본문이 그대로 살아 있으면 삭제 실패로 본다.
        return not (mf and page_logno(mf) == logno)
    except Exception:
        return False


def delete_one(page, logno: str, dry: bool) -> str:
    """반환: ok / skip:<이유> / fail:<이유>"""
    page.goto(f"https://blog.naver.com/{nc.BLOG_ID}/{logno}",
              wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    mf = next((f for f in page.frames if f.name == "mainFrame"), None)
    if not mf:
        return "fail:mainFrame 없음"

    got = page_logno(mf)
    if got != logno:
        return f"skip:열린 글이 다름 (기대 {logno} / 실제 {got or '미확인'})"

    # 한 글에 삭제 링크가 둘 있다 — ⋮ 메뉴 안의 숨은 것(_param(<logNo>|...))과
    # 글 하단의 보이는 것(_param(<글 순번>|...)). 둘 다 같은 글을 가리킨다(실측).
    # 보이는 것만 세고, 그 개수가 1이 아니면 손대지 않는다.
    total = mf.locator(DELETE_SEL).count()
    if total == 0:
        return "skip:삭제 링크 없음 (이미 삭제됐거나 권한 없음)"
    link = mf.locator(f"{DELETE_SEL}:visible")
    n = link.count()
    if n == 0:
        return f"skip:보이는 삭제 링크 없음 (전체 {total}개)"
    if n > 1:
        return f"skip:보이는 삭제 링크가 {n}개 — 오삭제 위험"

    # 링크가 대상 logNo 를 명시하고 있으면 그 값까지 대조한다.
    cls = link.first.get_attribute("class") or ""
    m = re.search(r"_param\((\d{6,})\|", cls)
    if m and m.group(1) != logno:
        return f"skip:삭제 링크가 다른 글({m.group(1)})을 가리킴"

    if dry:
        return "ok(dry)"

    # 네이티브 confirm 이 뜨면 수락
    page.once("dialog", lambda d: d.accept())
    link.first.click(timeout=15000)
    page.wait_for_timeout(2000)

    # 레이어형 확인창이면 그 안의 확정 버튼을 누른다
    for fr in page.frames:
        try:
            btn = fr.locator(
                "button:has-text('삭제'), a:has-text('삭제'), "
                "button:has-text('확인'), a:has-text('확인')")
            for i in range(min(btn.count(), 6)):
                b = btn.nth(i)
                if b.is_visible():
                    b.click(timeout=5000)
                    page.wait_for_timeout(1500)
                    raise StopIteration
        except StopIteration:
            break
        except Exception:
            continue

    page.wait_for_timeout(2500)
    return "ok" if is_gone(page, logno) else "fail:삭제 후에도 글이 남아 있음"


def main() -> None:
    ap = argparse.ArgumentParser(description="네이버 블로그 글 삭제")
    ap.add_argument("--file", help="대상 JSON ([{post,url}, ...])")
    ap.add_argument("--logno", action="append", default=[], help="개별 logNo (반복 가능)")
    ap.add_argument("--dry-run", action="store_true", help="확인만 하고 삭제하지 않음")
    ap.add_argument("--limit", type=int, help="이번 실행 최대 건수")
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--min-wait", type=int, default=6)
    ap.add_argument("--max-wait", type=int, default=12)
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

    targets: "list[dict]" = []
    if args.file:
        for row in json.loads(Path(args.file).read_text(encoding="utf-8")):
            # keep_url 이 있으면 '남길 쪽'을 검증한다. unknown 이면 중복 판정 자체가 의심스럽다.
            if "keep_url" in row and warn_unknown_pair(row["keep_url"], row.get("post", "")):
                continue
            targets.append({"post": row.get("post", ""), "logno": logno_of(row.get("url", ""))})
    for n in args.logno:
        targets.append({"post": "", "logno": logno_of(n)})
    targets = [t for t in targets if t["logno"]]
    if args.limit:
        targets = targets[:args.limit]
    if not targets:
        print("[ERROR] 삭제 대상이 없습니다")
        sys.exit(1)

    print(f"\n=== 삭제 {'미리보기' if args.dry_run else '실행'} "
          f"{time.strftime('%Y-%m-%d %H:%M:%S')} — {len(targets)}건 ===")
    for t in targets:
        print(f"  {t['logno']}  {t['post']}")
    print()

    from playwright.sync_api import sync_playwright

    results = []
    with sync_playwright() as pw:
        ctx = nc.launch(pw, headless=args.headless)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        try:
            if not nc.ensure_session(ctx, page, allow_login=True):
                print("[ERROR] 로그인 세션이 없습니다 — naver_crosspost.py --login 먼저 실행")
                sys.exit(2)
            for i, t in enumerate(targets):
                print(f"[{i + 1}/{len(targets)}] {t['logno']} {t['post']}")
                try:
                    r = delete_one(page, t["logno"], args.dry_run)
                except Exception as e:
                    r = f"fail:{str(e)[:120]}"
                print(f"    -> {r}")
                results.append({**t, "result": r})
                if i < len(targets) - 1:
                    time.sleep(random.randint(args.min_wait, args.max_wait))
            nc.save_cookies(ctx)
        finally:
            try:
                ctx.close()
            except Exception:
                pass

    ok = [r for r in results if r["result"].startswith("ok")]
    print(f"\n=== 결과: 성공 {len(ok)} / 전체 {len(results)} ===")
    for r in results:
        if not r["result"].startswith("ok"):
            print(f"  [{r['result']}] {r['logno']} {r['post']}")
    out = SCRIPT_DIR / ".naver_delete_result.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"기록: {out}")


if __name__ == "__main__":
    main()
