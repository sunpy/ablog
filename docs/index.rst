ABlog for Sphinx
================

ABlog is a Sphinx extension that converts any documentation or personal website project into a full-fledged blog with:

  * :ref:`Atom feeds <blog-feed>`
  * :ref:`Archive pages <blog-archives>`
  * :ref:`sidebars`
  * :ref:`disqus-integration`
  * :ref:`Font-Awesome integration <font-awesome>`
  * :doc:`manual/markdown`

Ablog is part of the `SunPy Project <https://www.sunpy.org>`__.

.. _installation:

Installation
------------

You can install ABlog using `pip <https://pip.pypa.io/en/stable/>`__::

   pip install -U ablog

or `miniforge <https://github.com/conda-forge/miniforge>`__::

   conda install ablog

This will also install `Sphinx <http://sphinx-doc.org/>`__, `feedgen <https://github.com/lkiesow/python-feedgen>`__, and `Invoke <https://www.pyinvoke.org/>`__ respectively required for building your website, making it look good, generating feeds, and running deploy commands.

Getting Started
---------------

If you are starting a new project, see the :ref:`quick-start` guide.
If you already have a project, enable blogging by making following changes in ``conf.py``:

.. code-block:: python

  # 1. Add 'ablog' and 'sphinx.ext.intersphinx' to the list of extensions
  extensions = [
      '...',
      'ablog',
      'sphinx.ext.intersphinx',
  ]

How it works
------------

If you are new to Sphinx_ and reStructuredText markup language, you might find `reStructuredText Primer`_ useful.
Once you have content (in ``.rst`` files), you can post *any page* using the :rst:dir:`post` directive as follows:

.. _reStructuredText Primer: http://www.sphinx-doc.org/en/master/

.. code-block:: rst

  .. post:: Apr 15, 2014
     :tags: earth, love, peace
     :category: python
     :author: me
     :location: SF
     :language: en

An alterative method is:

.. code-block:: rst

   :blogpost: true
   :date: Oct 10, 2020
   :author: Nabil Freij
   :location: World
   :category: Manual
   :language: English

at the top of the file.

ABlog will index all files posted as above and list them in archives and feeds specified in ``:tag:``, ``:category:``, etc. options.

You can also include a list of posts using :rst:dir:`postlist` directive:

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

.. only:: html

   .. image:: https://readthedocs.org/projects/ablog/badge/?version=latest
      :target: https://ablog.readthedocs.org/

.. toctree::
   :hidden:
   :glob:

   */*
