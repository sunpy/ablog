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
    assert app.statuscode == 0

    feed_path = app.outdir / "blog/atom.xml"
    assert (feed_path).exists()

    with feed_path.open() as feed_opened:
        feed_tree = lxml.etree.parse(feed_opened)
    entries = feed_tree.findall("{http://www.w3.org/2005/Atom}entry")
    assert len(entries) == 2

    entry = entries[0]
    title = entry.find("{http://www.w3.org/2005/Atom}title")
    assert title.text == "Foo Post Title"
    summary = entry.find("{http://www.w3.org/2005/Atom}summary")
    assert summary.text == "Foo post description with link."
    categories = entry.findall("{http://www.w3.org/2005/Atom}category")
    assert len(categories) == 2
    assert categories[0].attrib["label"] == "BarTag"
    assert categories[0].attrib["term"] == "BarTag"
    assert categories[1].attrib["label"] == "Foo Tag"
    assert categories[1].attrib["term"] == "FooTag"
    content = entry.find("{http://www.w3.org/2005/Atom}content")
    assert "Foo post content." in content.text

    empty_entry = entries[1]
    title = empty_entry.find("{http://www.w3.org/2005/Atom}title")
    assert title.text == "Foo Empty Post"
    summary = empty_entry.find("{http://www.w3.org/2005/Atom}summary")
    assert summary is None
    categories = empty_entry.findall("{http://www.w3.org/2005/Atom}category")
    assert len(categories) == 0
    content = empty_entry.find("{http://www.w3.org/2005/Atom}content")
    assert 'id="foo-empty-post"' in content.text

    social_path = app.outdir / "blog/social.xml"
    assert (social_path).exists()

    with social_path.open() as social_opened:
        social_tree = lxml.etree.parse(social_opened)
    social_entries = social_tree.findall("{http://www.w3.org/2005/Atom}entry")
    assert len(social_entries) == len(entries)

    social_entry = social_entries[0]
    title = social_entry.find("{http://www.w3.org/2005/Atom}title")
    assert title.text == "Foo Post Title"
    summary = social_entry.find("{http://www.w3.org/2005/Atom}summary")
    assert summary.text == "Foo post description with link."
    categories = social_entry.findall("{http://www.w3.org/2005/Atom}category")
    assert len(categories) == 2
    assert categories[0].attrib["label"] == "BarTag"
    assert categories[1].attrib["label"] == "Foo Tag"
    content = social_entry.find("{http://www.w3.org/2005/Atom}content")
    assert "Foo Post Title" in content.text
