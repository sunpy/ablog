ABlog v0.12 released
====================

.. post:: Nov 23, 2024
   :author: Nabil Freij
   :category: Release
   :location: World

ABlog v0.12 is released with the main focus being retemplating the library.

Features
--------

- None

Internal Fixes
--------------

- ``pyproject.toml`` is now the source of package information.
- ``ruff`` has been widely deployed to fix any underlying issues found.
- Internal process rewritten to follow modern sphinx.
- Increaseed pytest coverage

Breaking Changes
----------------

- Dropped support for Python 3.9
- Dropped support for Sphinx 5
- Removed non-ablog scoped templates
- Removed the myriad of language config options
