ABlog v0.11 released
====================

.. post:: March 23, 2023
   :author: Nabil Freij
   :category: Release
   :location: World

ABlog v0.11 is released with the main focus being to update and tweak the HTML templates allow themes to override the default templates.
In addition, all ablog elements in the templates wrapped in ``ablog__*`` divs to allow custom CSS rules.

We also adopt `NEP29 <https://numpy.org/neps/nep-0029-deprecation_policy.html>` and drop support for older versions of Python and package versions that are 24 months old or older at time of release.

Added support for external links to be posts.

There are several breaking changes:

- 1. The template files are now in the `templates/ablog` folder.
     Older templates are still in the old location but will raise a warning.
     These will be removed in a future version, please do not use them anymore.
     You will need to update any paths to them to add "ablog/" to the path.
- 2. ``ablog`` has support for not injecting its own templates into the Sphinx build.
     This is supported by add `skip_injecting_base_ablog_templates = True` to your configuration file.
- 3. Minimum version of Python is >=3.9 and Sphinx is >=5.0.

Pull Requests merged in:

`Template rework <https://github.com/sunpy/ablog/pull/144>`__.

`Add external links for posts <https://github.com/sunpy/ablog/pull/112>`__ from `Chris Holdgraf <https://github.com/choldgraf>`__.
