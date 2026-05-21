"""instructor-notes.md 발췌 — 섹션 헤딩·슬라이드 범위·슬라이드별 멘트."""
from __future__ import annotations
import re
from typing import Any, Dict, List

SECTION_RE = re.compile(r"^##\s+(.+?)\s*\(S(\d+)~S(\d+),\s*(\d+)분\)", re.M)
SLIDE_RE = re.compile(r"^###\s+S(\d+)\.\s*(.+)$", re.M)
BULLET_RE = re.compile(r"^-\s+\*\*(멘트|시간|강조|예상\s*Q|운영)\.\*\*\s*(.+)$", re.M)


def parse_notes(md: str) -> List[Dict[str, Any]]:
    """instructor-notes.md → 섹션·슬라이드별 dict 리스트."""
    sections: List[Dict[str, Any]] = []
    matches = list(SECTION_RE.finditer(md))
    for i, m in enumerate(matches):
        start_pos = m.end()
        end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        chunk = md[start_pos:end_pos]
        slides = _parse_slides_in_chunk(chunk)
        sections.append({
            "feature_name": m.group(1).strip(),
            "slide_start": int(m.group(2)),
            "slide_end": int(m.group(3)),
            "duration_min": int(m.group(4)),
            "slides": slides,
        })
    return sections


def _parse_slides_in_chunk(chunk: str) -> List[Dict[str, Any]]:
    slides: List[Dict[str, Any]] = []
    slide_matches = list(SLIDE_RE.finditer(chunk))
    for i, m in enumerate(slide_matches):
        start = m.end()
        end = slide_matches[i + 1].start() if i + 1 < len(slide_matches) else len(chunk)
        body = chunk[start:end]
        slide = {"n": int(m.group(1)), "title": m.group(2).strip(),
                 "ment": "", "time": "", "emphasis": "", "qa": "", "ops": ""}
        for b in BULLET_RE.finditer(body):
            label = b.group(1)
            label_norm = re.sub(r"\s+", "", label)
            mapping = {"멘트": "ment", "시간": "time", "강조": "emphasis", "예상Q": "qa", "운영": "ops"}
            field = mapping.get(label_norm, None)
            if field:
                slide[field] = b.group(2).strip()
        slides.append(slide)
    return slides


def slide_to_feature_map(sections: List[Dict[str, Any]]) -> Dict[int, str]:
    """슬라이드 번호 → 기능명 매핑 (strict 매핑용)."""
    m: Dict[int, str] = {}
    for sec in sections:
        for n in range(sec["slide_start"], sec["slide_end"] + 1):
            m[n] = sec["feature_name"]
    return m
