ABlog for Sphinx
================

.. image:: https://travis-ci.org/sunpy/ablog.svg?branch=master
    :target: https://travis-ci.org/sunpy/ablog
.. image:: https://circleci.com/gh/sunpy/ablog.svg?style=svg
    :target: https://circleci.com/gh/sunpy/ablog

**Please note that is an official continuation of** `Ahmet Bakan's Ablog Sphinx extension <https://github.com/abakan/ablog/>`_.

ABlog is a Sphinx extension that converts any documentation or personal website project into a full-fledged blog with:

  * `Atom feeds`_
  * `Archive pages`_
  * `Blog sidebars`_
  * `Disqus integration`_
  * `Font-Awesome integration`_
  * `Easy GitHub Pages deploys`_
  * `Jupiter Notebook Support for blog posts`_

.. _Atom feeds: http://ablog.readthedocs.org/blog/atom.xml
.. _Archive pages: http://ablog.readthedocs.org/blog/
.. _Blog sidebars: http://ablog.readthedocs.org/manual/ablog-configuration-options/#sidebars
.. _Disqus integration: http://ablog.readthedocs.org/manual/ablog-configuration-options/#disqus-integration
.. _Font-Awesome integration: http://ablog.readthedocs.org/manual/ablog-configuration-options/#fa
.. _Easy GitHub Pages deploys: http://ablog.readthedocs.org/manual/deploy-to-github-pages/
.. _Jupiter Notebook Support for blog posts: http://ablog.readthedocs.org/manual/notebook_support/

.. _installation:

Installation
------------

You can install ABlog using pip_::

    pip install -U ablog

or anaconda_::

    conda config --add channels conda-forge
    conda install ablog

This will also install `Sphinx <http://sphinx-doc.org/>`_, Alabaster_, Werkzeug_, and Invoke_ respectively required for building your website, making it look good, generating feeds, and running deploy commands.

.. _pip: https://pip.pypa.io
.. _anaconda: https://www.anaconda.com/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Alabaster: https://github.com/bitprophet/alabaster
.. _Invoke: http://www.pyinvoke.org/

Getting Started
---------------

If you are starting a new project, see `ABlog Quick Start`_ guide.

If you already have a project, enable blogging by making following changes in ``conf.py``:

.. code-block:: python

  # 1. Add 'ablog' to list of extensions
  extensions = [
      '...',
      'ablog'
  ]

  # 2. Add ablog templates path
  import ablog

  # 2a. if `templates_path` is not defined
  templates_path = [ablog.get_html_templates_path()]

  # 2b. if `templates_path` is defined
  templates_path.append(ablog.get_html_templates_path())

.. _ABlog Quick Start: http://ablog.readthedocs.org/manual/ablog-quick-start

How it works
------------

If you are new to Sphinx_ and reStructuredText markup language, you might find `reStructuredText Primer`_ useful.
Once you have content (in ``.rst`` files), you can post *any page* using the ``post`` directive as follows:

.. code-block:: rst

  .. post:: Apr 15, 2014
     :tags: earth, love, peace
     :category: python
     :author: me
     :location: SF
     :language: en

ABlog will index all files posted as above and list them in archives and feeds specified in ``:tag:``, ``:category:``, etc. options.

You can also include a list of posts using ``postlist`` directive:

.. code-block:: rst

  .. postlist::
     :list-style: circle
     :category: Manual
     :format: {title}
     :sort:

For ABlog documentation, this converts to the following where you can find more about configuring and using ABlog:

.. postlist::
   :category: Manual
   :list-style: circle
   :format: {title}
   :sort:


.. _reStructuredText Primer: http://sphinx-doc.org/rest.html

.. only:: html

   .. image:: https://secure.travis-ci.org/sunpy/ablog.png?branch=devel
      :target: http://travis-ci.org/#!/sunpy/ablog

   .. image:: https://readthedocs.org/projects/ablog/badge/?version=latest
      :target: http://ablog.readthedocs.org/

.. toctree::
   :hidden:
   :glob:

   */*
