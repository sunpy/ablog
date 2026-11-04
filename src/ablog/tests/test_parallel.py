import pytest


@pytest.mark.sphinx("html", testroot="parallel", parallel=2)  # using roots/test-parallel
def test_parallel_read(app, status, warning):
    app.build()
    assert app.statuscode == 0

    html = (app.outdir / "postlist.html").read_text(encoding="utf-8")
    for i in range(1, 5):
        assert f"post {i}" in html

    # merged posts must not keep the worker's env alive
    for posts in app.env.ablog_posts.values():
        for post in posts:
            assert post["doctree"].document.settings.env is app.env
