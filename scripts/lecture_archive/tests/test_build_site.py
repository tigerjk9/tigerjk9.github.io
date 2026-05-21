from pathlib import Path
import yaml
from lecture_archive.build_site import (
    write_feature_page, append_lecture_index,
)


def test_write_feature_page(tmp_path):
    lect_dir = tmp_path / "_lectures" / "kist-claude-code"
    lect_dir.mkdir(parents=True)
    feature = {
        "id": "F-035", "name": "CLAUDE.md", "slug": "claudemd",
        "track": "basic", "def": "프로젝트 컨텍스트 주입",
        "actions": ["a", "b", "c"], "usage_code": "claude\n/init",
        "usage_lang": "powershell", "rationale": "테스트",
        "related_slides": [{"n": 8, "title": "S8", "png": "/x.webp", "text": "..."}],
        "ment_excerpt": "강사 멘트", "lab_excerpt": "",
        "source_urls": ["https://docs.anthropic.com/claude-code"],
    }
    write_feature_page(lect_dir, "kist-claude-code", feature, prev_slug=None, next_slug="auto-memory")
    out = lect_dir / "claudemd.md"
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "F-035" in content
    assert "permalink: /lectures/kist-claude-code/claudemd/" in content
    assert "프로젝트 컨텍스트 주입" in content


def test_append_lecture_index_creates_new(tmp_path):
    data_file = tmp_path / "lectures.yml"
    data_file.write_text("[]", encoding="utf-8")
    block = {"slug": "kist-claude-code", "title": "Test", "feature_count": 22}
    append_lecture_index(data_file, block)
    loaded = yaml.safe_load(data_file.read_text(encoding="utf-8"))
    assert len(loaded) == 1
    assert loaded[0]["slug"] == "kist-claude-code"


def test_append_lecture_index_replaces_existing(tmp_path):
    data_file = tmp_path / "lectures.yml"
    yaml.dump([{"slug": "kist-claude-code", "title": "Old"}], data_file.open("w", encoding="utf-8"))
    block = {"slug": "kist-claude-code", "title": "New", "feature_count": 22}
    append_lecture_index(data_file, block)
    loaded = yaml.safe_load(data_file.read_text(encoding="utf-8"))
    assert len(loaded) == 1
    assert loaded[0]["title"] == "New"
