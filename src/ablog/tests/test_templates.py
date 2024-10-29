from pathlib import Path
import pytest
from sphinx.application import Sphinx
from sphinx.errors import ThemeError


@pytest.mark.sphinx("html", testroot="templates", confoverrides={"skip_injecting_base_ablog_templates": True})
def test_skip_ablog_templates_but_missing_templates(app: Sphinx):
    """Completely override the templates used by ablog, but not provide them."""
    with pytest.raises(
        ThemeError,
        match=r"An error happened in rendering the page blog/archive\.\nReason: TemplateNotFound\(\"'ablog/catalog.html' not found in *.",
    ):
        app.build()


@pytest.mark.sphinx(
    "html",
    testroot="templates",
    confoverrides={
        "templates_path": ["_templates"],
        "skip_injecting_base_ablog_templates": False,  # default value
        "html_sidebars": {"**": ["ablog/postcard.html"]},
    },
)
def test_override_template_but_fallback_missing(app: Sphinx, rootdir: Path):
    """Partically override the only some Ablog templates, but use the Ablog ones for missing as fallback."""
    app.build()

    # read the content of custom postcard template
    expected = (rootdir / "test-templates" / "_templates" / "ablog" / "postcard.html").read_text()

    # is it in the output?
    source = (app.outdir / "post.html").read_text()
    assert expected in source


@pytest.mark.sphinx(
    "html",
    testroot="templates",
    confoverrides={
        "html_sidebars": {"**": ["ablog/postcard.html"]},
        "html_theme_path": "_themes",
        "html_theme": "test_theme",
    },
)
def test_themes_templates_come_first(app: Sphinx, rootdir: Path):
    """Ensures that if theme supplies own Ablog template, it is used over the builtin one."""
    app.build()

    # read the content of custom postcard template
    expected = (rootdir / "test-templates" / "_themes" / "test_theme" / "ablog" / "postcard.html").read_text()

    # is it in the output?
    source = (app.outdir / "post.html").read_text()
    assert expected in source
