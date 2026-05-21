from pathlib import Path
from lecture_archive.parse_slides import parse_html

FIX = Path(__file__).parent / "fixtures" / "sample_slides.html"


def test_parse_html_counts_sections():
    slides = parse_html(FIX.read_text(encoding="utf-8"))
    assert len(slides) == 5


def test_parse_html_extracts_metadata():
    slides = parse_html(FIX.read_text(encoding="utf-8"))
    s2 = slides[1]
    assert s2["n"] == 2
    assert s2["block"] == "claudemd"
    assert s2["data_time"] == "1"
    assert s2["title"] == "CLAUDE.md 개념"
    assert s2["layout"] == "layout-bullets"


def test_parse_html_extracts_code_blocks():
    slides = parse_html(FIX.read_text(encoding="utf-8"))
    s2 = slides[1]
    assert len(s2["code_blocks"]) == 1
    assert s2["code_blocks"][0]["lang"] == "powershell"
    assert "claude" in s2["code_blocks"][0]["code"]


def test_parse_html_extracts_text():
    slides = parse_html(FIX.read_text(encoding="utf-8"))
    s4 = slides[3]
    assert "자연어로 정정 누적" in s4["text"]
