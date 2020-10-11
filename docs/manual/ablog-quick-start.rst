.. _quick-start:


ABlog Quick Start
=================

.. post:: Mar 1, 2015
   :tags: config, tips
   :author: Mehmet, Ahmet
   :category: Manual
   :location: SF

This short walk through of blogging work flow assumes that you have already installed ABlog. If not, see :ref:`installation` guide.

*Note that this post is a working draft. Feel free to revise it on GitHub.*

Start a Project
---------------

To start a new project, run ``ablog start`` command in a directory where you want to keep your project source files.
This command will ask you a few questions and create the following files:

  * :file:`conf.py` that contains project configuration for building HTML pages.

  * :file:`first-post.rst`, a blog post example.

  * :file:`index.rst` that contains content for the *landing* page of your website.

  * :file:`about.rst`, another non-post page example.


Build and View
--------------

With no further delay, let's see what your project will look like.
First run ``ablog build``, in your project folder, to have HTML pages built in :file:`_website` folder.
Then, call ``ablog serve`` to view them in your default web browser.
See :ref:`commands` for more information about these commands.

Your landing page is built from :file:`index.rst` and contains links to your first post and about page.
Take a look at :file:`index.rst` for some tips on navigation links within the project.

Write Content
-------------

If you are new to Sphinx_ and reStructuredText markup language, you might find `reStructuredText Primer`_ useful.

.. _reStructuredText Primer: http://sphinx-doc.org/rest.html

Pages
^^^^^

Pages in your project are :file:`.rst` files that are only a :rst:dir:`post` directive short of becoming blog posts.
To make regular pages accessible from the navigation bar, you need to list them in a :rst:dir:`toctree`.
This is shown for *about* page into :file:`index.rst`.

Posts
^^^^^

You can convert any page to a post with a :rst:dir:`post` directive.
ABlog will take care of listing posts in specified archives and sidebars.

Blog posts
^^^^^^^^^^

You can start new blog posts with either a front-matter or a directive using ABlog.
Simply use something based on the following template as the front-matter::

:blogpost: true
:date: January 1, 2020
:author: A. Author
:location: World
:category: Blog
:language: English
:tags: blog

Simply use something based on the following template as the directive for ABlog::

.. post:: January 1, 2020

  :author: A. Author
  :location: World
  :category: Blog
  :language: English
  :tags: blog

For more information, see :ref:`posting-directive` and :ref:`posting-front-matter`.

Comments
--------

You can enable comments in your website by creating a Disqus_ account and obtaining a unique identifier, i.e. :confval:`disqus_shortname`.
See :ref:`disqus-integration` for configuration options.

Analytics
---------

ABlog uses Alabaster_ theme by default. You can use theme options to set your `Google Analytics`_ identifier to enable tracking.

.. _Google Analytics: https://www.google.com/analytics/

Configuration
-------------

There are four major groups of configuration options that can help you customize how your website looks:

  * :ref:`config` - add blog authors, post locations and languages to your blog, adjust archive and feed content, etc.

  * `General configuration <http://sphinx-doc.org/config.html#general-configuration>`__ and `project information <http://sphinx-doc.org/config.html#project-information>`__

  * :ref:`html-options` - configure appearance of your website.

  * Alabaster_ theme options - link to your GitHub account and project, set up tracking, etc.

Other Folders
-------------

You might have noticed that your project contains three folders that we have not mention yet.
Here they are:

  * :file:`_static` is for keeping image, :file:`.js`, and :file:`.css` files.
    :confval:`html_static_path` Sphinx option for more information.

  * :file:`_templates` is for custom HTML templates.
    See :confval:`templates_path` for more information.

  * :file:`.doctree` folder, created after build command is called, is where Sphinx_ stores the state of your project.
    Files in this folder saves time when you rebuild your project.
