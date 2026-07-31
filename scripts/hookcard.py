#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""후킹 이미지 카드 1장 생성 — 블로그 글을 읽고 싶게 만드는 소셜용 티저.

  py -X utf8 scripts/hookcard.py _posts/2026-07-27-platformized-classroom-hyflex.md
  py -X utf8 scripts/hookcard.py <URL|PDF>
  py -X utf8 scripts/hookcard.py <입력> --dry-run          # 카피 JSON만
  py -X utf8 scripts/hookcard.py --rerender <출력폴더>      # card.json 수정 후 재렌더(무과금)
  py -X utf8 scripts/hookcard.py <입력> --image <파일>      # 이미지 직접 지정

설계 근거는 레퍼런스 이미지 실측(1080x1350):
  사진 (32,140)-(1048,1222) / 좌우 패딩 96 / 헤드라인 2행(흰색+금색) 피치 147px
  하단 y1229~1281 에 좌 로고 · 우 출처. 금색은 #F0B24B.

카드뉴스(cardnews.py)와 캔버스·폰트·로고·이미지 수급·렌더 파이프라인을 공유한다.
차이는 "여러 장 요약"이 아니라 "한 장으로 클릭을 유도"라는 목적이다.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

import cardnews as cn  # noqa: E402  (캔버스·폰트·로고·이미지·렌더 공용)

CARD_W, CARD_H = cn.CARD_W, cn.CARD_H
ACCENT = "#f0b24b"

DEFAULT_OUT = Path.home() / "Desktop" / "hookcard"

# cardnews.STYLE_SUFFIX 는 "16:9 wide composition"을 명시해 가로 슬롯을 전제한다.
# 후킹 카드는 세로 슬롯이고 아래 3분의 1을 헤드라인이 덮으므로, 피사체를 위쪽에 두라고
# 프롬프트 단계에서 못 박는다(사후 크롭보다 이쪽이 화질 손실이 없다).
STYLE_SUFFIX = (
    "Cinematic still, dark moody atmosphere, deep shadows, single dramatic light source, "
    "desaturated palette with warm amber accent, shallow depth of field, photorealistic, "
    "square composition. Place the main subject in the UPPER HALF of the frame; "
    "leave the bottom third dark, empty and free of any important detail. "
    "No text, no letters, no numbers, no logos, no watermark, no charts."
)

# 후킹 카드는 의문형이 정답이라 cardnews의 "~다로 끝나야 함" 규칙은 적용하지 않는다.
# 존칭체·훈계조·AI 티 표현만 코드로 잡는다.
COPY_RULES = cn.COPY_RULES


# ---------------------------------------------------------------- 입력 추출

def extract_post(path: Path) -> dict:
    """_posts/*.md 에서 제목·본문·출처를 뽑는다."""
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    fm, body = (m.group(1), m.group(2)) if m else ("", raw)

    def fm_get(key: str) -> str:
        mm = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
        return mm.group(1).strip().strip('"').strip("'") if mm else ""

    title = fm_get("title")
    tags = fm_get("tags")

    # 출처 섹션(있으면) → 표기 힌트
    src_hint = ""
    ms = re.search(r"^##\s*출처\s*$(.*?)(?=^##\s|\Z)", body, re.S | re.M)
    if ms:
        src_hint = " ".join(ms.group(1).split())[:400]

    # 본문에서 마크업·figure 걷어내기
    text = re.sub(r"<figure>.*?</figure>", " ", body, flags=re.S)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"[*_`>|#-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return {
        "title": title,
        "source_name": src_hint or title,
        "content": text,
        "tags": tags,
    }


def load_source(src: str, workdir: Path) -> dict:
    p = Path(src)
    if p.suffix.lower() == ".md" and p.exists():
        print(f"[INFO] 블로그 포스트 읽는 중: {p.name}")
        return extract_post(p)

    kind = cn.detect_kind(src)
    if kind == "youtube":
        print("[INFO] YouTube 자막 추출 중...")
        return cn.extract_youtube(src)
    if kind == "pdf":
        pdf = cn.ensure_local_pdf(src, workdir)
        print(f"[INFO] PDF 텍스트 추출 중: {pdf.name}")
        return cn.extract_pdf(pdf)
    print("[INFO] 웹 본문 추출 중...")
    return cn.extract_web(src)


# ---------------------------------------------------------------- 카피

def build_prompt(doc: dict) -> str:
    tpl = (SCRIPT_DIR / "hookcard_prompt_template.txt").read_text(encoding="utf-8")
    return (tpl
            .replace("{TITLE}", doc.get("title", "")[:200])
            .replace("{SOURCE_HINT}", doc.get("source_name", "")[:400])
            .replace("{CONTENT}", doc.get("content", "")[:14000]))


def validate_copy(card: dict) -> "list[str]":
    text = " ".join([card.get("eyebrow", ""), card.get("line1", ""), card.get("line2", "")])
    issues = [msg for pat, msg in COPY_RULES if re.search(pat, text)]
    for key in ("line1", "line2"):
        v = (card.get(key) or "").strip()
        if not v:
            issues.append(f"{key}가 비어 있음")
        elif len(v) > 11:
            issues.append(f"{key}가 {len(v)}자 — 8자 내외로 줄일 것 (길면 글자가 작아짐)")
    if ":" in (card.get("line1", "") + card.get("line2", "")):
        issues.append("헤드라인에 콜론 사용 — 콜론 없이 다시 쓸 것")
    # 단정체 종결에 물음표를 붙이면 비문이 된다(실측 반복: '모른다?', '실천이다?').
    # 의문형은 권장하지만 어미까지 의문형이어야 한다.
    tail = (card.get("line2") or "").strip()
    if tail.endswith("?") and re.search(r"(다|음|임|함)\?$", tail):
        issues.append(f"'{tail}' — 단정체 어미에 물음표를 붙여 비문이 됨. "
                      "의문형으로 쓰려면 '~인가?/~일까?/~하는가?'로 어미까지 바꿀 것")
    # 출처 제목을 어중간하게 잘라 조각을 남기는 실패가 잦다(말줄임표·중간 절단).
    src = (card.get("source") or "")
    if "..." in src or "…" in src:
        issues.append("출처 제목이 말줄임표로 끊김 — 짧고 완결된 제목으로 다시 쓸 것")
    return issues


def repair_copy(model: str, card: dict, issues: "list[str]", doc: dict) -> dict:
    prompt = (
        "아래 후킹 카드 카피가 규칙을 어겼다. 지적된 부분만 고쳐 같은 JSON 스키마로 다시 출력한다.\n\n"
        f"[현재 카피]\n{json.dumps(card, ensure_ascii=False, indent=2)}\n\n"
        f"[위반]\n- " + "\n- ".join(issues) + "\n\n"
        f"[원문 제목]\n{doc.get('title','')}\n\n"
        "line1+line2는 이어 읽어 한 문장이 되고, 각 행 8자 내외, 단정체(의문형 허용), "
        "존칭체·훈계조·콜론 금지. JSON 객체 하나만 출력한다."
    )
    try:
        return cn.gemini_copy(model, prompt)
    except Exception as e:
        print(f"[WARN] 카피 재작성 실패({e}) — 원본 유지")
        return card


def make_copy(model: str, doc: dict) -> dict:
    print(f"[INFO] 카피 생성 중 (모델: {model})...")
    card = cn.gemini_copy(model, build_prompt(doc))
    for attempt in range(2):
        issues = validate_copy(card)
        if not issues:
            break
        print(f"[WARN] 카피 규칙 위반 {len(issues)}건 — 재작성 {attempt + 1}/2")
        for i in issues:
            print(f"       - {i}")
        card = repair_copy(model, card, issues, doc)
    left = validate_copy(card)
    if left:
        print("[WARN] 남은 위반(수동 확인 필요):")
        for i in left:
            print(f"       - {i}")
    return card


# ---------------------------------------------------------------- 이미지

def pick_image(card: dict, doc: dict, src: str, outdir: Path,
               manual: "str | None", no_image: bool) -> "dict | None":
    """원자료 캡처 → 생성 → 검색 순으로 사진 1장을 확보한다."""
    render_dir = outdir / "render"
    render_dir.mkdir(parents=True, exist_ok=True)

    if no_image:
        return None

    if manual:
        mp = Path(manual)
        if not mp.exists():
            print(f"[WARN] 지정한 이미지가 없습니다: {mp}")
        else:
            dst = render_dir / f"hero{mp.suffix.lower()}"
            shutil.copy(mp, dst)
            _recompose(dst)
            return {"path": str(dst), "fit": _fit_for(dst), "note": "수동 지정"}

    # 1) 원자료에서 직접 캡처.
    #    단 후킹 카드는 "설명"이 아니라 "시선 붙잡기"가 목적이라 도표·논문 figure는 쓰지 않는다.
    #    흰 바탕 도표를 히어로로 깔면 다크 디자인과 충돌하고 도표 속 글자가 헤드라인과 경쟁한다.
    cands: "list[dict]" = []
    try:
        p = Path(src)
        if p.suffix.lower() == ".md" and p.exists():
            cands = _post_images(p, render_dir)
        elif cn.detect_kind(src) == "youtube":
            cands = cn.collect_youtube_frames(src, render_dir, 4)   # 실제 영상 프레임 = 사진
        elif cn.detect_kind(src) == "pdf":
            cands = []          # 논문 figure는 전부 도표라 후킹용으로 부적합
        else:
            cands = cn.collect_web_images(src, render_dir, 4)
    except Exception as e:
        print(f"[WARN] 원자료 이미지 수집 실패: {e}")

    cands = [c for c in cands if _photo_like(Path(c["path"]))]

    if cands:
        best = cands[0]
        bp = Path(best["path"])
        print(f"[INFO] 원자료 이미지 사용: {bp.name}")
        _recompose(bp)
        return {"path": str(bp), "fit": _fit_for(bp), "note": best.get("label", "원자료")}

    # 2) 생성 — 사진 슬롯이 세로(0.939)라 1:1로 뽑는다.
    #    카드뉴스 기본값 16:9를 그대로 쓰면 좌우가 크게 잘리고 피사체가 아래로 몰려
    #    헤드라인과 겹친다(실측). 1:1이 이 박스에 가장 가깝다.
    hint = card.get("image_hint") or card.get("image_query") or doc.get("title", "")
    gen = render_dir / "hero-gen.png"
    print("[INFO] 이미지 생성 시도 중 (1:1)...")
    try:
        if cn.gemini_image(f"{hint}. {STYLE_SUFFIX}", gen, aspect="1:1") and gen.exists():
            _trim_letterbox(gen)
            _recompose(gen)
            return {"path": str(gen), "fit": _fit_for(gen), "note": "생성"}
    except Exception as e:
        print(f"[WARN] 이미지 생성 실패: {e}")

    # 3) 검색
    q = card.get("image_query") or doc.get("title", "")
    found = render_dir / "hero-search.jpg"
    print(f"[INFO] 이미지 검색 시도: {q}")
    try:
        if cn.search_image(q, found) and found.exists():
            _recompose(found)
            return {"path": str(found), "fit": _fit_for(found), "note": "검색"}
    except Exception as e:
        print(f"[WARN] 이미지 검색 실패: {e}")

    print("[WARN] 이미지를 구하지 못했습니다 — 그라디언트 배경으로 렌더합니다")
    return None


def _post_images(post: Path, render_dir: Path) -> "list[dict]":
    """포스트 본문이 참조하는 /assets 이미지를 후보로 삼는다."""
    body = post.read_text(encoding="utf-8")
    out = []
    for rel in re.findall(r'<img src="(/assets/[^"]+)"', body):
        f = REPO_ROOT / rel.lstrip("/")
        if not f.exists():
            continue
        if not cn._img_ok(f, 500, 300, lo=0.5, hi=3.4):
            continue
        dst = render_dir / f.name
        shutil.copy(f, dst)
        out.append({"path": str(dst), "note": f"포스트 이미지 {f.name}"})
    return out


def _trim_letterbox(p: Path, thr: int = 14) -> None:
    """생성 이미지 가장자리의 균일한 검은 레터박스 띠를 잘라낸다.

    gemini 이미지 모델이 16:9를 맞추느라 위아래에 순수 검정 띠를 넣어 보내는 경우가 있다
    (실측: 1344x768 결과 상단 50px가 (0,0,0)). cover로 깔면 그 띠가 사진 상단의
    가로 이음매로 그대로 보인다.
    """
    try:
        from PIL import Image
        im = Image.open(p).convert("RGB")
        w, h = im.size
        px = im.load()

        def dark_row(y):
            return all(sum(px[x, y]) / 3 <= thr for x in range(0, w, max(1, w // 60)))

        def dark_col(x):
            return all(sum(px[x, y]) / 3 <= thr for y in range(0, h, max(1, h // 60)))

        # 비율 보정용 띠는 대개 얇다. 한도를 두지 않으면 다크 시네마틱 이미지의
        # 의도된 어두운 여백(프롬프트로 '하단 3분의 1을 비우라'고 요청한 영역)까지
        # 깎아내 해상도만 잃는다(실측: 1024 -> 783).
        capv, caph = int(h * 0.12), int(w * 0.12)
        top = 0
        while top < capv and dark_row(top):
            top += 1
        bot = h - 1
        while bot > h - 1 - capv and dark_row(bot):
            bot -= 1
        left = 0
        while left < caph and dark_col(left):
            left += 1
        right = w - 1
        while right > w - 1 - caph and dark_col(right):
            right -= 1

        if (top, left) == (0, 0) and (bot, right) == (h - 1, w - 1):
            return
        im.crop((left, top, right + 1, bot + 1)).save(p)
        print(f"[INFO] 생성 이미지 레터박스 제거: {w}x{h} -> {right - left + 1}x{bot - top + 1}")
    except Exception:
        pass


BOX_W, BOX_H = 1016, 1082
BOX_RATIO = BOX_W / BOX_H          # 0.939 — 사진 박스는 세로형이다
TEXT_TOP_FRAC = 0.66               # 이 아래는 아이브로우·헤드라인이 덮는 구역
MAX_UPSCALE = 1.35                 # 박스로 늘릴 때 허용할 최대 확대율 — 화질 보호


def _subject_band(im) -> "tuple[int, int, int]":
    """밝기 질량으로 피사체의 세로 구간(top, bottom)과 가로 중심을 추정한다.

    가장 밝은 행에서 **연결된 구간만** 넓힌다. 단순히 '문턱을 넘는 모든 행'으로 잡으면
    화면 맨 아래 바닥 반사·조명 띠까지 피사체로 묶여 구간이 100%까지 늘어난다(실측).
    """
    W, H = im.size
    px = im.load()

    def lum(c):
        return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

    step = max(1, W // 160)
    xs = range(0, W, step)
    # '밝기 합'이 아니라 '아주 밝은 픽셀 수'로 센다. 합계를 쓰면 어둡지만 폭이 넓은
    # 바닥 반사 띠가 작고 강한 실제 피사체(광원·얼굴)를 이긴다(실측: 오브 대신 바닥이 피크).
    samples = sorted(lum(px[x, y]) for y in range(0, H, max(1, H // 120)) for x in xs)
    hi = samples[int(len(samples) * 0.96)] if samples else 200
    hi = max(hi, 110)
    rows = [sum(1 for x in xs if lum(px[x, y]) >= hi) for y in range(H)]
    # 가벼운 평활화 — 한 줄짜리 잡음으로 구간이 끊기지 않게
    k = max(1, H // 100)
    sm = [sum(rows[max(0, y - k):min(H, y + k + 1)]) / len(rows[max(0, y - k):min(H, y + k + 1)])
          for y in range(H)]
    peak_y = max(range(H), key=lambda y: sm[y])
    thr = sm[peak_y] * 0.38

    top = peak_y
    while top > 0 and sm[top - 1] > thr:
        top -= 1
    bot = peak_y
    while bot < H - 1 and sm[bot + 1] > thr:
        bot += 1

    cols = [sum(max(0.0, lum(px[x, y]) - 45) for y in range(top, bot + 1, step)) for x in range(W)]
    tot = sum(cols) or 1.0
    cx = int(sum(x * v for x, v in enumerate(cols)) / tot)
    return top, bot, cx


def _recompose(p: Path) -> None:
    """피사체가 헤드라인 구역으로 내려앉지 않도록 박스 비율로 다시 잘라낸다.

    cover는 이미지를 박스에 꽉 채우므로, 가로로 긴 원본은 **세로 여백이 0**이 되어
    `object-position`으로는 위아래로 1px도 못 움직인다(실측). 그래서 CSS가 아니라
    파일 자체를 박스 비율(0.939)로 다시 잘라 피사체를 위로 올린다.
    확대 한도(MIN_KEEP)를 두어 화질이 뭉개지는 것보다는 덜 올라가는 쪽을 택한다.
    """
    try:
        from PIL import Image
        im = Image.open(p).convert("RGB")
        W, H = im.size
        top, bot, cx = _subject_band(im)

        # 화질 하한: 박스 높이를 MAX_UPSCALE 이내로 채울 수 있는 최소 crop 높이.
        # 원본이 이미 그보다 작으면(=이미 확대해 쓰는 중이면) 세로로는 더 자르지 않는다.
        floor_h = int(BOX_H / MAX_UPSCALE)
        if H <= floor_h:
            print(f"[INFO] 재배치 생략 — 원본 높이 {H}px, 이미 확대 사용 중(하한 {floor_h}px)")
            return

        # 피사체 아래가 텍스트 구역을 침범하지 않는 crop 높이를 찾는다.
        below = H - bot                      # 피사체 아래로 남은 여백
        want = int(below / max(1e-6, (1 - TEXT_TOP_FRAC)))   # 이 높이면 bot이 딱 TEXT_TOP_FRAC
        hc = max(floor_h, min(H, want))
        wc = int(round(hc * BOX_RATIO))
        if wc > W:                            # 원본이 이미 세로로 길면 폭이 기준
            wc = W
            hc = min(H, int(round(wc / BOX_RATIO)))

        y0 = int(round(bot - hc * TEXT_TOP_FRAC))
        y0 = max(0, min(H - hc, y0))
        x0 = max(0, min(W - wc, cx - wc // 2))

        if (wc, hc) == (W, H):
            return

        # 잘라도 별로 안 올라간다면 그냥 둔다 — 확대만 하고 개선이 없으면 화질만 손해다.
        oldbot = bot / H
        newbot = (bot - y0) / hc
        if oldbot - newbot < 0.05:
            print(f"[INFO] 재배치 생략 — 개선 폭이 작음 (하단 {oldbot:.0%}, 확대만 손해)")
            return

        im.crop((x0, y0, x0 + wc, y0 + hc)).save(p)
        print(f"[INFO] 피사체 재배치: {W}x{H} -> {wc}x{hc} "
              f"(피사체 하단 {oldbot:.0%} -> {newbot:.0%})")
    except Exception as e:
        print(f"[WARN] 재배치 건너뜀: {e}")


def _photo_like(p: Path) -> bool:
    """히어로로 쓸 만한 '사진'인지. 흰 바탕 도표·스크린샷류는 탈락시킨다."""
    if cn._is_paper(p):
        return False
    try:
        from PIL import Image, ImageStat
        with Image.open(p) as im:
            im = im.convert("RGB")
            st = ImageStat.Stat(im)
            # 채도가 거의 없고 아주 밝으면 문서·도표일 가능성이 높다
            mean = sum(st.mean) / 3
            spread = max(st.mean) - min(st.mean)
            if mean > 205 and spread < 12:
                return False
    except Exception:
        pass
    return True


def _fit_for(p: Path) -> str:
    """항상 cover(빈 문자열)로 채운다.

    후킹 카드의 사진은 '전부 보여줄 자료'가 아니라 헤드라인을 받치는 **배경**이다.
    가로로 긴 이미지를 contain으로 앉히면 위아래에 빈 띠가 생겨 사진 상단에
    가로 이음매처럼 보인다(실측 사고: 레터박스를 잘라 비율이 1.99가 되자
    가로형 판정 문턱을 넘어 contain으로 바뀌면서 오히려 띠가 생겼다).
    과감히 잘리더라도 프레임을 꽉 채우는 쪽이 항상 낫다.
    """
    return ""


# ---------------------------------------------------------------- 렌더

def render(card: dict, image: "dict | None", outdir: Path) -> Path:
    render_dir = outdir / "render"
    render_dir.mkdir(parents=True, exist_ok=True)
    cn.prep_logo(render_dir)
    font_css = cn._font_css(render_dir)

    edge = next((p for p in cn.EDGE_PATHS if Path(p).exists()), None)
    if not edge:
        raise SystemExit("[ERROR] Edge 브라우저를 찾을 수 없습니다")

    if image:
        p = Path(image["path"])
        if p.resolve().parent != render_dir.resolve():
            shutil.copy(p, render_dir / p.name)
        img_html = f'<img src="{p.name}" alt="">'
        fit = image.get("fit") or ""
    else:
        img_html, fit = "", "empty"

    source = cn.esc(card.get("source", "")).replace("\\n", "<br>").replace("\n", "<br>")

    html = ((SCRIPT_DIR / "hookcard_template.html").read_text(encoding="utf-8")
            .replace("{{FONT_FACES}}", font_css)
            .replace("{{FIT}}", fit)
            .replace("{{IMG}}", img_html)
            .replace("{{EYEBROW}}", cn.esc(card.get("eyebrow", "")))
            .replace("{{LINE1}}", cn.esc(card.get("line1", "")))
            .replace("{{LINE2}}", cn.esc(card.get("line2", "")))
            .replace("{{SOURCE}}", source))

    hp = render_dir / "hook-01.html"
    hp.write_text(html, encoding="utf-8")
    png = outdir / "hook-01.png"
    if not cn._shot(edge, hp, png):
        raise SystemExit("[ERROR] 렌더 실패")
    return png


def rerender(outdir: Path) -> None:
    doc = json.loads((outdir / "card.json").read_text(encoding="utf-8"))
    png = render(doc["card"], doc.get("image"), outdir)
    print(f"[OK] 재렌더 완료: {png}")


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description="후킹 이미지 카드 1장 생성")
    ap.add_argument("source", nargs="?", help="_posts/*.md · YouTube URL · 웹 URL · PDF 경로")
    ap.add_argument("--out", help="출력 폴더 (기본: 바탕화면/hookcard/<슬러그>)")
    ap.add_argument("--rerender", metavar="DIR", help="card.json 수정 후 재렌더 (Gemini 미호출)")
    ap.add_argument("--image", help="사진을 직접 지정")
    ap.add_argument("--no-image", action="store_true", help="사진 없이 그라디언트 배경")
    ap.add_argument("--dry-run", action="store_true", help="카피 JSON만 출력")
    ap.add_argument("--model", default="gemini-2.5-flash")
    args = ap.parse_args()

    if args.rerender:
        rerender(Path(args.rerender))
        return
    if not args.source:
        ap.error("source 를 지정하거나 --rerender 를 쓰세요")

    cn._load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit("[ERROR] GEMINI_API_KEY 가 없습니다 (.env 확인)")

    slug = re.sub(r"[^a-zA-Z0-9가-힣]+", "-", Path(args.source).stem or "hook")[:60].strip("-")
    outdir = Path(args.out) if args.out else DEFAULT_OUT / (slug or "hook")
    outdir.mkdir(parents=True, exist_ok=True)

    doc = load_source(args.source, outdir)
    if len((doc.get("content") or "")) < 200:
        raise SystemExit("[ERROR] 본문이 200자 미만입니다 — 추출 실패로 보입니다(환각 방지 중단)")

    card = make_copy(args.model, doc)

    print("\n" + json.dumps(card, ensure_ascii=False, indent=2) + "\n")
    if args.dry_run:
        return

    image = pick_image(card, doc, args.source, outdir, args.image, args.no_image)
    (outdir / "card.json").write_text(
        json.dumps({"card": card, "image": image, "source": args.source},
                   ensure_ascii=False, indent=2), encoding="utf-8")

    png = render(card, image, outdir)
    print(f"[OK] 완료: {png}")
    print(f"     카피 수정 후 재렌더: py -X utf8 scripts/hookcard.py --rerender \"{outdir}\"")


if __name__ == "__main__":
    main()
