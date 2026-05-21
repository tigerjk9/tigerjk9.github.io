"""강의자료 큐레이션 진입점.

호출 예:
  python -m scripts.lecture_archive.orchestrate <zip-path> --slug kist-claude-code
"""
from __future__ import annotations
import argparse
import zipfile
from pathlib import Path
from typing import Dict, Optional
import yaml

from .utils import slug_from_zip_name


REPO_ROOT = Path(__file__).resolve().parents[2]


def extract_zip(zip_path: Path, dst: Path) -> None:
    """zip 해제. 한글 파일명 cp437→utf-8 디코드."""
    dst.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            try:
                info.filename = info.filename.encode("cp437").decode("utf-8")
            except (UnicodeEncodeError, UnicodeDecodeError):
                pass
            z.extract(info, dst)
    # Handle nested zips
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
        # Skip macOS metadata
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


def write_brief(workspace: Path, slug: str, zip_path: Path, assets: Dict[str, Optional[Path]]) -> Path:
    brief = {
        "slug": slug,
        "title": "[강사 확인 필요]",
        "subtitle": "[강사 확인 필요]",
        "audience": "[강사 확인 필요]",
        "duration_min": 0,
        "environment": "[강사 확인 필요]",
        "atom_mode": "feature_catalog" if assets.get("feature_catalog") else "section_heading",
        "assets": {
            k: (str(v.relative_to(workspace)) if v else None)
            for k, v in assets.items()
        },
        "source_zip": str(zip_path),
    }
    out = workspace / "brief.yml"
    out.write_text(yaml.safe_dump(brief, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return out


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="강의자료 zip → _lectures/ 큐레이션")
    parser.add_argument("zip_path", help="강의자료 zip 절대 경로")
    parser.add_argument("--slug", default=None, help="강의 슬러그 (생략 시 zip 파일명에서 추론)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--skip-playwright", action="store_true")
    parser.add_argument("--rerun", choices=["parser", "curator", "builder"], default=None)
    args = parser.parse_args(argv)

    zip_path = Path(args.zip_path).resolve()
    if not zip_path.exists():
        print(f"[ERR] zip not found: {zip_path}")
        return 1

    slug = args.slug or slug_from_zip_name(zip_path.name)
    workspace = REPO_ROOT / "_workspace" / slug
    input_dir = workspace / "00_input"

    print(f"[INFO] slug: {slug}")
    print(f"[INFO] workspace: {workspace}")

    if not args.rerun:
        if workspace.exists():
            from datetime import datetime
            backup = workspace.with_name(f"{slug}_{datetime.now():%Y%m%d_%H%M%S}")
            workspace.rename(backup)
            print(f"[INFO] backed up existing workspace -> {backup.name}")
        workspace.mkdir(parents=True)
        extract_zip(zip_path, input_dir)

    assets = find_assets(input_dir)
    found = [k for k, v in assets.items() if v]
    print(f"[INFO] assets found: {found}")

    brief_path = write_brief(workspace, slug, zip_path, assets)
    print(f"[OK] brief.yml -> {brief_path}")
    print()
    print("[NEXT] Superpowers 멀티 에이전트 팀을 시작할 준비가 됐습니다.")
    print(f"       다음 단계는 .claude/skills/lecture-archive-orchestrator/SKILL.md 참조")
    print(f"       또는 슬래시 커맨드 /lecture-archive {zip_path} 로 자동 진행")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
