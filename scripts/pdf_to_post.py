#!/usr/bin/env python3
"""
pdf_to_post.py — PDF 논문을 Jekyll 블로그 포스트로 자동 변환

사용법:
  python scripts/pdf_to_post.py <PDF_경로> [옵션]

옵션:
  --date  YYYY-MM-DD   포스트 날짜 (기본값: 오늘)
  --slug  SLUG         파일명 슬러그 (기본값: PDF 파일명에서 자동 생성)
  --no-push            로컬 저장만 하고 git push 하지 않음
  --dry-run            _posts/ 에 저장하지 않고 터미널에 출력만
  --model  MODEL       Gemini 모델 ID (기본값: gemini-2.0-flash)

환경변수:
  GEMINI_API_KEY       Google AI Studio API 키 (필수)
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
POSTS_DIR = REPO_ROOT / "_posts"
ASSETS_DIR = REPO_ROOT / "assets"
PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "prompt_template.txt"
DEFAULT_MODEL = "gemini-2.0-flash"
MAX_CHARS = 100000  # Gemini 컨텍스트 한도 초과 방지

# Figure 추출 필터 기준
FIG_MIN_WIDTH = 300
FIG_MIN_HEIGHT = 200
FIG_MAX_COUNT = 6


# ──────────────────────────────────────────────────────────────
# 기존 카테고리/태그 수집
# ──────────────────────────────────────────────────────────────

def get_existing_taxonomy() -> tuple[list[str], list[str]]:
    """_posts/*.md 전체에서 기존 categories와 tags를 빈도순으로 반환."""
    cat_counter: Counter = Counter()
    tag_counter: Counter = Counter()

    for md_file in POSTS_DIR.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        # YAML front matter 추출 (--- ... --- 사이)
        fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            continue
        fm = fm_match.group(1)

        # categories 파싱: [A, B] 또는 멀티라인
        cats = _parse_yaml_list(fm, "categories")
        tags = _parse_yaml_list(fm, "tags")
        cat_counter.update(cats)
        tag_counter.update(tags)

    sorted_cats = [c for c, _ in cat_counter.most_common()]
    sorted_tags = [t for t, _ in tag_counter.most_common(40)]
    return sorted_cats, sorted_tags


def _parse_yaml_list(front_matter: str, key: str) -> list[str]:
    """YAML front matter에서 단일 라인 [a, b] 또는 멀티라인 - item 형식 파싱."""
    items: list[str] = []

    # 단일 라인: key: [a, b, c]
    inline = re.search(rf"^{key}:\s*\[(.+?)\]", front_matter, re.MULTILINE)
    if inline:
        for item in inline.group(1).split(","):
            val = item.strip().strip("'\"")
            if val:
                items.append(val)
        return items

    # 멀티라인: key:\n  - a\n  - b
    block = re.search(rf"^{key}:\s*\n((?:\s*-\s*.+\n?)+)", front_matter, re.MULTILINE)
    if block:
        for line in block.group(1).splitlines():
            m = re.match(r"\s*-\s*(.+)", line)
            if m:
                items.append(m.group(1).strip().strip("'\""))
    return items


# ──────────────────────────────────────────────────────────────
# PDF Figure 추출 (PyMuPDF)
# ──────────────────────────────────────────────────────────────

def extract_figures_from_pdf(pdf_path: str, slug: str) -> list[dict]:
    """PyMuPDF로 PDF에서 주요 Figure 이미지를 추출해 assets/ 에 저장.

    Returns:
        list of {"local_path": Path, "asset_url": str, "page": int, "w": int, "h": int}
        fitz 미설치 또는 추출 실패 시 빈 리스트 반환.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("[WARN] PyMuPDF(fitz)가 설치되어 있지 않습니다. Figure 추출을 건너뜁니다.")
        print("       pip install PyMuPDF")
        return []

    ASSETS_DIR.mkdir(exist_ok=True)

    seen_hashes: set[str] = set()
    candidates: list[dict] = []  # (area, page, xref, ext, bytes, w, h)

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"[WARN] Figure 추출 중 PDF 열기 실패: {e}")
        return []

    for page_num, page in enumerate(doc, start=1):
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                base_img = doc.extract_image(xref)
            except Exception:
                continue

            w = base_img.get("width", 0)
            h = base_img.get("height", 0)
            img_bytes = base_img.get("image", b"")
            ext = base_img.get("ext", "png")

            # 크기 필터
            if w < FIG_MIN_WIDTH or h < FIG_MIN_HEIGHT:
                continue

            # 중복 제거
            img_hash = hashlib.md5(img_bytes).hexdigest()
            if img_hash in seen_hashes:
                continue
            seen_hashes.add(img_hash)

            candidates.append({
                "page": page_num,
                "w": w,
                "h": h,
                "ext": ext,
                "bytes": img_bytes,
                "area": w * h,
            })

    doc.close()

    # 크기 내림차순 정렬 후 상위 N개
    candidates.sort(key=lambda x: x["area"], reverse=True)
    candidates = candidates[:FIG_MAX_COUNT]

    # 저장
    results: list[dict] = []
    for idx, fig in enumerate(candidates, start=1):
        ext = fig["ext"]
        # jpeg → jpg 정규화
        if ext in ("jpeg", "jpg"):
            ext = "jpg"
        filename = f"{slug}-fig-{idx}.{ext}"
        local_path = ASSETS_DIR / filename
        try:
            local_path.write_bytes(fig["bytes"])
        except Exception as e:
            print(f"[WARN] Figure 저장 실패 ({filename}): {e}")
            continue

        results.append({
            "local_path": local_path,
            "asset_url": f"/assets/{filename}",
            "page": fig["page"],
            "w": fig["w"],
            "h": fig["h"],
        })

    return results


def build_figure_instructions(figures: list[dict], slug: str) -> str:
    """추출된 Figure 목록을 Gemini 지시문 형태로 반환."""
    if not figures:
        return "- 이미지 태그 삽입 금지: 이 논문에서 추출된 Figure가 없으므로 이미지 삽입 코드를 작성하지 마세요."

    lines = [
        "- 아래 Figure 이미지들이 논문에서 추출되어 /assets/ 에 저장되어 있습니다.",
        "  포스트의 적절한 위치(주요 발견 섹션 내부 등)에 마크다운으로 삽입하세요.",
        "  alt 텍스트는 한국어로 그림 내용을 설명하세요.",
        "  모든 figure를 반드시 사용할 필요는 없으며, 가장 핵심적인 것 위주로 선택하세요.",
        "",
        "  사용 가능한 Figure:",
    ]
    for fig in figures:
        lines.append(
            f"  - {fig['asset_url']}  (p.{fig['page']}, {fig['w']}×{fig['h']}px)"
        )
    lines += [
        "",
        "  삽입 형식 예:",
        f"  ![그림 설명]({figures[0]['asset_url']})",
    ]
    return "\n".join(lines)


# ──────────────────────────────────────────────────────────────
# PDF 텍스트 추출
# ──────────────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """pdfplumber로 PDF 전체 텍스트 추출. 실패 시 RuntimeError."""
    try:
        import pdfplumber
    except ImportError:
        raise RuntimeError(
            "pdfplumber가 설치되어 있지 않습니다.\n"
            "pip install -r scripts/requirements.txt"
        )

    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        text = "\n\n".join(pages).strip()
    except Exception as e:
        raise RuntimeError(f"PDF 텍스트 추출 실패 (스캔 PDF는 지원하지 않습니다): {e}")

    if not text:
        raise RuntimeError("PDF에서 텍스트를 추출할 수 없습니다 (스캔 PDF는 지원하지 않습니다).")

    return text


def truncate_text(text: str, max_chars: int = MAX_CHARS) -> str:
    """Gemini 컨텍스트 한도 초과 방지용 앞부분 잘라내기."""
    if len(text) <= max_chars:
        return text
    print(f"[INFO] 텍스트가 {len(text):,}자로 길어 앞 {max_chars:,}자만 사용합니다.")
    return text[:max_chars]


# ──────────────────────────────────────────────────────────────
# Gemini API
# ──────────────────────────────────────────────────────────────

def load_prompt_template(
    date_str: str,
    categories: list[str],
    tags: list[str],
    figures: list[dict],
    slug: str,
) -> str:
    """prompt_template.txt 읽기 + 플레이스홀더 치환."""
    if not PROMPT_TEMPLATE_PATH.exists():
        raise RuntimeError(f"프롬프트 템플릿을 찾을 수 없습니다: {PROMPT_TEMPLATE_PATH}")
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")

    cats_str = ", ".join(categories) if categories else "AI, 교육"
    tags_str = ", ".join(tags) if tags else "논문리뷰, AI, 교육"
    fig_instructions = build_figure_instructions(figures, slug)

    time_str = datetime.now().strftime("%H:%M:%S")
    template = template.replace("{DATE_PLACEHOLDER}", f"{date_str} {time_str}")
    template = template.replace("{EXISTING_CATEGORIES}", cats_str)
    template = template.replace("{EXISTING_TAGS}", tags_str)
    template = template.replace("{FIGURE_INSTRUCTIONS}", fig_instructions)
    return template


def call_gemini_api(
    paper_text: str,
    system_prompt: str,
    model: str,
    figures: list[dict] | None = None,
) -> str:
    """Google Gemini SDK 호출 → 마크다운 문자열 반환. figures가 있으면 멀티모달."""
    try:
        import google.generativeai as genai
    except ImportError:
        raise RuntimeError(
            "google-generativeai 패키지가 설치되어 있지 않습니다.\n"
            "pip install -r scripts/requirements.txt"
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY 환경변수가 설정되지 않았습니다.\n"
            "export GEMINI_API_KEY=AIza..."
        )

    genai.configure(api_key=api_key)

    print(f"[INFO] Gemini API 호출 중 (모델: {model}) ...")
    gemini_model = genai.GenerativeModel(
        model_name=model,
        system_instruction=system_prompt,
    )

    # 멀티모달 파트 구성
    parts: list = [f"다음은 분석할 연구 논문 전문입니다:\n\n{paper_text}"]

    if figures:
        parts.append(
            "\n\n아래는 논문에서 추출한 Figure 이미지들입니다. "
            "포스트 적절한 위치에 삽입하세요."
        )
        for fig in figures:
            local_path: Path = fig["local_path"]
            asset_url: str = fig["asset_url"]
            ext = local_path.suffix.lstrip(".")
            mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
            try:
                img_bytes = local_path.read_bytes()
                parts.append(f"\n[Figure: {asset_url}]")
                parts.append(
                    {
                        "inline_data": {
                            "mime_type": mime,
                            "data": base64.b64encode(img_bytes).decode(),
                        }
                    }
                )
            except Exception as e:
                print(f"[WARN] Figure 이미지 읽기 실패 ({asset_url}): {e}")

    response = gemini_model.generate_content(parts)
    return response.text


# ──────────────────────────────────────────────────────────────
# 포스트 생성
# ──────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """문자열 → URL-safe 슬러그 (소문자, 하이픈)."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9가-힣\-]", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


def build_filename(date_str: str, slug: str) -> str:
    """'YYYY-MM-DD-{slug}.md' 형식 반환. 슬러그 충돌 시 타임스탬프 추가."""
    filename = f"{date_str}-{slug}.md"
    output_path = POSTS_DIR / filename
    if output_path.exists():
        ts = datetime.now().strftime("%H%M%S")
        filename = f"{date_str}-{slug}-{ts}.md"
        print(f"[WARN] 파일명 충돌 — 타임스탬프 추가: {filename}")
    return filename


def save_post(content: str, output_path: Path) -> None:
    """_posts/ 에 파일 저장."""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] 포스트 저장 완료: {output_path}")


# ──────────────────────────────────────────────────────────────
# Git
# ──────────────────────────────────────────────────────────────

def git_commit_and_push(file_paths: list[Path], commit_msg: str) -> None:
    """git add (복수 파일) → commit → push origin main."""
    # git add 각 파일
    for fp in file_paths:
        result = subprocess.run(
            ["git", "add", str(fp)],
            capture_output=True, text=True, cwd=str(REPO_ROOT),
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"git add 실패: {fp}\n{result.stderr.strip()}"
            )
    print(f"[OK] git add 완료 ({len(file_paths)}개 파일)")

    # git commit
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if result.returncode != 0:
        raise RuntimeError(f"git commit 실패:\n{result.stderr.strip()}")
    print("[OK] git commit 완료")

    # git push
    result = subprocess.run(
        ["git", "push", "origin", "main"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if result.returncode != 0:
        print(f"[WARN] git push 실패. 수동으로 push 하세요.")
        print(f"  → git push origin main")
        print(f"  상세: {result.stderr.strip()}")
    else:
        print("[OK] git push 완료")


# ──────────────────────────────────────────────────────────────
# Jekyll 설정 확인
# ──────────────────────────────────────────────────────────────

def ensure_timezone_config() -> bool:
    """_config.yml의 timezone이 Asia/Seoul인지 확인하고 필요하면 자동 수정.

    Returns:
        True  — 파일을 수정했음 (git commit 대상에 포함 필요)
        False — 이미 올바르게 설정되어 있음
    """
    config_path = REPO_ROOT / "_config.yml"
    if not config_path.exists():
        return False

    content = config_path.read_text(encoding="utf-8")

    # 이미 Asia/Seoul로 설정되어 있으면 스킵
    if re.search(r"^timezone:\s*Asia/Seoul\s*$", content, re.MULTILINE):
        return False

    # timezone 라인을 Asia/Seoul로 교체 (주석 처리 · 빈값 모두 포함)
    new_content = re.sub(
        r"^timezone:.*$",
        "timezone: Asia/Seoul",
        content,
        flags=re.MULTILINE,
    )

    if new_content == content:
        return False

    config_path.write_text(new_content, encoding="utf-8")
    print("[INFO] _config.yml timezone → Asia/Seoul 자동 수정 (KST 기준 포스트 노출)")
    return True


# ──────────────────────────────────────────────────────────────
# 진입점
# ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PDF 논문을 Jekyll 블로그 포스트로 자동 변환합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "예시:\n"
            "  python scripts/pdf_to_post.py _papers/selwyn-2025.pdf\n"
            "  python scripts/pdf_to_post.py _papers/selwyn-2025.pdf "
            "--date 2025-11-26 --slug When-the-prompting-stops\n"
            "  python scripts/pdf_to_post.py _papers/selwyn-2025.pdf --dry-run"
        ),
    )
    parser.add_argument("pdf_path", help="변환할 PDF 파일 경로 (예: _papers/paper.pdf)")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="포스트 날짜 YYYY-MM-DD (기본값: 오늘)",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="파일명 슬러그 (기본값: PDF 파일명에서 자동 생성)",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="로컬 저장만 하고 git push 하지 않음",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="_posts/ 에 저장하지 않고 터미널에 출력만",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini 모델 ID (기본값: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    # ── 환경변수 확인 ──
    if not os.environ.get("GEMINI_API_KEY"):
        print(
            "[ERROR] GEMINI_API_KEY 환경변수가 설정되지 않았습니다.\n"
            "  export GEMINI_API_KEY=AIza..."
        )
        sys.exit(1)

    # ── PDF 경로 확인 ──
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"[ERROR] 파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)

    # ── timezone 설정 확인 및 자동 수정 ──
    config_modified = ensure_timezone_config()

    # ── 슬러그 결정 ──
    slug = args.slug if args.slug else slugify(pdf_path.stem)

    # ── 기존 카테고리/태그 수집 ──
    print("[INFO] 기존 카테고리/태그 수집 중...")
    existing_cats, existing_tags = get_existing_taxonomy()
    print(f"[INFO] 기존 카테고리 {len(existing_cats)}개, 태그 {len(existing_tags)}개 확인")

    # ── Figure 추출 (dry-run 시 건너뜀) ──
    if args.dry_run:
        figures = []
        print("[INFO] dry-run 모드: Figure 추출을 건너뜁니다.")
    else:
        print(f"[INFO] PDF Figure 추출 중: {pdf_path}")
        figures = extract_figures_from_pdf(str(pdf_path), slug)
        if figures:
            print(f"[INFO] {len(figures)}개 Figure 추출 완료:")
            for fig in figures:
                print(f"       {fig['asset_url']} (p.{fig['page']}, {fig['w']}×{fig['h']}px)")
        else:
            print("[INFO] 추출된 Figure 없음 (텍스트 전용 모드)")

    # ── PDF 텍스트 추출 ──
    print(f"[INFO] PDF 텍스트 추출 중: {pdf_path}")
    try:
        raw_text = extract_text_from_pdf(str(pdf_path))
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    paper_text = truncate_text(raw_text)
    print(f"[INFO] 추출 완료 ({len(paper_text):,}자)")

    # ── 프롬프트 로드 ──
    try:
        system_prompt = load_prompt_template(
            args.date, existing_cats, existing_tags, figures, slug
        )
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # ── Gemini API 호출 ──
    try:
        markdown_content = call_gemini_api(
            paper_text, system_prompt, args.model,
            figures=figures or None,
        )
    except RuntimeError as e:
        print(f"[ERROR] Gemini API 호출 실패: {e}")
        sys.exit(1)

    print("[INFO] 요약 생성 완료")

    # ── dry-run: 출력만 ──
    if args.dry_run:
        print("\n" + "=" * 60)
        print(markdown_content)
        print("=" * 60)
        print("\n[dry-run] 파일 저장 및 git push를 건너뜁니다.")
        return

    # ── 파일 저장 ──
    filename = build_filename(args.date, slug)
    output_path = POSTS_DIR / filename
    save_post(markdown_content, output_path)

    # ── git commit + push ──
    if not args.no_push:
        # YAML front matter에서 title 추출
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', markdown_content, re.MULTILINE)
        short_title = title_match.group(1)[:50] if title_match else slug
        commit_msg = (
            f"Add: {short_title}\n\n"
            f"Auto-generated by pdf_to_post.py\n"
            f"Source: {pdf_path.name}"
        )
        all_files = [output_path] + [fig["local_path"] for fig in figures]
        if config_modified:
            all_files.append(REPO_ROOT / "_config.yml")
        try:
            git_commit_and_push(all_files, commit_msg)
        except RuntimeError as e:
            print(f"[ERROR] git 오류: {e}")
    else:
        print("[INFO] --no-push 옵션으로 git push를 건너뜁니다.")
        print(
            f"  수동 push: git add {output_path} && "
            f"git commit -m 'Add: {slug}' && git push origin main"
        )

    print(f"\n완료! 생성된 포스트: {output_path}")


if __name__ == "__main__":
    main()
