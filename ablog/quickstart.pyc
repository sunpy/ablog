# -*- coding: utf-8 -*-
"""
    ablog.quickstart
    ~~~~~~~~~~~~~~~~~

    Quickly setup documentation source to work with Ablog.

    :copyright: Copyright 2007-2015 by ?
    :license: ?
"""
import sys
import inspect
import optparse
from os import path



from sphinx import quickstart as sphinx_quickstart

from sphinx.util.console import purple, bold, red, turquoise, nocolor, color_terminal
USAGE = """\
Sphinx v%s
Usage: %%prog [options] [projectdir]
""" % sphinx_quickstart.__version__

EPILOG = """\
For more information, visit <http://sphinx-doc.org/>.
"""
DEFAULT_VALUE = {
    'path': '.',
    'sep': False,
    'dot': '_',
    'language': None,
    'suffix': '.rst',
    'master': 'index',
    'epub': False,
    'ext_autodoc': False,
    'ext_doctest': False,
    'makefile': True,
    'batchfile': True,
    'ext_ablog': True
    }

EXTENSIONS = ('autodoc', 'doctest', 'intersphinx', 'todo', 'coverage',
              'pngmath', 'mathjax', 'ifconfig', 'viewcode', 'ablog')

class MyFormatter(optparse.IndentedHelpFormatter):
    def format_usage(self, usage):
        return usage

    def format_help(self, formatter):
        result = []
        if self.description:
            result.append(self.format_description(formatter))
        if self.option_list:
            result.append(self.format_option_help(formatter))
        return "\n".join(result)
    
def sphinx_quickstart_main(argv=sys.argv):
    '''Borrowed from Sphinx 1.3b3'''
    if not color_terminal():
        nocolor()

    parser = optparse.OptionParser(USAGE, epilog=EPILOG,
                                   version='Sphinx v%s' % sphinx_quickstart.__version__,
                                   formatter=MyFormatter())
    parser.add_option('-q', '--quiet', action='store_true', dest='quiet',
                      default=False,
                      help='quiet mode')

    group = parser.add_option_group('Structure options')
    group.add_option('--sep', action='store_true', dest='sep',
                     help='if specified, separate source and build dirs')
    group.add_option('--dot', metavar='DOT', dest='dot',
                     help='replacement for dot in _templates etc.')

    group = parser.add_option_group('Project basic options')
    group.add_option('-p', '--project', metavar='PROJECT', dest='project',
                     help='project name')
    group.add_option('-a', '--author', metavar='AUTHOR', dest='author',
                     help='author names')
    group.add_option('-v', metavar='VERSION', dest='version',
                     help='version of project')
    group.add_option('-r', '--release', metavar='RELEASE', dest='release',
                     help='release of project')
    group.add_option('-l', '--language', metavar='LANGUAGE', dest='language',
                     help='document language')
    group.add_option('--suffix', metavar='SUFFIX', dest='suffix',
                     help='source file suffix')
    group.add_option('--master', metavar='MASTER', dest='master',
                     help='master document name')
    group.add_option('--epub', action='store_true', dest='epub',
                     default=False,
                     help='use epub')

    group = parser.add_option_group('Extension options')
    for ext in EXTENSIONS:
        group.add_option('--ext-' + ext, action='store_true',
                         dest='ext_' + ext, default=False,
                         help='enable %s extension' % ext)

    group = parser.add_option_group('Makefile and Batchfile creation')
    group.add_option('--makefile', action='store_true', dest='makefile',
                     default=False,
                     help='create makefile')
    group.add_option('--no-makefile', action='store_true', dest='no_makefile',
                     default=False,
                     help='not create makefile')
    group.add_option('--batchfile', action='store_true', dest='batchfile',
                     default=False,
                     help='create batchfile')
    group.add_option('--no-batchfile', action='store_true', dest='no_batchfile',
                     default=False,
                     help='not create batchfile')

    # parse options
    try:
        opts, args = parser.parse_args()
    except SystemExit as err:
        return err.code

    if len(args) > 0:
        opts.ensure_value('path', args[0])

    d = vars(opts)
    for k, v in list(d.items()):
        # delete None or False value
        if v is None or v is False:
            del d[k]

    try:
        if 'quiet' in d:
            if 'project' not in d or 'author' not in d or \
               'version' not in d:
                print('''"quiet" is specified, but any of "project", \
"author" or "version" is not specified.''')
                return

        if all(['quiet' in d, 'project' in d, 'author' in d,
                'version' in d]):
            # quiet mode with all required params satisfied, use default
            d.setdefault('release', d['version'])
            d2 = DEFAULT_VALUE.copy()
            d2.update(dict(("ext_"+ext, False) for ext in EXTENSIONS))
            d2.update(d)
            d = d2
            if 'no_makefile' in d:
                d['makefile'] = False
            if 'no_batchfile' in d:
                d['batchfile'] = False

            if path.exists(d['path']) and (
                    not path.isdir(d['path']) or os.listdir(d['path'])):
                print()
                print(bold('Error: specified path is not a directory, or not a'
                           ' empty directory.'))
                print('sphinx-quickstart only generate into a empty directory.'
                      ' Please specify a new root path.')
                return
        else:
            sphinx_quickstart.ask_user(d)
    except (KeyboardInterrupt, EOFError):
        print()
        print('[Interrupted.]')
        return
    sphinx_quickstart.generate(d)


def main(argv=sys.argv):
    
    sphinx_quickstart_main(argv)
    
   
    