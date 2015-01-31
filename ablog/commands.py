
import sys
import argparse


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


try:
    from .quickstart import main as start_main
except:
    pass
else:
    ablog_commands = ablog_parser.add_subparsers(
        title='subcommands')

    subparser = ablog_commands.add_parser('start',
            help='start a new blog project')
    subparser.set_defaults(func=lambda ns: start_main([]))
    subparser.set_defaults(subparser=subparser)


subparser = ablog_commands.add_parser('build',
        help='build your blog project')
subparser.set_defaults(func=lambda ns: main([]))
subparser.set_defaults(subparser=subparser)



def ablog_main():

    if len(sys.argv) == 1:
        ablog_parser.print_help()
    else:
        namespace = ablog_parser.parse_args()
        namespace.func(namespace)


if __name__ == '__main__':
    ablog_main()