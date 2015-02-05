
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

def ablog_post(subparser, **kwargs):

    POST_TEMPLATE =u'''
%(post_title)s
====================
.. post:: %(post_date)s
'''

    # We may need to augment this to use a specified folder
    blog_root = find_confdir()
    if(not blog_root):
        print('Configuration file (conf.py) could not be found '
            'in the current working directory and its parents.')
        sys.exit(1)
    

   
    from datetime import date
    from os import path

    #Generate basic post params.
    today = date.today()
    title = kwargs['post_title'].split('.')[0]
    body = kwargs['post_body']
    file_name = "{}_{}.rst".format(title.replace(' ', '_'), today).lower()
    file_path = path.join(blog_root, file_name)
    today = today.strftime("%b %d, %Y")
    
    pars = {'post_date': today,
            'post_title': title
            }
    
    print('Creating blog post in %s' % blog_root)

    #Check if we have the file in the target folder and rename accordingly
    #leaving the original in tact
    if path.isfile(file_path):
        import random
        from os import listdir
        file_base_name = path.splitext(path.basename(file_path))[0]
        file_ext = path.splitext(path.basename(file_path))[1]
        file_base_path = path.dirname(file_path)
        existing_posts = [f for f in listdir(blog_root) 
                            if '.rst' in f and path.isfile(f) and file_base_name in f]
        file_base_name += '_' + str(len(existing_posts)) + file_ext
        file_path = path.join(file_base_path, file_base_name)
        

    try:
        post_file = open(file_path, 'w')
        post_text = POST_TEMPLATE % pars
        post_text += ("\n%s" % body)
        post_file.write(post_text)

        print('Blog post template created: %s\n' % path.basename(file_path))
    except Exception, e:
        #This may be an access right issue or something along the lines.
        print(e)
        raise e
    finally:
        if(post_file):
            post_file.close()
    

    


subparser = ablog_commands.add_parser('post',
        help='creates a blank post with today''s date',
        version=ablog.__version__)

subparser.add_argument('-t', '--title', dest='post_title', type=str,
    default='New Post',
    help='path to your project built directory; default is `New Post`')
subparser.add_argument('-b', '--body', dest='post_body', type=str,
    default='',
    help='path to your project built directory; default is blank.')
subparser.set_defaults(func=lambda ns: ablog_post(**ns.__dict__))
subparser.set_defaults(subparser=subparser)



def ablog_main():


    if len(sys.argv) == 1:
        ablog_parser.print_help()
    else:
        namespace = ablog_parser.parse_args()
        namespace.func(namespace)


if __name__ == '__main__':
    ablog_main()