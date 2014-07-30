# -*- coding: utf-8 -*-
"""ABlog for Sphinx"""

import os

from .blog import Blog, CONFIG
from .post import (PostDirective, PostListDirective,
                   process_posts, process_postlist, purge_posts,
                   generate_archive_pages)

__version__ = '0.1'

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

    ld = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
    app.config.locale_dirs.append(ld)


def get_html_templates_path():
    """Return path to the folder containing ABlog templates."""

    return os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'templates')
