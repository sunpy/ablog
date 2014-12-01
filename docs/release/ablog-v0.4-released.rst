ABlog v0.4 released
===================

.. post::
   :author: Ahmet
   :category: Release
   :location: SF


ABlog v0.4 is released. This version comes with the following improvements
and bug fixes:

  * Added :confval:`blog_feed_titles`, :confval:`blog_feed_length`, and
    :confval:`blog_archive_titles` configuration options (see :issue:`24`).

  * Set the default for :confval:`blog_feed_archives` to ``False``, which
    was set to ``True`` although documented to be otherwise.

  * Fixed issues with :confval:`post_auto_excerpt` and
    :confval:`post_auto_image` configuration options.

  * Issue :issue:`2`, relative size of tags being the minimum size when
    all tags have the same number of posts, is fixed. Now, mean size is
    used, and max/min size can be controlled from template.

  * Issue :issue:`19` is fixed. Yearly archives are ordered by recency.

  * Issue :issue:`21`, duplicated post title in feeds, is fixed.

  * Issue :issue:`22`, :rst:dir:`postlist` directive listing more than
    specified number of posts, is fixed.

  * :rst:dir:`postlist` directive accepts arguments to format list items
    (:issue:`20`).