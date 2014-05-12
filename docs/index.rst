ABlog for Sphinx
================

It's a Blog... It's a Documentation... It's Sphinx with ABlog


ABlog is a Sphinx extension that can convert any documentation or personal
website project into a full-fledged blog with feeds. Looking for an example?
Just browse this documentation ;)

Installation
------------

ABlog is not released yet. It's being tested. If you are interested you can
get if from GitHub_.


..
  Install ABlog using pip_::

    pip install -U ABlog

In addition to Sphinx_, Werkzeug_ is required for generating feeds.


Configuration
-------------

To enable blogging in a Sphinx project, append ``ablog`` to the
list of extensions and ABlog template path to :confval:`template_path`
in :file:`conf.py`:

.. code-block:: python

  extensions = [
      '...',
      'ablog'
  ]
  templates_path.append(ablog.get_html_templates_path())

  # if `templates_path` is not defined before
  templates_path = [ablog.get_html_templates_path()]


See more detailed instructions in :ref:`get-started` post.

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

This converts to a list of links to the most recent posts in category
:ref:`category-release`:

.. postlist:: 2


Feedback
--------

ABlog has been used with the Sphinx_ 1.2.2, Python 2.7 and 3.4
to generate its documentation blog. If you try it with different
Python and Sphinx versions, please give feedback to help us improve it.
