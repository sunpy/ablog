Cross-referencing Blog Pages
============================

.. post:: May 11, 2014
   :tags: tips, Sphinx
   :category: Manual
   :location: Pittsburgh
   :author: Ahmet

ABlog creates references to all post and archive pages.  Posts can be
cross-referenced using the name of the file, or when the file is named
:file:`index`, the name of the folder that contains the file.

This page, :ref:`cross-referencing-blog-pages`, for example is referenced
as ``:ref:`cross-referencing-blog-pages``` using :rst:role:`ref` role.

.. _archives:

Archive pages
-------------

Archive pages, on the other hand, can be cross-referenced by combining
archive type and archive name as follows:

==============  ==========================  ===============================
Archive         Example                     reStructured Text
==============  ==========================  ===============================
Posts           :ref:`blog-posts`           ``:ref:`blog-posts```
Drafts          :ref:`blog-drafts`          ``:ref:`blog-drafts```
Tag             :ref:`tag-config`           ``:ref:`tag-config```
Author          :ref:`author-ahmet`         ``:ref:`author-ahmet```
Archive         :ref:`archive-2014`         ``:ref:`archive-2014```
Location        :ref:`location-pittsburgh`  ``:ref:`location-pittsburgh```
Category        :ref:`category-manual`      ``:ref:`category-manual```
==============  ==========================  ===============================

Following archive pages list all posts by grouping them:

==============  ==========================  ===============================
Archive         Example                     reStructured Text
==============  ==========================  ===============================
By tag          :ref:`blog-tags`            ``:ref:`blog-tags```
By author       :ref:`blog-authors`         ``:ref:`blog-authors```
By location     :ref:`blog-locations`       ``:ref:`blog-locations```
By category     :ref:`blog-categories`      ``:ref:`blog-categories```
By archive      :ref:`blog-archives`        ``:ref:`blog-archives```
==============  ==========================  ===============================


When posts have long file or folder names, it may be convenient to use
them repeatedly for cross-referencing.  An alternative that Sphinx_ offers
is creating your own short and unique labels for cross-referencing to posts.
See :ref:`xref-syntax` for details.