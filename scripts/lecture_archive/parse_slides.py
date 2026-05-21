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
