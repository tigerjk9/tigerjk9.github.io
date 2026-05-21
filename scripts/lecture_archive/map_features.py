"""슬라이드 ↔ 기능 매핑 — strict (notes) → heading (fuzzy) → llm (Gemini)."""
from __future__ import annotations
from difflib import SequenceMatcher
from typing import Any, Dict, List, Tuple, Optional, Callable

Mapping = Dict[int, Tuple[str, str]]  # n → (feature_name, method)
HEADING_THRESHOLD = 0.55


def map_strict(slides: List[Dict[str, Any]], slide_to_feature: Dict[int, str]) -> Mapping:
    """instructor-notes 헤딩의 (Sn~Sm) 범위로 직접 매핑."""
    out: Mapping = {}
    for slide in slides:
        n = slide["n"]
        if n in slide_to_feature:
            out[n] = (slide_to_feature[n], "strict")
    return out


def map_heading(unmapped_slides: List[Dict[str, Any]], catalog: List[Dict[str, Any]]) -> Mapping:
    """슬라이드 h2 ↔ 카탈로그 기능명 fuzzy matching."""
    out: Mapping = {}
    for slide in unmapped_slides:
        title = slide.get("title", "")
        if not title:
            continue
        best_score = 0.0
        best_name: Optional[str] = None
        for f in catalog:
            for candidate in (f.get("name", ""), f.get("name_ko", "")):
                if not candidate:
                    continue
                score = SequenceMatcher(None, title.lower(), candidate.lower()).ratio()
                # Boost when title's first token appears in the candidate
                first_token = title.split()[0].lower() if title.split() else ""
                if first_token and first_token in candidate.lower():
                    score = max(score, 0.7)
                if score > best_score:
                    best_score = score
                    best_name = f.get("name")
        if best_score >= HEADING_THRESHOLD and best_name:
            out[slide["n"]] = (best_name, "heading")
    return out


def map_llm(unmapped_slides: List[Dict[str, Any]], catalog: List[Dict[str, Any]],
            gemini_call: Callable) -> Mapping:
    """Gemini 분류 폴백. gemini_call(slide, catalog) → feature_name | None."""
    out: Mapping = {}
    for slide in unmapped_slides:
        name = gemini_call(slide, catalog)
        if name:
            out[slide["n"]] = (name, "llm")
    return out


def decide_mapping(*layers: Mapping) -> Mapping:
    """우선순위. 첫 번째 layer의 값이 우선."""
    final: Mapping = {}
    for layer in layers:
        for n, (name, method) in layer.items():
            if n not in final:
                final[n] = (name, method)
    return final


def call_gemini(slide: Dict[str, Any], catalog: List[Dict[str, Any]]) -> Optional[str]:
    """실제 Gemini 호출. .env GEMINI_API_KEY 사용."""
    import os
    try:
        import google.generativeai as genai
    except ImportError:
        return None
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    genai.configure(api_key=api_key)
    catalog_text = "\n".join(f"- {f['id']} {f['name']} — {f.get('def', '')}" for f in catalog)
    prompt = f"""다음 슬라이드를 카탈로그에서 하나의 기능에 분류하라.

[슬라이드]
제목. {slide.get('title', '')}
본문. {slide.get('text', '')[:500]}

[카탈로그]
{catalog_text}

분류 결과를 기능명만 한 줄로 답하라. 매칭되는 것이 없으면 'NONE'."""
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    resp = model.generate_content(prompt)
    name = resp.text.strip()
    if name == "NONE":
        return None
    # 카탈로그에 실제 존재하는 기능명인지 검증
    valid = {f["name"] for f in catalog}
    return name if name in valid else None
