from pathlib import Path
from subprocess import run
import sys
import pytest


@pytest.mark.xfail("win" in sys.platform, reason="Passes on Windows")
def test_not_safe_for_parallel_read(rootdir: Path, tmp_path: Path):
    """
    Ablog is NOT safe for parallel read.

    In such case, it doesn't collect any posts.
    """
    # https://github.com/sunpy/ablog/issues/297
    # Very ugly hack to change the parallel_read_safe value to True
    good_read_safe = '"parallel_read_safe": False'
    bad_read_safe = '"parallel_read_safe": True'
    init_py_path = Path(__file__).parent.parent / "__init__.py"
    assert good_read_safe in init_py_path.read_text(encoding="utf-8")
    original_init_py = init_py_path.read_text(encoding="utf-8")
    bad_init_py = original_init_py.replace(good_read_safe, bad_read_safe)
    init_py_path.write_text(bad_init_py, encoding="utf-8")
    try:
        # liborjelinek: I wasn't able to demonstrate the issue with the `parallel` argument to the `sphinx` fixture
        # @pytest.mark.sphinx("html", testroot="parallel", parallel=2)
        # therefore running sphinx-build externally
        indir = rootdir / "test-parallel"
        run(["sphinx-build", "-b", "html", indir.as_posix(), tmp_path.as_posix(), "-j", "auto"], check=True)

        # And posts are not collected by Ablog...
        html = (tmp_path / "postlist.html").read_text(encoding="utf-8")
        assert "post 1" not in html
        assert "post 2" not in html
        assert "post 3" not in html
        assert "post 4" not in html
    finally:
        init_py_path.write_text(original_init_py, encoding="utf-8")
