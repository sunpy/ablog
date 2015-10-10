import os
import sys
import glob
import ablog
import shutil
import argparse


def find_confdir():
    """Return path to current directory or its parent that contains conf.py"""

    from os.path import isfile, join, abspath
    confdir = os.getcwd()

    parent = lambda d: abspath(join(d, '..'))

    while not isfile(join(confdir, 'conf.py')) and confdir != parent(confdir):
        confdir = parent(confdir)

    conf = join(confdir, 'conf.py')

    if isfile(conf) and 'ablog' in open(conf).read():
        return confdir
    else:
        sys.exit("Current directory and its parents doesn't "
            "contain configuration file (conf.py).")


def read_conf(confdir):
    """Return conf.py file as a module."""

    sys.path.insert(0, confdir)
    conf = __import__('conf')
    sys.path.pop(0)
    return conf


parser = argparse.ArgumentParser(
    description="ABlog for blogging with Sphinx",
    epilog="See 'ablog <command> -h' for more information on a specific "
           "command.")

parser.add_argument('-v', '--version',
    help="print ABlog version and exit",
    action='version', version=ablog.__version__)


commands = ablog_commands = parser.add_subparsers(title='commands')

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

    arg(func, '-w', dest='website', type=str,
        help="path for website, default is _website when `ablog_website` "
            "is not set in conf.py")
    return func

def arg_doctrees(func):

    arg(func, '-d', dest='doctrees', type=str, default='.doctrees',
        help="path for the cached environment and doctree files, "
            "default .doctrees when `ablog_doctrees` is not set in conf.py")
    return func


from .start import ablog_start
cmd(ablog_start, name='start', help='start a new blog project',
    description="Start a new blog project by answering a few questions. "
    "You will end up with a configuration file and sample pages.")


@arg('-P', dest='runpdb',
    action='store_true', default=False,
    help="run pdb on exception")
@arg('-T', dest='traceback',
    action='store_true', default=False,
    help="show full traceback on exception")
@arg_doctrees
@arg_website
@arg('-s', dest='sourcedir', type=str,
    help="root path for source files, "
        "default is path to the folder that contains conf.py")
@arg('-b', dest='builder', type=str,
    help="builder to use, default `ablog_builder` or dirhtml")
@arg('-a', dest='allfiles',     action='store_true', default=False,
    help="write all files; default is to only write new and changed files")
@cmd(name='build', help='build your blog project',
    description="Path options can be set in conf.py. "
    "Default values of paths are relative to conf.py.")
def ablog_build(builder=None, sourcedir=None, website=None, doctrees=None,
    traceback=False, runpdb=False, allfiles=False, **kwargs):

    confdir = find_confdir()
    conf = read_conf(confdir)
    website = (website or
        os.path.join(confdir, getattr(conf, 'ablog_builddir', '_website')))
    doctrees = (doctrees or
        os.path.join(confdir, getattr(conf, 'ablog_doctrees', '.doctrees')))
    sourcedir = (sourcedir or confdir)
    argv = sys.argv[:1]
    argv.extend(['-b', builder or getattr(conf, 'ablog_builder', 'dirhtml')])
    argv.extend(['-d', doctrees])
    if traceback:
        argv.extend(['-T'])
    if runpdb:
        argv.extend(['-P'])
    if allfiles:
        argv.extend(['-a'])
    argv.extend([sourcedir, website])

    from sphinx import main
    main(argv)


@arg('-D', dest='deep', action='store_true', default=False,
    help="deep clean, remove cached environment and doctree files")
@arg_doctrees
@arg_website
@cmd(name='clean', help='clean your blog build files',
    description="Path options can be set in conf.py. "
    "Default values of paths are relative to conf.py.")
def ablog_clean(website=None, doctrees=None, deep=False, **kwargs):

    confdir = find_confdir()
    conf = read_conf(confdir)

    website = (website or
        os.path.join(confdir, getattr(conf, 'ablog_builddir', '_website')))

    doctrees = (doctrees or
        os.path.join(confdir, getattr(conf, 'ablog_doctrees', '.doctrees')))

    nothing = True
    if glob.glob(os.path.join(website, '*')):
        shutil.rmtree(website)
        print('Removed {}.'.format(os.path.relpath(website)))
        nothing = False

    if deep and glob.glob(os.path.join(doctrees, '*')):
        shutil.rmtree(doctrees)
        print('Removed {}.'.format(os.path.relpath(doctrees)))
        nothing = False

    if nothing:
        print('Nothing to clean.')


@arg('--patterns', dest='rebuild', action='store_false', default='*.rst;*.txt',
    help="patterns for triggering rebuilds")
@arg('-r', dest='rebuild', action='store_true', default=False,
    help="rebuild when a file matching patterns change or get added")
@arg('-n', dest='view', action='store_false', default=True,
    help="do not open website in a new browser tab")
@arg('-p', dest='port', type=int, default=8000,
    help='port number for HTTP server; default is 8000')
@arg_website
@cmd(name='serve', help='serve and view your project',
    description="Serve options can be set in conf.py. "
    "Default values of paths are relative to conf.py.")
def ablog_serve(website=None, port=8000, view=True, rebuild=False,
    patterns='*.rst;*.txt', **kwargs):

    confdir = find_confdir()
    conf = read_conf(confdir)

    try:
        import SimpleHTTPServer as server
    except ImportError:
        from http import server
        import socketserver
    else:
        import SocketServer as socketserver

    import webbrowser

    Handler = server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler)

    ip, port = httpd.socket.getsockname()
    print("Serving HTTP on {}:{}.".format(ip, port))
    print("Quit the server with Control-C.")

    website = (website or
        os.path.join(confdir, getattr(conf, 'ablog_builddir', '_website')))

    os.chdir(website)

    if rebuild:

        #from watchdog.watchmedo import observe_with
        from watchdog.observers import Observer
        from watchdog.tricks import ShellCommandTrick
        patterns = patterns.split(';')
        ignore_patterns = [os.path.join(website, '*')]
        handler = ShellCommandTrick(shell_command='ablog build',
                                    patterns=patterns,
                                    ignore_patterns=ignore_patterns,
                                    ignore_directories=False,
                                    wait_for_process=True,
                                    drop_during_process=False)

        observer = Observer(timeout=1)
        observer.schedule(handler, confdir, recursive=True)
        observer.start()
        try:
            if view:
                (webbrowser.open_new_tab('http://127.0.0.1:{}'.format(port)) and
                 httpd.serve_forever())
            else:
                httpd.serve_forever()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


    else:
        if view:
            (webbrowser.open_new_tab('http://127.0.0.1:{}'.format(port)) and
             httpd.serve_forever())
        else:
            httpd.serve_forever()


@arg('-t', dest='title', type=str,
    help='post title; default is formed from filename')
@arg(dest='filename', type=str,
    help='filename, e.g. my-nth-post (.rst appended)')
@cmd(name='post', help='create a blank post',)
def ablog_post(filename, title=None, **kwargs):

    POST_TEMPLATE =u'''
%(title)s
%(equal)s

.. post:: %(date)s
   :tags:
   :category:

'''
    from datetime import date
    from os import path

    #Generate basic post params.
    today = date.today()
    if not filename.lower().endswith('.rst'):
        filename += '.rst'

    today = today.strftime("%b %d, %Y")
    if not title:
        title = filename[:-4].replace('-', ' ').title()

    pars = {'date': today,
            'title': title,
            'equal': '=' * len(title)
            }

    if path.isfile(filename):
        pass
        # read the file, and add post directive
        # and save it
    else:
        with open(filename, 'w') as out:
            post_text = POST_TEMPLATE % pars
            out.write(post_text)

        print('Blog post created: %s' % filename)


@arg('--github-token', dest='github_token', type=str,
    help="environment variable name storing GitHub access token")
@arg('--push-quietly', dest='push_quietly', action='store_true', default=False,
    help="be more quiet when pushing changes")
@arg('-f', dest='push_force', action='store_true', default=False,
    help="owerwrites last commit, as 'commit --amend' and 'push -f'")
@arg('-m', dest='message', type=str, help="commit message")
@arg('-g', dest='github_pages', type=str,
    help="GitHub username for deploying to GitHub pages")
@arg_website
@cmd(name='deploy', help='deploy your website build files',
    description="Path options can be set in conf.py. "
    "Default values of paths are relative to conf.py.")
def ablog_deploy(website, message=None, github_pages=None,
    push_quietly=False, push_force=False, github_token=None, **kwargs):

    confdir = find_confdir()
    conf = read_conf(confdir)

    github_pages = (github_pages or getattr(conf, 'github_pages') or None)

    website = (website or
        os.path.join(confdir, getattr(conf, 'ablog_builddir', '_website')))

    tomove = glob.glob(os.path.join(website, '*'))
    if not tomove:
        print('Nothing to deploy, build first.')
        return

    try:
        from invoke import run
    except ImportError:
        raise ImportError("invoke is required by deploy command, "
            "run `pip install invoke`")


    if github_pages:

        gitdir = os.path.join(confdir, "{0}.github.io".format(github_pages))
        if os.path.isdir(gitdir):
            os.chdir(gitdir)
            run("git pull", echo=True)
        else:
            run("git clone https://github.com/{0}/{0}.github.io.git"
                .format(github_pages), echo=True)

        git_add = []
        for tm in tomove:
            for root, dirnames, filenames in os.walk(website):
                for filename in filenames:
                    fn = os.path.join(root, filename)
                    fnnew = fn.replace(website, gitdir)
                    try:
                        os.renames(fn, fnnew)
                    except OSError:
                        if os.path.isdir(fnnew):
                            shutil.rmtree(fnnew)
                        else:
                            os.remove(fnnew)
                        os.renames(fn, fnnew)

                    git_add.append(fnnew)
        print('Moved {} files to {}.github.io'
            .format(len(git_add), github_pages))

        os.chdir(gitdir)

        run("git add -f " + " ".join(['"{}"'.format(os.path.relpath(p))
                                      for p in git_add]), echo=True)
        if not os.path.isfile('.nojekyll'):
            open('.nojekyll', 'w')
            run("git add -f .nojekyll")

        commit = 'git commit -m "{}"'.format(message or 'Updates.')
        if push_force:
            commit += ' --amend'
        run(commit, echo=True)

        if github_token:
            with open(os.path.join(gitdir, '.git/credentials'), 'w') as out:
                out.write('https://{}:@github.com'
                    .format(os.environ[github_token]))
            run('git config credential.helper "store --file=.git/credentials"')
        push = 'git push'
        if push_quietly:
            push += ' -q'
        if push_force:
            push += ' -f'
        push += ' origin master'
        run(push, echo=True)

    else:
        print('No place to deploy.')


def ablog_main():

    if len(sys.argv) == 1:
        parser.print_help()
    else:
        namespace = parser.parse_args()
        namespace.func(**namespace.__dict__)


if __name__ == '__main__':
    ablog_main()
