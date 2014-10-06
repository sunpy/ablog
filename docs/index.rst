ABlog for Sphinx
================

It's a Blog... It's a Documentation... It's Sphinx with ABlog


ABlog is a Sphinx extension that can convert any documentation or personal
website project into a full-fledged blog with:

  * `Atom feeds <http://ablog.readthedocs.org/blog/atom.xml>`_
  * :ref:`archives`
  * :ref:`sidebars`
  * :ref:`disqus-integration`
  * :ref:`fa` integration

Looking for an example? Just browse this documentation ;)

Installation
------------

You can install ABlog using pip_::

    pip install -U ablog

In addition to Sphinx_, Werkzeug_ is required for generating feeds.


Configuration
-------------

To enable blogging in a Sphinx project, append ``ablog`` to the
list of extensions and ABlog template path to :confval:`templates_path`
in :file:`conf.py`:

.. code-block:: python

  extensions = [
      '...',
      'ablog'
  ]
  import ablog
  templates_path.append(ablog.get_html_templates_path())

  # if `templates_path` is not defined before
  templates_path = [ablog.get_html_templates_path()]


See more detailed instructions in :ref:`ablog-configuration-options`
and :ref:`posting-and-listing` posts.

**Read The Docs**

On `Read The Docs`_, ABlog may cause an exception when Sphinx build environment
is being pickled.  To circumvent this problem, include the following
in :file:`conf.py`::

  if os.environ.get('READTHEDOCS', None) == 'True':
      skip_pickling = True

This should not effect how the documentation is built.

How it works
------------

ABlog catalogs all :file:`.rst` files indicated as posts and creates
archive pages and a blog feed. It does not interfere with Sphinx's operations,
and you do not need to change how you structure content in separate folders.

You can convert *any page*, containing a new usage example or a new release
announcement, to a post with the :rst:dir:`post` directive as follows:

.. code-block:: rst

  .. post:: Apr 15, 2014
     :tags: python, earth, love, peace

ABlog will include the page in specified archive pages and the blog feed.

You can include a list of posts anywhere simply using :rst:dir:`postlist`
directive:

.. code-block:: rst

  .. postlist:: 2
     :category: Release

This converts to a list of links to the most recent five posts in
:ref:`category-release` category:

.. postlist:: 2
   :category: Release


Documentation
-------------

You can learn more about ablog features in the following posts:

.. postlist:: 10
   :category: Manual
   :sort:



Feedback
--------

ABlog has been used with the Sphinx_ 1.2.2, Python 2.7 and 3.4
to generate its documentation blog. If you try it with different
Python and Sphinx versions, please give feedback to help us improve it.
