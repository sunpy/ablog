.. _quick-start:


ABlog Quick Start
=================

.. post:: Mar 1, 2015
   :tags: config, start,
   :author: Mehmet, Ahmet
   :category: Manual
   :location: SF

This short walk through of blogging work flow assumes that you have already
installed ABlog. If not, see :ref:`installation` guide.

Start a Project
---------------

To start a new project, run ``ablog start`` command in a directory where
you want to keep your project source files. This command will ask you a
few questions and create following files:

  * :file:`conf.py` contains project configuration required for
    building HTML pages. You will find out more different groups of
    configuration options soon.

  * :file:`first-post.rst` is a blog post example.

  * :file:`index.rst` is going to be the *landing* page of your website.

  * :file:`about.rst` is another page where you may put information *about*
    yourself.



Build and View
--------------

Before any further details, let's see quickly what your project looks like.
First run ``ablog build`` in your project folder to create HTML pages in
:file:`_website` folder. Then, call ``ablog serve`` to open them in your
default browser.

What you see initially is built from :file:`index.rst`. In the page
and sidebar, you will find links to your first post and about page.
Find out more about controlling where links to other pages appear
in :file:`index.rst`.


Write Content
-------------

You will need to write content in reStructuredText format. If you are
Sphinx_

Pages
^^^^^

Pages in your project are :file:`.rst` files that are only a :rst:dir:`post`
directive short of becoming blog posts. While you may be planning to write
blog posts primarily, you may have more than a landing page in your website.
In that case, you will need to make them browsable from the landing page.
To this end, you need to list each non-post page in a TOCTree. This is shown
for *about* page into :file:`index.rst`. You can also find more about this
in ....


Posts
^^^^^

Posts are pages with a :rst:dir:`post` directive that tags, catgorizes
ABlog takes care of
listing posts in appropriate places, such as ``

ABlog also generates archive pages and atom feeds from your posts. A post
will appear


Comments
--------


Analytics
---------

ABlog uses Alabaster_ theme by default to make sure that your project does not
look like a Python package documentation. This may soon change though with
Alabaster_ becoming the default theme for Sphinx_ in v1.3. But for now,


Configuration
-------------

There are four major groups of configuration options that can help you
customize how your website looks:

  * :ref:`config` - add blog authors, post locations and languages to your
    blog, level of achives and feeds and how much content they display, etc.

  * Sphinx options -

  * HTML output options -

  * Alabaster_ theme options - you can


Other Folders
-------------

You might have noticed that your project contains three folders that we have
not mention yet. Here they are:

  * :file:`_static` is for keeping image, :file:`.js`, and :file:`.css` files.
    :confval:`html_static_path` Sphinx option for more information.

  * :file:`_templates` is for custom HTML templates. See
    :confval:`templates_path` for more information.

  * :file:`.doctree` folder, created after build command is called, is
    where Sphinx_ stores the state of your project. Files in this folder
    saves time when you rebuild your project.


