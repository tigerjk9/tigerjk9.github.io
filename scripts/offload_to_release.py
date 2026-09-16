#!/usr/bin/env python
"""대용량 문서를 GitHub 릴리스로 옮기고 본문 링크를 바꾼다. 기본은 미리보기.

GitHub Pages는 발행 사이트 1GB가 한도인데 강의 PDF·HWP가 그 대부분을 먹는다.
릴리스 자산은 이 한도에 포함되지 않으므로(파일당 2GB) 거기로 보낸다.

  py -X utf8 scripts/offload_to_release.py --dir assets/lectures/<slug> --tag <tag>
  py -X utf8 scripts/offload_to_release.py ... --apply

동작:
  1) 대상 디렉터리(+ --extra 로 지정한 개별 파일)의 문서 파일을 모은다
  2) **내용 해시로 중복을 묶어** 릴리스에는 한 번만 올린다 — 같은 파일이 포스트용과
     강의용으로 두 벌 있는 경우가 실제로 있었다(44MB)
  3) `_posts`·`_lectures` 등의 `/assets/...` 링크를 릴리스 URL로 바꾼다
  4) 원본을 지운다 (git rm)

주의: 릴리스는 한글 파일명을 뭉갠다. 자산 이름은 영문 슬러그만 쓴다.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOC_EXTS = {".pdf", ".hwp", ".hwpx", ".pptx", ".zip"}
SEARCH_DIRS = ["_posts", "_pages", "_lectures", "_data", "_includes", "_layouts"]
RELEASE_URL = "https://github.com/tigerjk9/tigerjk9.github.io/releases/download/{tag}/{name}"
SAFE_NAME = re.compile(r"^[A-Za-z0-9._-]+$")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_files() -> list[Path]:
    out = []
    for d in SEARCH_DIRS:
        base = REPO / d
        if base.is_dir():
            out += [p for p in base.rglob("*")
                    if p.is_file() and p.suffix.lower() in (".md", ".html", ".yml")]
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dir", action="append", default=[],
                    help="옮길 디렉터리 (repo 기준 상대경로, 반복 가능)")
    ap.add_argument("--extra", action="append", default=[],
                    help="개별 파일 추가 (repo 기준 상대경로, 반복 가능)")
    ap.add_argument("--tag", required=True, help="릴리스 태그")
    ap.add_argument("--min-size", type=int, default=1024 * 1024,
                    help="이보다 작은 문서는 저장소에 둔다 (기본 1MB)")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    files: list[Path] = []
    for d in a.dir:
        base = REPO / d
        files += [p for p in sorted(base.rglob("*"))
                  if p.is_file() and p.suffix.lower() in DOC_EXTS]
    for f in a.extra:
        p = REPO / f
        if p.is_file():
            files.append(p)
    files = [p for p in dict.fromkeys(files) if p.stat().st_size >= a.min_size]
    if not files:
        print("대상 없음")
        return 0

    # 내용이 같으면 하나만 올린다
    groups: dict[str, list[Path]] = {}
    for p in files:
        groups.setdefault(sha(p), []).append(p)

    texts = {p: p.read_text(encoding="utf-8") for p in text_files()}

    plan = []       # (asset_name, canonical_path, [all paths], bytes, [(textfile, old_url)])
    bad = []
    for digest, paths in groups.items():
        canon = min(paths, key=lambda p: len(p.as_posix()))
        name = canon.name
        if not SAFE_NAME.match(name):
            bad.append(canon)
            continue
        hits = []
        for p in paths:
            url = "/" + p.relative_to(REPO).as_posix()
            for tf, body in texts.items():
                if url in body:
                    hits.append((tf, url))
        plan.append((name, canon, paths, canon.stat().st_size, hits))

    names = [n for n, *_ in plan]
    assert len(names) == len(set(names)), "릴리스 자산 이름이 겹친다: " + str(
        [n for n in names if names.count(n) > 1])

    total = sum(s for _, _, paths, s, _ in plan for _ in paths)
    saved = sum(s * len(paths) for _, _, paths, s, _ in plan)
    print(f"파일 {len(files)}개 · 고유 {len(plan)}개 · 저장소에서 빠지는 용량 "
          f"{saved / 1024 / 1024:.0f}MB")
    unref = [n for n, c, paths, s, hits in plan if not hits]
    if unref:
        print(f"  본문 참조 없는 파일 {len(unref)}개 (링크 치환 없이 이동): "
              f"{', '.join(unref[:4])}{' ...' if len(unref) > 4 else ''}")
    for p in bad:
        print(f"  [건너뜀] 영문 슬러그가 아님: {p.relative_to(REPO)}")

    if not a.apply:
        for name, canon, paths, size, hits in sorted(plan, key=lambda x: -x[3])[:10]:
            dup = f" (사본 {len(paths)}개)" if len(paths) > 1 else ""
            print(f"  {size / 1024 / 1024:>6.1f}MB  {name}{dup}  ← 링크 {len(hits)}곳")
        print("\n미리보기 — 적용하려면 --apply")
        return 0

    # 1) 릴리스 보장 + 업로드
    subprocess.run(["gh", "release", "view", a.tag], capture_output=True, check=False)
    up = ["gh", "release", "upload", a.tag, "--clobber"] + [str(c) for _, c, *_ in plan]
    r = subprocess.run(up, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("[FAIL] 업로드 실패:", r.stderr[:400])
        return 1
    print(f"업로드 완료 {len(plan)}개")

    # 2) 링크 치환
    edited = 0
    for name, canon, paths, size, hits in plan:
        new = RELEASE_URL.format(tag=a.tag, name=name)
        for p in paths:
            old = "/" + p.relative_to(REPO).as_posix()
            for tf in list(texts):
                if old in texts[tf]:
                    texts[tf] = texts[tf].replace(old, new)
                    edited += 1
    for tf, body in texts.items():
        if body != tf.read_text(encoding="utf-8"):
            tf.write_text(body, encoding="utf-8", newline="")
    print(f"링크 치환 {edited}건")

    # 3) 원본 삭제
    rm = ["git", "-C", str(REPO), "rm", "-q", "--"]
    rm += [str(p.relative_to(REPO).as_posix()) for _, _, paths, _, _ in plan for p in paths]
    r = subprocess.run(rm, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print("[FAIL] git rm 실패:", r.stderr[:300])
        return 1
    print("원본 삭제 완료")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
