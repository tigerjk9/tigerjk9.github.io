#!/usr/bin/env python3
"""
yt_to_post.py — YouTube 영상을 Jekyll 블로그 포스트로 자동 변환

사용법:
  python scripts/yt_to_post.py <YouTube_URL> [옵션]

옵션:
  --date  YYYY-MM-DD   포스트 날짜 (기본값: 오늘)
  --slug  SLUG         파일명 슬러그 (기본값: 영상 제목에서 자동 생성)
  --lang  LANG         자막 우선 언어 (기본값: ko)
  --no-push            로컬 저장만 하고 git push 하지 않음
  --dry-run            _posts/ 에 저장하지 않고 터미널에 출력만
  --model  MODEL       Gemini 모델 ID (기본값: gemini-2.0-flash)

환경변수:
  GEMINI_API_KEY       Google AI Studio API 키 (필수) — .env 파일에 저장 권장
"""

from __future__ import annotations

import argparse
import io
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

# Windows 터미널 한글 깨짐 방지
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ──────────────────────────────────────────────────────────────
# 상수
# ──────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
POSTS_DIR = REPO_ROOT / "_posts"
PROMPT_TEMPLATE_PATH = SCRIPT_DIR / "yt_prompt_template.txt"
DEFAULT_MODEL = "gemini-2.0-flash"
MAX_TRANSCRIPT_CHARS = 80000  # Gemini 컨텍스트 한도 초과 방지


# ──────────────────────────────────────────────────────────────
# .env 자동 로드 (python-dotenv 없이 직접 파싱)
# ──────────────────────────────────────────────────────────────

def _load_dotenv() -> None:
    """REPO_ROOT/.env 파일을 읽어 환경변수로 설정 (이미 설정된 값은 덮어쓰지 않음)."""
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()


# ──────────────────────────────────────────────────────────────
# SSL 인증서 검증 우회 (기업 네트워크 self-signed 인증서 대응)
# ──────────────────────────────────────────────────────────────

import ssl as _ssl

_ssl._create_default_https_context = _ssl._create_unverified_context  # type: ignore[attr-defined]

try:
    import urllib3 as _urllib3  # type: ignore[import]
    _urllib3.disable_warnings(_urllib3.exceptions.InsecureRequestWarning)
except Exception:
    pass

try:
    import requests as _requests
    _requests.packages.urllib3.disable_warnings()  # type: ignore[attr-defined]
    # requests를 사용하는 youtube-transcript-api SSL 우회
    _orig_request = _requests.Session.request

    def _no_verify_request(self, method, url, **kwargs):  # type: ignore[no-untyped-def]
        kwargs.setdefault("verify", False)
        return _orig_request(self, method, url, **kwargs)

    _requests.Session.request = _no_verify_request  # type: ignore[method-assign]
except Exception:
    pass


# ──────────────────────────────────────────────────────────────
# 기존 카테고리/태그 수집 (pdf_to_post.py와 동일 로직)
# ──────────────────────────────────────────────────────────────

def get_existing_taxonomy() -> "tuple[list[str], list[str]]":
    """_posts/*.md 전체에서 기존 categories와 tags를 빈도순으로 반환."""
    cat_counter: Counter = Counter()
    tag_counter: Counter = Counter()

    for md_file in POSTS_DIR.glob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            continue
        fm = fm_match.group(1)

        cats = _parse_yaml_list(fm, "categories")
        tags = _parse_yaml_list(fm, "tags")
        cat_counter.update(cats)
        tag_counter.update(tags)

    sorted_cats = [c for c, _ in cat_counter.most_common()]
    sorted_tags = [t for t, _ in tag_counter.most_common(40)]
    return sorted_cats, sorted_tags


def _parse_yaml_list(front_matter: str, key: str) -> "list[str]":
    """YAML front matter에서 단일 라인 [a, b] 또는 멀티라인 - item 형식 파싱."""
    items: "list[str]" = []

    inline = re.search(rf"^{key}:\s*\[(.+?)\]", front_matter, re.MULTILINE)
    if inline:
        for item in inline.group(1).split(","):
            val = item.strip().strip("'\"")
            if val:
                items.append(val)
        return items

    block = re.search(rf"^{key}:\s*\n((?:\s*-\s*.+\n?)+)", front_matter, re.MULTILINE)
    if block:
        for line in block.group(1).splitlines():
            m = re.match(r"\s*-\s*(.+)", line)
            if m:
                items.append(m.group(1).strip().strip("'\""))
    return items


# ──────────────────────────────────────────────────────────────
# YouTube 비디오 ID 추출
# ──────────────────────────────────────────────────────────────

def extract_video_id(url: str) -> str:
    """YouTube URL에서 video ID 추출.

    지원 형식:
      - youtube.com/watch?v=VIDEO_ID
      - youtu.be/VIDEO_ID
      - youtube.com/shorts/VIDEO_ID
      - youtube.com/live/VIDEO_ID
    """
    parsed = urlparse(url)

    # youtu.be/VIDEO_ID
    if parsed.netloc in ("youtu.be",):
        vid = parsed.path.lstrip("/").split("/")[0]
        if vid:
            return vid

    # youtube.com/shorts/VIDEO_ID 또는 youtube.com/live/VIDEO_ID
    path_match = re.match(r"^/(shorts|live)/([A-Za-z0-9_-]{11})", parsed.path)
    if path_match:
        return path_match.group(2)

    # youtube.com/watch?v=VIDEO_ID
    qs = parse_qs(parsed.query)
    if "v" in qs and qs["v"]:
        return qs["v"][0]

    raise ValueError(f"YouTube video ID를 URL에서 추출할 수 없습니다: {url}")


# ──────────────────────────────────────────────────────────────
# 메타데이터 추출 (yt-dlp)
# ──────────────────────────────────────────────────────────────

def fetch_video_metadata(url: str) -> dict:
    """yt-dlp Python API로 영상 메타데이터를 가져옵니다.

    Returns dict with keys: title, channel, upload_date, description,
                            webpage_url, id
    """
    try:
        import yt_dlp
    except ImportError:
        raise RuntimeError(
            "yt-dlp가 설치되어 있지 않습니다.\n"
            "pip install -r scripts/requirements.txt"
        )

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
        "nocheckcertificate": True,  # 기업 네트워크 SSL 인증서 오류 우회
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            raise RuntimeError(f"영상 정보 가져오기 실패: {e}")

    return {
        "title": info.get("title", ""),
        "channel": info.get("channel") or info.get("uploader", ""),
        "upload_date": info.get("upload_date", ""),  # YYYYMMDD 형식
        "description": (info.get("description") or "")[:3000],
        "webpage_url": info.get("webpage_url", url),
        "id": info.get("id", ""),
    }


def fetch_auto_captions_via_ytdlp(url: str, lang_pref: str = "ko") -> str:
    """yt-dlp로 자동생성 자막(auto captions)을 텍스트로 추출합니다.

    youtube-transcript-api에서 자막을 못 가져왔을 때 최후 수단으로 사용.
    VTT 파일을 임시로 받아 텍스트만 추출 후 삭제.
    실패 시 빈 문자열 반환.
    """
    import tempfile
    try:
        import yt_dlp
    except ImportError:
        return ""

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                "quiet": True,
                "no_warnings": True,
                "skip_download": True,
                "writeautomaticsub": True,
                "subtitleslangs": [lang_pref, "en"],
                "subtitlesformat": "vtt",
                "nocheckcertificate": True,
                "outtmpl": str(Path(tmpdir) / "%(id)s.%(ext)s"),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # VTT 파일 찾기
            vtt_files = list(Path(tmpdir).glob("*.vtt"))
            if not vtt_files:
                return ""

            raw = vtt_files[0].read_text(encoding="utf-8", errors="ignore")

            # VTT에서 순수 텍스트만 추출 (타임코드·태그 제거, 중복 줄 제거)
            lines = []
            seen: "set[str]" = set()
            for line in raw.splitlines():
                line = line.strip()
                if not line or "-->" in line or line.startswith("WEBVTT") or line.isdigit():
                    continue
                # HTML 태그 제거
                line = re.sub(r"<[^>]+>", "", line)
                if line and line not in seen:
                    seen.add(line)
                    lines.append(line)

            text = " ".join(lines)
            if text:
                print(f"[INFO] yt-dlp 자동자막 추출 완료 ({len(text):,}자)")
            return text[:MAX_TRANSCRIPT_CHARS]
    except Exception as e:
        print(f"[WARN] yt-dlp 자동자막 추출 실패: {e}")
        return ""


def format_upload_date(upload_date: str) -> str:
    """YYYYMMDD → YYYY-MM-DD 변환. 변환 실패 시 원본 반환."""
    if len(upload_date) == 8 and upload_date.isdigit():
        return f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"
    return upload_date


# ──────────────────────────────────────────────────────────────
# 자막 추출 (youtube-transcript-api)
# ──────────────────────────────────────────────────────────────

def fetch_transcript(video_id: str, lang_pref: str = "ko") -> str:
    """youtube-transcript-api로 자막을 가져옵니다.

    시도 순서: lang_pref → en → 언어 무관
    모두 실패하면 빈 문자열 반환.

    v1.x API (인스턴스 메서드)와 v0.x API (클래스 메서드) 모두 지원.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("[WARN] youtube-transcript-api가 설치되어 있지 않습니다. 설명만으로 포스트를 생성합니다.")
        print("       pip install youtube-transcript-api")
        return ""

    def _join(chunks: list) -> str:
        return " ".join(
            (c.get("text", "") if isinstance(c, dict) else getattr(c, "text", ""))
            for c in chunks
        )

    # v1.x: 인스턴스 기반 API (api.fetch, api.list)
    try:
        api = YouTubeTranscriptApi()
        for lang in [lang_pref, "en"]:
            try:
                chunks = api.fetch(video_id, languages=[lang])
                text = _join(chunks)
                if text:
                    print(f"[INFO] 자막 가져오기 완료 ({lang}, {len(text):,}자)")
                    return text[:MAX_TRANSCRIPT_CHARS]
            except Exception:
                continue
        # 언어 무관 시도
        chunks = api.fetch(video_id)
        text = _join(chunks)
        if text:
            print(f"[INFO] 자막 가져오기 완료 (기본, {len(text):,}자)")
            return text[:MAX_TRANSCRIPT_CHARS]
    except AttributeError:
        pass  # v0.x fallback으로 이동
    except Exception as e:
        print(f"[WARN] 자막 없음 (v1.x 시도): {e}")
        return ""

    # v0.x: 클래스 메서드 API (get_transcript)
    try:
        for lang in [lang_pref, "en"]:
            try:
                chunks = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])  # type: ignore[attr-defined]
                text = _join(chunks)
                if text:
                    print(f"[INFO] 자막 가져오기 완료 ({lang}, {len(text):,}자)")
                    return text[:MAX_TRANSCRIPT_CHARS]
            except Exception:
                continue
        chunks = YouTubeTranscriptApi.get_transcript(video_id)  # type: ignore[attr-defined]
        text = _join(chunks)
        if text:
            print(f"[INFO] 자막 가져오기 완료 (기본, {len(text):,}자)")
            return text[:MAX_TRANSCRIPT_CHARS]
    except Exception as e:
        print(f"[WARN] 자막 없음: {e}")

    return ""


# ──────────────────────────────────────────────────────────────
# 프롬프트 로드
# ──────────────────────────────────────────────────────────────

def load_prompt_template(
    date_str: str,
    metadata: dict,
    transcript: str,
    categories: "list[str]",
    tags: "list[str]",
) -> str:
    """yt_prompt_template.txt 읽기 + 플레이스홀더 치환."""
    if not PROMPT_TEMPLATE_PATH.exists():
        raise RuntimeError(f"프롬프트 템플릿을 찾을 수 없습니다: {PROMPT_TEMPLATE_PATH}")
    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")

    cats_str = ", ".join(categories) if categories else "AI, 교육"
    tags_str = ", ".join(tags) if tags else "AI, 영상, 교육"
    time_str = datetime.now().strftime("%H:%M:%S")

    upload_date_formatted = format_upload_date(metadata.get("upload_date", ""))
    transcript_section = transcript if transcript else metadata.get("description", "(자막 없음)")

    template = template.replace("{DATE_PLACEHOLDER}", f"{date_str} {time_str}")
    template = template.replace("{VIDEO_TITLE}", metadata.get("title", ""))
    template = template.replace("{CHANNEL_NAME}", metadata.get("channel", ""))
    template = template.replace("{UPLOAD_DATE}", upload_date_formatted)
    template = template.replace("{VIDEO_URL}", metadata.get("webpage_url", ""))
    template = template.replace("{VIDEO_DESCRIPTION}", metadata.get("description", ""))
    template = template.replace("{TRANSCRIPT}", transcript_section)
    template = template.replace("{EXISTING_CATEGORIES}", cats_str)
    template = template.replace("{EXISTING_TAGS}", tags_str)
    return template


# ──────────────────────────────────────────────────────────────
# Gemini API
# ──────────────────────────────────────────────────────────────

def call_gemini_api(prompt: str, model: str) -> str:
    """Google Gemini SDK 호출 → 마크다운 문자열 반환 (텍스트 전용)."""
    try:
        import google.generativeai as genai
    except ImportError:
        raise RuntimeError(
            "google-generativeai 패키지가 설치되어 있지 않습니다.\n"
            "pip install -r scripts/requirements.txt"
        )

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY 환경변수가 설정되지 않았습니다.\n"
            "export GEMINI_API_KEY=AIza..."
        )

    genai.configure(api_key=api_key)

    print(f"[INFO] Gemini API 호출 중 (모델: {model}) ...")
    gemini_model = genai.GenerativeModel(model_name=model)
    response = gemini_model.generate_content(prompt)
    return _strip_code_fence(response.text)


def _strip_code_fence(text: str) -> str:
    """Gemini가 출력을 ```markdown ... ``` 또는 ``` ... ```으로 감싼 경우 벗겨냄."""
    text = text.strip()
    # ``` 또는 ```yaml, ```markdown, ```md 등 어떤 언어 태그든 제거
    stripped = re.sub(r"^```\w*\s*\n", "", text)
    if stripped != text:
        # 닫는 ``` 제거
        stripped = re.sub(r"\n```\s*$", "", stripped)
        return stripped.strip()
    return text


def _fix_date(text: str, correct_date_str: str) -> str:
    """Gemini가 front matter의 date를 임의로 변경한 경우 올바른 날짜로 복원."""
    return re.sub(
        r"^date:.*$",
        f"date: {correct_date_str} +0900",
        text,
        flags=re.MULTILINE,
    )


# ──────────────────────────────────────────────────────────────
# 포스트 생성 유틸리티
# ──────────────────────────────────────────────────────────────

def slugify(text: str, max_len: int = 60) -> str:
    """문자열 → URL-safe 슬러그 (소문자, 영숫자·하이픈만, 최대 max_len자)."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\-]", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    text = text.strip("-")
    return text[:max_len].rstrip("-")


def build_filename(date_str: str, slug: str) -> str:
    """'YYYY-MM-DD-{slug}.md' 형식 반환. 슬러그 충돌 시 타임스탬프 추가."""
    filename = f"{date_str}-{slug}.md"
    output_path = POSTS_DIR / filename
    if output_path.exists():
        ts = datetime.now().strftime("%H%M%S")
        filename = f"{date_str}-{slug}-{ts}.md"
        print(f"[WARN] 파일명 충돌 - 타임스탬프 추가: {filename}")
    return filename


def save_post(content: str, output_path: Path) -> None:
    """_posts/ 에 파일 저장."""
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] 포스트 저장 완료: {output_path}")


# ──────────────────────────────────────────────────────────────
# Git
# ──────────────────────────────────────────────────────────────

def _git(args: "list[str]", check: bool = True) -> subprocess.CompletedProcess:
    """git 명령 실행. check=True이면 실패 시 RuntimeError."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {args[0]} 실패:\n{result.stderr.strip()}")
    return result


def git_commit_and_push(file_paths: "list[Path]", commit_msg: str) -> None:
    """git add → commit → push origin main."""
    _git(["add", "--", *[str(fp) for fp in file_paths]])
    print(f"[OK] git add 완료 ({len(file_paths)}개 파일)")

    _git(["commit", "-m", commit_msg])
    print("[OK] git commit 완료")

    result = _git(["push", "origin", "main"], check=False)
    if result.returncode != 0:
        print("[WARN] git push 실패. 수동으로 push 하세요.")
        print("  → git push origin main")
        print(f"  상세: {result.stderr.strip()}")
    else:
        print("[OK] git push 완료")


# ──────────────────────────────────────────────────────────────
# Jekyll 설정 확인
# ──────────────────────────────────────────────────────────────

def ensure_timezone_config() -> bool:
    """_config.yml의 timezone이 Asia/Seoul인지 확인하고 필요하면 자동 수정.

    Returns:
        True  — 파일을 수정했음 (git commit 대상에 포함 필요)
        False — 이미 올바르게 설정되어 있음
    """
    config_path = REPO_ROOT / "_config.yml"
    if not config_path.exists():
        return False

    content = config_path.read_text(encoding="utf-8")

    if re.search(r"^timezone:\s*Asia/Seoul\s*$", content, re.MULTILINE):
        return False

    new_content = re.sub(
        r"^timezone:.*$",
        "timezone: Asia/Seoul",
        content,
        flags=re.MULTILINE,
    )

    if new_content == content:
        return False

    config_path.write_text(new_content, encoding="utf-8")
    print("[INFO] _config.yml timezone → Asia/Seoul 자동 수정 (KST 기준 포스트 노출)")
    return True


# ──────────────────────────────────────────────────────────────
# 진입점
# ──────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="YouTube 영상을 Jekyll 블로그 포스트로 자동 변환합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "예시:\n"
            "  python scripts/yt_to_post.py https://www.youtube.com/watch?v=dQw4w9WgXcQ\n"
            "  python scripts/yt_to_post.py https://youtu.be/dQw4w9WgXcQ --dry-run\n"
            "  python scripts/yt_to_post.py https://youtu.be/dQw4w9WgXcQ --no-push --lang en"
        ),
    )
    parser.add_argument("url", help="YouTube 영상 URL")
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="포스트 날짜 YYYY-MM-DD (기본값: 오늘)",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="파일명 슬러그 (기본값: 영상 제목에서 자동 생성)",
    )
    parser.add_argument(
        "--lang",
        default="ko",
        help="자막 우선 언어 코드 (기본값: ko)",
    )
    parser.add_argument(
        "--no-push",
        action="store_true",
        help="로컬 저장만 하고 git push 하지 않음",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="_posts/ 에 저장하지 않고 터미널에 출력만",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini 모델 ID (기본값: {DEFAULT_MODEL})",
    )
    args = parser.parse_args()

    # ── 환경변수 확인 ──
    if not os.environ.get("GEMINI_API_KEY"):
        print(
            "[ERROR] GEMINI_API_KEY 환경변수가 설정되지 않았습니다.\n"
            "  export GEMINI_API_KEY=AIza..."
        )
        sys.exit(1)

    # ── video ID 추출 ──
    try:
        video_id = extract_video_id(args.url)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    print(f"[INFO] Video ID: {video_id}")

    # ── timezone 설정 확인 및 자동 수정 ──
    config_modified = ensure_timezone_config()

    # ── 메타데이터 가져오기 ──
    print(f"[INFO] 영상 메타데이터 가져오는 중: {args.url}")
    try:
        metadata = fetch_video_metadata(args.url)
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    print(f"[INFO] 제목: {metadata['title']}")
    print(f"[INFO] 채널: {metadata['channel']}")
    print(f"[INFO] 업로드 날짜: {format_upload_date(metadata['upload_date'])}")

    # ── 슬러그 결정 ──
    if args.slug:
        slug = args.slug
    else:
        slug = slugify(metadata["title"])
        if not slug:
            slug = f"yt-{video_id}"
    print(f"[INFO] 슬러그: {slug}")

    # ── 자막 가져오기 ──
    print(f"[INFO] 자막 가져오는 중 (우선 언어: {args.lang}) ...")
    transcript = fetch_transcript(video_id, lang_pref=args.lang)
    if not transcript:
        print("[INFO] youtube-transcript-api 자막 없음 - yt-dlp 자동자막 시도 중...")
        transcript = fetch_auto_captions_via_ytdlp(args.url, lang_pref=args.lang)
    if not transcript:
        print("[INFO] 자막 없음 - 영상 설명(description)으로 포스트를 생성합니다.")

    # ── 기존 카테고리/태그 수집 ──
    print("[INFO] 기존 카테고리/태그 수집 중...")
    existing_cats, existing_tags = get_existing_taxonomy()
    print(f"[INFO] 기존 카테고리 {len(existing_cats)}개, 태그 {len(existing_tags)}개 확인")

    # ── 프롬프트 로드 ──
    try:
        prompt = load_prompt_template(
            args.date, metadata, transcript, existing_cats, existing_tags
        )
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    # ── Gemini API 호출 ──
    try:
        markdown_content = call_gemini_api(prompt, args.model)
    except RuntimeError as e:
        print(f"[ERROR] Gemini API 호출 실패: {e}")
        sys.exit(1)

    # Gemini가 date를 임의로 바꾸는 경우 복원
    correct_date = f"{args.date} {datetime.now().strftime('%H:%M:%S')}"
    markdown_content = _fix_date(markdown_content, correct_date)

    print("[INFO] 포스트 생성 완료")

    # ── dry-run: 출력만 ──
    if args.dry_run:
        print("\n" + "=" * 60)
        print(markdown_content)
        print("=" * 60)
        print("\n[dry-run] 파일 저장 및 git push를 건너뜁니다.")
        return

    # ── 파일 저장 ──
    filename = build_filename(args.date, slug)
    output_path = POSTS_DIR / filename
    save_post(markdown_content, output_path)

    # ── git commit + push ──
    if not args.no_push:
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', markdown_content, re.MULTILINE)
        short_title = title_match.group(1)[:50] if title_match else metadata["title"][:50]
        commit_msg = (
            f"Add: {short_title}\n\n"
            f"Auto-generated by yt_to_post.py\n"
            f"Source: {metadata['webpage_url']}"
        )
        all_files = [output_path]
        if config_modified:
            all_files.append(REPO_ROOT / "_config.yml")
        try:
            git_commit_and_push(all_files, commit_msg)
        except RuntimeError as e:
            print(f"[ERROR] git 오류: {e}")
    else:
        print("[INFO] --no-push 옵션으로 git push를 건너뜁니다.")
        print(
            f"  수동 push: git add \"{output_path}\" && "
            f"git commit -m 'Add: {slug}' && git push origin main"
        )

    print(f"\n완료! 생성된 포스트: {output_path}")


if __name__ == "__main__":
    main()
