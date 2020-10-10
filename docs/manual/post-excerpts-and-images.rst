Post Excerpts and Images
========================

.. post:: May 12, 2014
   :tags: directive
   :category: Manual
   :location: Pittsburgh
   :author: Ahmet
   :exclude:
   :image: 2

   This post describes how to choose an excerpt and an image image for a post to be displayed in archive pages.

Excerpts
--------

ABlog, by default, uses first paragraph of the document as post excerpt.
Default number of paragraphs to use in excerpts is controlled via :confval:`post_auto_excerpt` configuration variable.
This option can be overwritten using ``:excerpt:`` option in :rst:dir:`post` directive.

Alternatively, you can provide some content in a post directive as follows::

  .. post:: Apr 15, 2014

     This is all of the excerpt for this post.

This content is going to be used as excerpt in archive pages.
Furthermore, if you do not want the excerpt to be included in the post, you can use ``:exclude:`` option as follows::

  .. post:: Apr 15, 2014
     :exclude:

     This is all of the excerpt for this post.
     It will be displayed in archive pages and excluded from the post page.

Images
------

Let's first include a local and a non-local image in this post.

.. image:: /_static/ablog.png
.. image:: https://www.python.org/static/community_logos/python-logo.png

To link the second one of these, we add ``:image: 2`` option in :rst:dir:`post` directive.
