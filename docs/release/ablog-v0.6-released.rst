ABlog v0.6 released
===================

.. post:: Apr 8, 2015
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.6 is released with new :ref:`ablog-commands`. You can use
``ablog deploy`` to :ref:`deploy-to-github-pages`, and also ``ablog clean``
to do spring cleaning every once in a while.

ABlog v0.6.1 released
---------------------

.. post:: Apr 9, 2015
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.6.1 is released with improvements to ``ablog deploy`` command.
It will add ``.nojekyll`` file when needed to deployments to GitHub pages.

ABlog v0.6.2 released
---------------------

.. post:: Apr 14, 2015
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.6.2 is released to fix an issue with loading of Disqus comments
(:issue:`33`) and interpreting non-ascii characters (:issue:`34`).

ABlog v0.6.3 released
---------------------

.. post:: Apr 15, 2015
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.6.3 comes with Russian localisation and following enhancements:

  * Added ``:list-style:`` option to :rst:dir:`postlist` to enable
    controlling bullet list style.

  * ``ablog post`` command de-slugifies filename to make the title
    when it's not given.

ABlog v0.6.4 released
---------------------

.. post:: Apr 19, 2015
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.6.4 comes with improved ``ablog serve`` command that helps you
:ref:`watch-yourself-blogging`.

ABlog v0.6.5 released
---------------------

.. post:: Apr 27, 2015
   :author: Ahmet
   :category: Release
   :location: SF

ABlog v0.6.5 is a bug fix release to resolve :issue:`38`, an exception raised
when using :rst:dir:`postlist` without specifying number of posts.
