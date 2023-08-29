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
from copy import copy
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

from ablog.utils import is_path_or_empty, valid_dir
from ablog.defaults import CONFIG, CONFIG_DEFAULTS, INDEX, ABOUT, POST
from ablog.commands import get_parser
from ablog.version import __version__

__all__ = ["generate", "ask_user", "start_ablog"]


def ask_user(d):
    """
    Ask the user for quickstart values missing from *d*.

    Values are:

    * path:         root path
    * project:      project name
    * author:       author names
    * language:     document language
    * blog_baseurl: blog url
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
        print(__('ABlog will not overwrite existing ABlog projects.'))
        print()
        d['path'] = do_prompt(__('Please enter a new root path (or just Enter to exit)'),
                              '', is_path_or_empty)
        if not d['path']:
            raise SystemExit(1)
    if "project" not in d:
        print()
        print(
            __(
                "Project name will occur in several places in the website, "
                "including blog archive pages and atom feeds. Later, you can "
                "set separate names for different parts of the website in "
                "configuration file."
            )
        )
        d["project"] = do_prompt(__("Project name"))
    if "author" not in d:
        print(
            __(
                "This of author as the copyright holder of the content. "
                "If your blog has multiple authors, you might want to enter "
                "a team name here. Later, you can specify individual authors "
                "using `blog_authors` configuration option."
            )
        )
        d["author"] = do_prompt(__("Author name(s)"))
    # Sphinx wants these but they don't make
    # that much sense for a blog
    d["release"] = d["version"] = ""
    while path.isfile(path.join(d['path'], d['master'] + d['suffix'])) or \
            path.isfile(path.join(d['path'], 'source', d['master'] + d['suffix'])):
        print()
        print(bold(__('Error: the master file %s has already been found in the '
                      'selected root path.') % (d['master'] + d['suffix'])))
        print(__('ABlog will not overwrite the existing file.'))
        print()
        d['master'] = do_prompt(__('Please enter a new file name, or rename the '
                                   'existing file and press Enter'), d['master'])
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
    if "blog_baseurl" not in d:
        print()
        print(
            __(
                "Please enter the base URL for your project. Blog feeds will "
                "be generated relative to this URL. If you don't have one yet, "
                "you can set it in configuration file later."
            )
        )
        d["blog_baseurl"] = do_prompt("Base URL for your project", None, lambda x: x)
    print()

def generate(
    d: dict, overwrite: bool = True, silent: bool = False,
) -> None:
    """
    Generate project based on values in *d*.
    """
    texescape.init()
    if 'mastertoctree' not in d:
        d['mastertoctree'] = ''
    if 'mastertocmaxdepth' not in d:
        d['mastertocmaxdepth'] = 2
    d["now"] = time.asctime()
    d['copyright'] = time.strftime('%Y') + ', ' + d['author']
    d['project_underline'] = column_width(d['project']) * '='
    d["path"] = os.path.abspath(d['path'])
    ensuredir(d['path'])
    srcdir = path.join(d['path'], 'source') if d['sep'] else d['path']
    ensuredir(srcdir)
    d["exclude_patterns"] = ""
    ensuredir(path.join(srcdir, d["dot"] + "templates"))
    ensuredir(path.join(srcdir, d["dot"] + "static"))

    # ABlog extras
    d["author_texescaped"] = texescape.escape(str(d["author"]).translate(str(d["author"])))
    d["project_doc"] = d["project"] + " Blog"
    d["project_doc_texescaped"] = texescape.escape(
        str(d["project"] + " Blog").translate(str(d["project"] + " Documentation"))
    )
    d["project_fn"] = make_filename(d["project"])
    d["project_manpage"] = d["project_fn"].lower()
    d["post_date"] = datetime.datetime.today().strftime("%b %d, %Y")

    def write_file(fpath: str, content: str, newline: str | None = None) -> None:
        if overwrite or not path.isfile(fpath):
            if 'quiet' not in d:
                print(__('Creating file %s.') % fpath)
            with open(fpath, 'w', encoding='utf-8', newline=newline) as f:
                f.write(content)
        else:
            if 'quiet' not in d:
                print(__('File %s already exists, skipping.') % fpath)
    conf_text = CONFIG.format(**d)
    write_file(path.join(srcdir, "conf.py"), conf_text)
    masterfile = path.join(srcdir, d["master"] + d["suffix"])
    write_file(masterfile, INDEX.format(**d))
    about = path.join(srcdir, "about" + d["suffix"])
    write_file(about, ABOUT.format(**d))
    firstpost = path.join(srcdir, "first-post" + d["suffix"])
    write_file(firstpost, POST.format(**d))
    if silent:
        return
    print()
    print(bold(__('Finished: An initial directory structure has been created.')))
    print()
    print(__('Use ``ablog build`` command within the new directory to build the blog, like so:\n    ablog build'))
    print()


def start_ablog(argv: Sequence[str] = (), /) -> int:
    locale.setlocale(locale.LC_ALL, '')
    sphinx.locale.init_console()
    if not color_terminal():
        nocolor()
    # parse options
    parser = get_parser()
    try:
        args = parser.parse_args(argv or sys.argv[1:])
    except SystemExit as err:
        return err.code
    d = vars(args)
    # delete None or False value
    d = {k: v for k, v in d.items() if v is not None}
    # handle use of CSV-style extension values
    d.setdefault('extensions', [])
    for ext in d['extensions'][:]:
        if ',' in ext:
            d['extensions'].remove(ext)
            d['extensions'].extend(ext.split(','))
    try:
        if 'quiet' in d:
            if not {'project', 'author'}.issubset(d):
                print(__('"quiet" is specified, but any of "project" or '
                         '"author" is not specified.'))
                return 1
        if {'quiet', 'project', 'author'}.issubset(d):
            # quiet mode with all required params satisfied, use default
            d.setdefault('version', '')
            d.setdefault('release', d['version'])
            d2 = CONFIG.copy()
            d2.update(d)
            d = d2
            if not valid_dir(d):
                print()
                print(bold(__('Error: specified path is not a directory, or ablog'
                              ' files already exist.')))
                print(__('ablog start only generate into a empty directory.'
                         ' Please specify a new root path.'))
                return 1
        else:
            ask_user(d)
    except (KeyboardInterrupt, EOFError):
        print()
        print('[Interrupted.]')
        return 130  # 128 + SIGINT
    for variable in d.get('variables', []):
        try:
            name, value = variable.split('=')
            d[name] = value
        except ValueError:
            print(__('Invalid template variable: %s') % variable)
    generate(d, overwrite=False)
    return 0
