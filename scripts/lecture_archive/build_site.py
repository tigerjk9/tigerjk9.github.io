"""Jekyll collection·_data·_includes·assets 산출물 빌드."""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import yaml


def write_feature_page(lecture_dir: Path, lecture_slug: str, feature: Dict[str, Any],
                       prev_slug: Optional[str] = None, next_slug: Optional[str] = None) -> Path:
    """기능 페이지 마크다운 작성."""
    fm = {
        "title": f"{feature['name']} — {feature['id']}",
        "permalink": f"/lectures/{lecture_slug}/{feature['slug']}/",
        "layout": "lecture",
        "lecture_slug": lecture_slug,
        "feature_id": feature["id"],
        "feature_name": feature["name"],
        "feature_slug": feature["slug"],
        "track": feature["track"],
        "order": feature.get("order", 0),
    }
    body_parts = [
        '<div class="feature-header">',
        f'  <span class="feature-badge">{feature["id"]}</span>',
        f'  <span class="feature-badge track-{feature["track"]}">{feature["track"]}</span>',
        f'  <h1>{feature["name"]}</h1>',
        '</div>',
        "",
        f"{feature['def']}",
        "",
        "## 핵심 동작",
        "",
    ]
    for action in feature.get("actions", []):
        body_parts.append(f"- {action}")
    body_parts.extend([
        "",
        "## 사용법",
        "",
        f"```{feature.get('usage_lang', 'powershell')}",
        feature.get("usage_code", "").strip(),
        "```",
        "",
        "## 관련 슬라이드",
        "",
    ])
    for s in feature.get("related_slides", []):
        body_parts.extend([
            '<figure class="slide-excerpt">',
            f'  <img src="{s["png"]}" alt="S{s["n"]} — {s["title"]}" loading="lazy">',
            f'  <figcaption>S{s["n"]} · {s["title"]}</figcaption>',
            f'  <div class="slide-text">{s.get("text", "")[:300]}</div>',
            '</figure>',
            "",
        ])
    if feature.get("ment_excerpt"):
        body_parts.extend(["## 강사 멘트", "", f"> {feature['ment_excerpt']}", ""])
    if feature.get("lab_excerpt"):
        body_parts.extend(["## 실습", "", feature["lab_excerpt"], ""])
    if feature.get("rationale"):
        body_parts.extend(["## 활용 시사점", "", feature["rationale"], ""])
    if feature.get("source_urls"):
        body_parts.extend(["## 출처", ""])
        for url in feature["source_urls"]:
            body_parts.append(f"- <{url}>")
    out_path = lecture_dir / f"{feature['slug']}.md"
    fm_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False)
    content = f"---\n{fm_yaml}---\n\n" + "\n".join(body_parts) + "\n"
    out_path.write_text(content, encoding="utf-8")
    return out_path


def write_hub_page(lecture_dir: Path, lecture_slug: str, lecture_meta: Dict[str, Any],
                   features: List[Dict[str, Any]]) -> Path:
    """강의 허브 페이지 (index.md) 작성."""
    fm = {
        "title": lecture_meta["title"],
        "permalink": f"/lectures/{lecture_slug}/",
        "layout": "lecture",
        "lecture_slug": lecture_slug,
    }
    body = [
        f"## {lecture_meta.get('subtitle', '')}",
        "",
        f"- 청중. {lecture_meta.get('audience', '')}",
        f"- 시간. {lecture_meta.get('duration_min', 0)}분",
        f"- 환경. {lecture_meta.get('environment', '')}",
        "",
        "## 기능 카탈로그",
        "",
        '<div class="lecture-card-grid">',
    ]
    for f in features:
        body.append(
            f'  <a href="/lectures/{lecture_slug}/{f["slug"]}/" class="lecture-card">'
            f'<div class="card-id">{f["id"]}</div>'
            f'<div class="card-title">{f["name"]}</div>'
            f'<span class="card-track">{f["track"]}</span></a>'
        )
    body.extend(['</div>', "", "## 다운로드", "",
                 f"- [원본 슬라이드 풀스크린]({lecture_meta['assets']['slides']})",
                 f"- [핸드아웃 PDF]({lecture_meta['assets']['handout']})"])
    out_path = lecture_dir / "index.md"
    fm_yaml = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False)
    out_path.write_text(f"---\n{fm_yaml}---\n\n" + "\n".join(body) + "\n", encoding="utf-8")
    return out_path


def append_lecture_index(data_file: Path, block: Dict[str, Any]) -> None:
    """`_data/lectures.yml`에 강의 블록 추가/교체."""
    if data_file.exists():
        existing = yaml.safe_load(data_file.read_text(encoding="utf-8")) or []
    else:
        existing = []
    out = [b for b in existing if b.get("slug") != block.get("slug")]
    out.append(block)
    data_file.write_text(yaml.safe_dump(out, allow_unicode=True, sort_keys=False), encoding="utf-8")


def write_slides_index_json(slides_dir: Path, slides: List[Dict[str, Any]]) -> Path:
    """슬라이드별 텍스트·메타 JSON 인덱스 (검색용)."""
    slides_dir.mkdir(parents=True, exist_ok=True)
    out = slides_dir / "index.json"
    out.write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding="utf-8")
    return out
