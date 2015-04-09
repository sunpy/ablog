.. _commands:

ABlog Commands
==============

.. post:: Mar 1, 2015
   :tags: config, commands
   :author: Ahmet, Mehmet
   :category: Manual
   :location: SF


``ablog`` commands are for streamlining blog operations, i.e. building, serving,
and viewing blog pages, as well as starting a new blog.

::

  $ ablog
  usage: ablog [-h] [-v] {start,build,clean,serve,post,deploy} ...

  ABlog for blogging with Sphinx

  optional arguments:
    -h, --help            show this help message and exit
    -v, --version         print ABlog version and exit

  subcommands:
    {start,build,clean,serve,post,deploy}
      start               start a new blog project
      build               build your blog project
      clean               clean your blog build files
      serve               serve and view your project
      post                create a blank post
      deploy              deploy your website build files

  See 'ablog <command> -h' for more information on a specific command.




.. contents:: Here are all the things you can do:
   :local:
   :backlinks: top

Start a Project
---------------

``ablog start`` command is for quickly setting up a blog project. See
:ref:`quick-start` for how it works and what it prepares for you.


::

  $ ablog start -h
  usage: ablog start [-h]

  Start a new blog project with in less than 10 seconds. After answering a few
  questions, you will end up with a configuration file and sample pages.

  optional arguments:
    -h, --help  show this help message and exit



Build your Website
------------------

Running ``ablog build`` in your project folder builds your website HTML pages.

::

  $ ablog build -h
  usage: ablog build [-h] [-b BUILDER] [-d DOCTREES] [-s SOURCEDIR] [-w WEBSITE]
                     [-T]

  Path options can be set in conf.py. Default values of paths are relative to
  conf.py.

  optional arguments:
    -h, --help    show this help message and exit
    -b BUILDER    builder to use, default `ablog_builder` or dirhtml
    -d DOCTREES   path for the cached environment and doctree files, default
                  .doctrees when `ablog_doctrees` is not set in conf.py
    -s SOURCEDIR  root path for source files, default is path to the folder that
                  contains conf.py
    -w WEBSITE    path for website, default is _website when `ablog_website` is
                  not set in conf.py
    -T            show full traceback on exception

Serve and View
--------------

Running ``ablog serve``, after building your website, will start a Python
server and open up browser tab to view your website.

::

  $ ablog serve -h
  usage: ablog serve [-h] [-n] [-p PORT] [-w WEBSITE]

  Serve options can be set in conf.py. Default values of paths are relative to
  conf.py.

  optional arguments:
    -h, --help  show this help message and exit
    -n          do not open website in a new browser tab
    -p PORT     port number for HTTP server; default is 8000
    -w WEBSITE  path for website, default is _website when `ablog_website` is
                not set in conf.py

.. _deploy:

Deploy Website
--------------

Running ``ablog deploy`` will push your website to GitHub.

::

  $ ablog deploy -h
  usage: ablog deploy [-h] [-g GITHUB_PAGES] [-w WEBSITE]

  Path options can be set in conf.py. Default values of paths are relative to
  conf.py.

  optional arguments:
    -h, --help       show this help message and exit
    -g GITHUB_PAGES  GitHub user name for deploying to GitHub pages
    -w WEBSITE       path for website, default is _website when `ablog_website`
                     is not set in conf.py

Create a Post
-------------

Finally, ``ablog post`` will make a new post template file.

::

  $ ablog post -h
  usage: ablog post [-h] [-t TITLE] filename

  positional arguments:
    filename    filename, e.g. my-nth-post.rst

  optional arguments:
    -h, --help  show this help message and exit
    -t TITLE    post title; default is `New Post

Clean Files
-----------

In case you needed, running ``ablog clean`` will remove build files and
do a deep clean with ``-D`` option.

::

  $ ablog clean -h
  usage: ablog clean [-h] [-d DOCTREES] [-w WEBSITE] [-D]

  Path options can be set in conf.py. Default values of paths are relative to
  conf.py.

  optional arguments:
    -h, --help   show this help message and exit
    -d DOCTREES  path for the cached environment and doctree files, default
                 .doctrees when `ablog_doctrees` is not set in conf.py
    -w WEBSITE   path for website, default is _website when `ablog_website` is
                 not set in conf.py
    -D           deep clean, remove cached environment and doctree files


.. update:: Apr 7, 2015

   Added ``ablog clean`` and ``ablog deploy`` commands.