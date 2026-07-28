"""2026 인공지능 활용 선도교사 연수 아카이브 OG 커버 생성.

gen_lecture_cover.py와 같은 시각 언어(슬레이트 네이비 그라데이션 + 블루 액센트 +
도트 그리드)를 쓰되, 과정을 한눈에 보여주는 스텝 레일을 중심에 둔다.

원격(7과정)과 집합(6과정) 두 아카이브가 같은 판형을 공유하므로 VARIANTS로 갈라 둔다.
폰트는 .fonts/ 에 Pretendard가 있어야 한다(gitignore). ttf/otf 모두 허용.

    py scripts/gen_ai_leading_teacher_cover.py            # 원격·집합 모두
    py scripts/gen_ai_leading_teacher_cover.py onsite     # 집합만
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / ".fonts"

W, H = 1200, 630

BG_TOP = (15, 23, 42)
BG_BOTTOM = (23, 32, 58)
ACCENT = (96, 165, 250)
ACCENT_SOFT = (147, 197, 253)
WARM = (251, 191, 36)
INK = (248, 250, 252)
INK_DIM = (148, 163, 184)
LINE = (51, 65, 85)
CARD_BG = (17, 24, 39)
CARD_BORDER = (55, 65, 81)

VARIANTS = {
    "remote": {
        "slug": "ai-leading-teacher-2026",
        "eyebrow": "·  원격 7과정 · 11차시 · 초등",
        "title2": "원격 연수 아카이브",
        "sub": (
            "교육의 본질을 다시 묻는 데서 출발해 AI 윤리와 수업 설계를 지나",
            "평가와 도구를 하나의 흐름으로 잇는 일곱 과정.",
        ),
        "steps": [
            ("1", "교육의 중심"),
            ("2", "교사의 역할"),
            ("3", "AI 윤리"),
            ("4", "수업 설계"),
            ("5", "수업과 평가"),
            ("6", "도구의 숲"),
            ("7", "설계 실습"),
        ],
        "gap": 152,
        "active": (4, 6),  # 5·7과정 = 본인 설계 과정
    },
    "onsite": {
        "slug": "ai-leading-teacher-2026-onsite",
        "eyebrow": "·  집합 6과정 · 16차시 · 초등",
        "title2": "집합 연수 아카이브",
        "sub": (
            "원격에서 그린 설계안을 동료 앞에서 실행하고 데이터로 되짚어",
            "성장 로드맵까지 잇는 이틀, 여섯 과정.",
        ),
        "steps": [
            ("8", "실천의 문"),
            ("9", "설계 조율"),
            ("10", "마이크로티칭"),
            ("11", "데이터 진단"),
            ("12", "성찰 환류"),
            ("13", "성장 설계"),
        ],
        "gap": 182,
        "active": (2, 5),  # 10·13과정 = 실행과 마무리
    },
}


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    for ext in ("ttf", "otf"):
        p = FONT_DIR / f"Pretendard-{weight}.{ext}"
        if p.exists():
            return ImageFont.truetype(str(p), size)
    raise FileNotFoundError(f"Pretendard-{weight} not found in {FONT_DIR}")


def vertical_gradient(size, top, bottom) -> Image.Image:
    w, h = size
    grad = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        grad.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return grad.resize((w, h))


def add_glow(canvas: Image.Image) -> None:
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 520, -240, W + 180, 320], fill=(96, 165, 250, 70))
    gd.ellipse([-180, H - 260, 320, H + 140], fill=(251, 191, 36, 28))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))


def add_grid(canvas: Image.Image) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, W, 28):
        for y in range(0, H, 28):
            d.point((x, y), fill=(148, 163, 184, 22))
    canvas.alpha_composite(layer)


def draw_header(canvas: Image.Image, spec: dict) -> None:
    d = ImageDraw.Draw(canvas)
    x, y = 70, 74
    d.rectangle([x, y + 6, x + 36, y + 10], fill=ACCENT)
    d.text((x + 50, y), "TEACHER TRAINING ARCHIVE", font=font("Bold", 16), fill=ACCENT_SOFT)
    f = font("Medium", 16)
    d.text((x + 50 + 268, y), spec["eyebrow"], font=f, fill=INK_DIM)

    d.text((x, y + 46), "2026 인공지능 활용 선도교사", font=font("Black", 54), fill=INK)
    d.text((x, y + 112), spec["title2"], font=font("Black", 54), fill=ACCENT_SOFT)

    for i, line in enumerate(spec["sub"]):
        d.text((x, y + 190 + i * 32), line, font=font("Medium", 20), fill=INK_DIM)


def draw_steps(canvas: Image.Image, spec: dict) -> None:
    """과정 번호 칩 + 라벨의 레일로 전체 여정을 표현."""
    d = ImageDraw.Draw(canvas)
    x0, y0 = 70, 400
    gap = spec["gap"]
    steps = spec["steps"]
    for i, (num, label) in enumerate(steps):
        cx = x0 + i * gap
        # 연결선
        if i < len(steps) - 1:
            d.line([cx + 26, y0 + 22, cx + gap - 26, y0 + 22], fill=CARD_BORDER, width=2)
        ring = WARM if i in spec["active"] else ACCENT
        d.ellipse([cx, y0, cx + 44, y0 + 44], fill=CARD_BG, outline=ring, width=2)
        f = font("Bold", 20)
        bb = d.textbbox((0, 0), num, font=f)
        d.text(
            (cx + 22 - (bb[2] - bb[0]) / 2, y0 + 22 - (bb[3] - bb[1]) / 2 - bb[1]),
            num, font=f, fill=ring,
        )
        fl = font("SemiBold", 15)
        bl = d.textbbox((0, 0), label, font=fl)
        d.text((cx + 22 - (bl[2] - bl[0]) / 2, y0 + 58), label, font=fl, fill=INK_DIM)


def draw_footer(canvas: Image.Image) -> None:
    d = ImageDraw.Draw(canvas)
    d.line([70, H - 70, W - 70, H - 70], fill=LINE, width=1)
    d.text(
        (70, H - 52),
        "큐레이션 김진관 · 닷커넥터",
        font=font("Medium", 16),
        fill=INK_DIM,
    )
    right = "tigerjk9.github.io  /  lectures"
    f = font("SemiBold", 16)
    bb = d.textbbox((0, 0), right, font=f)
    d.text((W - 70 - (bb[2] - bb[0]), H - 52), right, font=f, fill=INK)


def render(spec: dict) -> None:
    base = vertical_gradient((W, H), BG_TOP, BG_BOTTOM).convert("RGBA")
    add_glow(base)
    add_grid(base)
    ImageDraw.Draw(base).rectangle([0, 0, 6, H], fill=ACCENT)

    draw_header(base, spec)
    draw_steps(base, spec)
    draw_footer(base)

    out = ROOT / "assets" / "lectures" / spec["slug"] / "cover.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out, "JPEG", quality=92, optimize=True)
    print(f"[OK] wrote {out.relative_to(ROOT)}  ({out.stat().st_size // 1024} KB)")


def main() -> None:
    names = sys.argv[1:] or list(VARIANTS)
    for name in names:
        if name not in VARIANTS:
            raise SystemExit(f"unknown variant: {name} (choose from {', '.join(VARIANTS)})")
        render(VARIANTS[name])


if __name__ == "__main__":
    main()
