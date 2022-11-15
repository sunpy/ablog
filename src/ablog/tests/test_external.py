import pytest


def read_text(path):
    """
    Support function to give backward compatibility with older sphinx (v2).
    """
    if hasattr(path, "read_text"):
        return path.read_text()
    return path.text()


@pytest.mark.sphinx("html", testroot="external")  # using roots/test-external
def test_external(app, status, warning):
    app.build()

    assert app.statuscode == 0
    assert (app.outdir / "external.html").exists()
    assert (app.outdir / "postlist.html").exists()

    html = read_text(app.outdir / "external.html")
    url = "https://www.sphinx-doc.org/en/master/"
    text = "This text will be in auto-generated post previews"
    # The page itself lacks the URL
    assert url not in html
    # It does have the text we added
    assert text in html

    html = read_text(app.outdir / "postlist.html")
    assert (
        '<a class="reference external" href="https://www.sphinx-doc.org/en/master/">External post</a></p></li>'
        in html
    )
