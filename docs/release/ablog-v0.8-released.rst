ABlog v0.8 released
===================

.. post:: Oct 12, 2015
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.8.0 is released with additions and changes:

  * Added ``-a`` argument to :ref:`ablog build <build>` command, with which
    you can force rewriting all pages when rebuilding your project. Default is
    writing only pages that have changed.

  * Added ``-f`` argument to :ref:`ablog deploy <deploy>` command, with which
    you can amend to latest commit to keep GitHub pages repository small.
    Thanks to `uralbash`_ for this contribution.

  * Added ``-p`` argument to :ref:`ablog deploy <deploy>` command, with which
    you can specify the path to your GitHub pages repository, i.e.
    ``username.github.io``.

  * Changed :confval:`fontawesome_link_cdn` to be a string argument to enable
    linking to desired version of `Font Awesome`_. Thanks to `Albert Mietus`_
    for this contribution.

  * Post lists font style is now controlled through CSS. Thanks to
    `Albert Mietus`_ for this contribution as well.

  * Fixed internal link resolution issue that affected atom feeds of
    collections, i.e. feeds of posts under a category, tag, or author.

.. _Font Awesome: https://fortawesome.github.io/Font-Awesome/
.. _Albert Mietus: https://github.com/AlbertMietus
.. _uralbash: https://github.com/uralbash

ABlog v0.8.1 released
---------------------

.. post:: Oct 24, 2015
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.8.1 is released to fix atom feed linking in HTML header (:issue:`54`).

ABlog v0.8.2 released
---------------------

.. post:: Jan 6, 2016
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.8.2 is released to fix date parsing (:issue:`58`) and Python 2.6
installation (:issue:`59`) issues.

ABlog v0.8.3 released
---------------------

.. post:: Apr 23, 2016
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.8.3 is released to bring you recent enhancements:

  * `ninmesara`_ added ``:nocomments:`` argument to :rst:dir:`post` directive
    to disable comments per post.
  * `José Carlos García`_ added Spanish translations.

.. _ninmesara: https://github.com/ninmesara
.. _José Carlos García: https://github.com/quobit
