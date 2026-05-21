from pathlib import Path
from lecture_archive.extract_notes import parse_notes, slide_to_feature_map

FIX = Path(__file__).parent / "fixtures" / "sample_instructor_notes.md"


def test_parse_notes_extracts_sections():
    sections = parse_notes(FIX.read_text(encoding="utf-8"))
    assert len(sections) == 3
    titles = [s["feature_name"] for s in sections]
    assert "도입" in titles
    assert "CLAUDE.md" in titles
    assert "Auto Memory" in titles


def test_parse_notes_extracts_slide_ranges():
    sections = parse_notes(FIX.read_text(encoding="utf-8"))
    claudemd = next(s for s in sections if s["feature_name"] == "CLAUDE.md")
    assert claudemd["slide_start"] == 7
    assert claudemd["slide_end"] == 10
    assert claudemd["duration_min"] == 5


def test_parse_notes_extracts_per_slide_notes():
    sections = parse_notes(FIX.read_text(encoding="utf-8"))
    claudemd = next(s for s in sections if s["feature_name"] == "CLAUDE.md")
    s8 = claudemd["slides"][0]
    assert s8["n"] == 8
    assert "첫 기능 CLAUDE.md입니다" in s8["ment"]
    assert "@import 한 줄" in s8["qa"]


def test_slide_to_feature_map():
    sections = parse_notes(FIX.read_text(encoding="utf-8"))
    m = slide_to_feature_map(sections)
    assert m[1] == "도입"
    assert m[7] == "CLAUDE.md"
    assert m[8] == "CLAUDE.md"
    assert m[10] == "CLAUDE.md"
    assert m[11] == "Auto Memory"
    assert m[13] == "Auto Memory"
