#!/usr/bin/env python3
"""
image_fetcher.py — Pexels 이미지 검색 후 포스트에 자동 삽입

web_to_post, yt_to_post, pdf_to_post, lecture_script 공용 모듈.
PEXELS_API_KEY 환경변수가 없으면 아무것도 하지 않고 원본 콘텐츠를 반환한다.
"""

from __future__ import annotations

import os
import re
import requests
from pathlib import Path
from typing import Optional

ASSETS_DIR = Path(__file__).parent.parent / "assets"


def _extract_query(markdown_content: str) -> str:
    """front matter의 title과 tags에서 Pexels 검색어를 추출한다."""
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', markdown_content, re.MULTILINE)
    tags_match = re.search(r'^tags:\s*\[(.+?)\]', markdown_content, re.MULTILINE)

    parts: list[str] = []
    if title_match:
        parts.extend(title_match.group(1).split()[:3])
    if tags_match:
        raw_tags = [t.strip().strip("\"'") for t in tags_match.group(1).split(",")]
        parts.extend(raw_tags[:2])

    return " ".join(parts[:5]) if parts else "education"


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


def _inject_figure(content: str, img_path: str) -> str:
    """첫 번째 ## 섹션 직전에 <figure> 블록을 삽입한다."""
    figure = f'\n<figure>\n<img src="{img_path}" alt="">\n</figure>\n'

    first = content.find("---")
    fm_end = content.find("---", first + 3)
    fm_end = content.find("\n", fm_end) + 1

    match = re.search(r"\n(## )", content[fm_end:])
    if not match:
        return content

    insert_pos = fm_end + match.start()
    return content[:insert_pos] + figure + content[insert_pos:]


def fetch_and_inject_image(
    markdown_content: str,
    slug: str,
) -> tuple[str, Optional[Path]]:
    """
    Pexels에서 이미지를 검색해 assets/{slug}-thumb.jpg 에 저장하고
    front matter(header.teaser)와 본문(<figure>)에 삽입한다.
    PEXELS_API_KEY 가 없거나 실패 시 원본 콘텐츠와 None 을 반환한다.
    """
    api_key = os.getenv("PEXELS_API_KEY", "").strip()
    if not api_key:
        print("[INFO] PEXELS_API_KEY 없음 - 이미지 삽입 건너뜀")
        return markdown_content, None

    query = _extract_query(markdown_content)
    print(f"[INFO] Pexels 이미지 검색: {query!r}")

    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        search_resp = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": api_key},
            params={"query": query, "per_page": 3, "orientation": "landscape"},
            timeout=10,
            verify=False,
        )
        search_resp.raise_for_status()
        photos = search_resp.json().get("photos", [])

        if not photos:
            print(f"[WARN] Pexels 검색 결과 없음: {query!r}")
            return markdown_content, None

        img_url = photos[0]["src"]["large2x"]
        img_resp = requests.get(img_url, timeout=30, verify=False)
        img_resp.raise_for_status()

        ASSETS_DIR.mkdir(exist_ok=True)
        filename = f"{slug}-thumb.jpg"
        img_path = ASSETS_DIR / filename
        img_path.write_bytes(img_resp.content)

        rel_path = f"/assets/{filename}"
        print(f"[OK] 이미지 저장: {rel_path}")

        markdown_content = _inject_teaser(markdown_content, rel_path)
        markdown_content = _inject_figure(markdown_content, rel_path)

        return markdown_content, img_path

    except Exception as exc:
        print(f"[WARN] 이미지 삽입 실패: {exc}")
        return markdown_content, None
