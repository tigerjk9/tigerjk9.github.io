"""스테이징된 변경에서 실제 시크릿을 찾아 커밋을 막는다.

공개 저장소라 한 번 올라가면 히스토리에 영구히 남는다(2026-09-22 실측: Gemini 키 1개와
네이버 세션 쿠키가 각각 2026-02-28·03-09부터 공개돼 있었다). 사후 제거보다 사전 차단이 싸다.

설계 원칙 둘:
1. **자리표시자를 막지 않는다.** 워크숍 교재에 `sk-ant-oat01-yyy`·`ghp_xxxxx` 같은 예시가
   정당하게 들어 있다. 그래서 길이를 실제 키 규격으로 못박고 xxx/yyy 류는 제외한다.
   한 번이라도 오탐으로 커밋을 막으면 다음부터 --no-verify로 우회하게 된다.
2. **의도적 공개 키는 통과시킨다.** `kakao_js_key`는 도메인 제한 클라이언트 키라 커밋이 정상이다.

우회가 필요하면 `git commit --no-verify`. 단 그 순간 공개된다는 뜻이다.
"""
from __future__ import annotations

import re
import subprocess
import sys

# 실제 키 규격에 맞춘 길이 고정 — 짧은 자리표시자는 걸리지 않는다
PATTERNS = [
    ("Google/Gemini API 키", re.compile(r"AIza[0-9A-Za-z_-]{35}")),
    ("Anthropic API 키", re.compile(r"sk-ant-[A-Za-z0-9]{8,}-[A-Za-z0-9_-]{24,}")),
    ("OpenAI API 키", re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{40,}")),
    ("GitHub 토큰", re.compile(r"gh[pousr]_[A-Za-z0-9]{36}")),
    ("GitHub PAT", re.compile(r"github_pat_[A-Za-z0-9_]{50,}")),
    ("Vercel 토큰", re.compile(r"vcp_[A-Za-z0-9]{40,}")),
    ("AWS 액세스 키", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Slack 토큰", re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}")),
    ("개인키 블록", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("네이버 세션 쿠키", re.compile(r"NID_(?:AUT|SES)\"?\s*[:=,]\s*\"?[A-Za-z0-9+/=_-]{32,}")),
]

# 파일명 자체가 위험한 것 — 내용을 보기 전에 막는다
BLOCKED_NAMES = [
    re.compile(r"(^|/)\.env$"),
    re.compile(r"(^|/)\.env\.(?!example$)[A-Za-z0-9_.-]+$"),
    re.compile(r"cookies?\.json$"),
    re.compile(r"(^|/)settings\.local\.json$"),
    re.compile(r"\.(pem|pfx|p12|keystore)$"),
]

# 자리표시자로 판정해 통과시킬 꼬리표
PLACEHOLDER = re.compile(r"(?i)(x{3,}|y{3,}|z{3,}|abc123|your[-_]?key|example|dummy|placeholder|<[^>]+>|\.\.\.)")


def staged_files():
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, encoding="utf-8", errors="ignore",
    ).stdout
    return [f for f in out.splitlines() if f.strip()]


def staged_content(path):
    """인덱스에 올라간 내용을 읽는다. 작업 트리가 아니라 실제 커밋될 내용이어야 한다."""
    p = subprocess.run(["git", "show", ":" + path], capture_output=True)
    if p.returncode != 0:
        return ""
    try:
        return p.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return ""  # 바이너리는 건너뛴다


def mask(s):
    return s[:6] + "..." + s[-2:] if len(s) > 12 else s[:3] + "..."


def main():
    findings = []
    for path in staged_files():
        for rx in BLOCKED_NAMES:
            if rx.search(path):
                findings.append((path, 0, "커밋 금지 파일명", path))
                break

        text = staged_content(path)
        if not text or len(text) > 2_000_000:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, rx in PATTERNS:
                for m in rx.finditer(line):
                    hit = m.group(0)
                    if PLACEHOLDER.search(hit):
                        continue  # 교재 예시 등 자리표시자
                    findings.append((path, lineno, label, mask(hit)))

    if not findings:
        return 0

    print("\n  커밋을 멈춥니다 — 시크릿으로 보이는 값이 있습니다.\n", file=sys.stderr)
    for path, lineno, label, hit in findings:
        where = "%s:%d" % (path, lineno) if lineno else path
        print("    [%s] %s" % (label, where), file=sys.stderr)
        print("        %s" % hit, file=sys.stderr)
    print("""
  이 저장소는 공개입니다. 올라가면 히스토리에서 지우기 어렵습니다.
  값을 .env로 옮기고 스테이징에서 빼세요:  git restore --staged <파일>
  자리표시자인데 걸렸다면 scripts/hooks/secret_scan.py 의 PLACEHOLDER를 넓히세요.
  정말 의도한 커밋이면:  git commit --no-verify
""", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
