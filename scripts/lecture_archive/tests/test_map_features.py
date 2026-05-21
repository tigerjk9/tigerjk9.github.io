from lecture_archive.map_features import (
    map_strict, map_heading, decide_mapping,
)


def test_map_strict_uses_notes_range():
    slide_to_feature = {7: "CLAUDE.md", 8: "CLAUDE.md", 11: "Auto Memory"}
    slides = [{"n": 7, "title": "CLAUDE.md"}, {"n": 8, "title": "CLAUDE.md 개념"}, {"n": 99, "title": "기타"}]
    result = map_strict(slides, slide_to_feature)
    assert result[7] == ("CLAUDE.md", "strict")
    assert result[8] == ("CLAUDE.md", "strict")
    assert 99 not in result  # strict 매핑 안 됨


def test_map_heading_fuzzy_matches():
    catalog = [
        {"id": "F-035", "name": "CLAUDE.md", "name_ko": "CLAUDE.md (프로젝트 컨텍스트)"},
        {"id": "F-036", "name": "Auto Memory", "name_ko": "Auto Memory (자동 메모리)"},
    ]
    unmapped = [{"n": 99, "title": "CLAUDE.md 응용"}]
    result = map_heading(unmapped, catalog)
    assert result[99] == ("CLAUDE.md", "heading")


def test_decide_mapping_prefers_strict():
    strict = {7: ("CLAUDE.md", "strict")}
    heading = {7: ("Other", "heading")}
    llm = {7: ("Yet Another", "llm")}
    final = decide_mapping(strict, heading, llm)
    assert final[7] == ("CLAUDE.md", "strict")


def test_decide_mapping_falls_through():
    strict = {}
    heading = {99: ("Heuristic", "heading")}
    llm = {99: ("LLM Guess", "llm")}
    final = decide_mapping(strict, heading, llm)
    assert final[99] == ("Heuristic", "heading")
