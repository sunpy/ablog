ABlog Internationalization
==========================

.. post:: Aug 30, 2014
   :tags: i18n
   :category: Manual
   :author: Luc, Ahmet
   :language: Chinese

ABlog automatically generates certain labels like :ref:`blog-posts` and :ref:`blog-categories`.
If these labels appear in English on your blog although you specified another language, then this page is for you.

ABlog needs your help for translation of these labels.
Translation process involves the following steps:

* Update translatable messages:

   Execute extract_messages_ each time a translatable message text is changed or added::

      $ python setup.py extract_messages -o ablog/locales/sphinx.pot
      ...

   This will create or update :file:`ablog/locales/sphinx.pot` file, the central messages catalog used by the different translations.

Either:

* Create new translation catalog:

   Execute init_catalog_ once for each *new* language, e.g.::

      $ python setup.py init_catalog -l de -i ablog/locales/sphinx.pot -o ablog/locales/de/LC_MESSAGES/sphinx.po

   This will create a file :file:`ablog/locales/de/LC_MESSAGES/sphinx.po` in which translations needs to be placed.

* Update translation catalog:

   Execute update_catalog_ for each *existing* language, e.g.::

      $ python setup.py update_catalog -l de -i ablog/locales/sphinx.pot -o ablog/locales/de/LC_MESSAGES/sphinx.po

   This will update file :file:`ablog/locales/de/LC_MESSAGES/sphinx.po` where translations of new text needs to be placed.

Finally:

* Compile catalogs:

   Execute compile_catalog_ for each existing language, e.g::

     $ python setup.py compile_catalog --directory ablog/locales/ --domain sphinx --locale de

   If you remove ``--locale de`` then all catalogs will be compiled.

.. _extract_messages: https://babel.pocoo.org/en/latest/setup.html#extract-messages
.. _init_catalog: https://babel.pocoo.org/en/latest/setup.html#init-catalog
.. _update_catalog: https://babel.pocoo.org/en/latest/setup.html#update-catalog
.. _compile_catalog: https://babel.pocoo.org/en/latest/setup.html#compile-catalog
