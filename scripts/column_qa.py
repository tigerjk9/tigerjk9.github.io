# -*- coding: utf-8 -*-
"""/column 칼럼 포스트 기계 검증기.

사용: py scripts/column_qa.py _posts/YYYY-MM-DD-slug.md [...]

FAIL(치명, exit 1): S1 금지 표현, 존칭 어미(따옴표 인용 밖), 콜론 헤딩,
  상투구, 로컬 경로 잔존, YAML 오류, 칼럼 태그/permalink 누락,
  제목 콜론·대시 부제, 출처 섹션이 맨 끝이 아님, 표 빈 셀, permalink 중복.
WARN(주의, exit 0): 볼드 남용, '것이다' 반복, '아니라' 대구 과용,
  문두 접속사 밀도, 명사형 종결, 의문형 제목 물음표 누락.

주의: 존칭 검사는 큰따옴표 인용(" " · " ") 안을 제외한다 — 취재원 발언
인용은 존칭일 수 있다. 작은따옴표는 용어 강조에 쓰이므로 제외하지 않는다.
"""
from __future__ import annotations

import glob
import io
import re
import sys

import yaml

S1_PATTERNS = [
    (r"통해", "S1 '~을/를 통해(서)'"),
    (r"[을를] 넘어", "S1 '~을/를 넘어'"),
    (r"결론적으로", "S1 '결론적으로'"),
    (r"시사하는 바가 크다", "S1 '시사하는 바가 크다'"),
    (r"혁신적", "S1 '혁신적'"),
    (r"[\U0001F300-\U0001FAFF☀-➿]", "S1 이모지"),
]

CLICHES = [
    "바야흐로", "우리 사회는", "에 다름 아니다", "필자는",
    "아무리 강조해도 지나치지", "선택이 아닌 필수",
]

HONORIFIC = re.compile(r"(합니다|됩니다|입니다|하세요|드립니다|해요|까요)[.!?\s]")
STRONG_Q_END = re.compile(r"(는가|은가|운가|인가|던가|한가|까|까요|나요|냐|느냐)$")


def strip_quotes(text: str) -> str:
    """큰따옴표 인용 스팬 제거 (존칭 검사용)."""
    return re.sub(r"[\"“][^\"“”]*[\"”]", "〇", text)


def check(path: str, all_permalinks: "dict[str, list[str]]") -> "tuple[list[str], list[str]]":
    fails: "list[str]" = []
    warns: "list[str]" = []
    text = io.open(path, encoding="utf-8").read()
    lines = text.splitlines()

    # --- front matter ---
    parts = text.split("---")
    fm = None
    if len(parts) < 3:
        fails.append("front matter 없음")
    else:
        try:
            fm = yaml.safe_load(parts[1])
        except Exception as e:
            fails.append("YAML 오류: %r" % e)
    title = (fm or {}).get("title", "") or ""
    tags = (fm or {}).get("tags") or []
    permalink = (fm or {}).get("permalink", "") or ""
    if fm is not None:
        if "칼럼" not in tags:
            fails.append("tags에 '칼럼' 없음")
        if not permalink.startswith("/post/"):
            fails.append("permalink가 /post/<슬러그>/ 형식이 아님")
        elif len(all_permalinks.get(permalink, [])) > 1:
            fails.append("permalink 중복: %s (%s)" % (permalink, ", ".join(all_permalinks[permalink])))
        if ": " in title:
            fails.append("제목에 콜론 부제: %s" % title)
        if " — " in title or " – " in title:
            fails.append("제목에 대시 부제: %s" % title)
        core = title.split("?")[0] if "?" in title else title
        if "?" not in title and STRONG_Q_END.search(core.strip()):
            warns.append("의문형 제목에 물음표 없음: %s" % title)

    body_at = text.find("---", text.find("---") + 3) + 3
    body = text[body_at:]

    # 잔류 코드펜스 (front matter 직후 5줄)
    for l in body.lstrip("\n").splitlines()[:5]:
        if l.strip().startswith("```"):
            fails.append("front matter 직후 잔류 코드펜스")
            break

    # --- 본문 라인 검사 ---
    for i, l in enumerate(lines, 1):
        if re.match(r"^#{2,3} .*: ", l) or re.match(r"^#{2,3} [^:]*[^ ]:$", l):
            fails.append("L%d 콜론 헤딩: %s" % (i, l[:60]))
        if re.match(r"^\|[^|]+\|\s*\|\s*\|?\s*$", l) and "---" not in l:
            fails.append("L%d 표 빈 셀 행: %s" % (i, l[:50]))
        if l.strip().startswith("<figure>") and i > 1 and lines[i - 2].strip() != "":
            fails.append("L%d figure 앞 빈 줄 없음" % i)

    if lines and max(len(l) for l in lines) > 3000:
        fails.append("3000자 초과 줄 존재 (표 구분선 폭발 의심)")

    # --- S1 / 상투구 / 로컬 경로 ---
    for pat, label in S1_PATTERNS:
        for m in re.finditer(pat, body):
            ln = body[: m.start()].count("\n") + 1
            fails.append("본문 L%d %s: …%s…" % (ln, label, body[max(0, m.start() - 15): m.end() + 15].replace("\n", " ")))
    for c in CLICHES:
        if c in body:
            fails.append("상투구 '%s'" % c)
    if re.search(r"C:[/\\]Users|scratchpad|AppData", body):
        fails.append("로컬 경로 잔존")

    # --- 존칭 (큰따옴표 인용 제외) ---
    for i, l in enumerate(body.splitlines(), 1):
        if l.startswith(">"):
            continue
        m = HONORIFIC.search(strip_quotes(l) + " ")
        if m:
            fails.append("본문 L%d 존칭 '%s': %s" % (i, m.group(1), l.strip()[:60]))

    # --- 출처 위치 ---
    idx = body.rfind("## 출처")
    if idx != -1:
        for l in body[idx:].splitlines()[1:]:
            if l.startswith("## "):
                fails.append("출처 뒤에 다른 섹션 존재")
                break

    # --- WARN: 리듬·남용 지표 ---
    bold = len(re.findall(r"\*\*[^*]+\*\*", body))
    if bold > 2:
        warns.append("볼드 %d회 (칼럼 기준 0~2회)" % bold)
    n = len(re.findall(r"것이다", body))
    if n > 3:
        warns.append("'것이다' %d회 (3회 이하 권장)" % n)
    n = len(re.findall(r" 아니라 |가 아니다|은 아니다|는 아니다", body))
    if n > 4:
        warns.append("'아니라/아니다' 대구 %d회 (4회 이하 권장)" % n)
    n = len(re.findall(r"(?m)^(또한|따라서|즉|그러나|하지만|그런데)[, ]", body))
    if n > 5:
        warns.append("문두 접속사 %d회 (5회 이하 권장)" % n)
    n = len(re.findall(r"[가-힣](함|임|됨)[.,]", body))
    if n > 2:
        warns.append("명사형 종결 %d회 (2회 이하 권장)" % n)

    return fails, warns


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    targets = sys.argv[1:]
    if not targets:
        print("사용법: py scripts/column_qa.py _posts/<파일>.md [...]")
        sys.exit(2)

    # permalink 중복 전수 스캔
    all_permalinks: "dict[str, list[str]]" = {}
    for p in glob.glob("_posts/*.md"):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        m = re.search(r"^permalink:\s*(\S+)", t, re.M)
        if m:
            all_permalinks.setdefault(m.group(1).strip('"'), []).append(p)

    any_fail = False
    for path in targets:
        fails, warns = check(path, all_permalinks)
        print("=" * 66)
        print(path)
        for f in fails:
            print("  [FAIL]", f)
        for w in warns:
            print("  [WARN]", w)
        if not fails and not warns:
            print("  [OK] 이슈 없음")
        elif not fails:
            print("  [PASS] 치명 이슈 없음 (경고 %d건은 판단 후 처리)" % len(warns))
        any_fail = any_fail or bool(fails)

    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
