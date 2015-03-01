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
where each manual and release is a blog post ;) 

.. _Atom feeds: http://ablog.readthedocs.org/blog/atom.xml
.. _Archive pages: http://ablog.readthedocs.org/blog/
.. _Blog sidebars: http://ablog.readthedocs.org/manual/ablog-configuration-options/#sidebars
.. _Disqus integration: http://ablog.readthedocs.org/manual/ablog-configuration-options/#disqus-integration
.. _Font-Awesome integration: http://ablog.readthedocs.org/manual/ablog-configuration-options/#fa

Installation
------------

You can install ABlog using pip_::

    pip install -U ablog

This will install Sphinx_ and Werkzeug_ as well, respectively required for 
building your website and generating feeds.

If you are starting a new Sphinx project, you might want to also install 
Alabaster_ to have a good looking website::

  pip install Alabaster

.. _pip: https://pip.pypa.io
.. _Sphinx: http://sphinx-doc.org/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Alabaster: https://github.com/bitprophet/alabaster


Getting Started
---------------

If you are starting a new project, see `ABlog Quick Start`_ guide.

If you already have a project, enable blogging by making following changes in ``conf.py``:

.. code-block:: python

  # 1. Append 'ablog' to list of extensions
  extensions = [
      '...',
      'ablog'
  ]
  
  # 2a. Append templates path to `templates_path`
  import ablog
  templates_path.append(ablog.get_html_templates_path())

  # 2b. If `templates_path` is not defined before
  templates_path = [ablog.get_html_templates_path()]

If you also installed Alabaster_, see how to configure it here_.

.. _ABlog Quick Start: http://ablog.readthedocs.org/manual/ablog-quick-start
.. templates_path: http://sphinx-doc.org/config.html#confval-templates_path
.. here_: https://github.com/bitprophet/alabaster#installation

How it works
------------

You can post *any page* with the ``post`` directive as follows:

.. code-block:: rst

  .. post:: Apr 15, 2014
     :tags: earth, love, peace
     :category: python
     :author: me
     :location: SF
     :language: en     

ABlog will index all posted ``.rst`` files (pages)  without interfering with Sphinx's operations. Since any page from any folder can be posted, you do not need to change how you organize project contents in separate folders. 

When building HTML pages, posts will be included in archives and feeds 
specified by ``:tag:``, ``:category:``, etc. options.

In addition, you can include a list of posts anywhere in your project 
simply using ``postlist`` directive:

.. code-block:: rst

  .. postlist:: 5
     :category: Manual
     :reverse:

For ABlog documentation, this converts to a list of links to the oldest 
five posts in Manual_ category:

  * `Posting and Listing <http://ablog.readthedocs.org/manual/posting-and-listing/>`_ 
  * `ABlog Configuration Options <http://ablog.readthedocs.org/manual/ablog-configuration-options/>`_ 
  * `Cross-referencing Blog Pages <http://ablog.readthedocs.org/manual/cross-referencing-blog-pages/>`_
  * `Post Excerpts and Images <http://ablog.readthedocs.org/manual/post-excerpts-and-images/>`_
  * `Posting Sections <http://ablog.readthedocs.org/manual/posting-and-listing/#posting-sections>`_
  

.. _Manual: http://ablog.readthedocs.org/blog/category/manual/

