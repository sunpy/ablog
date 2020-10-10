import sys
import time
import datetime
from os import path
from textwrap import wrap

from docutils.utils import column_width
from sphinx.cmd.quickstart import do_prompt, ensuredir, is_path
from sphinx.util import texescape
from sphinx.util.console import bold, color_terminal, nocolor
from sphinx.util.osutil import make_filename

from .version import version as __version__


def w(t, ls=80):
    return "\n".join(wrap(t, ls))


__all__ = ["generate", "ask_user", "ablog_start"]

ABLOG_CONF = "#!/usr/bin/env python\n"
ABLOG_CONF += """

# %(project)s build configuration file, created by
# `ablog start` on %(now)s.
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
blog_title = u'%(project_str)s Blog'

# Base URL for the website, required for generating feeds.
# e.g. blog_baseurl = "http://example.com/"
blog_baseurl = u'%(blog_baseurl)s'

# Choose to archive only post titles. Archiving only titles can speed
# up project building.
# blog_archive_titles = False

# -- Blog Authors, Languages, and Locations -----------------------------------

# A dictionary of author names mapping to author full display names and
# links. Dictionary keys are what should be used in ``post`` directive
# to refer to the author.  Default is ``{}``.
blog_authors = {
    '%(author_str)s': ('%(author_str)s', None),
}


# A dictionary of language code names mapping to full display names and
# links of these languages. Similar to :confval:`blog_authors`, dictionary
# keys should be used in ``post`` directive to refer to the locations.
# Default is ``{}``.
# blog_languages = {
#    'en': ('English', None),
# }


# A dictionary of location names mapping to full display names and
# links of these locations. Similar to :confval:`blog_authors`, dictionary
# keys should be used in ``post`` directive to refer to the locations.
# Default is ``{}``.
# blog_locations = {
#    'Earth': ('The Blue Planet', 'https://en.wikipedia.org/wiki/Earth),
# }

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
html_sidebars = {
    '**': [ 'about.html',
            'postcard.html', 'navigation.html',
            'recentposts.html', 'tagcloud.html',
            'categories.html',  'archives.html',
            'searchbox.html',
            ],
    }

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

# Add any paths that contain templates here, relative to this directory.
templates_path = ['%(dot)stemplates', ablog.get_html_templates_path()]

# The suffix(es) of source filenames.
source_suffix = '%(suffix)s'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = '%(master_str)s'

# General information about the project.
project = u'%(project_str)s'
copyright = u'%(copyright_str)s'
author = u'%(author_str)s'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '%(version_str)s'
# The full version, including alpha/beta/rc tags.
release = '%(release_str)s'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = %(language)r

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%%B %%d, %%Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = [%(exclude_patterns)s]

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
todo_include_todos = %(ext_todo)s


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'github_button': False,
}

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
html_static_path = ['%(dot)sstatic']

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
# html_additional_pages = {}

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
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = '%(project_fn)sdoc'


"""

ABLOG_INDEX = """
.. %(project)s index file, created by `ablog start` on %(now)s.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to %(author)s's Blog!
===========%(project_underline)s=================

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

About %(author)s
============================

The world wants to know more about you.

"""

ABLOG_POST = """
.. %(project)s post example, created by `ablog start` on %(post_date)s.

.. post:: %(post_date)s
   :tags: atag
   :author: %(author_str)s

First Post
==========

World, hello again! This very first paragraph of the post will be used
as excerpt in archives and feeds. Find out how to control how much is shown
in `Post Excerpts and Images
<https://ablog.readthedocs.org/manual/post-excerpts-and-images/>`__. Remember
that you can refer to posts by file name, e.g. ``:ref:`first-post``` results
in :ref:`first-post`. Find out more at `Cross-Referencing Blog Pages
<https://ablog.readthedocs.org/manual/cross-referencing-blog-pages/>`__.
"""


CONF_DEFAULTS = {
    "sep": False,
    "dot": "_",
    "language": None,
    "suffix": ".rst",
    "master": "index",
    "makefile": False,
    "batchfile": False,
    "epub": False,
    "ext_todo": False,
}


def generate(d, overwrite=True, silent=False):
    """
    Borrowed from Sphinx 1.3b3.
    """

    """Generate project based on values in *d*."""

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

    # escape backslashes and single quotes in strings that are put into
    # a Python string literal
    for key in (
        "project",
        "project_doc",
        "project_doc_texescaped",
        "author",
        "author_texescaped",
        "copyright",
        "version",
        "release",
        "master",
    ):
        d[key + "_str"] = d[key].replace("\\", "\\\\").replace("'", "\\'")

    if not path.isdir(d["path"]):
        ensuredir(d["path"])

    srcdir = d["sep"] and path.join(d["path"], "source") or d["path"]

    ensuredir(srcdir)
    d["exclude_patterns"] = ""
    # TODO: Work if we want this.
    # if d['sep']:
    #    builddir = path.join(d['path'], 'build')
    #
    # else:
    #    builddir = path.join(srcdir, d['dot'] + 'build')
    #    d['exclude_patterns'] = repr(d['dot'] + 'build')
    # ensuredir(builddir)
    ensuredir(path.join(srcdir, d["dot"] + "templates"))
    ensuredir(path.join(srcdir, d["dot"] + "static"))

    def write_file(fpath, content, newline=None):
        if overwrite or not path.isfile(fpath):
            print("Creating file %s." % fpath)
            f = open(fpath, "wt", encoding="utf-8", newline=newline)
            try:
                f.write(content)
            finally:
                f.close()
        else:
            print("File %s already exists, skipping." % fpath)

    conf_text = ABLOG_CONF % d
    write_file(path.join(srcdir, "conf.py"), conf_text)

    masterfile = path.join(srcdir, d["master"] + d["suffix"])
    write_file(masterfile, ABLOG_INDEX % d)

    about = path.join(srcdir, "about" + d["suffix"])
    write_file(about, ABLOG_ABOUT % d)

    d["post_date"] = datetime.datetime.today().strftime("%b %d, %Y")
    firstpost = path.join(srcdir, "first-post" + d["suffix"])
    write_file(firstpost, ABLOG_POST % d)

    if silent:
        return

    print(bold("Finished: An initial directory structure has been created."))


def ask_user(d):
    """
    Borrowed from Sphinx 1.3b3.

    Ask the user for quickstart values missing from *d*.

    Values are:

    * path:      root path
    * project:   project name
    * author:    author names
    * version:   version of project
    * release:   release of project
    """

    d.update(CONF_DEFAULTS)

    print(bold("Welcome to the ABlog %s quick start utility.") % __version__)
    print("")
    print(
        w(
            "Please enter values for the following settings (just press Enter "
            "to accept a default value, if one is given in brackets)."
        )
    )

    print("")
    if "path" in d:
        print(bold("Selected root path: %s" % d["path"]))
    else:
        print("Enter the root path for your blog project (path has to exist).")
        d["path"] = do_prompt("Root path for your project (path has to exist)", ".", is_path)

    while path.isfile(path.join(d["path"], "conf.py")) or path.isfile(
        path.join(d["path"], "source", "conf.py")
    ):
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
                    "Error: the master file %s has already been found in the "
                    "selected root path." % (d["master"] + d["suffix"])
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


def ablog_start(**kwargs):
    if not color_terminal():
        nocolor()

    d = CONF_DEFAULTS

    try:
        ask_user(d)
    except (KeyboardInterrupt, EOFError):
        print("")
        print("[Interrupted.]")
        return

    generate(d)
