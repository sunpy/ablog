Templating and Themes Support
=============================

.. post:: Oct 26, 2024
   :tags: themes
   :category: Manual
   :author: Libor

Ablog, being a Sphinx extension, has highly customizable HTML output. The generated HTML files are based on `Sphinx templates`_. You, or Sphinx themes, can partially or completely override these templates to customize the resulting HTML.

.. _Sphinx templates: https://www.sphinx-doc.org/en/master/development/html_themes/templating.html

.. versionchanged:: 0.11
   The :doc:`Ablog 0.11 </release/ablog-v0.11-released>` has changed and improved the way you can customize templates and themes. Please note that this document describes the new way of customizing templates and themes support.

.. _sidebars:

Blog sidebars
-------------

Sidebars are a common way to provide additional information to the reader. There are seven Ablog sidebars you can include in your HTML output using the Sphinx_ :confval:`html_sidebars` configuration option (in addition to your theme sidebars).

- ``alog/postcard.html`` provides information regarding the current post (when on a post page).
- ``alog/recentposts.html`` lists the most recent five posts.
- ``alog/tagcloud.html`` provides links to archive pages generated for each tag.
- ``alog/category.html``, ``alog/authors.html``, ``alog/languages.html``, and ``alog/locations.html`` sidebars generate lists of links to respective archive pages with the number of matching posts (e.g., "Manual (14)", "2023 (8)", "English (22)").

For example, the sidebars that you see on this website on the left are:

.. code-block:: python

   html_sidebars = {
      "**": [
         # Comes from Alabaster theme
         "about.html",  
         "searchfield.html",
         # Ablog sidebars
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

Ablog standard sidebars are wrapped in ``<div>`` with CSS classes like :samp:`ablog-sidebar-item ablog__{<template_name>}`, making them easier to style.

For example, the ``recentposts.html`` template is wrapped in ``<div class="ablog-sidebar-item ablog__recentposts">``.

.. seealso::
   
   Built-in sidebars can be found in the ``ablog/`` folder in the `Ablog source code <https://github.com/sunpy/ablog/tree/main/src/ablog/templates/ablog>`_.

If styling is not enough, you can override the Ablog templates in your Sphinx project or in the Sphinx theme.

Partial or complete override of Ablog templates
-----------------------------------------------

To control whether Ablog injects its own templates into the Sphinx build, you can use the following ``conf.py`` configuration option:

.. confval:: skip_injecting_base_ablog_templates
   
   If set to ``True``, Ablog will not inject its own templates into the Sphinx build. This is useful if you want to completely override Ablog templates in your Sphinx project or in the Sphinx theme. The default is ``False``.

Customizing templates in the project
------------------------------------

All Ablog templates are under the ``ablog/`` folder space. For example, ``ablog/postcard.html``. You can override these templates by placing them in the ``ablog/`` folder in your project templates folder.

#. Add the :confval:`templates_path` option in your ``conf.py`` file:

   .. code-block:: python

      templates_path = ["_templates"]

#. Create a folder ``_templates/`` next to your ``conf.py`` file. It will hold your custom templates.
#. Create a folder ``ablog/`` inside the ``_templates/`` folder.
#. Create a file here with the same name as the template you want to override. For example, ``postcard.html``. This file will be used as a custom template for the sidebar. You can copy the content of the original template from the Ablog source code and modify it as you need.
#. Optionally: if you want to completely override all Ablog templates, set the :confval:`skip_injecting_base_ablog_templates` option to ``True``, copy all Ablog templates here, and customize them as you need.

Customizing templates in the theme
----------------------------------

If you are a Sphinx theme author, you can ship customized Ablog templates in your theme. You can override Ablog templates by placing them in the ``ablog/`` folder in your theme templates, e.g., ``ablog/postcard.html``.

#. In the theme root (where the ``theme.toml`` (or ``theme.ini`` in older Sphinx themes) file is), create a folder ``ablog/``.
#. Create a file here with the same name as the template you want to override. For example, ``postcard.html``.
#. This file will be used as a custom template for the sidebar. You can copy the content of the original template from the Ablog source code and modify it as you need.
#. In your ``theme.toml`` file, add the following (under the ``[options]`` section):

   .. code-block:: toml
      
      ablog_inject_templates_after_theme = true
   
   This will ensure that Ablog templates are injected *after* the theme templates, so you can override them while still using the Ablog templates as a fallback.