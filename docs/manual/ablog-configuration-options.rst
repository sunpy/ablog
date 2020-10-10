.. _config:

ABlog Configuration Options
===========================

.. post:: May 10, 2014
   :tags: config
   :author: Ahmet
   :category: Manual
   :location: Pittsburgh


This post describes ABlog configuration options that go in :ref:`Sphinx build configuration file <sphinx:build-config>`.

General options
---------------

.. confval:: blog_path

   A path relative to the configuration directory for blog archive pages.
   Default is ``'blog'``.

.. confval:: blog_title

   The “title” for the blog, used in acthive pages.  Default is ``'Blog'``.

.. confval:: blog_baseurl

   Base URL for the website, required for generating feeds.

.. confval:: blog_archive_titles

   Choose to archive only post titles in collection pages, default is ``False``.

Authors, languages, & locations
-------------------------------

.. confval:: blog_authors

   A dictionary of author names mapping to author full display names and links.
   Dictionary keys are what should be used in ``post`` directive to refer to the author.
   Default is ``{}``.
   Example::

     blog_authors = {
         'Ahmet': ('Ahmet Bakan', 'http://ahmetbakan.com'),
         'Durden': ('Tyler Durden',
                    'https://en.wikipedia.org/wiki/Tyler_Durden'),
     }

.. confval:: blog_languages

   A dictionary of language code names mapping to full display names and links of these languages.
   Similar to :confval:`blog_authors`, dictionary keys should be used in ``post`` directive to refer to the locations.
   Default is ``{}``.
   Example::

     blog_languages = {
         'en': ('English', None),
     }

.. confval:: blog_locations

   A dictionary of location names mapping to full display names and links of these locations.
   Similar to :confval:`blog_authors`, dictionary keys should be used in ``post`` directive to refer to the locations.
   Default is ``{}``.

.. confval:: blog_default_author

   Name of the default author defined in :confval:`blog_authors`.
   Default is ``None``.

.. confval:: blog_default_language

   Code name of the default language defined in :confval:`blog_languages`.
   Default is ``None``.

.. confval:: blog_default_location

   Name of the default location defined in :confval:`blog_locations`.
   Default is ``None``.

.. update:: Sep 15, 2014

   Added :confval:`blog_languages` and :confval:`blog_default_language` configuration variables.

Post related
------------

.. confval:: post_date_format

   Date display format (default is ``'%b %d, %Y'``) for published posts that goes as input to :meth:`datetime.date.strftime`.

.. confval:: post_auto_excerpt

   Number of paragraphs (default is ``1``) that will be displayed as an excerpt from the post.
   Setting this ``0`` will result in displaying no post excerpt in archive pages.
   This option can be set on a per post basis using :rst:dir:`post` directive option ``excerpt``.

   See :ref:`post-excerpts-and-images` for a more detailed discussion.

.. confval:: post_auto_image

   Index of the image that will be displayed in the excerpt of the post.
   Default is ``0``, meaning no image.
   Setting this to ``1`` will include the first image, when available, to the excerpt.
   This option can be set on a per post basis using :rst:dir:`post` directive option ``image``.

.. confval:: post_redirect_refresh

   Number of seconds (default is ``5``) that a redirect page waits before refreshing the page to redirect to the post.

.. confval:: post_always_section

   When ``True``, post title and excerpt is always taken from the section that contains the :rst:dir:`post` directive, instead of the document.
   This is the behavior when :rst:dir:`post` is used multiple times in a document.
   Default is ``False``.

Blog feeds
----------

Turn feeds on by setting :confval:`blog_baseurl` configuration variable.

.. confval:: blog_feed_archives

   Choose to create feeds per author, location, tag, category, and year, default is ``False``.

.. confval:: blog_feed_fulltext

   Choose to display full text in blog feeds, default is ``False``.

.. confval:: blog_feed_subtitle

   Blog feed subtitle, default is ``None``.

.. confval:: blog_feed_titles

   Choose to feed only post titles, default is ``False``.

.. confval:: blog_feed_length

   Specify number of recent posts to include in feeds, default is ``None`` for all posts.

.. update:: Aug 24, 2014

   Added :confval:`blog_feed_archives`, :confval:`blog_feed_fulltext`, :confval:`blog_feed_subtitle`, and :confval:`post_always_section` options.

.. update:: Nov 27, 2014

   Added :confval:`blog_feed_titles`, :confval:`blog_feed_length`, and :confval:`blog_archive_titles` options.

.. _fa:

Font awesome
------------

ABlog templates will use of `Font Awesome`_ icons if one of the following is set:

.. _Font Awesome: https://fontawesome.io/

.. confval:: fontawesome_link_cdn

   URL to `Font Awesome`_ :file:`.css` hosted at `Bootstrap CDN`_ or anywhere else.
   Default: ``None``

   .. _Bootstrap CDN: https://www.bootstrapcdn.com/fontawesome/

.. update:: Jul 29, 2015

   :confval:`fontawesome_link_cdn` was a *boolean* option, and now became a *string* to enable using desired version of `Font Awesome`_.
   To get the old behavior, use ``‘https://netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.min.css'``.

.. confval:: fontawesome_included

   Sphinx_ theme already links to `Font Awesome`_.
   Default: ``False``

Alternatively, you can provide the path to `Font Awesome`_ :file:`.css` with the following configuration option:

.. confval:: fontawesome_css_file

   Path to `Font Awesome`_ :file:`.css` (default is ``None``) that will be linked to in HTML output by ABlog.

.. _disqus-integration:

Disqus integration
------------------

Of course one cannot think of a blog that doesn't allow for visitors to comment.
You can enable Disqus_ by setting :confval:`disqus_shortname` and :confval:`blog_baseurl` variables.
The reason for requiring :confval:`blog_baseurl` to be specified as of v0.7.2 is to ensure that Disqus associates correct URLs with threads when you serve new posts locally for the first time.

.. confval:: disqus_shortname

   Disqus_ short name for the website.

.. confval:: disqus_pages

   Choose to disqus pages that are not posts, default is ``False``.

.. confval:: disqus_drafts

   Choose to disqus posts that are drafts (without a published date), default is ``False``.

.. _sidebars:

Blog sidebars
-------------

Finally, there are seven sidebars you can include in your HTML output using Sphinx_ :confval:`html_sidebars` configuration option.
Sidebars that you see on the left are listed below in the same order:

.. code-block:: python

   html_sidebars = {
      '**': [...,
             'postcard.html', 'recentposts.html',
             'tagcloud.html', 'categories.html',
             'archives.html', ]
   }


:file:`postcard.html` provides information regarding the current post.
:file:`recentposts.html` lists most recent five posts.
Others provide a link to a archive pages generated for each tag, category, and year.
In addition, there are ``authors.html``, ``languages.html``, and ``locations.html`` sidebars that link to author and location archive pages.

Command Options
---------------

.. update:: Apr 7, 2015

   Added :ref:`commands` options.

.. confval:: ablog_website

   Directory name for build output files. Default is ``_website``.

.. confval:: ablog_doctrees

   Directory name for build cache files. Default is ``.doctrees``.

.. confval:: ablog_builder

   HTML builder, default is ``dirhtml``. Build HTML pages, but with a single directory per document.
   Makes for prettier URLs (no .html) if served from a webserver. Alternative is ``html`` to build one HTML file per document.

.. confval:: github_pages

   GitHub user name used by ``ablog deploy`` command.
   See :ref:`deploy` and :ref:`deploy-to-github-pages` for more information.
