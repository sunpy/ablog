ABlog v0.3 released
===================

.. post:: Sep 15, 2014
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.3 is released. This version comes with the following core
improvements:

  * You can now specify language of a post with ``:language:`` option,
    and an archive page will be created for each language.
    See :confval:`blog_languages` and :confval:`blog_default_language`
    if you are posting in multiple languages.

  * You can list language archives on your website by adding
    ``languages.html`` to :confval:`html_sidebars` configuration option.

  * :rst:dir:`postlist` directive takes options to filter posts.

ABlog v0.3.1 released
---------------------

.. post:: Sep 24, 2014
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.3.1 is a minor release to fix two issues in templates:

  * Links to collection (archive) feeds is displayed only on collection page
    (e.g. `:ref:`category-manual``), not on a catalog page that lists posts
    for multiple collections (e.g. `:ref:`blog-categories``).

  * Links to collection feeds is displayed only when they are generated
    (see :confval:`blog_feed_archives`). Previously, links would be generated
    to feeds that did not exist.
