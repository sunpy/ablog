import pytest


def read_text(path):
    """
    Support function to give backward compatibility with older sphinx (v2).
    """
    if hasattr(path, "read_text"):
        return path.read_text()
    return path.text()


@pytest.mark.sphinx("html", testroot="postlist")  # using roots/test-postlist
def test_postlist(app, status, warning):
    app.build()

    assert app.statuscode == 0
    assert (app.outdir / "postlist.html").exists()

    html = read_text(app.outdir / "postlist.html")
    assert '<ul class="postlist-style-none postlist simple">' in html
    assert (
        '<li class="ablog-post"><p class="ablog-post-title">01 December - <a class="reference internal" href="post.html">post</a></p></li>'
        in html
    )


@pytest.mark.sphinx("html", testroot="postlist", confoverrides={"post_date_format_short": "%Y-%m-%d"})
def test_postlist_date_format_conf(app, status, warning):
    app.build()

    assert app.statuscode == 0

    html = read_text(app.outdir / "postlist.html")
    assert (
        '<li class="ablog-post"><p class="ablog-post-title">2020-12-01 - <a class="reference internal" href="post.html">post</a></p></li>'
        in html
    )
