ABlog v0.10 released
====================

.. post:: Nov 17, 2019
   :author: Nabil
   :category: Release
   :location: World

ABlog v0.10 is released with the main focus being to support the latest version of Sphinx as well as Python 3 only support.

Ablog V0.9.X will no longer be supported as Python 2 comes to an end in a few months and it is time people upgraded.

Pull Requests merged in:

`Overhaul of package underneath for python3 only <https://github.com/sunpy/ablog/pull/41>`__ from `nabobalis <https://github.com/nabobalis>`__.

`Add validation for conf.py entries <https://github.com/sunpy/ablog/pull/38>`__ from `rayalan <https://github.com/rayalan>`__.

`Deploy improve <https://github.com/sunpy/ablog/pull/42>`__ from `rayalan <https://github.com/rayalan>`__.

`Get ablog ready for 0.10 <https://github.com/sunpy/ablog/pull/46>`__ from `nabobalis <https://github.com/nabobalis>`__.

ABlog v0.10.1 released
----------------------
.. post:: Dec 17, 2019
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Change StopIteration to return <https://github.com/sunpy/ablog/pull/48>`__ from `remyabel <https://github.com/remyabel>`__.

ABlog v0.10.2 released
----------------------
.. post:: Jan 2, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Fix unclosed span tag <https://github.com/sunpy/ablog/pull/41>`__ from `ykrods <https://github.com/ykrods>`__.

ABlog v0.10.3 released
----------------------
.. post:: Feb 12, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Pin werkzeug to < 1 <https://github.com/sunpy/ablog/pull/53>`__ from `dstansby <https://github.com/dstansby>`__.

`MNT: Fix Giles URL <https://github.com/sunpy/ablog/pull/50>`__ from `pllim <https://github.com/pllim>`__.

ABlog v0.10.4 released
----------------------
.. post:: March 24, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Add zh_CN locale <https://github.com/sunpy/ablog/pull/61>`__ from `daimon99 <https://github.com/daimon99>`__.

`Add intersphinx to the extension list <https://github.com/sunpy/ablog/pull/60>`__ from `plaindocs <https://github.com/plaindocs>`__.

`Fix "test5" <https://github.com/sunpy/ablog/pull/58>`__ and `Use "dirhtml" builder on Read The Docs <https://github.com/sunpy/ablog/pull/57>`__ from `blueyed <https://github.com/blueyed>`__.

ABlog v0.10.5 released
----------------------
.. post:: Apr 18, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Add custom GitHub URL support <https://github.com/sunpy/ablog/pull/63>`__ from `tg-m <https://github.com/tg-m>`__.

ABlog v0.10.6 released
----------------------
.. post:: May 27, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Add french locale <https://github.com/sunpy/ablog/pull/65>`__ from `kujiu <https://github.com/kujiu>`__.

ABlog v0.10.7 released
----------------------
.. post:: Sept 7, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Automatically add templates path to documentation <https://github.com/sunpy/ablog/pull/63>`__ from `choldgraf <https://github.com/choldgraf>`__.

ABlog v0.10.8 released
----------------------
.. post:: Sept 9, 2020
   :author: Nabil
   :category: Release
   :location: World

Removed the hard dependencies on alabaster and sphinx-automodapi.

Replaced `werkzeug <https://pypi.org/project/Werkzeug/>`__ with `feedgen <https://pypi.org/project/feedgen/>`__ due to the former removing ATOM support.

Version pin of nbsphinx has been removed.

ABlog v0.10.9 released
----------------------
.. post:: Sept 16, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`frontmatter and blog post matching <https://github.com/sunpy/ablog/pull/63>`__ from `choldgraf <https://github.com/choldgraf>`__.

ABlog v0.10.10 released
-----------------------
.. post:: Oct 10, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Various Issues <https://github.com/sunpy/ablog/pull/77>`__.

`Fix missing reference caused by ref with title <https://github.com/sunpy/ablog/pull/73>`__ from `ykrods <https://github.com/ykrods>`__.

`Add instructions for starting new blog posts with front-matter <https://github.com/sunpy/ablog/pull/71>`__ from `kakirastern <https://github.com/kakirastern>`__.

ABlog v0.10.11 released
-----------------------
.. post:: Oct 11, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`improving glob matching and documenting it <https://github.com/sunpy/ablog/pull/79>`__ from `choldgraf <https://github.com/choldgraf>`__.


ABlog v0.10.12 released
-----------------------
.. post:: Nov 3, 2020
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`id of feed is now blog.blog_baseurl <https://github.com/sunpy/ablog/pull/83>`__.

ABlog v0.10.13 released
-----------------------
.. post:: Jan 19, 2021
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`updated CI and py39 tests <https://github.com/sunpy/ablog/pull/86>`__.
`Add test #87 <https://github.com/sunpy/ablog/pull/87>`__.
`Some minor fixes <https://github.com/sunpy/ablog/pull/88>`__.
`Ensure blog_post_pattern are relative to srcdir <https://github.com/sunpy/ablog/pull/89>`__.

ABlog v0.10.14 released
-----------------------
.. post:: March 21, 2021
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`feat(feeds): Add missing Atom entry metadata <https://github.com/sunpy/ablog/pull/92>`__.
`feat(feeds): Add entry element template support <https://github.com/sunpy/ablog/pull/93>`__.
`misc update <https://github.com/sunpy/ablog/pull/94>`__.


ABlog v0.10.15 released
-----------------------
.. post:: March 22, 2021
   :author: Nabil
   :category: Release
   :location: World

Fixed `Index Out of Range with Atom Feeds <https://github.com/sunpy/ablog/issues/96>`__.

ABlog v0.10.16 released
-----------------------
.. post:: March 23, 2021
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`fix(feeds): Feed validation, templates regression <https://github.com/sunpy/ablog/pull/97>`__.

ABlog v0.10.17 released
-----------------------
.. post:: March 24, 2021
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Correct draft URL <https://github.com/sunpy/ablog/pull/98>`__.

ABlog v0.10.18 released
-----------------------
.. post:: April 26, 2021
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Correct posts URL <https://github.com/sunpy/ablog/pull/99>`__.
`Add isso integration <https://github.com/sunpy/ablog/pull/100>`__.

ABlog v0.10.19 released
-----------------------
.. post:: May 26, 2021
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`Add expand option <https://github.com/sunpy/ablog/pull/104>`__.


ABlog v0.10.20 released
-----------------------
.. post:: Oct 13, 2021
   :author: Nabil
   :category: Release
   :location: World

Pull Requests merged in:

`fix documentation typo in blog-drafts <https://github.com/sunpy/ablog/pull/105>`__.
`Fix typo in "extennsion" <https://github.com/sunpy/ablog/pull/109>`__.
`Catalan translation <https://github.com/sunpy/ablog/pull/113>`__.
`Fix ablog post <https://github.com/sunpy/ablog/pull/114>`__.
