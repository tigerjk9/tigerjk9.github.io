#!/usr/bin/env python3
"""교육자용 큐레이션 프롬프트 라이브러리 빌드.

prompts.chat(CC0 1.0) 원본 prompts.csv에서 교육·실무 관련 프롬프트를 화이트리스트로
선별 → Gemini로 한국어 번안 + 교육 활용 맥락 첨부 → assets/prompt-library.json 출력.

- 콘텐츠 라이선스: prompts.chat 프롬프트는 CC0 1.0 퍼블릭 도메인(출처 표기 의무 없음).
- 증분 캐시: 원문 prompt 텍스트 해시 기준. 원문이 그대로면 재번역 API 호출을 건너뛴다.
- 스키마(페이지 JS와 단일 계약): id, category, title_ko, desc_ko, prompt_ko, prompt_en,
  tags[], contributor, source_url, type

사용법:
  py scripts/build_prompt_library.py            # 빌드 (증분)
  py scripts/build_prompt_library.py --force     # 캐시 무시 전체 재번역
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import os
import ssl
import sys
from pathlib import Path

import requests

try:
    import google.generativeai as genai
except Exception:  # noqa
    genai = None

requests.packages.urllib3.disable_warnings()  # type: ignore
ssl._create_default_https_context = ssl._create_unverified_context

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "prompt-library.json"
CACHE = ROOT / "scripts" / ".prompt_library_cache.json"
CSV_URL = "https://raw.githubusercontent.com/f/prompts.chat/main/prompts.csv"
SOURCE_URL = "https://prompts.chat/"
MODEL = "gemini-2.5-flash"

# (act 이름, 교육 카테고리) — act 이름은 prompts.csv의 act 컬럼과 정확히 일치해야 한다.
WHITELIST = [
    ("Math Teacher", "수업·학습 설계"),
    ("Philosophy Teacher", "수업·학습 설계"),
    ("Instructor in a School", "수업·학습 설계"),
    ("Socratic Universal Tutor", "수업·학습 설계"),
    ("explain like I am 8", "수업·학습 설계"),
    ("Adaptive Socratic Learning Coach", "수업·학습 설계"),
    ("Spoken English Teacher and Improver", "언어·영어 지도"),
    ("English Pronunciation Helper", "언어·영어 지도"),
    ("English Grammar and Style Corrector", "언어·영어 지도"),
    ("English Teacher for Translation and Cultural Explanation", "언어·영어 지도"),
    ("Workplace English Speaking Coach", "언어·영어 지도"),
    ("Essay Writer", "글쓰기·문서"),
    ("Academic Text Refinement Assistant", "글쓰기·문서"),
    ("Academic Research Writer", "글쓰기·문서"),
    ("Professional Email Writer for Any Occasion", "글쓰기·문서"),
    ("Context-Aware Email Assistant", "글쓰기·문서"),
    ("Interactive Quiz", "평가·피드백"),
    ("Course Feedback Analysis", "평가·피드백"),
    ("Feedback Synthesizer", "평가·피드백"),
    ("Key Concepts and Essential Definitions for Exam", "평가·피드백"),
    ("Public Speaking Coach", "발표·소통"),
    ("Academic PowerPoint Presentation Designer", "발표·소통"),
    ("Debate Coach", "발표·소통"),
    ("Note-Taking Assistant", "연구·정리"),
    ("Act as a Senior Research Paper Evaluator", "연구·정리"),
    ("Comprehensive Academic Paper Writing Guide", "연구·정리"),
    ("Clean BibTeX Formatter for Academic Projects", "연구·정리"),
    ("Career Coach", "진로·멘토링"),
    ("Interview Preparation Coach", "진로·멘토링"),
    ("Motivational Coach", "진로·멘토링"),
    ("School Life Mentor", "진로·멘토링"),
    ("Senior Academic Advisor", "진로·멘토링"),
]

CATEGORY_ORDER = [
    "수업·학습 설계", "언어·영어 지도", "글쓰기·문서",
    "평가·피드백", "발표·소통", "연구·정리", "진로·멘토링",
]


def load_env_key() -> str:
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("GEMINI_API_KEY"):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return os.environ.get("GEMINI_API_KEY", "")


def fetch_csv_rows():
    r = requests.get(CSV_URL, verify=False, timeout=90,
                     headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    r.encoding = "utf-8"
    csv.field_size_limit(10_000_000)
    return list(csv.DictReader(io.StringIO(r.text)))


def h(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def clean_prompt(text: str) -> str:
    """prompts.chat 웹 UI용 ${변수} 자리표시자 정리 + 과잉 빈 줄 정돈.

    ${...}는 원 사이트의 변수 채우기 위젯 문법이라 카드에 그대로 노출되면
    사용자가 뜻 모를 코드로 오인한다. 문장이 깨지지 않게 3단계로 처리:
    ①`${이름:기본값}` → 기본값 인라인 치환 ②단독 라인 `${이름}` → 라인 제거
    ③인라인 `${이름}` → `[이름]` 입력란 표기.
    """
    import re
    text = text or ""
    text = re.sub(r"\$\{([^}:\n]*):([^}\n]*)\}",
                  lambda m: m.group(2).strip(), text)
    text = re.sub(r"^[ \t]*\$\{[^}\n]*\}[ \t]*$", "", text, flags=re.M)
    text = re.sub(r"\$\{([^}\n]*)\}", lambda m: "[" + m.group(1).strip() + "]", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


PROMPT_TMPL = """당신은 한국 교육 현장을 잘 아는 프롬프트 큐레이터다.
아래 영어 프롬프트(원문, CC0)를 한국 교사·교육 관계자가 그대로 복사해 쓸 수 있도록 한국어로 번안한다.

규칙:
- 번역이 아닌 번안: 원문 의도·구조를 유지하되 자연스러운 한국어 프롬프트로 재서술한다.
- prompt_ko는 사용자가 AI에게 바로 붙여넣어 쓰는 지시문이다. 완결된 프롬프트로 작성한다.
- desc_ko는 이 프롬프트를 언제·어떻게 쓰면 좋은지 한 문장(교육 현장 관점). 존칭 없이 단정체.
- title_ko는 12자 내외의 명료한 한국어 제목.
- tags는 2~4개의 한국어 키워드.
- 원문에 없는 기능을 지어내지 않는다.

반드시 아래 JSON 배열 형식으로만 응답한다(설명 문장 금지):
[{{"act":"<원문 act 그대로>","title_ko":"...","desc_ko":"...","prompt_ko":"...","tags":["..."]}}]

번안 대상:
{items}
"""


def translate_batch(model, items):
    payload = "\n\n".join(
        f'### act: {it["act"]}\n{it["prompt"]}' for it in items
    )
    resp = model.generate_content(
        PROMPT_TMPL.format(items=payload),
        generation_config={"response_mime_type": "application/json",
                           "temperature": 0.4},
    )
    return json.loads(resp.text)  # 순서 보존 리스트


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    key = load_env_key()
    if not key or genai is None:
        print("[ERROR] GEMINI_API_KEY 또는 google-generativeai 없음")
        sys.exit(1)
    genai.configure(api_key=key)
    model = genai.GenerativeModel(MODEL)

    print("[INFO] prompts.csv 다운로드 중...")
    rows = fetch_csv_rows()
    by_act = {}
    for r in rows:
        by_act.setdefault(r["act"], r)  # 첫 등장 우선
    print(f"[INFO] 원본 프롬프트 {len(rows)}개")

    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    if args.force:
        cache = {}

    # 캐시 미스만 카테고리 배치로 번역
    selected = []
    for act, cat in WHITELIST:
        row = by_act.get(act)
        if not row:
            print(f"[WARN] 원본에서 act 미발견: {act!r} (건너뜀)")
            continue
        selected.append((act, cat, row))

    todo = [(act, cat, row) for act, cat, row in selected
            if cache.get(act, {}).get("_hash") != h(row["prompt"])]
    print(f"[INFO] 선별 {len(selected)}개 · 번역 필요 {len(todo)}개")

    # 카테고리 순서로 5개씩 배치
    for i in range(0, len(todo), 5):
        batch = todo[i:i + 5]
        items = [{"act": act, "prompt": row["prompt"]} for act, _, row in batch]
        print(f"[INFO] Gemini 번역 배치 {i//5 + 1} ({len(batch)}개)...")
        out_list = translate_batch(model, items)
        by_resp = {d.get("act"): d for d in out_list if isinstance(d, dict)}
        for j, (act, cat, row) in enumerate(batch):
            d = by_resp.get(act)  # act 정확 매칭 우선
            if not d and j < len(out_list) and isinstance(out_list[j], dict):
                d = out_list[j]   # 폴백: 순서 기반 매칭
            if not d:
                print(f"[WARN] 번역 누락: {act!r}")
                continue
            cache[act] = {
                "_hash": h(row["prompt"]),
                "title_ko": d.get("title_ko", act),
                "desc_ko": d.get("desc_ko", ""),
                "prompt_ko": d.get("prompt_ko", ""),
                "tags": d.get("tags", []),
            }
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

    # 최종 레코드 조립
    records = []
    for idx, (act, cat, row) in enumerate(selected):
        c = cache.get(act, {})
        # 기여자는 GitHub 아이디로 보이는 값만 유지 — 이메일/다중어절은 개인정보라 제거
        # (prompt-library.json은 공개 커밋되므로 원본 이메일을 그대로 담지 않는다)
        contrib = (row.get("contributor", "") or "").split(",")[0].strip()
        if "@" in contrib or " " in contrib or not contrib:
            contrib = ""
        records.append({
            "id": f"pl-{idx:03d}",
            "category": cat,
            "title_ko": c.get("title_ko", act),
            "desc_ko": c.get("desc_ko", ""),
            "prompt_ko": clean_prompt(c.get("prompt_ko", "")),
            "prompt_en": clean_prompt(row["prompt"]),
            "tags": c.get("tags", []),
            "contributor": contrib,
            "type": row.get("type", "TEXT"),
            "source_url": SOURCE_URL,
        })

    doc = {
        "meta": {
            "source": "prompts.chat",
            "license": "CC0 1.0",
            "count": len(records),
            "categories": CATEGORY_ORDER,
        },
        "prompts": records,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] {OUT} - {len(records)}개 프롬프트 저장")


if __name__ == "__main__":
    main()
