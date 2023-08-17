import os
import sys
import glob
import shutil
import argparse
import webbrowser
import socketserver
from os import path
from http import server
from os.path import join, isfile, abspath
from datetime import date

from invoke import run
from watchdog.observers import Observer
from watchdog.tricks import ShellCommandTrick

import ablog
from ablog.start import ablog_start

__all__ = ["ablog_build", "ablog_clean", "ablog_serve", "ablog_deploy", "ablog_main"]

BUILDDIR = "_website"
DOCTREES = ".doctrees"
POST_TEMPLATE = """
{title}
{equal}

.. post:: {date}
   :tags:
   :category:

"""


def find_confdir(sourcedir=None):
    """
    Return path to current directory or its parent that contains conf.py.
    """
    confdir = sourcedir or os.getcwd()

    def parent(d):
        return abspath(join(d, ".."))

    while not isfile(join(confdir, "conf.py")) and confdir != parent(confdir):
        confdir = parent(confdir)
    conf = join(confdir, "conf.py")
    if isfile(conf) and "ablog" in open(conf).read():
        return confdir
    else:
        sys.exit("Current directory and its parents doesn't " "contain configuration file (conf.py).")


def read_conf(confdir):
    """
    Return conf.py file as a module.
    """
    sys.path.insert(0, confdir)
    conf = __import__("conf")
    sys.path.pop(0)
    return conf


parser = argparse.ArgumentParser(
    description="ABlog for blogging with Sphinx",
    epilog="See 'ablog <command> -h' for more information on a specific " "command.",
)
parser.add_argument("-v", "--version", help="print ABlog version and exit", action="version", version=ablog.__version__)
commands = ablog_commands = parser.add_subparsers(title="commands")


def cmd(func=None, **kwargs):
    if func is None:

        def cmd_inner(func):
            return cmd(func, **kwargs)

        return cmd_inner
    else:
        command = commands.add_parser(**kwargs)
        command.set_defaults(func=func)
        command.set_defaults(subparser=command)
        func.command = command
        return func


def arg(*args, **kwargs):
    if args and callable(args[0]):
        func = args[0]
        args = args[1:]
    else:
        func = None
    if func is None:

        def arg_inner(func):
            return arg(func, *args, **kwargs)

        return arg_inner
    else:
        func.command.add_argument(*args, **kwargs)
        return func


def arg_website(func):
    arg(
        func,
        "-w",
        dest="website",
        type=str,
        help=f"path for website, default is {BUILDDIR} when `ablog_website` is not set in conf.py",
    )
    return func


def arg_doctrees(func):
    arg(
        func,
        "-d",
        dest="doctrees",
        type=str,
        help="path for the cached environment and doctree files, "
        f"default {DOCTREES} when `ablog_doctrees` is not set in conf.py",
    )
    return func


cmd(
    ablog_start,
    name="start",
    help="start a new blog project",
    description="Start a new blog project by answering a few questions. "
    "You will end up with a configuration file and sample pages.",
)


@arg("-P", dest="runpdb", action="store_true", default=False, help="run pdb on exception")
@arg("-T", dest="traceback", action="store_true", default=False, help="show full traceback on exception")
@arg("-W", dest="werror", action="store_true", default=False, help="turn warnings into errors")
@arg("-N", dest="no_colors", action="store_true", default=False, help="do not emit colored output")
@arg("-Q", dest="extra_quiet", action="store_true", default=False, help="no output at all, not even warnings")
@arg(
    "-q",
    dest="quiet",
    action="store_true",
    default=False,
    help="no output on stdout, just warnings on stderr",
)
@arg("-v", dest="verbosity", action="count", default=0, help="increase verbosity (can be repeated)")
@arg_doctrees
@arg_website
@arg(
    "-s",
    dest="sourcedir",
    type=str,
    help="root path for source files, " "default is path to the folder that contains conf.py",
)
@arg("-b", dest="builder", type=str, help="builder to use, default `ablog_builder` or dirhtml")
@arg(
    "-a",
    dest="allfiles",
    action="store_true",
    default=False,
    help="write all files; default is to only write new and changed files",
)
@cmd(
    name="build",
    help="build your blog project",
    description="Path options can be set in conf.py. " "Default values of paths are relative to conf.py.",
)
def ablog_build(
    builder=None,
    sourcedir=None,
    website=None,
    doctrees=None,
    traceback=False,
    runpdb=False,
    allfiles=False,
    werror=False,
    verbosity=0,
    quiet=False,
    extra_quiet=False,
    no_colors=False,
    **kwargs,
):
    confdir = find_confdir(sourcedir)
    conf = read_conf(confdir)
    website = website or os.path.join(confdir, getattr(conf, "ablog_website", BUILDDIR))
    doctrees = doctrees or os.path.join(confdir, getattr(conf, "ablog_doctrees", DOCTREES))
    sourcedir = sourcedir or confdir
    argv = sys.argv[:1]
    argv.extend(["-b", builder or getattr(conf, "ablog_builder", "dirhtml")])
    argv.extend(["-d", doctrees])
    if traceback:
        argv.extend(["-T"])
    if runpdb:
        argv.extend(["-P"])
    if allfiles:
        argv.extend(["-a"])
    if werror:
        argv.extend(["-W"])
    if verbosity > 0:
        argv.extend(["-v"] * verbosity)
    if quiet:
        argv.extend(["-q"])
    if extra_quiet:
        argv.extend(["-Q"])
    if no_colors:
        argv.extend(["-N"])
    argv.extend([sourcedir, website])

    from sphinx.cmd.build import main

    sys.exit(main(argv[1:]))


@arg(
    "-D",
    dest="deep",
    action="store_true",
    default=False,
    help="deep clean, remove cached environment and doctree files",
)
@arg_doctrees
@arg_website
@cmd(
    name="clean",
    help="clean your blog build files",
    description="Path options can be set in conf.py. " "Default values of paths are relative to conf.py.",
)
def ablog_clean(website=None, doctrees=None, deep=False, **kwargs):
    confdir = find_confdir()
    conf = read_conf(confdir)
    website = website or os.path.join(confdir, getattr(conf, "ablog_website", BUILDDIR))
    doctrees = doctrees or os.path.join(confdir, getattr(conf, "ablog_doctrees", DOCTREES))
    nothing = True
    if glob.glob(os.path.join(website, "*")):
        shutil.rmtree(website)
        print(f"Removed {os.path.relpath(website)}.")
        nothing = False
    if deep and glob.glob(os.path.join(doctrees, "*")):
        shutil.rmtree(doctrees)
        print(f"Removed {os.path.relpath(doctrees)}.")
        nothing = False
    if nothing:
        print("Nothing to clean.")


@arg("--patterns", dest="patterns", default="*.rst;*.txt", help="patterns for triggering rebuilds")
@arg(
    "-r",
    dest="rebuild",
    action="store_true",
    default=False,
    help="rebuild when a file matching patterns change or get added",
)
@arg("-n", dest="view", action="store_false", default=True, help="do not open website in a new browser tab")
@arg("-p", dest="port", type=int, default=8000, help="port number for HTTP server; default is 8000")
@arg_website
@cmd(
    name="serve",
    help="serve and view your project",
    description="Serve options can be set in conf.py. " "Default values of paths are relative to conf.py.",
)
def ablog_serve(website=None, port=8000, view=True, rebuild=False, patterns="*.rst;*.txt", **kwargs):
    confdir = find_confdir()
    conf = read_conf(confdir)
    # to allow restarting the server in short succession
    socketserver.TCPServer.allow_reuse_address = True
    Handler = server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)
    ip, port = httpd.socket.getsockname()
    print(f"Serving HTTP on {ip}:{port}.")
    print("Quit the server with Control-C.")
    website = website or os.path.join(confdir, getattr(conf, "ablog_website", "_website"))
    os.chdir(website)
    if rebuild:
        patterns = patterns.split(";")
        ignore_patterns = [os.path.join(website, "*")]
        handler = ShellCommandTrick(
            shell_command="ablog build -s " + confdir,
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=False,
            wait_for_process=True,
            drop_during_process=False,
        )
        observer = Observer(timeout=1)
        observer.schedule(handler, confdir, recursive=True)
        observer.start()
        try:
            if view:
                webbrowser.open_new_tab(f"http://127.0.0.1:{port}") and httpd.serve_forever()
            else:
                httpd.serve_forever()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        if view:
            webbrowser.open_new_tab(f"http://127.0.0.1:{port}") and httpd.serve_forever()
        else:
            httpd.serve_forever()


@arg("-t", dest="title", type=str, help="post title; default is formed from filename")
@arg(dest="filename", type=str, help="filename, e.g. my-nth-post (.rst appended)")
@cmd(name="post", help="create a blank post")
def ablog_post(filename, title=None, **kwargs):
    # Generate basic post params.
    today = date.today()
    if not filename.lower().endswith(".rst"):
        filename += ".rst"
    today = today.strftime("%b %d, %Y")
    if not title:
        title = filename[:-4].replace("-", " ").title()
    pars = {"date": today, "title": title, "equal": "=" * len(title)}
    if path.isfile(filename):
        pass
    else:
        # read the file, and add post directive
        # and save it
        with open(filename, "w", encoding="utf-8") as out:
            post_text = POST_TEMPLATE.format(**pars)
            out.write(post_text)
        print(f"Blog post created: {filename}")


@arg(
    "--github-url",
    dest="github_url",
    type=str,
    default="git@github.com",
    help="Custom GitHub URL. Useful when multiple accounts are configured "
    "on the same machine. Default is: git@github.com",
)
@arg(
    "--github-token",
    dest="github_token",
    type=str,
    help="environment variable name storing GitHub access token",
)
@arg("--github-ssh", dest="github_is_http", action="store_true", help="use ssh when cloning website")
@arg(
    "--github-branch",
    dest="github_branch",
    type=str,
    help="Branch to use. Default is: master.",
    default="master",
)
@arg(
    "--push-quietly",
    dest="push_quietly",
    action="store_true",
    default=False,
    help="be more quiet when pushing changes",
)
@arg(
    "-f",
    dest="push_force",
    action="store_true",
    default=False,
    help="owerwrite last commit, i.e. `commit --amend; push -f`",
)
@arg("-m", dest="message", type=str, help="commit message")
@arg("-g", dest="github_pages", type=str, help="GitHub username for deploying to GitHub pages")
@arg(
    "-p",
    dest="repodir",
    type=str,
    help="path to the location of repository to be deployed, e.g. "
    "`../username.github.io`, default is folder containing `conf.py`",
)
@arg_website
@cmd(
    name="deploy",
    help="deploy your website build files",
    description="Path options can be set in conf.py. " "Default values of paths are relative to conf.py.",
)
def ablog_deploy(
    website,
    message=None,
    github_pages=None,
    push_quietly=False,
    push_force=False,
    github_token=None,
    github_is_http=True,
    github_url=None,
    github_branch=None,
    repodir=None,
    **kwargs,
):
    confdir = find_confdir()
    conf = read_conf(confdir)
    github_pages = github_pages or getattr(conf, "github_pages", None)
    github_url = github_url or getattr(conf, "github_url", None)
    github_url += ":"
    github_branch = github_branch or getattr(conf, "github_branch", "master")
    website = website or os.path.join(confdir, getattr(conf, "ablog_builddir", "_website"))
    tomove = glob.glob(os.path.join(website, "*"))
    if not tomove:
        print("Nothing to deploy, build first.")
        return
    if github_pages:
        if repodir is None:
            repodir = os.path.join(confdir, f"{github_pages}.github.io")
        if os.path.isdir(repodir):
            os.chdir(repodir)
            run("git pull", echo=True)
        else:
            run(
                "git clone "
                + ("https://github.com/" if github_is_http else github_url)
                + "{0}/{0}.github.io.git {1}".format(github_pages, repodir),
                echo=True,
            )
        git_add = []
        for tm in tomove:
            for root, dirnames, filenames in os.walk(website):
                for filename in filenames:
                    fn = os.path.join(root, filename)
                    fnnew = fn.replace(website, repodir)
                    try:
                        os.renames(fn, fnnew)
                    except OSError:
                        if os.path.isdir(fnnew):
                            shutil.rmtree(fnnew)
                        else:
                            os.remove(fnnew)
                        os.renames(fn, fnnew)

                    git_add.append(fnnew)
        print(f"Moved {len(git_add)} files to {github_pages}.github.io")
        os.chdir(repodir)
        run("git add -f " + " ".join(['"{}"'.format(os.path.relpath(p)) for p in git_add]), echo=True)
        if not os.path.isfile(".nojekyll"):
            open(".nojekyll", "w")
            run("git add -f .nojekyll")
        # Check to see if anything has actually been committed
        result = run("git diff --cached --name-status HEAD")
        if not result.stdout:
            print("Nothing changed from last deployment")
            return
        commit = f"git commit -m \"{message or 'Updates.'}\""
        if push_force:
            commit += " --amend"
        run(commit, echo=True)
        if github_token:
            with open(os.path.join(repodir, ".git/credentials"), "w") as out:
                out.write(f"https://{os.environ[github_token]}:@github.com")
            run('git config credential.helper "store --file=.git/credentials"')
        push = "git push"
        if push_quietly:
            push += " -q"
        if push_force:
            push += " -f"
        push += f" origin {github_branch}"
        run(push, echo=True)
    else:
        print("No place to deploy.")


def ablog_main():
    """
    Ablog Main.
    """
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        namespace = parser.parse_args()
        namespace.func(**namespace.__dict__)



def get_parser() -> argparse.ArgumentParser:
    description = __(
        "\n"
        "Generate required files for a Sphinx project.\n"
        "\n"
        "sphinx-quickstart is an interactive tool that asks some questions about your\n"
        "project and then generates a complete documentation directory and sample\n"
        "Makefile to be used with sphinx-build.\n",
    )
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTIONS] <PROJECT_DIR>',
        epilog=__("For more information, visit <https://www.sphinx-doc.org/>."),
        description=description)

    parser.add_argument('-q', '--quiet', action='store_true', dest='quiet',
                        default=None,
                        help=__('quiet mode'))
    parser.add_argument('--version', action='version', dest='show_version',
                        version='%%(prog)s %s' % __display_version__)

    parser.add_argument('path', metavar='PROJECT_DIR', default='.', nargs='?',
                        help=__('project root'))

    group = parser.add_argument_group(__('Structure options'))
    group.add_argument('--sep', action='store_true', dest='sep', default=None,
                       help=__('if specified, separate source and build dirs'))
    group.add_argument('--no-sep', action='store_false', dest='sep',
                       help=__('if specified, create build dir under source dir'))
    group.add_argument('--dot', metavar='DOT', default='_',
                       help=__('replacement for dot in _templates etc.'))

    group = parser.add_argument_group(__('Project basic options'))
    group.add_argument('-p', '--project', metavar='PROJECT', dest='project',
                       help=__('project name'))
    group.add_argument('-a', '--author', metavar='AUTHOR', dest='author',
                       help=__('author names'))
    group.add_argument('-v', metavar='VERSION', dest='version', default='',
                       help=__('version of project'))
    group.add_argument('-r', '--release', metavar='RELEASE', dest='release',
                       help=__('release of project'))
    group.add_argument('-l', '--language', metavar='LANGUAGE', dest='language',
                       help=__('document language'))
    group.add_argument('--suffix', metavar='SUFFIX', default='.rst',
                       help=__('source file suffix'))
    group.add_argument('--master', metavar='MASTER', default='index',
                       help=__('master document name'))
    group.add_argument('--epub', action='store_true', default=False,
                       help=__('use epub'))

    group = parser.add_argument_group(__('Extension options'))
    for ext in EXTENSIONS:
        group.add_argument('--ext-%s' % ext, action='append_const',
                           const='sphinx.ext.%s' % ext, dest='extensions',
                           help=__('enable %s extension') % ext)
    group.add_argument('--extensions', metavar='EXTENSIONS', dest='extensions',
                       action='append', help=__('enable arbitrary extensions'))

    group = parser.add_argument_group(__('Makefile and Batchfile creation'))
    group.add_argument('--makefile', action='store_true', dest='makefile', default=True,
                       help=__('create makefile'))
    group.add_argument('--no-makefile', action='store_false', dest='makefile',
                       help=__('do not create makefile'))
    group.add_argument('--batchfile', action='store_true', dest='batchfile', default=True,
                       help=__('create batchfile'))
    group.add_argument('--no-batchfile', action='store_false',
                       dest='batchfile',
                       help=__('do not create batchfile'))
    group.add_argument('-m', '--use-make-mode', action='store_true',
                       dest='make_mode', default=True,
                       help=__('use make-mode for Makefile/make.bat'))
    group.add_argument('-M', '--no-use-make-mode', action='store_false',
                       dest='make_mode',
                       help=__('do not use make-mode for Makefile/make.bat'))

    group = parser.add_argument_group(__('Project templating'))
    group.add_argument('-t', '--templatedir', metavar='TEMPLATEDIR',
                       dest='templatedir',
                       help=__('template directory for template files'))
    group.add_argument('-d', metavar='NAME=VALUE', action='append',
                       dest='variables',
                       help=__('define a template variable'))

    return parser


def main(argv: Sequence[str] = (), /) -> int:
    locale.setlocale(locale.LC_ALL, '')
    sphinx.locale.init_console()

    if not color_terminal():
        nocolor()

    # parse options
    parser = get_parser()
    try:
        args = parser.parse_args(argv or sys.argv[1:])
    except SystemExit as err:
        return err.code  # type: ignore[return-value]

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
            d2 = DEFAULTS.copy()
            d2.update(d)
            d = d2

            if not valid_dir(d):
                print()
                print(bold(__('Error: specified path is not a directory, or sphinx'
                              ' files already exist.')))
                print(__('sphinx-quickstart only generate into a empty directory.'
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

    generate(d, overwrite=False, templatedir=args.templatedir)
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
