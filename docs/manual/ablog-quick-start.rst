.. _workflow:


ABlog Quick Start
=================

.. post:: Mar 1, 2015
   :tags: config, start,
   :author: Mehmet
   :category: Manual
   :location: SF

This is a simple walk through of the `ablog start` flow,
intended to explain the options you're presented when
running the command to start your blog.

The start command will ask you to enter the following:

Basic Information:
^^^^^^^^^^^^^^^^^^

1. **Blog root folder:**
    This is where your configuration file and the rest of your projects files and folders will be created.
    The default is [.] the current working folder.

#. **Title of your blog:**
	Title of your blog. It will appear on various locations on your blog depending
	on your choice of themes.

#. **Author Name:**
	Name of the blog owner (person, project, organization, etc.)
	It will be the actual display 'title' of the blog.

#. **Blog URL:**
	The URL pointing to your intended publishing address of your blog.
	It will be used for feed generation. (e.g. Atom, RSS etc.)

Optional Features:
^^^^^^^^^^^^^^^^^^

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

