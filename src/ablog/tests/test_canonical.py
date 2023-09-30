import pytest

def read_text(path):
    """
    Support function to give backward compatibility with older sphinx (v2).
    """
    if hasattr(path, "read_text"):
        return path.read_text()
    return path.text()

@pytest.mark.sphinx("html", testroot="canonical")  # using roots/test-canonical
def test_canonical(app, status, warning):
    app.build()

    assert app.statuscode == 0
    assert (app.outdir / "post.html").exists()
    assert (app.outdir / "canonical.html").exists()
    
    html = read_text(app.outdir / "post.html")
    assert '<link rel="canonical" href="https://blog.example.com/post.html" />' in html

    html = read_text(app.outdir / "canonical.html")
    assert '<link rel="canonical" href="https://canonical.example.org/foo.html" />' in html
