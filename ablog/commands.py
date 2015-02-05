
import os
import sys
import ablog
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


class ABlogVersion(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):

        import ablog
        print("ABlog version " + ablog.__version__)
        parser.exit()


ablog_parser = argparse.ArgumentParser(
    description="ABlog for blogging with Sphinx",
    epilog="See 'ablog <command> -h' for more information on a specific "
           "command.")

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


if 0:
    def ablog_post(subparser, **kwargs):

        conf = read_conf(find_confdir(subparser))

        filename = kwargs['filename']
        title = kwargs['title']
        date_format = getattr(conf, 'post_date_format', '%b %d, %Y')

        # add template here and create file

        print('{} is ready to be edited.'.format(filename))

    subparser = ablog_commands.add_parser('post',
            help='post ',
            version=ablog.__version__)

    subparser.add_argument('filename', help='filename')

    subparser.add_argument('-t', '--title', dest='title', type=str,
        help='post title')

    subparser.set_defaults(func=lambda ns: ablog_post(**ns.__dict__))
    subparser.set_defaults(subparser=subparser)



def ablog_build(subparser, **kwargs):

    confdir = find_confdir(subparser)
    conf = read_conf(confdir)

    website = (kwargs['website'] or
        os.path.join(confdir, getattr(conf, 'ablog_builddir', '_website')))
    doctrees = (kwargs['doctrees'] or
        os.path.join(confdir, getattr(conf, 'ablog_doctrees', '_doctrees')))
    sourcedir = (kwargs['sourcedir'] or confdir)
    argv = sys.argv[:1]
    argv.extend(['-b', kwargs['builder'] or getattr(conf, 'ablog_builder', 'dirhtml')])
    argv.extend(['-d', doctrees])
    argv.extend([sourcedir, website])

    from sphinx import main
    main(argv)

subparser = ablog_commands.add_parser('build',
        help='build your blog project',
        description="Build options can be set in conf.py. "
        "Default values of paths are relative to conf.py.",
        version=ablog.__version__)

subparser.add_argument('-b', dest='builder', type=str,
    help="builder to use, default `ablog_builder` or dirhtml")

subparser.add_argument('-d', dest='doctrees', type=str,
    default='_doctrees',
    help="path for the cached environment and doctree files, "
        "default `ablog_doctrees` or _doctrees")

subparser.add_argument('-s', dest='sourcedir', type=str,
    help="root path for source files, "
        "default is path to the folder that contains conf.py")

subparser.add_argument('-w', dest='website', type=str,
    help="path for website, default `ablog_website` or _website")


subparser.set_defaults(func=lambda ns: ablog_build(**ns.__dict__))
subparser.set_defaults(subparser=subparser)



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

subparser = ablog_commands.add_parser('serve',
        help='serve and view your project',
        description="Serve options can be set in conf.py. "
        "Default values of paths are relative to conf.py.",
        version=ablog.__version__)

subparser.add_argument('-n', dest='view',
        action='store_false', default=True,
        help="do not open website in a new browser tab")

subparser.add_argument('-p', dest='port', type=int,
    default=8000,
    help='port number for HTTP server; default is 8000')

subparser.add_argument('-w', dest='website', type=str,
    help="path for website, "
        "default `ablog_website` or _website")

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