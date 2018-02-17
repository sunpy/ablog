ABlog v0.9 released
===================

.. post:: Feb 17, 2018
   :author: Nabil
   :category: Release
   :location: World


ABlog v0.9.0 is released with the main focus being to support the latest version of Sphinx.


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
