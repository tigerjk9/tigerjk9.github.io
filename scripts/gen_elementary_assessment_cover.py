"""Generate an OG cover for the 초등 학생평가 전문가 기본과정 lecture hub.

Design: same editorial dark-slate family as gen_lecture_cover.py (blue/amber on
slate-900 gradient, Pretendard), but the right/lower motif is a rubric scale
(채점 척도) instead of a terminal — matching the assessment topic.

Setup (.fonts/ is gitignored, download once): see gen_lecture_cover.py header.
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / ".fonts"
OUT = ROOT / "assets" / "lectures" / "elementary-assessment-expert" / "cover.jpg"

W, H = 1200, 630

BG_TOP = (15, 23, 42)
BG_BOTTOM = (23, 32, 58)
ACCENT = (96, 165, 250)
ACCENT_SOFT = (147, 197, 253)
WARM = (251, 191, 36)
INK = (248, 250, 252)
INK_DIM = (148, 163, 184)
INK_MUTED = (100, 116, 139)
LINE = (51, 65, 85)


def font(weight, size):
    return ImageFont.truetype(str(FONT_DIR / f"Pretendard-{weight}.otf"), size)


def vertical_gradient(size, top, bottom):
    w, h = size
    grad = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        grad.putpixel((0, y), (
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
        ))
    return grad.resize((w, h))


def add_glow(canvas):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 520, -240, W + 180, 320], fill=(96, 165, 250, 70))
    gd.ellipse([-180, H - 260, 320, H + 140], fill=(251, 191, 36, 30))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))


def add_grid(canvas):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, W, 28):
        for y in range(0, H, 28):
            d.point((x, y), fill=(148, 163, 184, 22))
    canvas.alpha_composite(layer)


def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def draw_eyebrow(canvas):
    d = ImageDraw.Draw(canvas)
    x, y = 70, 78
    d.rectangle([x, y + 6, x + 36, y + 10], fill=ACCENT)
    d.text((x + 50, y), "2026 초등 선도교원 연수", font=font("Bold", 17), fill=ACCENT_SOFT)
    tw = text_w(d, "2026 초등 선도교원 연수", font("Bold", 17))
    d.text((x + 50 + tw + 16, y), "·  대전", font=font("Medium", 17), fill=INK_DIM)


def draw_title(canvas):
    d = ImageDraw.Draw(canvas)
    x = 70
    d.text((x, 126), "개념기반 탐구수업으로 만드는", font=font("SemiBold", 40), fill=ACCENT)
    d.text((x, 190), "학생평가 전문가 기본과정", font=font("Black", 82), fill=INK)
    d.rectangle([x, 300, x + 118, 305], fill=WARM)
    d.text((x, 328), "서논술형 평가 도구 제작 · GRASPS 루브릭 설계 · 과정중심평가",
           font=font("Medium", 25), fill=INK_DIM)


def draw_rubric(canvas):
    """A rubric scale band (채점 척도) — 4 levels, blue→amber tint."""
    d = ImageDraw.Draw(canvas)
    x0, y = 70, 418
    d.text((x0, y), "루브릭 채점 척도", font=font("SemiBold", 16), fill=INK_DIM)

    cells = [
        ("노력 요함", (30, 41, 59)),
        ("보통", (30, 58, 95)),
        ("잘함", (37, 99, 160)),
        ("매우 잘함", (180, 120, 30)),
    ]
    labels_ink = [INK_DIM, ACCENT_SOFT, INK, WARM]
    top = y + 30
    h = 66
    gap = 14
    total = W - 70 - x0
    cw = (total - gap * (len(cells) - 1)) / len(cells)
    for i, (label, fill) in enumerate(cells):
        cx = x0 + i * (cw + gap)
        outline = WARM if i == 3 else (ACCENT if i == 2 else LINE)
        d.rounded_rectangle([cx, top, cx + cw, top + h], radius=12,
                            fill=fill, outline=outline, width=2)
        f = font("Bold", 20)
        lw = text_w(d, label, f)
        d.text((cx + (cw - lw) / 2, top + 14), label, font=f, fill=labels_ink[i])
        lv = f"Lv.{i + 1}"
        f2 = font("Medium", 13)
        lw2 = text_w(d, lv, f2)
        d.text((cx + (cw - lw2) / 2, top + 40), lv, font=f2, fill=INK_MUTED)


def draw_footer(canvas):
    d = ImageDraw.Draw(canvas)
    d.line([70, H - 66, W - 70, H - 66], fill=LINE, width=1)
    d.text((70, H - 48),
           "자료 황지연 · 정민수 · 지미정 외 · 2026 대전 학생평가 전문가 과정 연수",
           font=font("Medium", 15), fill=INK_DIM)
    right = "tigerjk9.github.io  /  lectures"
    f = font("SemiBold", 15)
    d.text((W - 70 - text_w(d, right, f), H - 48), right, font=f, fill=INK)


def main():
    base = vertical_gradient((W, H), BG_TOP, BG_BOTTOM).convert("RGBA")
    add_glow(base)
    add_grid(base)
    ImageDraw.Draw(base).rectangle([0, 0, 6, H], fill=ACCENT)
    draw_eyebrow(base)
    draw_title(base)
    draw_rubric(base)
    draw_footer(base)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT, "JPEG", quality=92, optimize=True)
    print(f"[OK] wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
