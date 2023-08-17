
import sys
import time
import datetime
from os import path
from textwrap import wrap
from __future__ import annotations
from docutils.utils import column_width

import sphinx.locale
from sphinx import __display_version__, package_dir
from sphinx.locale import __
from sphinx.util.console import (  # type: ignore[attr-defined]
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

__all__ = ["do_prompt", "is_path", "is_path_or_empty", "allow_empty", "nonempty", "choice", "boolean", "suffix", "ok", "ValidationError", "valid_dir"]

try:
    import readline
    if TYPE_CHECKING and sys.platform == "win32":  # always false, for type checking
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

if sys.platform == 'win32':
    # On Windows, show questions as bold because of color scheme of PowerShell (refs: #5294).
    COLOR_QUESTION = 'bold'
else:
    COLOR_QUESTION = 'purple'

PROMPT_PREFIX = '> '

class ValidationError(Exception):
    """
    Raised for validation errors.
    """

def term_input(prompt: str) -> str:
    """
    Get input from the terminal.

    Parameters
    ----------
    prompt : str
        Prompt to show.

    Returns
    -------
    str
        Input from the terminal.
    """
    if sys.platform == 'win32':
        # Important: On windows, readline is not enabled by default.
        # In these environment, escape sequences have been broken.
        # To avoid the problem, use ``print()`` to show prompt.
        print(prompt, end='')
        return input('')
    return input(prompt)


def is_path(x: str) -> str:
    x = path.expanduser(x)
    if not path.isdir(x):
        raise ValidationError(__("Please enter a valid path name."))
    return x


def is_path_or_empty(x: str) -> str:
    if x == '':
        return x
    return is_path(x)


def allow_empty(x: str) -> str:
    return x


def nonempty(x: str) -> str:
    if not x:
        raise ValidationError(__("Please enter some text."))
    return x


def choice(*l: str) -> Callable[[str], str]:
    def val(x: str) -> str:
        if x not in l:
            raise ValidationError(__('Please enter one of %s.') % ', '.join(l))
        return x
    return val


def boolean(x: str) -> bool:
    if x.upper() not in ('Y', 'YES', 'N', 'NO'):
        raise ValidationError(__("Please enter either 'y' or 'n'."))
    return x.upper() in ('Y', 'YES')


def suffix(x: str) -> str:
    if not (x[0:1] == '.' and len(x) > 1):
        raise ValidationError(__("Please enter a file suffix, e.g. '.rst' or '.txt'."))
    return x


def ok(x: str) -> str:
    return x


def do_prompt(
    text: str, default: str | None = None, validator: Callable[[str], Any] = nonempty,
) -> str | bool:
    while True:
        if default is not None:
            prompt = PROMPT_PREFIX + f'{text} [{default}]: '
        else:
            prompt = PROMPT_PREFIX + text + ': '
        if USE_LIBEDIT:
            # Note: libedit has a problem for combination of ``input()`` and escape
            # sequence (see #5335).  To avoid the problem, all prompts are not colored
            # on libedit.
            pass
        elif READLINE_AVAILABLE:
            # pass input_mode=True if readline available
            prompt = colorize(COLOR_QUESTION, prompt, input_mode=True)
        else:
            prompt = colorize(COLOR_QUESTION, prompt, input_mode=False)
        x = term_input(prompt).strip()
        if default and not x:
            x = default
        try:
            x = validator(x)
        except ValidationError as err:
            print(red('* ' + str(err)))
            continue
        break
    return x



def valid_dir(d: dict) -> bool:
    dir = d['path']
    if not path.exists(dir):
        return True
    if not path.isdir(dir):
        return False

    if {'Makefile', 'make.bat'} & set(os.listdir(dir)):
        return False

    if d['sep']:
        dir = os.path.join('source', dir)
        if not path.exists(dir):
            return True
        if not path.isdir(dir):
            return False

    reserved_names = [
        'conf.py',
        d['dot'] + 'static',
        d['dot'] + 'templates',
        d['master'] + d['suffix'],
    ]
    if set(reserved_names) & set(os.listdir(dir)):
        return False

    return True
