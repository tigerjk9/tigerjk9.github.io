#!/usr/bin/env python3
"""vocab_lexicon 검증 — US-001 / US-002 인수 조건."""
from __future__ import annotations

import random
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vocab_lexicon import Annotator, build_grade_index, build_lexicon  # noqa: E402

fails = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"  [{'OK  ' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
    if not cond:
        fails.append(name)


print("=== US-001 원천 정규화 ===")
lex = build_lexicon()
check("레코드 40,000개", len(lex) == 40000, f"실제 {len(lex)}")
dist = Counter(r["grade"] for r in lex)
expect = {1: 5000, 2: 2500, 3: 5500, 4: 10000, 5: 17000}
check("등급 분포 일치", dict(dist) == expect, str(dict(sorted(dist.items()))))
r0 = lex[0]
check("필드 8종", set(r0) == {"grade", "word", "homonym_no", "pos", "origin_type",
                              "source_word", "gloss", "field"}, str(sorted(r0)))
check("뜻풀이 보유율 99% 이상",
      sum(1 for r in lex if r["gloss"]) / len(lex) >= 0.99,
      f"{sum(1 for r in lex if r['gloss'])}/{len(lex)}")

idx = build_grade_index(lex)
check("동형어는 최저 등급 대표", idx.get("가") == min(
    r["grade"] for r in lex if r["word"] == "가"), f"'가' -> Lv{idx.get('가')}")

print("\n=== US-002 난이도 주석기 ===")
ann = Annotator(idx)

a = ann.annotate("두 다각형에서 서로 대응하는 각")
check("'두[Lv1]' 포함", "두[Lv1]" in a, a)
check("'다각형에서[Lv4]' 포함", "다각형에서[Lv4]" in a)
check("max_grade == 4", ann.max_grade("두 다각형에서 서로 대응하는 각") == 4)

for w in ("가깝다", "가까워지다", "가까이"):
    check(f"활용형 '{w}' 등급 조회", ann.lookup(w) is not None, f"Lv{ann.lookup(w)}")

for w, why in (("있는", "용언 어간+다"), ("돈으로", "조사 분리"), ("나타낸", "종성 축약 복원")):
    check(f"'{w}' ({why})", ann.lookup(w) is not None, f"Lv{ann.lookup(w)}")

check("미등재는 (추론 결과) 표기", "(추론 결과)" in ann.annotate("퀄리티가"),
      ann.annotate("퀄리티가"))

# 실제 뜻풀이 전체에 대한 조회 성공률 — 주석기 실용성의 핵심 지표
random.seed(20260803)
sample = random.sample([r for r in lex if r["gloss"]], 400)
tok = hit = 0
for r in sample:
    for t in r["gloss"].split():
        tok += 1
        if ann.lookup(t) is not None:
            hit += 1
rate = hit / tok
check("뜻풀이 어절 조회 성공률 80% 이상", rate >= 0.80, f"{rate:.1%} ({hit}/{tok})")

print(f"\n{'통과' if not fails else '실패 ' + str(len(fails)) + '건: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
