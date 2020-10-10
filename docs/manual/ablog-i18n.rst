ABlog Internationalization
==========================

.. post:: Aug 31, 2014
   :tags: i18n
   :category: Manual
   :author: Luc, Ahmet

ABlog automatically generates certain labels like :ref:`blog-posts` and :ref:`blog-categories`.
If these labels appear in English on your blog although you specified another language, then this page is for you.

ABlog needs your help for translation of these labels.
Translation process involves the following steps:


1. Update translatable messages:

   Execute extract_messages_ each time a translatable message text is changed or added::

      $ python setup.py extract_messages -o ablog/locale/sphinx.pot
      ...

   This will create or update :file:`ablog/locale/sphinx.pot` file, the central messages catalog used by the different translations.

2.

  a. Create new translation catalog:

     Execute init_catalog_ once for each *new* language, e.g.::

        $ python setup.py init_catalog -l de -i ablog/locale/sphinx.pot -o ablog/locale/de/LC_MESSAGES/sphinx.po

     This will create a file :file:`ablog/locale/de/LC_MESSAGES/sphinx.po` in which translations needs to be placed.

  b. Update translation catalog:

     Execute update_catalog_ for each *existing* language, e.g.::

        $ python setup.py update_catalog -l de -i ablog/locale/sphinx.pot -o ablog/locale/de/LC_MESSAGES/sphinx.po

     This will update file :file:`ablog/locale/de/LC_MESSAGES/sphinx.po` where translations of new text needs to be placed.

3. Compile catalogs:

   Execute compile_catalog_ for each existing language, e.g::

     $ python setup.py compile_catalog --directory ablog/locale/ --domain sphinx --locale de

.. _extract_messages: http://babel.edgewall.org/wiki/Documentation/setup.html#extract-messages
.. _init_catalog: http://babel.edgewall.org/wiki/Documentation/setup.html#init-catalog
.. _update_catalog: http://babel.edgewall.org/wiki/Documentation/setup.html#update-catalog
.. _compile_catalog: http://babel.edgewall.org/wiki/Documentation/setup.html#id4
