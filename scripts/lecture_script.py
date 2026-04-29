#!/usr/bin/env python3
"""
lecture_script.py — 다양한 입력(YouTube/웹/PDF/파일)에서 교사 연수용 강의 스크립트 생성

사용법:
  python scripts/lecture_script.py <입력> [옵션]

입력:
  YouTube URL, 웹 URL, PDF 파일 경로, 또는 텍스트 파일 경로

옵션:
  --duration N         강의 시간(분) (기본값: 45)
  --date  YYYY-MM-DD   포스트 날짜 (기본값: 오늘)
  --slug  SLUG         파일명 슬러그
  --no-push            로컬 저장만
  --dry-run            출력만 (파일 저장 없음)
  --model  MODEL       Gemini 모델 ID (기본값: gemini-2.5-flash)

환경변수:
  GEMINI_API_KEY       Google AI Studio API 키 (필수) — .env 파일에 저장 권장
"""

from __future__ import annotations

import argparse
import io
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Windows 터미널 한글 깨짐 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ──────────────────────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent

import sys as _sys
_sys.path.insert(0, str(SCRIPT_DIR))
from image_fetcher import fetch_and_inject_image  # noqa: E402
POSTS_DIR = REPO_ROOT / "_posts"
PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "lecture_prompt_template.txt"
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_CONTENT_CHARS = 80000


# ──────────────────────────────────────────────────────────────
# .env 자동 로드
# ──────────────────────────────────────────────────────────────

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


# ──────────────────────────────────────────────────────────────
# SSL 인증서 검증 우회 (기업 네트워크 대응)
# ──────────────────────────────────────────────────────────────

import ssl as _ssl

_ssl._create_default_https_context = _ssl._create_unverified_context  # type: ignore[attr-defined]

try:
    import urllib3 as _urllib3  # type: ignore[import]
    _urllib3.disable_warnings(_urllib3.exceptions.InsecureRequestWarning)
except Exception:
    pass

try:
    import requests as _requests
    _requests.packages.urllib3.disable_warnings()  # type: ignore[attr-defined]
    _orig_request = _requests.Session.request

    def _no_verify_request(self, method, url, **kwargs):  # type: ignore[no-untyped-def]
        kwargs.setdefault("verify", False)
        return _orig_request(self, method, url, **kwargs)

    _requests.Session.request = _no_verify_request  # type: ignore[method-assign]
except Exception:
    pass


# ──────────────────────────────────────────────────────────────
# 입력 타입 감지
# ──────────────────────────────────────────────────────────────

def detect_input_type(input_str: str) -> str:
    """'youtube', 'web', 'pdf', 'file' 중 하나 반환."""
    if re.search(r"(youtube\.com|youtu\.be)", input_str):
        return "youtube"
    if input_str.startswith("http://") or input_str.startswith("https://"):
        return "web"
    if Path(input_str).suffix.lower() == ".pdf":
        return "pdf"
    return "file"


# ──────────────────────────────────────────────────────────────
# 기존 카테고리/태그 수집
# ──────────────────────────────────────────────────────────────

def get_existing_taxonomy() -> tuple[list[str], list[str]]:
    cat_counter: Counter = Counter()
    tag_counter: Counter = Counter()
    for md_file in POSTS_DIR.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            continue
        fm = fm_match.group(1)
        cat_counter.update(_parse_yaml_list(fm, "categories"))
        tag_counter.update(_parse_yaml_list(fm, "tags"))
    return [c for c, _ in cat_counter.most_common()], [t for t, _ in tag_counter.most_common(40)]


def _parse_yaml_list(front_matter: str, key: str) -> list[str]:
    items: list[str] = []
    inline = re.search(rf"^{key}:\s*\[(.+?)\]", front_matter, re.MULTILINE)
    if inline:
        for item in inline.group(1).split(","):
            val = item.strip().strip("'\"")
            if val:
                items.append(val)
        return items
    block = re.search(rf"^{key}:\s*\n((?:\s*-\s*.+\n?)+)", front_matter, re.MULTILINE)
    if block:
        for line in block.group(1).splitlines():
            m = re.match(r"\s*-\s*(.+)", line)
            if m:
                items.append(m.group(1).strip().strip("'\""))
    return items


# ──────────────────────────────────────────────────────────────
# 관련 포스트 탐색
# ──────────────────────────────────────────────────────────────

# 너무 흔해서 변별력이 없는 단어들 — 매칭 점수 계산에서 제외
_STOP_WORDS = {
    "있다", "없다", "이다", "하다", "되다", "한다", "된다", "있는", "없는",
    "이를", "이에", "이가", "이와", "그리고", "하지", "때문", "대한", "통해",
    "위해", "하여", "것이", "수가", "수도", "수는", "이번", "지금", "오늘",
    "교사", "학생", "교육", "학교", "수업", "학습", "선생", "아이", "우리",
    "the", "and", "for", "that", "this", "with", "from", "have", "are",
}


def find_related_posts(content: str, title: str, max_posts: int = 3) -> list[dict]:
    """입력 콘텐츠와 주제가 겹치는 기존 포스트를 최대 max_posts개 반환.

    Returns:
        [{"title": str, "content": str}, ...]  — 본문은 최대 1,500자로 자름
    """
    # 입력에서 의미 있는 단어 추출 (한글 2자 이상, 영문 3자 이상)
    raw_words = re.findall(r"[가-힣]{2,}|[a-zA-Z]{3,}", content + " " + title)
    keywords = {w for w in raw_words if w not in _STOP_WORDS}

    candidates: list[dict] = []
    for md_file in POSTS_DIR.glob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        fm_match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not fm_match:
            continue
        fm = fm_match.group(1)

        post_title_m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', fm, re.MULTILINE)
        post_title = post_title_m.group(1).strip() if post_title_m else ""
        tags = _parse_yaml_list(fm, "tags")
        cats = _parse_yaml_list(fm, "categories")

        # 제목·태그·카테고리에서 키워드 매칭 수로 점수 산정
        searchable = " ".join([post_title] + tags + cats)
        score = sum(1 for kw in keywords if kw in searchable)

        if score > 0:
            body = re.sub(r"^---\s*\n.*?\n---\s*\n?", "", text, flags=re.DOTALL).strip()
            candidates.append({"title": post_title, "score": score, "content": body[:1500]})

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return [{"title": c["title"], "content": c["content"]} for c in candidates[:max_posts]]


# ──────────────────────────────────────────────────────────────
# YouTube 콘텐츠 추출
# ──────────────────────────────────────────────────────────────

def extract_youtube(url: str) -> tuple[str, str]:
    """(title, transcript) 반환. 자막 없으면 description으로 대체."""
    title = _get_video_title(url)
    transcript = _get_transcript(url)
    if not transcript.strip():
        print("[INFO] 자막 없음 — 영상 설명(description)으로 대체")
        transcript = _get_video_description(url)
    return title, transcript[:MAX_CONTENT_CHARS]


def _get_video_title(url: str) -> str:
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("title", "") or "YouTube 영상"
    except Exception:
        return "YouTube 영상"


def _get_video_description(url: str) -> str:
    try:
        import yt_dlp
        with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get("description", "") or ""
    except Exception:
        return ""


def _get_transcript(url: str) -> str:
    # youtube-transcript-api 시도 (한국어 → 영어 순)
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        video_id = _extract_video_id(url)
        for lang in ["ko", "en"]:
            try:
                entries = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                return " ".join(e["text"] for e in entries)
            except Exception:
                continue
    except Exception:
        pass

    # yt-dlp VTT 자동자막 폴백
    try:
        import yt_dlp
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            ydl_opts = {
                "quiet": True,
                "skip_download": True,
                "writeautomaticsub": True,
                "writesubtitles": True,
                "subtitleslangs": ["ko", "en"],
                "subtitlesformat": "vtt",
                "outtmpl": str(Path(tmp) / "sub"),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for f in sorted(Path(tmp).glob("*.vtt")):
                vtt = f.read_text(encoding="utf-8", errors="ignore")
                lines = [
                    ln for ln in vtt.splitlines()
                    if ln.strip()
                    and not ln.startswith("WEBVTT")
                    and "-->" not in ln
                    and not re.match(r"^\d+$", ln.strip())
                ]
                return " ".join(lines)
    except Exception:
        pass

    return ""


def _extract_video_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc in ("youtu.be",):
        return parsed.path.lstrip("/").split("/")[0]
    path_match = re.match(r"^/(shorts|live)/([A-Za-z0-9_-]{11})", parsed.path)
    if path_match:
        return path_match.group(2)
    qs = parse_qs(parsed.query)
    if "v" in qs and qs["v"]:
        return qs["v"][0]
    raise ValueError(f"YouTube video ID 추출 실패: {url}")


# ──────────────────────────────────────────────────────────────
# 웹 콘텐츠 추출
# ──────────────────────────────────────────────────────────────

def _get_naver_cookies():
    """Chrome/Edge의 Naver 로그인 쿠키를 읽어 반환. 실패 시 None."""
    try:
        import browser_cookie3
        for loader in (browser_cookie3.chrome, browser_cookie3.edge):
            try:
                jar = loader(domain_name=".naver.com")
                if any(True for _ in jar):
                    print("[INFO] browser_cookie3: Naver 쿠키 로드 성공")
                    return jar
            except Exception:
                continue
    except ImportError:
        pass
    naver_cookie = os.environ.get("NAVER_COOKIE", "")
    if naver_cookie:
        import requests
        jar = requests.cookies.RequestsCookieJar()
        for pair in naver_cookie.split(";"):
            pair = pair.strip()
            if "=" in pair:
                k, v = pair.split("=", 1)
                jar.set(k.strip(), v.strip(), domain=".naver.com")
        print("[INFO] env NAVER_COOKIE 사용")
        return jar
    return None


def _naver_mobile_url(url: str) -> str:
    """blog.naver.com → m.blog.naver.com 변환."""
    return url.replace("://blog.naver.com/", "://m.blog.naver.com/", 1)


def extract_web(url: str) -> tuple[str, str]:
    """(title, content) 반환. 본문 부족 시 Jina Reader 폴백."""
    is_naver_blog = "blog.naver.com" in url
    fetch_url = _naver_mobile_url(url) if is_naver_blog else url
    if is_naver_blog and fetch_url != url:
        print(f"[INFO] Naver 모바일 URL로 변환: {fetch_url}")

    is_naver = "naver.com" in url
    cookies = _get_naver_cookies() if is_naver else None
    title, content = _fetch_via_requests(fetch_url, cookies=cookies, mobile=is_naver_blog)
    if len(content) < 500:
        print("[INFO] 본문 부족 — Jina Reader 폴백 시도")
        title2, content2 = _fetch_via_jina(url, cookies=cookies if is_naver else None)
        if len(content2) > len(content):
            title = title2 or title
            content = content2
    return title, content[:MAX_CONTENT_CHARS]


def _fetch_via_requests(url: str, cookies=None, mobile: bool = False) -> tuple[str, str]:
    try:
        import requests
        from bs4 import BeautifulSoup
        if mobile:
            ua = (
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/16.0 Mobile/15E148 Safari/604.1"
            )
        else:
            ua = (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        headers = {
            "User-Agent": ua,
            "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
        }
        resp = requests.get(url, headers=headers, cookies=cookies, timeout=30)
        resp.encoding = resp.apparent_encoding or "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        title = ""
        og = soup.find("meta", property="og:title")
        if og and og.get("content"):
            title = og["content"].strip()
        if not title and soup.title:
            title = soup.title.get_text(strip=True)
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        content = soup.get_text(separator="\n", strip=True)
        return title, content
    except Exception as e:
        print(f"[WARN] requests 추출 실패: {e}")
        return "", ""


def _fetch_via_jina(url: str, cookies=None) -> tuple[str, str]:
    try:
        import requests
        resp = requests.get(f"https://r.jina.ai/{url}", cookies=cookies, timeout=60)
        text = resp.text
        title_match = re.search(r"^Title:\s*(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else ""
        return title, text
    except Exception as e:
        print(f"[WARN] Jina 폴백 실패: {e}")
        return "", ""


# ──────────────────────────────────────────────────────────────
# PDF 콘텐츠 추출
# ──────────────────────────────────────────────────────────────

def extract_pdf(path: str) -> tuple[str, str]:
    """(title, text) 반환. pdfplumber → PyMuPDF 순으로 시도."""
    title = Path(path).stem.replace("-", " ").replace("_", " ")
    text = ""

    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            parts = [page.extract_text() or "" for page in pdf.pages]
        text = "\n".join(p for p in parts if p)
    except Exception as e:
        print(f"[WARN] pdfplumber 실패: {e}")

    if not text.strip():
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(path)
            text = "\n".join(page.get_text() for page in doc)
        except Exception as e:
            print(f"[WARN] PyMuPDF 실패: {e}")

    return title, text[:MAX_CONTENT_CHARS]


# ──────────────────────────────────────────────────────────────
# 일반 파일 추출
# ──────────────────────────────────────────────────────────────

def extract_file(path: str) -> tuple[str, str]:
    """(title, content) 반환. docx 시도 후 텍스트로 읽기."""
    p = Path(path)
    title = p.stem.replace("-", " ").replace("_", " ")

    if p.suffix.lower() == ".docx":
        try:
            import docx
            doc = docx.Document(str(p))
            text = "\n".join(para.text for para in doc.paragraphs)
            return title, text[:MAX_CONTENT_CHARS]
        except ImportError:
            print("[WARN] python-docx 미설치. 텍스트로 읽기 시도.")
        except Exception as e:
            print(f"[WARN] docx 읽기 실패: {e}")

    text = p.read_text(encoding="utf-8", errors="ignore")
    return title, text[:MAX_CONTENT_CHARS]


# ──────────────────────────────────────────────────────────────
# 슬라이드 수 계산
# ──────────────────────────────────────────────────────────────

def calc_slide_range(duration_min: int) -> tuple[int, int]:
    """강의 시간(분) → (최소, 최대) 챕터 수 반환.

    챕터당 평균 45분 분량 (이야기 + 이론 서술 + 토의).
    60분 → 3~4챕터, 120분 → 3~4챕터, 360분 → 7~9챕터.
    """
    n = max(3, min(10, round(duration_min / 45)))
    return max(3, n - 1), n + 1


# ──────────────────────────────────────────────────────────────
# Gemini 호출
# ──────────────────────────────────────────────────────────────

def call_gemini(prompt: str, model: str) -> str:
    try:
        import google.generativeai as genai
    except ImportError:
        raise RuntimeError("google-generativeai 미설치. pip install google-generativeai")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

    genai.configure(api_key=api_key)
    model_obj = genai.GenerativeModel(model)
    response = model_obj.generate_content(prompt)
    return response.text


# ──────────────────────────────────────────────────────────────
# 슬러그 생성 (한국어 제목 → 영문)
# ──────────────────────────────────────────────────────────────

def generate_slug(title: str, model: str) -> str:
    try:
        prompt = (
            f"다음 제목의 영문 kebab-case 슬러그를 생성하세요. "
            f"3~5단어, 20자 이내, 소문자와 하이픈만 사용. 슬러그만 출력하세요.\n\n제목: {title}"
        )
        slug = call_gemini(prompt, model).strip().strip('"').strip("'")
        slug = re.sub(r"[^a-z0-9-]", "", slug.lower()).strip("-")
        return slug or "lecture-script"
    except Exception:
        return re.sub(r"[^a-z0-9]+", "-", title.lower())[:30].strip("-") or "lecture-script"


# ──────────────────────────────────────────────────────────────
# 날짜 버그 수정 (Gemini가 연도를 바꾸는 버그 대응)
# ──────────────────────────────────────────────────────────────

def fix_date(content: str, expected_date: str) -> str:
    def _replace(m: re.Match) -> str:
        suffix = m.group(2)[10:] if len(m.group(2)) > 10 else " 09:00:00 +0900"
        return m.group(1) + expected_date + suffix

    return re.sub(
        r"^(date:\s*)(\d{4}-\d{2}-\d{2}.*)$",
        _replace,
        content,
        flags=re.MULTILINE,
    )


# ──────────────────────────────────────────────────────────────
# git push
# ──────────────────────────────────────────────────────────────

def git_push(file_path: Path, extra_files: "list[Path] | None" = None) -> None:
    try:
        subprocess.run(["git", "stash"], cwd=REPO_ROOT, check=False)
        subprocess.run(["git", "pull", "origin", "main", "--rebase"], cwd=REPO_ROOT, check=False)
        subprocess.run(["git", "stash", "pop"], cwd=REPO_ROOT, check=False)
        subprocess.run(["git", "add", str(file_path)], cwd=REPO_ROOT, check=True)
        for extra in (extra_files or []):
            subprocess.run(["git", "add", str(extra)], cwd=REPO_ROOT, check=False)
        date_str = datetime.now().strftime("%Y%m%d%H%M")
        subprocess.run(
            ["git", "commit", "-m", f"Add: 강의 스크립트 {date_str}"],
            cwd=REPO_ROOT,
            check=True,
        )
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_ROOT, check=True)
        print("[OK] git push 완료")
    except subprocess.CalledProcessError as e:
        print(f"[WARN] git 명령 실패: {e}")


# ──────────────────────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="교사 연수용 강의 스크립트 생성기")
    parser.add_argument("inputs", nargs="+", help="YouTube URL / 웹 URL / PDF 경로 / 파일 경로 (복수 가능)")
    parser.add_argument("--duration", type=int, default=120, help="강의 시간(분) (기본값: 120)")
    parser.add_argument("--level", default="중급", choices=["초급", "중급"], help="강의 수준 (기본값: 중급)")
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="포스트 날짜")
    parser.add_argument("--slug", default="", help="파일명 슬러그")
    parser.add_argument("--no-push", action="store_true", dest="no_push")
    parser.add_argument("--dry-run", action="store_true", dest="dry_run")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--extra", default="", help="Gemini에 추가 지시 (프롬프트 끝에 삽입)")
    args = parser.parse_args()

    input_list = args.inputs
    print(f"[INFO] 입력 {len(input_list)}개 | 강의 시간: {args.duration}분 | 수준: {args.level}")

    # 콘텐츠 추출 (복수 입력 지원)
    titles, contents, source_labels = [], [], []
    for i, input_str in enumerate(input_list, 1):
        input_type = detect_input_type(input_str)
        print(f"[INFO] [{i}/{len(input_list)}] {input_type}: {input_str[:80]}")
        if input_type == "youtube":
            t, c = extract_youtube(input_str)
            source_labels.append(f"YouTube: {t} ({input_str})")
        elif input_type == "web":
            t, c = extract_web(input_str)
            source_labels.append(input_str)
        elif input_type == "pdf":
            t, c = extract_pdf(input_str)
            source_labels.append(Path(input_str).name)
        else:
            t, c = extract_file(input_str)
            source_labels.append(Path(input_str).name)
        if c.strip():
            titles.append(t)
            contents.append(c)
        else:
            print(f"[WARN] 콘텐츠 추출 실패: {input_str}")

    if not contents:
        print("[ERROR] 콘텐츠를 추출할 수 없습니다.")
        sys.exit(1)

    title = titles[0] if len(titles) == 1 else " / ".join(titles)
    content = "\n\n---\n\n".join(contents)
    source_label = "\n".join(source_labels)

    print(f"[INFO] 콘텐츠 추출 완료: {len(content):,}자 ({len(contents)}개 소스)")

    # 슬라이드 수 계산
    slide_min, slide_max = calc_slide_range(args.duration)

    # 관련 포스트 탐색
    related_posts = find_related_posts(content, title)
    if related_posts:
        print(f"[INFO] 관련 포스트 {len(related_posts)}개 발견: {[p['title'] for p in related_posts]}")
        related_posts_text = "\n\n".join(
            f"### {p['title']}\n{p['content']}" for p in related_posts
        )
    else:
        print("[INFO] 관련 포스트 없음")
        related_posts_text = "(관련 포스트 없음)"

    # 기존 분류 체계 수집
    existing_cats, existing_tags = get_existing_taxonomy()

    # 프롬프트 구성
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    date_with_time = f"{args.date} 09:00:00 +0900"
    prompt = (
        template
        .replace("{SOURCE_TITLE}", title)
        .replace("{SOURCE_LABEL}", source_label)
        .replace("{CONTENT}", content)
        .replace("{DURATION}", str(args.duration))
        .replace("{LEVEL}", args.level)
        .replace("{SLIDE_MIN}", str(slide_min))
        .replace("{SLIDE_MAX}", str(slide_max))
        .replace("{DATE_PLACEHOLDER}", date_with_time)
        .replace("{EXISTING_CATEGORIES}", ", ".join(existing_cats[:20]))
        .replace("{EXISTING_TAGS}", ", ".join(existing_tags))
        .replace("{RELATED_POSTS}", related_posts_text)
    )

    if args.extra:
        prompt += f"\n\n---\n\n## 추가 작성 지시\n\n{args.extra}"

    print(f"[INFO] Gemini({args.model}) 연수 교재 생성 중... ({args.level} / 챕터 {slide_min}~{slide_max}개 예상)")
    post_content = call_gemini(prompt, args.model)

    # 날짜 버그 수정
    post_content = fix_date(post_content, args.date)

    # Gemini가 ```markdown...``` 으로 감싸는 경우 제거
    post_content = post_content.strip()
    if post_content.startswith("```"):
        post_content = re.sub(r"^```[^\n]*\n", "", post_content)
        post_content = re.sub(r"\n```\s*$", "", post_content)
        post_content = post_content.strip()

    # 구조 레이블 제거 ([인사이트 갈무리] 등 지시 텍스트가 노출되는 경우)
    post_content = re.sub(r"^\[(?:인사이트 갈무리|케이스 오프너|탐구 에세이 본문)\]\s*\n?", "", post_content, flags=re.MULTILINE)

    # slug 필드 추출 후 front matter에서 제거
    slug = args.slug
    slug_match = re.search(r"^slug:\s*['\"]?([^'\"\n]+)['\"]?", post_content, re.MULTILINE)
    if slug_match:
        if not slug:
            slug = slug_match.group(1).strip()
        post_content = re.sub(r"^slug:.*\n", "", post_content, flags=re.MULTILINE)

    if not slug:
        slug = generate_slug(title, args.model)

    slug = re.sub(r"[^a-z0-9-]", "", slug.lower()).strip("-") or "lecture-script"
    filename = f"{args.date}-{slug}.md"

    if args.dry_run:
        print("\n" + "=" * 60)
        print(post_content)
        print("=" * 60)
        print(f"\n[DRY-RUN] 저장 없이 출력 완료. 예상 파일명: {filename}")
        return

    out_path = POSTS_DIR / filename
    post_content, thumb_path = fetch_and_inject_image(post_content, slug)
    out_path.write_text(post_content, encoding="utf-8")
    print(f"[OK] 저장 완료: {out_path}")

    if not args.no_push:
        git_push(out_path, extra_files=[thumb_path] if thumb_path else None)


if __name__ == "__main__":
    main()
