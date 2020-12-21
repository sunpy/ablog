import pytest


@pytest.mark.sphinx("html", testroot="postlist")  # using roots/test-postlist
def test_postlist(app, status, warning):
    app.build()

    assert app.statuscode == 0
    assert (app.outdir / "postlist.html").exists()

    html = (app.outdir / "postlist.html").read_text()
    assert '<ul class="postlist-style-none postlist simple">' in html
    assert (
        "<li><p>01 December - " '<a class="reference internal" href="post.html">post</a>' "</p></li>"
    ) in html


@pytest.mark.sphinx("html", testroot="postlist", confoverrides={"post_date_format_short": "%Y-%m-%d"})
def test_postlist_date_format_conf(app, status, warning):
    app.build()

    assert app.statuscode == 0

    html = (app.outdir / "postlist.html").read_text()
    assert (
        "<li><p>2020-12-01 - " '<a class="reference internal" href="post.html">post</a>' "</p></li>"
    ) in html
