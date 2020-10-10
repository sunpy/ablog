Posting and Listing
===================

.. post:: May 9, 2014
   :tags: directive
   :category: Manual
   :location: Pittsburgh
   :author: Ahmet

This post describes :rst:dir:`post`, :rst:dir:`update`, and :rst:dir:`postlist` directives.

Posting
-------

Any page in a Sphinx_ project can be converted to a post using the following directive:

.. rst:directive:: post

   All possible directive options are shown below::

     .. post:: 15 Apr, 2013
        :tags: tips, ablog, directive
        :category: Example, How To
        :author: Ahmet, Durden
        :location: Pittsburgh, SF
        :redirect: blog/old-page-name-for-the-post
        :excerpt: 2
        :image: 1
        :nocomments:

   **Drafts & Posts**

   Posts without dates or with future dates are considered as drafts and are published only in :ref:`blog-drafts` archive page.

   Posts with dates that are older than the day Sphinx project is built are published in :ref:`blog-posts` page.

   Post date format must follow the format specified with confval:`post_date_format` configuration option.

   **Tags & Categories**

   You can specify multiple tags and categories by separating them with commas.
   Posts will be listed in archive pages generated for each unique tag and category.

   **Authors, Languages, & Locations**

   Likewise, you can specify authors, languages, and locations of a post using ``:author:``, ``:language:``, and ``:location:`` options.
   All of these option names are in their singular form, but multiple values separated by commas are accepted.

   Using :confval:`blog_authors`, :confval:`blog_languages`, and :confval:`blog_locations` configuration variables, you can also provide home pages and/or full display names of authors, languages, and locations, which will be displayed in archive pages generated for all unique authors, languages, and locations.

   **Redirections**

   You can make ABlog create pages that will redirect to current post using ``:redirect:`` option.  It takes a comma separated list of paths, relative to the root folder.
   The redirect page waits for :confval:`post_redirect_refresh` seconds before redirection occurs.

   **Disable comments**

   You can disable comments for the current post using the ``:nocomments:`` option.
   Currently there is no way to disable comments in a specific page.

   **Excerpts & Images**

   By default, ABlog uses the first paragraph of a page as post excerpt.
   You can change this behavior and also add an image to the excerpt.
   To find out how, see :ref:`post-excerpts-and-images`.

   **Update Notes**

   .. rst:directive:: update

      Update in a post can be noted anywhere in the post as follows::

        .. update:: 20 Apr, 2014

           Added :rst:dir:`update` directive and :ref:`posting-sections` section.
           Also revised the text here and there.

      Update date format must follow the format specified with :confval:`post_date_format` configuration option.

      Update directive renders like the updates that are at the end of this post.

.. _posting-sections:

Posting Sections
----------------

.. post:: Aug 20, 2014
   :tags: directive
   :category: Manual
   :location: SF
   :author: Ahmet

:rst:dir:`post` directive can be used multiple times in a single page to create multiple posts of different sections of the document.

When :rst:dir:`post` is used more than once, post titles and excerpts are extracted from the sections that contain the directives.
This behavior can also be set as the default behavior using :confval:`post_always_section` configuration options.

Some caveats and differences from posting a document once are:

  * Next and previous links at the bottom will only regard the first post in the document.
  * Information displayed on the sidebar will belong to the first post.
  * References for section posts is not automatically created. Labels for cross-referencing needs to be created manually, e.g., ``.. _posting-sections``. See :ref:`xref-syntax` for details.

Multiple use of :rst:dir:`post` may be suitable for major additions to a previous post. For minor changes, :rst:dir:`update` directive may be preferred.

Listing
-------

A list of posts can be displayed in any page using the following directive:

.. rst:directive:: postlist

    Following example display all the options the directive takes::

     .. postlist:: 5
        :author: Ahmet
        :category: Manual
        :location: Pittsburgh
        :language: en
        :tags: tips
        :date: %A, %B %d, %Y
        :format: {title} by {author} on {date}
        :list-style: circle
        :excerpts:
        :sort:

   This will result in a bullet list of up to 5 posts (default is all) authored by `:ref:`author-ahmet`` in `:ref:`language-en`` when he was in `:ref:`location-pittsburgh`` and posted in `:ref:`category-manual`` with tags `:ref:`tag-tips``.
   Posts will be in ``:sort:``\ed to appear in chronological order and listed with their ``:excerpts:``.
   Here are those posts:

   .. postlist:: 5
      :author: Ahmet
      :category: Manual
      :location: Pittsburgh
      :language: en
      :tags: tips
      :date: %A, %B %d, %Y
      :format: {title} by {author} on {date}
      :list-style: circle
      :excerpts:
      :sort:


   When no options are given all posts will be considered and they will be ordered by recency.
   Also, note that if the current post is one of the most recent posts, it will be omitted.

.. update:: Aug 20, 2014

   Added :rst:dir:`update` directive and
   :ref:`posting-sections` section.
   Also revised the text here and there.

.. update:: Sep 15, 2014

   * :rst:dir:`post` directive has ``:language:`` option.
   * :rst:dir:`postlist` directive takes arguments to filter posts.

.. update:: Mar 28, 2015

   Added ``:excerpts:`` option to :rst:dir:`postlist` to list posts with their excerpts.

.. update:: Apr 14, 2015

   Added ``:list-style:`` option to :rst:dir:`postlist` to control bullet list style.
   *circle*, *disk*, and *none* (default) are recognized.
