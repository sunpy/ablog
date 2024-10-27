Templating and Themes Support
=============================

.. post:: Oct 26, 2024
   :tags: themes
   :category: Manual
   :author: Libor

Ablog, as being Sphinx extensions, it has highly customizable HTML output. The generated HTML files are based `Sphinx templates`_. You, or Sphinx themes can partially or completely override these templates to customize the resulting HTML.

.. _Sphinx templates: https://www.sphinx-doc.org/en/master/development/html_themes/templating.html

.. versionchanged:: 0.11
   The :doc:`Ablog 0.11 </release/ablog-v0.11-released>` has changed and improved the way how you can customize templates and themes. Please note that this document describes the new way of customizing templates and themes support.

.. _sidebars:

Blog sidebars
-------------

Sidebars are a common way to provide additional information to the reader. There are seven Ablog sidebars you can include in your HTML output using Sphinx_ :confval:`html_sidebars` configuration option (in addition to your theme sidebars).

- ``alog/postcard.html`` provides information regarding the current post (when on a post page)
- ``alog/recentposts.html`` lists most recent five posts.
- ``alog/tagcloud.html`` provides a links to a archive pages generated for each tag
- ``alog/category.html``, ``alog/authors.html``, ``alog/languages.html``, and ``alog/locations.html`` sidebars generates list of link to respective archive pages with number of matching posts (e.g., "Manual 14)", "2023 (8)", "English (22")).

For example, sidebars that you see on this website on the left are:

.. code-block:: python

   html_sidebars = {
      "**": [
         # Comes from Alabaster theme
         "about.html",  
         "searchfield.html",
         # Ablog sidebards
         "ablog/postcard.html",
         "ablog/recentposts.html",
         "ablog/tagcloud.html",
         "ablog/categories.html",
         "ablog/archives.html",
         "ablog/authors.html",
         "ablog/languages.html",
         "ablog/locations.html",
      ]
   }

Styling default Ablog sidebars
------------------------------

Ablog standard sidebars are wrapped in ``<div>`` with CSS classes like ``ablog-item ablog__{{ TEMPLATE-FILENAME }}`` making easier to style them. For example, the ``postcard.html`` template is wrapped in ``<div class="ablog-item ablog__postcard">``.

Buitin sidebars can be found in the ``ablog/`` folder in the `Ablog source code <https://github.com/sunpy/ablog/tree/main/src/ablog/templates/ablog>`_.

If styling is not enough, you can override the Ablog templates in your Sphinx project or in the Sphinx theme.

Partial or complete override of Ablog templates
-----------------------------------------------

To control whether Ablog injects its own templates into the Sphinx build, you can use the following ``conf.py`` configuration option:

.. confval:: skip_injecting_base_ablog_templates
   
   If set to ``True``, Ablog will not inject its own templates into the Sphinx build. This is useful if you want to completely override Ablog templates in your Sphinx project or in the Sphinx theme. Default is ``False``.

Customizing templates in the project
------------------------------------

All Ablog templates are under ``ablog/`` folder space. For example, ``ablog/postcard.html``. You can override these templates by placing them in the ``ablog/`` folder in your project templates folder.

#. Add the :confval:`templates_path` option in your ``conf.py`` file:

   .. code-block:: python

      templates_path = ["_templates"]

#. Create a folder ``_templates/`` next to your ``conf.py`` file. It will hold your custom templates.
#. Create a folder ``ablog/`` inside the ``_templates/`` folder.
#. Create here a file with the same name as the template you want to override. For example, ``postcard.html``. This file will be used as a custom template for the sidebar. You can copy the content of the original template from the Ablog source code and modify it as you need.
#. Optionall: if you want to complete override all Ablog templates, set the :confval:`skip_injecting_base_ablog_templates` option to ``True``, copy all Ablog templates here and customize them as you need.

Customizing templates in the theme
----------------------------------

If you are a Sphinx theme author, you can ship customized Ablog templates in your theme. You can override Ablog templates by placing them in the ``ablog/`` folder in your theme templates, e.g., ``ablog/postcard.html``.

#. In theme root (where is the ``theme.conf`` file), create a folder ``ablog/``.
#. Create here a file with the same name as the template you want to override. For example, ``postcard.html``.
#. This file will be used as a custom template for the sidebar. You can copy the content of the original template from the Ablog source code and modify it as you need.
#. In your ``theme.conf`` file, add the following (under the ``[options]`` section):

   .. code-block:: ini
      
      ablog_inject_templates_after_theme = true
   
   This will make sure that Ablog templates are injected *after* the theme templates, so you can override them while still using the Ablog templates as a fallback.