# -*- coding: utf-8 -*-
"""
build_research_db.py — 논문리뷰 포스트를 리서치 허브용 구조화 JSON으로 변환한다.

대상: _posts/*.md 중 '리뷰어의 ADD' 헤딩을 가진 포스트 (고정 6섹션 논문리뷰).
출력: assets/research-db.json

설계 원칙
- 섹션은 원자화하지 않고 텍스트 블롭으로 보존 (h2/h3·번호 off-by-one·존칭/단정체 편차 흡수).
- 섹션 매핑은 번호가 아니라 헤딩 키워드로 (목적/방법/발견/결론/ADD/탐구).
- 출처 포맷 6종(## 출처 · _**출처:**_ · **출처**: · ### APA · 📚 등) 유연 추출 후 arXiv/DOI 정규식.
- 요약은 연구목적 첫 문장에서 추출 (생성·환각 금지).

실행:  py scripts/build_research_db.py        # assets/research-db.json 생성
       py scripts/build_research_db.py --dry-run   # 리포트만, 파일 미기록

/paper 등 논문리뷰 포스트를 새로 올릴 때마다 재실행해 JSON을 갱신·커밋한다.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime

# Windows 콘솔 cp949에서 한글 print 안전
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_DIR = os.path.join(ROOT, "_posts")
OUT_PATH = os.path.join(ROOT, "assets", "research-db.json")

# '리뷰어의 ADD' 헤딩으로 논문리뷰 포스트를 식별
ADD_MARKER = "리뷰어의 ADD"

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_front_matter(text):
    """front matter를 손으로 파싱한다 (PyYAML 미설치 환경 대응)."""
    m = FM_RE.match(text)
    if not m:
        return None, text
    block = m.group(1)
    body = text[m.end():]
    fm = {}

    def scalar(key):
        mm = re.search(r"^%s:\s*(.+?)\s*$" % re.escape(key), block, re.MULTILINE)
        if not mm:
            return None
        v = mm.group(1).strip()
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        return v

    def array(key):
        # 인라인 [a, b, c] 우선, 아니면 - item 리스트
        mm = re.search(r"^%s:\s*\[(.*?)\]" % re.escape(key), block, re.MULTILINE | re.DOTALL)
        if mm:
            inner = mm.group(1)
            items = [x.strip().strip('"').strip("'") for x in inner.split(",")]
            return [x for x in items if x]
        # 블록 리스트
        items = []
        mm = re.search(r"^%s:\s*\n((?:\s*-\s*.+\n?)+)" % re.escape(key), block, re.MULTILINE)
        if mm:
            for line in mm.group(1).splitlines():
                lm = re.match(r"\s*-\s*(.+)", line)
                if lm:
                    items.append(lm.group(1).strip().strip('"').strip("'"))
        return items

    fm["title"] = scalar("title") or ""
    date_raw = scalar("date") or ""
    fm["date"] = date_raw[:10] if len(date_raw) >= 10 else date_raw
    fm["categories"] = array("categories")
    fm["tags"] = array("tags")
    fm["permalink"] = scalar("permalink") or ""
    # teaser는 header 아래 중첩 → 블록 전체에서 탐색
    tm = re.search(r"teaser:\s*(\S+)", block)
    fm["teaser"] = tm.group(1).strip().strip('"').strip("'") if tm else None
    return fm, body


def heading_iter(body, level):
    """정확히 level개의 # 를 가진 헤딩만 순회 (level+1 은 제외)."""
    pat = re.compile(r"^%s(?!#)[ \t]+(.+?)[ \t]*$" % ("#" * level), re.MULTILINE)
    return list(pat.finditer(body))


def detect_level(body):
    """'리뷰어의 ADD' 헤딩의 # 개수로 섹션 헤딩 레벨을 판정."""
    m = re.search(r"^(#{2,4})(?!#)[ \t]+.*리뷰어의 ADD", body, re.MULTILINE)
    if m:
        return len(m.group(1))
    return 2


def split_sections(body, level):
    """레벨 헤딩 기준으로 (heading, content) 목록 반환."""
    heads = heading_iter(body, level)
    out = []
    for i, h in enumerate(heads):
        start = h.end()
        end = heads[i + 1].start() if i + 1 < len(heads) else len(body)
        out.append((h.group(1).strip(), body[start:end].strip()))
    return out


def classify(heading):
    """헤딩 텍스트 → 표준 섹션 키 (키워드 우선순위)."""
    h = heading
    if "리뷰어" in h or "ADD" in h or "생각 더하기" in h:
        return "add_one"
    if "탐구" in h or ("질문" in h and "탐구" not in h) or "질문" in h:
        return "questions"
    if "결론" in h or "시사점" in h or "함의" in h:
        return "implications"
    if "발견" in h or "주요" in h or "결과" in h:
        return "findings"
    # '연구의 목적 및 방법' 결합 헤딩 대응: 목적을 방법보다 먼저 판정
    if "목적" in h or "서론" in h or "배경" in h:
        return "purpose"
    if "방법" in h:
        return "method"
    return None


FIG_RE = re.compile(r"<figure\b.*?</figure>", re.DOTALL | re.IGNORECASE)
IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


def clean_text(s):
    if not s:
        return ""
    s = FIG_RE.sub("", s)
    s = IMG_RE.sub("", s)
    s = BR_RE.sub("", s)
    s = COMMENT_RE.sub("", s)
    # 3+ 연속 공백 라인 축소
    s = re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", s)
    # 각 줄 우측 공백 제거
    s = "\n".join(line.rstrip() for line in s.splitlines())
    return s.strip()


def strip_markdown(s):
    """요약용: 마크다운 마커·괄호 번호·인용 기호를 제거해 평문화."""
    s = clean_text(s)
    s = re.sub(r"^[>*\-\s]+", "", s)          # 선행 인용/불릿
    s = re.sub(r"^\(\d+\)\s*", "", s)          # 선행 (1)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)     # bold
    s = re.sub(r"\*(.+?)\*", r"\1", s)          # italic
    s = re.sub(r"`(.+?)`", r"\1", s)            # code
    s = re.sub(r"#{1,4}\s*", "", s)             # 잔여 헤딩
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def make_summary(purpose_text, limit=150):
    """연구목적 첫 1~2문장에서 카드용 한 줄 요약 추출."""
    if not purpose_text:
        return ""
    flat = strip_markdown(purpose_text)
    if not flat:
        return ""
    # 문장 경계: 마침표 뒤 공백/끝
    sents = re.split(r"(?<=[.?!])\s+", flat)
    summary = ""
    for sent in sents:
        if not summary:
            summary = sent
        elif len(summary) < 70:
            summary = (summary + " " + sent).strip()
        else:
            break
    if len(summary) > limit:
        summary = summary[:limit].rstrip() + "…"
    return summary


# 출처 마커: 헤딩형 / 강조형 / 인라인형
SOURCE_MARKERS = [
    re.compile(r"^#{1,4}[ \t]*[^\n]*출처[^\n]*$", re.MULTILINE),
    re.compile(r"^#{1,4}[ \t]*[^\n]*APA[^\n]*$", re.MULTILINE),
    re.compile(r"^_?\*\*[^\n]*출처[^\n]*", re.MULTILINE),
    re.compile(r"^\*\*출처\*\*", re.MULTILINE),
    re.compile(r"^_+[^\n]*출처[^\n]*", re.MULTILINE),
]

ARXIV_RE = re.compile(r"ar[Xx]iv[^0-9]{0,22}(\d{4}\.\d{4,5})")
ARXIV_URL_RE = re.compile(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", re.IGNORECASE)
DOI_RE = re.compile(r"(?:doi\.org/|doi:\s*)(10\.\d{4,9}/[^\s\)\]\}<>_*]+)", re.IGNORECASE)


def extract_source(body):
    """출처 블록 텍스트 + arXiv id + DOI 추출."""
    best = None
    for pat in SOURCE_MARKERS:
        for m in pat.finditer(body):
            if best is None or m.start() > best.start():
                best = m
    blob = ""
    if best is not None:
        blob = body[best.start():best.start() + 900]
    # 정제: 마커·인용·강조 제거
    cite = blob
    cite = re.sub(r"^#{1,4}[ \t]*", "", cite, flags=re.MULTILINE)
    cite = re.sub(r"[>_*`]", "", cite)
    cite = re.sub(r"📚|✨|🔗", "", cite)
    cite = clean_text(cite)
    # 첫 줄이 '출처'/'APA' 라벨뿐이면 제거
    lines = [l for l in cite.splitlines() if l.strip()]
    if lines and re.fullmatch(r"[^\w가-힣]*(출처|APA[^\n]*|References?)[^\w가-힣]*", lines[0].strip(), re.IGNORECASE):
        lines = lines[1:]
    cite = "\n".join(lines).strip()
    if len(cite) > 500:
        cite = cite[:500].rstrip() + "…"

    search_space = blob if blob else body
    arxiv = None
    am = ARXIV_URL_RE.search(search_space) or ARXIV_RE.search(search_space)
    if am:
        arxiv = am.group(1)
    doi = None
    dm = DOI_RE.search(search_space)
    if dm:
        doi = dm.group(1).rstrip(".")
    # arXiv 링크 우선 구성
    link = None
    if arxiv:
        link = "https://arxiv.org/abs/%s" % arxiv
    elif doi:
        link = "https://doi.org/%s" % doi
    return {"citation": cite, "arxiv_id": arxiv, "doi": doi, "link": link}


def first_body_image(body):
    m = re.search(r'<img\s+src="([^"]+)"', body, re.IGNORECASE)
    return m.group(1) if m else None


def process(path):
    text = read(path)
    if ADD_MARKER not in text:
        return None, []
    fm, body = parse_front_matter(text)
    warns = []
    if fm is None:
        return None, ["front matter 파싱 실패: %s" % os.path.basename(path)]

    level = detect_level(body)
    sections_raw = split_sections(body, level)
    mapped = {}
    for heading, content in sections_raw:
        key = classify(heading)
        if key and key not in mapped:
            mapped[key] = clean_text(content)

    base = os.path.basename(path)
    for req in ("purpose", "findings", "implications", "add_one"):
        if req not in mapped or not mapped[req]:
            warns.append("[%s] 섹션 누락/빈값: %s" % (base, req))

    src = extract_source(body)
    if not src["citation"]:
        warns.append("[%s] 출처 추출 실패" % base)

    teaser = fm.get("teaser") or first_body_image(body)

    record = {
        "id": (fm.get("permalink") or "/" + base[:-3] + "/").strip("/"),
        "title": fm.get("title", "").strip(),
        "date": fm.get("date", ""),
        "year": (fm.get("date", "") or "")[:4],
        "url": fm.get("permalink") or "",
        "categories": fm.get("categories", []),
        "tags": fm.get("tags", []),
        "teaser": teaser,
        "summary": make_summary(mapped.get("purpose") or mapped.get("findings", "")),
        "sections": {
            "purpose": mapped.get("purpose", ""),
            "method": mapped.get("method", ""),
            "findings": mapped.get("findings", ""),
            "implications": mapped.get("implications", ""),
            "add_one": mapped.get("add_one", ""),
            "questions": mapped.get("questions", ""),
        },
        "source": src,
    }
    if not record["url"]:
        warns.append("[%s] permalink 없음 (파일명 파생)" % base)
        record["url"] = "/post/%s/" % base[11:-3]
    return record, warns


def main():
    dry = "--dry-run" in sys.argv
    files = sorted(
        os.path.join(POSTS_DIR, f)
        for f in os.listdir(POSTS_DIR)
        if f.endswith(".md")
    )
    records = []
    all_warns = []
    for path in files:
        rec, warns = process(path)
        all_warns.extend(warns)
        if rec:
            records.append(rec)

    # 최신순 정렬
    records.sort(key=lambda r: r["date"], reverse=True)

    # 태그 빈도 집계
    tag_freq = {}
    for r in records:
        for t in r["tags"]:
            tag_freq[t] = tag_freq.get(t, 0) + 1
    top_tags = sorted(tag_freq.items(), key=lambda kv: (-kv[1], kv[0]))
    years = sorted({r["year"] for r in records if r["year"]}, reverse=True)

    db = {
        "meta": {
            "count": len(records),
            "generated": datetime.now().strftime("%Y-%m-%d"),
            "years": years,
            "tags": [{"name": k, "count": v} for k, v in top_tags],
        },
        "posts": records,
    }

    # 리포트
    print("=" * 56)
    print("리서치 DB 빌드 리포트")
    print("=" * 56)
    print("논문리뷰 포스트: %d편" % len(records))
    fill = {k: 0 for k in ("purpose", "method", "findings", "implications", "add_one", "questions")}
    arxiv_n = doi_n = cite_n = 0
    for r in records:
        for k in fill:
            if r["sections"][k]:
                fill[k] += 1
        if r["source"]["arxiv_id"]:
            arxiv_n += 1
        if r["source"]["doi"]:
            doi_n += 1
        if r["source"]["citation"]:
            cite_n += 1
    print("섹션 채움률:")
    for k in ("purpose", "method", "findings", "implications", "add_one", "questions"):
        print("  - %-13s %3d/%d" % (k, fill[k], len(records)))
    print("출처: citation %d / arXiv %d / DOI %d" % (cite_n, arxiv_n, doi_n))
    print("고유 태그: %d개, 연도: %s" % (len(tag_freq), ", ".join(years)))
    if all_warns:
        print("-" * 56)
        print("경고 %d건:" % len(all_warns))
        for w in all_warns:
            print("  ! " + w)
    print("=" * 56)

    if dry:
        print("[dry-run] 파일 미기록")
        return

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, separators=(",", ":"))
    size_kb = os.path.getsize(OUT_PATH) / 1024
    print("기록 완료: %s (%.0f KB)" % (os.path.relpath(OUT_PATH, ROOT), size_kb))


if __name__ == "__main__":
    main()
