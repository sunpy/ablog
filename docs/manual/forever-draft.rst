Draft Example
=============

.. post::
   :tags: draft
   :category: Manual


As the title suggests, this is a draft example and shall remain so until the end of time or internet.

How do you draft a post?
------------------------

Just indicate that the page is a post using :rst:dir:`post` directive, but do not provide give a published date:

.. code-block:: rst

  .. post::
     :tags: draft
     :category: Manual

You can still label a post you are drafting with tags and categories, but the post will not be listed in corresponding archive pages until it is published.

How can you see a list of drafts?
---------------------------------

See :ref:`blog-drafts` archive page, which can be referred to as ``:ref:blog-drafs```.

Why would you make a post draft?
--------------------------------

Let's say you are using Disqus_ on your website, and allowing non-post pages to be discussed as well, but you don't want a draft to be discussed before it is published.
By adding :rst:dir:`post` directive without published date and keeping configuration variable :confval:`disqus_drafts` as ``False``, you can achieve that.
