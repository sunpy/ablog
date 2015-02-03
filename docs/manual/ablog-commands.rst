.. _commands:



ABlog Commands
==============

.. post:: Feb 1, 2015
   :tags: config
   :author: Ahmet
   :category: Manual
   :location: SF


`ablog` command is designed to streamline blog operations, i.e.
building, serving, and viewing blog pages, as well as starting a new
blog.


.. code-block::

   $ ablog

   usage: ablog [-h] [-v] {start,post,build,serve} ...

   ABlog for blogging with Sphinx

   optional arguments:
     -h, --help            show this help message and exit
     -v, --version         print ABlog version and exit

   subcommands:
     {start,post,build,serve}
       start               start a new blog project
       post                post
       build               build your blog project
       serve               serve your project locally

   See 'ablog <command> -h' for more information on a specific command.


`ablog start`
-------------

.. code-block::

   $ ablog start -h
   usage: ablog start [-h]

   optional arguments:
     -h, --help  show this help message and exit



`ablog build`
-------------

.. code-block::

  $ ablog build -h
  usage: ablog build [-h] [-v] [-b BUILDER] [-d DOCTREES] [-w WEBSITE]
                     [-s SOURCEDIR]

  Build options can be set in conf.py. Default values of path options are
  relative to conf.py.

  optional arguments:
    -h, --help     show this help message and exit
    -v, --version  show program's version number and exit
    -b BUILDER     builder to use, default is value of `ablog_builder` or
                   dirhtml
    -d DOCTREES    path for the cached environment and doctree files, default is
                   value of `ablog_doctrees` or _doctrees
    -w WEBSITE     path for website, default is value of `ablog_website` or
                   _website
    -s SOURCEDIR   root path for source files, default is path to the folder
                   that contains conf.py

`ablog serve`
-------------

.. code-block::

   $ ablog serve -h
   usage: ablog serve [-h] [-v] [-w WEBSITE] [-p PORT]

   optional arguments:
     -h, --help     show this help message and exit
     -v, --version  show program's version number and exit
     -w WEBSITE     path for website, default is value of `ablog_website` or
                    _website
     -p PORT        port number for HTTP server; default is 8000