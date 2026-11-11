import pytest

from ablog.commands import ablog_post


def test_post_creates_new_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    ablog_post("my-post.rst", title="Hello")
    content = (tmp_path / "my-post.rst").read_text(encoding="utf-8")
    assert "Hello" in content


def test_post_existing_file_is_not_silently_skipped(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    existing = tmp_path / "my-post.rst"
    existing.write_text("existing content", encoding="utf-8")
    with pytest.raises(SystemExit) as excinfo:
        ablog_post("my-post.rst", title="Again")
    assert excinfo.value.code != 0
    assert existing.read_text(encoding="utf-8") == "existing content"
