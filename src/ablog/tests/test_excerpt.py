import pytest


def read_text(path):
    """
    Support function to give backward compatibility with older sphinx (v2).
    """
    if hasattr(path, "read_text"):
        return path.read_text()
    return path.text()


# ``CheckFrontMatter`` reaches the Sphinx application through the deprecated
# ``SphinxTransform.app`` property. That is orthogonal to the excerpt handling
# exercised here, and the suite turns warnings into errors, so it is filtered
# rather than worked around.
pytestmark = pytest.mark.filterwarnings("ignore:'ablog.post.CheckFrontMatter.app' is deprecated")


@pytest.mark.sphinx("html", testroot="excerpt")  # using roots/test-excerpt
def test_excerpt_zero_in_front_matter_is_respected(app, status, warning):
    """
    An ``:excerpt: 0`` given as page front-matter must suppress the excerpt.

    Regression test: ``0`` is falsy, so it used to be overridden by
    ``post_auto_excerpt`` and the first paragraph leaked into the postlist.
    """
    app.build()

    assert app.statuscode == 0
    html = read_text(app.outdir / "postlist.html")

    assert "ZEROFIRSTPARA" not in html
    assert "ZEROSECONDPARA" not in html


@pytest.mark.sphinx("html", testroot="excerpt")
def test_excerpt_count_in_front_matter_is_respected(app, status, warning):
    """
    A non-zero ``:excerpt:`` still yields that many paragraphs.
    """
    app.build()

    assert app.statuscode == 0
    html = read_text(app.outdir / "postlist.html")

    assert "ONEFIRSTPARA" in html
    assert "ONESECONDPARA" not in html


@pytest.mark.sphinx("html", testroot="excerpt")
def test_excerpt_absent_falls_back_to_auto_excerpt(app, status, warning):
    """
    With no ``:excerpt:`` at all, ``post_auto_excerpt`` still applies.
    """
    app.build()

    assert app.statuscode == 0
    html = read_text(app.outdir / "postlist.html")

    assert "DEFAULTFIRSTPARA" in html
    assert "DEFAULTSECONDPARA" not in html


@pytest.mark.sphinx("html", testroot="excerpt", confoverrides={"post_auto_excerpt": 2})
def test_excerpt_zero_overrides_post_auto_excerpt(app, status, warning):
    """
    An explicit ``0`` wins over a non-default ``post_auto_excerpt``.
    """
    app.build()

    assert app.statuscode == 0
    html = read_text(app.outdir / "postlist.html")

    assert "ZEROFIRSTPARA" not in html
    assert "DEFAULTSECONDPARA" in html
