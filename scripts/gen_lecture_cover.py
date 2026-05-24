"""Generate a clean OG cover image for the Claude Code lecture hub.

Design direction: editorial / minimal. Strong typographic hierarchy with
Pretendard, a soft navy gradient backdrop, a single accent stripe, and a
restrained terminal mockup. The goal is breathing room — no walls of text.

Setup (.fonts/ is gitignored, download once):
    mkdir -p .fonts
    base="https://github.com/orioncactus/pretendard/raw/main/packages/pretendard/dist/public/static"
    for w in Black Bold SemiBold Medium Regular; do
      curl -sL -o ".fonts/Pretendard-$w.otf" "$base/Pretendard-$w.otf"
    done
"""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / ".fonts"
OUT = ROOT / "assets" / "lectures" / "claude-code-edu" / "cover.jpg"

W, H = 1200, 630

# Palette — anchored to the blog's dark skin
BG_TOP = (15, 23, 42)         # slate-900
BG_BOTTOM = (23, 32, 58)      # slightly lifted
ACCENT = (96, 165, 250)       # blue-400 (Claude-ish)
ACCENT_SOFT = (147, 197, 253) # blue-300
WARM = (251, 191, 36)         # amber-400 highlight
INK = (248, 250, 252)         # near-white text
INK_DIM = (148, 163, 184)     # slate-400
INK_MUTED = (100, 116, 139)   # slate-500
LINE = (51, 65, 85)           # divider
TERM_BG = (17, 24, 39)        # gray-900
TERM_BORDER = (55, 65, 81)


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONT_DIR / f"Pretendard-{weight}.otf"
    return ImageFont.truetype(str(path), size)


def vertical_gradient(size: tuple[int, int], top: tuple, bottom: tuple) -> Image.Image:
    w, h = size
    grad = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        grad.putpixel((0, y), (r, g, b))
    return grad.resize((w, h))


def add_glow(canvas: Image.Image) -> None:
    """Soft accent glow in the upper-right to add depth."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    # Large blue ellipse, blurred
    gd.ellipse([W - 520, -240, W + 180, 320], fill=(96, 165, 250, 70))
    # Warm accent low-left
    gd.ellipse([-180, H - 260, 320, H + 140], fill=(251, 191, 36, 28))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    canvas.alpha_composite(glow)


def add_grid(canvas: Image.Image) -> None:
    """Subtle dot grid — barely there, gives texture without noise."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    step = 28
    for x in range(0, W, step):
        for y in range(0, H, step):
            d.point((x, y), fill=(148, 163, 184, 22))
    canvas.alpha_composite(layer)


def rounded_rect(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int, int, int],
    radius: int,
    fill=None,
    outline=None,
    width: int = 1,
) -> None:
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_eyebrow(canvas: Image.Image) -> None:
    """Small accent stripe + label above the title."""
    d = ImageDraw.Draw(canvas)
    x = 70
    y = 80
    # Accent stripe
    d.rectangle([x, y + 6, x + 36, y + 10], fill=ACCENT)
    label = "EDUCATOR WORKSHOP"
    d.text((x + 50, y), label, font=font("Bold", 16), fill=ACCENT_SOFT)
    d.text((x + 50 + 230, y), "·  120분 · 22개 기능", font=font("Medium", 16), fill=INK_DIM)


def draw_title(canvas: Image.Image) -> None:
    d = ImageDraw.Draw(canvas)
    x = 70

    # Line 1: "Claude Code" — accent color
    d.text((x, 132), "Claude Code", font=font("Black", 88), fill=ACCENT)

    # Line 2: 한글 메인 — biggest, near-white
    d.text((x, 232), "실무 활용 가이드", font=font("Black", 96), fill=INK)

    # Underline accent
    d.rectangle([x, 348, x + 120, 352], fill=WARM)

    # Subtitle — calm, lighter
    d.text(
        (x, 372),
        "교육자를 위한 22개 기능, 2시간 트랙으로 정리하다",
        font=font("Medium", 26),
        fill=INK_DIM,
    )


def draw_tags(canvas: Image.Image) -> None:
    d = ImageDraw.Draw(canvas)
    x = 70
    y = 440
    tags = [
        ("Basic 12", ACCENT),
        ("Advanced 10", WARM),
        ("PowerShell · Windows", INK_DIM),
    ]
    pad_x, pad_y = 18, 9
    for label, color in tags:
        f = font("SemiBold", 18)
        bbox = d.textbbox((0, 0), label, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        w = tw + pad_x * 2
        h = th + pad_y * 2 + 4
        rounded_rect(
            d,
            (x, y, x + w, y + h),
            radius=h // 2,
            outline=color,
            width=2,
        )
        d.text((x + pad_x, y + pad_y - 2), label, font=f, fill=color)
        x += w + 12


def draw_terminal(canvas: Image.Image) -> None:
    """Restrained terminal card on the right."""
    d = ImageDraw.Draw(canvas)

    # Card
    card_x, card_y = 720, 150
    card_w, card_h = 420, 340
    # Shadow
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    rounded_rect(
        sd,
        (card_x + 6, card_y + 14, card_x + card_w + 6, card_y + card_h + 14),
        radius=18,
        fill=(0, 0, 0, 110),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    canvas.alpha_composite(shadow)

    rounded_rect(
        d,
        (card_x, card_y, card_x + card_w, card_y + card_h),
        radius=18,
        fill=TERM_BG,
        outline=TERM_BORDER,
        width=1,
    )

    # macOS-style dots
    dot_y = card_y + 22
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = card_x + 22 + i * 22
        d.ellipse([cx, dot_y, cx + 12, dot_y + 12], fill=color)

    # Tab label
    d.text(
        (card_x + 130, dot_y - 3),
        "claude-code  —  workshop",
        font=font("Medium", 14),
        fill=INK_MUTED,
    )

    # Divider
    d.line(
        [card_x, card_y + 50, card_x + card_w, card_y + 50],
        fill=TERM_BORDER,
        width=1,
    )

    # Prompt lines — chosen to read at-a-glance
    lines = [
        ("$ ", "claude ", "--permission-mode plan"),
        ("$ ", "/skill ", '"논문-요약"'),
        ("$ ", "claude -p ", '"수업안 만들어줘"'),
        ("", "", ""),
        ("> ", "Plan 모드: 변경 없이 ", "계획만"),
        ("> ", "Skill 호출: 한 줄에 ", "한 번 정의"),
        ("> ", "Headless: ", "JSON 자동화"),
    ]
    ty = card_y + 78
    code_font = font("Medium", 17)
    code_bold = font("SemiBold", 17)
    for sigil, cmd, arg in lines:
        if not sigil and not cmd and not arg:
            ty += 10
            continue
        tx = card_x + 28
        sigil_color = ACCENT if sigil.strip() == "$" else WARM
        d.text((tx, ty), sigil, font=code_bold, fill=sigil_color)
        bbox = d.textbbox((0, 0), sigil, font=code_bold)
        tx += bbox[2] - bbox[0]
        d.text((tx, ty), cmd, font=code_bold, fill=INK)
        bbox = d.textbbox((0, 0), cmd, font=code_bold)
        tx += bbox[2] - bbox[0]
        d.text((tx, ty), arg, font=code_font, fill=INK_DIM)
        ty += 30


def draw_footer(canvas: Image.Image) -> None:
    d = ImageDraw.Draw(canvas)
    # Divider
    d.line([70, H - 70, W - 70, H - 70], fill=LINE, width=1)

    # Left: attribution
    d.text(
        (70, H - 52),
        "원작 황민호 · Forward Deployed Engineer, Kakao AI Studio",
        font=font("Medium", 16),
        fill=INK_DIM,
    )

    # Right: site mark
    right = "tigerjk9.github.io  /  lectures"
    f = font("SemiBold", 16)
    bbox = d.textbbox((0, 0), right, font=f)
    tw = bbox[2] - bbox[0]
    d.text((W - 70 - tw, H - 52), right, font=f, fill=INK)


def main() -> None:
    base = vertical_gradient((W, H), BG_TOP, BG_BOTTOM).convert("RGBA")
    add_glow(base)
    add_grid(base)

    # Left rail accent
    d = ImageDraw.Draw(base)
    d.rectangle([0, 0, 6, H], fill=ACCENT)

    draw_eyebrow(base)
    draw_title(base)
    draw_tags(base)
    draw_terminal(base)
    draw_footer(base)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(OUT, "JPEG", quality=92, optimize=True)
    print(f"[OK] wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
