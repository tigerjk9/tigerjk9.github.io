#!/usr/bin/env python3
"""
web_to_post.py — 웹 아티클을 패러프레이즈해 Jekyll 블로그 포스트로 자동 변환

사용법:
  python scripts/web_to_post.py <URL> [옵션]

옵션:
  --date  YYYY-MM-DD   포스트 날짜 (기본값: 오늘)
  --slug  SLUG         파일명 슬러그 (기본값: 제목에서 자동 생성)
  --no-push            로컬 저장만 하고 git push 하지 않음
  --dry-run            _posts/ 에 저장하지 않고 터미널에 출력만
  --model  MODEL       Gemini 모델 ID (기본값: gemini-2.5-flash)

환경변수:
  GEMINI_API_KEY       Google AI Studio API 키 (필수) — .env 파일에 저장 권장
"""

from __future__ import annotations

import argparse
import io
import os
import random
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

# Windows 터미널 한글 깨짐 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ──────────────────────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
POSTS_DIR = REPO_ROOT / "_posts"
PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "web_prompt_template.txt"
MULTI_PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "web_multi_prompt_template.txt"
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_CONTENT_CHARS = 80000
MAX_CONTENT_CHARS_PER_URL = 40000  # 복수 URL 시 출처당 최대 글자 수

CROSSOVER_DOMAINS = [
    "신경과학",
    "행동경제학",
    "생태학·먹이그물 이론",
    "언어학·인지언어학",
    "음악이론·즉흥연주",
    "요리과학·발효학",
    "스포츠과학·운동학습",
    "도시계획·공간행동학",
    "연극학·서사이론",
    "진화생물학·공진화",
    "철학·인식론",
    "인류학·문화진화론",
    "물리학·복잡계 이론",
    "면역학·항상성",
    "경제사·제도경제학",
    "게임이론·협력의 진화",
    "수면과학·기억 공고화",
    "동물행동학·각인 이론",
    "기상학·카오스 이론",
    "정보이론·엔트로피",
]


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
# SSL 인증서 검증 우회
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
# 기존 카테고리/태그 수집
# ──────────────────────────────────────────────────────────────

def get_existing_taxonomy() -> "tuple[list[str], list[str]]":
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
    sorted_cats = [c for c, _ in cat_counter.most_common()]
    sorted_tags = [t for t, _ in tag_counter.most_common(40)]
    return sorted_cats, sorted_tags


def _parse_yaml_list(front_matter: str, key: str) -> "list[str]":
    items: "list[str]" = []
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
# 웹 콘텐츠 추출
# ──────────────────────────────────────────────────────────────

MIN_CONTENT_CHARS = 500  # 이 미만이면 JS 렌더링 페이지로 판단, Jina 폴백 시도


def _fetch_via_requests(url: str) -> "tuple[str, str, str]":
    """requests + BeautifulSoup으로 웹 페이지 콘텐츠 추출."""
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
    }

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding or "utf-8"

    soup = BeautifulSoup(resp.text, "html.parser")

    # 제목 추출: og:title > <title> > <h1>
    title = ""
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    if not title and soup.title:
        title = soup.title.get_text(strip=True)
    if not title:
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
    title = title or "제목 없음"

    # 사이트명 추출: og:site_name > 도메인
    site_name = ""
    og_site = soup.find("meta", property="og:site_name")
    if og_site and og_site.get("content"):
        site_name = og_site["content"].strip()
    if not site_name:
        site_name = urlparse(url).netloc

    # 불필요한 태그 제거
    for tag in soup.find_all(["script", "style", "nav", "header", "footer",
                               "aside", "noscript", "iframe", "form",
                               "button", "input", "select", "textarea"]):
        tag.decompose()
    for tag in soup.find_all(True, {"class": re.compile(
        r"(nav|menu|sidebar|footer|header|ad|cookie|popup|modal|banner|"
        r"comment|related|share|social|recommend)", re.I
    )}):
        tag.decompose()

    # 본문 영역: <article> > <main> > 텍스트 최대 블록
    content_el = soup.find("article") or soup.find("main")
    if not content_el:
        candidates = soup.find_all(["div", "section"])
        if candidates:
            content_el = max(candidates, key=lambda el: len(el.get_text()))
        else:
            content_el = soup.body or soup

    content_text = content_el.get_text(separator="\n", strip=True) if content_el else ""
    content_text = re.sub(r"\n{3,}", "\n\n", content_text)
    return title, site_name, content_text[:MAX_CONTENT_CHARS]


def _fetch_via_jina(url: str) -> "tuple[str, str, str]":
    """Jina Reader (r.jina.ai)로 JS 렌더링 페이지 콘텐츠 추출.

    JS 렌더링 사이트에서 requests가 실패하거나 내용이 너무 짧을 때 폴백으로 사용.
    반환값: (title, site_name, content_text)
    """
    import requests

    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        "Accept": "text/plain",
        "X-Return-Format": "text",
    }
    print("[INFO] Jina Reader로 재시도 중 (JS 렌더링 페이지 대응)...")
    resp = requests.get(jina_url, headers=headers, timeout=60)
    resp.raise_for_status()
    text = resp.text.strip()

    # Jina 응답에서 제목 추출 (첫 번째 # 헤딩 또는 Title: 라인)
    title = ""
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("Title:"):
            title = line[len("Title:"):].strip()
            break
        if line.startswith("# "):
            title = line[2:].strip()
            break
    title = title or urlparse(url).netloc

    site_name = urlparse(url).netloc
    content_text = re.sub(r"\n{3,}", "\n\n", text)
    return title, site_name, content_text[:MAX_CONTENT_CHARS]


def fetch_web_content(url: str) -> "tuple[str, str, str]":
    """URL에서 제목·사이트명·본문 텍스트 추출.

    1차: requests + BeautifulSoup
    2차: 본문이 너무 짧으면 Jina Reader 폴백 (JS 렌더링 사이트 대응)

    Returns:
        (title, site_name, content_text)
    """
    try:
        import requests  # noqa: F401
    except ImportError:
        raise RuntimeError("requests가 설치되지 않았습니다.\npip install requests")

    try:
        import bs4  # noqa: F401
    except ImportError:
        raise RuntimeError("beautifulsoup4가 설치되지 않았습니다.\npip install beautifulsoup4")

    print(f"[INFO] 웹 페이지 가져오는 중: {url}")
    title, site_name, content_text = _fetch_via_requests(url)
    print(f"[INFO] 1차 추출 — 제목: {title}, 본문: {len(content_text):,}자")

    if len(content_text) < MIN_CONTENT_CHARS:
        print(f"[WARN] 본문이 {MIN_CONTENT_CHARS}자 미만 — JS 렌더링 페이지로 추정")
        try:
            jina_title, jina_site, jina_content = _fetch_via_jina(url)
            if len(jina_content) > len(content_text):
                title = jina_title or title
                site_name = jina_site or site_name
                content_text = jina_content
                print(f"[INFO] Jina Reader 추출 성공 — 본문: {len(content_text):,}자")
            else:
                print("[WARN] Jina Reader도 내용 부족 — 1차 결과 유지")
        except Exception as e:
            print(f"[WARN] Jina Reader 실패: {e} — 1차 결과로 계속 진행")

    print(f"[INFO] 최종 추출 완료 — 제목: {title}, 사이트: {site_name}, 본문: {len(content_text):,}자")
    return title, site_name, content_text


# ──────────────────────────────────────────────────────────────
# 프롬프트 로드
# ──────────────────────────────────────────────────────────────

def load_prompt_template(
    date_str: str,
    url: str,
    title: str,
    site_name: str,
    content: str,
    categories: "list[str]",
    tags: "list[str]",
) -> "tuple[str, str]":
    if not PROMPT_TEMPLATE_PATH.exists():
        raise RuntimeError(f"프롬프트 템플릿을 찾을 수 없습니다: {PROMPT_TEMPLATE_PATH}")
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")

    cats_str = ", ".join(categories) if categories else "AI, 교육"
    tags_str = ", ".join(tags) if tags else "AI, 교육"
    time_str = datetime.now().strftime("%H:%M:%S")
    crossover_domain = random.choice(CROSSOVER_DOMAINS)

    template = template.replace("{DATE_PLACEHOLDER}", f"{date_str} {time_str}")
    template = template.replace("{PAGE_TITLE}", title)
    template = template.replace("{PAGE_URL}", url)
    template = template.replace("{SITE_NAME}", site_name)
    template = template.replace("{PAGE_CONTENT}", content)
    template = template.replace("{EXISTING_CATEGORIES}", cats_str)
    template = template.replace("{EXISTING_TAGS}", tags_str)
    template = template.replace("{CROSSOVER_DOMAIN}", crossover_domain)
    return template, crossover_domain


# ──────────────────────────────────────────────────────────────
# 복수 URL 프롬프트 로드
# ──────────────────────────────────────────────────────────────

def load_multi_prompt_template(
    date_str: str,
    sources: "list[tuple[str, str, str, str]]",  # [(url, title, site_name, content), ...]
    categories: "list[str]",
    tags: "list[str]",
) -> "tuple[str, str]":
    if not MULTI_PROMPT_TEMPLATE_PATH.exists():
        raise RuntimeError(f"멀티 프롬프트 템플릿을 찾을 수 없습니다: {MULTI_PROMPT_TEMPLATE_PATH}")
    template = MULTI_PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")

    multi_sources_blocks = []
    for i, (url, title, site_name, content) in enumerate(sources, 1):
        block = (
            f"### [출처 {i}] {title}\n"
            f"- URL: {url}\n"
            f"- 사이트: {site_name}\n\n"
            f"{content}"
        )
        multi_sources_blocks.append(block)
    multi_sources_str = "\n\n---\n\n".join(multi_sources_blocks)

    multi_urls_str = "\n".join(f"- {url}" for url, _, _, _ in sources)

    cats_str = ", ".join(categories) if categories else "AI, 교육"
    tags_str = ", ".join(tags) if tags else "AI, 교육"
    time_str = datetime.now().strftime("%H:%M:%S")
    crossover_domain = random.choice(CROSSOVER_DOMAINS)

    template = template.replace("{DATE_PLACEHOLDER}", f"{date_str} {time_str}")
    template = template.replace("{MULTI_SOURCES}", multi_sources_str)
    template = template.replace("{MULTI_URLS}", multi_urls_str)
    template = template.replace("{EXISTING_CATEGORIES}", cats_str)
    template = template.replace("{EXISTING_TAGS}", tags_str)
    template = template.replace("{CROSSOVER_DOMAIN}", crossover_domain)
    return template, crossover_domain


# ──────────────────────────────────────────────────────────────
# Gemini API
# ──────────────────────────────────────────────────────────────

def call_gemini_api(prompt: str, model: str) -> str:
    try:
        import google.generativeai as genai
    except ImportError:
        raise RuntimeError(
            "google-generativeai 패키지가 설치되지 않았습니다.\n"
            "pip install -r scripts/requirements.txt"
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")

    genai.configure(api_key=api_key)
    print(f"[INFO] Gemini API 호출 중 (모델: {model}) ...")
    gemini_model = genai.GenerativeModel(model_name=model)
    response = gemini_model.generate_content(prompt)
    return _strip_code_fence(response.text)


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    stripped = re.sub(r"^```\w*\s*\n", "", text)
    if stripped != text:
        stripped = re.sub(r"\n```\s*$", "", stripped)
        return stripped.strip()
    return text


def _fix_date(text: str, correct_date_str: str) -> str:
    return re.sub(
        r"^date:.*$",
        f"date: {correct_date_str} +0900",
        text,
        flags=re.MULTILINE,
    )


# ──────────────────────────────────────────────────────────────
# 포스트 생성 유틸리티
# ──────────────────────────────────────────────────────────────

def slugify(text: str, max_len: int = 60) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\-]", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    text = text.strip("-")
    return text[:max_len].rstrip("-")


def extract_slug_from_content(content: str) -> "str | None":
    m = re.search(r"^slug:\s*[\"']?([a-z0-9][a-z0-9\-]{1,40})[\"']?\s*$", content, re.MULTILINE)
    return m.group(1).strip("-") if m else None


def remove_slug_field(content: str) -> str:
    return re.sub(r"^slug:.*\n", "", content, flags=re.MULTILINE)


def build_filename(date_str: str, slug: str) -> str:
    filename = f"{date_str}-{slug}.md"
    output_path = POSTS_DIR / filename
    if output_path.exists():
        ts = datetime.now().strftime("%H%M%S")
        filename = f"{date_str}-{slug}-{ts}.md"
        print(f"[WARN] 파일명 충돌 - 타임스탬프 추가: {filename}")
    return filename


def save_post(content: str, output_path: Path) -> None:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] 포스트 저장 완료: {output_path}")


# ──────────────────────────────────────────────────────────────
# Git
# ──────────────────────────────────────────────────────────────

def _git(args: "list[str]", check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {args[0]} 실패:\n{result.stderr.strip()}")
    return result


def git_commit_and_push(file_paths: "list[Path]", commit_msg: str) -> None:
    _git(["add", "--", *[str(fp) for fp in file_paths]])
    print(f"[OK] git add 완료 ({len(file_paths)}개 파일)")
    _git(["commit", "-m", commit_msg])
    print("[OK] git commit 완료")
    result = _git(["push", "origin", "main"], check=False)
    if result.returncode != 0:
        print("[WARN] git push 실패. 수동으로 push 하세요.")
        print("  → git push origin main")
        print(f"  상세: {result.stderr.strip()}")
    else:
        print("[OK] git push 완료")


# ──────────────────────────────────────────────────────────────
# Jekyll 설정 확인
# ──────────────────────────────────────────────────────────────

def ensure_timezone_config() -> bool:
    config_path = REPO_ROOT / "_config.yml"
    if not config_path.exists():
        return False
    content = config_path.read_text(encoding="utf-8")
    if re.search(r"^timezone:\s*Asia/Seoul\s*$", content, re.MULTILINE):
        return False
    new_content = re.sub(
        r"^timezone:.*$", "timezone: Asia/Seoul", content, flags=re.MULTILINE
    )
    if new_content == content:
        return False
    config_path.write_text(new_content, encoding="utf-8")
    print("[INFO] _config.yml timezone → Asia/Seoul 자동 수정")
    return True


# ──────────────────────────────────────────────────────────────
# 진입점
# ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="웹 아티클을 패러프레이즈해 Jekyll 블로그 포스트로 자동 변환합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "예시:\n"
            "  python scripts/web_to_post.py https://example.com/article\n"
            "  python scripts/web_to_post.py https://a.com/1 https://b.com/2  # 통합 포스트\n"
            "  python scripts/web_to_post.py https://example.com/article --dry-run\n"
            "  python scripts/web_to_post.py https://example.com/article --no-push"
        ),
    )
    parser.add_argument("urls", nargs="+", help="웹 페이지 URL (복수 지정 시 하나의 통합 포스트 생성)")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="포스트 날짜 YYYY-MM-DD (기본값: 오늘)",
    )
    parser.add_argument("--slug", default=None, help="파일명 슬러그 (기본값: 제목에서 자동 생성)")
    parser.add_argument("--no-push", action="store_true", help="로컬 저장만 하고 git push 하지 않음")
    parser.add_argument("--dry-run", action="store_true", help="_posts/ 에 저장하지 않고 터미널에 출력만")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Gemini 모델 ID (기본값: {DEFAULT_MODEL})")
    args = parser.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        print("[ERROR] GEMINI_API_KEY 환경변수가 설정되지 않았습니다.\n  export GEMINI_API_KEY=AIza...")
        sys.exit(1)

    config_modified = ensure_timezone_config()

    # 기존 카테고리/태그 수집
    print("[INFO] 기존 카테고리/태그 수집 중...")
    existing_cats, existing_tags = get_existing_taxonomy()
    print(f"[INFO] 기존 카테고리 {len(existing_cats)}개, 태그 {len(existing_tags)}개 확인")

    is_multi = len(args.urls) > 1

    if is_multi:
        # ── 복수 URL: 모두 가져와서 통합 포스트 생성 ──
        print(f"[INFO] 복수 URL 모드 — {len(args.urls)}개 출처를 통합해 포스트 생성")
        per_url_limit = max(MAX_CONTENT_CHARS_PER_URL, MAX_CONTENT_CHARS // len(args.urls))
        sources: "list[tuple[str, str, str, str]]" = []
        for url in args.urls:
            try:
                title, site_name, content_text = fetch_web_content(url)
            except Exception as e:
                print(f"[ERROR] 웹 페이지 가져오기 실패 ({url}): {e}")
                sys.exit(1)
            if not content_text.strip():
                print(f"[ERROR] 본문 텍스트를 추출할 수 없습니다: {url}")
                sys.exit(1)
            sources.append((url, title, site_name, content_text[:per_url_limit]))

        try:
            prompt, crossover_domain = load_multi_prompt_template(
                args.date, sources, existing_cats, existing_tags,
            )
            print(f"[INFO] 크로스오버 분야: {crossover_domain}")
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

        source_label = ", ".join(args.urls)
        fallback_title = " + ".join(t for _, t, _, _ in sources)
    else:
        # ── 단일 URL ──
        url = args.urls[0]
        try:
            title, site_name, content_text = fetch_web_content(url)
        except Exception as e:
            print(f"[ERROR] 웹 페이지 가져오기 실패: {e}")
            sys.exit(1)

        if not content_text.strip():
            print("[ERROR] 본문 텍스트를 추출할 수 없습니다. URL을 확인하세요.")
            sys.exit(1)

        try:
            prompt, crossover_domain = load_prompt_template(
                args.date, url, title, site_name, content_text,
                existing_cats, existing_tags,
            )
            print(f"[INFO] 크로스오버 분야: {crossover_domain}")
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

        source_label = url
        fallback_title = title

    # Gemini API 호출
    try:
        markdown_content = call_gemini_api(prompt, args.model)
    except RuntimeError as e:
        print(f"[ERROR] Gemini API 호출 실패: {e}")
        sys.exit(1)

    # 날짜 복원
    correct_date = f"{args.date} {datetime.now().strftime('%H:%M:%S')}"
    markdown_content = _fix_date(markdown_content, correct_date)

    # 슬러그 확정: CLI 옵션 > Gemini front matter > 제목 폴백
    if args.slug:
        slug = args.slug
    else:
        gemini_slug = extract_slug_from_content(markdown_content)
        if gemini_slug:
            slug = gemini_slug
            print(f"[INFO] 슬러그 (Gemini 생성): {slug}")
        else:
            slug = slugify(fallback_title)[:50] or "web-post"
            print(f"[INFO] 슬러그 (제목 폴백): {slug}")

    markdown_content = remove_slug_field(markdown_content)
    print("[INFO] 포스트 생성 완료")

    if args.dry_run:
        print("\n" + "=" * 60)
        print(markdown_content)
        print("=" * 60)
        print("\n[dry-run] 파일 저장 및 git push를 건너뜁니다.")
        return

    filename = build_filename(args.date, slug)
    output_path = POSTS_DIR / filename
    save_post(markdown_content, output_path)

    if not args.no_push:
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', markdown_content, re.MULTILINE)
        short_title = title_match.group(1)[:50] if title_match else fallback_title[:50]
        commit_msg = (
            f"Add: {short_title}\n\n"
            f"Auto-generated by web_to_post.py\n"
            f"Source: {source_label}"
        )
        all_files = [output_path]
        if config_modified:
            all_files.append(REPO_ROOT / "_config.yml")
        try:
            git_commit_and_push(all_files, commit_msg)
        except RuntimeError as e:
            print(f"[ERROR] git 오류: {e}")
    else:
        print("[INFO] --no-push 옵션으로 git push를 건너뜁니다.")
        print(f"  수동 push: git add \"{output_path}\" && git commit -m 'Add: {slug}' && git push origin main")

    print(f"\n완료! 생성된 포스트: {output_path}")


if __name__ == "__main__":
    main()
