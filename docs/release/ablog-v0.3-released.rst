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