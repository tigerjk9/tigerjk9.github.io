"""Reveal.js 슬라이드 추출 — BeautifulSoup 정적 파싱 + Playwright 동적 캡처."""
from __future__ import annotations
from typing import Any, List, Dict
from bs4 import BeautifulSoup


def parse_html(html: str) -> List[Dict[str, Any]]:
    """slides.html → 슬라이드별 dict 리스트 (1-based n, 메타·텍스트·코드)."""
    soup = BeautifulSoup(html, "html.parser")
    sections = soup.select(".reveal .slides > section")
    slides: List[Dict[str, Any]] = []
    for i, sec in enumerate(sections, start=1):
        sec_classes = sec.get("class", [])
        layouts = [c for c in sec_classes if c.startswith("layout-")]
        if layouts:
            layout = layouts[0]
        elif "title-slide" in sec_classes:
            layout = "title-slide"
        else:
            layout = ""
        h = sec.find(["h1", "h2"])
        title = h.get_text(strip=True) if h else ""
        code_blocks = []
        for pre in sec.find_all("pre"):
            code_el = pre.find("code")
            if not code_el:
                continue
            code_classes = code_el.get("class", []) or []
            lang_classes = [c for c in code_classes if c.startswith("language-")]
            lang = lang_classes[0].replace("language-", "") if lang_classes else ""
            code_blocks.append({"lang": lang, "code": code_el.get_text()})
        # 텍스트 추출: 헤딩·코드 제외하고
        for tag in sec.find_all(["pre", "h1", "h2"]):
            tag.decompose()
        text = " ".join(sec.get_text(separator=" ").split())
        slides.append({
            "n": i,
            "block": sec.get("data-block", ""),
            "data_time": sec.get("data-time", ""),
            "layout": layout,
            "title": title,
            "text": text,
            "code_blocks": code_blocks,
            "images": [img.get("src", "") for img in sec.find_all("img")],
        })
    return slides


def capture_pngs(slides_html, output_dir, viewport=(1920, 1080)):
    """Playwright headless로 슬라이드별 PNG 캡처.

    Reveal.js의 fragment를 비활성화하고 각 슬라이드 첫 상태만 캡처.
    """
    from pathlib import Path
    from playwright.sync_api import sync_playwright
    slides_html = Path(slides_html)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    pngs = []
    url = f"file:///{slides_html.resolve().as_posix()}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
        page.goto(url, wait_until="networkidle")
        total = page.evaluate("Reveal.getTotalSlides()")
        for i in range(total):
            page.evaluate(f"Reveal.slide({i})")
            page.wait_for_timeout(300)
            png_path = output_dir / f"slide-{i+1:02d}.png"
            page.screenshot(path=str(png_path), full_page=False, clip={
                "x": 0, "y": 0, "width": viewport[0], "height": viewport[1]
            })
            pngs.append(png_path)
        browser.close()
    return pngs


def convert_to_webp(pngs, max_width=1280, quality=80):
    """PNG -> WebP 변환 + 리사이즈."""
    from PIL import Image
    webps = []
    for png in pngs:
        with Image.open(png) as img:
            if img.width > max_width:
                ratio = max_width / img.width
                img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)
            webp_path = png.with_suffix(".webp")
            img.save(webp_path, "WebP", quality=quality)
            webps.append(webp_path)
    return webps
