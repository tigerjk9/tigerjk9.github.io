#!/usr/bin/env python3
"""
image_fetcher.py — 이미지 검색·삽입 공용 모듈

우선순위:
  1. ## 출처 URL에서 OG/트위터 이미지 추출
  2. DuckDuckGo 이미지 웹서치 (API 키 불필요)
  3. Pexels API 폴백 (PEXELS_API_KEY 필요)

4개 자동화 스크립트 공유.
"""

from __future__ import annotations

import os
import re
import ssl
import requests
import urllib3
from pathlib import Path
from typing import Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ASSETS_DIR = Path(__file__).parent.parent / "assets"

_SESSION: Optional[requests.Session] = None


def _session() -> requests.Session:
    """SSL 우회 설정된 공용 requests 세션."""
    global _SESSION
    if _SESSION is None:
        _SESSION = requests.Session()
        _SESSION.verify = False
        _SESSION.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        })
    return _SESSION


# ---------------------------------------------------------------------------
# 검색어·URL 추출
# ---------------------------------------------------------------------------

def _extract_query(markdown_content: str) -> str:
    """front matter title + tags에서 이미지 검색어를 만든다."""
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', markdown_content, re.MULTILINE)
    tags_match = re.search(r'^tags:\s*\[(.+?)\]', markdown_content, re.MULTILINE)

    parts: list[str] = []
    if title_match:
        parts.extend(title_match.group(1).split()[:3])
    if tags_match:
        raw_tags = [t.strip().strip("\"'") for t in tags_match.group(1).split(",")]
        parts.extend(raw_tags[:2])

    return " ".join(parts[:5]) if parts else "education"


def _extract_source_urls(markdown_content: str) -> list[str]:
    """## 출처 섹션에서 HTTP URL 목록을 추출한다."""
    match = re.search(r'## 출처\s*\n(.*?)(?=\n## |\Z)', markdown_content, re.DOTALL)
    if not match:
        return []
    return re.findall(r'https?://[^\s\)\]\'"]+', match.group(1))


# ---------------------------------------------------------------------------
# 1순위: 출처 URL OG 이미지
# ---------------------------------------------------------------------------

def _fetch_og_image_url(page_url: str) -> Optional[str]:
    """HTML 페이지에서 og:image / twitter:image URL을 추출한다."""
    try:
        from bs4 import BeautifulSoup
        resp = _session().get(page_url, timeout=10, allow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for prop in ("og:image", "twitter:image", "og:image:url"):
            tag = (
                soup.find("meta", property=prop)
                or soup.find("meta", attrs={"name": prop})
            )
            if tag and tag.get("content"):
                url = tag["content"].strip()
                if url.startswith("//"):
                    url = "https:" + url
                if url.startswith("/"):
                    from urllib.parse import urlparse
                    parsed = urlparse(page_url)
                    url = f"{parsed.scheme}://{parsed.netloc}{url}"
                return url
    except Exception:
        pass
    return None


def _try_og_image(markdown_content: str, slug: str) -> Optional[Path]:
    """## 출처 URL들에서 OG 이미지를 시도한다."""
    urls = _extract_source_urls(markdown_content)
    if not urls:
        return None

    for url in urls[:3]:
        print(f"[INFO] OG 이미지 시도: {url[:70]}...")
        img_url = _fetch_og_image_url(url)
        if not img_url:
            continue

        result = _download_image(img_url, slug, source_label="OG")
        if result:
            return result

    return None


# ---------------------------------------------------------------------------
# 2순위: DuckDuckGo 이미지 검색
# ---------------------------------------------------------------------------

def _try_ddg_image(query: str, slug: str) -> Optional[Path]:
    """DuckDuckGo 이미지 검색으로 관련 이미지를 가져온다."""
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        print("[INFO] duckduckgo-search 미설치 - DDG 검색 건너뜀 (pip install duckduckgo-search)")
        return None

    print(f"[INFO] DDG 이미지 검색: {query!r}")
    try:
        # verify=False: 기업 네트워크 SSL 우회
        with DDGS(verify=False) as ddgs:
            results = list(ddgs.images(
                query,
                max_results=15,
                type_image="photo",
                layout="Wide",
            ))
    except Exception as exc:
        print(f"[WARN] DDG 검색 실패: {exc}")
        return None

    for r in results:
        img_url = r.get("image", "")
        w, h = r.get("width", 0), r.get("height", 0)
        if not img_url or w < 400 or h < 200:
            continue

        result = _download_image(
            img_url, slug,
            source_label=f"DDG({r.get('source', '')[:30]})"
        )
        if result:
            return result

    print("[WARN] DDG 결과에서 유효한 이미지를 찾지 못함")
    return None


# ---------------------------------------------------------------------------
# 3순위: Pexels 폴백
# ---------------------------------------------------------------------------

def _try_pexels_image(query: str, slug: str) -> Optional[Path]:
    """Pexels에서 이미지를 검색한다 (폴백)."""
    api_key = os.getenv("PEXELS_API_KEY", "").strip()
    if not api_key:
        return None

    print(f"[INFO] Pexels 폴백: {query!r}")
    try:
        resp = _session().get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": api_key},
            params={"query": query, "per_page": 3, "orientation": "landscape"},
            timeout=10,
        )
        resp.raise_for_status()
        photos = resp.json().get("photos", [])
        if not photos:
            print(f"[WARN] Pexels 검색 결과 없음: {query!r}")
            return None

        img_url = photos[0]["src"]["large2x"]
        return _download_image(img_url, slug, source_label="Pexels")

    except Exception as exc:
        print(f"[WARN] Pexels 실패: {exc}")
        return None


# ---------------------------------------------------------------------------
# 공통 다운로드 헬퍼
# ---------------------------------------------------------------------------

def _download_image(img_url: str, slug: str, source_label: str = "") -> Optional[Path]:
    """이미지 URL을 다운로드해 assets/{slug}-thumb.{ext}에 저장한다."""
    try:
        resp = _session().get(img_url, timeout=20, allow_redirects=True)
        resp.raise_for_status()

        content_type = resp.headers.get("content-type", "").lower()
        if not content_type.startswith("image/"):
            return None
        if len(resp.content) < 5_000:  # 5KB 미만은 아이콘·플레이스홀더 제외
            return None

        if "png" in content_type:
            ext = "png"
        elif "webp" in content_type:
            ext = "webp"
        else:
            ext = "jpg"

        ASSETS_DIR.mkdir(exist_ok=True)
        filename = f"{slug}-thumb.{ext}"
        img_path = ASSETS_DIR / filename
        img_path.write_bytes(resp.content)

        label = f" [{source_label}]" if source_label else ""
        print(f"[OK] 이미지 저장{label}: /assets/{filename} ({len(resp.content)//1024}KB)")
        return img_path

    except Exception as exc:
        print(f"[WARN] 이미지 다운로드 실패 ({source_label}): {exc}")
        return None


# ---------------------------------------------------------------------------
# front matter / 본문 삽입
# ---------------------------------------------------------------------------

def _inject_teaser(content: str, img_path: str) -> str:
    """front matter에 header.teaser를 삽입한다. 이미 있으면 교체한다."""
    first = content.find("---")
    second = content.find("---", first + 3)
    if first == -1 or second == -1:
        return content

    fm = content[first:second]
    rest = content[second:]

    if "header:" in fm:
        if "teaser:" in fm:
            fm = re.sub(r"(\s+teaser:)\s*.+", f"\\1 {img_path}", fm)
        else:
            fm = re.sub(r"(header:\s*\n)", f"\\1  teaser: {img_path}\n", fm)
    else:
        fm = fm.rstrip("\n") + f"\nheader:\n  teaser: {img_path}\n"

    return fm + rest


def _inject_figure(content: str, img_path: str, alt: str = "") -> str:
    """첫 번째 ## 섹션 직전에 <figure> 블록을 삽입한다."""
    figure = f'\n<figure>\n<img src="{img_path}" alt="{alt}">\n</figure>\n'

    first = content.find("---")
    fm_end = content.find("---", first + 3)
    fm_end = content.find("\n", fm_end) + 1

    match = re.search(r"\n(## )", content[fm_end:])
    if not match:
        return content

    insert_pos = fm_end + match.start()
    return content[:insert_pos] + figure + content[insert_pos:]


def _extract_title(markdown_content: str) -> str:
    """front matter에서 title 값을 추출한다."""
    m = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', markdown_content, re.MULTILINE)
    return m.group(1).strip() if m else ""


# ---------------------------------------------------------------------------
# 공개 진입점
# ---------------------------------------------------------------------------

def fetch_and_inject_image(
    markdown_content: str,
    slug: str,
) -> tuple[str, Optional[Path]]:
    """
    이미지를 우선순위대로 검색해 assets/{slug}-thumb.{ext}에 저장하고
    front matter(header.teaser)와 본문(<figure>)에 삽입한다.

    우선순위:
      1. ## 출처 URL에서 OG 이미지
      2. DuckDuckGo 이미지 웹서치
      3. Pexels API (PEXELS_API_KEY 필요)
    """
    query = _extract_query(markdown_content)
    alt = _extract_title(markdown_content)

    # 1순위
    img_path = _try_og_image(markdown_content, slug)

    # 2순위
    if img_path is None:
        img_path = _try_ddg_image(query, slug)

    # 3순위
    if img_path is None:
        img_path = _try_pexels_image(query, slug)

    if img_path is None:
        print("[INFO] 이미지 삽입 건너뜀 - 모든 소스 실패")
        return markdown_content, None

    rel_path = f"/assets/{img_path.name}"
    markdown_content = _inject_teaser(markdown_content, rel_path)
    markdown_content = _inject_figure(markdown_content, rel_path, alt=alt)

    return markdown_content, img_path
