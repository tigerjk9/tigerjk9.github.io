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
  --keep-pdf           처리 후 원본 PDF를 삭제하지 않음 (기본: 삭제)

환경변수:
  GEMINI_API_KEY       Google AI Studio API 키 (필수)
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import os
import random
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# Windows 터미널 한글 깨짐 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Python 3.9 호환: importlib.metadata.packages_distributions은 3.11에서 추가됨
try:
    import importlib.metadata as _im
    if not hasattr(_im, "packages_distributions"):
        _im.packages_distributions = lambda: {}
except Exception:
    pass

# ──────────────────────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent

import sys as _sys
_sys.path.insert(0, str(SCRIPT_DIR))
from image_fetcher import fetch_and_inject_image, inject_permalink, get_existing_taxonomy, replace_image_markers, CROSSOVER_DOMAINS  # noqa: E402


# ──────────────────────────────────────────────────────────────
# .env 자동 로드 (python-dotenv 없이 직접 파싱)
# ──────────────────────────────────────────────────────────────
def _load_dotenv() -> None:
    """REPO_ROOT/.env 파일을 읽어 환경변수로 설정 (이미 설정된 값은 덮어쓰지 않음)."""
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


_load_dotenv()


def _sanitize_content(content: str) -> str:
    content = re.sub(r"\n[-]{3,}\s*$", "", content.rstrip()) + "\n"
    lines = content.split("\n")
    in_source = False
    result = []
    for line in lines:
        if line.strip() == "## 출처":
            in_source = True
            result.append(line)
            continue
        if in_source and line.startswith("## "):
            in_source = False
        if in_source and re.match(r"^- https?://", line) and "<" not in line:
            line = re.sub(r"^(- )(https?://\S+)", r"\1<\2>", line)
        result.append(line)
    return "\n".join(result)


POSTS_DIR = REPO_ROOT / "_posts"
ASSETS_DIR = REPO_ROOT / "assets"
PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "prompt_template.txt"
EDIT_PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "edit_paper_prompt_template.txt"
MULTI_PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "paper_multi_prompt_template.txt"
EDIT_MULTI_PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "edit_paper_multi_prompt_template.txt"
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_CHARS = 100000  # Gemini 컨텍스트 한도 초과 방지

# Figure 추출 필터 기준
FIG_MIN_WIDTH = 300
FIG_MIN_HEIGHT = 200
FIG_MAX_COUNT = 6




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
    candidates: list[dict] = []

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


def build_figure_instructions(figures: list[dict]) -> str:
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
        "  삽입 형식 예 (반드시 아래 HTML 형식 사용, 마크다운 ![](url) 절대 금지):",
        "  <figure>",
        f"  <img src=\"{figures[0]['asset_url']}\" alt=\"한국어 그림 설명\">",
        "  <figcaption>그림에 대한 한국어 캡션</figcaption>",
        "  </figure>",
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


GITHUB_REPO_BASE = "https://github.com/tigerjk9/tigerjk9.github.io/blob/main"


def github_pdf_url(pdf_path: Path) -> str:
    """_papers/ 에 저장된 PDF의 GitHub blob URL을 반환.

    URL은 추측 없이 레포에 실제 존재하는 파일 경로에서 결정되므로 항상 정확하다.
    예: _papers/Some Paper.pdf
      → https://github.com/tigerjk9/tigerjk9.github.io/blob/main/_papers/Some%20Paper.pdf
    """
    # REPO_ROOT 기준 상대 경로로 변환
    try:
        rel = pdf_path.resolve().relative_to(REPO_ROOT.resolve())
    except ValueError:
        rel = pdf_path  # 절대 경로 변환 실패 시 원본 사용

    # URL 인코딩: 공백 → %20, 한글 등 non-ASCII → percent-encode
    from urllib.parse import quote
    encoded = quote(rel.as_posix(), safe="/")
    return f"{GITHUB_REPO_BASE}/{encoded}"


# ──────────────────────────────────────────────────────────────
# Gemini API
# ──────────────────────────────────────────────────────────────

def load_prompt_template(
    date_str: str,
    categories: list[str],
    tags: list[str],
    figures: list[dict],
    edit: bool = False,
) -> str:
    """prompt_template.txt 읽기 + 플레이스홀더 치환."""
    template_path = EDIT_PROMPT_TEMPLATE_PATH if edit else PROMPT_TEMPLATE_PATH
    if not template_path.exists():
        raise RuntimeError(f"프롬프트 템플릿을 찾을 수 없습니다: {template_path}")
    template = template_path.read_text(encoding="utf-8")

    cats_str = ", ".join(categories) if categories else "AI, 교육"
    tags_str = ", ".join(tags) if tags else "논문리뷰, AI, 교육"
    time_str = datetime.now().strftime("%H:%M:%S")

    template = template.replace("{DATE_PLACEHOLDER}", f"{date_str} {time_str}")
    template = template.replace("{EXISTING_CATEGORIES}", cats_str)
    template = template.replace("{EXISTING_TAGS}", tags_str)
    template = template.replace("{FIGURE_INSTRUCTIONS}", build_figure_instructions(figures))
    if edit:
        crossover_domain = random.choice(CROSSOVER_DOMAINS)
        template = template.replace("{CROSSOVER_DOMAIN}", crossover_domain)
    return template


def load_multi_prompt_template(
    date_str: str,
    categories: list[str],
    tags: list[str],
    edit: bool = False,
) -> "tuple[str, str]":
    """복수 PDF용 프롬프트 템플릿 읽기 + 플레이스홀더 치환."""
    template_path = EDIT_MULTI_PROMPT_TEMPLATE_PATH if edit else MULTI_PROMPT_TEMPLATE_PATH
    if not template_path.exists():
        raise RuntimeError(f"멀티 프롬프트 템플릿을 찾을 수 없습니다: {template_path}")
    template = template_path.read_text(encoding="utf-8")

    cats_str = ", ".join(categories) if categories else "AI, 교육"
    tags_str = ", ".join(tags) if tags else "논문리뷰, AI, 교육"
    time_str = datetime.now().strftime("%H:%M:%S")
    crossover_domain = random.choice(CROSSOVER_DOMAINS)

    template = template.replace("{DATE_PLACEHOLDER}", f"{date_str} {time_str}")
    template = template.replace("{EXISTING_CATEGORIES}", cats_str)
    template = template.replace("{EXISTING_TAGS}", tags_str)
    template = template.replace("{CROSSOVER_DOMAIN}", crossover_domain)
    return template, crossover_domain


def call_gemini_api(
    paper_text: str,
    system_prompt: str,
    model: str,
    figures: list[dict] | None = None,
    preamble: str = "다음은 분석할 연구 논문 전문입니다:\n\n",
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
    parts: list = [f"{preamble}{paper_text}"]

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
        print(f"[WARN] 파일명 충돌 - 타임스탬프 추가: {filename}")
    return filename


def save_post(content: str, output_path: Path) -> None:
    """_posts/ 에 파일 저장."""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] 포스트 저장 완료: {output_path}")


# ──────────────────────────────────────────────────────────────
# Git
# ──────────────────────────────────────────────────────────────

def _git(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """git 명령 실행. check=True이면 실패 시 RuntimeError."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, encoding="utf-8", cwd=str(REPO_ROOT),
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {args[0]} 실패:\n{result.stderr.strip()}")
    return result


def git_commit_and_push(file_paths: list[Path], commit_msg: str) -> None:
    """git add → commit → fetch → rebase(--autostash) → push origin main."""
    _git(["add", "--", *[str(fp) for fp in file_paths]])
    print(f"[OK] git add 완료 ({len(file_paths)}개 파일)")

    _git(["commit", "-m", commit_msg])
    print("[OK] git commit 완료")

    # 원격 최신 커밋 가져온 뒤 rebase. --autostash가 unstaged 변경사항을 자동 처리
    _git(["fetch", "origin"], check=False)
    rebase = _git(["rebase", "origin/main", "--autostash"], check=False)
    if rebase.returncode != 0:
        print(f"[WARN] rebase 실패 (계속 push 시도): {rebase.stderr.strip()}")

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
    parser.add_argument(
        "pdf_paths",
        nargs="+",
        help="변환할 PDF 파일 경로 (복수 가능: _papers/a.pdf _papers/b.pdf)",
    )
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
    parser.add_argument(
        "--keep-pdf",
        action="store_true",
        help="처리 후 원본 PDF를 삭제하지 않음 (기본: 삭제하여 로컬 용량 절약)",
    )
    parser.add_argument(
        "--edit",
        action="store_true",
        help="edit 모드: 블로그 주인장 목소리 강화 프롬프트 사용",
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
    pdf_path_list = [Path(p) for p in args.pdf_paths]
    for p in pdf_path_list:
        if not p.exists():
            print(f"[ERROR] 파일을 찾을 수 없습니다: {p}")
            sys.exit(1)

    is_multi = len(pdf_path_list) > 1

    # /paper (--edit 없음)는 단일 PDF만 허용. 복수 PDF는 /edit-paper를 사용.
    if is_multi and not args.edit:
        print("[ERROR] /paper 스킬은 PDF 한 개만 지원합니다.")
        print("        복수 PDF를 하나의 포스트로 통합하려면 /edit-paper 를 사용하세요.")
        sys.exit(1)

    # ── timezone 설정 확인 및 자동 수정 ──
    config_modified = ensure_timezone_config()

    # ── 슬러그 결정 ──
    if args.slug:
        slug = args.slug
    elif is_multi:
        slug = slugify("-".join(p.stem[:20] for p in pdf_path_list[:2]))
    else:
        slug = slugify(pdf_path_list[0].stem)

    # ── 기존 카테고리/태그 수집 ──
    print("[INFO] 기존 카테고리/태그 수집 중...")
    existing_cats, existing_tags = get_existing_taxonomy()
    print(f"[INFO] 기존 카테고리 {len(existing_cats)}개, 태그 {len(existing_tags)}개 확인")

    if is_multi:
        # ── 복수 PDF 모드 ──
        figures = []
        papers_texts = []
        for pdf_path in pdf_path_list:
            print(f"[INFO] PDF 텍스트 추출 중: {pdf_path}")
            try:
                raw = extract_text_from_pdf(str(pdf_path))
            except RuntimeError as e:
                print(f"[ERROR] {e}")
                sys.exit(1)
            truncated = truncate_text(raw, max_chars=MAX_CHARS // len(pdf_path_list))
            print(f"[INFO] 추출 완료 ({len(truncated):,}자): {pdf_path.name}")
            papers_texts.append((pdf_path.name, truncated))

        combined_papers = "\n\n---\n\n".join(
            f"### [논문 {i}] {name}\n\n{text}"
            for i, (name, text) in enumerate(papers_texts, 1)
        )

        try:
            system_prompt, crossover_domain = load_multi_prompt_template(
                args.date, existing_cats, existing_tags, edit=args.edit
            )
            print(f"[INFO] 크로스오버 분야: {crossover_domain}")
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

        try:
            markdown_content = call_gemini_api(
                combined_papers, system_prompt, args.model,
                preamble="다음은 분석할 복수의 연구 논문들입니다:\n\n",
            )
        except RuntimeError as e:
            print(f"[ERROR] Gemini API 호출 실패: {e}")
            sys.exit(1)

        source_label = ", ".join(p.name for p in pdf_path_list)

    else:
        # ── 단일 PDF 모드 ──
        pdf_path = pdf_path_list[0]

        # Figure 추출 (dry-run 시 건너뜀)
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

        print(f"[INFO] PDF 텍스트 추출 중: {pdf_path}")
        try:
            raw_text = extract_text_from_pdf(str(pdf_path))
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

        paper_text = truncate_text(raw_text)
        print(f"[INFO] 추출 완료 ({len(paper_text):,}자)")

        try:
            system_prompt = load_prompt_template(
                args.date, existing_cats, existing_tags, figures, edit=args.edit
            )
        except RuntimeError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

        try:
            markdown_content = call_gemini_api(
                paper_text, system_prompt, args.model,
                figures=figures or None,
            )
        except RuntimeError as e:
            print(f"[ERROR] Gemini API 호출 실패: {e}")
            sys.exit(1)

        source_label = pdf_path.name

    print("[INFO] 요약 생성 완료")

    # ── dry-run: 출력만 ──
    if args.dry_run:
        print("\n" + "=" * 60)
        print(markdown_content)
        print("=" * 60)
        print("\n[dry-run] 파일 저장 및 git push를 건너뜁니다.")
        return

    # PDF figure를 소스 이미지로 전달 (단일 PDF만; 복수 모드는 figure 미추출)
    _source_images = [fig["local_path"] for fig in figures] if not is_multi else []

    if args.edit:
        markdown_content, img_paths = replace_image_markers(markdown_content, slug, source_images=_source_images or None)
        thumb_path = img_paths[0] if img_paths else None
    else:
        markdown_content, thumb_path = fetch_and_inject_image(markdown_content, slug, source_images=_source_images or None)
        img_paths = [thumb_path] if thumb_path else []
    markdown_content = _sanitize_content(markdown_content)
    markdown_content = inject_permalink(markdown_content, slug)

    # ── 파일 저장 ──
    filename = build_filename(args.date, slug)
    output_path = POSTS_DIR / filename
    save_post(markdown_content, output_path)

    # ── git commit + push ──
    if not args.no_push:
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', markdown_content, re.MULTILINE)
        short_title = title_match.group(1)[:50] if title_match else slug
        commit_msg = (
            f"Add: {short_title}\n\n"
            f"Auto-generated by pdf_to_post.py\n"
            f"Source: {source_label}"
        )
        all_files = [output_path] + [fig["local_path"] for fig in figures]
        all_files.extend(img_paths)
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

    # ── 원본 PDF 자동 삭제 (기본 동작; --keep-pdf 로 보존) ──
    if args.keep_pdf:
        for pdf_path in pdf_path_list:
            print(f"[INFO] --keep-pdf 옵션으로 원본 PDF를 보존합니다: {pdf_path}")
    else:
        for pdf_path in pdf_path_list:
            try:
                pdf_path.unlink()
                print(f"[OK] 원본 PDF 삭제 완료: {pdf_path}")
            except Exception as e:
                print(f"[WARN] 원본 PDF 삭제 실패: {e}")

    print(f"\n완료! 생성된 포스트: {output_path}")


if __name__ == "__main__":
    main()
