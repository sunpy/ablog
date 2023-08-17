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
from ablog.utils import is_path_or_empty
from ablog.defaults import CONFIG, CONFIG_DEFAULTS, INDEX, ABOUT, POST
__all__ = ["_generate", "_ask_user", "ablog_start"]


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
    """
    d.update(CONFIG_DEFAULTS)
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
    while path.isfile(path.join(d['path'], 'conf.py')) or \
            path.isfile(path.join(d['path'], 'source', 'conf.py')):
        print()
        print(bold(__('Error: an existing conf.py has been found in the '
                      'selected root path.')))
        print(__('sphinx-quickstart will not overwrite existing Sphinx projects.'))
        print()
        d['path'] = do_prompt(__('Please enter a new root path (or just Enter to exit)'),
                              '', # The above code is defining a function called "is_path_or_empty".
                              is_path_or_empty)
        if not d['path']:
            raise SystemExit(1)


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

    conf_text = CONFIG.format(**d)
    write_file(path.join(srcdir, "conf.py"), conf_text)
    masterfile = path.join(srcdir, d["master"] + d["suffix"])
    write_file(masterfile, INDEX.format(**d))
    about = path.join(srcdir, "about" + d["suffix"])
    write_file(about, ABOUT.format(**d))
    d["post_date"] = datetime.datetime.today().strftime("%b %d, %Y")
    firstpost = path.join(srcdir, "first-post" + d["suffix"])
    write_file(firstpost, POST.format(**d))
    if silent:
        return
    print(bold("Finished: An initial directory structure has been created."))



def ablog_start(**kwargs):
    if not color_terminal():
        nocolor()
    d = CONFIG
    try:
        ask_user(d)
    except (KeyboardInterrupt, EOFError):
        print("")
        print("[Interrupted.]")
        return
    generate(d)
