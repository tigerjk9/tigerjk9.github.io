"""강의자료 큐레이션 진입점.

지원 입력 형식:
  zip  — 강의 묶음 (slides·notes·handout·labs·카탈로그)
  pdf  — 단일 PDF (텍스트 추출 → instructor-notes.md 변환)
  html — 단일 HTML (Reveal.js 슬라이드로 취급)
  dir  — 이미 풀린 디렉토리

호출 예:
  python -m scripts.lecture_archive.orchestrate <input-path> --slug my-lecture
"""
from __future__ import annotations

import argparse
import shutil
import zipfile
from pathlib import Path
from typing import Dict, Optional
import yaml

from .utils import slug_from_filename


REPO_ROOT = Path(__file__).resolve().parents[2]

# 입력 확장자 → 처리 타입
_ZIP_EXTS  = {".zip"}
_PDF_EXTS  = {".pdf"}
_HTML_EXTS = {".html", ".htm"}


# ---------------------------------------------------------------------------
# 입력 타입 감지
# ---------------------------------------------------------------------------

def detect_input_type(input_path: Path) -> str:
    """입력 경로의 종류를 반환: 'zip' | 'pdf' | 'html' | 'dir' | 'unknown'"""
    if input_path.is_dir():
        return "dir"
    ext = input_path.suffix.lower()
    if ext in _ZIP_EXTS:
        return "zip"
    if ext in _PDF_EXTS:
        return "pdf"
    if ext in _HTML_EXTS:
        return "html"
    return "unknown"


# ---------------------------------------------------------------------------
# 입력별 00_input 준비
# ---------------------------------------------------------------------------

def prepare_zip(zip_path: Path, dst: Path) -> None:
    """zip 해제. 한글 파일명 cp437→utf-8 디코드."""
    dst.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            try:
                info.filename = info.filename.encode("cp437").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
            z.extract(info, dst)
    # 중첩 zip 재귀 해제
    for nested in list(dst.rglob("*.zip")) + list(dst.rglob("*.Zip")) + list(dst.rglob("*.ZIP")):
        if nested.parent == dst.parent:
            continue
        try:
            with zipfile.ZipFile(nested) as z:
                nested_dst = nested.parent / nested.stem
                nested_dst.mkdir(parents=True, exist_ok=True)
                for info in z.infolist():
                    try:
                        info.filename = info.filename.encode("cp437").decode("utf-8")
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        pass
                    z.extract(info, nested_dst)
        except zipfile.BadZipFile:
            continue


def prepare_pdf(pdf_path: Path, dst: Path) -> None:
    """PDF에서 텍스트를 추출해 instructor-notes.md로 저장."""
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(pdf_path, dst / pdf_path.name)

    try:
        import pdfplumber
    except ImportError:
        print("[WARN] pdfplumber 없음 — pip install pdfplumber. 텍스트 추출 스킵.")
        return

    notes_path = dst / "instructor-notes.md"
    lines = []
    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        print(f"[INFO] PDF 총 {total}페이지 추출 중...")
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            if text.strip():
                lines.append(f"## 페이지 {i}\n\n{text.strip()}\n")

    notes_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] PDF 텍스트 추출 → {notes_path} ({len(lines)}페이지)")


def prepare_html(html_path: Path, dst: Path) -> None:
    """HTML 파일을 slides.html로 복사."""
    dst.mkdir(parents=True, exist_ok=True)
    dest = dst / "slides.html"
    shutil.copy2(html_path, dest)
    print(f"[OK] HTML 복사 → {dest}")


def prepare_dir(src_dir: Path, dst: Path) -> None:
    """이미 풀린 디렉토리를 00_input으로 복사 (같은 경로면 스킵)."""
    dst.mkdir(parents=True, exist_ok=True)
    if src_dir.resolve() == dst.resolve():
        print(f"[INFO] 입력 디렉토리 == 00_input, 복사 생략")
        return
    for item in src_dir.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)
    print(f"[OK] 디렉토리 복사 → {dst}")


# ---------------------------------------------------------------------------
# 자산 탐색
# ---------------------------------------------------------------------------

def find_assets(input_dir: Path) -> Dict[str, Optional[Path]]:
    """입력 디렉토리에서 표준 자산 탐색. 우선순위: v2 → 기본."""
    assets: Dict[str, Optional[Path]] = {
        "slides_html": None,
        "instructor_notes": None,
        "handout_html": None,
        "labs_md": None,
        "feature_catalog": None,
    }
    for p in input_dir.rglob("*"):
        if not p.is_file():
            continue
        name = p.name.lower()
        if "__macosx" in str(p).lower():
            continue
        if "slides" in name and name.endswith(".html"):
            if assets["slides_html"] is None or "v2" in name:
                assets["slides_html"] = p
        elif "instructor" in name and name.endswith(".md"):
            if assets["instructor_notes"] is None or "v2" in name:
                assets["instructor_notes"] = p
        elif (name == "handout.html" or name.startswith("handout")) and name.endswith(".html"):
            if assets["handout_html"] is None or "v2" in name:
                assets["handout_html"] = p
        elif name == "labs.md" or (name.startswith("labs") and name.endswith(".md")):
            assets["labs_md"] = p
        elif "feature_ideas" in name or "07_feature" in name:
            assets["feature_catalog"] = p
    return assets


# ---------------------------------------------------------------------------
# atom_mode 결정
# ---------------------------------------------------------------------------

def decide_atom_mode(assets: Dict[str, Optional[Path]], input_type: str) -> str:
    """입력 자산·형식에 따라 atom_mode 자동 결정."""
    if assets.get("feature_catalog"):
        return "feature_catalog"
    if input_type == "html" or assets.get("slides_html"):
        return "slide_group"
    # PDF 또는 노트만 있는 경우
    return "section_heading"


# ---------------------------------------------------------------------------
# brief.yml 생성
# ---------------------------------------------------------------------------

def write_brief(
    workspace: Path,
    slug: str,
    source_path: Path,
    input_type: str,
    assets: Dict[str, Optional[Path]],
) -> Path:
    atom_mode = decide_atom_mode(assets, input_type)
    brief = {
        "slug": slug,
        "title": "[강사 확인 필요]",
        "subtitle": "[강사 확인 필요]",
        "audience": "[강사 확인 필요]",
        "duration_min": 0,
        "environment": "[강사 확인 필요]",
        "input_type": input_type,
        "atom_mode": atom_mode,
        "assets": {
            k: (str(v.relative_to(workspace)) if v else None)
            for k, v in assets.items()
        },
        "source_input": str(source_path),
    }
    out = workspace / "brief.yml"
    out.write_text(yaml.safe_dump(brief, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="강의자료 → _lectures/ 큐레이션 (zip·pdf·html·dir 지원)"
    )
    parser.add_argument("input_path", help="강의자료 경로 (zip·pdf·html·디렉토리)")
    parser.add_argument("--slug", default=None, help="강의 슬러그 (생략 시 파일명에서 추론)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--skip-playwright", action="store_true")
    parser.add_argument("--rerun", choices=["parser", "curator", "builder"], default=None)
    args = parser.parse_args(argv)

    input_path = Path(args.input_path).resolve()
    if not input_path.exists():
        print(f"[ERR] 입력 경로를 찾을 수 없음: {input_path}")
        return 1

    input_type = detect_input_type(input_path)
    if input_type == "unknown":
        print(f"[ERR] 지원하지 않는 형식: {input_path.suffix}")
        print("      지원 형식: .zip, .pdf, .html, .htm, 디렉토리")
        return 1

    slug = args.slug or slug_from_filename(input_path.name)
    workspace = REPO_ROOT / "_workspace" / slug
    input_dir = workspace / "00_input"

    print(f"[INFO] 입력 형식: {input_type}")
    print(f"[INFO] slug:      {slug}")
    print(f"[INFO] workspace: {workspace}")

    if not args.rerun:
        if workspace.exists():
            from datetime import datetime
            backup = workspace.with_name(f"{slug}_{datetime.now():%Y%m%d_%H%M%S}")
            workspace.rename(backup)
            print(f"[INFO] 기존 workspace 백업 → {backup.name}")
        workspace.mkdir(parents=True)

        dispatch = {
            "zip": prepare_zip,
            "pdf": prepare_pdf,
            "html": prepare_html,
            "dir": prepare_dir,
        }
        dispatch[input_type](input_path, input_dir)

    assets = find_assets(input_dir)
    found = [k for k, v in assets.items() if v]
    print(f"[INFO] 자산 발견: {found}")

    brief_path = write_brief(workspace, slug, input_path, input_type, assets)
    print(f"[OK] brief.yml → {brief_path}")
    print()
    print("[NEXT] 에이전트 팀을 시작할 준비가 됐습니다.")
    print(f"       슬래시 커맨드: /lecture-archive {input_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
