.. _commands:

ABlog Commands
==============

.. post:: Mar 1, 2015
   :tags: config
   :author: Ahmet, Mehmet
   :category: Manual
   :location: SF


``ablog`` commands are for streamlining blog operations, i.e. building, serving,
and viewing blog pages, as well as starting a new blog.

::

  $ ablog
  usage: ablog [-h] [-v] {start,build,serve,post} ...

  ABlog for blogging with Sphinx

  optional arguments:
    -h, --help            show this help message and exit
    -v, --version         print ABlog version and exit

  subcommands:
    {start,build,serve,post}
      start               start a new blog project
      build               build your blog project
      serve               serve and view your project
      post                create a blank post

  See 'ablog <command> -h' for more information on a specific command.


Start a Project
---------------

``ablog start`` command is for quickly setting up a blog project. See
:ref:`quick-start` for how it works and what it prepares for you.


::

  $ ablog serve -h
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

  Build options can be set in conf.py. Default values of paths are relative to
  conf.py.

  optional arguments:
    -h, --help    show this help message and exit
    -b BUILDER    builder to use, default `ablog_builder` or dirhtml
    -d DOCTREES   path for the cached environment and doctree files, default
                  `ablog_doctrees` or .doctrees
    -s SOURCEDIR  root path for source files, default is path to the folder that
                  contains conf.py
    -w WEBSITE    path for website, default `ablog_website` or _website
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
    -w WEBSITE  path for website, default `ablog_website` or _website

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