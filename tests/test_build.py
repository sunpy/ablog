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
    assert len(entries) == 2, "Wrong number of Atom feed entries"

    entry = entries[0]
    title = entry.find("{http://www.w3.org/2005/Atom}title")
    assert title.text == "Foo Post Title", "Wrong Atom feed entry title"
    summary = entry.find("{http://www.w3.org/2005/Atom}summary")
    assert summary.text == "Foo post description with link.", "Wrong Atom feed entry summary"
    categories = entry.findall("{http://www.w3.org/2005/Atom}category")
    assert len(categories) == 2, "Wrong number of Atom feed categories"
    assert categories[0].attrib["label"] == "Foo Tag", "Wrong Atom feed first category"
    assert categories[0].attrib["term"] == "FooTag", "Wrong Atom feed first category"
    assert categories[1].attrib["label"] == "BarTag", "Wrong Atom feed second category"
    assert categories[1].attrib["term"] == "BarTag", "Wrong Atom feed second category"
    content = entry.find("{http://www.w3.org/2005/Atom}content")
    assert "Foo post content." in content.text, "Wrong Atom feed entry content"

    empty_entry = entries[1]
    title = empty_entry.find("{http://www.w3.org/2005/Atom}title")
    assert title.text == "Foo Empty Post", "Wrong Atom feed empty entry title"
    summary = empty_entry.find("{http://www.w3.org/2005/Atom}summary")
    assert summary is None, "Atom feed empty entry contains optional summary element"
    categories = empty_entry.findall("{http://www.w3.org/2005/Atom}category")
    assert len(categories) == 0, "Atom categories rendered for empty post"
    content = empty_entry.find("{http://www.w3.org/2005/Atom}content")
    assert 'id="foo-empty-post"' in content.text, "Atom feed empty entry missing post ID"

    social_path = app.outdir / "blog/social.xml"
    assert (social_path).exists(), "Social media feed was not built"

    with social_path.open() as social_opened:
        social_tree = lxml.etree.parse(social_opened)
    social_entries = social_tree.findall("{http://www.w3.org/2005/Atom}entry")
    assert len(social_entries) == len(entries), "Wrong number of Social media feed entries"

    social_entry = social_entries[0]
    title = social_entry.find("{http://www.w3.org/2005/Atom}title")
    assert title.text == "Foo Post Title", "Wrong Social media feed entry title"
    summary = social_entry.find("{http://www.w3.org/2005/Atom}summary")
    assert summary.text == "Foo post description with link.", "Wrong Social media feed entry summary"
    categories = social_entry.findall("{http://www.w3.org/2005/Atom}category")
    assert len(categories) == 2, "Wrong number of Social media feed categories"
    assert categories[0].attrib["label"] == "Foo Tag", "Wrong Social media feed first category"
    assert categories[1].attrib["label"] == "BarTag", "Wrong Social media feed second category"
    content = social_entry.find("{http://www.w3.org/2005/Atom}content")
    assert "Foo Post Title #FooTag #BarTag" in content.text, "Wrong Social media feed entry content"
