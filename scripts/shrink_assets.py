#!/usr/bin/env python
"""assets/ 이미지를 표시 크기에 맞게 줄인다. 기본은 미리보기(dry-run).

블로그 본문 표시폭은 약 900px인데 12,000px짜리 원본이 그대로 올라가 있다.
GitHub Pages 1GB 한도가 코앞이라(2026-09-16 기준 930MB) 표시에 쓰이지 않는
픽셀을 걷어낸다.

  py -X utf8 scripts/shrink_assets.py                # 미리보기
  py -X utf8 scripts/shrink_assets.py --apply        # 실제 적용
  py -X utf8 scripts/shrink_assets.py --max-width 1600 --quality 85

원칙:
  * **확장자를 바꾸지 않는다.** PNG는 PNG로 남긴다 — 포스트 본문의 `<img src>`를
    고치지 않아도 되게. 이름이 바뀌면 679편을 전부 손봐야 하고 그만큼 사고가 난다.
  * **줄이기만 한다.** 이미 작은 것은 건드리지 않는다.
  * 줄여도 용량이 안 줄면 원본을 그대로 둔다.
  * 카드(1080x1350)·로고·파비콘 등 의도된 규격은 건너뛴다.
"""
from __future__ import annotations

import argparse
import io
import math
import sys
from pathlib import Path

from PIL import Image, ImageChops

Image.MAX_IMAGE_PIXELS = None          # 논문 figure 원본이 매우 클 수 있다

REPO = Path(__file__).resolve().parent.parent
ASSETS = REPO / "assets"
EXTS = {".png", ".jpg", ".jpeg", ".webp"}

# 규격이 의미를 갖는 것들 — 줄이면 안 된다
SKIP_NAMES = {"logo.jpg", "logo.png", "favicon.png", "favicon.ico"}
SKIP_SUFFIXES = ("-card.jpg", "-card.png")     # 소셜 카드 1080x1350


MAX_QUANT_RMS = 5.0        # 256색 양자화 허용 오차 (0~255 척도). 실측치는 1.6~3.8이었다.


def rms_error(a: Image.Image, b: Image.Image) -> float:
    """두 이미지의 채널별 RMS 차이. 팔레트 양자화가 그림을 뭉갰는지 본다."""
    hist = ImageChops.difference(a, b).histogram()
    total = squares = 0
    for ch in range(3):
        for value, count in enumerate(hist[ch * 256:(ch + 1) * 256]):
            squares += count * value * value
            total += count
    return math.sqrt(squares / total) if total else 0.0


def is_opaque(im: Image.Image) -> bool:
    if im.mode not in ("RGBA", "LA", "P"):
        return True
    alpha = im.convert("RGBA").getchannel("A")
    return alpha.getextrema()[0] == 255


def reencode(path: Path, max_width: int, quality: int) -> bytes | None:
    """줄인 바이트를 돌려준다. 줄일 필요가 없거나 이득이 없으면 None."""
    with Image.open(path) as im:
        im.load()
        w, h = im.size
        if w <= max_width:
            return None
        new_h = max(1, round(h * max_width / w))
        resized = im.resize((max_width, new_h), Image.LANCZOS)

        buf = io.BytesIO()
        ext = path.suffix.lower()
        if ext in (".jpg", ".jpeg"):
            resized.convert("RGB").save(buf, "JPEG", quality=quality,
                                        optimize=True, progressive=True)
        elif ext == ".webp":
            resized.save(buf, "WEBP", quality=quality, method=6)
        else:  # PNG — 확장자를 지키되, 불투명하면 팔레트로 줄인다
            if is_opaque(resized):
                out = resized.convert("RGB")
                pal = out.quantize(colors=256, method=Image.MEDIANCUT,
                                   dither=Image.FLOYDSTEINBERG)
                a, b = io.BytesIO(), io.BytesIO()
                out.save(a, "PNG", optimize=True, compress_level=9)
                # 256색으로 뭉갰을 때 손실이 크면(그라디언트가 많은 사진 등)
                # 용량이 줄더라도 팔레트본을 쓰지 않는다.
                use_pal = a.tell() > 0 and rms_error(out, pal.convert("RGB")) <= MAX_QUANT_RMS
                if use_pal:
                    pal.save(b, "PNG", optimize=True, compress_level=9)
                buf = b if use_pal and b.tell() < a.tell() else a
            else:
                resized.save(buf, "PNG", optimize=True, compress_level=9)

    data = buf.getvalue()
    return data if len(data) < path.stat().st_size else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--max-width", type=int, default=1600,
                    help="이 폭을 넘는 것만 줄인다 (기본 1600 = 표시폭 900의 약 1.8배)")
    ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--min-size", type=int, default=200 * 1024,
                    help="이보다 작은 파일은 건드리지 않는다")
    ap.add_argument("--limit", type=int, default=0, help="처음 N개만 (시험용)")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    targets = []
    for p in sorted(ASSETS.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXTS:
            continue
        if p.name in SKIP_NAMES or p.name.endswith(SKIP_SUFFIXES):
            continue
        if p.stat().st_size < a.min_size:
            continue
        targets.append(p)
    if a.limit:
        targets = targets[:a.limit]

    before = after = 0
    changed = []
    failed = []
    for p in targets:
        size = p.stat().st_size
        try:
            data = reencode(p, a.max_width, a.quality)
        except Exception as exc:  # noqa: BLE001
            failed.append((p, type(exc).__name__))
            continue
        if not data:
            continue
        before += size
        after += len(data)
        changed.append((size - len(data), size, len(data), p))
        if a.apply:
            tmp = p.with_name(p.name + ".shrink.tmp")
            tmp.write_bytes(data)
            tmp.replace(p)

    changed.sort(reverse=True)
    for saved, old, new, p in changed[:15]:
        print(f"  -{saved / 1024 / 1024:>5.1f}MB  {old / 1024 / 1024:>5.1f} -> "
              f"{new / 1024 / 1024:<5.1f}MB  {p.relative_to(ASSETS)}")
    if len(changed) > 15:
        print(f"  ... 외 {len(changed) - 15}개")
    for p, err in failed[:5]:
        print(f"  [실패] {p.relative_to(ASSETS)} — {err}")

    print(f"\n대상 {len(targets):,}개 중 {len(changed):,}개 축소 "
          f"({before / 1024 / 1024:.0f}MB -> {after / 1024 / 1024:.0f}MB, "
          f"-{(before - after) / 1024 / 1024:.0f}MB)")
    print("적용됨" if a.apply else "미리보기 — 적용하려면 --apply")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
