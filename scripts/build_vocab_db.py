#!/usr/bin/env python3
"""학습자 친화적 어휘 데이터베이스 생성.

  py -X utf8 scripts/build_vocab_db.py --dry-run          # 대상·프롬프트만
  py -X utf8 scripts/build_vocab_db.py --limit 20         # 20개만 생성(중단 후 재개 가능)
  py -X utf8 scripts/build_vocab_db.py                    # 전체(기본 500개)
  py -X utf8 scripts/build_vocab_db.py --targets 1000     # 대상 규모 확장

KICE 연구보고 RRI 2026-1 이 만든 어휘 DB 는 미공개다. 그 방식·형식을 공개 자료로
재현한다. 원천은 국립국어원 국어 기초 어휘 40,000개(표준국어대사전 뜻풀이 포함).

핵심은 '난이도 주석'이 창작이 아니라 **등급표 조회**라는 점이다. 생성된 뜻풀이의
어절을 등급표에 대조해 [LvN] 을 붙이고, 4등급 이상이 섞이면 다시 쓰게 한다.
KICE 는 이 규칙을 입력측(표준국어대사전 뜻풀이가 어려우면 LLM 개입)에 썼고,
여기서는 출력측(생성 결과가 어려우면 재작성)에도 적용해 결과를 보증한다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from vocab_lexicon import (Annotator, _drop_coda, build_grade_index,  # noqa: E402
                           build_lexicon)

TARGETS_FILE = SCRIPT_DIR / ".vocab_targets.json"
CACHE_FILE = SCRIPT_DIR / ".vocab_cache.json"
OUT_FILE = ROOT / "assets" / "vocab-db.json"

DEFAULT_TARGETS = 500          # KICE 사고도구어 500개 선례
EASY_MAX_GRADE = 3             # 생성 뜻풀이가 넘지 말아야 할 등급
MAX_REWRITES = 2

CONTENT_POS = ("명사", "동사", "형용사")

SUBJECTS = ("국어", "수학", "사회", "과학", "도덕", "음악", "미술",
            "체육", "실과", "영어", "역사", "기술", "가정")

# 학습자용 도구에 실으면 안 되는 말. 국립국어원 목록은 국어 어휘 전체를 등급화한
# 것이라 비하 표현도 등급이 매겨져 들어 있다(예: '병신' — 장애 비하). 사전으로서는
# 수록이 맞지만, 초·중학생이 검색하는 화면에 뜻풀이와 예문을 붙여 놓을 이유는 없다.
BLOCKLIST = {"병신", "생지옥", "따발총"}


# ---------------------------------------------------------------- 대상 선정

def select_targets(n: int = DEFAULT_TARGETS, force: bool = False) -> List[dict]:
    """교과 학습에서 실제로 걸리는 사고도구어 성격의 어휘를 고른다.

    선정 규칙 — 다섯을 모두 만족해야 한다.
      ① 등급 3~4      : 1~2등급은 이미 쉽고, 5등급은 초·중학교 교과 범위를 넘는다
      ② 품사 명사/동사/형용사 : 조사·어미는 뜻풀이 대상이 아니다
      ③ 분야 일반어    : 전문어(의학·법률 등)는 교과 공통 어휘가 아니다
      ④ 어종 한자어/혼종어 + 추상 뜻풀이
         사고도구어(분석·비교·근거·조건처럼 여러 교과에서 사고에 쓰이는 말)를
         가려내는 **대리 지표**다. KICE 는 교과서 말뭉치의 교차 출현 빈도로 500개를
         뽑았지만 그 말뭉치가 공개돼 있지 않다. 한자어 여부와 뜻풀이의 추상성
         (`~하는 일/~함/~것/~성질/~상태`로 끝남)으로 근사한다.
         '가래떡·가마솥' 같은 구체 명사가 걸러진다.
      ⑤ 기존 뜻풀이의 최고 등급 4 이상
         = 표준국어대사전 뜻풀이 자체가 어려워 재작성 가치가 있는 것.
           KICE 가 LLM 을 개입시킨 조건과 같다.
    """
    if TARGETS_FILE.exists() and not force:
        cached = json.loads(TARGETS_FILE.read_text(encoding="utf-8"))
        if len(cached) >= n:
            return cached[:n]

    lex = build_lexicon()
    ann = Annotator(build_grade_index(lex))
    abstract = re.compile(r"(하는 일|하는 것|되는 일|되는 것|함\.|짓\.|성질|상태|정도|"
                          r"관계|방법|과정|결과|현상|생각|태도|모양)")

    picked = []
    for r in lex:
        if r["word"] in BLOCKLIST:
            continue
        if r["grade"] not in (3, 4):
            continue
        if not any(p in r["pos"] for p in CONTENT_POS):
            continue
        if "전문어" in r["field"]:
            continue
        if r["origin_type"] not in ("한자어", "혼종어"):
            continue
        gloss = r["gloss"]
        if not gloss or len(gloss) < 6:
            continue
        if not abstract.search(gloss):
            continue
        mg = ann.max_grade(gloss)
        if mg < 4:
            continue
        picked.append({**r, "max_grade_original": mg})

    # 결정적 정렬 후, 목록이 n 보다 많으면 **일정 간격으로 솎아** 가나다 전 구간을 덮는다.
    # 앞에서 n 개를 자르면 '가'로 시작하는 말만 뽑히는 쏠림이 생긴다(실측).
    picked.sort(key=lambda r: (r["grade"], r["word"], r["homonym_no"]))
    if len(picked) > n:
        stride = len(picked) / n
        picked = [picked[int(i * stride)] for i in range(n)]

    TARGETS_FILE.write_text(json.dumps(picked, ensure_ascii=False, indent=1), encoding="utf-8")
    return picked


# ---------------------------------------------------------------- 생성

PROMPT = """너는 초등 고학년~중학생을 위한 국어 어휘 교육 전문가다.
아래 낱말의 사전 뜻풀이를 학습자가 이해할 수 있는 말로 다시 쓰고, 예시문 두 개를 만든다.

[낱말] {word}
[품사] {pos}
[사전 뜻풀이] {gloss}

규칙
1. 쉬운 뜻풀이는 한 문장. 어려운 말을 쓰지 않는다. 초등 고학년이 읽고 바로 이해할 수준.
2. **뜻풀이 안에 '{word}' 라는 말을 절대 쓰지 않는다.** 그 말을 모르는 사람에게 설명하는 것이다.
3. 품사에 맞게 끝맺는다. 명사는 '~것.' 또는 '~일.', 동사는 '~하다.', 형용사는 '~하다.'
4. 원래 뜻을 바꾸거나 좁히지 않는다. 사전 뜻풀이에 없는 내용을 지어내지 않는다.
5. 예시문 두 개는 모두 '{word}' 를 넣어 자연스러운 문장으로 만든다.
   - example_general: 일상에서 쓰는 맥락
   - example_subject: 학교 교과 수업 맥락. subject 에 그 교과명을 쓴다
     (국어, 수학, 사회, 과학, 도덕, 음악, 미술, 체육, 실과, 영어 중 하나)
6. 문장은 짧게. 한 문장이 25자를 넘지 않게 한다.

JSON 객체 하나만 출력한다. 다른 말은 쓰지 않는다.
{{"easy_gloss": "...", "example_general": "...", "example_subject": "...", "subject": "..."}}"""

REWRITE = """방금 쓴 쉬운 뜻풀이에 아직 어려운 말이 있다.

[낱말] {word}
[품사] {pos}
[사전 뜻풀이] {gloss}
[직전 뜻풀이] {prev}
[지적된 문제] {hard}

지적된 문제를 모두 고쳐 다시 쓴다. 뜻은 그대로 두고 표현만 바꾼다.
'{word}' 라는 말은 여전히 쓰지 않는다. 존댓말('~입니다')이 아니라 사전 문체로 쓴다.
규칙은 앞과 같다.

JSON 객체 하나만 출력한다.
{{"easy_gloss": "...", "example_general": "...", "example_subject": "...", "subject": "..."}}"""


def _load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def gemini_json(model: str, prompt: str) -> dict:
    """REST 직접 호출. google-generativeai SDK 를 쓰지 않는 이유가 있다.

    gemini-2.5-flash 는 thinking 이 기본 켜져 있어 maxOutputTokens 를 사고 과정이
    먼저 소진한다. 그러면 JSON 이 중간에 끊겨 파싱이 통째로 실패한다(실측: 19개
    연속 'Unterminated string'). thinkingBudget: 0 으로 꺼야 하는데 이 머신의
    SDK 버전은 GenerationConfig 에서 thinking_config 를 거부한다.
    research-ask/lib/store.js 가 같은 이유로 REST 를 쓴다.
    """
    import ssl
    import urllib.error
    import urllib.request

    url = (f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
           f"?key={os.environ['GEMINI_API_KEY']}")
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            # 스키마로 모양을 못 박는다. 프롬프트에 교과명을 열거하는 것만으로는
            # '법률·의학·기상·건축' 같은 값이 223종까지 흩어졌다(실측). enum 이 필요하다.
            # 문자열 자리에 dict 를 넣어 보내던 실패도 구조적으로 막힌다.
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "easy_gloss": {"type": "STRING"},
                    "example_general": {"type": "STRING"},
                    "example_subject": {"type": "STRING"},
                    "subject": {"type": "STRING", "enum": list(SUBJECTS)},
                },
                "required": ["easy_gloss", "example_general",
                             "example_subject", "subject"],
            },
            "temperature": 0.4,
            "maxOutputTokens": 800,
            "thinkingConfig": {"thinkingBudget": 0},
        },
    }).encode("utf-8")
    req = urllib.request.Request(url, data=body,
                                 headers={"Content-Type": "application/json"})
    raw = urllib.request.urlopen(req, context=ssl._create_unverified_context(),
                                 timeout=90).read()
    data = json.loads(raw.decode("utf-8"))
    cand = data["candidates"][0]
    if cand.get("finishReason") not in (None, "STOP"):
        raise RuntimeError(f"생성 중단: {cand.get('finishReason')}")
    return json.loads(cand["content"]["parts"][0]["text"])


def _s(v) -> str:
    """Gemini 가 문자열 자리에 객체/배열을 넣어 보내는 경우가 있다(실측: easy_gloss 가 dict).
    그대로 .strip() 하면 AttributeError 로 배치가 통째로 죽으므로 여기서 흡수한다."""
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, (list, tuple)):
        return " ".join(_s(x) for x in v).strip()
    if isinstance(v, dict):
        return " ".join(_s(x) for x in v.values()).strip()
    return "" if v is None else str(v).strip()


# ---------------------------------------------------------------- 검증

def validate(rec: dict, card: dict, ann: Annotator) -> List[str]:
    """생성 결과 검사. 반환된 문제 목록이 비어야 통과."""
    issues = []
    word, pos = rec["word"], rec["pos"]
    gloss = _s(card.get("easy_gloss"))

    if not gloss:
        issues.append("easy_gloss 가 비어 있음")
        return issues

    # 순환 정의 — 모르는 말을 그 말로 설명하면 뜻풀이가 아니다
    if word in gloss:
        issues.append(f"뜻풀이에 표제어 '{word}' 가 등장(순환 정의)")

    hard = [t for t in gloss.split() if (ann.lookup(t) or 0) > EASY_MAX_GRADE]
    if hard:
        issues.append("어려운 말: " + " ".join(hard))

    if re.search(r"(입니다|합니다|됩니다|습니다)", gloss):
        issues.append("존댓말 사용 — 사전 문체로 쓸 것")

    # 품사별 종결 — 명사는 명사구로, 용언은 '~다' 로 끝나야 한다.
    # 허용 어미를 열거하면 '~모습./~행동.' 같은 정상 뜻풀이가 오탐된다. 명사는
    # '용언으로 끝나지 않을 것'만 본다(실측: 열거 방식에서 11/96 오탐).
    ends_verb = gloss.rstrip(".").endswith("다")
    if "명사" in pos and "동사" not in pos and "형용사" not in pos and ends_verb:
        issues.append("명사인데 '~다' 로 끝남(명사구여야 함)")
    if ("동사" in pos or "형용사" in pos) and not ends_verb:
        issues.append("용언인데 '~다' 로 끝나지 않음")

    # 예시문은 활용형으로 쓰이므로 표제어를 그대로 찾으면 안 된다.
    # '궁리하다' -> '궁리했다', '당돌하다' -> '당돌한'. 어간으로 대조한다.
    stem = re.sub(r"(하다|되다|다)$", "", word) or word
    # ㅂ불규칙: '호사스럽다' 의 예문은 '호사스러운' 이라 어간이 그대로 나오지 않는다.
    # -스럽다/-롭다 형용사가 이 목록에 흔해 오탐이 잦다. 받침 뗀 형태도 인정한다.
    stems = {stem}
    if stem:
        bare = _drop_coda(stem[-1])
        if bare:
            stems.add(stem[:-1] + bare)

    for key in ("example_general", "example_subject"):
        ex = _s(card.get(key))
        if not ex:
            issues.append(f"{key} 가 비어 있음")
        elif not any(st in ex for st in stems):
            issues.append(f"{key} 에 '{stem}' 가 없음")

    # 교과명 자리에 표제어를 그대로 넣어 보내는 실패가 있다(실측: subject='궁리하다').
    subj = _s(card.get("subject"))
    if subj and subj not in SUBJECTS:
        issues.append(f"교과명이 아님: '{subj}'")
    return issues


def _key(rec: dict) -> str:
    raw = f"{rec['word']}|{rec['homonym_no']}|{rec['pos']}|{rec['gloss']}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _cache_key(v: dict) -> str:
    """캐시 레코드의 키. 'key' 필드가 생기기 전에 만들어진 항목도 복원한다."""
    if v.get("key"):
        return v["key"]
    return _key({"word": v["word"], "homonym_no": v["homonym_no"],
                 "pos": v["pos"], "gloss": v["gloss_original"]})


# ---------------------------------------------------------------- 메인

def main() -> None:
    ap = argparse.ArgumentParser(description="학습자 친화적 어휘 DB 생성")
    ap.add_argument("--targets", type=int, default=DEFAULT_TARGETS, help="대상 어휘 수")
    ap.add_argument("--limit", type=int, help="이번 실행에서 새로 생성할 최대 항목 수")
    ap.add_argument("--dry-run", action="store_true", help="API 호출 없이 대상·프롬프트만")
    ap.add_argument("--model", default="gemini-2.5-flash")
    ap.add_argument("--reselect", action="store_true", help="대상 목록 다시 선정")
    ap.add_argument("--revalidate", action="store_true",
                    help="캐시 항목을 검증만 다시 (API 미호출). 검증 규칙을 고친 뒤 쓴다")
    ap.add_argument("--drop-bad", action="store_true",
                    help="--revalidate 후 문제가 남은 항목을 캐시에서 빼 재생성 대상으로 만든다")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass

    lex = build_lexicon()
    ann = Annotator(build_grade_index(lex))
    targets = select_targets(args.targets, force=args.reselect)
    print(f"대상 어휘 {len(targets)}개 (등급 3~4 · 일반어 · 사전 뜻풀이 최고등급 4 이상)")

    if args.dry_run:
        print("\n앞 20개:")
        for r in targets[:20]:
            print(f"  [{r['grade']}등급/{r['pos']}] {r['word']}"
                  f"{r['homonym_no'] or ''} (뜻풀이 최고 Lv{r['max_grade_original']})")
            print(f"      {r['gloss'][:70]}")
        print("\n프롬프트 예시:\n" + "-" * 60)
        t = targets[0]
        print(PROMPT.format(word=t["word"], pos=t["pos"], gloss=t["gloss"]))
        return

    if args.revalidate:
        cache = json.loads(CACHE_FILE.read_text(encoding="utf-8")) if CACHE_FILE.exists() else {}
        by_key = {_key(r): r for r in targets}
        changed = dropped = 0
        for k, v in list(cache.items()):
            rec = by_key.get(k)
            if not rec:
                continue
            fresh = validate(rec, {
                "easy_gloss": v["gloss_easy"],
                "example_general": v["example_general"],
                "example_subject": v["example_subject"],
                "subject": v.get("subject", ""),
            }, ann)
            if fresh != v.get("issues"):
                changed += 1
            v["issues"] = fresh
            v["max_grade_easy"] = ann.max_grade(v["gloss_easy"])
            v["gloss_easy_annotated"] = ann.annotate(v["gloss_easy"])
            if fresh and args.drop_bad:
                del cache[k]
                dropped += 1
        CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
        left = sum(1 for v in cache.values() if v.get("issues"))
        print(f"재검증 {len(cache)}개 — 판정 변경 {changed}, 제거 {dropped}, 문제 잔존 {left}")
        return

    _load_dotenv()
    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit("[ERROR] GEMINI_API_KEY 없음 (.env)")

    cache: Dict[str, dict] = (json.loads(CACHE_FILE.read_text(encoding="utf-8"))
                              if CACHE_FILE.exists() else {})
    made = reused = failed = 0

    for i, rec in enumerate(targets):
        k = _key(rec)
        if k in cache:
            reused += 1
            continue
        if args.limit and made >= args.limit:
            break

        card, issues = None, ["시작"]
        for attempt in range(MAX_REWRITES + 1):
            prompt = (PROMPT.format(word=rec["word"], pos=rec["pos"], gloss=rec["gloss"])
                      if attempt == 0 else
                      REWRITE.format(word=rec["word"], pos=rec["pos"], gloss=rec["gloss"],
                                     prev=_s(card.get("easy_gloss")),
                                     hard="; ".join(issues)))
            try:
                card = gemini_json(args.model, prompt)
            except Exception as e:
                print(f"  [{i+1}/{len(targets)}] {rec['word']} — API 실패: {str(e)[:80]}")
                time.sleep(3)
                card = None
                break
            issues = validate(rec, card, ann)
            if not issues:
                break

        if card is None:
            failed += 1
            continue

        easy = _s(card.get("easy_gloss"))
        cache[k] = {
            "key": k,
            "word": rec["word"],
            "homonym_no": rec["homonym_no"],
            "pos": rec["pos"],
            "grade": rec["grade"],
            "origin_type": rec["origin_type"],
            "source_word": rec["source_word"],
            "gloss_original": rec["gloss"],
            "gloss_easy": easy,
            "gloss_easy_annotated": ann.annotate(easy),
            "example_general": _s(card.get("example_general")),
            "example_subject": _s(card.get("example_subject")),
            "subject": _s(card.get("subject")),
            "max_grade_original": rec["max_grade_original"],
            "max_grade_easy": ann.max_grade(easy),
            "issues": issues,
        }
        made += 1
        flag = "" if not issues else "  ! " + "; ".join(issues)[:70]
        print(f"  [{i+1}/{len(targets)}] {rec['word']}: {easy}{flag}")
        if made % 10 == 0:
            CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=1),
                                  encoding="utf-8")

    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")

    order = {_key(r): i for i, r in enumerate(targets)}
    # 차단 목록은 출력에서도 거른다. 대상 목록(.vocab_targets.json)이 캐시돼 있어
    # 선정 단계 필터만으로는 이미 뽑힌 항목이 그대로 남는다.
    rows = sorted((v for k, v in cache.items()
                   if _cache_key(v) in order and v["word"] not in BLOCKLIST),
                  key=lambda v: order[_cache_key(v)])
    OUT_FILE.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")

    ok = sum(1 for r in rows if r["max_grade_easy"] <= EASY_MAX_GRADE)
    print(f"\n신규 {made} / 재사용 {reused} / 실패 {failed}")
    print(f"기록: {OUT_FILE.relative_to(ROOT)} — {len(rows)}개")
    if rows:
        print(f"쉬운 뜻풀이 Lv{EASY_MAX_GRADE} 이하: {ok}/{len(rows)} ({ok/len(rows):.1%})")


if __name__ == "__main__":
    main()
