"""
Quick setup to get started with ABlog.

Borrowed heavily from Sphinx quickstart.
"""
from __future__ import annotations

import sys
import time
import datetime
from os import path
from textwrap import wrap
from docutils.utils import column_width

import sphinx.locale
from sphinx import __display_version__, package_dir
from sphinx.locale import __
from sphinx.util.console import (
    bold,
    color_terminal,
    colorize,
    nocolor,
    red,
)
from sphinx.util.osutil import ensuredir
from sphinx.util.template import SphinxRenderer
from collections.abc import Sequence

from docutils.utils import column_width
from sphinx.cmd.quickstart import do_prompt, is_path
from sphinx.util import texescape
from sphinx.util.console import bold, color_terminal, nocolor
from sphinx.util.osutil import ensuredir, make_filename
import argparse
import locale
import os
import sys
import time
from os import path
from typing import TYPE_CHECKING, Any, Callable

try:
    import readline
    if TYPE_CHECKING and sys.platform == "win32":
        raise ImportError
    READLINE_AVAILABLE = True
    if readline.__doc__ and 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
        USE_LIBEDIT = True
    else:
        readline.parse_and_bind("tab: complete")
        USE_LIBEDIT = False
except ImportError:
    READLINE_AVAILABLE = False
    USE_LIBEDIT = False

from ablog import __version__


__all__ = ["_generate", "_ask_user", "ablog_start"]

ABLOG_CONFIG = """
#!/usr/bin/env python

# {project} build configuration file, created by
# `ablog start` on {now}.
#
# Note that not all possible configuration values are present in this file.
# All configuration values have a default; values that are commented out
# serve to show the default.

import os
import sys
import ablog
import alabaster

# -- General ABlog Options ----------------------------------------------------

# A path relative to the configuration directory for blog archive pages.
# blog_path = 'blog'

# The "title" for the blog, used in active pages.  Default is ``'Blog'``.
blog_title = "{project} Blog"

# Base URL for the website, required for generating feeds.
# e.g. blog_baseurl = "http://example.com/"
blog_baseurl = "{blog_baseurl}"

# Choose to archive only post titles. Archiving only titles can speed
# up project building.
# blog_archive_titles = False

# -- Blog Authors, Languages, and Locations -----------------------------------

# A dictionary of author names mapping to author full display names and
# links. Dictionary keys are what should be used in ``post`` directive
# to refer to the author.  Default is ``{{}}``.
blog_authors = {{
    "{author}": ("{author}", None),
}}


# A dictionary of language code names mapping to full display names and
# links of these languages. Similar to :confval:`blog_authors`, dictionary
# keys should be used in ``post`` directive to refer to the locations.
# Default is ``{{}}``.
# blog_languages = {{
#    'en': ('English', None),
# }}


# A dictionary of location names mapping to full display names and
# links of these locations. Similar to :confval:`blog_authors`, dictionary
# keys should be used in ``post`` directive to refer to the locations.
# Default is ``{{}}``.
# blog_locations = {{
#    'Earth': ('The Blue Planet', 'https://en.wikipedia.org/wiki/Earth),
# }}

# This will prevent ablog from injecting its own templates into the Sphinx
# build. This is only useful when you have a custom template bridge (rare).
# See https://github.com/sunpy/ablog/pull/144 for the full context.
# skip_injecting_base_ablog_templates = False

# -- Blog Post Related --------------------------------------------------------

# Format date for a post.
# post_date_format = '%%b %%d, %%Y'

# Number of paragraphs (default is ``1``) that will be displayed as an excerpt
# from the post. Setting this ``0`` will result in displaying no post excerpt
# in archive pages.  This option can be set on a per post basis using
# post_auto_excerpt = 1

# Index of the image that will be displayed in the excerpt of the post.
# Default is ``0``, meaning no image.  Setting this to ``1`` will include
# the first image, when available, to the excerpt.  This option can be set
# on a per post basis using :rst:dir:`post` directive option ``image``.
# post_auto_image = 0

# Number of seconds (default is ``5``) that a redirect page waits before
# refreshing the page to redirect to the post.
# post_redirect_refresh = 5

# When ``True``, post title and excerpt is always taken from the section that
# contains the :rst:dir:`post` directive, instead of the document. This is the
# behavior when :rst:dir:`post` is used multiple times in a document. Default
# is ``False``.
# post_always_section = False

# When ``True``, links to the previous and next posts will be rendered at the
# bottom of the page.
# Default is ``True``
# post_show_prev_next = True

# When ``False``, the :rst:dir:`orphan` directive is not automatically set
# for each post. Without this directive, Sphinx will warn about posts that
# are not explicitly referenced via another document. :rst:dir:`orphan` can
# be set on a per-post basis as well if this is false. Default is ``True``.
# post_auto_orphan = True

# -- ABlog Sidebars -------------------------------------------------------

# There are seven sidebars you can include in your HTML output.
# postcard.html provides information regarding the current post.
# recentposts.html lists most recent five posts. Others provide
# a link to a archive pages generated for each tag, category, and year.
# In addition, there are authors.html, languages.html, and locations.html
# sidebars that link to author and location archive pages.
html_sidebars = {{
    '**': [ 'ablog/postcard.html', 'navigation.html',
            'ablog/recentposts.html', 'ablog/tagcloud.html',
            'ablog/categories.html',  'ablog/archives.html',
            'searchbox.html',
            ],
    }}

# -- Blog Feed Options --------------------------------------------------------

# Turn feeds by setting :confval:`blog_baseurl` configuration variable.
# Choose to create feeds per author, location, tag, category, and year,
# default is ``False``.
# blog_feed_archives = False

# Choose to display full text in blog feeds, default is ``False``.
# blog_feed_fulltext = False

# Blog feed subtitle, default is ``None``.
# blog_feed_subtitle = None

# Choose to feed only post titles, default is ``False``.
# blog_feed_titles = False

# Specify custom Jinja2 templates for feed entry elements:
#     `title`, `summary`, or `content`
# For example, to add an additional feed for posting to social media:
# blog_feed_templates = {{
#     # Use defaults, no templates
#     "atom": {{}},
#     # Create content text suitable posting to social media
#     "social": {{
#         # Format tags as hashtags and append to the content
#         "content": "{{ title }}{{% for tag in post.tags %}}"
#         " #{{ tag.name|trim()|replace(' ', '') }}"
#         "{{% endfor %}}",
#     }},
# }}
# Default: Create one `atom.xml` feed without any templates
# blog_feed_templates = {{"atom": {{}} }}

# Specify number of recent posts to include in feeds, default is ``None``
# for all posts.
# blog_feed_length = None

# -- Font-Awesome Options -----------------------------------------------------

# ABlog templates will use of Font Awesome icons if one of the following
# is ``True``

# Link to `Font Awesome`_ at `Bootstrap CDN`_ and use icons in sidebars
# and post footers.  Default: ``None``
# fontawesome_link_cdn = None

# Sphinx_ theme already links to `Font Awesome`_.  Default: ``False``
# fontawesome_included = False

# Alternatively, you can provide the path to `Font Awesome`_ :file:`.css`
# with the configuration option: fontawesome_css_file
# Path to `Font Awesome`_ :file:`.css` (default is ``None``) that will
# be linked to in HTML output by ABlog.
# fontawesome_css_file = None

# -- Disqus Integration -------------------------------------------------------

# You can enable Disqus_ by setting ``disqus_shortname`` variable.
# Disqus_ short name for the blog.
# disqus_shortname = None

# Choose to disqus pages that are not posts, default is ``False``.
# disqus_pages = False

# Choose to disqus posts that are drafts (without a published date),
# default is ``False``.
# disqus_drafts = False

# -- Sphinx Options -----------------------------------------------------------

# If your project needs a minimal Sphinx version, state it here.
needs_sphinx = '1.2'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'alabaster',
    'ablog',
]

# The suffix(es) of source filenames.
source_suffix = "{suffix}"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "{master}"

# General information about the project.
project = "{project}"
copyright = "{copyright}"
author = "{author}"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = "{version}"
# The full version, including alpha/beta/rc tags.
release = "{release}"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "{language}"

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%%B %%d, %%Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["{exclude_patterns}"]

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = {ext_todo}

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {{
    'github_button': False,
}}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = [alabaster.get_path()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["{dot}static"]

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%%b %%d, %%Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {{}}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {{'type': 'default'}}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = "{project_fn}doc"
"""

ABLOG_INDEX = """
.. {project} index file, created by `ablog start` on {now}.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to {author}'s Blog!
==========={project_underline}=================

Hello World! Find more about me here: :ref:`about`

Here is a list of most recent posts:

.. postlist:: 5
   :excerpts:

.. `toctree` directive, below, contains list of non-post `.rst` files.
   This is how they appear in Navigation sidebar. Note that directive
   also contains `:hidden:` option so that it is not included inside the page.

   Posts are excluded from this directive so that they aren't double listed
   in the sidebar both under Navigation and Recent Posts.

.. toctree::
   :hidden:

   about.rst
"""

ABLOG_ABOUT = """
.. _about:

About {author}
============================

The world wants to know more about you.
"""

ABLOG_POST = """
.. {project} post example, created by `ablog start` on {post_date}.

.. post:: {post_date}
   :tags: atag
   :author: {author}

First Post
==========

World, hello again! This very first paragraph of the post will be used
as excerpt in archives and feeds. Find out how to control how much is shown
in `Post Excerpts and Images
<https://ablog.readthedocs.io/manual/post-excerpts-and-images/>`__. Remember
that you can refer to posts by file name, e.g. ``:ref:`first-post``` results
in :ref:`first-post`. Find out more at `Cross-Referencing Blog Pages
<https://ablog.readthedocs.io/manual/cross-referencing-blog-pages/>`__.
"""

ABLOG_CONFIG_DEFAULTS = {
    "sep": False,
    "dot": "_",
    "language": "en",
    "suffix": ".rst",
    "master": "index",
    "makefile": False,
    "batchfile": False,
    "epub": False,
    "ext_todo": False,
}

def _ask_user(d):
    """
    Ask the user for quickstart values missing from *d*.

    Values are:

    * path:      root path
    * sep:       separate source and build dirs (bool)
    * dot:       replacement for dot in _templates etc.
    * project:   project name
    * author:    author names
    * version:   version of project
    * release:   release of project
    * language:  document language
    * suffix:    source file suffix
    * master:    master document name
    * extensions:  extensions to use (list)
    * makefile:  make Makefile
    * batchfile: make command file
    """
    d.update(ABLOG_CONFIG_DEFAULTS)
    print(bold(f"Welcome to the ABlog {__version__} quick start utility."))
    print()
    print(__('Please enter values for the following settings (just press Enter to\n'
             'accept a default value, if one is given in brackets).'))
    print()
    if "path" in d:
        print(bold(__('Selected root path: %s')) % d['path'])
    else:
        print(__('Enter the root path for your project.'))
        d['path'] = do_prompt(__('Root path for your project'), '.', is_path)


    while path.isfile(path.join(d["path"], "conf.py")) or path.isfile(path.join(d["path"], "source", "conf.py")):
        print("")
        print(bold(w("Error: an existing conf.py has been found in the " "selected root path.")))
        print("ablog start will not overwrite existing Sphinx projects.")
        print("")
        d["path"] = do_prompt("Please enter a new root path (or just Enter to exit)", ".", is_path)
        if not d["path"]:
            sys.exit(1)
    if "project" not in d:
        print("")
        print(
            w(
                "Project name will occur in several places in the website, "
                "including blog archive pages and atom feeds. Later, you can "
                "set separate names for different parts of the website in "
                "configuration file."
            )
        )
        d["project"] = do_prompt("Project name")
    if "author" not in d:
        print(
            w(
                "This of author as the copyright holder of the content. "
                "If your blog has multiple authors, you might want to enter "
                "a team name here. Later, you can specify individual authors "
                "using `blog_authors` configuration option."
            )
        )
        d["author"] = do_prompt("Author name(s)")
    d["release"] = d["version"] = ""
    while path.isfile(path.join(d["path"], d["master"] + d["suffix"])) or path.isfile(
        path.join(d["path"], "source", d["master"] + d["suffix"])
    ):
        print("")
        print(
            bold(
                w(
                    f"Error: the master file {d['master'] + d['suffix']} has already been found in the "
                    "selected root path."
                )
            )
        )
        print("ablog-start will not overwrite the existing file.")
        print("")
        d["master"] = do_prompt(
            w("Please enter a new file name, or rename the " "existing file and press Enter"), d["master"]
        )
    if "blog_baseurl" not in d:
        print("")
        print(
            w(
                "Please enter the base URL for your project. Blog feeds will "
                "be generated relative to this URL. If you don't have one yet, "
                "you can set it in configuration file later."
            )
        )
        d["blog_baseurl"] = do_prompt("Base URL for your project", None, lambda x: x)
    print("")


def ask_user(d: dict[str, Any]) -> None:
    """Ask the user for quickstart values missing from *d*.

    Values are:

    * path:      root path
    * sep:       separate source and build dirs (bool)
    * dot:       replacement for dot in _templates etc.
    * project:   project name
    * author:    author names
    * version:   version of project
    * release:   release of project
    * language:  document language
    * suffix:    source file suffix
    * master:    master document name
    * extensions:  extensions to use (list)
    * makefile:  make Makefile
    * batchfile: make command file
    """

    print(bold(__('Welcome to the Sphinx %s quickstart utility.')) % __display_version__)
    print()
    print(__('Please enter values for the following settings (just press Enter to\n'
             'accept a default value, if one is given in brackets).'))

    if 'path' in d:
        print()
        print(bold(__('Selected root path: %s')) % d['path'])
    else:
        print()
        print(__('Enter the root path for documentation.'))
        d['path'] = do_prompt(__('Root path for the documentation'), '.', is_path)

    while path.isfile(path.join(d['path'], 'conf.py')) or \
            path.isfile(path.join(d['path'], 'source', 'conf.py')):
        print()
        print(bold(__('Error: an existing conf.py has been found in the '
                      'selected root path.')))
        print(__('sphinx-quickstart will not overwrite existing Sphinx projects.'))
        print()
        d['path'] = do_prompt(__('Please enter a new root path (or just Enter to exit)'),
                              '', is_path_or_empty)
        if not d['path']:
            raise SystemExit(1)

    if 'sep' not in d:
        print()
        print(__('You have two options for placing the build directory for Sphinx output.\n'
                 'Either, you use a directory "_build" within the root path, or you separate\n'
                 '"source" and "build" directories within the root path.'))
        d['sep'] = do_prompt(__('Separate source and build directories (y/n)'), 'n', boolean)

    if 'dot' not in d:
        print()
        print(__('Inside the root directory, two more directories will be created; "_templates"\n'      # noqa: E501
                 'for custom HTML templates and "_static" for custom stylesheets and other static\n'    # noqa: E501
                 'files. You can enter another prefix (such as ".") to replace the underscore.'))       # noqa: E501
        d['dot'] = do_prompt(__('Name prefix for templates and static dir'), '_', ok)

    if 'project' not in d:
        print()
        print(__('The project name will occur in several places in the built documentation.'))
        d['project'] = do_prompt(__('Project name'))
    if 'author' not in d:
        d['author'] = do_prompt(__('Author name(s)'))

    if 'version' not in d:
        print()
        print(__('Sphinx has the notion of a "version" and a "release" for the\n'
                 'software. Each version can have multiple releases. For example, for\n'
                 'Python the version is something like 2.5 or 3.0, while the release is\n'
                 "something like 2.5.1 or 3.0a1. If you don't need this dual structure,\n"
                 'just set both to the same value.'))
        d['version'] = do_prompt(__('Project version'), '', allow_empty)
    if 'release' not in d:
        d['release'] = do_prompt(__('Project release'), d['version'], allow_empty)

    if 'language' not in d:
        print()
        print(__(
            'If the documents are to be written in a language other than English,\n'
            'you can select a language here by its language code. Sphinx will then\n'
            'translate text that it generates into that language.\n'
            '\n'
            'For a list of supported codes, see\n'
            'https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.',
        ))
        d['language'] = do_prompt(__('Project language'), 'en')
        if d['language'] == 'en':
            d['language'] = None

    if 'suffix' not in d:
        print()
        print(__('The file name suffix for source files. Commonly, this is either ".txt"\n'
                 'or ".rst". Only files with this suffix are considered documents.'))
        d['suffix'] = do_prompt(__('Source file suffix'), '.rst', suffix)

    if 'master' not in d:
        print()
        print(__('One document is special in that it is considered the top node of the\n'
                 '"contents tree", that is, it is the root of the hierarchical structure\n'
                 'of the documents. Normally, this is "index", but if your "index"\n'
                 'document is a custom template, you can also set this to another filename.'))
        d['master'] = do_prompt(__('Name of your master document (without suffix)'), 'index')

    while path.isfile(path.join(d['path'], d['master'] + d['suffix'])) or \
            path.isfile(path.join(d['path'], 'source', d['master'] + d['suffix'])):
        print()
        print(bold(__('Error: the master file %s has already been found in the '
                      'selected root path.') % (d['master'] + d['suffix'])))
        print(__('sphinx-quickstart will not overwrite the existing file.'))
        print()
        d['master'] = do_prompt(__('Please enter a new file name, or rename the '
                                   'existing file and press Enter'), d['master'])

    if 'extensions' not in d:
        print(__('Indicate which of the following Sphinx extensions should be enabled:'))
        d['extensions'] = []
        for name, description in EXTENSIONS.items():
            if do_prompt(f'{name}: {description} (y/n)', 'n', boolean):
                d['extensions'].append('sphinx.ext.%s' % name)

        # Handle conflicting options
        if {'sphinx.ext.imgmath', 'sphinx.ext.mathjax'}.issubset(d['extensions']):
            print(__('Note: imgmath and mathjax cannot be enabled at the same time. '
                     'imgmath has been deselected.'))
            d['extensions'].remove('sphinx.ext.imgmath')

    if 'makefile' not in d:
        print()
        print(__('A Makefile and a Windows command file can be generated for you so that you\n'
                 "only have to run e.g. `make html' instead of invoking sphinx-build\n"
                 'directly.'))
        d['makefile'] = do_prompt(__('Create Makefile? (y/n)'), 'y', boolean)

    if 'batchfile' not in d:
        d['batchfile'] = do_prompt(__('Create Windows command file? (y/n)'), 'y', boolean)
    print()



def _generate(
    d: dict, overwrite: bool = True, silent: bool = False, templatedir: str | None = None,
) -> None:
    """Generate project based on values in *d*."""
    template = QuickstartRenderer(templatedir or '')

    if 'mastertoctree' not in d:
        d['mastertoctree'] = ''
    if 'mastertocmaxdepth' not in d:
        d['mastertocmaxdepth'] = 2

    d['root_doc'] = d['master']
    d['now'] = time.asctime()
    d['project_underline'] = column_width(d['project']) * '='
    d.setdefault('extensions', [])
    d['copyright'] = time.strftime('%Y') + ', ' + d['author']

    d["path"] = os.path.abspath(d['path'])
    ensuredir(d['path'])

    srcdir = path.join(d['path'], 'source') if d['sep'] else d['path']

    ensuredir(srcdir)
    if d['sep']:
        builddir = path.join(d['path'], 'build')
        d['exclude_patterns'] = ''
    else:
        builddir = path.join(srcdir, d['dot'] + 'build')
        exclude_patterns = map(repr, [
            d['dot'] + 'build',
            'Thumbs.db', '.DS_Store',
        ])
        d['exclude_patterns'] = ', '.join(exclude_patterns)
    ensuredir(builddir)
    ensuredir(path.join(srcdir, d['dot'] + 'templates'))
    ensuredir(path.join(srcdir, d['dot'] + 'static'))

    def write_file(fpath: str, content: str, newline: str | None = None) -> None:
        if overwrite or not path.isfile(fpath):
            if 'quiet' not in d:
                print(__('Creating file %s.') % fpath)
            with open(fpath, 'w', encoding='utf-8', newline=newline) as f:
                f.write(content)
        else:
            if 'quiet' not in d:
                print(__('File %s already exists, skipping.') % fpath)

    conf_path = os.path.join(templatedir, 'conf.py_t') if templatedir else None
    if not conf_path or not path.isfile(conf_path):
        conf_path = os.path.join(package_dir, 'templates', 'quickstart', 'conf.py_t')
    with open(conf_path, encoding="utf-8") as f:
        conf_text = f.read()

    write_file(path.join(srcdir, 'conf.py'), template.render_string(conf_text, d))

    masterfile = path.join(srcdir, d['master'] + d['suffix'])
    if template._has_custom_template('quickstart/master_doc.rst_t'):
        msg = ('A custom template `master_doc.rst_t` found. It has been renamed to '
               '`root_doc.rst_t`.  Please rename it on your project too.')
        print(colorize('red', msg))
        write_file(masterfile, template.render('quickstart/master_doc.rst_t', d))
    else:
        write_file(masterfile, template.render('quickstart/root_doc.rst_t', d))

    if d.get('make_mode') is True:
        makefile_template = 'quickstart/Makefile.new_t'
        batchfile_template = 'quickstart/make.bat.new_t'
    else:
        makefile_template = 'quickstart/Makefile_t'
        batchfile_template = 'quickstart/make.bat_t'

    if d['makefile'] is True:
        d['rsrcdir'] = 'source' if d['sep'] else '.'
        d['rbuilddir'] = 'build' if d['sep'] else d['dot'] + 'build'
        # use binary mode, to avoid writing \r\n on Windows
        write_file(path.join(d['path'], 'Makefile'),
                   template.render(makefile_template, d), '\n')

    if d['batchfile'] is True:
        d['rsrcdir'] = 'source' if d['sep'] else '.'
        d['rbuilddir'] = 'build' if d['sep'] else d['dot'] + 'build'
        write_file(path.join(d['path'], 'make.bat'),
                   template.render(batchfile_template, d), '\r\n')

    if silent:
        return
    print()
    print(bold(__('Finished: An initial directory structure has been created.')))
    print()
    print(__('You should now populate your master file %s and create other documentation\n'
             'source files. ') % masterfile, end='')
    if d['makefile'] or d['batchfile']:
        print(__('Use the Makefile to build the docs, like so:\n'
                 '   make builder'))
    else:
        print(__('Use the sphinx-build command to build the docs, like so:\n'
                 '   sphinx-build -b builder %s %s') % (srcdir, builddir))
    print(__('where "builder" is one of the supported builders, '
             'e.g. html, latex or linkcheck.'))
    print()


def generate(d, overwrite=True, silent=False):
    """
    Borrowed from Sphinx 1.3b3.

    Generate project based on values in *d*.
    """
    texescape.init()
    if "mastertoctree" not in d:
        d["mastertoctree"] = ""
    if "mastertocmaxdepth" not in d:
        d["mastertocmaxdepth"] = 2
    d["project_fn"] = make_filename(d["project"])
    d["project_manpage"] = d["project_fn"].lower()
    d["now"] = time.asctime()
    d["project_underline"] = column_width(d["project"]) * "="
    d["copyright"] = time.strftime("%Y") + ", " + d["author"]
    d["author_texescaped"] = texescape.escape(str(d["author"]).translate(str(d["author"])))
    d["project_doc"] = d["project"] + " Documentation"
    d["project_doc_texescaped"] = texescape.escape(
        str(d["project"] + " Documentation").translate(str(d["project"] + " Documentation"))
    )
    if not path.isdir(d["path"]):
        ensuredir(d["path"])
    srcdir = d["sep"] and path.join(d["path"], "source") or d["path"]
    ensuredir(srcdir)
    d["exclude_patterns"] = ""
    ensuredir(path.join(srcdir, d["dot"] + "templates"))
    ensuredir(path.join(srcdir, d["dot"] + "static"))

    def write_file(fpath, content, newline=None):
        if overwrite or not path.isfile(fpath):
            print(f"Creating file {fpath}.")
            f = open(fpath, "wt", encoding="utf-8", newline=newline)
            try:
                f.write(content)
            finally:
                f.close()
        else:
            print(f"File {fpath} already exists, skipping.")

    conf_text = ABLOG_CONFIG.format(**d)
    write_file(path.join(srcdir, "conf.py"), conf_text)
    masterfile = path.join(srcdir, d["master"] + d["suffix"])
    write_file(masterfile, ABLOG_INDEX.format(**d))
    about = path.join(srcdir, "about" + d["suffix"])
    write_file(about, ABLOG_ABOUT.format(**d))
    d["post_date"] = datetime.datetime.today().strftime("%b %d, %Y")
    firstpost = path.join(srcdir, "first-post" + d["suffix"])
    write_file(firstpost, ABLOG_POST.format(**d))
    if silent:
        return
    print(bold("Finished: An initial directory structure has been created."))



def ablog_start(**kwargs):
    if not color_terminal():
        nocolor()
    d = ABLOG_CONFIG
    try:
        ask_user(d)
    except (KeyboardInterrupt, EOFError):
        print("")
        print("[Interrupted.]")
        return
    generate(d)
