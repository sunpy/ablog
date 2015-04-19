
import os
import sys
import glob
import ablog
import shutil
import argparse




def find_confdir(subparser):

    from os.path import isfile, join, abspath
    confdir = os.getcwd()

    parent = lambda d: abspath(join(d, '..'))

    while not isfile(join(confdir, 'conf.py')) and confdir != parent(confdir):

        confdir = parent(confdir)


    conf = join(confdir, 'conf.py')

    if isfile(conf) and 'ablog' in open(conf).read():
        return confdir
    else:
        subparser.exit("Current directory and its parents doesn't "
            "contain configuration file (conf.py).")


def read_conf(confdir):

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
    description="Start a new blog project with in less than 10 seconds. "
    "After answering a few questions, you will end up with a configuration "
    "file and sample pages.")


@arg('-T', dest='traceback',
    action='store_true', default=False,
    help="show full traceback on exception")
@arg_doctrees
@arg('-s', dest='sourcedir', type=str,
    help="root path for source files, "
        "default is path to the folder that contains conf.py")
@arg_website
@arg('-b', dest='builder', type=str,
    help="builder to use, default `ablog_builder` or dirhtml")
@cmd(name='build', help='build your blog project',
    description="Path options can be set in conf.py. "
    "Default values of paths are relative to conf.py.")
def ablog_build(subparser, **kwargs):

    confdir = find_confdir(subparser)
    conf = read_conf(confdir)
    website = (kwargs['website'] or
        os.path.join(confdir, getattr(conf, 'ablog_builddir', '_website')))
    doctrees = (kwargs['doctrees'] or
        os.path.join(confdir, getattr(conf, 'ablog_doctrees', '.doctrees')))
    sourcedir = (kwargs['sourcedir'] or confdir)
    argv = sys.argv[:1]
    argv.extend(['-b', kwargs['builder'] or getattr(conf, 'ablog_builder', 'dirhtml')])
    argv.extend(['-d', doctrees])
    if kwargs['traceback']:
        argv.extend(['-T'])
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
def ablog_clean(subparser, **kwargs):

    confdir = find_confdir(subparser)
    conf = read_conf(confdir)

    website = (kwargs['website'] or
        os.path.join(confdir, getattr(conf, 'ablog_builddir', '_website')))

    doctrees = (kwargs['doctrees'] or
        os.path.join(confdir, getattr(conf, 'ablog_doctrees', '.doctrees')))


    if glob.glob(os.path.join(website, '*')):
        shutil.rmtree(website)
        print('Removed {}.'.format(os.path.relpath(website)))
    else:
        print('Nothing to clean.')

    if kwargs['deep'] and glob.glob(os.path.join(doctrees, '*')):
        shutil.rmtree(doctrees)
        print('Removed {}.'.format(os.path.relpath(doctrees)))


@arg('-n', dest='view',
    action='store_false', default=True,
    help="do not open website in a new browser tab")
@arg('-p', dest='port', type=int, default=8000,
    help='port number for HTTP server; default is 8000')
@arg_website
@cmd(name='serve', help='serve and view your project',
    description="Serve options can be set in conf.py. "
    "Default values of paths are relative to conf.py.")
def ablog_serve(subparser, **kwargs):

    confdir = find_confdir(subparser)
    conf = read_conf(confdir)

    import SimpleHTTPServer
    import SocketServer
    import webbrowser


    port = kwargs['port']
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), Handler)

    ip, port = httpd.socket.getsockname()
    print("Serving HTTP on {}:{}.".format(ip, port))
    print("Quit the server with Control-C.")

    website = (kwargs['website'] or
        os.path.join(confdir, getattr(conf, 'ablog_builddir', '_website')))

    os.chdir(website)

    if kwargs['view']:
        (webbrowser.open_new_tab('http://127.0.0.1:{}'.format(port)) and
         httpd.serve_forever())
    else:
        httpd.serve_forever()



@arg('-t', dest='title', type=str,
    help='post title; default is formed from filename')
@arg(dest='filename', type=str,
    help='filename, e.g. my-nth-post (.rst appended)')
@cmd(name='post', help='create a blank post',)
def ablog_post(subparser, **kwargs):

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
    title = kwargs['title']
    filename = kwargs['filename']
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
@arg('--push-quietly', dest='push_quietly',
    action='store_true', default=False,
    help="be more quiet when pushing changes")
@arg('-m', dest='message', type=str,
    help="commit message")
@arg('-g', dest='github_pages', type=str,
    help="GitHub username for deploying to GitHub pages")
@arg_website
@cmd(name='deploy', help='deploy your website build files',
    description="Path options can be set in conf.py. "
    "Default values of paths are relative to conf.py.")
def ablog_deploy(subparser, **kwargs):

    confdir = find_confdir(subparser)
    conf = read_conf(confdir)

    github_pages = (kwargs['github_pages'] or
        getattr(conf, 'github_pages') or None)

    #from subprocess import call

    website = (kwargs['website'] or
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
                    os.renames(fn, fnnew)
                    git_add.append(fnnew)
        print('Moved {} files to {}.github.io'
            .format(len(git_add), github_pages))

        os.chdir(gitdir)

        run("git add -f " +
            " ".join([os.path.relpath(p) for p in git_add]), echo=True)
        if not os.path.isfile('.nojekyll'):
            open('.nojekyll', 'w')
            run("git add -f .nojekyll")

        run('git commit -m "{}"'.format(kwargs.get('message', 'Updates.'), echo=True))

        if kwargs['github_token']:
            with open(os.path.join(gitdir, '.git/credentials'), 'w') as out:
                out.write('https://{}:@github.com'
                    .format(os.environ[kwargs['github_token']]))
            run('git config credential.helper "store --file=.git/credentials"')
        push = 'git push'
        if kwargs['push_quietly']:
            push += ' -q'
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