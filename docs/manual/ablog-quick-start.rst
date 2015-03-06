.. _workflow:


ABlog Quick Start
=================

.. post:: Mar 1, 2015
   :tags: config, start,
   :author: Mehmet, Ahmet
   :category: Manual
   :location: SF

This is a short walk through of blogging work flow and description of blog
components.

The start command will ask you to enter the following:

Blogging Workflow
-----------------

1. `ablog start`

   Run this command to kick start your project. You will be a few simple
   questions and end up with a sample page and a post.

2. `ablog build`

   This command will prepare HTML pages for you.

3. `ablog serve`

   You are now ready to view your website in a browser.

4. Write new content in reStructuredText, and repeated #2 and #3.



Archives
--------

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
