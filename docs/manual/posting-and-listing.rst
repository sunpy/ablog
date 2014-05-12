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

Any page in a Sphinx_ project can be converted to a post using the
following directive:


.. rst:directive:: post

   All possible directive options are shown below::

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

   You can specify the author and location of a post using ``:author:``
   and ``:location:`` options. Using :confval:`blog_authors` and
   :confval:`blog_locations` configuration variables, you can also provide
   a link to authors and locations, which will be displayed in
   archive pages generated for all unique authors and locations.

   **Tags & Categories**

   You can specify multiple tags and categories per post, and the post
   will be listed in archive pages generated for each unique tag and
   category.

   **Redirections**

   You can make ABlog create pages that will redirect to current post
   using ``:redirect:`` option.  It takes a comma separated list of paths,
   relative to the root folder.  The redirect page waits for
   :confval:`post_redirect_refresh` seconds before redirection occurs.

   **Excerpts & Images**

   By default, ABlog uses the first paragraph of a page as post excerpt.
   You can change this behavior and also add an image to the excerpt.
   To find out how, see :ref:`post-excerpts-and-images`.


Listing
-------

A list of posts can be displayed in any page using the following directive:

.. rst:directive:: postlist

   Following example will list most recent 5 posts::

     .. postlist:: 5


   .. postlist:: 5


   Note that if the current post is one of the most recent posts, it will
   be omitted.

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

