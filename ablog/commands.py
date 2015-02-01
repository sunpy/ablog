
import os
import sys
import ablog
import argparse


def find_confdir():

    from os.path import isfile, join, abspath
    confdir = os.getcwd()

    parent = lambda d: abspath(join(d, '..'))

    while not isfile(join(confdir, 'conf.py')) and confdir != parent(confdir):

        confdir = parent(confdir)


    conf = join(confdir, 'conf.py')

    if isfile(conf) and 'ablog' in open(conf).read():
        return confdir
    else:
        return None



class ABlogVersion(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):

        import ablog
        print("ABlog version " + ablog.__version__)
        parser.exit()


ablog_parser = argparse.ArgumentParser(
    description="ABlog for blogging with Sphinx",
    epilog="See 'ablog <command> -h' for more information on a specific "
           "command."
    )

ablog_parser.add_argument('-v', '--version',
    help="print ABlog version and exit",
    action=ABlogVersion, nargs=0)


from .start import ablog_start
ablog_commands = ablog_parser.add_subparsers(
    title='subcommands')
subparser = ablog_commands.add_parser('start',
        help='start a new blog project')
subparser.set_defaults(func=lambda ns: ablog_start())
subparser.set_defaults(subparser=subparser)


def ablog_build(**kwargs):

    argv = sys.argv[:1]
    argv.extend(['-b', kwargs['builder']])
    argv.extend(['-d', kwargs['doctrees']])
    argv.extend(['.', kwargs['outdir']])

    from sphinx import main
    main(argv)

subparser = ablog_commands.add_parser('build',
        help='build your blog project',
        version=ablog.__version__)

subparser.add_argument('-b', '--builder', dest='builder', type=str,
    default='dirhtml',
    help='sphinx builder to use; default is `dirhtml`')

subparser.add_argument('-d', '--doctrees', dest='doctrees', type=str,
    default='_doctrees',
    help='path for the cached environment and doctree files; default is `_doctrees`')

subparser.add_argument('-o', '--outdir', dest='outdir', type=str,
    default='_output',
    help='path for your; default is `_output`')


subparser.set_defaults(func=lambda ns: ablog_build(**ns.__dict__))
subparser.set_defaults(subparser=subparser)



def ablog_serve(subparser, **kwargs):

    confdir = find_confdir()
    if not confdir:
        subparser.exit('Configuration file (conf.py) could not be found '
            'in the current working directory and its parents.')

    import SimpleHTTPServer
    import SocketServer
    import webbrowser


    PORT = kwargs['port']
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)

    sa = httpd.socket.getsockname()

    msg = "Serving HTTP on", sa[0], "port", sa[1], "..."
    print(msg)
    print("Quit the server with CONTROL-C.")

    outdir = os.path.join(confdir, kwargs['outdir'])

    os.chdir(outdir)

    (webbrowser.open_new_tab('http://127.0.0.1:8000') and
     httpd.serve_forever())


subparser = ablog_commands.add_parser('serve',
        help='serve your project locally',
        version=ablog.__version__)

subparser.add_argument('-o', '--outdir', dest='outdir', type=str,
    default='_output',
    help='path to your project built directory; default is `_output`')

subparser.add_argument('-p', '--port', dest='port', type=int,
    default=8000,
    help='port number for HTTP server; default is 8000')

subparser.set_defaults(func=lambda ns: ablog_serve(**ns.__dict__))
subparser.set_defaults(subparser=subparser)




def ablog_main():


    if len(sys.argv) == 1:
        ablog_parser.print_help()
    else:
        namespace = ablog_parser.parse_args()
        namespace.func(namespace)


if __name__ == '__main__':
    ablog_main()