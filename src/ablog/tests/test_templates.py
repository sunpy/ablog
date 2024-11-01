from pathlib import Path
import pytest
from sphinx.application import Sphinx
from sphinx.errors import ThemeError


@pytest.mark.sphinx("html", testroot="templates", confoverrides={"skip_injecting_base_ablog_templates": True})
def test_skip_ablog_templates_but_missing_templates(app: Sphinx):
    """
    Completely override the templates used by ablog, but not provide them.
    """
    with pytest.raises(
        ThemeError,
        match=r"An error happened in rendering the page blog/author\.\nReason: TemplateNotFound\(\"'ablog/catalog.html' not found in *.",
    ):
        app.build()


@pytest.mark.sphinx(
    "html",
    testroot="templates",
    confoverrides={
        "templates_path": ["_templates"],
        "skip_injecting_base_ablog_templates": False,  # default value
        "html_sidebars": {
            "**": [
                # overridden by user
                "ablog/postcard.html",
                # fallback to builtin
                "ablog/authors.html",
            ]
        },
    },
)
def test_override_template_but_fallback_missing(app: Sphinx, rootdir: Path):
    """
    Partially override the only some Ablog templates, but use the Ablog ones
    for missing as fallback.
    """
    app.build()

    # is the customized template it in the output?
    customized = (rootdir / "test-templates" / "_templates" / "ablog" / "postcard.html").read_text()
    source = (app.outdir / "post.html").read_text()
    assert customized in source

    # is builtin template in the output?
    builtin = '<div class="ablog-sidebar-item ablog__authors">'
    assert builtin in source


@pytest.mark.sphinx(
    "html",
    testroot="templates",
    confoverrides={
        "html_sidebars": {
            "**": [
                # overridden by theme
                "ablog/postcard.html",
                # fallback to builtin
                "ablog/authors.html",
            ]
        },
        "html_theme_path": "_themes",
        "html_theme": "test_theme",
    },
)
def test_themes_templates_come_first(app: Sphinx, rootdir: Path):
    """
    Ensures that if theme supplies own Ablog template, it is used over the
    builtin one, but fallback to builtin for missing ones.
    """
    app.build()

    # is the customized template it in the output?
    customized = (rootdir / "test-templates" / "_themes" / "test_theme" / "ablog" / "postcard.html").read_text()
    source = (app.outdir / "post.html").read_text()
    assert customized in source

    # is builtin template in the output?
    builtin = '<div class="ablog-sidebar-item ablog__authors">'
    assert builtin in source
