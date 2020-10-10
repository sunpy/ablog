.. _commands:

ABlog Commands
==============

.. post:: Mar 1, 2015
   :tags: config, commands
   :author: Ahmet, Mehmet
   :category: Manual
   :location: SF


``ablog`` commands are for streamlining blog operations, i.e. building, serving, and viewing blog pages, as well as starting a new blog::

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

.. _start:

Start a New Project
-------------------

``ablog start`` command is for quickly setting up a blog project.
See :ref:`quick-start` for how it works and what it prepares for you::

  $ ablog start -h
  usage: ablog start [-h]

  Start a new blog project by answering a few questions. You will end up with a
  configuration file and sample pages.

  optional arguments:
    -h, --help  show this help message and exit

.. _build:

Build your Website
------------------

Running ``ablog build`` in your project folder builds your website HTML pages::

  $ ablog build -h
  usage: ablog build [-h] [-a] [-b BUILDER] [-s SOURCEDIR] [-w WEBSITE]
                     [-d DOCTREES] [-T] [-P]

  Path options can be set in conf.py. Default values of paths are relative to
  conf.py.

  optional arguments:
    -h, --help    show this help message and exit
    -a            write all files; default is to only write new and changed
                  files
    -b BUILDER    builder to use, default `ablog_builder` or dirhtml
    -s SOURCEDIR  root path for source files, default is path to the folder that
                  contains conf.py
    -w WEBSITE    path for website, default is _website when `ablog_website` is
                  not set in conf.py
    -d DOCTREES   path for the cached environment and doctree files, default
                  .doctrees when `ablog_doctrees` is not set in conf.py
    -T            show full traceback on exception
    -P            run pdb on exception

Serve and View Locally
----------------------

Running ``ablog serve``, after building your website, will start a Python server and open up browser tab to view your website::

  $ ablog serve -h
  usage: ablog serve [-h] [-w WEBSITE] [-p PORT] [-n] [-r] [--patterns]

  Serve options can be set in conf.py. Default values of paths are relative to
  conf.py.

  optional arguments:
    -h, --help  show this help message and exit
    -w WEBSITE  path for website, default is _website when `ablog_website` is
                not set in conf.py
    -p PORT     port number for HTTP server; default is 8000
    -n          do not open website in a new browser tab
    -r          rebuild when a file matching patterns change or get added
    --patterns  patterns for triggering rebuilds

.. _deploy:

Deploy to GitHub Pages
----------------------

Running ``ablog deploy`` will push your website to GitHub::

  $ ablog deploy -h
  usage: ablog deploy [-h] [-w WEBSITE] [-p REPODIR] [-g GITHUB_PAGES]
                      [-m MESSAGE] [-f] [--push-quietly]
                      [--github-token GITHUB_TOKEN]

  Path options can be set in conf.py. Default values of paths are relative to
  conf.py.

  optional arguments:
    -h, --help            show this help message and exit
    -w WEBSITE            path for website, default is _website when
                          `ablog_website` is not set in conf.py
    -p REPODIR            path to the location of repository to be deployed,
                          e.g. `../username.github.io`, default is folder
                          containing `conf.py`
    -g GITHUB_PAGES       GitHub username for deploying to GitHub pages
    -m MESSAGE            commit message
    -f                    owerwrite last commit, i.e. `commit --amend; push -f`
    --push-quietly        be more quiet when pushing changes
    --github-token GITHUB_TOKEN
                          environment variable name storing GitHub access token

Create a Post
-------------

Finally, ``ablog post`` will make a new post template file::

  $ ablog post -h
  usage: ablog post [-h] [-t TITLE] filename

  positional arguments:
    filename    filename, e.g. my-nth-post (.rst appended)

  optional arguments:
    -h, --help  show this help message and exit
    -t TITLE    post title; default is formed from filename

Clean Build Files
-----------------

In case you needed, running ``ablog clean`` will remove build files and do a deep clean with ``-D`` option::

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
