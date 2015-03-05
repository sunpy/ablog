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
  questions and end up with

2. `ablog build`

3. `ablog serve`

4. Write new content in reStructuredText, and repeated #2 and #3.



Archives
--------

ABlog generates archives pages automatically for pretty much everything ...


Blog Feeds
----------

Feeds are generated for ...


Blog Theme
----------

**Alabaster Sphinx theme opt-in:**
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

Alabaster GitHub Options:
^^^^^^^^^^^^^^^^^^^^^^^^^

		1. **GitHub Project Name:**
		The name of the GitHub project, just the project name.
		e.g. `http://www.github.com/abakan/ablog` --> `ablog`

		#. **GitHub User Name:**
			The user name of the GitHub project owner.
			e.g. `http://www.github.com/abakan/ablog` --> `abakan`

		#. **GitHub Project Description:**
			A single line (short line) description for the GitHhub project.

		#. **GitHub Project Logo:**
			Path to the GitHub project logo.
			Relative to project root or external (http, etc.).
			Default is blank and you can leave blank to disable.

		#. **Travis-CI Button Opt-In:**
			If your project is linked to Travis-CI you can enable the
			Travis-CI button/build badge, if you like.
			Default is [n].



