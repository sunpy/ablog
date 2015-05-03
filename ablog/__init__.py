# -*- coding: utf-8 -*-
"""ABlog for Sphinx"""
import os

from .blog import Blog, CONFIG
from .post import (PostDirective, PostListDirective, UpdateDirective,
                   UpdateNode, process_posts, process_postlist, purge_posts,
                   generate_archive_pages, generate_atom_feeds,
                   missing_reference)

__version__ = '0.7.0'


def anchor(post):
    """Return anchor string for posts that arepage sections."""

    if post.section:
        return '#' + post.section
    else:
        return ''


def html_page_context(app, pagename, templatename, context, doctree):

    context['ablog'] = Blog(app)
    context['anchor'] = anchor


def setup(app):
    """Setup ABlog extension."""

    for args in CONFIG:
        app.add_config_value(*args)

    app.add_directive('post', PostDirective)
    app.add_directive('postlist', PostListDirective)

    app.connect('doctree-read', process_posts)

    app.connect('env-purge-doc', purge_posts)
    app.connect('doctree-resolved', process_postlist)
    app.connect('missing-reference', missing_reference)
    app.connect('html-collect-pages', generate_archive_pages)
    app.connect('html-collect-pages', generate_atom_feeds)
    app.connect('html-page-context', html_page_context)

    app.add_directive('update', UpdateDirective)
    app.add_node(UpdateNode,
                 html=(lambda s, n: s.visit_admonition(n),
                       lambda s, n: s.depart_admonition(n)),
                 latex=(lambda s, n: s.visit_admonition(n),
                       lambda s, n: s.depart_admonition(n)),
                 )

    pkgdir = os.path.abspath(os.path.dirname(__file__))
    locale_dir = os.path.join(pkgdir, 'locale')
    app.config.locale_dirs.append(locale_dir)


def get_html_templates_path():
    """Return path to ABlog templates folder."""

    pkgdir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(pkgdir, 'templates')