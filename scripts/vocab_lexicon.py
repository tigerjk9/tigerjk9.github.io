#!/usr/bin/env python3
"""국립국어원 국어 기초 어휘(2023) 40,000개 목록 로더 + 난이도 주석기.

원천: https://www.korean.go.kr/front/reportData/reportDataView.do?mn_id=207&report_seq=1160
      첨부 '국어 기초 어휘 선정 및 어휘 등급화 목록 전체.xlsx' (공개 자료)
      → _papers/vocab/nikl-basic-vocab-2023.xlsx (용량이 커 gitignore)

KICE 연구보고 RRI 2026-1 이 쓴 세 원천 중 하나이며, 표준국어대사전 뜻풀이가 함께
들어 있어 '기존 뜻풀이' 열을 그대로 얻을 수 있다.

난이도 주석([LvN])은 창작이 아니라 이 등급표 조회다. 이 머신에 한국어 형태소
분석기가 없어(konlpy/mecab 부재) 어절에서 표제어를 **최장일치**로 찾는다.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "_papers" / "vocab" / "nikl-basic-vocab-2023.xlsx"
CACHE = ROOT / "scripts" / ".vocab_lexicon.json"
SHEET_ALL = "전체(1~5등급), 40,000개"

_PUNCT = re.compile(r"[^\w가-힣]+")

# 조사 — 긴 것부터 떼어 낸다. 형태소 분석기가 없어 어절에서 조사를 잘라 표제어를 남긴다.
_JOSA = tuple(sorted(
    ["으로서", "으로써", "에게서", "이라고", "라고", "에서", "에게", "으로", "부터", "까지",
     "보다", "처럼", "만큼", "조차", "마저", "밖에", "이나", "이란", "이며", "이고", "라도",
     "든지", "마다", "이야", "으로부터", "한테", "에다", "이랑", "하고", "와", "과", "은",
     "는", "이", "가", "을", "를", "에", "의", "도", "만", "로", "나", "며", "고", "뿐"],
    key=len, reverse=True))

# 받침이 어미로 축약된 활용형 복원용: '나타낸' -> '나타내'
_CODA_STRIP = {4, 8, 16, 17, 21}   # ㄴ ㄹ ㅁ ㅂ ㅆ 의 종성 인덱스


def _drop_coda(ch: str) -> Optional[str]:
    """마지막 음절의 종성을 떼어 낸 글자. 종성이 없거나 대상이 아니면 None."""
    code = ord(ch) - 0xAC00
    if not 0 <= code <= 11171:
        return None
    coda = code % 28
    if coda not in _CODA_STRIP:
        return None
    return chr(0xAC00 + (code - coda))


def _norm_grade(s) -> int:
    m = re.search(r"(\d)", str(s or ""))
    return int(m.group(1)) if m else 0


def build_lexicon(force: bool = False) -> List[dict]:
    """xlsx → 레코드 리스트. 두 번째 호출부터는 JSON 캐시를 읽는다."""
    if CACHE.exists() and not force:
        return json.loads(CACHE.read_text(encoding="utf-8"))

    import openpyxl

    if not XLSX.exists():
        raise SystemExit(
            f"[ERROR] 원천 파일이 없습니다: {XLSX}\n"
            "        국립국어원 '2023년 국어 기초 어휘 선정 및 어휘 등급화 연구' 페이지의\n"
            "        '국어 기초 어휘 선정 및 어휘 등급화 목록 전체.xlsx' 를 받아 두세요."
        )

    wb = openpyxl.load_workbook(XLSX, read_only=True)
    ws = wb[SHEET_ALL]
    out: List[dict] = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or not row[1]:
            continue
        out.append({
            "grade": _norm_grade(row[0]),
            "word": str(row[1]).strip(),
            "homonym_no": int(row[2] or 0) if str(row[2] or "").strip().isdigit() else 0,
            "pos": str(row[3] or "").strip(),
            "origin_type": str(row[4] or "").strip(),
            "source_word": str(row[5] or "").strip(),
            "gloss": str(row[6] or "").strip(),
            "field": str(row[7] or "").strip(),
        })
    CACHE.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    return out


def build_grade_index(lex: Optional[List[dict]] = None) -> Dict[str, int]:
    """표제어 → 대표 등급. 동형어가 여럿이면 **최저 등급**을 쓴다.

    가장 쉬운 뜻으로 읽힐 수 있으면 그 어절은 그만큼 쉽다고 보는 쪽이 안전하다.
    """
    lex = lex if lex is not None else build_lexicon()
    idx: Dict[str, int] = {}
    for r in lex:
        w, g = r["word"], r["grade"]
        if not w or not g:
            continue
        if w not in idx or g < idx[w]:
            idx[w] = g
    return idx


class Annotator:
    """어절에 [LvN] 을 붙인다. KICE 부록의 난이도_주석 열과 같은 표기."""

    #: 표제어 후보 최소 길이. 1글자까지 허용하면 '이/그/수' 같은 조각이 과하게 잡힌다.
    MIN_STEM = 2

    def __init__(self, index: Optional[Dict[str, int]] = None):
        self.index = index if index is not None else build_grade_index()
        self._max_word_len = max((len(w) for w in self.index), default=0)

    def lookup(self, token: str) -> Optional[int]:
        """어절에서 표제어를 찾아 등급을 돌려준다.

        형태소 분석기가 없어 네 갈래로 근사한다. 앞쪽일수록 신뢰도가 높다.
          1) 어절이 곧 표제어          '가깝다' -> 가깝다
          2) 조사를 떼어 낸 명사        '돈으로' -> 돈 / '다각형에서' -> 다각형
          3) 용언 어간 + '다'          '있는' -> 있다 / '대응하는' -> 대응하다
          4) 종성 축약 복원 + '다'      '나타낸' -> 나타내다
        """
        t = _PUNCT.sub("", token)
        if not t:
            return None

        cands: List[int] = []
        if t in self.index:                                    # 1
            cands.append(self.index[t])

        for j in _JOSA:                                        # 2
            if t.endswith(j) and len(t) > len(j):
                stem = t[: -len(j)]
                if stem in self.index:
                    cands.append(self.index[stem])
                    break

        upper = min(len(t), self._max_word_len)
        for end in range(upper, 0, -1):                        # 3
            if (t[:end] + "다") in self.index:
                cands.append(self.index[t[:end] + "다"])
                break

        for end in range(upper, 0, -1):                        # 4
            bare = _drop_coda(t[end - 1])
            if not bare:
                continue
            cand = t[: end - 1] + bare + "다"
            if cand in self.index:
                cands.append(self.index[cand])
                break

        if not cands:                                          # 접두 최장일치(마지막 수단)
            for end in range(upper, self.MIN_STEM - 1, -1):
                if t[:end] in self.index:
                    cands.append(self.index[t[:end]])
                    break

        # 여러 해석이 가능하면 **가장 쉬운 것**을 택한다. 동형어 대표 등급을 최저로
        # 잡은 것과 같은 원칙이다. 이게 없으면 '하지 않고'의 '하지'가 한자어 명사
        # 下肢(Lv5)로 잡혀 쉬운 문장이 어렵다고 판정된다(실측).
        return min(cands) if cands else None

    def annotate(self, text: str) -> str:
        """어절마다 등급 배지를 붙인 문자열. 미등재는 '(추론 결과)' 표기."""
        out = []
        for tok in (text or "").split():
            g = self.lookup(tok)
            out.append(f"{tok}[Lv{g}]" if g else f"{tok}[Lv1(추론 결과)]")
        return " ".join(out)

    def grades(self, text: str) -> List[int]:
        return [g for g in (self.lookup(t) for t in (text or "").split()) if g]

    def max_grade(self, text: str) -> int:
        """그 텍스트에 쓰인 최고 등급. 미등재 어절은 등급 판단에서 제외한다."""
        gs = self.grades(text)
        return max(gs) if gs else 0


if __name__ == "__main__":
    lex = build_lexicon()
    from collections import Counter

    dist = Counter(r["grade"] for r in lex)
    print(f"레코드 {len(lex)}개")
    print("등급 분포: " + ", ".join(f"{g}등급={dist[g]}" for g in sorted(dist)))

    idx = build_grade_index(lex)
    print(f"고유 표제어 {len(idx)}개")

    ann = Annotator(idx)
    for s in ("두 다각형에서 서로 대응하는 각",
              "물건이 지니고 있는 가치를 돈으로 나타낸 것"):
        print(f"\n  입력: {s}")
        print(f"  주석: {ann.annotate(s)}")
        print(f"  최고등급: {ann.max_grade(s)}")
