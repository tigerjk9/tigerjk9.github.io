"""공용 헬퍼 — zip 디코드·slug·경로."""
import re
import unicodedata
from typing import Union


KOREAN_TRANSLIT = {
    "황민호": "hwangminho",
    "강의자료": "lecture",
    "사용법": "usage",
}


def decode_zip_filename(raw: Union[bytes, str]) -> str:
    """zip 내 한글 파일명을 디코드.

    우선순위:
    1. str이면 그대로 반환
    2. UTF-8로 직접 디코드 시도 (zip flag 0x800 또는 UTF-8 저장 파일)
    3. cp437 mojibake → utf-8 복원 시도 (레거시 zip)
    4. 최후: replace 모드로 utf-8 디코드
    """
    if isinstance(raw, str):
        return raw
    # Try UTF-8 first (most modern zips store filenames as UTF-8)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    # Try cp437 mojibake reversal (legacy zip: bytes stored as cp437-encoded UTF-8)
    try:
        return raw.decode("cp437").encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass
    return raw.decode("utf-8", errors="replace")


def slug_from_zip_name(filename: str) -> str:
    """zip 파일명에서 영문 slug 추출. 한글 블록은 transliteration."""
    base = re.sub(r"\.[zZ][iI][pP]$", "", filename)
    parts = re.split(r"[_\-\s]+", base)
    out = []
    for p in parts:
        if not p:
            continue
        if re.match(r"^[A-Za-z0-9]+$", p):
            out.append(p.lower())
        elif p in KOREAN_TRANSLIT:
            out.append(KOREAN_TRANSLIT[p])
        else:
            ascii_form = unicodedata.normalize("NFKD", p).encode("ascii", "ignore").decode("ascii")
            if ascii_form:
                out.append(ascii_form.lower())
    return "-".join(out)


def safe_slug(text: str) -> str:
    """페이지 slug — 영문·숫자·하이픈만."""
    text = text.lower()
    for k, v in KOREAN_TRANSLIT.items():
        text = text.replace(k.lower(), v)
    # Remove dots and other punctuation that should not become separators
    text = re.sub(r"\.", "", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")
