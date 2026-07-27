#!/usr/bin/env python3
"""유튜브·웹 아티클·논문(PDF) → 닷커넥터 카드뉴스 이미지 생성.

디자인(2026-07-27 리뉴얼 — 다크 시네마틱):
1080x1350(4:5), 짙은 차콜 그라디언트 배경, 상단 흰 스크립트 로고 + 노란 닷네트워크 마크,
헤드라인 2단(흰 주제 라벨 + 노란 핵심 주장, Black Han Sans, 폭·높이 자동 맞춤),
노란 세로 바가 붙은 본문 2~3줄(단정체), 라운드 16:9 이미지,
하단 큰 페이지 번호 + "출처: OOO". 마지막 장은 고정 브랜드 아웃트로 카드.

이미지 우선순위 (원자료 → 생성 → 검색):
1. 원자료 캡처 — YouTube 실제 프레임 / 웹 기사 본문 이미지 / 논문 PDF figure
2. Gemini 이미지 생성 (gemini-2.5-flash-image, 16:9, 다크 시네마틱)
3. DuckDuckGo 이미지 검색 (image_query)
4. 전부 실패 시 노란 인용 패널

카드↔이미지 짝짓기는 Gemini 멀티모달이 후보 이미지를 직접 보고 배정한다(실패 시 순서대로).

사용법:
  py -X utf8 scripts/cardnews.py <YouTube URL|웹 URL|PDF 경로/URL|로컬 md> [--cards 10]
  py -X utf8 scripts/cardnews.py <입력> --dry-run      # 카피 JSON만 출력(렌더 없음)
  py -X utf8 scripts/cardnews.py <입력> --no-imggen    # Gemini 이미지 생성 생략
  py -X utf8 scripts/cardnews.py <입력> --no-outro     # 브랜드 아웃트로 카드 생략
  py -X utf8 scripts/cardnews.py --rerender <출력폴더>  # cards.json 수정 후 재렌더(무과금)

폰트: 헤드라인은 Black Han Sans(OFL). `.fonts/`가 gitignore라 없으면 자동으로 내려받는다.
출력: 바탕화면 cardnews/<날짜>-<슬러그>/card-01.png ... + cards.json(재편집용)
"""
from __future__ import annotations

import argparse
import base64
import datetime as _dt
import hashlib
import json
import os
import re
import ssl
import sys
import subprocess
import tempfile
from pathlib import Path
from urllib.parse import urljoin, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

ssl._create_default_https_context = ssl._create_unverified_context

CARD_W, CARD_H = 1080, 1350
IMG_MODEL_CANDIDATES = ["gemini-2.5-flash-image", "gemini-2.5-flash-image-preview"]

# 레퍼런스 카드의 이미지 톤: 어두운 배경 + 강한 단일 광원 + 얕은 심도
STYLE_SUFFIX = (
    "Cinematic still, dark moody atmosphere, deep shadows, single dramatic light source, "
    "desaturated palette with warm amber accent, shallow depth of field, photorealistic, "
    "16:9 wide composition. No text, no letters, no numbers, no logos, no watermark, no charts."
)

BRAND = {
    "ko": "닷커넥터",
    "handle": "@Dot_Connector",
    "follow": "팔로우하고 다음 인사이트를 받아보세요",
    "link": "linktr.ee/Dot_Connector",
}

FIG_MIN_W, FIG_MIN_H = 300, 200        # 논문 figure 최소 크기
WEB_IMG_MIN_W, WEB_IMG_MIN_H = 620, 330  # 기사 본문 이미지 최소 크기(카드 폭 926px 기준)
MAX_CANDIDATES = 16                    # 멀티모달 배정에 넘길 후보 상한

EDGE_PATHS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/122.0 Safari/537.36")

BAD_IMG_HINTS = ("logo", "icon", "avatar", "sprite", "banner", "profile", "badge",
                 "button", "emoji", "favicon", "pixel", "tracking", "ads", "advert")


def _load_dotenv() -> None:
    env = REPO_ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def _requests():
    import requests
    requests.packages.urllib3.disable_warnings()  # type: ignore
    return requests


# ---------------------------------------------------------------- 입력 추출

def detect_kind(src: str) -> str:
    low = src.lower()
    if "youtube.com" in low or "youtu.be" in low:
        return "youtube"
    if low.endswith(".pdf") or "arxiv.org/pdf/" in low or "arxiv.org/abs/" in low:
        return "pdf"
    return "web"


def ensure_local_pdf(src: str, workdir: Path) -> Path:
    """PDF 경로면 그대로, URL이면 내려받아 로컬 경로를 반환."""
    p = Path(src)
    if p.exists():
        return p
    url = src
    if "arxiv.org/abs/" in url:
        url = url.replace("/abs/", "/pdf/")
    requests = _requests()
    print(f"[INFO] PDF 다운로드: {url}")
    r = requests.get(url, headers={"User-Agent": UA}, verify=False, timeout=90)
    r.raise_for_status()
    name = re.sub(r"[^A-Za-z0-9._-]", "_", Path(urlparse(url).path).name or "paper")
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    dst = workdir / name
    dst.write_bytes(r.content)
    return dst


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
    }


def extract_web(src: str) -> dict:
    from web_to_post import fetch_content
    title, site, content = fetch_content(src)
    return {"title": title, "source_name": site or "웹 아티클", "content": content}


def extract_pdf(path: Path) -> dict:
    import pdfplumber
    chunks = []
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages[:30]:
            chunks.append(page.extract_text() or "")
    text = "\n".join(chunks)
    title = path.stem
    for line in text.splitlines():
        if len(line.strip()) > 15:
            title = line.strip()[:120]
            break
    # 출처 표기는 추출된 값만 쓴다 (arXiv ID 환각 금지).
    # arXiv 스탬프는 세로 회전 텍스트라 추출 순서가 뒤로 밀린다 → 앞 8000자 전체를 훑는다.
    m = re.search(r"arXiv[:\s]\s*(\d{4}\.\d{4,5})", text[:8000], re.I)
    if m:
        source = f"arXiv:{m.group(1)}"
    else:
        # 제목 앞부분을 쓰되 단어 중간에서 자르지 않는다 ("Experiential Versus Instru" 방지)
        head = re.split(r"[:：]", title)[0].strip()
        source = head if len(head) <= 30 else ""
        if not source:
            for w in head.split():
                nxt = f"{source} {w}".strip()
                if len(nxt) > 30:
                    break
                source = nxt
        source = source.rstrip(" ,.-") or "논문"
    return {"title": title, "source_name": source, "content": text}


# ---------------------------------------------------------------- 원자료 이미지 캡처

def _img_ok(path: Path, min_w: int, min_h: int,
            lo: float = 0.75, hi: float = 3.4) -> "tuple[int, int] | None":
    """PIL로 열어 크기·비율을 검사. 통과하면 (w, h)."""
    try:
        from PIL import Image
        with Image.open(path) as im:
            w, h = im.size
    except Exception:
        return None
    if w < min_w or h < min_h:
        return None
    ratio = w / max(h, 1)
    if ratio < lo or ratio > hi:
        return None
    return w, h


def collect_youtube_frames(url: str, outdir: Path, n: int) -> "list[dict]":
    """영상 프레임 n개 추출 (인트로·아웃트로 10% 제외 균등, 암전 프레임 회피)."""
    try:
        import cv2
        import yt_dlp
    except ImportError:
        print("[WARN] opencv/yt-dlp 미설치 - 프레임 추출 생략")
        return []
    out: "list[dict]" = []
    print(f"[INFO] 영상 프레임 추출 중 ({n}개 목표)...")
    with tempfile.TemporaryDirectory() as tmp:
        opts = {
            "quiet": True, "no_warnings": True, "nocheckcertificate": True, "noprogress": True,
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
            base = start + int(span * (i + 0.5) / n)
            for off in (0, int(fps * 2), int(fps * -2), int(fps * 5)):
                idx = min(max(base + off, 0), total - 1)
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ok, frame = cap.read()
                if not ok:
                    continue
                # 암전·단색 전환 프레임만 걸러낸다. 어두운 영상(3B1B식 검은 배경 강의)이
                # 통째로 탈락하지 않도록 문턱은 낮게 잡는다 (실측: mean 22 기준은 6장 중 5장 탈락).
                if float(frame.mean()) < 9 or float(frame.std()) < 7:
                    continue
                fp = outdir / f"frame-{i+1:02d}.jpg"
                cv2.imwrite(str(fp), frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                out.append({"path": fp, "label": f"영상 화면 {fmt_ts(idx / fps)}",
                            "note": f"화면 {fmt_ts(idx / fps)}", "fit": "cover"})
                break
        cap.release()
    print(f"[INFO] 프레임 {len(out)}개 확보")
    return out


def _is_paper(path: Path) -> bool:
    """가장자리가 대부분 흰색이면 사진이 아니라 도표·인포그래픽(종이)으로 본다."""
    try:
        from PIL import Image
        with Image.open(path) as im:
            g = im.convert("L")
            w, h = g.size
            edge = ([g.getpixel((x, 1)) for x in range(0, w, max(w // 40, 1))]
                    + [g.getpixel((x, h - 2)) for x in range(0, w, max(w // 40, 1))]
                    + [g.getpixel((1, y)) for y in range(0, h, max(h // 40, 1))]
                    + [g.getpixel((w - 2, y)) for y in range(0, h, max(h // 40, 1))])
        return sum(1 for v in edge if v > 234) / max(len(edge), 1) > 0.75
    except Exception:
        return False


def _upsize(u: str) -> str:
    """썸네일 URL을 원본·대형 버전으로 바꾼다 (위키미디어 220px, 워드프레스 -800x450 등).

    기사 페이지의 img src는 대개 목록용 축소본이라 그대로 쓰면 카드(926px)에서 뭉개진다.
    """
    out = re.sub(r"/\d{2,4}px-", "/1280px-", u)                       # 위키미디어 thumb
    out = re.sub(r"-\d{3,4}x\d{3,4}(\.(?:jpe?g|png|webp))", r"\1", out)  # 워드프레스 리사이즈
    out = re.sub(r"([?&](?:w|width|maxwidth)=)\d+", r"\g<1>1600", out)
    out = re.sub(r"([?&](?:h|height)=)\d+", r"\g<1>900", out)
    return out


def collect_web_images(url: str, outdir: Path, limit: int = MAX_CANDIDATES) -> "list[dict]":
    """기사 페이지의 대표 이미지(og:image)와 본문 이미지를 내려받는다."""
    if not url.lower().startswith("http"):
        return []
    requests = _requests()
    try:
        from bs4 import BeautifulSoup
        r = requests.get(url, headers={"User-Agent": UA}, verify=False, timeout=40)
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[WARN] 기사 이미지 수집 실패: {e}")
        return []

    urls: "list[str]" = []

    def add(u: str) -> None:
        if not u:
            return
        u = urljoin(url, u.strip().split(" ")[0])
        if not u.lower().startswith("http"):
            return
        low = u.lower()
        if low.endswith((".svg", ".gif")) or any(b in low for b in BAD_IMG_HINTS):
            return
        if u not in urls:
            urls.append(u)

    for sel, attr in (('meta[property="og:image"]', "content"),
                      ('meta[name="twitter:image"]', "content")):
        for tag in soup.select(sel):
            add(tag.get(attr, ""))
    for scope in ("article img", "figure img", ".entry-content img", "main img", "img"):
        for tag in soup.select(scope):
            add(tag.get("src") or tag.get("data-src") or tag.get("data-original") or "")
        if len(urls) >= limit * 3:
            break

    print(f"[INFO] 기사 이미지 후보 {len(urls)}개 발견 - 내려받는 중...")
    got: "list[tuple[int, dict]]" = []
    seen: "set[str]" = set()
    for u in urls[: limit * 3]:
        if len(got) >= limit * 2:
            break
        big = _upsize(u)
        for cand in ([big, u] if big != u else [u]):
            try:
                resp = requests.get(cand, headers={"User-Agent": UA, "Referer": url},
                                    verify=False, timeout=30)
                if resp.status_code != 200 or len(resp.content) < 12000:
                    continue
                digest = hashlib.md5(resp.content).hexdigest()
                if digest in seen:
                    break
                ext = {"image/png": "png", "image/webp": "webp"}.get(
                    resp.headers.get("content-type", "").split(";")[0].strip(), "jpg")
                fp = outdir / f"web-{len(got)+1:02d}.{ext}"
                fp.write_bytes(resp.content)
                size = _img_ok(fp, WEB_IMG_MIN_W, WEB_IMG_MIN_H)
                if not size:
                    fp.unlink(missing_ok=True)
                    continue
                seen.add(digest)
                # 도표·인포그래픽을 16:9로 자르면 내용이 날아간다
                if _is_paper(fp):
                    fit = "contain"                      # 흰 바탕 도표 → 종이 패널
                elif size[0] / size[1] < 1.35:
                    fit = "fit"                          # 세로로 긴 사진 → 어두운 박스
                else:
                    fit = "cover"
                got.append((size[0] * size[1],
                            {"path": fp, "label": f"기사 이미지 ({size[0]}x{size[1]})",
                             "note": "", "fit": fit}))
                break
            except Exception:
                continue
    # 카드 폭이 926px라 작은 썸네일은 흐려진다 → 큰 것부터 남긴다
    got.sort(key=lambda t: t[0], reverse=True)
    out = [d for _, d in got[:limit]]
    print(f"[INFO] 기사 이미지 {len(out)}개 확보")
    return out


def _trim_white(path: Path, pad: int = 14) -> "tuple[int, int, float] | None":
    """흰 여백을 잘라내고 (w, h, 잉크비율)을 돌려준다. 거의 빈 이미지면 None."""
    try:
        from PIL import Image, ImageChops
        im = Image.open(path).convert("RGB")
        diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255)))
        bbox = diff.convert("L").point(lambda v: 255 if v > 18 else 0).getbbox()
        if not bbox:
            return None
        x0, y0, x1, y1 = bbox
        im = im.crop((max(x0 - pad, 0), max(y0 - pad, 0),
                      min(x1 + pad, im.width), min(y1 + pad, im.height)))
        im.save(path)
        gray = im.convert("L").point(lambda v: 255 if v < 235 else 0)
        ink = gray.histogram()[255] / max(im.width * im.height, 1)
        return im.width, im.height, ink
    except Exception:
        return None


def collect_pdf_figures(pdf: Path, outdir: Path, limit: int = MAX_CANDIDATES) -> "list[dict]":
    """논문 PDF의 그림을 캡션 기준으로 오려낸다.

    `page.get_images()`(래스터 임베딩 추출)는 벡터로 그린 도해를 못 잡고 대신 부록의
    프롬프트 스크린샷·로고를 끌어오는 일이 잦다(실측: ToT 논문에서 크로스워드 프롬프트
    텍스트 상자가 1순위로 뽑힘). 그래서 "Figure N" 캡션 블록을 찾아 **그 위 영역을
    페이지째 렌더**한다 — 벡터·래스터 모두 그대로 잡히고 캡션 없는 잡동사니는 안 잡힌다.
    캡션을 하나도 못 찾으면 기존 래스터 추출로 폴백한다.
    """
    try:
        import fitz
    except ImportError:
        print("[WARN] PyMuPDF 미설치 - figure 추출 생략")
        return []
    try:
        doc = fitz.open(str(pdf))
    except Exception as e:
        print(f"[WARN] PDF 열기 실패: {e}")
        return []

    out: "list[dict]" = []
    for pno, page in enumerate(doc, start=1):
        if len(out) >= limit:
            break
        blocks = [b for b in page.get_text("blocks") if (b[4] or "").strip()]
        for b in blocks:
            head = (b[4] or "").strip().replace("\n", " ")
            m = re.match(r"^(?:Figure|Fig\.?|그림)\s*(\d+)", head)
            if not m:
                continue
            cx0, cy0, cx1, cy1 = b[:4]
            width = cx1 - cx0
            x0, x1 = cx0, cx1
            # 캡션 위쪽에서 같은 칼럼에 걸치는 '본문 단락'의 최하단부터 자른다.
            # 그림 안의 짧은 라벨(Input/Output 등)은 경계로 삼지 않는다.
            top = page.rect.y0 + 30
            for o in blocks:
                if o is b or o[3] > cy0 - 2:
                    continue
                if min(o[2], x1) - max(o[0], x0) < width * 0.3:
                    continue
                if len((o[4] or "").strip()) < 90 and (o[2] - o[0]) < width * 0.55:
                    continue
                top = max(top, o[3] + 5)
            # 그림 요소(벡터 드로잉·삽입 이미지)의 실제 범위로 좌우·상단을 넓힌다
            try:
                rects = [d["rect"] for d in page.get_drawings()]
            except Exception:
                rects = []
            for img in page.get_images(full=True):
                try:
                    rects.extend(page.get_image_rects(img[0]))
                except Exception:
                    pass
            band = [r for r in rects
                    if r.y0 >= top - 4 and r.y1 <= cy0 + 2 and r.width > 4 and r.height > 4
                    and min(r.x1, x1 + width) - max(r.x0, x0 - width) > 0]
            if band:
                x0 = min([x0] + [r.x0 for r in band])
                x1 = max([x1] + [r.x1 for r in band])
                top = max(top, min(r.y0 for r in band) - 8)
            x0 = max(page.rect.x0 + 6, x0 - 6)
            x1 = min(page.rect.x1 - 6, x1 + 6)
            if cy0 - top < 60 or x1 - x0 < 90:
                continue
            rect = fitz.Rect(x0, max(top, cy0 - 460), x1, cy0 - 2)
            fp = outdir / f"fig-{len(out)+1:02d}.png"
            try:
                page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=rect, alpha=False).save(str(fp))
            except Exception:
                continue
            info = _trim_white(fp)
            if not info or info[0] < 260 or info[1] < 150 or info[2] < 0.012:
                fp.unlink(missing_ok=True)
                continue
            out.append({"path": fp, "label": f"논문 {pno}쪽 {head[:60]}",
                        "note": f"p.{pno}", "fit": "contain"})
            if len(out) >= limit:
                break

    if not out:   # 캡션 미발견 논문 → 래스터 임베딩 폴백
        seen: "set[str]" = set()
        cands: "list[dict]" = []
        for pno, page in enumerate(doc, start=1):
            for img in page.get_images(full=True):
                try:
                    base = doc.extract_image(img[0])
                except Exception:
                    continue
                if base.get("width", 0) < FIG_MIN_W or base.get("height", 0) < FIG_MIN_H:
                    continue
                digest = hashlib.md5(base.get("image", b"")).hexdigest()
                if digest in seen:
                    continue
                seen.add(digest)
                cands.append({"page": pno, "area": base["width"] * base["height"],
                              "ext": base.get("ext", "png"), "bytes": base["image"]})
        cands.sort(key=lambda c: c["area"], reverse=True)
        for i, c in enumerate(cands[:limit], start=1):
            ext = "jpg" if c["ext"] in ("jpg", "jpeg") else c["ext"]
            fp = outdir / f"fig-{i:02d}.{ext}"
            fp.write_bytes(c["bytes"])
            if not _img_ok(fp, FIG_MIN_W, FIG_MIN_H, 0.4, 4.0):
                fp.unlink(missing_ok=True)
                continue
            out.append({"path": fp, "label": f"논문 {c['page']}쪽 이미지",
                        "note": f"p.{c['page']}", "fit": "contain"})
    doc.close()
    print(f"[INFO] 논문 figure {len(out)}개 확보")
    return out


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


def match_images(model_name: str, cards: "list[dict]", cands: "list[dict]") -> "list[int | None]":
    """후보 이미지를 직접 보고 카드마다 가장 맞는 것을 배정. 실패 시 순서대로."""
    fallback: "list[int | None]" = [i if i < len(cands) else None for i in range(len(cards))]
    if len(cands) < 2:
        return fallback
    try:
        from PIL import Image as PILImage
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        parts: list = [
            "카드뉴스 각 장에 붙일 사진을 고른다. 아래 후보 이미지들을 직접 보고, "
            "카드의 주장과 시각적으로 가장 잘 맞는 후보를 하나씩 배정하라.\n"
            "규칙: 한 후보는 한 카드에만 쓴다. 어울리는 후보가 없으면 null. "
            "글자·자막·로고가 화면을 덮은 이미지, 사람 얼굴만 크게 잡힌 이미지는 피한다.\n"
        ]
        for i, c in enumerate(cands):
            im = PILImage.open(c["path"]).convert("RGB")
            im.thumbnail((512, 512))
            parts.append(f"[후보 {i}] {c['label']}")
            parts.append(im)
        deck = [{"카드": i, "주제": c.get("headline_top", ""),
                 "주장": c.get("headline_highlight", ""),
                 "설명": " ".join(c.get("body", []))} for i, c in enumerate(cards)]
        parts.append("카드 목록:\n" + json.dumps(deck, ensure_ascii=False, indent=1))
        parts.append('출력은 JSON만: {"assign": [카드0의 후보번호 또는 null, 카드1의 ..., ...]} '
                     f"배열 길이는 정확히 {len(cards)}.")
        model = genai.GenerativeModel(model_name)
        resp = model.generate_content(
            parts, generation_config={"response_mime_type": "application/json", "temperature": 0.2})
        raw = json.loads(resp.text).get("assign", [])
        out: "list[int | None]" = []
        used: "set[int]" = set()
        for i in range(len(cards)):
            v = raw[i] if i < len(raw) else None
            if isinstance(v, int) and 0 <= v < len(cands) and v not in used:
                used.add(v)
                out.append(v)
            else:
                out.append(None)
        # 배정 못 받은 카드에 남은 후보를 순서대로 채움
        spare = [i for i in range(len(cands)) if i not in used]
        for i, v in enumerate(out):
            if v is None and spare:
                out[i] = spare.pop(0)
        print(f"[INFO] 이미지 배정: {out}")
        return out
    except Exception as e:
        print(f"[WARN] 이미지 배정 실패 - 순서대로 배정: {e}")
        return fallback


def gemini_image(prompt: str, out_path: Path) -> bool:
    """Gemini 이미지 생성. 성공 시 out_path 저장 후 True."""
    requests = _requests()
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


def search_image(query: str, out_path: Path) -> bool:
    """DuckDuckGo 이미지 검색 폴백 (레이트리밋이 잦아 최후 수단)."""
    if not query:
        return False
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        return False
    requests = _requests()
    try:
        with DDGS(verify=False) as ddgs:
            results = list(ddgs.images(query, max_results=12, type_image="photo", layout="Wide"))
    except Exception as e:
        print(f"  [warn] DDG 검색 실패({query}): {e}")
        return False
    for r in results:
        u = r.get("image", "")
        if not u or r.get("width", 0) < 800:
            continue
        try:
            resp = requests.get(u, headers={"User-Agent": UA}, verify=False, timeout=25)
            if resp.status_code != 200 or len(resp.content) < 20000:
                continue
            out_path.write_bytes(resp.content)
            if _img_ok(out_path, 700, 380):
                return True
            out_path.unlink(missing_ok=True)
        except Exception:
            continue
    return False


# ---------------------------------------------------------------- 렌더

def fmt_ts(sec: float) -> str:
    m, s = int(sec // 60), int(sec % 60)
    return f"{m:02d}:{s:02d}"


def esc(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def prep_logo(render_dir: Path, ink: "tuple[int, int, int]" = (246, 243, 234)) -> None:
    """logo.jpg → 배경·슬로건 띠 제거한 투명 logo.png ('Dot Connector' 스크립트만).

    다크 배경 카드용이라 잉크는 기본 흰색(#f6f3ea)으로 칠한다.
    크림색 배경은 밝기 기반 알파(잉크=불투명, 배경=투명, 중간 선형 보간)로 제거해
    안티앨리어싱을 보존한다. 하단 "배움, 나눔, 성장…" 슬로건 띠는 잉크의 **연속 런**이
    행 폭 20%를 넘는 행(실측: 띠 269px vs 스크립트 획 최대 96px — 행 잉크 총량 기준은
    굵은 브러시 획을 오탐해 로고 중간 행을 지우는 사고가 있었음)으로 찾고, 띠 내부의
    흰 글자 행은 런이 짧아 개별 탐지가 안 되므로 첫 탐지 행~끝 탐지 행 블록 전체를
    ±2행 여유로 제거한 뒤 남은 잉크의 bbox로 크롭한다.
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
                    opx[x, y] = (ink[0], ink[1], ink[2], a)
        bbox = out.getchannel("A").getbbox()
        if bbox:
            out = out.crop(bbox)
        out.save(dst)
    except Exception:
        import shutil
        shutil.copy(src, dst)


BHS_URL = ("https://raw.githubusercontent.com/google/fonts/main/ofl/blackhansans/"
           "BlackHanSans-Regular.ttf")


def ensure_headline_font() -> Path:
    """헤드라인 폰트(Black Han Sans, OFL)를 확보한다. `.fonts/`는 gitignore라 클론마다 없다."""
    fp = REPO_ROOT / ".fonts" / "BlackHanSans-Regular.ttf"
    if fp.exists():
        return fp
    print("[INFO] 헤드라인 폰트(Black Han Sans) 내려받는 중...")
    try:
        requests = _requests()
        r = requests.get(BHS_URL, verify=False, timeout=90)
        r.raise_for_status()
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_bytes(r.content)
    except Exception as e:
        print(f"[WARN] 폰트 다운로드 실패({e}) - 헤드라인이 Pretendard로 대체됨")
    return fp


def _font_css(render_dir: Path) -> str:
    """Pretendard 4종 + Black Han Sans(헤드라인)를 렌더 디렉토리로 복사."""
    import shutil
    fonts = REPO_ROOT / ".fonts"
    ensure_headline_font()
    css = ""
    for weight, name in ((900, "Black"), (700, "Bold"), (600, "SemiBold"), (500, "Medium")):
        f = fonts / f"Pretendard-{name}.ttf"
        if f.exists():
            shutil.copy(f, render_dir / f.name)
            css += ("@font-face{font-family:'Pretendard';font-weight:%d;src:url('%s');}\n"
                    % (weight, f.name))
    bhs = fonts / "BlackHanSans-Regular.ttf"
    if bhs.exists():
        shutil.copy(bhs, render_dir / bhs.name)
        css += "@font-face{font-family:'BlackHanSans';src:url('%s');}\n" % bhs.name
    return css


def _shot(edge: str, html: Path, png: Path) -> bool:
    with tempfile.TemporaryDirectory() as prof:
        subprocess.run([
            edge, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--window-size={CARD_W},{CARD_H}", "--force-device-scale-factor=1",
            "--virtual-time-budget=5000", f"--user-data-dir={prof}",
            f"--screenshot={png}", html.as_uri(),
        ], capture_output=True, timeout=120)
    return png.exists()


def render_cards(doc: dict, outdir: Path, images: "list[dict | None]") -> "list[Path]":
    """카드 PNG를 렌더한다. images[i] = {"path":.., "fit":.., "note":..} 또는 None."""
    template = (SCRIPT_DIR / "cardnews_template.html").read_text(encoding="utf-8")
    outro_tpl = (SCRIPT_DIR / "cardnews_outro.html").read_text(encoding="utf-8")
    render_dir = outdir / "render"
    render_dir.mkdir(parents=True, exist_ok=True)
    prep_logo(render_dir)
    font_css = _font_css(render_dir)

    edge = next((p for p in EDGE_PATHS if Path(p).exists()), None)
    if not edge:
        print("[ERROR] Edge 브라우저를 찾을 수 없습니다")
        sys.exit(1)

    cards = doc["cards"]
    total = len(cards) + (1 if doc.get("outro", True) else 0)
    src_label = doc.get("source_label", "")
    pngs: "list[Path]" = []

    for i, card in enumerate(cards):
        img = images[i] if i < len(images) else None
        if img:
            rel = Path(img["path"]).name
            if Path(img["path"]).resolve().parent != render_dir.resolve():
                import shutil
                shutil.copy(img["path"], render_dir / rel)
            fit = img.get("fit", "cover")
            cls = f"photo {fit}" if fit in ("contain", "fit") else "photo"
            img_html = f'<div class="{cls}"><img src="{rel}" alt=""></div>'
        else:
            img_html = ('<div class="photo quote-panel"><span>'
                        f'{esc(card.get("headline_highlight", ""))}</span></div>')
        note = (img or {}).get("note", "")
        source = f"출처: {src_label}" if src_label else ""
        if note:
            source = f"{source} · {note}" if source else note
        body = "<br>".join(esc(l) for l in card.get("body", []) if l)
        html = (template
                .replace("{{FONT_FACES}}", font_css)
                .replace("{{HEADLINE_TOP}}", esc(card.get("headline_top", "")))
                .replace("{{HEADLINE_HL}}", esc(card.get("headline_highlight", "")))
                .replace("{{BODY}}", body)
                .replace("{{IMAGE_BLOCK}}", img_html)
                .replace("{{PAGE}}", f"{i+1:02d}")
                .replace("{{TOTAL}}", f"{total:02d}")
                .replace("{{SOURCE}}", esc(source)))
        hp = render_dir / f"card-{i+1:02d}.html"
        hp.write_text(html, encoding="utf-8")
        png = outdir / f"card-{i+1:02d}.png"
        if _shot(edge, hp, png):
            pngs.append(png)
            print(f"  [OK] {png.name}")
        else:
            print(f"  [FAIL] {png.name} 렌더 실패")

    if doc.get("outro", True):
        html = (outro_tpl
                .replace("{{FONT_FACES}}", font_css)
                .replace("{{BRAND_KO}}", BRAND["ko"])
                .replace("{{HANDLE}}", BRAND["handle"])
                .replace("{{FOLLOW_TEXT}}", BRAND["follow"])
                .replace("{{LINK}}", BRAND["link"]))
        hp = render_dir / f"card-{total:02d}.html"
        hp.write_text(html, encoding="utf-8")
        png = outdir / f"card-{total:02d}.png"
        if _shot(edge, hp, png):
            pngs.append(png)
            print(f"  [OK] {png.name} (아웃트로)")
    return pngs


# ---------------------------------------------------------------- main

def rerender(outdir: Path) -> None:
    """cards.json을 고친 뒤 Gemini 재호출 없이 카드만 다시 그린다."""
    doc = json.loads((outdir / "cards.json").read_text(encoding="utf-8"))
    images: "list[dict | None]" = []
    for entry in doc.get("images") or []:
        if isinstance(entry, dict) and Path(entry.get("path", "")).exists():
            images.append({"path": Path(entry["path"]), "fit": entry.get("fit", "cover"),
                           "note": entry.get("note", "")})
        elif isinstance(entry, str) and Path(entry).exists():
            images.append({"path": Path(entry), "fit": "cover", "note": ""})
        else:
            images.append(None)
    pngs = render_cards(doc, outdir, images)
    print(f"\n재렌더 완료! {len(pngs)}장: {outdir}")


def main() -> None:
    ap = argparse.ArgumentParser(description="유튜브·기사·논문 → 닷커넥터 카드뉴스")
    ap.add_argument("source", nargs="?", help="YouTube URL / 웹 URL / PDF 경로·URL / 로컬 md")
    ap.add_argument("--rerender", metavar="DIR",
                    help="기존 출력 폴더의 cards.json으로 카드만 다시 렌더 (Gemini 재호출 없음)")
    ap.add_argument("--cards", type=int, default=10,
                    help="총 카드 수 (기본 10 — 아웃트로 카드 포함)")
    ap.add_argument("--out", default=None, help="출력 폴더 (기본: 바탕화면 cardnews/)")
    ap.add_argument("--dry-run", action="store_true", help="카피 JSON만 출력")
    ap.add_argument("--no-imggen", action="store_true", help="Gemini 이미지 생성 생략")
    ap.add_argument("--no-search", action="store_true", help="DDG 이미지 검색 폴백 생략")
    ap.add_argument("--no-outro", action="store_true", help="브랜드 아웃트로 카드 생략")
    ap.add_argument("--model", default="gemini-2.5-flash", help="카피 생성 모델")
    args = ap.parse_args()

    if args.rerender:
        rerender(Path(args.rerender))
        return
    if not args.source:
        ap.error("입력(URL/PDF) 또는 --rerender 중 하나는 있어야 합니다")

    _load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        print("[ERROR] GEMINI_API_KEY 없음 (.env)")
        sys.exit(1)

    today = _dt.date.today()
    n_content = max(args.cards - (0 if args.no_outro else 1), 1)

    kind = detect_kind(args.source)
    print(f"[INFO] 입력 유형: {kind}")
    tmpdir = Path(tempfile.mkdtemp(prefix="cardnews-"))
    pdf_path = None
    if kind == "youtube":
        data = extract_youtube(args.source)
    elif kind == "pdf":
        pdf_path = ensure_local_pdf(args.source, tmpdir)
        data = extract_pdf(pdf_path)
        # 입력이 arXiv URL이면 ID가 확실하므로 출처 라벨로 쓴다 (PDF 스탬프 추출 실패 대비)
        m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", args.source, re.I)
        if m:
            data["source_name"] = f"arXiv:{m.group(1)}"
    else:
        data = extract_web(args.source)
    if len(data["content"]) < 200:
        print("[ERROR] 본문 추출 실패 또는 너무 짧음 - 카드뉴스 생성 중단 (환각 방지)")
        sys.exit(1)
    print(f"[INFO] 제목: {data['title'][:60]}")
    print(f"[INFO] 본문 {len(data['content'])}자 확보")

    tmpl = (SCRIPT_DIR / "cardnews_prompt_template.txt").read_text(encoding="utf-8")
    prompt = (tmpl
              .replace("{N_CARDS}", str(n_content))
              .replace("{SOURCE_TYPE}", {"youtube": "유튜브 영상", "pdf": "논문",
                                         "web": "웹 아티클"}[kind])
              .replace("{TITLE}", data["title"])
              .replace("{SOURCE_NAME}", data["source_name"])
              .replace("{CONTENT}", data["content"][:45000]))
    print(f"[INFO] Gemini 카피 생성 중 ({args.model})...")
    doc = gemini_copy(args.model, prompt)
    cards = doc.get("cards", [])[:n_content]
    doc["cards"] = cards
    doc["date"] = today.strftime("%Y.%m.%d")
    doc["outro"] = not args.no_outro
    label = (doc.get("source_label") or data["source_name"]).strip()
    doc["source_label"] = re.sub(r"^\s*출처\s*[:：]\s*", "", label)  # 템플릿이 "출처:"를 붙인다
    if not cards:
        print("[ERROR] 카피 생성 실패")
        sys.exit(1)
    quotes = str.maketrans("", "", "\"'“”‘’")   # 카피에 따옴표 금지 (프롬프트 규칙 강제)
    for c in cards:
        for k in ("headline_top", "headline_highlight"):
            c[k] = (c.get(k) or "").translate(quotes).rstrip(". ")
        if isinstance(c.get("body"), str):
            c["body"] = [c["body"]]
        c["body"] = [str(x).translate(quotes)
                     for x in (c.get("body") or []) if str(x).strip()][:3]
    print(f"[INFO] 카드 {len(cards)}장 카피 확보")

    if args.dry_run:
        print(json.dumps(doc, ensure_ascii=False, indent=2))
        return

    slug = re.sub(r"[^a-z0-9-]", "",
                  (doc.get("slug") or "cardnews").lower().replace(" ", "-"))[:40] or "cardnews"
    outdir = Path(args.out) if args.out else Path.home() / "Desktop" / "cardnews" / f"{today:%Y%m%d}-{slug}"
    outdir.mkdir(parents=True, exist_ok=True)
    render_dir = outdir / "render"
    render_dir.mkdir(exist_ok=True)

    # ---- 1순위: 원자료에서 이미지 캡처
    if kind == "youtube":
        cands = collect_youtube_frames(args.source, render_dir, len(cards))
    elif kind == "pdf":
        cands = collect_pdf_figures(pdf_path, render_dir)
    else:
        cands = collect_web_images(args.source, render_dir)

    images: "list[dict | None]" = [None] * len(cards)
    if cands:
        assign = match_images(args.model, cards, cands)
        for i, ci in enumerate(assign):
            if ci is not None:
                images[i] = cands[ci]

    # ---- 2·3순위: Gemini 생성 → 웹 검색
    missing = [i for i, im in enumerate(images) if im is None]
    if missing and not args.no_imggen:
        print(f"[INFO] 이미지 없는 카드 {len(missing)}장 - Gemini 생성 시도...")
        for i in missing:
            card = cards[i]
            hint = card.get("image_hint") or card.get("headline_highlight", "")
            fp = render_dir / f"gen-{i+1:02d}.png"
            if gemini_image(f"{hint}. {STYLE_SUFFIX}", fp):
                images[i] = {"path": fp, "fit": "cover", "note": ""}
                print(f"  [OK] gen-{i+1:02d}.png")
    missing = [i for i, im in enumerate(images) if im is None]
    if missing and not args.no_search:
        print(f"[INFO] 남은 {len(missing)}장 - 웹 이미지 검색 폴백...")
        for i in missing:
            q = cards[i].get("image_query") or cards[i].get("headline_highlight", "")
            fp = render_dir / f"search-{i+1:02d}.jpg"
            if search_image(q, fp):
                images[i] = {"path": fp, "fit": "cover", "note": ""}
                print(f"  [OK] search-{i+1:02d}.jpg ({q})")
            else:
                print(f"  [warn] 카드 {i+1} 이미지 확보 실패 - 인용 패널로 대체")

    # 재렌더(--rerender)를 위해 이미지 경로·표시방식·푸터 주석까지 함께 저장
    doc["images"] = [({"path": str(im["path"]), "fit": im.get("fit", "cover"),
                       "note": im.get("note", "")} if im else None) for im in images]
    print("[INFO] 카드 렌더링 중...")
    pngs = render_cards(doc, outdir, images)
    (outdir / "cards.json").write_text(json.dumps(doc, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
    print(f"\n완료! {len(pngs)}장 생성: {outdir}")


if __name__ == "__main__":
    main()
