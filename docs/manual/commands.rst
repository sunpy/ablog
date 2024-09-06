.. _ablog_manual_commands:

**************
ABlog Commands
**************

``ablog`` has commands for streamlining blog operations, i.e., building, serving, and viewing blog pages, as well as starting a new blog:

.. code-block:: bash

    $ ablog
    usage: ablog [-h] [-v] {start,build,clean,serve,post,deploy} ...

    ABlog for blogging with Sphinx

    options:
      -h, --help            show this help message and exit
      -v, --version         print ABlog version and exit

    commands:
      {start,build,clean,serve,post,deploy}
        start               start a new blog project
        build               build your blog project
        clean               clean your blog build files
        serve               serve and view your project
        post                create a blank post
        deploy              deploy your website build files

    See 'ablog <command> -h' for more information on a specific command.

Start a New Project
===================

``ablog start`` command is for quickly setting up a blog project.
See :ref:`quick-start` for how it works and what it prepares for you.

Build your Website
==================

Running ``ablog build`` in your project folder builds your website HTML pages.

Serve and View Locally
======================

Running ``ablog serve`` after building your website, will start a Python server and open up browser tab to view your website.


Deploy to GitHub Pages
======================

Running ``ablog deploy`` will push your website to GitHub.

Create a Post
=============

Running ``ablog post`` will make a new post template file.

Clean Build Files
=================

In case you needed, running ``ablog clean`` will remove build files and do a deep clean with ``-D`` option.
