ABlog for Sphinx
================

ABlog is a Sphinx extension that converts any documentation or personal
website project into a full-fledged blog with:

  * `Atom feeds`_
  * `Archive pages`_
  * `Blog sidebars`_
  * `Disqus integration`_
  * `Font-Awesome integration`_

Looking for an example? Take a look at `ABlog documentation <http://ablog.readthedocs.org>`_
where each manual page and release note is a blog post ;)

.. _Atom feeds: http://ablog.readthedocs.org/blog/atom.xml
.. _Archive pages: http://ablog.readthedocs.org/blog/
.. _Blog sidebars: http://ablog.readthedocs.org/manual/ablog-configuration-options/#sidebars
.. _Disqus integration: http://ablog.readthedocs.org/manual/ablog-configuration-options/#disqus-integration
.. _Font-Awesome integration: http://ablog.readthedocs.org/manual/ablog-configuration-options/#fa

.. _installation:

Installation
------------

You can install ABlog using pip_::

    pip install -U ablog

This will also install `Sphinx <http://sphinx-doc.org/>`_, Alabaster_, and
Werkzeug_, respectively required for building your website, making it look
good, and generating feeds.

.. _pip: https://pip.pypa.io
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Alabaster: https://github.com/bitprophet/alabaster


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

If you are new to Sphinx_ and reStructuredText markup language,
you might find `reStructuredText Primer`_ useful. Once you have
content (in ``.rst`` files), you can post *any page* using the
``post`` directive as follows:

.. code-block:: rst

  .. post:: Apr 15, 2014
     :tags: earth, love, peace
     :category: python
     :author: me
     :location: SF
     :language: en

ABlog will index all files posted as above and list them in archives and feeds
specified in ``:tag:``, ``:category:``, etc. options.

You can also include a list of posts using ``postlist`` directive:

.. code-block:: rst

  .. postlist:: 5
     :category: Manual
     :sort:

For ABlog documentation, this converts to the following where you
can find more about configuring and using ABlog:

* `Posting and Listing <http://ablog.readthedocs.org/manual/posting-and-listing/>`_
* `ABlog Configuration Options <http://ablog.readthedocs.org/manual/ablog-configuration-options/>`_
* `Cross-referencing Blog Pages <http://ablog.readthedocs.org/manual/cross-referencing-blog-pages/>`_
* `Post Excerpts and Images <http://ablog.readthedocs.org/manual/post-excerpts-and-images/>`_
* `Posting Sections <http://ablog.readthedocs.org/manual/posting-and-listing/#posting-sections>`_


.. _reStructuredText Primer: http://sphinx-doc.org/rest.html

For existing projects, it is important to note that ABlog does not intertere
with any Sphinx operations. Since you can post any page from any folder,
you do not need to change how you organize project contents.


.. image:: https://secure.travis-ci.org/abakan/ablog.png?branch=devel
   :target: http://travis-ci.org/#!/abakan/ablog

.. image:: https://pypip.in/v/ABlog/badge.png
   :target: https://pypi.python.org/pypi/ABlog

.. image:: https://pypip.in/d/ABlog/badge.png
   :target: https://crate.io/packages/ablog
