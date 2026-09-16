#!/usr/bin/env python
"""블로그 자동화 건강검진 — 조용히 죽어 있는 것을 찾는다.

`/video`가 서비스에서 내려간 모델 ID를 붙들고 404로 죽고 있었는데 아무도 몰랐다
(2026-09-16 실측). 그런 종류의 고장은 다음 배치가 통째로 날아가고 나서야 드러난다.
이 스크립트는 생성 호출을 하지 않고(무과금) 각 자동화의 전제 조건만 점검한다.

  py -X utf8 scripts/health_check.py            # 전체
  py -X utf8 scripts/health_check.py --quick    # 네트워크 점검 생략
  py -X utf8 scripts/health_check.py --json     # 기계 판독용

종료코드: 실패가 하나라도 있으면 1.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import ssl
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

OK, WARN, FAIL = "ok", "warn", "fail"
MARK = {OK: "OK ", WARN: "경고", FAIL: "실패"}

results: list[tuple[str, str, str]] = []   # (섹션, 상태, 메시지)


def add(section: str, status: str, message: str) -> None:
    results.append((section, status, message))


def load_env() -> dict:
    env = {}
    path = REPO / ".env"
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env


# ── 1. 환경 ────────────────────────────────────────────────────────────────
def check_env(env: dict) -> None:
    for key in ("GEMINI_API_KEY", "ASK_ACCESS_KEY"):
        if env.get(key):
            add("환경", OK, f"{key} 있음")
        else:
            add("환경", FAIL if key == "GEMINI_API_KEY" else WARN,
                f"{key} 없음 — .env 확인")


# ── 2. 모델 ID ─────────────────────────────────────────────────────────────
MODEL_RE = re.compile(r'"((?:gemini|lyria|nano-banana|gemma)[a-z0-9.\-]*)"')


def scan_model_refs() -> dict[str, list[str]]:
    """소스에서 모델 ID를 긁는다. 목록을 코드에 박지 않아야 새 참조도 잡힌다."""
    refs: dict[str, list[str]] = {}
    for path in sorted(SCRIPTS.rglob("*.py")):
        if path.name == Path(__file__).name:
            continue
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for name in MODEL_RE.findall(line):
                if len(name.split("-")) < 2:
                    continue
                refs.setdefault(name, []).append(f"{path.relative_to(REPO).as_posix()}:{i}")
    return refs


def check_models(env: dict) -> set[str]:
    refs = scan_model_refs()
    if not env.get("GEMINI_API_KEY"):
        add("모델", WARN, f"모델 {len(refs)}종 참조 — 키가 없어 대조 생략")
        return set()
    try:
        import google.generativeai as genai
        genai.configure(api_key=env["GEMINI_API_KEY"])
        live = {m.name.split("/")[-1] for m in genai.list_models()}
    except Exception as exc:  # noqa: BLE001
        add("모델", FAIL, f"모델 목록 조회 실패 — {type(exc).__name__}: {str(exc)[:120]}")
        return set()
    add("API 키", OK, f"GEMINI_API_KEY 유효 (모델 {len(live)}개 조회)")
    dead = {n: locs for n, locs in refs.items() if n not in live}
    if dead:
        for name, locs in sorted(dead.items()):
            add("모델", FAIL, f"{name} — 서비스에 없음 ({', '.join(locs[:3])})")
    else:
        total = sum(len(v) for v in refs.values())
        add("모델", OK, f"모델 {len(refs)}종 · 참조 {total}곳 모두 유효")
    return live


# ── 3. 파이썬 의존성 ────────────────────────────────────────────────────────
IMPORT_NAME = {
    "google-generativeai": "google.generativeai",
    "beautifulsoup4": "bs4",
    "PyMuPDF": "fitz",
    "duckduckgo-search": "duckduckgo_search",
    "opencv-python-headless": "cv2",
    "Pillow": "PIL",
    "youtube-transcript-api": "youtube_transcript_api",
    "yt-dlp": "yt_dlp",
}


def check_deps() -> None:
    import importlib.util
    req = SCRIPTS / "requirements.txt"
    if not req.exists():
        add("의존성", WARN, "requirements.txt 없음")
        return
    missing = []
    for line in req.read_text(encoding="utf-8").splitlines():
        pkg = re.split(r"[><=!]", line.strip())[0].strip()
        if not pkg or pkg.startswith("#"):
            continue
        mod = IMPORT_NAME.get(pkg, pkg.replace("-", "_"))
        try:
            found = importlib.util.find_spec(mod) is not None
        except (ImportError, ValueError):
            found = False
        if not found:
            missing.append(pkg)
    if missing:
        add("의존성", FAIL, f"미설치 {len(missing)}개: {', '.join(missing)} "
                            f"→ py -m pip install -r scripts/requirements.txt")
    else:
        add("의존성", OK, "requirements.txt 전부 임포트 가능")


# ── 4. 외부 도구 ────────────────────────────────────────────────────────────
def check_tools() -> None:
    for name, hint in [("git", "필수"), ("gh", "릴리스·배포 확인용")]:
        if shutil.which(name):
            add("도구", OK, f"{name} 있음")
        else:
            add("도구", FAIL if hint == "필수" else WARN, f"{name} 없음 ({hint})")
    edge = [r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"]
    if any(Path(p).exists() for p in edge) or shutil.which("msedge"):
        add("도구", OK, "Edge 있음 (헤드리스 캡처)")
    else:
        add("도구", WARN, "Edge 없음 — 카드뉴스·훅 렌더 불가")
    try:
        import imageio_ffmpeg
        imageio_ffmpeg.get_ffmpeg_exe()
        add("도구", OK, "ffmpeg 있음")
    except Exception:  # noqa: BLE001
        add("도구", WARN, "ffmpeg 없음 — 영상 처리 불가")


# ── 5. 콘텐츠 소스 ──────────────────────────────────────────────────────────
UA_RE = re.compile(r"Mozilla/5\.0[^\"']*Chrome/(\d+)[^\"']*Safari/[\d.]+")
UA_MIN_MAJOR = 130          # 이보다 낮으면 사이트가 봇으로 본다 (GeekNews 실측)


def pipeline_headers() -> dict:
    """web_to_post.py가 실제로 보내는 헤더를 소스에서 그대로 읽는다."""
    src = (SCRIPTS / "web_to_post.py").read_text(encoding="utf-8", errors="ignore")
    joined = re.sub(r"\"\s*\n\s*\"", "", src)          # 여러 줄로 쪼개 쓴 UA를 잇는다
    m = UA_RE.search(joined)
    ua = m.group(0) if m else "Mozilla/5.0"
    return {"User-Agent": ua, "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8"}


def check_user_agent() -> None:
    """낡은 UA는 조용한 403의 원인이다 — Chrome/120에서 GeekNews가 막혔다(2026-09-16)."""
    stale = []
    for path in sorted(SCRIPTS.rglob("*.py")):
        if path.name == Path(__file__).name:
            continue
        src = re.sub(r"\"\s*\n\s*\"", "", path.read_text(encoding="utf-8", errors="ignore"))
        for major in UA_RE.findall(src):
            if int(major) < UA_MIN_MAJOR:
                stale.append(f"{path.relative_to(REPO).as_posix()} (Chrome/{major})")
    if stale:
        add("UA", WARN, f"낡은 브라우저 UA {len(stale)}곳: {', '.join(stale[:3])} "
                        f"— 최신 Chrome 버전으로 올릴 것")
    else:
        add("UA", OK, f"브라우저 UA 최신 (Chrome/{UA_MIN_MAJOR}+ 기준)")


# (이름, URL, 헤더 종류) — 파이프라인이 그 소스에 실제로 쓰는 헤더를 따라간다.
SOURCES = [
    ("GeekNews", "https://news.hada.io/topic?id=1", "web"),
    ("Jina Reader", "https://r.jina.ai/https://example.com", "jina"),
    ("네이버 모바일 블로그", "https://m.blog.naver.com", "web"),
    ("YouTube", "https://www.youtube.com", "web"),
    ("AI 챗봇 API", "https://dotconnector-ask.vercel.app/api/health", "plain"),
    ("블로그", "https://tigerjk9.github.io/", "plain"),
]


def probe(item: tuple[str, str, str]) -> tuple[str, str, str]:
    """파이프라인이 실제로 쓰는 헤더로 찔러 본다.

    비슷한 헤더로 따로 요청하면 거짓 통과가 난다 — GeekNews는 Chrome/120에는 403,
    최신 UA에는 200을 준다(실측). 점검이 본체와 다른 경로를 타면 안 된다.
    """
    name, url, kind = item
    headers = {"jina": {"Accept": "text/plain"}, "plain": {}}.get(kind) or pipeline_headers()
    try:
        import requests
        import urllib3
        urllib3.disable_warnings()
        r = requests.get(url, timeout=12, verify=False, headers=headers)
        if r.status_code < 400:
            return ("소스", OK, f"{name} {r.status_code}")
        return ("소스", WARN, f"{name} {r.status_code} — 차단 가능성, 우회 경로 확인")
    except Exception as exc:  # noqa: BLE001
        return ("소스", WARN, f"{name} 실패 — {type(exc).__name__}")


def check_sources() -> None:
    ssl._create_default_https_context = ssl._create_unverified_context
    with ThreadPoolExecutor(max_workers=6) as pool:
        for r in pool.map(probe, SOURCES):
            results.append(r)


# ── 6. 데이터 신선도 ────────────────────────────────────────────────────────
def check_data() -> None:
    posts = list((REPO / "_posts").glob("*.md"))
    review = [p for p in posts
              if "논문리뷰" in p.read_text(encoding="utf-8", errors="ignore")[:600]]
    db = REPO / "assets/research-db.json"
    if not db.exists():
        add("데이터", FAIL, "research-db.json 없음 → py scripts/build_research_db.py")
        return
    entries = json.loads(db.read_text(encoding="utf-8"))
    count = len(entries.get("posts", entries) if isinstance(entries, dict) else entries)
    gap = len(review) - count
    if gap > 0:
        add("데이터", WARN, f"리서치 허브 {count}편 / 논문리뷰 태그 {len(review)}편 — "
                            f"{gap}편 누락 가능. build_research_db.py → build_embeddings.py 재실행")
    else:
        add("데이터", OK, f"리서치 허브 {count}편 (포스트 {len(posts)}편)")
    for name in ("research-emb-posts.json", "research-rag-index.json"):
        p = REPO / "assets" / name
        if p.exists():
            age = (time.time() - p.stat().st_mtime) / 86400
            add("데이터", OK if age < 30 else WARN, f"{name} {age:.0f}일 전 갱신")
        else:
            add("데이터", FAIL, f"{name} 없음 → py scripts/build_embeddings.py")


# ── 7. 네이버 크로스포스팅 ──────────────────────────────────────────────────
def check_naver() -> None:
    cookies = SCRIPTS / ".naver_profile/cookies.json"
    if not cookies.exists():
        add("네이버", WARN, "쿠키 백업 없음 — py scripts/naver_crosspost.py --login")
    else:
        try:
            data = json.loads(cookies.read_text(encoding="utf-8"))
            auth = [c for c in data if c.get("name") == "NID_AUT" and c.get("expires", 0) > 0]
            if not auth:
                add("네이버", WARN, "NID_AUT가 세션 쿠키 — 상태유지 없이 로그인된 상태")
            else:
                exp = datetime.fromtimestamp(max(c["expires"] for c in auth), tz=timezone.utc)
                days = (exp - datetime.now(timezone.utc)).days
                status = OK if days > 7 else (WARN if days > 0 else FAIL)
                add("네이버", status,
                    f"세션 만료까지 {days}일 ({exp.astimezone():%Y-%m-%d})"
                    + ("" if days > 7 else " → --login 재실행 필요"))
        except Exception as exc:  # noqa: BLE001
            add("네이버", WARN, f"쿠키 파싱 실패 — {type(exc).__name__}")

    if sys.platform == "win32":
        try:
            out = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "$i=Get-ScheduledTaskInfo -TaskName NaverCrosspost -ErrorAction Stop;"
                 "$t=Get-ScheduledTask -TaskName NaverCrosspost;"
                 "\"$($t.State)|$($i.LastTaskResult)|$($i.LastRunTime)\""],
                capture_output=True, text=True, timeout=30)
            line = out.stdout.strip()
            if out.returncode != 0 or "|" not in line:
                add("네이버", FAIL, "스케줄 작업 NaverCrosspost 없음 — 재등록 필요")
            else:
                state, code, last = line.split("|", 2)
                add("네이버", OK if code.strip() in ("0", "267009") else WARN,
                    f"스케줄 작업 {state} · 마지막 결과 {code} · {last}")
        except Exception as exc:  # noqa: BLE001
            add("네이버", WARN, f"스케줄 작업 조회 실패 — {type(exc).__name__}")

    ledger = SCRIPTS / "naver_crosspost_state.json"
    if ledger.exists():
        try:
            d = json.loads(ledger.read_text(encoding="utf-8"))
            rows = d.get("posted", d) if isinstance(d, dict) else d
            unknown = sum(1 for r in rows if isinstance(r, dict) and r.get("url") == "unknown")
            add("네이버", WARN if unknown else OK,
                f"게시 이력 {len(rows)}건"
                + (f" · url=unknown {unknown}건 → --audit 권장" if unknown else ""))
        except Exception as exc:  # noqa: BLE001
            add("네이버", WARN, f"이력 파싱 실패 — {type(exc).__name__}")


# ── 8. 용량 (GitHub Pages 1GB 한도) ─────────────────────────────────────────
def dir_size(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def check_size() -> None:
    assets = REPO / "assets"
    if not assets.is_dir():
        return
    mb = dir_size(assets) / 1024 / 1024
    status = OK if mb < 800 else (WARN if mb < 950 else FAIL)
    add("용량", status, f"assets/ {mb:.0f}MB — Pages 한도 1GB"
        + ("" if status == OK else " · 대용량 자료는 GitHub 릴리스로"))


def notice(path: Path) -> int:
    """예약 점검이 남긴 결과를 세션 시작 때 한 줄로 알린다.

    로그만 쌓고 아무도 안 읽으면 조용한 고장을 못 잡는다는 원래 문제로 돌아간다.
    """
    try:
        Path.cwd().relative_to(REPO)          # 이 저장소 밖에서는 조용히 넘어간다
    except ValueError:
        return 0
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return 0
    age_days = (time.time() - path.stat().st_mtime) / 86400
    if age_days > 3:
        print(f"[건강검진] 마지막 점검이 {age_days:.0f}일 전이다 — "
              f"py -X utf8 scripts/health_check.py")
        return 0
    counts = data.get("summary", {})
    problems = data.get("problems", [])
    if not counts.get("fail") and not problems:
        return 0
    head = "실패 %d · 경고 %d" % (counts.get("fail", 0), counts.get("warn", 0))
    first = problems[0]["message"] if problems else ""
    print(f"[건강검진] {head} — {first}"
          + (f" 외 {len(problems) - 1}건" if len(problems) > 1 else ""))
    return 0


# ── 실행 ────────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--quick", action="store_true", help="네트워크 점검 생략")
    ap.add_argument("--json", action="store_true", help="JSON으로 출력")
    ap.add_argument("--notice", action="store_true",
                    help="점검을 돌리지 않고 마지막 결과만 한 줄로 알린다 (훅용)")
    ap.add_argument("--status-file", type=Path, default=None,
                    help="요약을 JSON 파일로 남긴다 (예약 실행용)")
    a = ap.parse_args()

    if a.notice:
        return notice(a.status_file or SCRIPTS / ".health_status.json")

    started = time.time()
    env = load_env()
    check_env(env)
    if not a.quick:
        check_models(env)
    check_deps()
    check_tools()
    check_user_agent()
    if not a.quick:
        check_sources()
    check_data()
    check_naver()
    check_size()

    counts = {OK: 0, WARN: 0, FAIL: 0}
    for _, status, _ in results:
        counts[status] += 1

    if a.json:
        print(json.dumps({"results": [{"section": s, "status": st, "message": m}
                                      for s, st, m in results],
                          "summary": counts}, ensure_ascii=False, indent=2))
    else:
        width = max(len(s) for s, _, _ in results)
        for section, status, message in results:
            print(f"[{MARK[status]}] {section:<{width}}  {message}")
        print(f"\n통과 {counts[OK]} · 경고 {counts[WARN]} · 실패 {counts[FAIL]} "
              f"({time.time() - started:.1f}초)")
    if a.status_file:
        payload = {
            "checked_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "summary": counts,
            "problems": [{"section": s, "status": st, "message": m}
                         for s, st, m in results if st != OK],
        }
        a.status_file.parent.mkdir(parents=True, exist_ok=True)
        a.status_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + chr(10), encoding="utf-8")

    return 1 if counts[FAIL] else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
