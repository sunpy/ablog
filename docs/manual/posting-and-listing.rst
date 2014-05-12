Posting and Listing
===================

.. post:: May 9, 2014
   :tags: directive
   :category: Manual
   :location: Pittsburgh
   :author: Ahmet

This post describes :rst:dir:`post` and :rst:dir:`postlist` directives
introduced by ABlog.

Posting
-------

Any document in a Sphinx_ project can be converted to a post using the
following directive:


.. rst:directive:: post

   Following example shows all possible directive options::

     .. post:: 15 Apr, 2013
        :tags: tips, ablog, directive
        :author: Ahmet, Durden
        :location: Pittsburgh, SF
        :category: Example, How To
        :redirect: blog/old-page-name-for-the-post
        :excerpt: 2
        :image: 1


   **Drafts & Posts**

   Posts without dates or with future dates are considered as drafts and
   are published only in :ref:`blog-drafts` page.

   Posts with dates that are older than the day Sphinx project is built are
   published in :ref:`blog-posts` page.

   Post date format must match the format specified with
   :confval:`post_date_format` configuration option.

   **Authors & Locations**

   **Tags & Categories**

   **Redirections**

   You can make ABlog create pages that will redirect to current post
   using ``:redirect:`` option.  It takes a comma separated list of paths,
   relative to the root folder.  The redirect page waits for
   :confval:`post_redirect_refresh` seconds before redirection occurs.

   **Excerpts & Images**



Listing
-------

A list of posts can be displayed in any page using the following directive:

.. rst:directive:: postlist

   Following example will list most recent 5 posts::

     .. postlist:: 5


.. postlist:: 5

..
        :tags: tips
        :author: Ahmet
        :location: Pittsburgh
        :category: How To
        :reverse:

   This will result in a bullet list of up to 6 posts (default is all)
   authored by :ref:`author-ahmet` from :ref:`location-pittsburgh` posted
   in :ref:`category-manual` and tagged with :ref:`tag-tips`.  Posts
   will be in reverse chronological order.

