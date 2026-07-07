"""Generate uniform OG-style covers for the Book-Publisher manuscript cards.

Same editorial direction as gen_lecture_cover.py — slate navy gradient,
Pretendard typography, one accent color per volume, a ghost volume numeral
instead of the terminal mockup. Output: assets/lectures/books/book-0N-cover.jpg

Setup (.fonts/ is gitignored, download once):
    mkdir -p .fonts
    base="https://github.com/orioncactus/pretendard/raw/main/packages/pretendard/dist/public/static"
    for w in Black Bold SemiBold Medium Regular; do
      curl -sL -o ".fonts/Pretendard-$w.otf" "$base/Pretendard-$w.otf"
    done
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / ".fonts"
OUT_DIR = ROOT / "assets" / "lectures" / "books"

W, H = 1200, 630

BG_TOP = (15, 23, 42)
BG_BOTTOM = (23, 32, 58)
INK = (248, 250, 252)
INK_DIM = (148, 163, 184)
INK_MUTED = (100, 116, 139)
LINE = (51, 65, 85)

BOOKS = [
    {
        "volume": 7,
        "slug": "book-07",
        "accent": (96, 165, 250),   # blue-400
        "title_lines": ["교육자를 위한", "에이전트 엔지니어링"],
        "subtitle": "프롬프트에서 하네스까지, 교육 에이전트 설계·운영 실전 가이드",
        "chips": ["13장 + 부록 A~C", "교사 · 강사 · 교수"],
        "status": "최신",
    },
    {
        "volume": 6,
        "slug": "book-06",
        "accent": (167, 139, 250),  # violet-400
        "title_lines": ["AI의 지문", "강이솔의 수사일지"],
        "subtitle": "AI 오류 사건 10건을 수사하는 스토리 학습서",
        "chips": ["Case 10편 + 부록 A~C", "초5-6 · 중1-2"],
        "status": None,
    },
    {
        "volume": 5,
        "slug": "book-05",
        "accent": (52, 211, 153),   # emerald-400
        "title_lines": ["명탐정 준의", "AI 수사일지"],
        "subtitle": "소년 탐정 준과 AI 히어로들의 수사 학습 어드벤처",
        "chips": ["수사일지 10편 + 부록 A~C", "초5-6 · 중1-2"],
        "status": None,
    },
    {
        "volume": 4,
        "slug": "book-04",
        "accent": (251, 146, 60),   # orange-400
        "title_lines": ["바이브 코딩을 위한", "Git & GitHub 완벽 가이드"],
        "subtitle": "비개발자 교사를 위한 버전 관리 입문",
        "chips": ["10장 + 부록 A~B", "바이브 코딩 입문자"],
        "status": None,
    },
    {
        "volume": 3,
        "slug": "book-03",
        "accent": (56, 189, 248),   # sky-400
        "title_lines": ["AI 디지털 교육의", "본질 그리고 확장"],
        "subtitle": "이론 기반으로 다시 보는 AI 디지털 교육",
        "chips": ["12장 + 부록 A~C", "중급 교사"],
        "status": None,
    },
    {
        "volume": 2,
        "slug": "book-02",
        "accent": (251, 113, 133),  # rose-400
        "title_lines": ["교사를 위한 Claude Code", "& Cowork 완벽 가이드"],
        "subtitle": "두 도구를 한 권으로 익히는 비개발자 가이드",
        "chips": ["15장 + 부록 A~J", "교사 · 강사"],
        "status": "이전 판",
    },
    {
        "volume": 1,
        "slug": "book-01",
        "accent": (251, 191, 36),   # amber-400
        "title_lines": ["교사를 위한", "클로드코드 완벽 입문"],
        "subtitle": "VS Code로 시작하는 AI 수업 조교",
        "chips": ["11장 + 부록 A~F", "초등 담임 교사"],
        "status": "이전 판",
    },
]


def font(weight: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / f"Pretendard-{weight}.otf"), size)


def text_width(d: ImageDraw.ImageDraw, s: str, f: ImageFont.FreeTypeFont) -> int:
    bbox = d.textbbox((0, 0), s, font=f)
    return bbox[2] - bbox[0]


def fit_font(d: ImageDraw.ImageDraw, s: str, weight: str, size: int, max_w: int) -> ImageFont.FreeTypeFont:
    """Shrink from `size` until the string fits in max_w."""
    while size > 24:
        f = font(weight, size)
        if text_width(d, s, f) <= max_w:
            return f
        size -= 4
    return font(weight, size)


def vertical_gradient(size: Tuple[int, int], top: tuple, bottom: tuple) -> Image.Image:
    w, h = size
    grad = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        grad.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return grad.resize((w, h))


def add_glow(canvas: Image.Image, accent: tuple) -> None:
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 520, -240, W + 180, 320], fill=accent + (60,))
    gd.ellipse([-180, H - 260, 320, H + 140], fill=accent + (22,))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    canvas.alpha_composite(glow)


def add_grid(canvas: Image.Image) -> None:
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for x in range(0, W, 28):
        for y in range(0, H, 28):
            d.point((x, y), fill=(148, 163, 184, 22))
    canvas.alpha_composite(layer)


def draw_ghost_numeral(canvas: Image.Image, volume: int, accent: tuple) -> None:
    """Oversized watermark volume number on the right."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    s = f"{volume:02d}"
    f = font("Black", 430)
    bbox = d.textbbox((0, 0), s, font=f)
    tw = bbox[2] - bbox[0]
    d.text((W - tw - 40, 90), s, font=f, fill=accent + (34,))
    canvas.alpha_composite(layer)


def draw_cover(book: dict) -> Path:
    canvas = vertical_gradient((W, H), BG_TOP, BG_BOTTOM).convert("RGBA")
    accent = book["accent"]
    add_glow(canvas, accent)
    add_grid(canvas)
    draw_ghost_numeral(canvas, book["volume"], accent)

    d = ImageDraw.Draw(canvas)
    d.rectangle([0, 0, 6, H], fill=accent)

    x = 70
    max_w = 800

    # Eyebrow
    y = 84
    d.rectangle([x, y + 6, x + 36, y + 10], fill=accent)
    d.text((x + 50, y), "DOT CONNECTOR BOOKS", font=font("Bold", 16), fill=accent)
    d.text((x + 50 + 245, y), f"·  제{book['volume']}권", font=font("Medium", 16), fill=INK_DIM)

    # Title — line 1 accent, line 2 main ink (both autofit)
    f1 = fit_font(d, book["title_lines"][0], "Black", 66, max_w)
    d.text((x, 148), book["title_lines"][0], font=f1, fill=accent)
    f2 = fit_font(d, book["title_lines"][1], "Black", 84, max_w)
    d.text((x, 236), book["title_lines"][1], font=f2, fill=INK)

    # Underline + subtitle
    d.rectangle([x, 356, x + 120, 360], fill=accent)
    fs = fit_font(d, book["subtitle"], "Medium", 26, W - x - 90)
    d.text((x, 380), book["subtitle"], font=fs, fill=INK_DIM)

    # Chips
    cy = 448
    cx = x
    chips: List[Tuple[str, tuple]] = [(c, INK_DIM) for c in book["chips"]]
    if book["status"]:
        chips.insert(0, (book["status"], accent))
    for label, color in chips:
        f = font("SemiBold", 18)
        tw = text_width(d, label, f)
        bh = 40
        d.rounded_rectangle([cx, cy, cx + tw + 36, cy + bh], radius=bh // 2, outline=color, width=2)
        d.text((cx + 18, cy + 8), label, font=f, fill=color)
        cx += tw + 36 + 12

    # Footer
    d.line([70, H - 70, W - 70, H - 70], fill=LINE, width=1)
    d.text((70, H - 52), "집필 닷커넥터 김진관 · AI 멀티에이전트 파이프라인", font=font("Medium", 16), fill=INK_DIM)
    right = "tigerjk9.github.io  /  lectures"
    f = font("SemiBold", 16)
    tw = text_width(d, right, f)
    d.text((W - 70 - tw, H - 52), right, font=f, fill=INK)

    out = OUT_DIR / f"{book['slug']}-cover.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out, "JPEG", quality=90, optimize=True)
    return out


def main() -> None:
    for book in BOOKS:
        out = draw_cover(book)
        print(f"[OK] {out.relative_to(ROOT)}  ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
