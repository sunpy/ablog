ABlog v0.11 released
====================

.. post:: july 25, 2022
   :author: Nabil Freij
   :category: Release
   :location: World

ABlog v0.11 is released with the main focus being to update and tweak the HTML templates allow themes to override the default templates.
In addition, all ablog elements in the templates wrapped in ``ablog__*`` divs to allow custom CSS rules.

Added support for external links to be posts.

There are several breaking changes:

- 1. The template files are now in the `templates/ablog` folder.
- 2. In theory ablog will now append the tempaltes to the start of the template list, this could break themes without support for it.
- 3. Minimum version of Python is >=3.8 and Sphinx is >=5.0.
- 4. Latex building is now not possible anymore.
     This could change in future but for the first release of 0.11, it is nonfunctional.

Pull Requests merged in:

`Template rework <https://github.com/sunpy/ablog/pull/144>`__.

`Add external links for posts <https://github.com/sunpy/ablog/pull/112>`__ from `Chris Holdgraf <https://github.com/choldgraf>`__.