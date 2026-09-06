"""「40분 중 20분, AI를 껐습니다」 발표 자료실 OG 커버 생성.

gen_lecture_cover.py / gen_elementary_assessment_cover.py 와 같은 시각 언어
(슬레이트 네이비 그라데이션 + 블루/앰버 액센트 + 도트 그리드 + Pretendard)를 쓰되,
주제를 담는 모티프는 한 차시 40분의 흐름 막대다.

  [ AI 도구 10분 ] [ 판단과 성찰 · 도구 없이 20분 ] [ AI 도구 10분 ]

가운데 20분만 도구를 들이지 않는다는 설계를 한눈에 보여 준다. 양옆 구간이 AI를
실제로 쓰는 모습을 함께 담아, 제목이 잘려 인용돼도 'AI 반대'로 오해되지 않도록 한다.

폰트는 .fonts/ 에 Pretendard(.otf)가 있어야 한다(gitignore).

    py scripts/gen_ai_off_cover.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / ".fonts"
OUT = ROOT / "assets" / "lectures" / "ai-off-for-20-minutes" / "cover.jpg"

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

SIDE_FILL = (30, 45, 72)      # AI 도구 구간 (블루 계열)
MID_FILL = (92, 62, 20)       # 판단과 성찰 구간 (앰버 계열)


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / f"Pretendard-{weight}.otf"), size)


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
    gd.ellipse([-180, H - 260, 320, H + 140], fill=(251, 191, 36, 30))
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120)))


def add_grid(canvas: Image.Image) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, W, 28):
        for y in range(0, H, 28):
            d.point((x, y), fill=(148, 163, 184, 22))
    canvas.alpha_composite(layer)


def text_w(d, s, f) -> float:
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def draw_eyebrow(canvas: Image.Image) -> None:
    d = ImageDraw.Draw(canvas)
    x, y = 70, 78
    d.rectangle([x, y + 6, x + 36, y + 10], fill=ACCENT)
    lead = "2026 에듀테크 코리아 페어"
    d.text((x + 50, y), lead, font=font("Bold", 17), fill=ACCENT_SOFT)
    tw = text_w(d, lead, font("Bold", 17))
    d.text((x + 50 + tw + 16, y), "·  이노베이션 아레나 · 교사 실행 사례",
           font=font("Medium", 17), fill=INK_DIM)


def draw_title(canvas: Image.Image) -> None:
    d = ImageDraw.Draw(canvas)
    x = 70
    d.text((x, 126), "40분 중 20분,", font=font("SemiBold", 40), fill=ACCENT)
    d.text((x, 190), "AI를 껐습니다", font=font("Black", 82), fill=INK)
    d.rectangle([x, 300, x + 118, 305], fill=WARM)
    d.text((x, 328), "수업설계안에 담긴 판단과 성찰",
           font=font("Medium", 25), fill=INK_DIM)


def draw_timeline(canvas: Image.Image) -> None:
    """한 차시 40분을 분수(分數)에 비례한 세 구간의 막대로 표현."""
    d = ImageDraw.Draw(canvas)
    x0, x1 = 70, W - 70
    span = x1 - x0

    d.text((x0, 410), "한 차시 40분의 설계", font=font("SemiBold", 16), fill=INK_DIM)

    def mx(minute):  # 분 → x 좌표
        return x0 + span * (minute / 40)

    top, h = 448, 72
    gap = 12  # 셀 사이 간격

    # (시작분, 끝분, fill, outline, 라벨, 라벨색, 시간, 시간색)
    cells = [
        (0, 10, SIDE_FILL, ACCENT, "AI 도구", ACCENT_SOFT, "10분", INK_MUTED),
        (10, 30, MID_FILL, WARM, "판단과 성찰", INK, "도구 없이 20분", WARM),
        (30, 40, SIDE_FILL, ACCENT, "AI 도구", ACCENT_SOFT, "10분", INK_MUTED),
    ]

    for i, (m0, m1, fill, outline, label, lab_col, sub, sub_col) in enumerate(cells):
        cx0 = mx(m0) + (gap / 2 if i > 0 else 0)
        cx1 = mx(m1) - (gap / 2 if i < len(cells) - 1 else 0)
        d.rounded_rectangle([cx0, top, cx1, top + h], radius=12,
                            fill=fill, outline=outline, width=2)
        cw = cx1 - cx0
        is_mid = i == 1
        fl = font("Bold", 26 if is_mid else 20)
        lw = text_w(d, label, fl)
        d.text((cx0 + (cw - lw) / 2, top + (14 if is_mid else 16)),
               label, font=fl, fill=lab_col)
        fs = font("Medium", 15 if is_mid else 13)
        sw = text_w(d, sub, fs)
        d.text((cx0 + (cw - sw) / 2, top + (44 if is_mid else 42)),
               sub, font=fs, fill=sub_col)

    # 분 눈금: 0 · 10 · 30 · 40 (가운데 구간의 경계를 드러냄)
    fm = font("Medium", 13)
    for minute, anchor in ((0, "l"), (10, "c"), (30, "c"), (40, "r")):
        tx = mx(minute)
        label = f"{minute}분"
        lw = text_w(d, label, fm)
        if anchor == "l":
            px = tx
        elif anchor == "r":
            px = tx - lw
        else:
            px = tx - lw / 2
        d.text((px, top + h + 8), label, font=fm, fill=INK_MUTED)


def draw_footer(canvas: Image.Image) -> None:
    d = ImageDraw.Draw(canvas)
    d.line([70, H - 60, W - 70, H - 60], fill=LINE, width=1)
    d.text((70, H - 44), "발표 김진관 · 닷커넥터 · 2026.09.19 코엑스",
           font=font("Medium", 15), fill=INK_DIM)
    right = "tigerjk9.github.io  /  lectures"
    f = font("SemiBold", 15)
    d.text((W - 70 - text_w(d, right, f), H - 44), right, font=f, fill=INK)


def main() -> None:
    base = vertical_gradient((W, H), BG_TOP, BG_BOTTOM).convert("RGBA")
    add_glow(base)
    add_grid(base)
    ImageDraw.Draw(base).rectangle([0, 0, 6, H], fill=ACCENT)
    draw_eyebrow(base)
    draw_title(base)
    draw_timeline(base)
    draw_footer(base)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT, "JPEG", quality=92, optimize=True)
    print(f"[OK] wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
