#!/usr/bin/env python3
"""
image_fetcher.py — 이미지 검색·삽입 공용 모듈

우선순위:
  1. 사용자 제공 소스 이미지 (YouTube 썸네일, PDF figure, 웹 OG 이미지)
  2. ## 출처 URL에서 OG/트위터 이미지 추출 (source_images 미제공 시 첫 마커만)
  3. Pexels API (PEXELS_API_KEY 필요, 고품질 큐레이션)
  4. DuckDuckGo 이미지 웹서치 (API 키 불필요, 최후 폴백)

4개 자동화 스크립트 공유.
"""

from __future__ import annotations

import hashlib
import os
import re
import ssl
import random
import requests
import urllib3
from collections import Counter
from pathlib import Path
from typing import Optional

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ASSETS_DIR = Path(__file__).parent.parent / "assets"
POSTS_DIR = Path(__file__).parent.parent / "_posts"

_SESSION: Optional[requests.Session] = None
_USED_OG_URLS: set[str] = set()  # 세션 내 사용한 OG URL 캐시 (같은 도메인 기본값 감지)


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


def _get_existing_src_hashes() -> set[str]:
    """assets/ 내 기존 *-src*-thumb.* 파일의 MD5 해시 집합을 반환한다.
    site-wide 기본 OG 이미지 감지에 사용한다."""
    hashes: set[str] = set()
    for f in ASSETS_DIR.glob("*-src*-thumb.*"):
        try:
            hashes.add(hashlib.md5(f.read_bytes()).hexdigest())
        except Exception:
            pass
    return hashes


def _is_duplicate_src_image(img_path: Path, existing_hashes: set[str]) -> bool:
    """다운로드한 이미지가 기존 src 이미지와 동일한지 확인한다.
    True이면 site-wide 기본값으로 간주해 폴백 처리한다."""
    try:
        return hashlib.md5(img_path.read_bytes()).hexdigest() in existing_hashes
    except Exception:
        return False


def _try_og_image(markdown_content: str, slug: str) -> Optional[Path]:
    """## 출처 URL들에서 OG 이미지를 시도한다. site-wide 기본값이면 None 반환."""
    urls = _extract_source_urls(markdown_content)
    if not urls:
        return None

    existing_hashes = _get_existing_src_hashes()

    for url in urls[:3]:
        print(f"[INFO] OG 이미지 시도: {url[:70]}...")
        img_url = _fetch_og_image_url(url)
        if not img_url:
            continue

        # 세션 내 URL 중복 → site-wide 기본값으로 추정
        if img_url in _USED_OG_URLS:
            print(f"[WARN] OG URL 중복 감지 - site-wide 기본값으로 추정, Pexels/DDG 폴백")
            continue

        result = _download_image(img_url, slug, source_label="OG")
        if not result:
            continue

        # 파일 해시 중복 → 기존 포스트와 동일 이미지 → site-wide 기본값
        if existing_hashes and _is_duplicate_src_image(result, existing_hashes):
            print(f"[WARN] OG 이미지 중복 감지 (기존 포스트와 동일) - Pexels/DDG 폴백")
            result.unlink(missing_ok=True)
            continue

        _USED_OG_URLS.add(img_url)
        return result

    return None


# ---------------------------------------------------------------------------
# 3순위: DuckDuckGo 이미지 검색 (최후 폴백)
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
# 2순위: Pexels (API 키 지정 고품질 이미지)
# ---------------------------------------------------------------------------

def _try_pexels_image(query: str, slug: str) -> Optional[Path]:
    """Pexels에서 이미지를 검색한다 (API 키 필요, DDG 이전 2순위)."""
    api_key = os.getenv("PEXELS_API_KEY", "").strip()
    if not api_key:
        return None

    print(f"[INFO] Pexels 검색: {query!r}")
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


def _use_source_image(source: "Path | str", img_slug: str) -> "Optional[Path]":
    """소스 이미지 준비. Path이면 파일 존재 확인 후 그대로 반환, URL 문자열이면 다운로드."""
    if isinstance(source, Path):
        return source if source.exists() else None
    return _download_image(str(source), img_slug, source_label="source")


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
# 소스 이미지 공개 유틸
# ---------------------------------------------------------------------------

def fetch_og_image_url(page_url: str) -> "Optional[str]":
    """HTML 페이지에서 og:image / twitter:image URL을 추출한다 (공개 인터페이스)."""
    return _fetch_og_image_url(page_url)


def download_image(img_url: str, slug: str, source_label: str = "") -> "Optional[Path]":
    """이미지 URL을 다운로드해 assets/{slug}-thumb.{ext}에 저장한다 (공개 인터페이스).

    source_label에 'OG'가 포함되면 site-wide 기본값 감지를 수행한다:
    - 세션 내 URL 중복 체크
    - 기존 *-src*-thumb.* 파일과 MD5 해시 비교
    중복 감지 시 파일 삭제 후 None 반환 → 호출자가 Pexels/DDG로 폴백.
    """
    if "OG" in source_label:
        if img_url in _USED_OG_URLS:
            print(f"[WARN] OG URL 중복 감지 - site-wide 기본값으로 추정, Pexels/DDG 폴백")
            return None
        existing_hashes = _get_existing_src_hashes()
        result = _download_image(img_url, slug, source_label)
        if result and existing_hashes and _is_duplicate_src_image(result, existing_hashes):
            print(f"[WARN] OG 이미지 중복 감지 (기존 포스트와 동일) - Pexels/DDG 폴백")
            result.unlink(missing_ok=True)
            return None
        if result:
            _USED_OG_URLS.add(img_url)
        return result
    return _download_image(img_url, slug, source_label)


# ---------------------------------------------------------------------------
# 공개 진입점
# ---------------------------------------------------------------------------

def replace_image_markers(
    markdown_content: str,
    slug: str,
    source_images: "list[Path | str] | None" = None,
) -> "tuple[str, list[Path]]":
    """
    Gemini가 본문에 삽입한 [IMAGE: query] 마커를 실제 이미지로 교체한다.

    - 마커 형식: [IMAGE: english search query]
    - 각 마커를 <figure> 블록으로 교체
    - 첫 번째 이미지는 header.teaser에도 삽입
    - 이미지 파일명: {slug}-img1.jpg, {slug}-img2.jpg ...
    - 우선순위: source_images[i] → (i==0이고 source_images 없을 때) 출처 OG → Pexels → DDG
    """
    pattern = re.compile(r'\[IMAGE:\s*([^\]]+?)\s*\]')
    markers = pattern.findall(markdown_content)

    if not markers:
        print("[INFO] [IMAGE:] 마커 없음 - 이미지 삽입 건너뜀")
        return markdown_content, []

    print(f"[INFO] [IMAGE:] 마커 {len(markers)}개 발견 - 이미지 검색 시작")
    if source_images:
        print(f"[INFO] 소스 이미지 {len(source_images)}개 우선 사용")
    alt = _extract_title(markdown_content)
    downloaded_paths: list[Path] = []

    for i, query in enumerate(markers):
        img_num = i + 1
        img_slug = f"{slug}-img{img_num}"
        print(f"[INFO] 이미지 {img_num}/{len(markers)} 처리: {query!r}")

        img_path: Optional[Path] = None

        # 1순위: 소스 이미지 (사용자 제공 URL/PDF figure/YT 썸네일)
        if source_images and i < len(source_images):
            img_path = _use_source_image(source_images[i], img_slug)
            if img_path:
                print(f"[OK] 소스 이미지 사용: /assets/{img_path.name}")

        # 2순위: 출처 URL OG 이미지 (첫 마커, source_images 미제공 시에만)
        if img_path is None and i == 0 and not source_images:
            img_path = _try_og_image(markdown_content, img_slug)

        # 3순위: Pexels → DDG
        if img_path is None:
            img_path = _try_pexels_image(query, img_slug) or _try_ddg_image(query, img_slug)

        if img_path:
            rel_path = f"/assets/{img_path.name}"
            figure_html = f'\n<figure>\n<img src="{rel_path}" alt="{alt}">\n</figure>\n'
            markdown_content = pattern.sub(figure_html, markdown_content, count=1)
            downloaded_paths.append(img_path)
            if i == 0:
                markdown_content = _inject_teaser(markdown_content, rel_path)
            print(f"[OK] 이미지 {img_num} 삽입 완료: /assets/{img_path.name}")
        else:
            markdown_content = pattern.sub("", markdown_content, count=1)
            print(f"[WARN] 이미지 {img_num} 처리 실패 - 마커 제거")

    return markdown_content, downloaded_paths


def fetch_and_inject_image(
    markdown_content: str,
    slug: str,
    source_images: "list[Path | str] | None" = None,
    inject_body: bool = True,
) -> "tuple[str, Optional[Path]]":
    """
    이미지를 우선순위대로 검색해 assets/{slug}-thumb.{ext}에 저장하고
    front matter(header.teaser)와 본문(<figure>)에 삽입한다.

    우선순위:
      1. source_images[0] (사용자 제공 소스에서 추출한 이미지)
      2. ## 출처 URL에서 OG 이미지
      3. Pexels API (PEXELS_API_KEY 필요, 고품질 큐레이션 이미지)
      4. DuckDuckGo 이미지 웹서치 (API 키 불필요, 최후 폴백)

    inject_body=False이면 teaser만 삽입하고 본문 <figure>는 건너뜀.
    PDF figure처럼 Gemini가 이미 본문에 배치한 경우에 사용한다.
    """
    query = _extract_query(markdown_content)
    alt = _extract_title(markdown_content)

    # 1순위: 소스 이미지 (사용자 제공)
    if source_images:
        img_path = _use_source_image(source_images[0], slug)
        if img_path:
            rel_path = f"/assets/{img_path.name}"
            markdown_content = _inject_teaser(markdown_content, rel_path)
            if inject_body:
                markdown_content = _inject_figure(markdown_content, rel_path, alt=alt)
            return markdown_content, img_path

    # 2순위: 출처 URL OG 이미지
    img_path = _try_og_image(markdown_content, slug)

    # 3순위: Pexels (API 키 지정 고품질)
    if img_path is None:
        img_path = _try_pexels_image(query, slug)

    # 4순위: DuckDuckGo 폴백
    if img_path is None:
        img_path = _try_ddg_image(query, slug)

    if img_path is None:
        print("[INFO] 이미지 삽입 건너뜀 - 모든 소스 실패")
        return markdown_content, None

    rel_path = f"/assets/{img_path.name}"
    markdown_content = _inject_teaser(markdown_content, rel_path)
    markdown_content = _inject_figure(markdown_content, rel_path, alt=alt)

    return markdown_content, img_path


def replace_frame_markers(
    markdown_content: str,
    frame_paths: "list[Path]",
    slug: str,
) -> "tuple[str, list[Path]]":
    """
    [FRAME:N] 마커를 실제 영상 캡쳐 프레임 <figure> 블록으로 교체한다.

    - 마커 형식: [FRAME:N] (1-indexed)
    - 첫 번째 사용된 프레임을 header.teaser에도 삽입
    """
    pattern = re.compile(r'\[FRAME:(\d+)\]')
    markers = pattern.findall(markdown_content)

    if not markers:
        print("[INFO] [FRAME:] 마커 없음 - 프레임 삽입 건너뜀")
        return markdown_content, []

    print(f"[INFO] [FRAME:] 마커 {len(markers)}개 발견 - 프레임 교체 시작")
    alt = _extract_title(markdown_content)
    used_paths: list[Path] = []

    def replacer(m: "re.Match[str]") -> str:
        n = int(m.group(1)) - 1  # 0-indexed
        if 0 <= n < len(frame_paths):
            fp = frame_paths[n]
            if fp.exists():
                rel_path = f"/assets/{fp.name}"
                used_paths.append(fp)
                print(f"[OK] [FRAME:{n + 1}] 삽입: {rel_path}")
                return f'\n<figure>\n<img src="{rel_path}" alt="{alt}">\n</figure>\n'
        print(f"[WARN] [FRAME:{n + 1}] 프레임 파일 없음 - 마커 제거")
        return ""

    markdown_content = pattern.sub(replacer, markdown_content)

    if used_paths:
        markdown_content = _inject_teaser(markdown_content, f"/assets/{used_paths[0].name}")

    return markdown_content, used_paths


def inject_permalink(markdown_content: str, slug: str) -> str:
    """
    front matter에 permalink: /post/<slug>/ 자동 삽입.

    Jekyll 기본 slugify가 한글 카테고리(AI디지털기반교육혁신 등)를
    'aidigital기반교육혁신' 같은 한영 혼재 슬러그로 변환해 URL이 추하게 깨지는 문제를
    회피한다. 영문 slug 기반 permalink를 직접 지정해 깔끔한 URL을 보장한다.

    이미 permalink:가 있으면 변경하지 않는다.
    """
    if re.search(r"^permalink:", markdown_content, re.MULTILINE):
        return markdown_content

    parts = markdown_content.split("---", 2)
    if len(parts) < 3:
        return markdown_content

    fm_body = parts[1].rstrip()
    new_fm = f"{fm_body}\npermalink: /post/{slug}/\n"
    return f"---{new_fm}---{parts[2]}"


# ---------------------------------------------------------------------------
# 공유 상수·유틸 (4개 자동화 스크립트 공통)
# ---------------------------------------------------------------------------

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


def _parse_yaml_list(front_matter: str, key: str) -> list[str]:
    """YAML front matter에서 단일 라인 [a, b] 또는 멀티라인 - item 형식 파싱."""
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


def get_existing_taxonomy() -> tuple[list[str], list[str]]:
    """_posts/*.md 전체에서 기존 categories와 tags를 빈도순으로 반환."""
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
