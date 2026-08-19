"""Generate the OG cover for the 서·논술형 평가도구 개발 자료 archive page.

Same editorial dark-slate family as gen_elementary_assessment_cover.py
(blue/amber on slate-900 gradient, Pretendard), but the lower motif is a row of
subject cards with page counts — the archive is a multi-subject document set.

Fonts live in .fonts/ (gitignored). Pretendard TTFs required.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / ".fonts"
OUT = ROOT / "assets" / "lectures" / "eval-assessment-tool" / "cover.jpg"

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

# 교과별 PDF 쪽수 = 평가도구 개발 자료 + 평가지 모음 (합계 2,519쪽 = 표지 상단 수치)
SUBJECTS = [("국어", "514쪽"), ("수학", "649쪽"), ("사회", "657쪽"), ("과학", "699쪽")]


def font(weight, size):
    return ImageFont.truetype(str(FONT_DIR / f"Pretendard-{weight}.ttf"), size)


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
    x, y = 70, 74
    d.rectangle([x, y + 6, x + 36, y + 10], fill=ACCENT)
    label = "2026학년도 초등학교 학생평가"
    d.text((x + 50, y), label, font=font("Bold", 17), fill=ACCENT_SOFT)
    tw = text_w(d, label, font("Bold", 17))
    d.text((x + 50 + tw + 16, y), "·  대전교육과학연구원", font=font("Medium", 17), fill=INK_DIM)


def draw_title(canvas):
    d = ImageDraw.Draw(canvas)
    x = 70
    d.text((x, 122), "3~6학년 국어 · 수학 · 사회 · 과학", font=font("SemiBold", 38), fill=ACCENT)
    d.text((x, 182), "서·논술형 평가도구", font=font("Black", 76), fill=INK)
    d.text((x, 268), "개발 자료", font=font("Black", 76), fill=INK)
    d.rectangle([x, 372, x + 118, 377], fill=WARM)
    d.text((x, 398), "1·2학기 전체  ·  PDF 2,519쪽  ·  편집용 HWP 포함",
           font=font("Medium", 25), fill=INK_DIM)


def draw_subject_cards(canvas):
    """A row of subject cards — the archive spans four subjects."""
    d = ImageDraw.Draw(canvas)
    x0, top, h, gap = 70, 452, 74, 14
    total = W - 70 - x0
    cw = (total - gap * (len(SUBJECTS) - 1)) / len(SUBJECTS)
    for i, (name, pages) in enumerate(SUBJECTS):
        cx = x0 + i * (cw + gap)
        d.rounded_rectangle([cx, top, cx + cw, top + h], radius=12,
                            fill=(30, 41, 59), outline=LINE, width=2)
        d.rectangle([cx + 1, top + 14, cx + 5, top + h - 14], fill=ACCENT if i % 2 == 0 else WARM)
        f = font("Bold", 24)
        d.text((cx + 22, top + 12), name, font=f, fill=INK)
        f2 = font("Medium", 15)
        d.text((cx + 22, top + 44), pages, font=f2, fill=INK_MUTED)


def draw_footer(canvas):
    d = ImageDraw.Draw(canvas)
    d.line([70, H - 62, W - 70, H - 62], fill=LINE, width=1)
    d.text((70, H - 44), "자료 대전교육과학연구원  ·  아카이빙 닷커넥터",
           font=font("Medium", 15), fill=INK_DIM)
    right = "tigerjk9.github.io  /  lectures"
    f = font("SemiBold", 15)
    d.text((W - 70 - text_w(d, right, f), H - 44), right, font=f, fill=INK)


def main():
    base = vertical_gradient((W, H), BG_TOP, BG_BOTTOM).convert("RGBA")
    add_glow(base)
    add_grid(base)
    ImageDraw.Draw(base).rectangle([0, 0, 6, H], fill=ACCENT)
    draw_eyebrow(base)
    draw_title(base)
    draw_subject_cards(base)
    draw_footer(base)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT, "JPEG", quality=92, optimize=True)
    print(f"[OK] wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
