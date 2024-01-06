"""
ABlog for Sphinx.
"""

import os
from glob import glob
from pathlib import PurePath

from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.jinja2glue import BuiltinTemplateLoader, SphinxFileSystemLoader
from sphinx.locale import get_translation

from .blog import CONFIG, Blog
from .post import (
    CheckFrontMatter,
    PostDirective,
    PostListDirective,
    UpdateDirective,
    UpdateNode,
    generate_archive_pages,
    generate_atom_feeds,
    missing_reference,
    process_postlist,
    process_posts,
    purge_posts,
)
from .version import version as __version__

__all__ = ["setup", "__version__"]

PKGDIR = os.path.abspath(os.path.dirname(__file__))
# Name used for the *.pot, *.po and *.mo files
MESSAGE_CATALOG_NAME = "sphinx"
_ = get_translation(MESSAGE_CATALOG_NAME)  # NOQA


def get_html_templates_path():
    """
    Return path to ABlog templates folder.
    """
    pkgdir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(pkgdir, "templates")


def anchor(post):
    """
    Return anchor string for posts that are page sections.
    """
    if post.section:
        return "#" + post.section
    else:
        return ""


def builder_support(builder):
    """
    Return True when builder is supported.

    Supported builders output in html format, but exclude
    `PickleHTMLBuilder` and `JSONHTMLBuilder`, which run into issues
    when serializing blog objects.
    """
    if hasattr(builder, "builder"):
        builder = builder.builder
    not_supported = {"json", "pickle"}
    return builder.format == "html" and builder.name not in not_supported


def html_page_context(app, pagename, templatename, context, doctree):
    if builder_support(app):
        context["ablog"] = blog = Blog(app)
        context["anchor"] = anchor
        if pagename in blog and blog[pagename].canonical_link:
            context["pageurl"] = blog[pagename].canonical_link
        # following is already available for archive pages
        if blog.blog_baseurl and "feed_path" not in context:
            context["feed_path"] = blog.blog_path
            context["feed_title"] = blog.blog_title


def config_inited(app, config):
    # Automatically identify any blog posts if a pattern is specified in the config
    if isinstance(config.blog_post_pattern, str):
        config.blog_post_pattern = [config.blog_post_pattern]
    matched_patterns = []
    for pattern in config.blog_post_pattern:
        pattern = os.path.join(app.srcdir, pattern)
        # make sure that blog post paths have forward slashes even on windows
        matched_patterns.extend(
            PurePath(ii).relative_to(app.srcdir).with_suffix("").as_posix() for ii in glob(pattern, recursive=True)
        )
    app.config.matched_blog_posts = matched_patterns

    # Add ablog stylesheets to static_path.
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "stylesheets"))
    app.config.html_static_path.append(static_path)


def builder_inited(app):
    if not isinstance(app.builder, StandaloneHTMLBuilder) or app.config.skip_injecting_base_ablog_templates:
        return
    if not isinstance(app.builder.templates, BuiltinTemplateLoader):
        raise Exception(
            "Ablog does not know how to inject templates into with custom "
            "template bridges. You can use `ablog.get_html_templates_path()` to "
            "get the path to add in your custom template bridge and set "
            "`skip_injecting_base_ablog_templates = False` in your "
            "`conf.py` file."
        )
    if get_html_templates_path() in app.config.templates_path:
        raise Exception(
            "Found the path from `ablog.get_html_templates_path()` in the "
            "`templates_path` variable from `conf.py`. Doing so interferes "
            "with Ablog's ability to stay compatible with Sphinx themes that "
            "support it out of the box. Please remove `get_html_templates_path` "
            "from `templates_path` in your `conf.py` to resolve this."
        )
    theme = app.builder.theme
    loaders = app.builder.templates.loaders
    templatepathlen = app.builder.templates.templatepathlen
    if theme.get_config("ablog", "inject_templates_after_theme", False):
        # Inject *after* the user templates and the theme templates,
        # allowing themes to override the templates provided by this
        # extension while those templates still serve as a fallback.
        loaders.append(SphinxFileSystemLoader(get_html_templates_path()))
    else:
        # Inject *after* the user templates and *before* the theme
        # templates. This enables ablog to provide support for themes
        # that don't support it out-of-the-box, like alabaster.
        loaders.insert(templatepathlen, SphinxFileSystemLoader(get_html_templates_path()))


def setup(app):
    """
    Setup ABlog extension.
    """
    for args in CONFIG:
        app.add_config_value(*args[:3])
    app.add_directive("post", PostDirective)
    app.add_directive("postlist", PostListDirective)
    app.connect("config-inited", config_inited)
    app.connect("builder-inited", builder_inited)
    app.connect("doctree-read", process_posts)
    app.connect("env-purge-doc", purge_posts)
    app.connect("doctree-resolved", process_postlist)
    app.connect("missing-reference", missing_reference)
    app.connect("html-collect-pages", generate_archive_pages)
    app.connect("html-collect-pages", generate_atom_feeds)
    app.connect("html-page-context", html_page_context)
    app.add_transform(CheckFrontMatter)
    app.add_directive("update", UpdateDirective)
    app.add_node(
        UpdateNode,
        html=(lambda s, n: s.visit_admonition(n), lambda s, n: s.depart_admonition(n)),
        latex=(lambda s, n: s.visit_admonition(n), lambda s, n: s.depart_admonition(n)),
    )
    pkgdir = os.path.abspath(os.path.dirname(__file__))
    locale_dir = os.path.join(pkgdir, "locales")
    app.add_message_catalog(MESSAGE_CATALOG_NAME, locale_dir)
    return {"version": __version__}  # identifies the version of our extension
