#!/usr/bin/env python3
"""유튜브·웹 아티클·논문(PDF) → 닷커넥터 카드뉴스 이미지 생성.

레퍼런스 디자인(2026-07-19 근쌤AI 카드뉴스 스타일을 닷커넥터 브랜딩으로 번안):
1080x1350(4:5), 아이보리 배경, 상단 로고+날짜, 2줄 헤드라인(둘째 줄 노란 형광),
라운드 이미지, 2줄 본문(존칭체), 출처·페이지 푸터.

이미지 소스:
- YouTube: 실제 영상 프레임(yt-dlp 최저화질 + OpenCV, 인트로·아웃트로 10% 제외 균등)
- 논문·기사: Gemini 이미지 생성(gemini-2.5-flash-image, 16:9) — 실패 시 텍스트 패널 카드

사용법:
  py scripts/cardnews.py <YouTube URL|웹 URL|PDF|로컬 md>  [--cards 8] [--out DIR]
  py scripts/cardnews.py <입력> --dry-run     # 카피 JSON만 출력(렌더 없음)
  py scripts/cardnews.py <입력> --no-imggen   # 이미지 생성 생략(텍스트 패널)

출력: 바탕화면 cardnews/<날짜>-<슬러그>/card-01.png ... + cards.json(재편집용)
"""
from __future__ import annotations

import argparse
import base64
import datetime as _dt
import json
import os
import re
import ssl
import sys
import subprocess
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

ssl._create_default_https_context = ssl._create_unverified_context

CARD_W, CARD_H = 1080, 1350
IMG_MODEL_CANDIDATES = ["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview"]
STYLE_SUFFIX = (
    "Photorealistic photo, warm natural light, modern Korean office or classroom, "
    "clean minimal composition, 16:9 wide. No text, no letters, no logos in the image."
)

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def _load_dotenv() -> None:
    env = REPO_ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


# ---------------------------------------------------------------- 입력 추출

def detect_kind(src: str) -> str:
    low = src.lower()
    if "youtube.com" in low or "youtu.be" in low:
        return "youtube"
    if low.endswith(".pdf"):
        return "pdf"
    return "web"


def extract_youtube(url: str) -> dict:
    from yt_to_post import (extract_video_id, fetch_video_metadata,
                            fetch_transcript, fetch_auto_captions_via_ytdlp)
    vid = extract_video_id(url)
    meta = fetch_video_metadata(url)
    text = ""
    try:
        text = fetch_transcript(vid) or ""
    except Exception:
        pass
    if len(text) < 300:
        try:
            text = fetch_auto_captions_via_ytdlp(url) or ""
        except Exception:
            pass
    if len(text) < 300:
        text = meta.get("description", "") or ""
    return {
        "title": meta.get("title", ""),
        "source_name": meta.get("uploader") or meta.get("channel") or "YouTube",
        "content": text,
        "duration": meta.get("duration") or 0,
    }


def extract_web(src: str) -> dict:
    from web_to_post import fetch_content
    title, site, content = fetch_content(src)
    return {"title": title, "source_name": site or "웹 아티클", "content": content}


def extract_pdf(path: str) -> dict:
    import pdfplumber
    p = Path(path)
    chunks = []
    with pdfplumber.open(str(p)) as pdf:
        for page in pdf.pages[:30]:
            chunks.append(page.extract_text() or "")
    text = "\n".join(chunks)
    title = p.stem
    for line in text.splitlines():
        if len(line.strip()) > 15:
            title = line.strip()[:120]
            break
    return {"title": title, "source_name": "논문", "content": text}


# ---------------------------------------------------------------- 프레임 (YouTube)

def grab_frames(url: str, outdir: Path, n: int) -> "list[tuple[Path, float]]":
    """영상 프레임 n개를 outdir에 저장 (인트로·아웃트로 10% 제외 균등 분포)."""
    try:
        import cv2
        import yt_dlp
    except ImportError:
        print("[WARN] opencv/yt-dlp 미설치 - 프레임 추출 생략")
        return []
    results = []
    print(f"[INFO] 영상 프레임 추출 중 ({n}개 목표)...")
    with tempfile.TemporaryDirectory() as tmp:
        opts = {
            "quiet": True, "no_warnings": True, "nocheckcertificate": True,
            "format": "bestvideo[height<=480][ext=mp4]/worst[ext=mp4]/worst",
            "outtmpl": str(Path(tmp) / "v.%(ext)s"),
            "extractor_args": {"youtube": {"player_client": ["android", "web"]}},
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"[WARN] 영상 다운로드 실패: {e}")
            return []
        files = [f for f in Path(tmp).iterdir() if f.suffix.lower() in (".mp4", ".webm", ".mkv")]
        if not files:
            return []
        cap = cv2.VideoCapture(str(files[0]))
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        if total < 1:
            cap.release()
            return []
        start, end = int(total * 0.1), int(total * 0.9)
        span = max(end - start, 1)
        for i in range(n):
            idx = start + int(span * (i + 0.5) / n)
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ok, frame = cap.read()
            if not ok:
                continue
            ts = idx / fps
            fp = outdir / f"frame-{i+1:02d}.jpg"
            cv2.imwrite(str(fp), frame, [cv2.IMWRITE_JPEG_QUALITY, 88])
            results.append((fp, ts))
        cap.release()
    print(f"[INFO] 프레임 {len(results)}개 확보")
    return results


# ---------------------------------------------------------------- Gemini

def gemini_copy(model_name: str, prompt: str) -> dict:
    import google.generativeai as genai
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json", "temperature": 0.5},
    )
    return json.loads(resp.text)


def gemini_image(prompt: str, out_path: Path) -> bool:
    """Gemini 이미지 생성. 성공 시 out_path 저장 후 True."""
    import requests
    requests.packages.urllib3.disable_warnings()  # type: ignore
    key = os.environ["GEMINI_API_KEY"]
    for model in IMG_MODEL_CANDIDATES:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": "16:9"}},
        }
        try:
            r = requests.post(url, json=body, verify=False, timeout=180)
            if r.status_code != 200:
                continue
            parts = r.json()["candidates"][0]["content"]["parts"]
            for p in parts:
                if "inlineData" in p:
                    out_path.write_bytes(base64.b64decode(p["inlineData"]["data"]))
                    return True
        except Exception as e:
            print(f"  [warn] 이미지 생성 실패({model}): {e}")
    return False


# ---------------------------------------------------------------- 렌더

def fmt_ts(sec: float) -> str:
    m, s = int(sec // 60), int(sec % 60)
    return f"{m:02d}:{s:02d}"


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def prep_logo(render_dir: Path) -> None:
    """logo.jpg → 배경·슬로건 띠 제거한 투명 logo.png ('Dot Connector' 스크립트만).

    크림색 배경은 밝기 기반 알파(잉크=불투명, 배경=투명, 중간 선형 보간)로 제거해
    안티앨리어싱을 보존한다. 하단 "배움, 나눔, 성장…" 슬로건 띠는 잉크의 **연속 런**이
    행 폭 20%를 넘는 행(실측: 띠 269px vs 스크립트 획 최대 96px — 행 잉크 총량 기준은
    굵은 브러시 획을 오탐해 로고 중간 행을 지우는 사고가 있었음)으로 찾고, 띠 내부의
    흰 글자 행은 런이 짧아 개별 탐지가 안 되므로 첫 탐지 행~끝 탐지 행 블록 전체를
    ±2행 여유로 제거한 뒤 남은 잉크의 bbox로 크롭한다. Pillow 부재 등 실패 시 원본
    jpg를 그대로 복사(템플릿이 logo.png를 참조 — Chromium은 내용 스니핑으로 렌더).
    """
    src = REPO_ROOT / "assets" / "logo.jpg"
    dst = render_dir / "logo.png"
    try:
        from PIL import Image
        im = Image.open(src).convert("L")
        w, h = im.size
        corners = [im.getpixel(p) for p in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3))]
        bg = sum(corners) / 4
        lo, hi = 40, max(bg - 12, 80)
        gpx = im.load()
        alpha = [[(255 if g <= lo else 0 if g >= hi else int(255 * (hi - g) / (hi - lo)))
                  for g in (gpx[x, y] for x in range(w))] for y in range(h)]

        def longest_run(row):
            best = cur = 0
            for a in row:
                cur = cur + 1 if a > 60 else 0
                best = max(best, cur)
            return best

        bar_rows = [y for y in range(h) if longest_run(alpha[y]) > w * 0.2]
        drop = (set(range(max(0, bar_rows[0] - 2), min(h, bar_rows[-1] + 3)))
                if bar_rows else set())
        out = Image.new("RGBA", im.size, (0, 0, 0, 0))
        opx = out.load()
        for y in range(h):
            if y in drop:
                continue
            for x, a in enumerate(alpha[y]):
                if a:
                    opx[x, y] = (28, 28, 28, a)
        bbox = out.getchannel("A").getbbox()
        if bbox:
            out = out.crop(bbox)
        out.save(dst)
    except Exception:
        import shutil
        shutil.copy(src, dst)


def render_cards(doc: dict, outdir: Path, images: "list[Path | None]") -> "list[Path]":
    template = (SCRIPT_DIR / "cardnews_template.html").read_text(encoding="utf-8")
    render_dir = outdir / "render"
    render_dir.mkdir(parents=True, exist_ok=True)

    # 로고·폰트를 렌더 디렉토리로 복사 (file:// 상대 참조)
    import shutil
    prep_logo(render_dir)
    fonts_dir = REPO_ROOT / ".fonts"
    font_css = ""
    if (fonts_dir / "Pretendard-Bold.ttf").exists():
        for w, name in ((700, "Bold"), (600, "SemiBold"), (500, "Medium"), (900, "Black")):
            shutil.copy(fonts_dir / f"Pretendard-{name}.ttf", render_dir / f"Pretendard-{name}.ttf")
            font_css += ("@font-face{font-family:'Pretendard';font-weight:%d;"
                         "src:url('Pretendard-%s.ttf');}\n" % (w, name))

    edge = next((p for p in EDGE_PATHS if Path(p).exists()), None)
    if not edge:
        print("[ERROR] Edge 브라우저를 찾을 수 없습니다")
        sys.exit(1)

    cards = doc["cards"]
    total = len(cards)
    pngs = []
    for i, card in enumerate(cards):
        img = images[i] if i < len(images) else None
        if img:
            img_html = f'<div class="photo"><img src="{img.name}" alt=""></div>'
        else:
            quote = esc(card.get("headline_highlight", ""))
            img_html = f'<div class="photo quote-panel"><span>{quote}</span></div>'
        html = (template
                .replace("{{FONT_FACES}}", font_css)
                .replace("{{DATE}}", doc["date"])
                .replace("{{HEADLINE_TOP}}", esc(card.get("headline_top", "")))
                .replace("{{HEADLINE_HL}}", esc(card.get("headline_highlight", "")))
                .replace("{{IMAGE_BLOCK}}", img_html)
                .replace("{{BODY1}}", esc(card.get("body_line1", "")))
                .replace("{{BODY2}}", esc(card.get("body_line2", "")))
                .replace("{{FOOTER_NOTE}}", esc(card.get("footer_note", "")))
                .replace("{{PAGE}}", f"{i+1:02d}/{total:02d}"))
        hp = render_dir / f"card-{i+1:02d}.html"
        hp.write_text(html, encoding="utf-8")
        png = outdir / f"card-{i+1:02d}.png"
        with tempfile.TemporaryDirectory() as prof:
            subprocess.run([
                edge, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                f"--window-size={CARD_W},{CARD_H}", "--force-device-scale-factor=1",
                "--virtual-time-budget=4000", f"--user-data-dir={prof}",
                f"--screenshot={png}", hp.as_uri(),
            ], capture_output=True, timeout=90)
        if png.exists():
            pngs.append(png)
            print(f"  [OK] {png.name}")
        else:
            print(f"  [FAIL] {png.name} 렌더 실패")
    return pngs


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description="유튜브·기사·논문 → 닷커넥터 카드뉴스")
    ap.add_argument("source", help="YouTube URL / 웹 URL / PDF 경로 / 로컬 md")
    ap.add_argument("--cards", type=int, default=8, help="카드 수 (기본 8, 표지·마무리 포함)")
    ap.add_argument("--out", default=None, help="출력 폴더 (기본: 바탕화면 cardnews/)")
    ap.add_argument("--dry-run", action="store_true", help="카피 JSON만 출력")
    ap.add_argument("--no-imggen", action="store_true", help="이미지 생성 생략(텍스트 패널)")
    ap.add_argument("--model", default="gemini-2.5-flash", help="카피 생성 모델")
    args = ap.parse_args()

    _load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        print("[ERROR] GEMINI_API_KEY 없음 (.env)")
        sys.exit(1)

    kind = detect_kind(args.source)
    print(f"[INFO] 입력 유형: {kind}")
    if kind == "youtube":
        data = extract_youtube(args.source)
    elif kind == "pdf":
        data = extract_pdf(args.source)
    else:
        data = extract_web(args.source)
    if len(data["content"]) < 200:
        print("[ERROR] 본문 추출 실패 또는 너무 짧음 - 카드뉴스 생성 중단 (환각 방지)")
        sys.exit(1)
    print(f"[INFO] 제목: {data['title'][:60]}")
    print(f"[INFO] 본문 {len(data['content'])}자 확보")

    today = _dt.date.today()
    tmpl = (SCRIPT_DIR / "cardnews_prompt_template.txt").read_text(encoding="utf-8")
    prompt = (tmpl
              .replace("{N_CARDS}", str(args.cards))
              .replace("{SOURCE_TYPE}", {"youtube": "유튜브 영상", "pdf": "논문", "web": "웹 아티클"}[kind])
              .replace("{TITLE}", data["title"])
              .replace("{SOURCE_NAME}", data["source_name"])
              .replace("{CONTENT}", data["content"][:45000]))
    print(f"[INFO] Gemini 카피 생성 중 ({args.model})...")
    doc = gemini_copy(args.model, prompt)
    doc["date"] = today.strftime("%Y.%m.%d")
    cards = doc.get("cards", [])[:args.cards]
    doc["cards"] = cards
    if not cards:
        print("[ERROR] 카피 생성 실패")
        sys.exit(1)
    for c in cards:  # 레퍼런스 스타일: 헤드라인은 마침표 없이
        for k in ("headline_top", "headline_highlight"):
            c[k] = (c.get(k) or "").rstrip(".")
    print(f"[INFO] 카드 {len(cards)}장 카피 확보")

    if args.dry_run:
        print(json.dumps(doc, ensure_ascii=False, indent=2))
        return

    slug = re.sub(r"[^a-z0-9-]", "", (doc.get("slug") or "cardnews").lower().replace(" ", "-"))[:40] or "cardnews"
    outdir = Path(args.out) if args.out else Path.home() / "Desktop" / "cardnews" / f"{today:%Y%m%d}-{slug}"
    outdir.mkdir(parents=True, exist_ok=True)

    # ---- 카드 이미지 준비
    render_dir = outdir / "render"
    render_dir.mkdir(exist_ok=True)
    images: "list[Path | None]" = [None] * len(cards)
    if kind == "youtube":
        frames = grab_frames(args.source, render_dir, len(cards))
        for i in range(len(cards)):
            if i < len(frames):
                images[i] = frames[i][0]
                note = cards[i].get("footer_note", "").strip()
                cards[i]["footer_note"] = (f"{note} · 화면 {fmt_ts(frames[i][1])}" if note
                                           else f"화면 {fmt_ts(frames[i][1])}")
    if (kind != "youtube" or not any(images)) and not args.no_imggen:
        print("[INFO] Gemini 이미지 생성 중 (카드당 1장)...")
        for i, card in enumerate(cards):
            if images[i]:
                continue
            hint = card.get("image_hint", "") or card.get("headline_highlight", "")
            fp = render_dir / f"gen-{i+1:02d}.png"
            if gemini_image(f"{hint}. {STYLE_SUFFIX}", fp):
                images[i] = fp
                print(f"  [OK] gen-{i+1:02d}.png")
            else:
                print(f"  [warn] 카드 {i+1} 이미지 생성 실패 - 텍스트 패널로 대체")

    # 출처 라벨을 첫/마지막 카드 푸터에 반영
    src_label = doc.get("source_label", "")
    if src_label:
        for idx in (0, len(cards) - 1):
            note = cards[idx].get("footer_note", "").strip()
            if src_label not in note:
                cards[idx]["footer_note"] = f"{src_label}" + (f" · {note}" if note else "")

    print("[INFO] 카드 렌더링 중...")
    pngs = render_cards(doc, outdir, images)
    (outdir / "cards.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n완료! {len(pngs)}장 생성: {outdir}")


if __name__ == "__main__":
    main()
