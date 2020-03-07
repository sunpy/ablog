ABlog for Sphinx
================

.. image:: https://travis-ci.org/sunpy/ablog.svg?branch=master
    :target: https://travis-ci.org/sunpy/ablog
.. image:: https://circleci.com/gh/sunpy/ablog.svg?style=svg
    :target: https://circleci.com/gh/sunpy/ablog
.. image:: https://ci.appveyor.com/api/projects/status/cmmiadqoy5lx7l78?svg=true
    :target: https://ci.appveyor.com/project/sunpy/ablog


Note
----

Please note that is an official new home of `Ahmet Bakan's Ablog Sphinx extension <https://github.com/abakan/ablog/>`__.
This version is maintined with the aim to keep it working for SunPy's website and thus new features are unlikely.

ABlog
-----

ABlog is a Sphinx extension that converts any documentation or personal website project into a full-fledged blog with:

  * `Atom feeds`_
  * `Archive pages`_
  * `Blog sidebars`_
  * `Disqus integration`_
  * `Font-Awesome integration`_
  * `Easy GitHub Pages deploys`_
  * `Jupiter Notebook Support for blog posts`_

.. _Atom feeds: https://ablog.readthedocs.org/blog/atom.xml
.. _Archive pages: https://ablog.readthedocs.org/blog/
.. _Blog sidebars: https://ablog.readthedocs.org/manual/ablog-configuration-options/#sidebars
.. _Disqus integration: https://ablog.readthedocs.org/manual/ablog-configuration-options/#disqus-integration
.. _Font-Awesome integration: https://ablog.readthedocs.org/manual/ablog-configuration-options/#fa
.. _Easy GitHub Pages deploys: https://ablog.readthedocs.org/manual/deploy-to-github-pages/
.. _Jupiter Notebook Support for blog posts: https://ablog.readthedocs.org/manual/notebook_support/

Installation
------------

You can install ABlog using pip_::

    pip install -U ablog

or anaconda_::

    conda config --add channels conda-forge
    conda install ablog

This will also install `Sphinx <http://sphinx-doc.org/>`__, Alabaster_, Werkzeug_, and Invoke_ respectively required for building your website, making it look good, generating feeds, and running deploy commands.

.. _pip: https://pip.pypa.io
.. _anaconda: https://www.anaconda.com/
.. _Werkzeug: https://werkzeug.pocoo.org/
.. _Alabaster: https://github.com/bitprophet/alabaster
.. _Invoke: https://www.pyinvoke.org/

Getting Started
---------------

If you are starting a new project, see `ABlog Quick Start`_ guide.

If you already have a project, enable blogging by making following changes in ``conf.py``:

.. code-block:: python

  # 1. Add 'ablog' and 'sphinx.ext.intersphinx' to the list of extensions
  extensions = [
      '...',
      'ablog',
      'sphinx.ext.intersphinx',
  ]

  # 2. Add ablog templates path
  import ablog

  # 2a. if `templates_path` is not defined
  templates_path = [ablog.get_html_templates_path()]

  # 2b. if `templates_path` is defined
  templates_path.append(ablog.get_html_templates_path())

.. _ABlog Quick Start: https://ablog.readthedocs.org/manual/ablog-quick-start

How it works
------------

If you are new to Sphinx and reStructuredText markup language, you might find `reStructuredText Primer`_ useful.
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

.. _reStructuredText Primer: http://sphinx-doc.org/rest.html
