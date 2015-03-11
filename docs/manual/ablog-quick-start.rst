.. _workflow:


ABlog Quick Start
=================

.. post:: Mar 1, 2015
   :tags: config, start,
   :author: Mehmet, Ahmet
   :category: Manual
   :location: SF

This short walk through assumes that you have installed ABlog. If not,
see :ref:`installation` guide.

Start a Project
---------------

To start a new project, run ``ablog start`` command in a directory where
you want to keep your project source files. This command will ask you a
few questions and create following files and folders:

  * :file:`conf.py` contains project configuration required for
    building HTML pages.

  * :file:`index.rst` becomes the landing page of your website. See the inside
    of it for more information.

  * :file:`about.rst` may contain information about you. A link to this
    page will show up in `Navigation` sidebar.

  * :file:`first-post.rst` is a blog post example that contains
    :rst:dir:`post` directive. See

  * :file:`_static` is for keeping image, :file:`.js`, and :file:`.css` files.
    Once you go through this page, you may find out more
    about this folder  :confval:`html_static_path` for more information.

  * :file:`_templates` is for custom HTML templates. See
    :confval:`templates_path` for more information.



Build and View
--------------


Write Content
-------------



Blog Components
---------------

ABlog generates archives pages automatically for pretty much everything ...


Blog Feeds
----------

Feeds are generated for ...


Blog Theme
----------

Alabaster is the default theme for ABlog. It
If you happen to have Alabaster Sphinx theme installed on your system,
you will be asked whether you'd like to enable it.
The default value is [y] and you'll only be asked, if you have alabaster
installed on your system. If you don't see this prompt and wan't to install
alabaster on your system, you can do so by using the following command:

    >>> pip install alabaster

Please see `Alabaster GitHub home`_ for more information.

.. _`Alabaster GitHub home`: https://github.com/bitprophet/alabaster

**This is the end, if you're not using 'Alabaster'.**


Alabaster Options:
^^^^^^^^^^^^^^^^^^

	1. **Google Analytics ID:**
	Google Analytics ID for the blog to track traffic.
	The default is blank. Leave blank to disable.

	2. **Alabaster GitHub Options:**
	Enables GitHub options for Alabaster and will lead to a few more
	questions.

**This is the end, if you're not using GitHub options for `Alabaster`**
