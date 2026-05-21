from pathlib import Path
from lecture_archive.utils import (
    decode_zip_filename,
    slug_from_zip_name,
    safe_slug,
)


def test_decode_zip_filename_korean():
    # Simulate zip internal bytes: filename stored as UTF-8 in zip archive
    raw = "260429_황민호_강의자료.zip".encode("utf-8")
    result = decode_zip_filename(raw)
    assert "황민호" in result


def test_slug_from_zip_name_extracts_korean_blocks():
    assert slug_from_zip_name("260429_황민호_강의자료.zip") == "260429-hwangminho-lecture"


def test_safe_slug_strips_unicode():
    assert safe_slug("CLAUDE.md 사용법") == "claudemd-usage"
    assert safe_slug("Auto Memory") == "auto-memory"
    assert safe_slug("---test---") == "test"
