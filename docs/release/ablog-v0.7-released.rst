ABlog v0.7 released
===================

.. post:: May 3, 2015
   :author: Ahmet
   :category: Release
   :location: Denizli

ABlog v0.7.0 is released to fix the long standing :issue:`1` related to
pickling of Sphinx build environment on Read The Docs. Improvements
also resolved issues with using LaTeX builder, improved cross-referencing
for non-html builders.

ABlog v0.7.1 released
---------------------

ABlog v0.7.1 is released to fix Python 3 import issues in :command:`ablog serve`
command.

ABlog v0.7.2 released
---------------------

ABlog v0.7.2 is released to prevent potential issues with Disqus thread URLs
by requiring :confval:`disqus_shortname` and :confval:`blog_baseurl`
to be specified together for Disqus integration.

ABlog v0.7.3 released
---------------------

ABlog v0.7.3 makes use of `python-dateutil`__ for parsing post dates, so now you
can be flexible with the format you use in posts. Thanks to `Andy Maloney`__
for this improvement.

__ https://pypi.python.org/pypi/python-dateutil
__ https://github.com/amaloney

ABlog v0.7.5 released
---------------------

ABlog v0.7.5 is released to fix Windows specific path resolving issue with
archive pages. Thanks to Peter Mills for reporting this issue.

ABlog v0.7.6 released
---------------------

ABlog v0.7.6 is released to fix path resolving issue that arose when
``:excerpts:`` is used in :rst:dir:`postlist` directive. Once again, thanks
to Peter Mills for reporting this issue. Other minor changes are:

  * ``-P`` argument is added to :ref:`ablog build <build>` command to enable running pdb
    on exceptions.

  * ``conf.py`` file created by :ref:`ablog start <start>` updated to include
    ``about.html`` sidebar that comes with Alabaster_ theme.

ABlog v0.7.7 released
---------------------

ABlog v0.7.7 is released to fix path resolving :issue:`41` that arose when
cross-references were used in post excerpts, and also post redirect
issue in templates.

ABlog v0.7.8 released
---------------------

ABlog v0.7.8 is released to fix a Python 2 issue that appears when creating
collection pages that contain non-ascii characters in their names (:issue:`45`)
and filename escaping issue when committing changes using
:ref:`ablog deploy <deploy>` command (:pull:`44`).
Thanks to `uralbash`_ for these contributions.

.. _uralbash: https://github.com/uralbash

ABlog v0.7.9 released
---------------------

ABlog v0.7.9 is released to fix Windows specific file renaming issue in
:ref:`ablog deploy <deploy>` command (:issue:`46`). Thanks to `Velimir`_
for the fix.

.. _Velimir: https://github.com/montyvesselinov

ABlog v0.7.10 released
----------------------

ABlog v0.7.10 is released to resolve Sphinx JSON/Pickle builder issues
related to serialization.

ABlog v0.7.12 released
----------------------

ABlog v0.7.12 (and also v0.7.11) maintenance release are available.
