ABlog for Sphinx
================

It's a Blog... It's a Documentation... It's Sphinx with ABlog

ABlog is a Sphinx extension that converts any documentation or personal
website project into a full-fledged blog with:

  * `Atom feeds`_, e.g. `ABlog feed`_
  * `Archive pages`_, e.g. `ABlog archive`_
  * `Blog sidebars`_ with including tag cloud, archive links, etc.
  * `Disqus integration`_
  * `Font-Awesome integration`_

Looking for an example? Take a look at `ABlog documentation <http://ablog.readthedocs.org>`_ 
where each manual page and release is a blog post ;) 

.. _Atom feeds: http://ablog.readthedocs.org/manual/ablog-configuration-options/#blog-feeds
.. _ABlog feed: http://ablog.readthedocs.org/blog/atom.xml
.. _Archive pages: http://ablog.readthedocs.org/manual/cross-referencing-blog-pages/#archives
.. _ABlog archive: http://ablog.readthedocs.org/blog/
.. _Blog sidebars: http://ablog.readthedocs.org/manual/ablog-configuration-options/#sidebars
.. _Disqus integration: http://ablog.readthedocs.org/manual/ablog-configuration-options/#disqus-integration
.. _Font-Awesome integration: http://ablog.readthedocs.org/manual/ablog-configuration-options/#fa

Installation
------------

You can install ABlog using pip_::

    pip install -U ablog

This will also install required packages Sphinx_ and Werkzeug_, respectively required 
for building your website and generating feeds.

If you don't already have a Sphinx project with a nice theme, you might want to 
install Alabaster_ to start with a good looking website::

  pip install Alabaster

.. _pip: https://pip.pypa.io
.. _Sphinx: http://sphinx-doc.org/
.. _Werkzeug: http://werkzeug.pocoo.org/
.. _Alabaster: https://github.com/bitprophet/alabaster


Getting Started
---------------

If you are starting a new project, see `ABlog Quick Start`_ guide.

If you already have a project, enable blogging by editing ``conf.py``
as follows:

.. code-block:: python

  # 1. append ablog to list of extensions
  extensions = [
      '...',
      'ablog'
  ]
  
  # 2a. append ABlog templates path to `templates_path`
  import ablog
  templates_path.append(ablog.get_html_templates_path())

  # 2b. if `templates_path` is not defined before
  templates_path = [ablog.get_html_templates_path()]

If you have also installed Alabaster_, see here_ how to configure it.

.. here_: https://github.com/bitprophet/alabaster#installation


.. _ABlog Quick Start: http://ablog.readthedocs.org/manual/ablog-quick-start
.. templates_path: http://sphinx-doc.org/config.html#confval-templates_path

How it works
------------

You can convert *any page* to a post with the ``post`` directive as follows:

.. code-block:: rst

  .. post:: Apr 15, 2014
     :tags: python, earth, love, peace
     :category:
     :language: en
     :location: Milky Way
     :author:
     
  Here Goes Your Post or Page Title
  =================================
  
  Followed by an awesome content!

ABlog will catalog all ``.rst`` files (pages) indicated as posts as above, 
whithout interfering with Sphinx's operations. Since any page from any folder 
in your project can be posted, you do not need to change how you organize
content in separate folders. 

When you are building HTML pages, posts will be included in archives and feeds 
specified by ``:tag:``, ``:category:``, etc. options automatically.

In additon, you can include a list of posts anywhere in your project 
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
  * `Posting Sections <http://ablog.readthedocs.org/manual/posting-and-listing/#posting-sections>_`
  

.. _Manual: http://ablog.readthedocs.org/blog/category/manual/

