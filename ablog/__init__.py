# -*- coding: utf-8 -*-
"""ABlog for Sphinx"""

import os

from .blog import Blog, CONFIG
from .post import (PostDirective, PostListDirective, UpdateDirective,
                   UpdateNode, process_posts, process_postlist, purge_posts,
                   generate_archive_pages, generate_atom_feeds)

__version__ = '0.3.1'

def anchor(post):


    if post.section:
        return '#' + post.section
    else:
        return ''

def init_ablog(app):
    """Instantiate ABlog and link from `html_context` so that it can be
    reached from templates."""

    app.config.html_context['ablog'] = Blog(app)
    app.config.html_context['anchor'] = anchor

def setup(app):
    """Setup ABlog extension."""

    for args in CONFIG:
        app.add_config_value(*args)

    app.add_directive('post', PostDirective)
    app.add_directive('postlist', PostListDirective)
    app.connect('builder-inited', init_ablog)
    app.connect('doctree-read', process_posts)
    app.connect('env-purge-doc', purge_posts)
    app.connect('doctree-resolved', process_postlist)
    app.connect('html-collect-pages', generate_archive_pages)
    app.connect('html-collect-pages', generate_atom_feeds)

    app.add_directive('update', UpdateDirective)
    app.add_node(UpdateNode,
                 html=(lambda s, n: s.visit_admonition(n),
                       lambda s, n: s.depart_admonition(n)))

    ld = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
    app.config.locale_dirs.append(ld)


def get_html_templates_path():
    """Return path to the folder containing ABlog templates."""

    return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'templates')
