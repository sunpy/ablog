"""
ABlog for Sphinx.
"""

import os
from glob import glob

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

__all__ = ["setup"]


def anchor(post):
    """
    Return anchor string for posts that arepage sections.
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
        # following is already available for archive pages
        if blog.blog_baseurl and "feed_path" not in context:
            context["feed_path"] = blog.blog_path
            context["feed_title"] = blog.blog_title


def setup(app):
    """
    Setup ABlog extension.
    """

    for args in CONFIG:
        app.add_config_value(*args[:3])

    app.add_directive("post", PostDirective)
    app.add_directive("postlist", PostListDirective)

    app.connect("config-inited", config_inited)
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
    locale_dir = os.path.join(pkgdir, "locale")
    app.config.locale_dirs.append(locale_dir)

    return {"version": __version__}  # identifies the version of our extension


def config_inited(app, config):
    app.config.templates_path.append(get_html_templates_path())
    app.config.matched_blog_posts = [os.path.splitext(ii)[0] for ii in glob(config.blog_post_pattern)]


def get_html_templates_path():
    """
    Return path to ABlog templates folder.
    """

    pkgdir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(pkgdir, "templates")
