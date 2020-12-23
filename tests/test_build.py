import pytest


@pytest.mark.sphinx("html", testroot="build")  # using roots/test-build
def test_build(app, status, warning):
    app.build()

    assert app.statuscode == 0
    assert (app.outdir / "index.html").exists()
    assert (app.outdir / "blog/archive.html").exists()
    assert (app.outdir / "post.html").exists()
