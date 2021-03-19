import lxml
import pytest


@pytest.mark.sphinx("html", testroot="build")  # using roots/test-build
def test_build(app, status, warning):
    app.build()

    assert app.statuscode == 0
    assert (app.outdir / "index.html").exists()
    assert (app.outdir / "blog/archive.html").exists()
    assert (app.outdir / "post.html").exists()


@pytest.mark.sphinx("html", testroot="build")  # using roots/test-build
def test_feed(app, status, warning):
    """
    Atom syndication feeds are built correctly.
    """
    app.build()
    assert app.statuscode == 0, "Test ABlog project did not build successfully"

    feed_path = app.outdir / "blog/atom.xml"
    assert (feed_path).exists(), "Atom feed was not built"

    with feed_path.open() as feed_opened:
        feed_tree = lxml.etree.parse(feed_opened)
    entries = feed_tree.findall("{http://www.w3.org/2005/Atom}entry")
    assert len(entries) == 1, "Wrong number of Atom feed entries"

    entry = entries[0]
    title = entry.find("{http://www.w3.org/2005/Atom}title")
    assert title.text == "Foo Post Title", "Wrong Atom feed entry title"
    content = entry.find("{http://www.w3.org/2005/Atom}content")
    assert "Foo post content." in content.text, "Wrong Atom feed entry content"
